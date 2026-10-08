import { requirePermissions, requireRead, requireWrite } from '../support/execution_permissions.ts';
import { randomUUID } from 'node:crypto';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import type { TaskLedger, Binding } from '../harness/task_ledger.ts';
import { requireAuthorization } from '../harness/authorization.ts';
import type { Authorizer } from '../harness/authorization.ts';
import { ResourceController, outputBytes } from '../harness/resources.ts';
import { PythonWorkflowRunner } from '../adapters/python_workflow.ts';
import type { WorkflowOptions } from '../adapters/python_workflow.ts';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { canonicalTarget } from '../support/paths.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';
import { ReviewService } from './review_service.ts';
import type { ReviewerCommand } from './review_service.ts';
import { validateCriteria } from './review_contract.ts';
import type { ReviewCriteria } from './review_contract.ts';
import { appliedIssueIds, assertRevisionDiff, compileRevision, nativeSnapshot } from './native_revision_scope.ts';
import type { RevisionIssue, RevisionScope, CompiledRevision } from './native_revision_scope.ts';
import { verifyRevisionIntegrity } from './revision_schema.ts';

export type CandidateReview={taskId:string;requestRef:string;receiptRef:string};
export type RevisionPolicy={criteria:ReviewCriteria;scopes:RevisionScope[];issues:RevisionIssue[];
  limits:{maxRounds:number;maxFailures:number;maxStagnant:number;minImprovement:number}};
type Definition={rootTaskId:string;policy:RevisionPolicy;baseline:CandidateReview;
  authorizationRef:string;authorizationScopeSha256:string};
/** 原范围内的所有轮次复用同一授权主题；新目标/字段/依赖/限额不能暗中扩展。 */
export function revisionAuthorizationSubject(definition:Definition){
  return {action:'continue' as const,identitySha256:sha256(stableJson(definition))};
}
function validPolicy(value:RevisionPolicy){
  check(isObject(value)&&Object.keys(value).sort().join(',')==='criteria,issues,limits,scopes','revision_policy_invalid');
  validateCriteria(value.criteria);const limits=value.limits;
  check(isObject(limits)&&Object.keys(limits).sort().join(',')==='maxFailures,maxRounds,maxStagnant,minImprovement'
    &&[limits.maxRounds,limits.maxFailures,limits.maxStagnant].every(item=>Number.isSafeInteger(item)&&item>0&&item<=100)
    &&Number.isFinite(limits.minImprovement)&&limits.minImprovement>=0&&limits.minImprovement<=1000,'revision_policy_invalid');
}
function overlaps(left:string,right:string){const path=relative(left,right);return path===''||(!path.startsWith('..'+ '/')&&path!=='..'&&!path.startsWith('/'));}

/** 修订协调器使用唯一SQL账本和现有原生执行器；不知道的结果永不重放。 */
export class RevisionService{
  ledger:TaskLedger;quality:ReviewService;authorize?:Authorizer;
  constructor(ledger:TaskLedger,quality:ReviewService,options:{authorize?:Authorizer}={}){
    check(quality.ledger===ledger,'revision_ledger_mismatch');this.ledger=ledger;this.quality=quality;this.authorize=options.authorize;
  }
  private row(loopId:string){
    verifyRevisionIntegrity(this.ledger.db);
    const row=this.ledger.db.prepare('SELECT * FROM revision_loops WHERE loop_id=?').get(loopId) as any;
    check(row,'revision_loop_missing');const definition=parseJson(row.definition) as Definition;validPolicy(definition.policy);
    const root=this.ledger.getTask(definition.rootTaskId);
    check(root.binding.authorizationRef===definition.authorizationRef&&root.binding.authorizationScopeSha256===definition.authorizationScopeSha256,'revision_policy_invalid');
    return {...row,definition};
  }
  private permitted(definition:Definition){return requireAuthorization(this.authorize,definition,revisionAuthorizationSubject(definition));}
  project(taskId:string){
    const subject=this.quality.capture(taskId),task=this.ledger.getTask(taskId);
    const bytes=readBoundFile(task.binding.outputRoot,'project.fcproj',64*1024*1024);
    check(sha256(bytes)===subject.projectSha256,'revision_source_stale');
    const manifest=parseJson(readBoundFile(task.binding.outputRoot,'manifest.json').toString('utf8'));
    const snapshot=nativeSnapshot(bytes,task.binding.outputRoot,manifest.assets);
    check(stableJson(snapshot.dependencyHashes)===stableJson(subject.inputHashes)
      &&stableJson(subject)===stableJson(this.quality.capture(taskId)),'revision_source_stale');return snapshot;
  }
  private candidate(reference:CandidateReview,definition:Definition,compiled?:CompiledRevision){
    check(isObject(reference)&&isHash(reference.requestRef)&&isHash(reference.receiptRef),'revision_review_invalid');
    const request=this.quality.readRequest(reference.requestRef,definition.policy.criteria);
    check(request.subject.taskId===reference.taskId,'revision_review_invalid');
    const result=this.quality.readCurrent(reference.requestRef,reference.receiptRef,definition.policy.criteria);
    const project=this.project(reference.taskId),scope=compiled?assertRevisionDiff(compiled,project):null;
    const applied=appliedIssueIds(project,definition.policy.scopes,definition.policy.issues),required=definition.policy.criteria.rubric.required;
    const eligible=result.engineeringAcceptance==='PASS'&&result.technicalAcceptance==='PASS'
      &&required.every(name=>result.dimensions[name].status==='PASS');
    const score=required.filter(name=>result.dimensions[name].status==='PASS').length*10+applied.length+(result.creativeScore??0)/10;
    return {reference,result,scope,applied,eligible,score,projectSha256:project.sourceSha256};
  }
  open(rootTaskId:string,policy:RevisionPolicy,baseline:CandidateReview){
    validPolicy(policy);check(baseline.taskId===rootTaskId,'revision_review_invalid');
    const root=this.ledger.getTask(rootTaskId),definition:Definition={rootTaskId,policy,baseline,
      authorizationRef:root.binding.authorizationRef,authorizationScopeSha256:root.binding.authorizationScopeSha256};
    this.permitted(definition);this.candidate(baseline,definition);
    const source=this.project(rootTaskId);compileRevision(source,source.sourceSha256,policy.scopes,policy.issues,policy.criteria.goal.audioRequired);
    new ResourceController(this.ledger).snapshot(rootTaskId);
    const encoded=stableJson(definition),digest=sha256(encoded);
    const loopId=this.ledger.transaction(()=>{
      this.permitted(definition);
      const old=this.ledger.db.prepare('SELECT * FROM revision_loops WHERE root_task_id=?').get(rootTaskId) as any;
      if(old){check(old.policy_sha256===digest&&old.definition===encoded,'revision_policy_conflict');return old.loop_id;}
      const id=randomUUID();this.ledger.db.prepare('INSERT INTO revision_loops VALUES(?,?,?,?,?,?,?,?)')
        .run(id,rootTaskId,digest,encoded,'active',null,1,Date.now());return id;
    });
    this.refreshStop(loopId);return this.snapshot(loopId);
  }
  /** 宿主收到目标或rubric变更时先失效旧循环；保留审计，不重置轮数或沿用旧最佳。 */
  invalidateCriteria(loopId:string,current:ReviewCriteria){
    validateCriteria(current);const row=this.row(loopId);this.permitted(row.definition);
    if(stableJson(current)!==stableJson(row.definition.policy.criteria)){
      this.ledger.db.prepare("UPDATE revision_loops SET state='stopped',reason='criteria_changed',generation=generation+1 WHERE loop_id=? AND reason IS NOT 'criteria_changed'").run(loopId);
    }
    return this.snapshot(loopId);
  }
  snapshot(loopId:string){
    const row=this.row(loopId),definition=row.definition as Definition;
    const rounds=this.ledger.db.prepare('SELECT * FROM revision_rounds WHERE loop_id=? ORDER BY round_no').all(loopId) as any[];
    let best:any=null,bestScore=-Infinity,progress=-Infinity,stagnant=0,failures=0,latest:any=null;
    const invalidEvidence:{taskId:string;reason:string}[]=[];
    const observe=(reference:CandidateReview,compiled?:CompiledRevision)=>{
      try{
        const value=this.candidate(reference,definition,compiled);latest=value;
        if(value.eligible&&value.score>bestScore){best={...reference,projectSha256:value.projectSha256,score:value.score,scope:'engineering and every required loop rubric dimension; not user acceptance'};bestScore=value.score;}
        return value;
      }catch(error:any){invalidEvidence.push({taskId:reference.taskId,reason:error.code??'revision_evidence_unavailable'});return null;}
    };
    const initial=observe(definition.baseline);progress=initial?.score??-Infinity;
    for(const round of rounds){
      if(['pending','unknown'].includes(round.state)){continue;}
      if(round.state!=='reviewed'){failures++;stagnant++;continue;}
      const result=parseJson(round.result),intent=parseJson(round.intent),value=observe(result.review,intent.compiled);
      if(!value||value.result.decision==='blocked'){failures++;}
      if(value&&value.score>progress+definition.policy.limits.minImprovement){progress=value.score;stagnant=0;}else{stagnant++;}
    }
    if(row.reason==='criteria_changed'){best=null;latest=null;invalidEvidence.push({taskId:definition.rootTaskId,reason:'revision_criteria_changed'});}
    const unresolved=definition.policy.issues.filter(issue=>!latest?.applied.includes(issue.id)).map(issue=>issue.id);
    const missing=latest?definition.policy.criteria.rubric.required.filter(name=>latest.result.dimensions[name].status!=='PASS')
      :definition.policy.criteria.rubric.required;
    const budget=new ResourceController(this.ledger).snapshot(definition.rootTaskId);
    return {loopId,rootTaskId:definition.rootTaskId,state:row.state,reason:row.reason,generation:row.generation,
      rounds:rounds.length,failures,stagnant,pending:rounds.find(round=>['pending','unknown'].includes(round.state))?.child_task_id??null,
      best,latestEligible:latest?.eligible??false,unresolvedIssues:unresolved,unresolvedQuality:missing,invalidEvidence,budget,
      creativeAcceptance:latest?.result.creativeAcceptance??'NOT_RUN',userAcceptance:'NOT_RUN'};
  }
  private refreshStop(loopId:string){
    const row=this.row(loopId),view=this.snapshot(loopId),limits=row.definition.policy.limits;
    if(row.state==='stopped'){return view;}
    let reason:string|null=view.budget.state!=='active'?(view.budget.reason??'budget_stopped'):null;
    if(!view.pending){
      reason??=view.latestEligible&&view.unresolvedIssues.length===0?'issues_resolved'
        :view.failures>=limits.maxFailures?'failure_limit':view.stagnant>=limits.maxStagnant?'stagnation_limit'
        :view.rounds>=limits.maxRounds?'round_limit':null;
    }
    if(reason){this.ledger.db.prepare("UPDATE revision_loops SET state='stopped',reason=?,generation=generation+1 WHERE loop_id=? AND state='active'").run(reason,loopId);}
    return this.snapshot(loopId);
  }
  private finish(loopId:string,childId:string,state:'reviewed'|'rejected'|'failed',result:unknown){
    const encoded=stableJson(result);this.ledger.transaction(()=>{
      const round=this.ledger.db.prepare('SELECT * FROM revision_rounds WHERE loop_id=? AND child_task_id=?').get(loopId,childId) as any;
      check(round,'revision_round_missing');
      if(!['pending','unknown'].includes(round.state)){check(round.state===state&&round.result===encoded,'revision_result_conflict');return;}
      this.ledger.db.prepare('UPDATE revision_rounds SET state=?,result=?,result_sha256=? WHERE loop_id=? AND child_task_id=?')
        .run(state,encoded,sha256(encoded),loopId,childId);
      this.ledger.db.prepare('UPDATE revision_loops SET generation=generation+1 WHERE loop_id=?').run(loopId);
      if(state==='rejected'){this.ledger.db.prepare("UPDATE revision_loops SET state='stopped',reason='scope_violation' WHERE loop_id=?").run(loopId);}
    });return this.refreshStop(loopId);
  }
  /** 已停止/失败后不新建依赖；未知轮次仅观察，可在独立恢复后重新验证而不重放原生。 */
  observe(loopId:string,childId:string,reviewer?:ReviewerCommand|CandidateReview){
    const row=this.row(loopId),round=this.ledger.db.prepare('SELECT * FROM revision_rounds WHERE loop_id=? AND child_task_id=?').get(loopId,childId) as any;
    check(round,'revision_round_missing');if(!['pending','unknown'].includes(round.state)){return this.snapshot(loopId);}
    const task=this.ledger.getTask(childId),intent=parseJson(round.intent);
    if(task.state==='failed'||task.state==='cancelled'){return this.finish(loopId,childId,'failed',{state:task.state});}
    if(task.state!=='verifying'){
      if(task.attemptId){this.ledger.db.prepare("UPDATE revision_rounds SET state='unknown' WHERE loop_id=? AND child_task_id=?").run(loopId,childId);}
      return this.snapshot(loopId);
    }
    try{assertRevisionDiff(intent.compiled,this.project(childId));}
    catch(error:any){return this.finish(loopId,childId,'rejected',{reason:error.code??'revision_scope_unconfirmed'});}
    if(!reviewer){return this.snapshot(loopId);}
    let review:CandidateReview;
    if('requestRef' in reviewer){check(reviewer.taskId===childId,'revision_review_invalid');review=reviewer;}
    else{
      const created=this.quality.create(childId,row.definition.policy.criteria);
      const assessed=this.quality.runExternal(created.requestRef,reviewer);
      review={taskId:childId,requestRef:created.requestRef,receiptRef:assessed.receiptRef};
    }
    this.candidate(review,row.definition,intent.compiled);
    return this.finish(loopId,childId,'reviewed',{review});
  }
  /** 每轮先原子登记新任务/意图，再复用共享预算执行；只首次提交，从不自动重试未知。 */
  async execute(loopId:string,sourceTaskId:string,childId:string,outputRoot:string,options:WorkflowOptions,reviewer?:ReviewerCommand){
    let row=this.row(loopId);this.permitted(row.definition);
    const old=this.ledger.db.prepare('SELECT * FROM revision_rounds WHERE loop_id=? AND child_task_id=?').get(loopId,childId) as any;
    if(old){
      const intent=parseJson(old.intent);check(intent.sourceTaskId===sourceTaskId&&intent.child.outputRoot===canonicalTarget(outputRoot),'revision_intent_conflict');
      // 原生只要有尝试记录就不再次调用执行器；恢复由独立RecoveryService处理。
      if(this.ledger.getTask(childId).attemptId||!['pending','unknown'].includes(old.state)){return this.observe(loopId,childId,reviewer);}
    }else{
      const current=this.refreshStop(loopId);check(current.state==='active','revision_loop_stopped');check(!current.pending,'revision_round_pending');
    }
    row=this.row(loopId);const definition=row.definition as Definition,root=this.ledger.getTask(definition.rootTaskId);
    const allowedSources=[definition.rootTaskId,...this.ledger.db.prepare("SELECT child_task_id FROM revision_rounds WHERE loop_id=? AND state='reviewed'").all(loopId).map((value:any)=>value.child_task_id)];
    check(allowedSources.includes(sourceTaskId),'revision_source_outside_loop');
    const permissions=requirePermissions(options.permissions);
    check(root.binding.executionPermissionsSha256===sha256(stableJson(permissions)),'permission_identity_conflict');
    requireRead(root.binding.outputRoot,permissions);requireRead(this.ledger.getTask(sourceTaskId).binding.outputRoot,permissions);
    requireWrite(outputRoot,permissions);
    const source=this.project(sourceTaskId),compiled=compileRevision(source,source.sourceSha256,definition.policy.scopes,definition.policy.issues,definition.policy.criteria.goal.audioRequired);
    outputRoot=canonicalTarget(outputRoot);
    for(const id of allowedSources){const path=this.ledger.getTask(id).binding.outputRoot;check(!overlaps(path,outputRoot)&&!overlaps(outputRoot,path),'revision_output_overlaps');}
    const planBytes=stableJson(compiled.plan)+'\n',planRoot=join(this.quality.store,'revision-plans');requireWrite(planRoot,permissions);mkdirSync(planRoot,{recursive:true,mode:0o700});
    const planName=sha256(planBytes),planFile=join(planRoot,planName);
    if(!existsSync(planFile)){writeFileSync(planFile,planBytes,{flag:'wx',mode:0o400});}
    check(readBoundFile(planRoot,planName).toString('utf8')===planBytes,'revision_plan_conflict');
    const runner=new PythonWorkflowRunner(this.ledger,this.quality.index,options),prepared=runner.prepare(planFile,outputRoot,this.ledger.getTask(sourceTaskId).binding.outputRoot);
    check(options.sourceRevision===root.binding.sourceRevision&&prepared.sourceTreeSha256===root.binding.sourceTreeSha256
      &&prepared.runtimeIdentity.sha256===root.binding.runtimeIdentity.sha256&&prepared.runtimeIdentity.mode===root.binding.runtimeIdentity.mode
      &&prepared.runtimeIdentity.pluginVersion===root.binding.runtimeIdentity.pluginVersion
      &&stableJson(prepared.inputHashes)===stableJson(root.binding.inputHashes),'revision_execution_scope_change');
    const child:Binding={...root.binding,taskId:childId,idempotencyKey:'revision:'+loopId+':'+childId,outputRoot,
      projectKey:prepared.projectKey,projectRevision:source.sourceSha256,planHash:prepared.planIdentity.canonicalPlanSha256,
      nativePlanHash:prepared.planIdentity.workflowPlanSha256,runtimeIdentity:prepared.runtimeIdentity};
    const parent=this.ledger.getTask(sourceTaskId),sourceIdentity=this.quality.capture(sourceTaskId);
    const admission=this.ledger.beginContinuation(sourceTaskId,parent.epoch,sha256(stableJson(sourceIdentity)),child,(intentId)=>{
      this.permitted(definition);const current=this.snapshot(loopId),fresh=this.row(loopId);
      const existing=this.ledger.db.prepare('SELECT * FROM revision_rounds WHERE loop_id=? AND child_task_id=?').get(loopId,childId) as any;
      if(existing){check(parseJson(existing.intent).child.taskId===childId&&existing.intent_sha256===sha256(existing.intent),'revision_intent_conflict');return;}
      check(fresh.state==='active'&&!current.pending&&current.rounds<definition.policy.limits.maxRounds
        &&current.failures<definition.policy.limits.maxFailures&&current.stagnant<definition.policy.limits.maxStagnant,'revision_loop_stopped');
      check(stableJson(sourceIdentity)===stableJson(this.quality.capture(sourceTaskId)),'revision_source_stale');
      const intent=stableJson({child,sourceTaskId,compiled,planFileSha256:planName,generation:fresh.generation+1,continuationIntentId:intentId});
      check(Buffer.byteLength(intent)<=8*1024*1024,'revision_plan_too_large');
      this.ledger.db.prepare('INSERT INTO revision_rounds VALUES(?,?,?,?,?,?,?,?)').run(loopId,current.rounds+1,childId,sha256(intent),intent,'pending',null,null);
      this.ledger.db.prepare('UPDATE revision_loops SET generation=generation+1 WHERE loop_id=?').run(loopId);
    });
    const pending=this.ledger.db.prepare('SELECT intent FROM revision_rounds WHERE loop_id=? AND child_task_id=?').get(loopId,childId) as any;
    const intent=parseJson(pending.intent),resources=new ResourceController(this.ledger);
    resources.settle(definition.rootTaskId,{stopped:true,outputBytes:outputBytes(root.binding.outputRoot)});
    const rootReservation=resources.snapshot(definition.rootTaskId).reservations.find(value=>value.task_id===definition.rootTaskId)!;
    const dispatch=()=>{
      this.permitted(definition);const fresh=this.row(loopId);check(fresh.state==='active'&&fresh.generation===intent.generation,'revision_dispatch_fenced');
      check(this.project(sourceTaskId).sourceSha256===source.sourceSha256,'revision_source_stale');
    };
    const controlled=new PythonWorkflowRunner(this.ledger,this.quality.index,{...options,beforeDispatch:()=>{options.beforeDispatch?.();dispatch();},
      resources:{allocation:{...parseJson(rootReservation.allocation),revisions:1}},budgetParentId:definition.rootTaskId});
    try{await controlled.run(child,planFile,parent.binding.outputRoot);}
    catch(error:any){
      if(this.ledger.getTask(childId).attemptId){
        // 即使回复丢失也保留待核验轮次；后续只能独立修复/观察。
        this.ledger.db.prepare("UPDATE revision_rounds SET state='unknown' WHERE loop_id=? AND child_task_id=?").run(loopId,childId);throw error;
      }
      if(error.code==='budget_concurrency_exceeded'){return this.snapshot(loopId);}
      this.finish(loopId,childId,'failed',{reason:error.code??'revision_dispatch_failed'});throw error;
    }
    this.ledger.observeContinuation(admission.intentId);return this.observe(loopId,childId,reviewer);
  }
}
