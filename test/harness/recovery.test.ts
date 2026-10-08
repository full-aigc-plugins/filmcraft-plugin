import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { RecoveryService } from '../../src/harness/recovery.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { normalizePlan } from '../../src/adapters/plan_identity.ts';
import { binding, hash, workspace } from './fixtures.ts';

function files(root: string) {
  const result: Record<string, string> = {};
  function walk(path: string) {
    for (const name of readdirSync(path, { withFileTypes: true })) {
      const file = join(path, name.name);
      if (name.isDirectory()) { walk(file); }
      else { result[relative(root, file)] = sha256(readFileSync(file)); }
    }
  }
  walk(root); return result;
}
function unknownTask(t: Parameters<typeof workspace>[0]) {
  const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file);
  t.after(() => db.close()); const task = binding(root); db.register(task);
  const lease = db.claim(task.taskId, 'worker', 60_000); db.beginAttempt(lease, 'native-workflow');
  db.finishAttempt(lease, { outcome: 'unknown', stopped: false, receiptSha256: null });
  return { root, file, db, task, lease, service: new RecoveryService(file, join(root, 'missing-blobs')) };
}

test('read-only diagnosis sees committed WAL state without changing database, sidecars, projects or missing blob directories', t => {
  const { root, db, task, service } = unknownTask(t);
  const before = files(root), inspection = service.inspect(task.taskId);
  assert.equal(inspection.task?.state, 'reconciling'); assert.equal(inspection.diagnosis, 'unknown');
  assert.equal(inspection.replayAllowed, false); assert.deepEqual(files(root), before);
  assert.equal(existsSync(join(root, 'missing-blobs')), false);
  assert.throws(() => service.repair(task.taskId, { expectedEpoch: inspection.task!.epoch,
    inspectionSha256: inspection.evidenceSha256, authorizationRef: task.authorizationRef,
    authorizationScopeSha256: task.authorizationScopeSha256 }), /outcome_unknown/);
  assert.deepEqual(files(root), before);
  assert.equal(db.getTask(task.taskId).state, 'reconciling');
});

test('damaged database and missing receipts remain structured unknown and never create or overwrite state', t => {
  const root = workspace(t), file = join(root, 'broken.sqlite'); writeFileSync(file, 'preserve damaged state');
  const service = new RecoveryService(file, join(root, 'blobs')), before = files(root);
  assert.equal(service.inspect('task-1').diagnosis, 'unknown');
  assert.ok(service.inspect('task-1').error); assert.deepEqual(files(root), before);
  const missing = new RecoveryService(join(root, 'absent.sqlite'), join(root, 'blobs'));
  assert.equal(missing.inspect('task-1').diagnosis, 'unknown'); assert.deepEqual(files(root), before);
});

test('an actually running detached process remains occupied after its host state becomes unknown', async t => {
  const { root, file, db, task, service } = unknownTask(t);
  // 独立子进程模拟宿主退出后仍在运行的原生任务；只结束本测试创建的进程。
  const child = spawn(process.execPath, ['-e', 'process.stdout.write("READY\\n");setInterval(()=>{},1000)'], { detached: true, stdio: ['ignore', 'pipe', 'pipe'] });
  await new Promise<void>((resolve, reject) => { child.stdout!.once('data', () => resolve()); child.once('error', reject); });
  t.after(() => { try { process.kill(-child.pid!, 'SIGTERM'); } catch {} });
  db.db.prepare('UPDATE attempts SET pid=? WHERE attempt_id=?').run(child.pid!, db.getTask(task.taskId).attemptId);
  const before = files(root), observation = service.inspect(task.taskId);
  assert.equal(observation.process.status, 'alive'); assert.equal(observation.diagnosis, 'running');
  assert.deepEqual(files(root), before); assert.equal(db.getTask(task.taskId).state, 'reconciling');
  assert.throws(() => service.repair(task.taskId, { expectedEpoch: observation.task!.epoch,
    inspectionSha256: observation.evidenceSha256, authorizationRef: task.authorizationRef,
    authorizationScopeSha256: task.authorizationScopeSha256 }), /outcome_unknown/);
  db.register(binding(root, { taskId: 'other', idempotencyKey: 'other', outputRoot: join(root, 'other') }));
  assert.throws(() => db.claim('other', 'another', 1000), /project_busy/);
  process.kill(-child.pid!, 'SIGTERM'); await new Promise(resolve => child.once('close', resolve));
});

function lostReply(t: Parameters<typeof workspace>[0]) {
  const root = workspace(t), output = join(root, 'delivery'); mkdirSync(output);
  const plan = { schema: 'fixture-only/v1' }, caps = { schema: 'filmcraft-capability-snapshot/v1', mode: 'headless' };
  const payloads = { 'plan.json': JSON.stringify(plan), 'project.fcproj': 'fixture project; no native acceptance', 'capabilities.json': JSON.stringify(caps) };
  for (const [name, text] of Object.entries(payloads)) { writeFileSync(join(output, name), text); }
  const identity = normalizePlan(join(output, 'plan.json')), base = binding(root);
  const task = { ...base, planHash: identity.canonicalPlanSha256, nativePlanHash: identity.workflowPlanSha256,
    runtimeIdentity: { ...base.runtimeIdentity, capabilitySnapshotSha256: sha256(stableJson(caps)) } };
  const dbFile = join(root, 'ledger.sqlite'), db = new TaskLedger(dbFile); t.after(() => db.close());
  db.register(task); const lease = db.claim(task.taskId, 'original', 60_000); db.beginAttempt(lease, 'workflow');
  const process = spawnSync(globalThis.process.execPath, ['-e', '']); assert.equal(process.status, 0);
  db.markSubmitted(lease, process.pid!);
  writeFileSync(join(output, 'manifest.json'), JSON.stringify({ schema: 'filmcraft-delivery/v1', runtimeSha256: task.runtimeIdentity.sha256,
    sourceProjectSha256: null, assets: {}, files: Object.fromEntries(Object.entries(payloads).map(([name,text]) => [name,sha256(text)])) }));
  const guard = '.filmcraft-execution-' + sha256(task.outputRoot) + '.json';
  writeFileSync(join(root, guard), JSON.stringify({ schema: 'filmcraft-output-execution/v1', targetHash: sha256(task.outputRoot),
    state: 'finished', ownerPid: process.pid, identity: { planHash: task.nativePlanHash, inputHashes: {}, projectRevision: null, runtimeSha256: task.runtimeIdentity.sha256 } }));
  db.finishAttempt(lease, { outcome: 'unknown', stopped: true, receiptSha256: null });
  const service = new RecoveryService(dbFile, join(root, 'blobs'));
  return { root, output, db, dbFile, task, lease, service, guard };
}

test('lost replies are diagnosed without writes and repaired only with fresh evidence, matching authorization and fenced intent', t => {
  const { root, output, db, task, lease, service } = lostReply(t);
  assert.equal(db.getTask(task.taskId).state, 'reconciling');
  const before = files(root), inspection = service.inspect(task.taskId);
  assert.equal(inspection.diagnosis, 'executed'); assert.equal(inspection.process.status, 'stopped');
  assert.deepEqual(files(root), before);
  const request = { expectedEpoch: inspection.task!.epoch, inspectionSha256: inspection.evidenceSha256,
    authorizationRef: task.authorizationRef, authorizationScopeSha256: task.authorizationScopeSha256 };
  assert.throws(() => service.repair(task.taskId, { ...request, authorizationRef: 'other-grant' }), /authorization_required/);
  assert.throws(() => service.repair(task.taskId, { ...request, expectedEpoch: inspection.task!.epoch - 1 }), /stale_epoch/);
  assert.deepEqual(files(root), before);
  const result = service.repair(task.taskId, request);
  assert.equal(result.state, 'verifying'); assert.equal(result.attemptId, lease.attemptId);
  assert.equal(result.replayed, false); assert.equal(result.receipt.technicalAcceptance, 'NOT_RUN');
  assert.equal(readFileSync(join(output, 'project.fcproj'), 'utf8'), 'fixture project; no native acceptance');
  assert.equal(db.listAttempts(task.taskId).length, 1); assert.equal(db.listRecoveryIntents(task.taskId)[0].state, 'applied');
  assert.throws(() => db.finishAttempt(lease, { outcome: 'succeeded', stopped: true, receiptSha256: hash() }), /stale_epoch/);
  db.register(binding(root, { taskId: 'new', idempotencyKey: 'new', outputRoot: join(root, 'revision') }));
  assert.equal(db.claim('new', 'new-worker', 1000).taskId, 'new');
});

test('changed candidate, missing export record or missing process identity cannot unlock or repair an unknown task', t => {
  const { root, output, db, task, service, guard } = lostReply(t);
  const inspection = service.inspect(task.taskId), request = { expectedEpoch: inspection.task!.epoch,
    inspectionSha256: inspection.evidenceSha256, authorizationRef: task.authorizationRef, authorizationScopeSha256: task.authorizationScopeSha256 };
  writeFileSync(join(output, 'project.fcproj'), 'changed');
  assert.throws(() => service.repair(task.taskId, request), /inspection_stale|outcome_unknown/);
  writeFileSync(join(output, 'project.fcproj'), 'fixture project; no native acceptance');
  const record = JSON.parse(readFileSync(join(root, guard), 'utf8')); record.ownerPid += 1;
  writeFileSync(join(root, guard), JSON.stringify(record));
  assert.equal(service.inspect(task.taskId).diagnosis, 'unknown');
  record.ownerPid -= 1; rmSync(join(root, guard));
  assert.equal(service.inspect(task.taskId).diagnosis, 'unknown');
  writeFileSync(join(root, guard), JSON.stringify(record));
  db.db.prepare('UPDATE attempts SET pid=NULL WHERE attempt_id=?').run(db.getTask(task.taskId).attemptId);
  assert.equal(service.inspect(task.taskId).diagnosis, 'unknown');
  assert.equal(db.getTask(task.taskId).state, 'reconciling'); assert.equal(db.listRecoveryIntents(task.taskId).length, 0);
});

test('recovery intent survives reopening; an active or expired old recovery owner cannot commit', async t => {
  const { db, dbFile, task, service } = lostReply(t);
  const first = service.inspect(task.taskId), now = Date.now();
  const lease = db.beginRecovery(task.taskId, first.task!.epoch, first.evidenceSha256, 'repair-owner', 20, now);
  const reader = new TaskLedger(dbFile, { readOnly: true });
  assert.equal(reader.listRecoveryIntents(task.taskId)[0].state, 'pending'); reader.close();
  assert.throws(() => db.beginRecovery(task.taskId, lease.epoch, first.evidenceSha256, 'competing', 20, now + 1), /recovery_busy/);
  const second = db.beginRecovery(task.taskId, lease.epoch, first.evidenceSha256, 'fresh-owner', 20, now + 21);
  assert.throws(() => db.finishRecovery(lease, hash(), hash(), hash(), now + 22), /stale_epoch/);
  assert.throws(() => db.finishRecovery(second, hash(), hash(), hash(), now + 22), /recovery_evidence_missing/);
  assert.deepEqual(db.listRecoveryIntents(task.taskId).map(row => row.state), ['abandoned', 'pending']);
  assert.equal(db.getTask(task.taskId).state, 'reconciling');
});

test('legacy ledger snapshots remain read-only and an explicit writer upgrades without replacing task or attempt identities', t => {
  const root = workspace(t), file = join(root, 'ledger.sqlite'); let db = new TaskLedger(file);
  db.register(binding(root)); const lease = db.claim('task-1', 'worker', 60_000); db.beginAttempt(lease, 'workflow');
  db.finishAttempt(lease, { outcome: 'unknown', stopped: false, receiptSha256: null });
  db.db.exec('DROP TABLE recovery_intents; PRAGMA user_version=1'); db.close();
  const before = files(root), service = new RecoveryService(file, join(root, 'blobs'));
  const inspected = service.inspect('task-1'); assert.equal(inspected.task?.attemptId, lease.attemptId);
  assert.deepEqual(files(root), before);
  db = new TaskLedger(file); t.after(() => db.close());
  assert.equal((db.db.prepare('PRAGMA user_version').get() as any).user_version, 2);
  assert.equal(db.getTask('task-1').attemptId, lease.attemptId); assert.equal(db.getTask('task-1').state, 'reconciling');
  assert.equal(db.listRecoveryIntents('task-1').length, 0);
});

test('CLI inspect and reconcile are both read-only; unknown diagnosis is explicit', t => {
  const { root, file, task } = unknownTask(t), before = files(root);
  const cli = new URL('../../src/cli/recovery.ts', import.meta.url);
  for (const action of ['inspect', 'reconcile']) {
    const result = spawnSync(process.execPath, [cli.pathname, action, '--ledger', file, '--blobs', join(root, 'blobs'), '--task', task.taskId], { encoding: 'utf8' });
    assert.equal(result.status, 2, result.stderr);
    assert.equal(JSON.parse(result.stdout).diagnosis, 'unknown'); assert.deepEqual(files(root), before);
  }
});

test('freshly requested repair of an already reconciled attempt is read-only and does not create another recovery intent', t => {
  const { root, db, task, service } = lostReply(t);
  function request() { const observation = service.inspect(task.taskId); return { expectedEpoch: observation.task!.epoch,
    inspectionSha256: observation.evidenceSha256, authorizationRef: task.authorizationRef, authorizationScopeSha256: task.authorizationScopeSha256 }; }
  service.repair(task.taskId, request());
  const fresh = request(), before = files(root), reused = service.repair(task.taskId, fresh);
  assert.equal(reused.reused, true); assert.equal(reused.replayed, false); assert.equal(reused.state, 'verifying');
  assert.deepEqual(files(root), before); assert.equal(db.listRecoveryIntents(task.taskId).length, 1);
});

test('two actual recovery processes cannot apply the same uncertain attempt twice', async t => {
  const { root, dbFile, db, task, service } = lostReply(t), observation = service.inspect(task.taskId);
  const request = { expectedEpoch: observation.task!.epoch, inspectionSha256: observation.evidenceSha256,
    authorizationRef: task.authorizationRef, authorizationScopeSha256: task.authorizationScopeSha256 };
  const url = new URL('../../src/harness/recovery.ts', import.meta.url).href;
  const code = `import {RecoveryService} from ${JSON.stringify(url)};const s=new RecoveryService(process.argv[1],process.argv[2]);try{s.repair(process.argv[3],JSON.parse(process.argv[4]));console.log('APPLIED')}catch(e){console.log(e.code)}`;
  function child() { return new Promise<string>((resolve, reject) => {
    const process = spawn(globalThis.process.execPath, ['--input-type=module', '-e', code, dbFile, join(root, 'blobs'), task.taskId, JSON.stringify(request)]);
    let stdout = '', stderr = ''; process.stdout!.on('data', value => stdout += value); process.stderr!.on('data', value => stderr += value);
    process.on('error', reject); process.on('close', code => code === 0 ? resolve(stdout.trim()) : reject(new Error(stderr)));
  }); }
  const results = await Promise.all([child(), child()]);
  assert.equal(results.filter(value => value === 'APPLIED').length, 1, JSON.stringify(results));
  assert.equal(db.getTask(task.taskId).state, 'verifying');
  assert.equal(db.listRecoveryIntents(task.taskId).filter(value => value.state === 'applied').length, 1);
  assert.equal(db.listAttempts(task.taskId).length, 1);
});

test('logical task identity corruption is diagnosed as unknown without rewriting corrupt bytes', t => {
  const { root, db, task, service } = unknownTask(t);
  db.db.prepare("UPDATE tasks SET binding='{}' WHERE task_id=?").run(task.taskId);
  const before = files(root), observed = service.inspect(task.taskId);
  assert.equal(observed.diagnosis, 'unknown'); assert.equal(observed.error?.code, 'invalid_task_binding');
  assert.deepEqual(files(root), before);
});
