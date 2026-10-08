/** 固定安装副本的真实首次准入验收；只使用私有合成输入和显式本机测试授权。 */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import { TaskLedger } from '../src/harness/task_ledger.ts';
import { LocalAuthorizationStore } from '../src/harness/authorization.ts';
import { WorkflowAdmission, executionSubject } from '../src/harness/workflow_admission.ts';
import { PythonWorkflowRunner, fingerprintSkill } from '../src/adapters/python_workflow.ts';
import { ReceiptIndex } from '../src/artifacts/receipt_index.ts';
import { sha256, stableJson } from '../src/support/json.ts';

const { values } = parseArgs({ options: { output: { type: 'string' }, python: { type: 'string' } } });
assert.ok(values.output && values.python);
const root = resolve(values.output), plugin = resolve(dirname(fileURLToPath(import.meta.url)), '..');
assert.equal(existsSync(root), false, 'output_exists'); mkdirSync(root, { mode: 0o700 });
const skill = join(plugin, 'skills/filmcraft-use'), sourceSha = JSON.parse(readFileSync(join(plugin, 'skills.lock.json'), 'utf8')).sources[0].sha;
const skillBefore = fingerprintSkill(skill), version = JSON.parse(readFileSync(join(plugin, 'plugin.json'), 'utf8')).version;
const resources = { limits: { timeMs: 600_000, diskBytes: 128_000_000, outputBytes: 128_000_000, slots: 2, revisions: 2 },
  allocation: { timeMs: 120_000, diskBytes: 64_000_000, outputBytes: 64_000_000, slots: 1, revisions: 0 } };
const resourcesFile = join(root, 'resources.json'); writeFileSync(resourcesFile, JSON.stringify(resources));
const options = { resources, python: values.python, skillDirectory: skill, sourceRevision: sourceSha,
  runtimeHome: join(root, 'fresh-runtime'), pluginVersion: version };
const image = join(root, 'still.png');
assert.equal(spawnSync(values.python, ['-c', 'from PIL import Image; import sys; Image.new("RGBA",(32,32),(239,91,54,255)).save(sys.argv[1])', image]).status, 0);
const plan = JSON.parse(readFileSync(join(skill, 'examples/native-workflow.json'), 'utf8'));
plan.assets = { still: { path: image, sha256: sha256(readFileSync(image)) } };
const planFile = join(root, 'plan.json'); writeFileSync(planFile, JSON.stringify(plan));
const ledger = join(root, 'ledger.sqlite'), blobs = join(root, 'blobs'), grants = join(root, 'host-grants');
mkdirSync(grants, { mode: 0o700 });
const db = new TaskLedger(ledger), index = new ReceiptIndex(db, blobs), runner = new PythonWorkflowRunner(db, index, options);
const cases: any[] = [];
const grant: any = { schema: 'filmcraft-local-authorization/v1', authorizationRef: 'bounded-local-QA',
  authorizationScopeSha256: sha256('synthetic first admission and explicit refusal verification'),
  expiresAt: Date.now() + 900_000, revoked: false, subjects: [] };
const grantFile = join(grants, sha256(grant.authorizationRef) + '.json');
const writeGrant = () => writeFileSync(grantFile, JSON.stringify(grant), { mode: 0o600 });
const authorize = new LocalAuthorizationStore(grants).authorize;
function binding(id: string, prepared: ReturnType<PythonWorkflowRunner['prepare']>) {
  return { taskId: id, namespace: 'admission-native-QA', idempotencyKey: id, planHash: prepared.planIdentity.canonicalPlanSha256,
    nativePlanHash: prepared.planIdentity.workflowPlanSha256, inputHashes: prepared.inputHashes,
    inputRefs: Object.entries(prepared.inputHashes).map(([assetId, digest]) => ({ assetId, version: 'synthetic-v1', sha256: digest as string })),
    projectRevision: prepared.projectRevision, projectKey: prepared.projectKey, outputRoot: prepared.outputRoot,
    sourceRevision: sourceSha, sourceTreeSha256: prepared.sourceTreeSha256, runtimeIdentity: prepared.runtimeIdentity,
    authorizationRef: grant.authorizationRef, authorizationScopeSha256: grant.authorizationScopeSha256,
    deadline: Date.now() + 600_000 };
}
function permit(task: ReturnType<typeof binding>) { grant.subjects.push(sha256(stableJson(executionSubject(task, resources)))); writeGrant(); }
function cli(task: ReturnType<typeof binding>) {
  const file = join(root, task.taskId + '.binding.json'); writeFileSync(file, JSON.stringify(task));
  return spawnSync(process.execPath, [join(plugin, 'src/cli/workflow.ts'), 'run', '--binding', file,
    '--plan', planFile, '--resources', resourcesFile, '--ledger', ledger, '--blobs', blobs, '--authorization-root', grants,
    '--runtime-home', options.runtimeHome, '--python', values.python!], { encoding: 'utf8', timeout: 180_000 });
}
try {
  const output = join(root, 'created'), prepared = runner.prepare(planFile, output), task = binding('create', prepared);
  const service = new WorkflowAdmission(db, index, options, authorize);
  writeGrant();
  await assert.rejects(service.run(task, planFile), /authorization_scope_change_required/);
  assert.throws(() => db.getTask(task.taskId), /task_missing/);
  cases.push({ id: 'ungranted-exact-subject', status: 'PASS', attempts: 0, outputExists: existsSync(output) });
  permit(task);
  const createdRaw = cli(task); assert.equal(createdRaw.status, 0, createdRaw.stdout + createdRaw.stderr);
  const created = JSON.parse(createdRaw.stdout);
  assert.equal(created.state, 'verifying'); assert.equal(created.process.stopped, true); assert.equal(created.receipt.status, 'linked');
  const project = join(output, 'project.fcproj'), projectSha = sha256(readFileSync(project));
  cases.push({ id: 'actual-cli-authorized-native-create', status: 'PASS', projectSha256: projectSha,
    movieSha256: sha256(readFileSync(join(output, 'film.mp4'))), state: created.state, stopped: true });
  const again = cli(task); assert.equal(again.status, 0, again.stdout + again.stderr);
  assert.equal(JSON.parse(again.stdout).reused, true); assert.equal(db.listAttempts(task.taskId).length, 1);
  cases.push({ id: 'existing-valid-grant-idempotent-reuse', status: 'PASS', attempts: 1 });
  grant.revoked = true; writeGrant();
  const revoked = cli(task); assert.equal(revoked.status, 1); assert.equal(JSON.parse(revoked.stdout).error.code, 'authorization_required');
  assert.equal(db.listAttempts(task.taskId).length, 1); assert.equal(sha256(readFileSync(project)), projectSha);
  cases.push({ id: 'revoked-grant-refuses-even-reuse', status: 'PASS', attempts: 1, originalPreserved: true });
  grant.revoked = false; writeGrant();
  const changed = { ...binding('drift', runner.prepare(planFile, join(root, 'drift'))),
    runtimeIdentity: { ...prepared.runtimeIdentity, sha256: '0'.repeat(64) } };
  permit(changed);
  await assert.rejects(service.run(changed, planFile), /runtime_identity_conflict/);
  assert.throws(() => db.getTask(changed.taskId), /task_missing/);
  cases.push({ id: 'authorized-runtime-drift-before-registration', status: 'PASS', attempts: 0 });
  const stopTask = binding('revoke-at-submit', runner.prepare(planFile, join(root, 'revoke-at-submit')));
  permit(stopTask); let gates = 0;
  const gateService = new WorkflowAdmission(db, index, { ...options, beforeDispatch: () => {
    if (++gates === 3) { grant.revoked = true; writeGrant(); }
  } }, authorize);
  await assert.rejects(gateService.run(stopTask, planFile), /authorization_required/);
  assert.equal(db.getTask(stopTask.taskId).state, 'failed'); assert.equal(db.listAttempts(stopTask.taskId).length, 1);
  assert.equal(existsSync(stopTask.outputRoot), false); grant.revoked = false; writeGrant();
  cases.push({ id: 'revocation-after-intent-before-spawn', status: 'PASS', attempts: 1, nativeLaunched: false, state: 'failed' });
  // 用真实原生生成的另一个工程版本模拟 GUI 保存后的版本变化，拒绝旧计划。
  const source = join(root, 'source-copy'); cpSync(output, source, { recursive: true });
  const revisionPlan = { ...plan, expectedProjectSha256: projectSha }; delete revisionPlan.document; delete revisionPlan.assets;
  revisionPlan.operations = [{ command: 'timeline.select', params: { clips: { $ref: 'clip.clips' }, add: false, toggle: false } }, structuredClone(plan.operations.at(-1))];
  revisionPlan.operations[1].params.params.speed = 200;
  const revisionFile = join(root, 'revision.json'); writeFileSync(revisionFile, JSON.stringify(revisionPlan));
  const nextOutput = join(root, 'revision'), next = binding('revision', runner.prepare(revisionFile, nextOutput, source)); permit(next);
  const edited = await service.run(next, revisionFile, source); assert.equal(edited.state, 'verifying');
  const staleOutput = join(root, 'stale'), stale = binding('stale', runner.prepare(revisionFile, staleOutput, source)); permit(stale);
  cpSync(join(nextOutput, 'project.fcproj'), join(source, 'project.fcproj'));
  const changedSource = sha256(readFileSync(join(source, 'project.fcproj'))); assert.notEqual(changedSource, projectSha);
  await assert.rejects(service.run(stale, revisionFile, source), /revision_conflict/);
  assert.throws(() => db.getTask(stale.taskId), /task_missing/);
  assert.equal(sha256(readFileSync(join(source, 'project.fcproj'))), changedSource);
  assert.equal(sha256(readFileSync(project)), projectSha);
  cases.push({ id: 'actual-native-revision-and-stale-source-conflict', status: 'PASS',
    originalSha256: projectSha, changedSha256: changedSource, staleAttempts: 0, sourcePreserved: true });
  assert.equal(fingerprintSkill(skill), skillBefore);
  const report = { schema: 'filmcraft-workflow-admission-verification/v1', result: 'PASS', layer: 'actual-native',
    pluginVersion: version, sourceRevision: sourceSha, skillSha256: skillBefore, skillHashAlgorithm: 'path-nul-raw-bytes-nul', runtimeIdentity: prepared.runtimeIdentity,
    platform: process.platform + '-' + process.arch, nodeVersion: process.version, cases,
    planSha256: sha256(readFileSync(planFile)), inputSha256: sha256(readFileSync(image)),
    installedSkillPreserved: true, authorization: 'private host LocalAuthorizationStore; explicit exact subjects; no production grants',
    scope: 'initial execution admission and bounded native revision/refusal; full TX-001/other routes/platforms/V1 remain unqualified',
    fullV1: 'NOT_PROVEN', technicalAcceptance: 'NOT_RUN', creativeAcceptance: 'NOT_RUN', userAcceptance: 'NOT_RUN' };
  writeFileSync(join(root, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ result: report.result, cases: cases.length, runtime: prepared.runtimeIdentity.cliVersion }));
} finally { db.close(); }
