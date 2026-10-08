import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { WorkflowAdmission, executionSubject } from '../../src/harness/workflow_admission.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { binding, fixtureAuthorizer, workspace } from './fixtures.ts';

function setup(t: any, authorize?: any, hook?: () => void) {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite'));
  t.after(() => db.close());
  const options = { skillDirectory: join(root, 'absent-skill'), sourceRevision: 'd'.repeat(40),
    runtimeHome: join(root, 'runtime'), pluginVersion: 'test', beforeDispatch: hook };
  return { root, db, task: binding(root), service: new WorkflowAdmission(db, new ReceiptIndex(db, join(root, 'blobs')), options, authorize) };
}

test('initial admission refuses missing host authority before preflight, installation or task registration', async t => {
  const f = setup(t);
  await assert.rejects(f.service.run(f.task, join(f.root, 'absent-plan')), /authorization_verifier_required/);
  assert.throws(() => f.db.getTask(f.task.taskId), /task_missing/);
  assert.equal(existsSync(join(f.root, 'runtime')), false);
});

test('execution authorization binds every task identity dimension instead of trusting a reference', t => {
  const task = binding(workspace(t)), subject = executionSubject(task);
  assert.equal(subject.action, 'execute');
  for (const delta of [{ planHash: '1'.repeat(64) }, { projectRevision: '2'.repeat(64) },
    { inputHashes: { media: '3'.repeat(64) } }, { runtimeIdentity: { ...task.runtimeIdentity, cliVersion: 'changed' } },
    { authorizationScopeSha256: '4'.repeat(64) }, { outputRoot: join(task.outputRoot, 'other') },
    { sourceRevision: '5'.repeat(40) }, { deadline: task.deadline + 1 }]) {
    assert.notEqual(executionSubject({ ...task, ...delta }).identitySha256, subject.identitySha256);
  }
});

test('expired and mismatched execution decisions refuse admission without claiming an attempt', async t => {
  for (const decision of [(subject: any, request: any) => ({ ...fixtureAuthorizer(subject, request), expiresAt: 1 }),
    (subject: any, request: any) => ({ ...fixtureAuthorizer(subject, request), subjectSha256: '0'.repeat(64) })]) {
    const f = setup(t, decision);
    await assert.rejects(f.service.run(f.task, 'unused'), /authorization_expired|authorization_scope_change_required/);
    assert.throws(() => f.db.getTask(f.task.taskId), /task_missing/);
  }
});

test('revocation in host dispatch hook is re-read before any preflight or native launch', async t => {
  let revoked = false, checks = 0;
  const f = setup(t, (subject: any, request: any) => { checks++; return revoked ? null : fixtureAuthorizer(subject, request); }, () => { revoked = true; });
  await assert.rejects(f.service.run(f.task, 'unused'), /authorization_required/);
  assert.ok(checks >= 3);
  assert.throws(() => f.db.getTask(f.task.taskId), /task_missing/);
  assert.equal(existsSync(join(f.root, 'runtime')), false);
});

test('a valid exact execute decision reaches the adapter without granting other subjects', async t => {
  let expected: string;
  const f = setup(t, (subject: any, request: any) => {
    assert.equal(sha256(stableJson(subject)), expected);
    return fixtureAuthorizer(subject, request);
  }, () => { throw new Error('authorized_adapter_boundary'); });
  expected = sha256(stableJson(executionSubject(f.task)));
  await assert.rejects(f.service.run(f.task, 'unused'), /authorized_adapter_boundary/);
  assert.throws(() => f.db.getTask(f.task.taskId), /task_missing/);
});

test('workflow CLI computes a subject read-only and refuses missing authority before creating a ledger', async t => {
  const { spawnSync } = await import('node:child_process');
  const { writeFileSync } = await import('node:fs');
  const root = workspace(t), task = binding(root), file = join(root, 'binding.json'), ledger = join(root, 'absent.sqlite');
  writeFileSync(file, JSON.stringify(task));
  const cli = new URL('../../src/cli/workflow.ts', import.meta.url).pathname;
  const subject = spawnSync(process.execPath, [cli, 'subject', '--binding', file], { encoding: 'utf8' });
  assert.equal(subject.status, 0, subject.stderr);
  assert.deepEqual(JSON.parse(subject.stdout), executionSubject(task));
  const policy = join(root, 'resources.json'); writeFileSync(policy, JSON.stringify({ limits: {}, allocation: {} }));
  const run = spawnSync(process.execPath, [cli, 'run', '--binding', file, '--resources', policy, '--plan', 'absent', '--ledger', ledger,
    '--blobs', join(root, 'blobs'), '--authorization-root', join(root, 'grants'), '--runtime-home', join(root, 'runtime')], { encoding: 'utf8' });
  assert.equal(run.status, 1);
  assert.equal(JSON.parse(run.stdout).error.code, 'authorization_required');
  assert.equal(existsSync(ledger), false);
  assert.equal(existsSync(join(root, 'runtime')), false);
});


test('resource policy is part of the exact execution grant', t => {
  const task = binding(workspace(t));
  const policy = { limits: { timeMs: 1000, diskBytes: 1000, outputBytes: 1000, slots: 1, revisions: 0 },
    allocation: { timeMs: 1000, diskBytes: 1000, outputBytes: 1000, slots: 1, revisions: 0 } };
  assert.notEqual(executionSubject(task, policy).identitySha256, executionSubject(task).identitySha256);
  assert.notEqual(executionSubject(task, policy).identitySha256,
    executionSubject(task, { ...policy, limits: { ...policy.limits, outputBytes: 2000 } }).identitySha256);
});
