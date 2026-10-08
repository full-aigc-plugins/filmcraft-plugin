import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cpSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { RevisionService } from '../../src/quality/revision_service.ts';
import { compileRevision } from '../../src/quality/native_revision_scope.ts';
import { ResourceController } from '../../src/harness/resources.ts';
import { StateMaintenance } from '../../src/harness/state_maintenance.ts';
import { normalizePlan } from '../../src/adapters/plan_identity.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { qualityFixture } from './quality_fixtures.ts';
import { captureEvidence, fixtureAuthorizer, hash } from './fixtures.ts';

// 合成原生结构、可信宿主回执与SQL记录只用于状态门禁测试；真实原生另行执行。
function fixture(t:any,limits={maxRounds:3,maxFailures:2,maxStagnant:2,minImprovement:0},unconfirmed=false){
  const project={format:'filmcraft.project',schema_version:12,project:{items:{
    '7':{id:7,kind:{Sequence:{video_tracks:[{id:1,items:[{id:9,item:8,start:0,duration:100,speed:1,reverse:false,gain_db:0,
      effects:[{effect:'time_remap',params:{speed:{value:{Float:100}}}}]}]},{id:2,items:[],name:'untouched'}],audio_tracks:[]}}},
    '8':{id:8,kind:{Media:{media:{File:{path:'assets/still.png'}}}}}}}};
  const f=qualityFixture(t,Buffer.from(JSON.stringify(project)));
  f.criteria.rubric.required=['decode'];delete f.assessment.dimensions.continuity;
  if(unconfirmed){f.assessment.engineering.status='NOT_RUN';f.assessment.dimensions.decode.status='NOT_RUN';}
  const resources=new ResourceController(f.db);resources.reserve(f.task.taskId,{limits:{timeMs:100000,diskBytes:100000,outputBytes:100000,slots:2,revisions:5},
    allocation:{timeMs:10000,diskBytes:10000,outputBytes:10000,slots:1,revisions:0}});resources.settle(f.task.taskId,{stopped:true,outputBytes:100});
  const policy={criteria:f.criteria,limits,scopes:[{ownerPlugin:'filmcraft',sequenceId:'7',trackId:'1',objectId:'9',startTick:'0',endTick:'100',
    fields:['/speed','/reverse','/duration','/effects/0/params/speed/value/Float'],dependencies:['still']}],
    issues:[{id:'double-speed',target:'7/1/9',command:'clip.speedDuration',params:{speed:200,reverse:false,ripple:false}}]};
  const created=f.service.create(f.task.taskId,f.criteria),imported=f.service.importIndependent(created.requestRef,f.assessment,'fixture',f.verify(created.request));
  const baseline={taskId:f.task.taskId,requestRef:created.requestRef,receiptRef:imported.receiptRef};
  const loop=new RevisionService(f.db,f.service,{authorize:fixtureAuthorizer}),opened=loop.open(f.task.taskId,policy,baseline);
  return {...f,project,resources,policy,baseline,loop,opened};
}
function child(f:ReturnType<typeof fixture>,name='child',outside=false){
  const source=f.loop.project(f.task.taskId),compiled=compileRevision(source,source.sourceSha256,f.policy.scopes,f.policy.issues);
  const output=join(f.root,name);cpSync(f.output,output,{recursive:true});
  const modified=structuredClone(f.project),clip=modified.project.items['7'].kind.Sequence.video_tracks[0].items[0];
  clip.speed=2;clip.duration=50;clip.effects[0].params.speed.value.Float=200;
  if(outside){modified.project.items['7'].kind.Sequence.video_tracks[1].name='outside';}
  writeFileSync(join(output,'project.fcproj'),JSON.stringify(modified));
  const identity=normalizePlan(join(output,'plan.json'));
  const binding={...f.task,taskId:name,idempotencyKey:name,outputRoot:output,projectKey:hash(name==='child'?'c':'d'),
    projectRevision:source.sourceSha256,planHash:identity.canonicalPlanSha256,nativePlanHash:identity.workflowPlanSha256};
  const manifest=JSON.parse(readFileSync(join(output,'manifest.json'),'utf8'));manifest.sourceProjectSha256=source.sourceSha256;
  manifest.files['project.fcproj']=sha256(readFileSync(join(output,'project.fcproj')));
  const loss=JSON.parse(readFileSync(join(output,'exchange-loss.json'),'utf8'));loss.native.sha256=manifest.files['project.fcproj'];
  writeFileSync(join(output,'exchange-loss.json'),JSON.stringify(loss));manifest.files['exchange-loss.json']=sha256(readFileSync(join(output,'exchange-loss.json')));
  manifest.lossReport.sha256=manifest.files['exchange-loss.json'];writeFileSync(join(output,'manifest.json'),JSON.stringify(manifest));
  const parent=f.db.getTask(f.task.taskId);f.db.beginContinuation(f.task.taskId,parent.epoch,hash(),binding);
  const lease=f.db.claim(name,'synthetic-worker',60000);f.db.beginAttempt(lease,'synthetic-native');f.db.markSubmitted(lease,123456);
  const guard='.filmcraft-execution-'+sha256(output)+'.json';writeFileSync(join(f.root,guard),JSON.stringify({schema:'filmcraft-output-execution/v1',
    targetHash:sha256(output),state:'finished',ownerPid:123456,context:{taskId:name,attemptId:lease.attemptId,sourceRevision:binding.sourceRevision,sourceTreeSha256:binding.sourceTreeSha256},
    identity:{planHash:binding.nativePlanHash,inputHashes:binding.inputHashes,projectRevision:binding.projectRevision,runtimeSha256:binding.runtimeIdentity.sha256}}));
  const receipt=f.service.index.ingest(name,lease.attemptId,'delivery','manifest.json');f.service.index.ingest(name,lease.attemptId,'output-execution',guard);
  f.db.finishAttempt(lease,{outcome:'succeeded',stopped:true,receiptSha256:receipt.sha256});
  const count=f.loop.snapshot(f.opened.loopId).rounds+1;
  const intent=stableJson({child:binding,sourceTaskId:f.task.taskId,compiled,generation:f.opened.generation});
  f.db.db.prepare('INSERT INTO revision_rounds VALUES(?,?,?,?,?,?,?,?)').run(f.opened.loopId,count,name,sha256(intent),intent,'pending',null,null);
  const review=f.service.create(name,f.criteria),result=f.service.importIndependent(review.requestRef,f.assessment,'fixture',f.verify(review.request));
  return {taskId:name,requestRef:review.requestRef,receiptRef:result.receiptRef,output};
}
test('persisted policy cannot reset rounds or expand field/goal scope; original authorization reference is reused',t=>{
  const f=fixture(t);assert.equal(f.loop.open(f.task.taskId,f.policy,f.baseline).loopId,f.opened.loopId);
  assert.throws(()=>f.loop.open(f.task.taskId,{...f.policy,limits:{...f.policy.limits,maxRounds:99}},f.baseline),/revision_policy_conflict/);
  const another=new RevisionService(f.db,f.service,{authorize:fixtureAuthorizer});assert.equal(another.snapshot(f.opened.loopId).rounds,0);
  assert.equal(f.opened.best.taskId,f.task.taskId);assert.deepEqual(f.opened.unresolvedIssues,['double-speed']);
  captureEvidence('revision-policy-restart','synthetic persistent SQL scope, no native or creative acceptance',{loopId:f.opened.loopId,policyPreserved:true});
});
test('a new candidate needs its own review; old task PASS cannot be relabeled',t=>{
  const f=fixture(t),next=child(f);
  assert.throws(()=>f.loop.observe(f.opened.loopId,next.taskId,{...f.baseline,taskId:next.taskId}),/revision_review_invalid/);
  const result=f.loop.observe(f.opened.loopId,next.taskId,next);
  assert.equal(result.state,'stopped');assert.equal(result.reason,'issues_resolved');assert.equal(result.best.taskId,next.taskId);
  assert.equal(result.userAcceptance,'NOT_RUN');assert.equal(f.db.getTask(next.taskId).state,'verifying');
});
test('non-target mutation rejects candidate and retains original verified best',t=>{
  const f=fixture(t),next=child(f,'child',true),result=f.loop.observe(f.opened.loopId,next.taskId,next);
  assert.equal(result.reason,'scope_violation');assert.equal(result.best.taskId,f.task.taskId);
  captureEvidence('revision-scope-rejection','synthetic current candidate and full-project diff',{reason:result.reason,bestPreserved:true});
});
test('failure limit retains a verified best and unresolved technical findings',t=>{
  const f=fixture(t,{maxRounds:5,maxFailures:1,maxStagnant:5,minImprovement:0});
  f.assessment.dimensions.decode.status='FAIL';const next=child(f),result=f.loop.observe(f.opened.loopId,next.taskId,next);
  assert.equal(result.reason,'failure_limit');assert.equal(result.best.taskId,f.task.taskId);assert.deepEqual(result.unresolvedQuality,['decode']);
  captureEvidence('revision-failure-limit','synthetic independent FAIL gate',{reason:result.reason,bestPreserved:true});
});
for(const reason of ['stagnation_limit','round_limit']){
  test(reason+' stops with explicit null when no candidate is verified',t=>{
    const f=fixture(t,{maxRounds:reason==='round_limit'?1:3,maxFailures:5,maxStagnant:reason==='stagnation_limit'?1:5,minImprovement:2},true);
    const next=child(f),result=f.loop.observe(f.opened.loopId,next.taskId,next);
    assert.equal(result.reason,reason);assert.equal(result.best,null);assert.ok(result.unresolvedQuality.length);
    captureEvidence('revision-'+reason,'synthetic unconfirmed quality, no best fabricated',{reason:result.reason,best:null});
  });
}
test('unknown pending round blocks dispatch and cannot reuse its slot after a restart',async t=>{
  const f=fixture(t),next=child(f);f.db.db.prepare("UPDATE tasks SET state='reconciling' WHERE task_id=?").run(next.taskId);
  const result=f.loop.observe(f.opened.loopId,next.taskId);assert.equal(result.pending,next.taskId);
  const reopened=new RevisionService(f.db,f.service,{authorize:fixtureAuthorizer});
  await assert.rejects(reopened.execute(f.opened.loopId,f.task.taskId,'another',join(f.root,'another'),{} as any),/revision_round_pending/);
  assert.equal(f.db.listAttempts(next.taskId).length,1);
});
test('budget stop and stale best remain explicit; no last candidate is promoted',t=>{
  const f=fixture(t);f.resources.halt(f.task.taskId,'budget_revisions_exceeded');
  const stopped=f.loop.open(f.task.taskId,f.policy,f.baseline);assert.equal(stopped.reason,'budget_revisions_exceeded');assert.ok(stopped.best);
  writeFileSync(join(f.output,'film.mp4'),'changed');const stale=f.loop.snapshot(f.opened.loopId);
  assert.equal(stale.best,null);assert.equal(stale.invalidEvidence.length,1);assert.ok(stale.unresolvedIssues.length);
});
test('state integrity refuses a modified round rather than trusting stored self-evaluation',t=>{
  const f=fixture(t);child(f);f.db.db.prepare("UPDATE revision_rounds SET intent='{}'").run();
  assert.throws(()=>f.db.verifyIntegrity(),/ledger_revision_corrupt/);
  assert.throws(()=>new StateMaintenance(join(f.root,'ledger.sqlite')).inspect(),/ledger_revision_corrupt/);
});

test('goal or rubric change invalidates all previous best evidence and permanently fences dispatch',async t=>{
  const f=fixture(t),changed={...f.criteria,goal:{...f.criteria.goal,text:'A different creative goal'}};
  const invalid=f.loop.invalidateCriteria(f.opened.loopId,changed);
  assert.equal(invalid.reason,'criteria_changed');assert.equal(invalid.best,null);
  assert.ok(invalid.unresolvedIssues.length);assert.equal(invalid.userAcceptance,'NOT_RUN');
  const reopened=new RevisionService(f.db,f.service,{authorize:fixtureAuthorizer});
  assert.equal(reopened.snapshot(f.opened.loopId).best,null);
  await assert.rejects(reopened.execute(f.opened.loopId,f.task.taskId,'new-goal',join(f.root,'new-goal'),{} as any),/revision_loop_stopped/);
  captureEvidence('revision-criteria-invalidated','synthetic goal drift invalidates old best across restart',{reason:invalid.reason,best:null});
});
