import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {spawnSync} from 'node:child_process';
import {mkdirSync,readFileSync,readdirSync,writeFileSync} from 'node:fs';
import {join,relative} from 'node:path';
import {pathToFileURL} from 'node:url';
const baseline=process.env.FILMCRAFT_RED_BASELINE!, candidate=process.env.FILMCRAFT_RED_CANDIDATE!;
assert.ok(baseline && candidate, 'explicit old baseline and current fixture roots required');
const {TaskLedger}=await import(pathToFileURL(join(baseline, 'src/harness/task_ledger.ts')).href);
const {RecoveryService}=await import(pathToFileURL(join(baseline, 'src/harness/recovery.ts')).href);
const {normalizePlan}=await import(pathToFileURL(join(baseline, 'src/adapters/plan_identity.ts')).href);
const {sha256,stableJson}=await import(pathToFileURL(join(baseline, 'src/support/json.ts')).href);
const {binding,workspace,fixtureAuthorizer}=await import(pathToFileURL(join(candidate, 'test/harness/fixtures.ts')).href);
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
    state: 'finished', ownerPid: process.pid, context: { taskId: task.taskId, attemptId: lease.attemptId, sourceRevision: task.sourceRevision, sourceTreeSha256: task.sourceTreeSha256 }, identity: { planHash: task.nativePlanHash, inputHashes: {}, projectRevision: null, runtimeSha256: task.runtimeIdentity.sha256 } }));
  db.finishAttempt(lease, { outcome: 'unknown', stopped: true, receiptSha256: null });
  const service = new RecoveryService(dbFile, join(root, 'blobs'), { authorize: fixtureAuthorizer });
  return { root, output, db, dbFile, task, lease, service, guard };
}

test('matching authorization references alone cannot authorize state repair', t => {
  const { dbFile, root, task, service } = lostReply(t);
  const observation = service.inspect(task.taskId), before = files(root);
  const unverified = new RecoveryService(dbFile, join(root, 'blobs'));
  assert.throws(() => unverified.repair(task.taskId, { expectedEpoch: observation.task!.epoch,
    inspectionSha256: observation.evidenceSha256, authorizationRef: task.authorizationRef,
    authorizationScopeSha256: task.authorizationScopeSha256 }), /authorization_verifier_required/);
  assert.deepEqual(files(root), before);
});

test('expired or revoked host authorization cannot change an uncertain attempt', t => {
  const { dbFile, root, task, service } = lostReply(t);
  const observation = service.inspect(task.taskId), before = files(root);
  const expired = new RecoveryService(dbFile, join(root, 'blobs'), { authorize: () => ({ expiresAt: Date.now() - 1 }) });
  assert.throws(() => expired.repair(task.taskId, { expectedEpoch: observation.task!.epoch,
    inspectionSha256: observation.evidenceSha256, authorizationRef: task.authorizationRef,
    authorizationScopeSha256: task.authorizationScopeSha256 }), /authorization_expired/);
  const revoked = new RecoveryService(dbFile, join(root, 'blobs'), { authorize: () => null });
  assert.throws(() => revoked.repair(task.taskId, { expectedEpoch: observation.task!.epoch,
    inspectionSha256: observation.evidenceSha256, authorizationRef: task.authorizationRef,
    authorizationScopeSha256: task.authorizationScopeSha256 }), /authorization_required/);
  assert.deepEqual(files(root), before);
});

test('legacy writer has no verified backup gate',t=>{const root=workspace(t),file=join(root,'ledger.sqlite'),db=new TaskLedger(file);db.register(binding(root));db.db.exec('DROP TABLE IF EXISTS continuation_intents;DROP TABLE recovery_intents;PRAGMA user_version=1');db.close();assert.throws(()=>new TaskLedger(file),/ledger_upgrade_required/);});
test('existing empty SQLite is not owned',t=>{const root=workspace(t),file=join(root,'empty.sqlite'),db=new DatabaseSync(file);db.exec('PRAGMA user_version=0');db.close();assert.throws(()=>new TaskLedger(file),/ledger_schema_unknown/);});
test('matching columns without ownership constraints are not enough',t=>{const root=workspace(t),file=join(root,'ledger.sqlite'),db=new TaskLedger(file);db.register(binding(root));db.close();const raw=new DatabaseSync(file);raw.exec('PRAGMA foreign_keys=OFF;ALTER TABLE tasks RENAME TO tasks_old;CREATE TABLE tasks AS SELECT * FROM tasks_old;DROP TABLE tasks_old;');raw.close();assert.throws(()=>new TaskLedger(file,{readOnly:true}),/ledger_schema_unknown/);});
