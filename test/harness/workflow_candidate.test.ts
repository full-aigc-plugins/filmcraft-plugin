import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {existsSync,mkdirSync,readFileSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {fingerprintSkill} from '../../src/adapters/python_workflow.ts';
import {RuntimeDeployment} from '../../src/adapters/runtime_deployment.ts';
import {TaskLedger} from '../../src/harness/task_ledger.ts';
import {executionSubject} from '../../src/harness/workflow_admission.ts';
import {sha256,stableJson} from '../../src/support/json.ts';
import {binding,fixtureAuthorizer,workspace} from './fixtures.ts';
function setup(t:any){
 const root=workspace(t),skill=join(root,'retained-skill');mkdirSync(skill);writeFileSync(join(skill,'identity.txt'),'owned synthetic fixture');
 const manifest=JSON.parse(readFileSync(new URL('../../plugin.json',import.meta.url),'utf8')).version;
 const task=binding(root);task.sourceTreeSha256=fingerprintSkill(skill);task.runtimeIdentity.pluginVersion=manifest;
 const candidate={schema:'filmcraft-runtime-candidate/v1',skillDirectory:skill,sourceRevision:task.sourceRevision,sourceTreeSha256:task.sourceTreeSha256};
 const file=join(root,'candidate.json'),bound=join(root,'binding.json'),resources=join(root,'resources.json'),ledger=join(root,'state.sqlite'),grants=join(root,'grants');
 writeFileSync(file,JSON.stringify(candidate));writeFileSync(bound,JSON.stringify(task));writeFileSync(resources,JSON.stringify({limits:{},allocation:{}}));
 const cli=new URL('../../src/cli/workflow.ts',import.meta.url).pathname;
 const run=(command='subject')=>{const p=spawnSync(process.execPath,[cli,command,'--binding',bound,'--resources',resources,'--candidate',file,
  ...(command==='run'?['--plan',join(root,'absent-plan'),'--ledger',ledger,'--blobs',join(root,'blobs'),'--authorization-root',grants,'--runtime-home',join(root,'runtime')]:[])],{encoding:'utf8'});return {status:p.status,body:JSON.parse(p.stdout)};};
 const authorize=()=>{mkdirSync(grants,{mode:0o700});writeFileSync(join(grants,sha256(task.authorizationRef)+'.json'),JSON.stringify({schema:'filmcraft-local-authorization/v1',authorizationRef:task.authorizationRef,authorizationScopeSha256:task.authorizationScopeSha256,subjects:[sha256(stableJson(executionSubject(task,{limits:{},allocation:{}})))],expiresAt:Date.now()+60000,revoked:false}),{mode:0o600});};
 return {root,skill,task,candidate,file,ledger,run,authorize};
}
test('retained candidate subject is read-only and remains bound to the exact source',t=>{
 const f=setup(t),r=f.run();assert.equal(r.status,0);assert.deepEqual(r.body,executionSubject(f.task,{limits:{},allocation:{}}));
 assert.equal(existsSync(f.ledger),false);assert.equal(existsSync(join(f.root,'runtime')),false);
});
test('candidate caller cannot supply availability or a mismatched source identity',t=>{
 const f=setup(t);
 for(const [candidate,code] of [[{...f.candidate,available:true},'runtime_candidate_invalid'],[{...f.candidate,sourceRevision:'a'.repeat(40)},'runtime_candidate_binding_mismatch']] as const){
  writeFileSync(f.file,JSON.stringify(candidate));assert.equal(f.run().body.error.code,code);
 }
 assert.equal(existsSync(f.ledger),false);
});
test('retained source drift refuses the subject before installation',t=>{
 const f=setup(t);writeFileSync(join(f.skill,'identity.txt'),'changed');assert.equal(f.run().body.error.code,'runtime_candidate_changed');assert.equal(existsSync(f.ledger),false);
});
test('candidate selection never replaces the required execution grant',t=>{
 const f=setup(t);assert.equal(f.run('run').body.error.code,'authorization_required');assert.equal(existsSync(f.ledger),false);
});
test('an execution grant cannot bypass runtime selection for a retained candidate',t=>{
 const f=setup(t);f.authorize();assert.equal(f.run('run').body.error.code,'runtime_selection_required');
 const db=new TaskLedger(f.ledger);db.close();assert.equal(f.run('run').body.error.code,'runtime_selection_required');
 assert.equal(existsSync(join(f.root,'runtime')),false);
});
test('a selected different runtime fences an otherwise authorized retained candidate',t=>{
 const f=setup(t);f.authorize();const db=new TaskLedger(f.ledger);new RuntimeDeployment(db,{authorize:fixtureAuthorizer}).activate({sourceRevision:'a'.repeat(40),sourceTreeSha256:f.task.sourceTreeSha256,runtimeIdentity:f.task.runtimeIdentity,ledgerSchemas:[6]},f.task);db.close();
 assert.equal(f.run('run').body.error.code,'runtime_selection_mismatch');assert.equal(existsSync(join(f.root,'runtime')),false);
});
test('matching activated candidate reaches its own adapter instead of the bundled source',t=>{
 const f=setup(t);f.authorize();const db=new TaskLedger(f.ledger);new RuntimeDeployment(db,{authorize:fixtureAuthorizer}).activate({sourceRevision:f.task.sourceRevision,sourceTreeSha256:f.task.sourceTreeSha256,runtimeIdentity:f.task.runtimeIdentity,ledgerSchemas:[6]},f.task);db.close();
 assert.equal(f.run('run').body.error.code,'capability_adapter_missing');assert.equal(existsSync(join(f.root,'runtime')),false);
});
