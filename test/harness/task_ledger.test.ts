import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, symlinkSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { binding, hash, workspace } from './fixtures.ts';

test('same idempotency key returns the original task; changed identity conflicts without replacing it', t => {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite'));
  t.after(() => db.close());
  const original = binding(root);
  db.register(original);
  assert.equal(db.register({ ...original, taskId: 'other-proposed-id' }).taskId, original.taskId);
  for (const changed of [{ planHash: hash('b') }, { sourceTreeSha256: hash('f') },
    { authorizationScopeSha256: hash('e') }, { runtimeIdentity: { ...original.runtimeIdentity, mode: 'bridge' } },
    { inputHashes: { media: hash() }, inputRefs: [{ assetId: 'media', version: 'one', sha256: hash() }] }]) {
    assert.throws(() => db.register({ ...original, ...changed }), /idempotency_conflict/);
  }
  assert.deepEqual(db.getTask(original.taskId).binding, original);
});

test('task IDs cannot overwrite another caller and input versions remain bound', t => {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite'));
  t.after(() => db.close());
  db.register(binding(root));
  assert.throws(() => db.register(binding(root, { namespace: 'other-host' })), /task_identity_conflict/);
  assert.throws(() => db.register(binding(root, { inputHashes: { media: hash() }, inputRefs: [] })), /input_identity_mismatch/);
});

test('project occupancy survives close/reopen and unknown execution does not free the writer', t => {
  const root = workspace(t), file = join(root, 'ledger.sqlite');
  let db = new TaskLedger(file);
  db.register(binding(root));
  const lease = db.claim('task-1', 'worker', 60_000);
  const attempt = db.beginAttempt(lease, 'native-workflow');
  assert.equal(attempt.fresh, true);
  assert.equal(db.beginAttempt(lease, 'native-workflow').fresh, false);
  db.finishAttempt(lease, { outcome: 'unknown', stopped: false, receiptSha256: null });
  db.close(); db = new TaskLedger(file); t.after(() => db.close());
  db.register(binding(root, { taskId: 'task-2', idempotencyKey: 'request-2', outputRoot: join(root, 'other-output') }));
  assert.throws(() => db.claim('task-2', 'worker-2', 60_000), /project_busy/);
  assert.equal(db.getTask('task-1').state, 'reconciling');
  assert.equal(db.listAttempts('task-1')[0].state, 'unknown');
  assert.throws(() => db.claim('task-1', 'worker', 60_000), /outcome_unknown/);
});

test('expired leases are fenced without automatically taking over or accepting an old completion', t => {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  db.register(binding(root));
  const now = Date.now(), lease = db.claim('task-1', 'worker', 20, now);
  db.beginAttempt(lease, 'native-workflow', now);
  assert.throws(() => db.claim('task-1', 'new-worker', 50, now + 21), /outcome_unknown/);
  assert.equal(db.getTask('task-1').state, 'reconciling');
  assert.ok(db.getTask('task-1').epoch > lease.epoch);
  assert.throws(() => db.finishAttempt(lease, { outcome: 'succeeded', stopped: true, receiptSha256: hash() }, now + 22), /stale_epoch/);
});

test('intent is committed before submission and accepted execution is not completed delivery', t => {
  const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file); t.after(() => db.close());
  db.register(binding(root)); const lease = db.claim('task-1', 'worker', 60_000);
  assert.throws(() => db.markSubmitted(lease, 123), /intent_missing/);
  db.beginAttempt(lease, 'workflow');
  const observer = new TaskLedger(file, { readOnly: true });
  assert.equal(observer.listAttempts('task-1')[0].state, 'intent'); observer.close();
  db.markSubmitted(lease, 123);
  db.finishAttempt(lease, { outcome: 'succeeded', stopped: true, receiptSha256: hash() });
  assert.equal(db.getTask('task-1').state, 'verifying');
  assert.notEqual(db.getTask('task-1').state, 'completed');
  db.register(binding(root, { taskId: 'task-2', idempotencyKey: 'request-2' }));
  assert.equal(db.claim('task-2', 'second-worker', 60_000).taskId, 'task-2');
});

test('missing stop confirmation remains unknown; receipts cannot be spliced across attempts', t => {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  db.register(binding(root)); const lease = db.claim('task-1', 'worker', 60_000); db.beginAttempt(lease, 'workflow');
  db.register(binding(root, { taskId: 'task-2', idempotencyKey: 'request-2', projectKey: hash('d'), outputRoot: join(root, 'second') }));
  const second = db.claim('task-2', 'worker-2', 60_000); db.beginAttempt(second, 'workflow');
  assert.throws(() => db.recordReceipt('task-1', second.attemptId, 'command', hash(), {}, 'linked'), /attempt_task_mismatch/);
  db.recordReceipt('task-1', lease.attemptId, 'command', hash(), {}, 'linked');
  assert.throws(() => db.recordReceipt('task-1', lease.attemptId, 'command', hash('b'), {}, 'linked'), /receipt_conflict/);
  assert.equal(db.receipts('task-1', lease.attemptId)[0].sha256, hash());
  db.finishAttempt(lease, { outcome: 'succeeded', stopped: false, receiptSha256: hash() });
  assert.equal(db.getTask('task-1').state, 'reconciling');
});

test('deadline and unsupported state database refuse execution without editing user files', t => {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  db.register(binding(root, { deadline: Date.now() - 1 }));
  assert.throws(() => db.claim('task-1', 'worker', 100), /deadline_exceeded/);
  assert.equal(db.listAttempts('task-1').length, 0);
  const file = join(root, 'user-file'); writeFileSync(file, 'not a ledger');
  assert.throws(() => new TaskLedger(file), /database|ledger/i);
  assert.equal(readFileSync(file, 'utf8'), 'not a ledger');
});

test('two actual processes cannot acquire the same project writer', async t => {
  const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file);
  db.register(binding(root)); db.close();
  const url = new URL('../../src/harness/task_ledger.ts', import.meta.url).href;
  const code = `import {TaskLedger} from ${JSON.stringify(url)};const db=new TaskLedger(process.argv[1]);try{db.claim('task-1',process.argv[2],60000);console.log('CLAIMED')}catch(e){console.log(e.code)}finally{db.close()}`;
  function child(owner: string) { return new Promise<string>((resolve, reject) => {
    const child = spawn(process.execPath, ['--input-type=module', '-e', code, file, owner]);
    let output = '', error = ''; child.stdout.on('data', x => output += x); child.stderr.on('data', x => error += x);
    child.on('error', reject); child.on('exit', code => code === 0 ? resolve(output.trim()) : reject(new Error(error)));
  }); }
  const results = await Promise.all([child('one'), child('two')]);
  assert.equal(results.filter(x => x === 'CLAIMED').length, 1);
  assert.equal(results.filter(x => x === 'lease_busy').length, 1);
});

test('aliased output parents share idempotency and occupancy even with a different project key', t => {
  const root = workspace(t), real = join(root, 'real'), alias = join(root, 'alias');
  mkdirSync(real); symlinkSync(real, alias);
  const db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  const task = binding(root, { outputRoot: join(alias, 'new', 'delivery') });
  const stored = db.register(task);
  assert.equal(stored.binding.outputRoot, join(real, 'new', 'delivery'));
  assert.equal(db.register({ ...task, outputRoot: join(real, 'new', 'delivery') }).taskId, task.taskId);
  db.claim(task.taskId, 'first', 60_000);
  db.register({ ...task, taskId: 'other', idempotencyKey: 'other', projectKey: hash('d') });
  assert.throws(() => db.claim('other', 'second', 60_000), /output_busy/);
});

test('an unrelated SQLite database with user_version 1 is rejected without changing its bytes', t => {
  const root = workspace(t), file = join(root, 'foreign.sqlite'), foreign = new DatabaseSync(file);
  foreign.exec('CREATE TABLE user_data(content TEXT); INSERT INTO user_data VALUES(\'keep\'); PRAGMA user_version=1');
  foreign.close(); const before = readFileSync(file);
  assert.throws(() => new TaskLedger(file), /ledger_schema_unknown/);
  assert.deepEqual(readFileSync(file), before);
  assert.throws(() => new TaskLedger(file, { readOnly: true }), /ledger_schema_unknown/);
});
