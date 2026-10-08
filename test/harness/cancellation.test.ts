import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { once } from 'node:events';
import { join } from 'node:path';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ResourceController } from '../../src/harness/resources.ts';
import { CancellationService, cancellationSubject } from '../../src/harness/cancellation.ts';
import { groupState } from '../../src/harness/process_identity.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { binding, fixtureAuthorizer, workspace, captureEvidence } from './fixtures.ts';

const amounts = { timeMs: 60_000, diskBytes: 1_000_000, outputBytes: 1_000_000, slots: 2, revisions: 1 };
async function fixture(t: any, stopSupported = true, asChild = false) {
  const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file);
  t.after(() => db.close()); const task = binding(root); db.register(task);
  const resources = new ResourceController(db), scopeLimits = { ...amounts, timeMs: 120_000 };
  if (asChild) {
    const parent = binding(root,{ taskId:'parent',idempotencyKey:'parent',outputRoot:join(root,'parent'),projectKey:'e'.repeat(64) });db.register(parent);
    resources.reserve(parent.taskId,{limits:scopeLimits,allocation:{timeMs:1000,diskBytes:0,outputBytes:0,slots:1,revisions:0}});
    const parentLease=db.claim(parent.taskId,'parent-host',1000);db.beginAttempt(parentLease,'parent');
    db.finishAttempt(parentLease,{outcome:'succeeded',stopped:true,receiptSha256:'a'.repeat(64)});
    resources.settle(parent.taskId,{stopped:true,outputBytes:0});
  }
  resources.reserve(task.taskId, { ...(asChild ? {} : {limits:scopeLimits}), allocation: { ...amounts, slots: 1, revisions: 0 } }, asChild?'parent':undefined);
  const lease = db.claim(task.taskId, 'host', 60_000); db.beginAttempt(lease, 'actual-controlled-process');
  mkdirSync(task.outputRoot); writeFileSync(join(task.outputRoot, 'partial.txt'), 'preserve partial output');
  const child = spawn(process.execPath, ['-e', 'setInterval(()=>{},1000)'], { detached: true, stdio: 'ignore' });
  await once(child, 'spawn'); const closed = once(child, 'close');
  t.after(async () => { if (child.exitCode === null && child.signalCode === null) { try { process.kill(-child.pid!, 'SIGTERM'); } catch {} } await closed; });
  db.markSubmitted(lease, child.pid!);
  const service = new CancellationService(db, { authorize: fixtureAuthorizer });
  assert.equal(service.bindProcess(lease, child.pid!, stopSupported), true);
  return { root, file, db, task, resources, lease, child, closed, service };
}
test('cancel request persists before signalling, invalidates the writer, and confirms only after native group stops', { timeout: 15_000 }, async t => {
  const { db, task, resources, lease, child, closed, service } = await fixture(t);
  assert.throws(() => new CancellationService(db).request(task.taskId, task), /authorization_verifier_required/);
  service.request(task.taskId, task);
  assert.equal(db.getTask(task.taskId).state, 'cancel_requested');
  assert.equal(groupState(child.pid!), 'running');
  assert.equal(resources.snapshot(task.taskId).reservations[0].state, 'reserved');
  assert.throws(() => db.finishAttempt(lease, { outcome: 'failed', stopped: true, receiptSha256: null }), /stale_epoch/);
  const requested = service.reconcile(task.taskId, { signal: true });
  assert.equal(requested.signalled, true);
  await closed;
  const confirmed = service.reconcile(task.taskId);
  assert.equal(confirmed.state, 'cancelled'); assert.equal(confirmed.process, 'stopped');
  assert.equal(db.db.prepare('SELECT COUNT(*) AS n FROM project_leases').get()!.n, 0);
  assert.equal(resources.snapshot(task.taskId).reservations[0].state, 'settled');
  assert.equal(readFileSync(join(task.outputRoot, 'partial.txt'), 'utf8'), 'preserve partial output');
  captureEvidence('actual-budget-cancel-confirmed', 'actual controlled POSIX process group', { requestState: 'cancel_requested', finalState: confirmed.state, signalled: true, partialPreserved: true });
});
test('unsupported cancellation retains running process, occupancy, reservation and partial diagnostics after reopen', { timeout: 15_000 }, async t => {
  const { file, db, task, child, service } = await fixture(t, false);
  service.request(task.taskId, task);
  const reopened = new TaskLedger(file); t.after(() => reopened.close());
  const report = new CancellationService(reopened, { authorize: fixtureAuthorizer }).reconcile(task.taskId, { signal: true });
  assert.equal(report.state, 'cancel_requested'); assert.equal(report.process, 'running'); assert.equal(report.signalled, false);
  assert.equal(groupState(child.pid!), 'running');
  assert.equal(db.db.prepare('SELECT COUNT(*) AS n FROM project_leases').get()!.n, 1);
  assert.equal(new ResourceController(reopened).snapshot(task.taskId).reservations[0].state, 'reserved');
  assert.equal(existsSync(join(task.outputRoot, 'partial.txt')), true);
  captureEvidence('budget-cancel-unsupported','actual controlled process, declared stop unsupported',{state:report.state,process:report.process,signalled:false,reservation:'reserved',occupancy:1});
});
test('PID reuse or changed birth identity cannot signal a process even when its numeric PID matches', { timeout: 15_000 }, async t => {
  const { db, task, child, service } = await fixture(t);
  const row = db.db.prepare('SELECT process_identity FROM task_resources WHERE task_id=?').get(task.taskId)!;
  const bound = JSON.parse(String(row.process_identity)); bound.identity.started += '-different-birth';
  db.db.prepare('UPDATE task_resources SET process_identity=? WHERE task_id=?').run(JSON.stringify(bound), task.taskId);
  service.request(task.taskId, task);
  const result = service.reconcile(task.taskId, { signal: true });
  assert.equal(result.process, 'unknown'); assert.equal(result.signalled, false); assert.equal(result.state, 'cancel_requested');
  assert.equal(groupState(child.pid!), 'running');
  captureEvidence('budget-cancel-pid-reuse','injected birth mismatch on actual controlled process',{state:result.state,process:result.process,signalled:false,originalStillRunning:true});
});
test('lost cancellation reply is recovered from durable request without new attempts or double settlement', { timeout: 15_000 }, async t => {
  const { file, task, db, closed, service } = await fixture(t);
  service.request(task.taskId, task); service.reconcile(task.taskId, { signal: true }); await closed;
  const restart = new TaskLedger(file); t.after(() => restart.close());
  const resumed = new CancellationService(restart, { authorize: fixtureAuthorizer });
  assert.equal(resumed.reconcile(task.taskId).state, 'cancelled');
  assert.equal(resumed.reconcile(task.taskId).signalled, false);
  assert.equal(db.listAttempts(task.taskId).length, 1);
  assert.equal(db.db.prepare('SELECT COUNT(*) AS n FROM cancel_intents').get()!.n, 1);
  captureEvidence('budget-cancel-reply-lost','actual controlled process and reopened SQLite',{state:'cancelled',attempts:1,cancelIntents:1,duplicateSignal:false});
});
test('restart after confirmed cancellation but before settlement finishes accounting exactly once', { timeout: 15_000 }, async t => {
  const { db, task, service, closed } = await fixture(t);
  service.request(task.taskId,task);service.reconcile(task.taskId,{signal:true});await closed;service.reconcile(task.taskId);
  // 故障注入：停止确认已提交，而随后的预算结算尚未提交。
  db.db.prepare("UPDATE task_resources SET state='reserved',consumed=NULL WHERE task_id=?").run(task.taskId);
  assert.equal(service.reconcile(task.taskId).state,'cancelled');
  assert.equal(new ResourceController(db).snapshot(task.taskId).reservations[0].state,'settled');
});
test('parent cancellation fences its running child and prevents any new dependent dispatch', { timeout: 15_000 }, async t => {
  const { root, db, task, resources, service, child } = await fixture(t, false, true);
  const childTask = binding(root, { taskId: 'child', idempotencyKey: 'child', projectKey: 'c'.repeat(63)+'d', outputRoot: join(root,'child') });
  db.register(childTask);
  resources.reserve(childTask.taskId, { allocation: { ...amounts, slots: 1, revisions: 1, timeMs: 1, diskBytes: 0, outputBytes: 0 } }, task.taskId);
  service.request('parent', task);
  assert.equal(db.getTask(task.taskId).state, 'cancel_requested');
  assert.equal(groupState(child.pid!),'running');
  assert.equal(resources.snapshot(task.taskId).scopeId,'parent');
  assert.equal(db.getTask(childTask.taskId).state, 'cancelled');
  assert.throws(() => db.claim(childTask.taskId, 'child', 1000), /invalid_task_state/);
  const later = binding(root, { taskId: 'later', idempotencyKey: 'later', outputRoot: join(root,'later') }); db.register(later);
  assert.throws(() => resources.reserve(later.taskId, { allocation: { ...amounts, slots: 1 } }, task.taskId), /cancel_requested/);
  captureEvidence('budget-parent-cancel-live-child','actual identity-bound detached child',{childState:'cancel_requested',childStillRunning:true,sameScope:true,newDependencyRefused:true});
});
test('revocation before the supported stop action leaves a requested cancellation and running native group', { timeout: 15_000 }, async t => {
  const { db, task, child, service } = await fixture(t);
  service.request(task.taskId, task);
  assert.throws(() => new CancellationService(db, { authorize: () => null }).reconcile(task.taskId, { signal: true }), /authorization_required/);
  assert.equal(groupState(child.pid!), 'running'); assert.equal(db.getTask(task.taskId).state, 'cancel_requested');
});
test('an exited actual host leaves its identity-bound detached child running, budget held and cancellation unconfirmed', { timeout: 15_000 }, async t => {
  const root = workspace(t), file = join(root,'ledger.sqlite'), task = binding(root);
  const module = (name: string) => new URL('../../src/harness/'+name+'.ts', import.meta.url).href;
  const code = `import {spawn} from 'node:child_process';
    import {TaskLedger} from ${JSON.stringify(module('task_ledger'))};
    import {ResourceController} from ${JSON.stringify(module('resources'))};
    import {CancellationService} from ${JSON.stringify(module('cancellation'))};
    const db=new TaskLedger(process.argv[1]),task=JSON.parse(process.argv[2]);db.register(task);
    new ResourceController(db).reserve(task.taskId,JSON.parse(process.argv[3]));
    const lease=db.claim(task.taskId,'departed-host',60000);db.beginAttempt(lease,'orphan');
    const child=spawn(process.execPath,['-e','setInterval(()=>{},1000)'],{detached:true,stdio:'ignore'});
    child.on('spawn',()=>{db.markSubmitted(lease,child.pid);new CancellationService(db).bindProcess(lease,child.pid,false);
      console.log(child.pid);db.close();child.unref();});`;
  const host = spawnSync(process.execPath, ['--input-type=module','-e',code,file,JSON.stringify(task),JSON.stringify({limits:amounts, allocation:{...amounts,slots:1}})], { encoding:'utf8',timeout:10_000 });
  assert.equal(host.status,0,host.stderr);const pid=Number(host.stdout.trim());assert.ok(pid>0);
  t.after(()=>{try{process.kill(-pid,'SIGTERM');}catch{}});
  const db=new TaskLedger(file);t.after(()=>db.close());
  const service=new CancellationService(db,{authorize:fixtureAuthorizer});service.request(task.taskId,task);
  const result=service.reconcile(task.taskId,{signal:true});
  assert.equal(groupState(pid),'running');assert.equal(result.state,'cancel_requested');assert.equal(result.signalled,false);
  assert.equal(new ResourceController(db).snapshot(task.taskId).reservations[0].state,'reserved');
  assert.equal(db.db.prepare('SELECT COUNT(*) AS n FROM project_leases').get()!.n,1);
  captureEvidence('budget-host-exited-child-alive','actual host exit and identity-bound detached child',{hostExitCode:host.status,child:result.process,state:result.state,reservation:'reserved',occupancy:1});
});
test('actual cancellation CLI uses a private host grant and requires an explicit signal action', {timeout:15_000},async t=>{
  const {root,file,db,task,child,closed}=await fixture(t);
  const grants=join(root,'grants');mkdirSync(grants,{mode:0o700});
  writeFileSync(join(grants,sha256(task.authorizationRef)+'.json'),JSON.stringify({schema:'filmcraft-local-authorization/v1',
    authorizationRef:task.authorizationRef,authorizationScopeSha256:task.authorizationScopeSha256,expiresAt:Date.now()+60_000,
    revoked:false,subjects:[sha256(stableJson(cancellationSubject(db,task.taskId)))]}),{mode:0o600});
  const base=[new URL('../../src/cli/recovery.ts',import.meta.url).pathname];
  const run=(action:string,extra:string[]=[])=>spawnSync(process.execPath,[...base,action,'--ledger',file,'--task',task.taskId,...extra],{encoding:'utf8',timeout:10_000});
  const requested=run('cancel',['--authorization-root',grants,'--authorization-ref',task.authorizationRef,'--authorization-scope-sha256',task.authorizationScopeSha256]);
  assert.equal(requested.status,0,requested.stdout+requested.stderr);assert.equal(groupState(child.pid!),'running');
  const observed=run('cancel-reconcile');assert.equal(observed.status,0,observed.stdout);assert.equal(JSON.parse(observed.stdout).signalled,false);
  const missingGrant=run('cancel-reconcile',['--signal']);assert.equal(missingGrant.status,1);assert.equal(groupState(child.pid!),'running');
  const signalled=run('cancel-reconcile',['--signal','--authorization-root',grants]);assert.equal(signalled.status,0,signalled.stdout);
  await closed;const confirmed=run('cancel-reconcile');assert.equal(confirmed.status,0,confirmed.stdout);
  assert.equal(JSON.parse(confirmed.stdout).state,'cancelled');
  captureEvidence('budget-cancel-private-cli','actual CLI, private grant and controlled POSIX process',{requestOnlyKeptRunning:true,unauthorizedSignalRefused:true,confirmed:'cancelled'});
});
