import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { mkdirSync, readFileSync, writeFileSync, symlinkSync } from 'node:fs';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { normalizePlan } from '../../src/adapters/plan_identity.ts';
import { sha256, parseJson, stableJson } from '../../src/support/json.ts';
import { binding, hash, workspace } from './fixtures.ts';

function setup(t: Parameters<typeof workspace>[0]) {
  const root = workspace(t), output = join(root, 'delivery'); mkdirSync(output);
  const plan = join(root, 'input.json'); writeFileSync(plan, '{"name":"中文","time":9007199254740993,"operations":[]}');
  const identity = normalizePlan(plan);
  const db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  const task = binding(root, { planHash: identity.canonicalPlanSha256, nativePlanHash: identity.commandPlanSha256 });
  db.register(task); const lease = db.claim(task.taskId, 'worker', 60_000); db.beginAttempt(lease, 'native');
  const index = new ReceiptIndex(db, join(root, 'blobs'));
  return { root, output, task, lease, db, index, identity };
}

test('legacy command receipt is linked without rewriting native integers or declaring completion', t => {
  const { output, task, lease, db, index, identity } = setup(t);
  const raw = '{"schema":"craft-command-receipt/v1","planSha256":"' + identity.commandPlanSha256
    + '","runtimeSha256":"' + task.runtimeIdentity.sha256 + '","mode":"headless","inputs":{},"result":"PASS","steps":[{"id":9007199254740993}]}';
  writeFileSync(join(output, 'success.json'), raw);
  const linked = index.ingest(task.taskId, lease.attemptId, 'command', 'success.json');
  assert.equal(linked.status, 'linked'); assert.equal(linked.sha256, sha256(Buffer.from(raw)));
  assert.equal(readFileSync(index.blobPath(linked.sha256), 'utf8'), raw);
  assert.equal(db.getTask(task.taskId).state, 'running');
  assert.equal(index.collect(task.taskId, lease.attemptId).technicalAcceptance, 'NOT_RUN');
});

test('conflicting identity, absent identity and duplicate JSON keys cannot become a successful receipt', t => {
  const { output, task, lease, index } = setup(t);
  for (const [name, value, expected] of [
    ['conflict', { schema: 'craft-command-receipt/v1', planSha256: hash('f'), runtimeSha256: task.runtimeIdentity.sha256, mode: 'headless', inputs: {}, result: 'PASS' }, 'conflict'],
    ['legacy', { schema: 'craft-command-receipt/v1', result: 'PASS' }, 'unknown'],
  ] as const) {
    writeFileSync(join(output, name + '.json'), JSON.stringify(value));
    assert.equal(index.inspect(task.taskId, lease.attemptId, 'command', name + '.json').status, expected);
  }
  writeFileSync(join(output, 'duplicate.json'), '{"schema":"bad","schema":"craft-command-receipt/v1"}');
  assert.throws(() => index.ingest(task.taskId, lease.attemptId, 'command', 'duplicate.json'), /duplicate_json_key/);
  assert.throws(() => index.collect(task.taskId, 'another-attempt'), /attempt_task_mismatch/);
});

test('a moved or replaced candidate makes evidence stale and does not overwrite stored originals', t => {
  const { output, task, lease, db, index, identity } = setup(t);
  writeFileSync(join(output, 'success.json'), JSON.stringify({ schema: 'craft-command-receipt/v1',
    planSha256: identity.commandPlanSha256, runtimeSha256: task.runtimeIdentity.sha256, mode: 'headless', inputs: {}, result: 'PASS' }));
  const before = index.ingest(task.taskId, lease.attemptId, 'command', 'success.json');
  writeFileSync(join(output, 'success.json'), '{}');
  assert.equal(index.collect(task.taskId, lease.attemptId).status, 'stale');
  assert.equal(db.receipts(task.taskId, lease.attemptId)[0].sha256, before.sha256);
  assert.equal(JSON.parse(readFileSync(index.blobPath(before.sha256), 'utf8')).result, 'PASS');
});

test('receipt paths reject traversal and symlinks before reading their targets', t => {
  const { root, output, task, lease, index } = setup(t);
  writeFileSync(join(root, 'outside.json'), '{"secret":"must-not-read"}');
  symlinkSync(join(root, 'outside.json'), join(output, 'linked.json'));
  for (const path of ['../outside.json', 'linked.json']) {
    assert.throws(() => index.ingest(task.taskId, lease.attemptId, 'command', path), /unsafe_receipt_path/);
  }
});

test('strict lossless parsing preserves unsafe native integers and rejects ambiguity', () => {
  assert.equal(parseJson('{"id":9007199254740993}').id, '9007199254740993');
  assert.equal(parseJson('{"id":18446744073709551615}').id, '18446744073709551615');
  for (const raw of ['{"nested":{"id":1,"id":2}}', '{"v":NaN}', '{"x":01}', '[1,]', '{"a":1}garbage']) {
    assert.throws(() => parseJson(raw), /json/);
  }
  const data = parseJson('{"__proto__":{"polluted":true}}');
  assert.equal(Object.prototype.hasOwnProperty.call(data, '__proto__'), true);
  assert.equal(({} as any).polluted, undefined);
});

test('plan normalization keeps Python native hashes compatible and refuses duplicate or nonfinite values', t => {
  const root = workspace(t), path = join(root, 'plan.json');
  writeFileSync(path, '{"time":9007199254740993,"name":"中文"}');
  const first = normalizePlan(path);
  writeFileSync(path, '{"name":"中文", "time":9007199254740993}');
  const second = normalizePlan(path);
  assert.equal(first.commandPlanSha256, second.commandPlanSha256);
  assert.equal(first.canonicalPlanSha256, second.canonicalPlanSha256);
  assert.notEqual(first.fileSha256, second.fileSha256);
  for (const raw of ['{"x":1,"x":2}', '{"x":NaN}']) {
    writeFileSync(path, raw); assert.throws(() => normalizePlan(path), /invalid_plan/);
  }
});

function delivery(t: Parameters<typeof workspace>[0], inherited = false) {
  const root = workspace(t), output = join(root, 'delivery'); mkdirSync(output); mkdirSync(join(output, 'assets'));
  const media = Buffer.from('unit-fixture-media; no media acceptance claimed'), mediaHash = sha256(media);
  const plan = { schema: 'fixture-domain-plan/v1', ...(inherited ? {} : { assets: { still: { path: 'input.png', sha256: mediaHash } } }) };
  const snapshot = { schema: 'filmcraft-capability-snapshot/v1', mode: 'headless', fixture: true };
  const files: Record<string, Buffer> = {
    'plan.json': Buffer.from(JSON.stringify(plan)), 'project.fcproj': Buffer.from('fixture-native-project; not a real project'),
    'assets/still.png': media, 'capabilities.json': Buffer.from(JSON.stringify({ ...snapshot, commandChecks: [], resourceChecks: [] })),
    'exchange-loss.json': Buffer.from('{}'),
  };
  for (const [name, bytes] of Object.entries(files)) { writeFileSync(join(output, name), bytes); }
  const identity = normalizePlan(join(output, 'plan.json'));
  const base = binding(root);
  const task = { ...base, planHash: identity.canonicalPlanSha256, nativePlanHash: identity.workflowPlanSha256,
    projectRevision: inherited ? hash('f') : null, inputHashes: { still: mediaHash },
    inputRefs: [{ assetId: 'still', version: 'media-version-7', sha256: mediaHash }],
    runtimeIdentity: { ...base.runtimeIdentity, capabilitySnapshotSha256: sha256(stableJson(snapshot)) } };
  const manifest = { schema: 'filmcraft-delivery/v1', runtimeSha256: task.runtimeIdentity.sha256,
    sourceProjectSha256: task.projectRevision, assets: { still: { path: 'assets/still.png', sha256: mediaHash } },
    files: Object.fromEntries(Object.entries(files).map(([name, bytes]) => [name, sha256(bytes)])) };
  writeFileSync(join(output, 'manifest.json'), JSON.stringify(manifest));
  const db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  db.register(task); const lease = db.claim(task.taskId, 'worker', 60_000); db.beginAttempt(lease, 'native');
  const index = new ReceiptIndex(db, join(root, 'blobs'));
  return { root, output, task, lease, db, index, manifest, mediaHash };
}

test('delivery mapping binds native project, input versions, packaged dependencies and exchange loss without quality PASS', t => {
  const { root, output, task, lease, db, index, manifest, mediaHash } = delivery(t);
  assert.equal(index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json').status, 'linked');
  db.markSubmitted(lease, 123456);
  index.ingest(task.taskId, lease.attemptId, 'output-execution', executionFixture(root, task, 123456, lease.attemptId));
  const result = index.collect(task.taskId, lease.attemptId);
  assert.equal(result.status, 'linked'); assert.equal(result.outputRefs.length, Object.keys(manifest.files).length);
  for (const artifact of result.outputRefs) {
    assert.equal(artifact.protocolVersion, 'craft-artifact/v1');
    assert.deepEqual(artifact.sourceRefs, [{ assetId: 'still', version: 'media-version-7', sha256: mediaHash }]);
    assert.equal(artifact.nativeProjectRef.sha256, manifest.files['project.fcproj']);
    assert.equal(artifact.dependencies[0].packaged, true); assert.equal(artifact.dependencies[0].assetRef.version, 'media-version-7');
    assert.equal(artifact.lossReportRef.sha256, manifest.files['exchange-loss.json']);
  }
  assert.equal(db.getTask(task.taskId).state, 'running'); assert.equal(result.technicalAcceptance, 'NOT_RUN');
  writeFileSync(join(output, 'assets/still.png'), 'replaced');
  assert.equal(index.collect(task.taskId, lease.attemptId).status, 'stale');
  assert.equal(index.collect(task.taskId, lease.attemptId).outputRefs.length, 0);
});

test('missing capability evidence remains unknown and a mismatching packaged dependency cannot be delivered', t => {
  const { output, task, lease, index, manifest } = delivery(t);
  delete manifest.files['capabilities.json']; writeFileSync(join(output, 'manifest.json'), JSON.stringify(manifest));
  assert.equal(index.inspect(task.taskId, lease.attemptId, 'delivery', 'manifest.json').status, 'unknown');
  manifest.assets.still.path = 'not-packaged.png';
  writeFileSync(join(output, 'manifest.json'), JSON.stringify(manifest));
  assert.equal(index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json').status, 'unknown');
  assert.equal(index.collect(task.taskId, lease.attemptId).outputRefs.length, 0);
});

test('legacy output execution maps declared new inputs separately from inherited project inputs', t => {
  const { root, output, task, lease, index, db } = delivery(t, true);
  db.markSubmitted(lease, 123456);
  const name = '.filmcraft-execution-' + sha256(task.outputRoot) + '.json';
  const raw = { schema: 'filmcraft-output-execution/v1', targetHash: sha256(task.outputRoot), state: 'finished', ownerPid: 123456,
    identity: { planHash: task.nativePlanHash, inputHashes: {}, projectRevision: task.projectRevision, runtimeSha256: task.runtimeIdentity.sha256 } };
  writeFileSync(join(root, name), JSON.stringify(raw));
  assert.equal(index.ingest(task.taskId, lease.attemptId, 'output-execution', name).status, 'unknown');
  assert.equal(index.inspect(task.taskId, lease.attemptId, 'output-execution', name).summary.inputIdentity, 'match');
  raw.identity.inputHashes = { forged: hash() }; writeFileSync(join(root, name), JSON.stringify(raw));
  assert.equal(index.inspect(task.taskId, lease.attemptId, 'output-execution', name).status, 'conflict');
  assert.equal(index.collect(task.taskId, lease.attemptId).status, 'stale');
  assert.throws(() => index.inspect(task.taskId, lease.attemptId, 'output-execution', 'arbitrary.json'), /unsafe_receipt_path/);
  assert.ok(readFileSync(join(output, 'project.fcproj')).length);
});

test('failed-stage receipts retain original bytes and missing historical identities without following stage paths', t => {
  const { output, task, lease, db, index } = setup(t);
  const raw = '{"schema":"craft-failed-stage/v1","outcome":"outcome_unknown","stage":"../../private","error":"lost reply","replayAllowed":true}';
  writeFileSync(join(output, 'failure.json'), raw);
  const record = index.ingest(task.taskId, lease.attemptId, 'failed-stage', 'failure.json');
  assert.equal(record.status, 'unknown'); assert.equal(readFileSync(index.blobPath(record.sha256), 'utf8'), raw);
  const summary = db.receipts(task.taskId, lease.attemptId)[0].summary;
  assert.equal(summary.replayAllowed, false); assert.equal(summary.planIdentity, 'unknown');
  assert.equal(summary.nativeOutcome, 'outcome_unknown'); assert.equal(index.collect(task.taskId, lease.attemptId).outputRefs.length, 0);
});

function executionFixture(root: string, task: ReturnType<typeof binding>, ownerPid: number | undefined, attemptId: string) {
  const name = '.filmcraft-execution-' + sha256(task.outputRoot) + '.json';
  const plan = parseJson(readFileSync(join(task.outputRoot, 'plan.json'), 'utf8'));
  const inputHashes = Object.fromEntries(Object.entries(plan.assets ?? {}).map(([key, value]: [string, any]) => [key, value.sha256]));
  const raw = { schema: 'filmcraft-output-execution/v1', targetHash: sha256(task.outputRoot), state: 'finished',
    ...(ownerPid === undefined ? {} : { ownerPid }),
    context: { taskId: task.taskId, attemptId, sourceRevision: task.sourceRevision, sourceTreeSha256: task.sourceTreeSha256 },
    identity: { planHash: task.nativePlanHash, inputHashes, projectRevision: task.projectRevision,
      runtimeSha256: task.runtimeIdentity.sha256 } };
  writeFileSync(join(root, name), JSON.stringify(raw));
  return name;
}

test('delivery without the same-attempt execution record remains unknown and cannot expose output artifacts', t => {
  const { output, task, lease, index, db } = delivery(t);
  const original = readFileSync(join(output, 'manifest.json'));
  const record = index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json');
  assert.equal(record.status, 'linked', 'a delivery may link individually without proving complete provenance');
  const result = index.collect(task.taskId, lease.attemptId);
  assert.equal(result.status, 'unknown'); assert.deepEqual(result.outputRefs, []);
  assert.deepEqual(result.missingReceiptKinds, ['output-execution']);
  assert.deepEqual(readFileSync(index.blobPath(record.sha256)), original);
  assert.equal(db.getTask(task.taskId).state, 'running');
});

test('execution owner PID must match the attempt and legacy missing process identity stays unknown', t => {
  const { root, task, lease, index, db } = delivery(t);
  db.markSubmitted(lease, 123456);
  for (const [pid, expected] of [[undefined, 'unknown'], [123457, 'conflict'], [123456, 'linked']] as const) {
    const name = executionFixture(root, task, pid, lease.attemptId);
    assert.equal(index.inspect(task.taskId, lease.attemptId, 'output-execution', name).status, expected);
  }
});

test('old artifacts cannot be relabeled as a later task attempt even when plan and runtime match', t => {
  const { root, output, task, lease, db, index } = delivery(t);
  db.markSubmitted(lease, 123456);
  const name = executionFixture(root, task, 123456, lease.attemptId);
  index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json');
  const original = index.ingest(task.taskId, lease.attemptId, 'output-execution', name);
  db.finishAttempt(lease, { outcome: 'failed', stopped: true, receiptSha256: original.sha256 });
  const later = { ...task, taskId: 'later-task', idempotencyKey: 'later-request' };
  db.register(later); const next = db.claim(later.taskId, 'later-worker', 60_000);
  db.beginAttempt(next, 'native'); db.markSubmitted(next, 123456); // 模拟 OS 复用 PID，仍不能继承旧尝试。
  assert.equal(index.ingest(later.taskId, next.attemptId, 'delivery', 'manifest.json').status, 'linked');
  assert.equal(index.ingest(later.taskId, next.attemptId, 'output-execution', name).status, 'conflict');
  const result = index.collect(later.taskId, next.attemptId);
  assert.equal(result.status, 'conflict'); assert.deepEqual(result.outputRefs, []);
  assert.equal(index.collect(task.taskId, lease.attemptId).status, 'linked');
  assert.equal(readFileSync(join(output, 'project.fcproj'), 'utf8'), 'fixture-native-project; not a real project');
});

test('conflicting same-kind observations retain original CAS bytes and do not replace the original association', t => {
  const { output, task, lease, db, index } = delivery(t);
  const original = index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json');
  const bytes = readFileSync(index.blobPath(original.sha256));
  const changed = parseJson(readFileSync(join(output, 'manifest.json'), 'utf8'));
  changed.runtimeSha256 = hash('a'); writeFileSync(join(output, 'manifest.json'), JSON.stringify(changed));
  assert.throws(() => index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json'), /receipt_conflict/);
  assert.equal(db.receipts(task.taskId, lease.attemptId)[0].sha256, original.sha256);
  assert.deepEqual(readFileSync(index.blobPath(original.sha256)), bytes);
  assert.equal(index.collect(task.taskId, lease.attemptId).status, 'stale');
});

test('current missing process evidence cannot inherit an older linked conclusion from the receipt index', t => {
  const { root, task, lease, index, db } = delivery(t);
  db.markSubmitted(lease, 123456);
  index.ingest(task.taskId, lease.attemptId, 'delivery', 'manifest.json');
  index.ingest(task.taskId, lease.attemptId, 'output-execution', executionFixture(root, task, 123456, lease.attemptId));
  assert.equal(index.collect(task.taskId, lease.attemptId).status, 'linked');
  db.db.prepare('UPDATE attempts SET pid=NULL WHERE attempt_id=?').run(lease.attemptId);
  const current = index.collect(task.taskId, lease.attemptId);
  assert.equal(current.status, 'unknown'); assert.deepEqual(current.outputRefs, []);
});
