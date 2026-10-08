import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { RevisionService, revisionAuthorizationSubject } from '../../src/quality/revision_service.ts';
import { ReviewService, reviewerIdentity } from '../../src/quality/review_service.ts';
import { PythonWorkflowRunner } from '../../src/adapters/python_workflow.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { assertRevisionDiff } from '../../src/quality/native_revision_scope.ts';
import { captureEvidence } from './fixtures.ts';

/** 真实固定原生执行、工程差异、独立重评、停止与最佳候选保全；不是创作/用户接受。 */
export async function nativeRevisionFixture(context:any){
  const {root,db,index,options,task,planFile,grant,writeGrant,localAuthorizer}=context;
  const tools={...JSON.parse(process.env.FILMCRAFT_QUALITY_TOOLS!),native:join(options.runtimeHome,'filmcraft',task.runtimeIdentity.cliVersion,'filmcraft-cli')};
  const command={id:'filmcraft-independent-media',version:'1',executable:options.python,
    script:new URL('../../scripts/review_media.py',import.meta.url).pathname,tools};
  const quality=new ReviewService(db,index,join(root,'revision-quality'));
  const service=new RevisionService(db,quality,{authorize:localAuthorizer});
  function policy(task:any,expected:number,reverse=false){
    const snapshot=service.project(task.taskId),items=snapshot.project.project.items;
    const sequence=Object.values(items).find((item:any)=>item.kind?.Sequence) as any;
    const track=sequence.kind.Sequence.video_tracks.find((track:any)=>track.items.length),clip=track.items[0];
    const timeIndex=clip.effects.findIndex((effect:any)=>effect.effect==='time_remap');
    const scope={ownerPlugin:'filmcraft',sequenceId:String(sequence.id),trackId:String(track.id),objectId:String(clip.id),
      startTick:'0',endTick:String(clip.duration),fields:['/speed','/reverse','/duration',`/effects/${timeIndex}/params/speed/value/Float`],dependencies:['still']};
    const criteria={goal:{text:reverse?'Reverse the still while preserving duration':'Double playback speed and halve duration',
      constraints:['Preserve every other track and dependency'],audioRequired:false,expectedDurationMs:expected},
      rubric:{id:'native-scoped-revision',version:'1',required:['decode','videoTiming'],thresholds:{syncToleranceMs:50,clippingAmplitude:.999,clippingFraction:.001}},
      reviewer:reviewerIdentity(command)};
    return {criteria,scopes:[scope],issues:[{id:reverse?'reverse-still':'double-speed',target:[scope.sequenceId,scope.trackId,scope.objectId].join('/'),
      command:'clip.speedDuration',params:{speed:reverse?100:200,reverse,ripple:false}}],limits:{maxRounds:2,maxFailures:1,maxStagnant:1,minImprovement:0}};
  }
  function open(task:any,value:any){
    const request=quality.create(task.taskId,value.criteria),review=quality.runExternal(request.requestRef,command);
    const baseline={taskId:task.taskId,requestRef:request.requestRef,receiptRef:review.receiptRef};
    const definition={rootTaskId:task.taskId,policy:value,baseline,authorizationRef:task.authorizationRef,authorizationScopeSha256:task.authorizationScopeSha256};
    grant.subjects.push(sha256(stableJson(revisionAuthorizationSubject(definition))));writeGrant();
    return {opened:service.open(task.taskId,value,baseline),baseline};
  }
  const sourceProject=sha256(readFileSync(join(task.outputRoot,'project.fcproj'))),value=policy(task,500),first=open(task,value);
  assert.equal(first.opened.best,null,'wrong source duration cannot become the verified best');
  const revised=await service.execute(first.opened.loopId,task.taskId,'quality-revision-1',join(root,'quality-revision-1'),options,command);
  assert.equal(revised.reason,'issues_resolved');assert.equal(revised.best.taskId,'quality-revision-1');
  assert.equal(revised.userAcceptance,'NOT_RUN');assert.equal(revised.creativeAcceptance,'manual_review');
  assert.equal(sha256(readFileSync(join(task.outputRoot,'project.fcproj'))),sourceProject);
  assert.equal(db.listAttempts('quality-revision-1').length,1);
  const reused=await service.execute(first.opened.loopId,task.taskId,'quality-revision-1',join(root,'quality-revision-1'),options,command);
  assert.equal(reused.best.projectSha256,revised.best.projectSha256);assert.equal(db.listAttempts('quality-revision-1').length,1);
  assert.throws(()=>quality.readCurrent(revised.best.requestRef,first.baseline.receiptRef,value.criteria),/review_response_mismatch/);
  const intents=db.db.prepare('SELECT * FROM revision_rounds WHERE loop_id=?').all(first.opened.loopId);
  const diff=assertRevisionDiff(JSON.parse(intents[0].intent).compiled,service.project('quality-revision-1'));
  const authorizationRefReused=db.getTask('quality-revision-1').binding.authorizationRef===task.authorizationRef;
  assert.ok(authorizationRefReused);
  captureEvidence('actual-native-scoped-revision','actual native save/reopen, complete semantic diff, independent current review and repeated-call no replay',
    {loop:revised,rounds:intents,diff,authorizationRefReused,sourceProjectPreserved:true,sourceProjectSha256:sourceProject,candidateProjectSha256:revised.best.projectSha256,
      sourceAttempts:db.listAttempts(task.taskId).length,candidateAttempts:db.listAttempts('quality-revision-1').length,oldReviewRejected:true});
  // 另一个真实来源额度为0；拒绝首次修订，同时保留明确未解决问题与已验证来源。
  const output=join(root,'quality-budget-source'),restricted={...options,resources:{...options.resources,limits:{...options.resources.limits,revisions:0}}};
  const runner=new PythonWorkflowRunner(db,index,restricted),prepared=runner.prepare(planFile,output);
  const budgetTask={...task,taskId:'quality-budget-source',idempotencyKey:'quality-budget-source',outputRoot:output,projectKey:prepared.projectKey};
  const made=await runner.run(budgetTask,planFile);assert.equal(made.state,'verifying');
  const original=sha256(readFileSync(join(output,'project.fcproj'))),budgetPolicy=policy(budgetTask,1000,true),budget=open(budgetTask,budgetPolicy);
  assert.equal(budget.opened.best.taskId,budgetTask.taskId);
  await assert.rejects(service.execute(budget.opened.loopId,budgetTask.taskId,'quality-over-budget',join(root,'quality-over-budget'),restricted,command),/budget_revisions_exceeded/);
  const stopped=service.snapshot(budget.opened.loopId);
  assert.equal(stopped.reason,'budget_revisions_exceeded');assert.equal(stopped.best.taskId,budgetTask.taskId);
  assert.equal(db.listAttempts('quality-over-budget').length,0);assert.equal(sha256(readFileSync(join(output,'project.fcproj'))),original);
  assert.deepEqual(stopped.unresolvedIssues,['reverse-still']);
  captureEvidence('actual-native-revision-budget-best','actual pinned native source and independent review; durable zero revision budget rejects before attempt',
    {loop:stopped,sourceProjectPreserved:true,attempts:0,bestProjectSha256:original,authorizationRefReused:true});
}
