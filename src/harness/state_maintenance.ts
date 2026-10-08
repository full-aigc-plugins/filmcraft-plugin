import { DatabaseSync } from 'node:sqlite';
import { closeSync, existsSync, fsyncSync, mkdirSync, openSync, realpathSync, writeFileSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { forensicSnapshot } from './forensic_snapshot.ts';
import { APPLICATION_ID, CONTINUATION_SCHEMA, RECOVERY_SCHEMA } from './task_ledger.ts';
import { RESOURCE_SCHEMA, RESOURCE_TABLES } from './resource_schema.ts';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { requireAuthorization } from './authorization.ts';
import type { Authorizer, AuthorizationRequest } from './authorization.ts';
import { check, sha256, stableJson } from '../support/json.ts';

const tables = ['tasks', 'project_leases', 'attempts', 'receipts'];
function records(db: DatabaseSync) {
  const result: Record<string, any> = {};
  for (const name of [...tables, 'recovery_intents', 'continuation_intents', ...RESOURCE_TABLES]) {
    if (db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name=?").get(name)) {
      result[name] = db.prepare('SELECT * FROM ' + name + ' ORDER BY rowid').all();
    }
  }
  return result;
}
function baseRecords(value: Record<string, any>) {
  return Object.fromEntries(tables.map(name => [name, value[name]]));
}
function durable(path: string, data: string | Buffer) {
  const fd = openSync(path, 'wx', 0o600);
  try { writeFileSync(fd, data); fsyncSync(fd); } finally { closeSync(fd); }
}
function syncDirectory(path: string) {
  const fd = openSync(path, 'r'); try { fsyncSync(fd); } finally { closeSync(fd); }
}

/** 显式、可审计的状态升级/回退；先隔离核验，再锁住写入并保全旧原始记录。 */
export class StateMaintenance {
  file: string;
  authorize?: Authorizer;
  constructor(file: string, options: { authorize?: Authorizer } = {}) { this.file = resolve(file); this.authorize = options.authorize; }
  inspect() {
    return forensicSnapshot(this.file, (ledger, bytes) => ({ version: Number(ledger.db.prepare('PRAGMA user_version').get()!.user_version),
      bytes, records: records(ledger.db) }));
  }
  private locked<T>(expected: ReturnType<StateMaintenance['inspect']>, work: (db: DatabaseSync) => T) {
    const db = new DatabaseSync(this.file); let committed = false;
    try {
      db.exec('PRAGMA busy_timeout=0; PRAGMA foreign_keys=ON; BEGIN IMMEDIATE;');
      check(Number(db.prepare('PRAGMA application_id').get()!.application_id) === APPLICATION_ID
        && Number(db.prepare('PRAGMA user_version').get()!.user_version) === expected.version
        && stableJson(records(db)) === stableJson(expected.records), 'ledger_changed');
      // 不在仍有有效执行/恢复写租约时升级；未知结果的持久占用仍完整保留。
      check(!db.prepare("SELECT task_id FROM tasks WHERE state IN ('running','reconciling','cancel_requested') AND owner IS NOT NULL AND lease_until>?").get(Date.now()), 'ledger_not_quiescent');
      const result = work(db); db.exec('COMMIT'); committed = true; return result;
    } finally { if (!committed) { try { db.exec('ROLLBACK'); } catch {} } db.close(); }
  }
  upgrade(backupRoot: string, request: AuthorizationRequest) {
    const captured = this.inspect(); check([1, 2, 3].includes(captured.version), 'ledger_upgrade_unsupported');
    const subject = { action: 'upgrade' as const, identitySha256: sha256(stableJson(captured)) };
    requireAuthorization(this.authorize, request, subject);
    backupRoot = resolve(backupRoot); check(!existsSync(backupRoot), 'backup_exists');
    return this.locked(captured, db => {
      requireAuthorization(this.authorize, request, subject);
      mkdirSync(backupRoot, { mode: 0o700 });
      const sourceParent = realpathSync(dirname(this.file)), sourceName = basename(this.file);
      const files: Record<string, string> = {};
      for (const [suffix, name] of [['', 'database.sqlite'], ['-wal', 'database.sqlite-wal'], ['-shm', 'shm.audit']]) {
        try { const bytes = readBoundFile(sourceParent, sourceName + suffix, 64 * 1024 * 1024);
          durable(join(backupRoot, name), bytes); files[name] = sha256(bytes);
        } catch (error: any) { if (suffix === '' || error.code !== 'ENOENT') { throw error; } }
      }
      const verified = forensicSnapshot(join(backupRoot, 'database.sqlite'), ledger => records(ledger.db));
      check(stableJson(verified) === stableJson(captured.records), 'backup_invalid');
      const manifest = { schema: 'filmcraft-ledger-backup/v1', fromVersion: captured.version, toVersion: 4,
        recordsSha256: sha256(stableJson(captured.records)), baseRecordsSha256: sha256(stableJson(baseRecords(captured.records))),
        files, complete: true };
      const data = stableJson(manifest) + '\n'; durable(join(backupRoot, 'manifest.json'), data);
      durable(join(backupRoot, 'upgrade-intent.json'), stableJson({ subject, ...request, backupManifestSha256: sha256(data) }) + '\n');
      syncDirectory(backupRoot); requireAuthorization(this.authorize, request, subject);
      if (captured.version === 1) { db.exec(RECOVERY_SCHEMA); }
      if (captured.version < 3) { db.exec(CONTINUATION_SCHEMA); }
      db.exec(RESOURCE_SCHEMA + ' PRAGMA user_version=4;');
      const after = records(db);
      check(Object.keys(captured.records).every(name => stableJson(after[name]) === stableJson(captured.records[name])), 'migration_data_changed');
      return { fromVersion: captured.version, toVersion: 4, backupRoot, backupManifestSha256: sha256(data), recordsPreserved: true };
    });
  }
  rollback(backupRoot: string, request: AuthorizationRequest) {
    backupRoot = realpathSync(backupRoot);
    const raw = readBoundFile(backupRoot, 'manifest.json'), manifest = JSON.parse(raw.toString('utf8'));
    check(manifest.schema === 'filmcraft-ledger-backup/v1' && manifest.complete === true
      && [1, 2, 3].includes(manifest.fromVersion) && [3, 4].includes(manifest.toVersion)
      && manifest.fromVersion < manifest.toVersion, 'backup_invalid');
    for (const [name, digest] of Object.entries(manifest.files)) { check(sha256(readBoundFile(backupRoot, name, 64 * 1024 * 1024)) === digest, 'backup_invalid'); }
    const restored = forensicSnapshot(join(backupRoot, 'database.sqlite'), ledger => records(ledger.db));
    check(sha256(stableJson(restored)) === manifest.recordsSha256, 'backup_invalid');
    const captured = this.inspect();
    const subject = { action: 'rollback' as const, identitySha256: sha256(stableJson({ backupManifestSha256: sha256(raw), recordsSha256: manifest.recordsSha256 })) };
    requireAuthorization(this.authorize, request, subject);
    check(captured.version === manifest.toVersion || captured.version === manifest.fromVersion, 'ledger_downgrade_unsupported');
    check(sha256(stableJson(baseRecords(captured.records))) === manifest.baseRecordsSha256
      && Object.keys(captured.records).every(name => stableJson(captured.records[name] ?? []) === stableJson(restored[name] ?? [])), 'rollback_changes_conflict');
    if (captured.version === manifest.fromVersion) { return { version: captured.version, reused: true, recordsPreserved: true }; }
    return this.locked(captured, db => {
      requireAuthorization(this.authorize, request, subject);
      durable(join(backupRoot, 'rollback-intent.json'), stableJson({ subject, ...request, currentRecordsSha256: sha256(stableJson(captured.records)) }) + '\n');
      syncDirectory(backupRoot); requireAuthorization(this.authorize, request, subject);
      if (manifest.toVersion === 4) { db.exec('DROP TABLE cancel_intents; DROP TABLE task_resources; DROP TABLE resource_scopes;'); }
      if (manifest.fromVersion < 3) { db.exec('DROP TABLE continuation_intents;'); }
      if (manifest.fromVersion === 1) { db.exec('DROP TABLE recovery_intents;'); }
      db.exec('PRAGMA user_version=' + manifest.fromVersion);
      check(stableJson(records(db)) === stableJson(restored), 'rollback_data_changed');
      return { version: manifest.fromVersion, reused: false, recordsPreserved: true };
    });
  }
}
