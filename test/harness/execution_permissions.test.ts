import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync, symlinkSync, renameSync } from 'node:fs';
import { join } from 'node:path';
import { workspace, binding, fixtureAuthorizer } from './fixtures.ts';
import { executionSubject, WorkflowAdmission } from '../../src/harness/workflow_admission.ts';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { validatePermissions, requireRead, requireWrite } from '../../src/support/execution_permissions.ts';

function policy(root: string) { return { schema: 'filmcraft-execution-permissions/v1' as const, readRoots: [root], writeRoots: [root] }; }
test('trusted canonical roots refuse broad grants, extra fields and parent symlink replacement', t => {
 const root=workspace(t), inside=join(root,'inside'),outside=join(root,'outside');mkdirSync(inside);mkdirSync(outside);
 assert.deepEqual(validatePermissions(policy(inside)),policy(inside));
 assert.throws(()=>validatePermissions({...policy(inside),metadata:'OWNED_TEST_CANARY'}),/^HarnessError: invalid_execution_permissions$/);
 assert.throws(()=>validatePermissions({...policy(inside),writeRoots:['/']}),/invalid_execution_permissions/);
 const link=join(root,'link');symlinkSync(outside,link);assert.throws(()=>validatePermissions(policy(link)),/invalid_execution_permissions/);
 assert.throws(()=>requireRead(join(outside,'secret'),policy(inside)),/permission_read_denied/);
 assert.throws(()=>requireWrite(join(outside,'project'),policy(inside)),/permission_write_denied/);
});
test('changing trusted roots changes execute authorization even with identical plan and resources', t => {
 const root=workspace(t),extra=join(root,'extra');mkdirSync(extra);const task=binding(root);
 const first=executionSubject(task,undefined,policy(root)),second=executionSubject(task,undefined,policy(extra));
 assert.notEqual(first.identitySha256,second.identitySha256);
 assert.notEqual(first.identitySha256,executionSubject(task).identitySha256);
});
test('legacy exact grant cannot dispatch without trusted directory policy', async t => {
 const root=workspace(t),db=new TaskLedger(join(root,'ledger.sqlite'));t.after(()=>db.close());
 const runner=new WorkflowAdmission(db,new ReceiptIndex(db,join(root,'blobs')),{skillDirectory:join(root,'missing-skill'),sourceRevision:'d'.repeat(40),runtimeHome:join(root,'runtime'),pluginVersion:'test'},fixtureAuthorizer);
 await assert.rejects(runner.run(binding(root),join(root,'plan.json')),/execution_permissions_required/);
 assert.equal(db.db.prepare('SELECT count(*) AS n FROM tasks').get()?.n,0);
});
test('runner rejects outside plan before reading it or touching runtime', async t => {
 const root=workspace(t),allowed=join(root,'allowed');mkdirSync(allowed);
 const { PythonWorkflowRunner }=await import('../../src/adapters/python_workflow.ts');
 const runner=new PythonWorkflowRunner(null as any,null as any,{skillDirectory:join(root,'missing-skill'),sourceRevision:'d'.repeat(40),runtimeHome:join(root,'runtime'),pluginVersion:'test',permissions:policy(allowed)});
 assert.throws(()=>runner.prepare(join(root,'missing.json'),join(allowed,'delivery')),/permission_read_denied/);
});

test('parent directory replacement cannot reauthorize an outside root', t => {
 const root=workspace(t),parent=join(root,'parent'),outside=join(root,'outside');mkdirSync(parent);mkdirSync(outside);mkdirSync(join(parent,'media'));mkdirSync(join(outside,'media'));
 const accepted=validatePermissions(policy(join(parent,'media')));renameSync(parent,join(root,'old-parent'));symlinkSync(outside,parent);
 assert.throws(()=>validatePermissions(accepted),/invalid_execution_permissions/);
});
