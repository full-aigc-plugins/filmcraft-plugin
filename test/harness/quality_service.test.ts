import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { normalizePlan } from '../../src/adapters/plan_identity.ts';
import { ReviewService, reviewerIdentity } from '../../src/quality/review_service.ts';
import { reviewRequestHash } from '../../src/quality/review_contract.ts';
import type { ReviewCriteria, Assessment } from '../../src/quality/review_contract.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { binding, hash, workspace } from './fixtures.ts';

// 此 fixture 只证明 SQL/回执/隔离/失效规则，不声称合成字节是原生工程或视频。
function setup(t:Parameters<typeof workspace>[0]) {
  const root=workspace(t),output=join(root,'delivery');mkdirSync(output);mkdirSync(join(output,'assets'));
  const media=Buffer.from('synthetic input; not real media'),mediaHash=sha256(media);
  const snapshot={schema:'filmcraft-capability-snapshot/v1',mode:'headless',fixture:true};
  const files:Record<string,Buffer>={
    'plan.json':Buffer.from(JSON.stringify({assets:{still:{path:'input.png',sha256:mediaHash}}})),
    'project.fcproj':Buffer.from('synthetic project'), 'film.mp4':Buffer.from('synthetic film'),
    'assets/still.png':media,'exchange-loss.json':Buffer.from('{}'),
    'capabilities.json':Buffer.from(JSON.stringify({...snapshot,commandChecks:[],resourceChecks:[]})),
    'generator-private.txt':Buffer.from('generator self defense must not enter review'),
  };
  for(const [name,bytes] of Object.entries(files)){writeFileSync(join(output,name),bytes);}
  const identity=normalizePlan(join(output,'plan.json')),base=binding(root);
  const task={...base,planHash:identity.canonicalPlanSha256,nativePlanHash:identity.workflowPlanSha256,
    inputHashes:{still:mediaHash},inputRefs:[{assetId:'still',version:'fixture-v1',sha256:mediaHash}],
    runtimeIdentity:{...base.runtimeIdentity,capabilitySnapshotSha256:sha256(stableJson(snapshot))}};
  writeFileSync(join(output,'manifest.json'),JSON.stringify({schema:'filmcraft-delivery/v1',runtimeSha256:task.runtimeIdentity.sha256,
    sourceProjectSha256:null,assets:{still:{path:'assets/still.png',sha256:mediaHash}},
    files:Object.fromEntries(Object.entries(files).map(([name,bytes])=>[name,sha256(bytes)]))}));
  const db=new TaskLedger(join(root,'ledger.sqlite'));t.after(()=>db.close());db.register(task);
  const lease=db.claim(task.taskId,'worker',60_000);db.beginAttempt(lease,'native');db.markSubmitted(lease,123456);
  const index=new ReceiptIndex(db,join(root,'blobs')),execution='.filmcraft-execution-'+sha256(output)+'.json';
  writeFileSync(join(root,execution),JSON.stringify({schema:'filmcraft-output-execution/v1',targetHash:sha256(output),state:'finished',ownerPid:123456,
    context:{taskId:task.taskId,attemptId:lease.attemptId,sourceRevision:task.sourceRevision,sourceTreeSha256:task.sourceTreeSha256},
    identity:{planHash:task.nativePlanHash,inputHashes:task.inputHashes,projectRevision:null,runtimeSha256:task.runtimeIdentity.sha256}}));
  const linked=index.ingest(task.taskId,lease.attemptId,'delivery','manifest.json');
  index.ingest(task.taskId,lease.attemptId,'output-execution',execution);
  db.finishAttempt(lease,{outcome:'succeeded',stopped:true,receiptSha256:linked.sha256});
  const service=new ReviewService(db,index,join(root,'quality'));
  const criteria:ReviewCriteria={goal:{text:'明确的目标',constraints:['保留字幕'],audioRequired:false},
    rubric:{id:'test',version:'1',required:['decode','continuity'],thresholds:{syncToleranceMs:50,clippingAmplitude:.999,clippingFraction:1e-7}},
    reviewer:{id:'host-reviewer',kind:'host',version:'1',implementationSha256:hash()}};
  const assessment:Assessment={engineering:{status:'PASS',reason:'synthetic reopen',evidence:['fixture']},
    dimensions:{decode:{status:'PASS',reason:'synthetic decode',evidence:['fixture']},continuity:{status:'PASS',reason:'synthetic review',evidence:['fixture']}},
    evidenceCapabilities:['native-reopen','full-video','independent-creative-review']};
  const create=()=>service.create(task.taskId,criteria);
  const verify=(request:any)=>()=>({requestSha256:reviewRequestHash(request),reviewer:criteria.reviewer,contextId:'independent-host-context',
    independence:'host' as const,observedFiles:Object.fromEntries(Object.entries(request.subject.files).map(([name,file]:[string,any])=>[name,file.sha256]))});
  return {root,output,db,task,service,criteria,assessment,create,verify};
}
test('import requires a trusted independent context verifier; body declarations cannot authorize it',t=>{
  const f=setup(t),{requestRef,request}=f.create();
  assert.throws(()=>f.service.importIndependent(requestRef,f.assessment,'self-declared'),/review_context_verifier_required/);
  assert.throws(()=>f.service.importIndependent(requestRef,f.assessment,'missing',()=>null),/review_context_unconfirmed/);
  const trusted=f.verify(request)();
  for(const context of [{...trusted,contextId:request.subject.attemptId},{...trusted,requestSha256:hash('b')},
    {...trusted,observedFiles:{}},{...trusted,independence:'manual'}]){
    assert.throws(()=>f.service.importIndependent(requestRef,f.assessment,'forged',()=>context),/review_context_unconfirmed/);
  }
  const {receiptRef}=f.service.importIndependent(requestRef,f.assessment,'host-reference',f.verify(request));
  const result=f.service.readCurrent(requestRef,receiptRef,f.criteria);
  assert.equal(result.decision,'review_ready');assert.equal(result.userAcceptance,'NOT_RUN');
  assert.equal(f.db.getTask(f.task.taskId).state,'verifying');
  // 人工评审走同一可信宿主核验路径；不是评审者自行声明独立。
  f.criteria.reviewer.kind='manual';const manual=f.create();
  const context={...f.verify(manual.request)(),independence:'manual' as const};
  const receipt=f.service.importIndependent(manual.requestRef,f.assessment,'actual-host-manual-reference',()=>context);
  assert.equal(f.service.readCurrent(manual.requestRef,receipt.receiptRef,f.criteria).decision,'review_ready');
});
for(const changed of ['candidate','project','input','execution','epoch','goal','rubric','reviewer']){
  test('stored PASS cannot replay after '+changed+' changes',t=>{
    const f=setup(t),{requestRef,request}=f.create();
    const {receiptRef}=f.service.importIndependent(requestRef,f.assessment,'host',f.verify(request));
    if(changed==='goal'){f.criteria.goal.text='new goal';}
    if(changed==='rubric'){f.criteria.rubric.version='2';}
    if(changed==='reviewer'){f.criteria.reviewer.version='2';}
    if(changed==='candidate'){writeFileSync(join(f.output,'film.mp4'),'changed');}
    if(changed==='project'){writeFileSync(join(f.output,'project.fcproj'),'changed');}
    if(changed==='input'){writeFileSync(join(f.output,'assets/still.png'),'changed');}
    if(changed==='execution'){f.db.db.prepare('UPDATE attempts SET pid=999 WHERE task_id=?').run(f.task.taskId);}
    if(changed==='epoch'){f.db.db.prepare('UPDATE tasks SET epoch=epoch+1 WHERE task_id=?').run(f.task.taskId);}
    assert.throws(()=>f.service.readCurrent(requestRef,receiptRef,f.criteria),/review_evidence_stale|review_source_unconfirmed|stale_epoch|attempt/);
  });
}
test('external process receives only frozen work and explicit environment, excludes generator context',t=>{
  const f=setup(t),script=join(f.root,'reviewer.py');
  writeFileSync(script,`import argparse,hashlib,json,os,pathlib\np=argparse.ArgumentParser()\nfor n in ['request','artifacts','tools']:p.add_argument('--'+n)\na=p.parse_args()\nr=pathlib.Path(a.request).read_bytes()\nfiles={str(x.relative_to(a.artifacts)) for x in pathlib.Path(a.artifacts).rglob('*') if x.is_file()}\nassert files=={'project.fcproj','film.mp4','assets/still.png'}\nassert 'FILMCRAFT_GENERATOR_RATIONALE' not in os.environ\nassert pathlib.Path.cwd()==pathlib.Path(os.environ['HOME'])\nprint(json.dumps({'schema':'filmcraft-review-assessment/v1','requestSha256':hashlib.sha256(r[:-1]).hexdigest(),'assessment':{'engineering':{'status':'NOT_RUN','reason':'isolation test only','evidence':[]},'dimensions':{}}}))\n`);
  const command={id:'isolation-fixture',version:'1',executable:process.env.FILMCRAFT_PYTHON??'python3',script,tools:{}};
  // realpath requires an absolute executable; resolution remains a host responsibility.
  const python=process.env.FILMCRAFT_PYTHON;
  if(!python){command.executable='/usr/bin/python3';}
  f.criteria.reviewer=reviewerIdentity(command);process.env.FILMCRAFT_GENERATOR_RATIONALE='perfect';
  t.after(()=>delete process.env.FILMCRAFT_GENERATOR_RATIONALE);
  const {requestRef}=f.create(),result=f.service.runExternal(requestRef,command);
  assert.equal(result.evaluation.decision,'manual_review');
  const receipt=JSON.parse(readFileSync(join(f.root,'quality',result.receiptRef),'utf8'));
  assert.equal(receipt.context.source,'external-process');assert.equal(receipt.context.workingDirectory,'fresh-private');
  assert.ok(receipt.context.pid>0);assert.equal(f.db.getTask(f.task.taskId).state,'verifying');
  writeFileSync(script,'changed reviewer');assert.throws(()=>f.service.runExternal(requestRef,command),/reviewer_identity_mismatch/);
});
test('private review CAS refuses replaced originals',t=>{
  const f=setup(t),{requestRef}=f.create();writeFileSync(join(f.root,'quality',requestRef),'{}');
  assert.throws(()=>f.service.runExternal(requestRef,{} as any),/review_record_conflict/);
});
test('candidate mutation during trusted context verification cannot commit a successful receipt',t=>{
  const f=setup(t),{requestRef,request}=f.create(),trusted=f.verify(request)();
  assert.throws(()=>f.service.importIndependent(requestRef,f.assessment,'host',()=>{
    writeFileSync(join(f.output,'film.mp4'),'changed during host verification');return trusted;
  }),/review_evidence_stale|review_source_unconfirmed/);
});
