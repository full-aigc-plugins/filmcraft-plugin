/** 固定安装内部原生验收；原始回执保留在私有工作目录，公共报告不提升质量状态。 */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { TaskLedger } from '../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../src/artifacts/receipt_index.ts';
import { PythonWorkflowRunner, fingerprintSkill } from '../src/adapters/python_workflow.ts';
import { publicTask } from '../src/adapters/protocol_mapping.ts';
import { normalizePlan } from '../src/adapters/plan_identity.ts';
import { parseJson, sha256, stableJson } from '../src/support/json.ts';
import { RecoveryService } from '../src/harness/recovery.ts';

const args = Object.fromEntries(Array.from({ length: (process.argv.length - 2) / 2 }, (_, i) =>
  [process.argv[2 + 2 * i].replace(/^--/, ''), process.argv[3 + 2 * i]]));
const plugin = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const skill = join(plugin, 'skills/filmcraft-use'), root = resolve(args.output), python = args.python;
assert.match(args.source, /^[a-f0-9]{40}$/);
mkdirSync(root, { mode: 0o700 });
const image = join(root, 'still.png');
const fixture = spawnSync(python, ['-c', 'from PIL import Image; import sys; Image.new("RGBA", (32,32), (239,91,54,255)).save(sys.argv[1])', image]);
assert.equal(fixture.status, 0, fixture.stderr.toString());
const imageHash = sha256(readFileSync(image));
const plan = JSON.parse(readFileSync(join(skill, 'examples/native-workflow.json'), 'utf8'));
plan.assets = { still: { path: image, sha256: imageHash } };
const planFile = join(root, 'plan.json'); writeFileSync(planFile, JSON.stringify(plan));
const dbFile = join(root, 'ledger.sqlite'), blobs = join(root, 'blobs'), db = new TaskLedger(dbFile);
const index = new ReceiptIndex(db, blobs);
const version = JSON.parse(readFileSync(join(plugin, 'plugin.json'), 'utf8')).version;
const runner = new PythonWorkflowRunner(db, index, { python, skillDirectory: skill, sourceRevision: args.source,
  runtimeHome: join(root, 'runtime'), pluginVersion: version });
const cases: any[] = [], publicTasks: any[] = [], publicArtifacts: any[] = [], archived: any[] = [];
const observations: any[] = [];

function binding(id: string, prepared: ReturnType<PythonWorkflowRunner['prepare']>) {
  return { taskId: id, namespace: 'fixed-lineage-test', idempotencyKey: id,
    planHash: prepared.planIdentity.canonicalPlanSha256, nativePlanHash: prepared.planIdentity.workflowPlanSha256,
    inputHashes: prepared.inputHashes, inputRefs: Object.entries(prepared.inputHashes).map(([assetId, sha256]) =>
      ({ assetId, version: 'synthetic-fixture-v1', sha256: sha256 as string })),
    projectRevision: prepared.projectRevision, projectKey: prepared.projectKey, outputRoot: prepared.outputRoot,
    sourceRevision: args.source, sourceTreeSha256: prepared.sourceTreeSha256, runtimeIdentity: prepared.runtimeIdentity,
    authorizationRef: 'existing-local-test-authorization', authorizationScopeSha256: sha256('bounded synthetic local fixture'),
    deadline: Date.now() + 3600_000 };
}
function archive(taskId: string, attemptId: string) {
  for (const record of db.receipts(taskId, attemptId)) {
    const data = readFileSync(index.blobPath(record.sha256));
    assert.equal(sha256(data), record.sha256);
    archived.push({ taskId, attemptId, kind: record.kind, sha256: record.sha256, bytes: data.length,
      projection: parseJson(data.toString('utf8')), originalBytesPreserved: true });
  }
}
function mapped(taskId: string, attemptId: string) {
  const result = index.collect(taskId, attemptId);
  assert.equal(result.status, 'linked'); assert.equal(result.technicalAcceptance, 'NOT_RUN');
  publicTasks.push(publicTask(db, taskId, { schemaVersion: 'filmcraft-native-workflow/v1' },
    { currency: 'USD', maxMinorUnits: 0, maxRevisions: 0, maxExternalCalls: 0 }));
  publicArtifacts.push(...result.outputRefs); archive(taskId, attemptId);
  return result;
}
try {
  const output = join(root, 'delivery'), prepared = runner.prepare(planFile, output), task = binding('create', prepared);
  const created = await runner.run(task, planFile);
  assert.equal(created.state, 'verifying'); assert.equal(created.process!.stopped, true);
  const linked = mapped(task.taskId, created.attemptId!); observations.push(linked);
  const project = join(output, 'project.fcproj'), projectHash = sha256(readFileSync(project));
  const rawGuard = join(root, '.filmcraft-execution-' + sha256(prepared.outputRoot) + '.json');
  const execution = parseJson(readFileSync(rawGuard, 'utf8'));
  assert.deepEqual({ ...execution.context }, { taskId: task.taskId, attemptId: created.attemptId,
    sourceRevision: args.source, sourceTreeSha256: prepared.sourceTreeSha256 });
  cases.push({ case: 'actual-create-and-attempt-context', result: 'PASS', state: created.state, receiptKinds: db.receipts(task.taskId, created.attemptId!).map(r => r.kind) });
  const reused = await runner.run(task, planFile);
  assert.equal(reused.reused, true); assert.equal(db.listAttempts(task.taskId).length, 1);
  cases.push({ case: 'idempotent-no-native-replay', result: 'PASS', attemptId: reused.attemptId });
  const movie = join(output, 'film.mp4'), originalMovie = readFileSync(movie);
  writeFileSync(movie, Buffer.from('changed same-name candidate'));
  assert.equal(index.collect(task.taskId, created.attemptId!).status, 'stale');
  assert.deepEqual(index.collect(task.taskId, created.attemptId!).outputRefs, []);
  writeFileSync(movie, originalMovie); assert.equal(index.collect(task.taskId, created.attemptId!).status, 'linked');
  cases.push({ case: 'actual-candidate-digest-change', result: 'PASS', originalRestored: true });
  const manifestPath = join(output, 'manifest.json'), manifestBytes = readFileSync(manifestPath);
  const changed = parseJson(manifestBytes.toString('utf8')); changed.runtimeSha256 = '0'.repeat(64);
  writeFileSync(manifestPath, JSON.stringify(changed));
  assert.throws(() => index.ingest(task.taskId, created.attemptId!, 'delivery', 'manifest.json'), /receipt_conflict/);
  writeFileSync(manifestPath, manifestBytes); archive(task.taskId, created.attemptId!);
  cases.push({ case: 'same-kind-conflict-original-CAS', result: 'PASS' });

  // 对真实旧产物构造另一个账本尝试；即使复用 PID 也必须因上下文冲突拒绝。
  const foreign = { ...task, taskId: 'foreign-attempt', idempotencyKey: 'foreign-attempt' };
  db.register(foreign); const lease = db.claim(foreign.taskId, 'adversarial-relabel', 60_000);
  db.beginAttempt(lease, 'relabel-only-no-native-dispatch'); db.markSubmitted(lease, execution.ownerPid);
  index.ingest(foreign.taskId, lease.attemptId, 'delivery', 'manifest.json');
  const partial = index.collect(foreign.taskId, lease.attemptId);
  assert.equal(partial.status, 'unknown'); assert.deepEqual(partial.outputRefs, []);
  assert.deepEqual(partial.missingReceiptKinds, ['output-execution']);
  assert.equal(index.ingest(foreign.taskId, lease.attemptId, 'output-execution', rawGuard.split('/').at(-1)!).status, 'conflict');
  assert.equal(index.collect(foreign.taskId, lease.attemptId).status, 'conflict');
  assert.deepEqual(index.collect(foreign.taskId, lease.attemptId).outputRefs, []);
  cases.push({ case: 'cross-attempt-relabel-with-same-PID', result: 'PASS', executionLayer: 'synthetic adversarial ledger attempt against actual native records; no native replay' });
  cases.push({ case: 'missing-execution-receipt', result: 'PASS' });
  const oldGuard = readFileSync(rawGuard), legacy = parseJson(oldGuard.toString('utf8')); delete legacy.context;
  writeFileSync(rawGuard, JSON.stringify(legacy));
  assert.equal(index.inspect(task.taskId, created.attemptId!, 'output-execution', rawGuard.split('/').at(-1)!).status, 'unknown');
  writeFileSync(rawGuard, oldGuard);
  cases.push({ case: 'legacy-missing-context', result: 'PASS', historicalFields: 'unknown, not fabricated' });

  const commandPlan = JSON.parse(readFileSync(join(skill, 'examples/desktop-first-use.json'), 'utf8'));
  const commandFile = join(root, 'commands.json'); writeFileSync(commandFile, JSON.stringify(commandPlan));
  const commandOutput = join(root, 'command-delivery');
  const run = spawnSync(python, ['-I', '-B', join(skill, 'scripts/commands.py'), 'run', commandFile,
    '--output', commandOutput, '--runtime-home', join(root, 'runtime')], { encoding: 'utf8', timeout: 180_000 });
  assert.equal(run.status, 0, run.stderr);
  const rawCommand = parseJson(readFileSync(join(commandOutput, 'success.json'), 'utf8'));
  const identity = normalizePlan(commandFile, python);
  const commandTask = { ...task, taskId: 'commands', idempotencyKey: 'commands', outputRoot: commandOutput,
    projectKey: sha256(commandOutput), planHash: identity.canonicalPlanSha256, nativePlanHash: identity.commandPlanSha256,
    inputHashes: {}, inputRefs: [] };
  db.register(commandTask); const commandLease = db.claim(commandTask.taskId, 'command-mapper', 60_000);
  db.beginAttempt(commandLease, 'actual-public-command'); db.markSubmitted(commandLease, run.pid!);
  assert.equal(index.ingest(commandTask.taskId, commandLease.attemptId, 'command', 'success.json').status, 'linked');
  archive(commandTask.taskId, commandLease.attemptId);
  assert.deepEqual(index.collect(commandTask.taskId, commandLease.attemptId).outputRefs, []);
  assert.equal(rawCommand.result, 'PASS'); cases.push({ case: 'actual-command-v1-mapping', result: 'PASS' });

  const failurePlan = structuredClone(plan); failurePlan.operations = [{ command: 'native.command',
    params: { command: 'captions.setStyle', params: { track: 'C1', font: 'missing-lineage-font' } } }];
  const failureFile = join(root, 'failure-plan.json'); writeFileSync(failureFile, JSON.stringify(failurePlan));
  const failureOutput = join(root, 'failed-delivery'), failurePrepared = runner.prepare(failureFile, failureOutput);
  const failedTask = binding('failure', failurePrepared), failed = await runner.run(failedTask, failureFile);
  assert.equal(failed.state, 'failed'); assert.equal(failed.receipt!.status, 'unknown');
  assert.deepEqual(failed.receipt!.outputRefs, []); archive(failedTask.taskId, failed.attemptId!);
  cases.push({ case: 'actual-failed-stage-v1-mapping', result: 'PASS', outcome: failed.state });

  // 真实导出后第二次索引交接丢失：诊断不写原数据，修复同一尝试而不重跑工作流。
  const lostOutput = join(root, 'partial-handoff'), lostPrepared = runner.prepare(planFile, lostOutput);
  const lostTask = binding('partial-handoff', lostPrepared), partialBlobs = join(root, 'partial-blobs');
  const lostIndex = new ReceiptIndex(db, partialBlobs), ingest = lostIndex.ingest.bind(lostIndex); let calls = 0;
  lostIndex.ingest = (...args) => { if (++calls === 2) { throw new Error('injected_second_receipt_handoff_lost'); } return ingest(...args); };
  const lostRunner = new PythonWorkflowRunner(db, lostIndex, runner.options);
  await assert.rejects(lostRunner.run(lostTask, planFile), /injected_second_receipt_handoff_lost/);
  assert.equal(lostIndex.collect(lostTask.taskId, db.getTask(lostTask.taskId).attemptId!).status, 'unknown');
  const service = new RecoveryService(dbFile, partialBlobs, { authorize: (subject, request) => ({ ...request,
    expiresAt: Date.now() + 60_000, subjectSha256: sha256(stableJson(subject)) }) }), observation = service.inspect(lostTask.taskId);
  assert.equal(observation.diagnosis, 'executed');
  const repaired = service.repair(lostTask.taskId, { expectedEpoch: observation.task!.epoch,
    inspectionSha256: observation.evidenceSha256, authorizationRef: lostTask.authorizationRef,
    authorizationScopeSha256: lostTask.authorizationScopeSha256 });
  assert.equal(repaired.receipt.status, 'linked'); assert.equal(repaired.replayed, false);
  assert.equal(db.listAttempts(lostTask.taskId).length, 1);
  cases.push({ case: 'actual-partial-receipt-handoff-repair', result: 'PASS', replayed: false, attemptCount: 1 });
  assert.equal(sha256(readFileSync(image)), imageHash); assert.equal(sha256(readFileSync(project)), projectHash);
  assert.equal(fingerprintSkill(skill), prepared.sourceTreeSha256);
  const report = { schema: 'filmcraft-fixed-lineage-native/v1', result: 'PASS', pluginVersion: version,
    sourceRevision: args.source, sourceTreeSha256: prepared.sourceTreeSha256, runtimeIdentity: prepared.runtimeIdentity,
    nodeVersion: process.version, platform: process.platform + '-' + process.arch, cases, observations, archived,
    publicTasks, publicArtifacts, installedSkillUnchanged: true, inputPreserved: true, originalProjectPreserved: true,
    technicalAcceptance: 'NOT_RUN', creativeAcceptance: 'NOT_RUN', userAcceptance: 'NOT_RUN',
    authorizationEnforcement: 'HOST_REQUIRED', fullV1: 'INCOMPLETE' };
  writeFileSync(join(root, 'report.private.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ result: 'PASS', cases: cases.length, publicTasks: publicTasks.length, publicArtifacts: publicArtifacts.length }));
} finally { db.close(); }
