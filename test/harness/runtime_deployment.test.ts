import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { RuntimeDeployment } from '../../src/adapters/runtime_deployment.ts';
import { binding, workspace, fixtureAuthorizer, hash } from './fixtures.ts';

function setup(t:any){
 const root=workspace(t),ledger=new TaskLedger(join(root,'state.sqlite'));t.after(()=>ledger.close());
 const service=new RuntimeDeployment(ledger,{authorize:fixtureAuthorizer});
 const old=binding(root),next=binding(root,{sourceRevision:'a'.repeat(40),sourceTreeSha256:hash('b'),runtimeIdentity:{...old.runtimeIdentity,cliVersion:'0.2.0-craft.5',sha256:hash('c')}});
 const descriptor=(b:any)=>({sourceRevision:b.sourceRevision,sourceTreeSha256:b.sourceTreeSha256,runtimeIdentity:b.runtimeIdentity,ledgerSchemas:[6]});
 const grant={authorizationRef:old.authorizationRef,authorizationScopeSha256:old.authorizationScopeSha256};
 return {root,ledger,service,old,next,descriptor,grant};
}
test('runtime switch persists generation, retains old identity and fences stale admission',t=>{
 const f=setup(t),a=f.service.activate(f.descriptor(f.old),f.grant),b=f.service.activate(f.descriptor(f.next),f.grant);
 assert.equal(a.generation,1);assert.equal(b.generation,2);assert.equal(f.service.history().length,2);
 assert.throws(()=>f.ledger.register(f.old),/runtime_selection_mismatch/);
 assert.equal(f.ledger.register(f.next).state,'planned');
});
test('planned, live and unknown work prevent upgrade without switching identity',t=>{
 const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);f.ledger.register(f.old);
 assert.throws(()=>f.service.activate(f.descriptor(f.next),f.grant),/runtime_not_drained/);
 assert.equal(f.service.current().generation,1);
});
test('compatible rollback preserves history and incompatible schema cannot become active',t=>{
 const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);f.service.activate(f.descriptor(f.next),f.grant);
 assert.throws(()=>f.service.activate({...f.descriptor(f.old),ledgerSchemas:[5]},f.grant),/runtime_state_incompatible/);
 const back=f.service.rollback(1,f.grant);assert.equal(back.generation,3);assert.equal(f.service.history().length,3);
 assert.equal(f.ledger.register(f.old).state,'planned');
});
test('runtime selection cannot be authorized by its own body',t=>{
 const f=setup(t),untrusted=new RuntimeDeployment(f.ledger);
 assert.throws(()=>untrusted.activate(f.descriptor(f.old),f.grant),/authorization_verifier_required/);
 assert.equal(f.service.current(),null);
});
test('selection survives a new connection and history corruption fails closed',t=>{
 const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);f.service.activate(f.descriptor(f.next),f.grant);
 const reopened=new TaskLedger(join(f.root,'state.sqlite'));t.after(()=>reopened.close());
 assert.throws(()=>reopened.register(f.old),/runtime_selection_mismatch/);
 assert.equal(new RuntimeDeployment(reopened).current().generation,2);
 reopened.db.prepare("UPDATE runtime_deployments SET descriptor='{}' WHERE generation=1").run();
 assert.throws(()=>reopened.register(f.next),/runtime_descriptor_invalid/);
});
for(const outcome of ['live','unknown'] as const){
 test(outcome+' execution retains its occupancy and refuses runtime replacement',t=>{
  const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);f.ledger.register(f.old);
  const lease=f.ledger.claim(f.old.taskId,'owner',60000);f.ledger.beginAttempt(lease,'op');
  if(outcome==='unknown'){f.ledger.finishAttempt(lease,{outcome:'unknown',stopped:false,receiptSha256:null});}
  assert.throws(()=>f.service.activate(f.descriptor(f.next),f.grant),/runtime_not_drained/);
  assert.equal(f.service.current().generation,1);assert.equal(f.ledger.listAttempts(f.old.taskId).length,1);
  assert.equal(f.ledger.db.prepare('SELECT COUNT(*) AS n FROM project_leases').get()!.n,1);
 });
}
test('revoked authorization before publication preserves generation and old identity',t=>{
 const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);let reads=0;
 const service=new RuntimeDeployment(f.ledger,{authorize:(subject,request)=>++reads===1?fixtureAuthorizer(subject,request):null});
 assert.throws(()=>service.activate(f.descriptor(f.next),f.grant),/authorization_required/);
 assert.equal(f.service.current().generation,1);assert.equal(f.service.history().length,1);
});
test('activation write transaction excludes another admission connection before selection publication',t=>{
 const f=setup(t),other=new TaskLedger(join(f.root,'state.sqlite'));t.after(()=>other.close());
 other.db.exec('PRAGMA busy_timeout=0');let blocked=0;
 const service=new RuntimeDeployment(f.ledger,{authorize:(subject,request)=>{
  assert.throws(()=>other.register(f.old),/database is locked/);blocked++;
  return fixtureAuthorizer(subject,request);
 }});
 service.activate(f.descriptor(f.next),f.grant);assert.equal(blocked,2);
 assert.throws(()=>other.register(f.old),/runtime_selection_mismatch/);
});
test('an upgrade grant subject is specific to its actual ledger path',t=>{
 const f=setup(t),other=new TaskLedger(join(f.root,'another.sqlite'));t.after(()=>other.close());
 const descriptor=f.descriptor(f.old);
 assert.notEqual(f.service.subject(descriptor,'upgrade').identitySha256,new RuntimeDeployment(other).subject(descriptor,'upgrade').identitySha256);
});
test('failed or identity-drifting live probe cannot publish a new generation',t=>{
 const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);
 for(const verifyCandidate of [()=>{throw new Error('probe_failed');},(d:any)=>({...d,sourceTreeSha256:hash('f')})]){
  const service=new RuntimeDeployment(f.ledger,{authorize:fixtureAuthorizer,verifyCandidate});
  assert.throws(()=>service.activate(f.descriptor(f.next),f.grant),/probe_failed|runtime_probe_changed/);
  assert.equal(f.service.current().generation,1);
 }
});
test('a stale activation generation is rejected before probing or publishing',t=>{
 const f=setup(t);f.service.activate(f.descriptor(f.old),f.grant);let probed=false;
 const service=new RuntimeDeployment(f.ledger,{authorize:fixtureAuthorizer,expectedGeneration:0,verifyCandidate:d=>{probed=true;return d;}});
 assert.throws(()=>service.activate(f.descriptor(f.next),f.grant),/runtime_generation_stale/);assert.equal(probed,false);
});
