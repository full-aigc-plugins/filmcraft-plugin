import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ResourceController } from '../../src/harness/resources.ts';
import { binding, workspace, captureEvidence } from './fixtures.ts';
import { spawn } from 'node:child_process';
import { once } from 'node:events';

const limits = { timeMs: 60_000, diskBytes: 100_000, outputBytes: 100_000, slots: 1, revisions: 1 };
const allocation = { timeMs: 10_000, diskBytes: 10_000, outputBytes: 10_000, slots: 1, revisions: 0 };
function fixture(t: Parameters<typeof workspace>[0]) {
  const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file);
  t.after(() => db.close());
  const task = binding(root); db.register(task);
  const resources = new ResourceController(db, { freeBytes: () => 1_000_000 });
  return { root, file, db, task, resources };
}
test('reservations survive reopening without a second charge; unknown retains concurrency and disk', t => {
  const { file, db, task, resources } = fixture(t);
  resources.reserve(task.taskId, { limits, allocation });
  const reopened = new TaskLedger(file); t.after(() => reopened.close());
  const restarted = new ResourceController(reopened);
  assert.equal(restarted.reserve(task.taskId, { limits, allocation }).reused, true);
  assert.equal(restarted.snapshot(task.taskId).reservations.length, 1);
  const lease = db.claim(task.taskId, 'owner', 1000); db.beginAttempt(lease, 'operation');
  db.finishAttempt(lease, { outcome: 'unknown', stopped: false, receiptSha256: null });
  assert.throws(() => restarted.settle(task.taskId, { stopped: false, outputBytes: 2 }), /native_stop_unconfirmed/);
  assert.equal(restarted.snapshot(task.taskId).reservations[0].state, 'reserved');
  captureEvidence('budget-restart-unknown','actual reopened SQLite with synthetic unknown attempt',{reservations:1,reused:true,state:'reserved',releaseRefused:true});
});
for (const [field, value, error] of [
  ['timeMs', 60_001, 'budget_time_exceeded'], ['diskBytes', 100_001, 'budget_disk_exceeded'],
  ['outputBytes', 100_001, 'budget_output_exceeded'], ['slots', 2, 'budget_concurrency_exceeded'],
  ['revisions', 2, 'budget_revisions_exceeded'],
] as const) {
  test('deterministic rejection for ' + field + ' preserves reason and starts no attempt', t => {
    const { db, task, resources } = fixture(t);
    assert.throws(() => resources.reserve(task.taskId, { limits, allocation: { ...allocation, [field]: value } }), new RegExp(error));
    assert.equal(resources.snapshot(task.taskId).reason, error);
    assert.equal(db.listAttempts(task.taskId).length, 0);
    captureEvidence('budget-limit-'+field,'deterministic quota boundary',{refused:error,attempts:0,persistedReason:resources.snapshot(task.taskId).reason});
  });
}
test('physical disk shortage rejects before reservation even when numeric quota permits it', t => {
  const { db, task } = fixture(t), resources = new ResourceController(db, { freeBytes: () => 1 });
  assert.throws(() => resources.reserve(task.taskId, { limits, allocation }), /disk_space_insufficient/);
  assert.equal(resources.snapshot(task.taskId).reservations.length, 0);
  captureEvidence('budget-disk-shortage','fault injected available-byte probe',{freeBytes:1,refused:'disk_space_insufficient',reservations:0});
});
test('parent and child share reservation, deadline, concurrency and revision count', t => {
  const { root, db, task, resources } = fixture(t);
  resources.reserve(task.taskId, { limits, allocation });
  const child = binding(root, { taskId: 'child', idempotencyKey: 'child', projectKey: 'f'.repeat(64), outputRoot: join(root, 'child'), deadline: task.deadline + 100_000 }); db.register(child);
  assert.throws(() => resources.reserve(child.taskId, { allocation }, task.taskId), /budget_concurrency_exceeded/);
  const lease = db.claim(task.taskId, 'owner', 1000); db.beginAttempt(lease, 'operation');
  db.finishAttempt(lease, { outcome: 'failed', stopped: true, receiptSha256: null });
  resources.settle(task.taskId, { stopped: true, outputBytes: 5 });
  resources.reserve(child.taskId, { allocation: { ...allocation, revisions: 1 } }, task.taskId);
  const snap = resources.snapshot(child.taskId);
  assert.equal(snap.scopeId, task.taskId); assert.equal(snap.deadline, task.deadline);
  assert.equal(snap.reservations.length, 2);
  resources.halt(task.taskId, 'budget_output_exceeded');
  assert.throws(() => db.claim(child.taskId, 'child-owner', 1000), /budget_output_exceeded/);
  captureEvidence('budget-parent-child','actual SQLite parent-child shared reservation',{sameScope:true,sharedDeadline:true,reservations:2,dependencyRefused:'budget_output_exceeded'});
});
test('expired time reservation halts new dependencies without releasing unknown work', t => {
  const { task, resources } = fixture(t);
  resources.reserve(task.taskId, { limits, allocation });
  const snap = resources.snapshot(task.taskId);
  assert.equal(resources.observe(task.taskId, 0, snap.reservations[0].reserved_at + allocation.timeMs + 1), 'budget_time_exceeded');
  assert.equal(resources.snapshot(task.taskId).reservations[0].state, 'reserved');
});
test('schema4 forensic integrity rejects altered consumed accounting before trusting recovered reservations', t => {
  const { db, task, resources } = fixture(t);
  resources.reserve(task.taskId, { limits, allocation });
  db.db.prepare("UPDATE task_resources SET state='settled',consumed=? WHERE task_id=?").run('{"timeMs":-1}', task.taskId);
  assert.throws(() => db.verifyIntegrity(), /ledger_resource_corrupt/);
});
test('an actual killed reservation owner cannot reset durable charges or create a second reservation', { timeout: 15_000 }, async t => {
  const root = workspace(t), file = join(root, 'crashed.sqlite'), task = binding(root);
  const ledgerModule = new URL('../../src/harness/task_ledger.ts', import.meta.url).href;
  const resourcesModule = new URL('../../src/harness/resources.ts', import.meta.url).href;
  const program = `import {TaskLedger} from ${JSON.stringify(ledgerModule)}; import {ResourceController} from ${JSON.stringify(resourcesModule)};
    const db=new TaskLedger(process.argv[1]); const task=JSON.parse(process.argv[2]); db.register(task);
    new ResourceController(db).reserve(task.taskId,JSON.parse(process.argv[3])); console.log('reserved'); setInterval(()=>{},1000);`;
  const owner = spawn(process.execPath, ['--input-type=module', '-e', program, file, JSON.stringify(task), JSON.stringify({ limits, allocation })], { stdio: ['ignore','pipe','pipe'] });
  const closed = once(owner, 'close');
  t.after(async () => { if (owner.exitCode === null && owner.signalCode === null) { owner.kill('SIGKILL'); } await closed; });
  const [ready] = await once(owner.stdout!, 'data'); assert.equal(ready.toString().trim(), 'reserved');
  owner.kill('SIGKILL'); await closed;
  const db = new TaskLedger(file); t.after(() => db.close()); const resource = new ResourceController(db);
  assert.equal(resource.reserve(task.taskId, { limits, allocation }).reused, true);
  assert.equal(resource.snapshot(task.taskId).reservations.length, 1);
  captureEvidence('budget-reservation-owner-killed','actual SIGKILL after durable reservation',{ownerSignal:'SIGKILL',reused:true,reservations:1});
});
