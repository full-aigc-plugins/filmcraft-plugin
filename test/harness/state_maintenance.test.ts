import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { StateMaintenance } from '../../src/harness/state_maintenance.ts';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { forensicSnapshot } from '../../src/harness/forensic_snapshot.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { binding, hash, workspace, fixtureAuthorizer, captureEvidence } from './fixtures.ts';

function fixture(t: Parameters<typeof workspace>[0], version = 2) {
  const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file);
  const task = binding(root); db.register(task); const lease = db.claim(task.taskId, 'old-owner', 1000);
  db.beginAttempt(lease, 'old-operation'); db.finishAttempt(lease, { outcome: 'unknown', stopped: false, receiptSha256: null });
  db.recordReceipt(task.taskId, lease.attemptId, 'failed-stage', hash(), {}, 'unknown');
  db.db.exec('UPDATE tasks SET lease_until=0; DROP TABLE runtime_deployments;');
  if(version<5){db.db.exec('DROP TABLE revision_rounds; DROP TABLE revision_loops;');}
  if (version < 4) { db.db.exec('DROP TABLE cancel_intents; DROP TABLE task_resources; DROP TABLE resource_scopes;'); }
  if (version < 3) { db.db.exec('DROP TABLE continuation_intents;'); }
  if (version === 1) { db.db.exec('DROP TABLE recovery_intents;'); }
  db.db.exec('PRAGMA user_version=' + version); db.close();
  return { root, file, task, lease, service: new StateMaintenance(file, { authorize: fixtureAuthorizer }),
    grant: { authorizationRef: 'existing-maintenance-grant', authorizationScopeSha256: hash() } };
}
function files(root: string) {
  return Object.fromEntries(readdirSync(root).filter(name => !name.startsWith('backup')).map(name => [name, sha256(readFileSync(join(root, name)))]));
}
for (const version of [1, 2, 3, 4, 5]) {
  test('schema' + version + ' backup, upgrade and compatible rollback preserve unknown task, attempts, receipts and occupancy', t => {
    const { root, file, task, lease, service, grant } = fixture(t, version);
    const baseline = service.inspect(), before = files(root), backup = join(root, 'backup');
    assert.throws(() => new TaskLedger(file), /ledger_upgrade_required/); assert.deepEqual(files(root), before);
    const upgraded = service.upgrade(backup, grant); assert.equal(upgraded.toVersion, 6);
    const manifestBytes = readFileSync(join(backup, 'manifest.json')), manifest = JSON.parse(manifestBytes.toString());
    assert.equal(sha256(manifestBytes), upgraded.backupManifestSha256);
    for (const [name, digest] of Object.entries(manifest.files)) { assert.equal(sha256(readFileSync(join(backup, name))), digest); }
    assert.equal(existsSync(join(backup, 'upgrade-intent.json')), true);
    const db = new TaskLedger(file); assert.equal(db.getTask(task.taskId).attemptId, lease.attemptId);
    assert.equal(db.getTask(task.taskId).state, 'reconciling'); assert.equal(db.receipts(task.taskId, lease.attemptId).length, 1);
    assert.equal(db.db.prepare('SELECT COUNT(*) AS n FROM project_leases').get()!.n, 1); db.close();
    assert.equal(service.rollback(backup, grant).version, version);
    assert.deepEqual(service.inspect().records, baseline.records);
    assert.equal(service.rollback(backup, grant).reused, true);
    assert.equal(sha256(readFileSync(join(backup, 'manifest.json'))), upgraded.backupManifestSha256);
    assert.throws(() => new TaskLedger(file), /ledger_upgrade_required/);
    captureEvidence('schema'+version+'-upgrade-rollback', 'actual SQLite maintenance; synthetic operation records', { version, before, after: files(root), manifest, logicalBeforeSha256: sha256(stableJson(baseline.records)), logicalAfterSha256: sha256(stableJson(service.inspect().records)), originalAttemptId: lease.attemptId, recordsPreserved: true });
  });
}

test('committed uncheckpointed WAL is preserved in backup and read-only diagnosis cannot alter any original sidecar', t => {
  const { root, file, service, grant } = fixture(t, 2), writer = new DatabaseSync(file);
  t.after(() => writer.close()); writer.exec('PRAGMA wal_autocheckpoint=0; UPDATE tasks SET epoch=epoch+1;');
  const before = files(root); assert.ok(existsSync(file + '-wal'));
  const snapshot = service.inspect(); assert.deepEqual(files(root), before);
  const result = service.upgrade(join(root, 'backup'), grant), manifest = JSON.parse(readFileSync(join(root, 'backup/manifest.json'), 'utf8'));
  assert.equal(result.recordsPreserved, true); assert.ok(manifest.files['database.sqlite-wal']); assert.ok(manifest.files['shm.audit']);
  assert.equal(sha256(readFileSync(join(root, 'backup/database.sqlite-wal'))), manifest.files['database.sqlite-wal']);
  assert.deepEqual(service.inspect().records.tasks, snapshot.records.tasks);
});

test('a changed original during isolated inspection is unknown rather than a reusable old snapshot', t => {
  const { file, task } = fixture(t), writer = new DatabaseSync(file); t.after(() => writer.close());
  assert.throws(() => forensicSnapshot(file, copy => {
    const epoch = copy.getTask(task.taskId).epoch;
    writer.prepare('UPDATE tasks SET epoch=epoch+1 WHERE task_id=?').run(task.taskId);
    return epoch;
  }), /ledger_changed/);
  assert.equal(new StateMaintenance(file).inspect().records.tasks[0].epoch, 3);
  captureEvidence('inspection-concurrent-write', 'actual concurrent SQLite commit during isolated observation', { refused: 'ledger_changed', currentEpoch: 3 });
});

test('rollback refuses to discard new task records and does not overwrite the immutable old backup', t => {
  const { root, file, service, grant } = fixture(t), backup = join(root, 'backup'); service.upgrade(backup, grant);
  const originalBackup = sha256(readFileSync(join(backup, 'database.sqlite')));
  const writer = new TaskLedger(file); writer.register(binding(root, { taskId: 'new-task', idempotencyKey: 'new-operation' })); writer.close();
  const before = files(root); assert.throws(() => service.rollback(backup, grant), /rollback_changes_conflict/);
  assert.deepEqual(files(root), before); assert.equal(sha256(readFileSync(join(backup, 'database.sqlite'))), originalBackup);
  captureEvidence('rollback-preserves-new-records', 'actual SQLite with synthetic new task', { before, after: files(root), originalBackupSha256: originalBackup, refused: 'rollback_changes_conflict' });
});

test('corrupt backups, unsupported ledgers and logical damage cannot be upgraded or claimed', t => {
  const { root, file, service, grant } = fixture(t), backup = join(root, 'backup'); service.upgrade(backup, grant);
  writeFileSync(join(backup, 'database.sqlite'), 'corrupt backup');
  assert.throws(() => service.rollback(backup, grant), /backup_invalid/);
  const db = new TaskLedger(file); db.db.exec('PRAGMA user_version=99'); db.close(); const before = files(root);
  assert.throws(() => service.upgrade(join(root, 'backup-new'), grant), /ledger_schema_unsupported/);
  assert.deepEqual(files(root), before); assert.equal(existsSync(join(root, 'backup-new')), false);
});

test('maintenance cannot run without authorization or while a live write lease is held', t => {
  const { root, file, service, grant } = fixture(t), before = files(root);
  assert.throws(() => new StateMaintenance(file).upgrade(join(root, 'backup'), grant), /authorization_verifier_required/);
  assert.deepEqual(files(root), before);
  const db = new DatabaseSync(file); db.prepare('UPDATE tasks SET lease_until=?').run(Date.now()+60_000); db.close();
  assert.throws(() => service.upgrade(join(root, 'backup'), grant), /ledger_not_quiescent/);
  assert.equal(existsSync(join(root, 'backup')), false);
});

test('an existing empty SQLite database is unknown, never an invitation to initialize FilmCraft state', t => {
  const root = workspace(t), file = join(root, 'foreign-empty.sqlite'), foreign = new DatabaseSync(file);
  foreign.exec('PRAGMA user_version=0;'); foreign.close(); const before = files(root);
  assert.throws(() => new TaskLedger(file), /ledger_schema_unknown/);
  assert.deepEqual(files(root), before);
});

test('foreign and logically damaged ledgers are rejected before any backup or original SQLite write', t => {
  const { root, file, task, grant } = fixture(t), raw = new DatabaseSync(file);
  raw.prepare("UPDATE tasks SET identity_hash=? WHERE task_id=?").run(hash('f'), task.taskId); raw.close();
  const before = files(root), maintenance = new StateMaintenance(file, { authorize: fixtureAuthorizer });
  assert.throws(() => maintenance.upgrade(join(root, 'backup'), grant), /ledger_identity_corrupt/);
  assert.deepEqual(files(root), before); assert.equal(existsSync(join(root, 'backup')), false);
  const foreignFile = join(root, 'foreign.sqlite'), foreign = new DatabaseSync(foreignFile);
  foreign.exec('CREATE TABLE user_data(value TEXT); PRAGMA user_version=2;'); foreign.close();
  const foreignBefore = files(root);
  assert.throws(() => new StateMaintenance(foreignFile, { authorize: fixtureAuthorizer }).upgrade(join(root, 'backup-foreign'), grant), /ledger_schema_unknown/);
  assert.deepEqual(files(root), foreignBefore);
});

test('revocation after backup intent preserves original schema and the complete backup audit', t => {
  const { root, file, grant } = fixture(t); let gates = 0;
  const maintenance = new StateMaintenance(file, { authorize: (subject, request) => ++gates === 3 ? null : fixtureAuthorizer(subject, request) });
  const baseline = maintenance.inspect();
  assert.throws(() => maintenance.upgrade(join(root, 'backup'), grant), /authorization_required/);
  assert.deepEqual(maintenance.inspect().records, baseline.records); assert.equal(maintenance.inspect().version, 2);
  assert.equal(existsSync(join(root, 'backup/upgrade-intent.json')), true);
  const manifest = JSON.parse(readFileSync(join(root, 'backup/manifest.json'), 'utf8')); assert.equal(manifest.complete, true);
});

test('matching column names without FilmCraft structural constraints cannot claim a ledger', t => {
  const { file } = fixture(t), raw = new DatabaseSync(file);
  raw.exec('PRAGMA foreign_keys=OFF; ALTER TABLE tasks RENAME TO tasks_old; CREATE TABLE tasks AS SELECT * FROM tasks_old; DROP TABLE tasks_old;'); raw.close();
  assert.throws(() => new TaskLedger(file, { readOnly: true }), /ledger_schema_unknown/);
});

test('the actual previous installed dev45 core refuses schema6 without editing current state',
  { skip: !process.env.FILMCRAFT_PREVIOUS_CORE }, t => {
    const root = workspace(t), file = join(root, 'ledger.sqlite'), db = new TaskLedger(file);
    db.register(binding(root)); db.close(); const before = files(root);
    const module = new URL('file://' + process.env.FILMCRAFT_PREVIOUS_CORE + '/src/harness/task_ledger.ts').href;
    const code = `import {TaskLedger} from ${JSON.stringify(module)};try{new TaskLedger(process.argv[1]);process.exit(1)}catch(e){console.log(e.code)}`;
    const result = spawnSync(process.execPath, ['--input-type=module', '-e', code, file], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr); assert.equal(result.stdout.trim(), 'ledger_schema_unsupported');
    assert.deepEqual(files(root), before);
    captureEvidence('actual-previous-version-downgrade-refusal', 'actual fixed dev45 installed core versus current schema6 SQLite fixture', { before, after: files(root), error: result.stdout.trim(), previousVersion: '0.1.0-dev.45' });
  });
