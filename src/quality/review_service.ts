import { spawnSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { lstatSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';
import type { TaskLedger } from '../harness/task_ledger.ts';
import { ReceiptIndex, readBoundFile } from '../artifacts/receipt_index.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';
import { createReviewRequest, evaluateReview, reviewRequestHash, validateCriteria } from './review_contract.ts';
import type { Assessment, ReviewCriteria, ReviewRequest, ReviewerIdentity, ReviewSubject } from './review_contract.ts';

export type ReviewerCommand = { id:string; version:string; executable:string; script:string; tools:Record<string,string> };
export type TrustedReviewContext = { requestSha256:string; reviewer:ReviewerIdentity; contextId:string;
  independence:'host'|'manual'; observedFiles:Record<string,string> };
export type ContextVerifier = (opaqueRef:string)=>TrustedReviewContext|null;
/** 评审者身份绑定实际程序、解释器与工具字节；路径只用于本机执行。 */
export function reviewerIdentity(command:ReviewerCommand):ReviewerIdentity {
  check(typeof command.id==='string'&&typeof command.version==='string'&&isObject(command.tools)
    &&Object.keys(command.tools).every(key=>['native','ffmpeg','ffprobe'].includes(key)),'invalid_reviewer_command');
  const files={executable:command.executable,script:command.script,...Object.fromEntries(Object.entries(command.tools).map(([key,value])=>['tool:'+key,value]))};
  const digests=Object.fromEntries(Object.entries(files).map(([name,path])=>{
    const canonical=realpathSync(path);check(lstatSync(canonical).isFile(),'invalid_reviewer_command');return [name,sha256(readFileSync(canonical))];
  }));
  return {id:command.id,kind:'external',version:command.version,implementationSha256:sha256(stableJson(digests))};
}

/** 当前同尝试交付的质量证据 CAS；不改任务状态，不把评审变成第二操作账本。 */
export class ReviewService {
  ledger:TaskLedger;
  index:ReceiptIndex;
  store:string;
  constructor(ledger:TaskLedger,index:ReceiptIndex,store:string){
    this.ledger=ledger;this.index=index;this.store=store;
    mkdirSync(store,{recursive:true,mode:0o700});
    const info=lstatSync(store);check(info.isDirectory()&&!info.isSymbolicLink()&&(info.mode&0o077)===0
      &&(process.getuid===undefined||info.uid===process.getuid()),'review_store_unsafe');
  }
  private put(value:unknown){
    const bytes=stableJson(value)+'\n';check(Buffer.byteLength(bytes)<=16*1024*1024,'review_record_too_large');
    const digest=sha256(bytes),path=join(this.store,digest);
    try{writeFileSync(path,bytes,{flag:'wx',mode:0o600});}
    catch(error:any){if(error.code!=='EEXIST'){throw error;}check(sha256(readBoundFile(this.store,digest))===digest,'review_record_conflict');}
    return digest;
  }
  private get(digest:string){
    check(isHash(digest),'invalid_review_digest');const bytes=readBoundFile(this.store,digest);
    check(sha256(bytes)===digest,'review_record_conflict');return parseJson(bytes.toString('utf8'));
  }
  capture(taskId:string):ReviewSubject {
    const task=this.ledger.getTask(taskId);
    check(task.state==='verifying'&&task.attemptId,'review_source_unconfirmed');
    const collection=this.index.collect(taskId,task.attemptId);
    check(collection.status==='linked'&&collection.outputRefs.length>0,'review_source_unconfirmed');
    const files=Object.fromEntries(collection.outputRefs.map(file=>[file.location,{sha256:file.sha256,bytes:file.bytes}]));
    check(isHash(files['project.fcproj']?.sha256),'review_source_unconfirmed');
    const attempt=this.ledger.verifyAttempt(taskId,task.attemptId);
    return {taskId,attemptId:task.attemptId,epoch:task.epoch,bindingSha256:sha256(stableJson(task.binding)),
      candidateSha256:sha256(stableJson(files)),projectSha256:files['project.fcproj'].sha256,inputHashes:{...task.binding.inputHashes},
      executionSha256:sha256(stableJson({attempt,runtime:task.binding.runtimeIdentity,sourceRevision:task.binding.sourceRevision,sourceTreeSha256:task.binding.sourceTreeSha256})),files};
  }
  create(taskId:string,criteria:ReviewCriteria){
    const request=createReviewRequest(this.capture(taskId),criteria);
    return {requestRef:this.put(request),request};
  }
  private current(request:ReviewRequest,criteria:ReviewCriteria){
    validateCriteria(criteria);reviewRequestHash(request);
    check(stableJson(request.criteria)===stableJson(criteria),'review_evidence_stale');
    check(stableJson(this.capture(request.subject.taskId))===stableJson(request.subject),'review_evidence_stale');
  }
  /** 宿主/人工评审只接受可信核验器返回的独立上下文，拒绝回执自行声明 freshContext。 */
  importIndependent(requestRef:string,assessment:Assessment,opaqueRef:string,verify?:ContextVerifier){
    const request=this.get(requestRef) as ReviewRequest;this.current(request,request.criteria);
    check(typeof verify==='function','review_context_verifier_required');const context=verify(opaqueRef);
    check(context&&['host','manual'].includes(context.independence)&&context.independence===request.criteria.reviewer.kind
      &&context.requestSha256===reviewRequestHash(request)&&stableJson(context.reviewer)===stableJson(request.criteria.reviewer)
      &&typeof context.contextId==='string'&&context.contextId.length>0&&context.contextId!==request.subject.attemptId
      &&isObject(context.observedFiles)&&Object.entries(request.subject.files).every(([name,file])=>context.observedFiles[name]===file.sha256),'review_context_unconfirmed');
    evaluateReview(request,assessment);
    this.current(request,request.criteria);
    return {receiptRef:this.put({schema:'filmcraft-review-receipt/v1',requestRef,requestSha256:reviewRequestHash(request),
      reviewer:request.criteria.reviewer,assessment,context:{...context,source:'trusted-host-verifier'}})};
  }
  /** 新进程只接收冻结作品和最小请求；没有继承生成器环境、对话或自评字段。 */
  runExternal(requestRef:string,command:ReviewerCommand){
    const request=this.get(requestRef) as ReviewRequest;this.current(request,request.criteria);
    const identity=reviewerIdentity(command);
    check(stableJson(identity)===stableJson(request.criteria.reviewer),'reviewer_identity_mismatch');
    if(command.tools.native){check(sha256(readFileSync(realpathSync(command.tools.native)))===this.ledger.getTask(request.subject.taskId).binding.runtimeIdentity.sha256,'reviewer_native_identity_mismatch');}
    const directory=realpathSync(mkdtempSync(join(tmpdir(),'filmcraft-review-'))),artifacts=join(directory,'artifacts');
    mkdirSync(artifacts,{mode:0o700});
    try{
      const task=this.ledger.getTask(request.subject.taskId),exposed:Record<string,string>={};let bytes=0;
      const inputHashes=new Set(Object.values(request.subject.inputHashes));
      for(const [name,file] of Object.entries(request.subject.files)){
        if(!['film.mp4','project.fcproj','captions.srt'].includes(name)&&!inputHashes.has(file.sha256)){continue;}
        check(!['plan.json','operations.json','capabilities.json','manifest.json'].includes(name),'generator_context_rejected');
        bytes+=file.bytes;check(bytes<=256*1024*1024,'review_context_limit');
        const content=readBoundFile(task.binding.outputRoot,name,256*1024*1024);
        check(sha256(content)===file.sha256,'review_evidence_stale');
        const path=join(artifacts,name);mkdirSync(dirname(path),{recursive:true,mode:0o700});writeFileSync(path,content,{flag:'wx',mode:0o400});
        exposed[name]=file.sha256;
      }
      const requestFile=join(directory,'request.json'),toolsFile=join(directory,'tools.json');
      writeFileSync(requestFile,stableJson(request)+'\n',{mode:0o400});
      const tools=Object.fromEntries(Object.entries(command.tools).map(([key,value])=>[key,realpathSync(value)]));
      writeFileSync(toolsFile,stableJson(tools)+'\n',{mode:0o400});
      check(stableJson(reviewerIdentity(command))===stableJson(identity),'reviewer_identity_mismatch');
      const result=spawnSync(realpathSync(command.executable),['-I','-B',realpathSync(command.script),'--request',requestFile,'--artifacts',artifacts,'--tools',toolsFile],
        {cwd:directory,env:{PATH:'/usr/bin:/bin',HOME:directory,TMPDIR:directory,LANG:'C.UTF-8'},encoding:'utf8',shell:false,timeout:90_000,maxBuffer:8*1024*1024});
      check(!result.error&&result.status===0,'reviewer_execution_failed');
      check(stableJson(reviewerIdentity(command))===stableJson(identity),'reviewer_identity_mismatch');
      check(readFileSync(requestFile,'utf8')===stableJson(request)+'\n','review_context_changed');
      for(const [name,digest] of Object.entries(exposed)){check(sha256(readBoundFile(artifacts,name,256*1024*1024))===digest,'review_context_changed');}
      const wire=parseJson(result.stdout);
      check(isObject(wire)&&Object.keys(wire).sort().join(',')==='assessment,requestSha256,schema'
        &&wire.schema==='filmcraft-review-assessment/v1'&&wire.requestSha256===reviewRequestHash(request),'review_response_mismatch');
      const evaluation=evaluateReview(request,wire.assessment);
      this.current(request,request.criteria);
      const receipt={schema:'filmcraft-review-receipt/v1',requestRef,requestSha256:reviewRequestHash(request),reviewer:identity,assessment:wire.assessment,
        context:{source:'external-process',contextId:randomUUID(),pid:result.pid,exitCode:result.status,
          workingDirectory:'fresh-private',environmentKeys:['PATH','HOME','TMPDIR','LANG'],exposedFiles:exposed,
          responseSha256:sha256(result.stdout),stderrSha256:sha256(result.stderr),implementationSha256:identity.implementationSha256}};
      return {receiptRef:this.put(receipt),evaluation};
    }finally{rmSync(directory,{recursive:true,force:true});}
  }
  readCurrent(requestRef:string,receiptRef:string,criteria:ReviewCriteria){
    const request=this.get(requestRef) as ReviewRequest;this.current(request,criteria);
    const receipt=this.get(receiptRef);
    check(receipt.schema==='filmcraft-review-receipt/v1'&&receipt.requestRef===requestRef&&receipt.requestSha256===reviewRequestHash(request)
      &&stableJson(receipt.reviewer)===stableJson(criteria.reviewer)
      &&['external-process','trusted-host-verifier'].includes(receipt.context?.source),'review_response_mismatch');
    return evaluateReview(request,receipt.assessment);
  }
  /** 循环需要明确核验质量证据所属任务；返回当前请求而不提升任务状态。 */
  readRequest(requestRef:string,criteria:ReviewCriteria){
    const request=this.get(requestRef) as ReviewRequest;this.current(request,criteria);return request;
  }
}
