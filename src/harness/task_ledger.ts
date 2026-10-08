import { DatabaseSync } from 'node:sqlite';
import { randomUUID } from 'node:crypto';
import { isAbsolute, normalize } from 'node:path';
import { check, HarnessError, isHash, isObject, sha256, stableJson } from '../support/json.ts';
import { canonicalTarget } from '../support/paths.ts';

/** 仅为 ArtCraft 公共 runtimeIdentity 的领域消费类型，规范仍在固定所有者引用。 */
export type RuntimeIdentity = { pluginId: string; pluginVersion: string; cliVersion: string; sha256: string; mode: string; capabilitySnapshotSha256: string };
export type Binding = {
  taskId: string; namespace: string; idempotencyKey: string; planHash: string; nativePlanHash: string;
  inputHashes: Record<string, string>; inputRefs: { assetId: string; version: string; sha256: string }[];
  projectRevision: string | null; projectKey: string; outputRoot: string;
  sourceRevision: string; sourceTreeSha256: string; runtimeIdentity: RuntimeIdentity;
  authorizationRef: string; authorizationScopeSha256: string; deadline: number;
};
export type Lease = { taskId: string; attemptId: string; owner: string; epoch: number; expiresAt: number };
export type RecoveryLease = Lease & { recoveryId: string };
type Row = Record<string, any>;
const APPLICATION_ID = 0x46434c47;
const RECOVERY_SCHEMA = `CREATE TABLE recovery_intents(intent_id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(task_id),
  attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id), epoch INTEGER NOT NULL, owner TEXT NOT NULL, lease_until INTEGER NOT NULL,
  evidence_sha256 TEXT NOT NULL, state TEXT NOT NULL, completion_sha256 TEXT, reason TEXT, UNIQUE(task_id,epoch)) STRICT;`;
function identifier(value: unknown) { return typeof value === 'string' && value.length > 0 && value.length <= 256; }
function validate(binding: Binding) {
  check(isObject(binding), 'invalid_task_binding');
  for (const key of ['taskId', 'namespace', 'idempotencyKey', 'authorizationRef'] as const) {
    check(identifier(binding[key]), 'invalid_task_binding', key);
  }
  for (const key of ['planHash', 'nativePlanHash', 'projectKey', 'sourceTreeSha256', 'authorizationScopeSha256'] as const) {
    check(isHash(binding[key]), 'invalid_task_binding', key);
  }
  check(binding.projectRevision === null || isHash(binding.projectRevision), 'invalid_task_binding', 'projectRevision');
  check(typeof binding.sourceRevision === 'string' && /^[a-f0-9]{40}$/.test(binding.sourceRevision), 'invalid_task_binding', 'sourceRevision');
  check(typeof binding.outputRoot === 'string' && isAbsolute(binding.outputRoot) && normalize(binding.outputRoot) === binding.outputRoot, 'invalid_task_binding', 'outputRoot');
  check(Number.isSafeInteger(binding.deadline), 'invalid_task_binding', 'deadline');
  const runtime = binding.runtimeIdentity;
  check(isObject(runtime) && Object.keys(runtime).sort().join(',') === ['pluginId', 'pluginVersion', 'cliVersion', 'sha256', 'mode', 'capabilitySnapshotSha256'].sort().join(','), 'invalid_runtime_identity');
  check(runtime.pluginId === 'filmcraft' && identifier(runtime.pluginVersion) && identifier(runtime.cliVersion)
    && isHash(runtime.sha256) && isHash(runtime.capabilitySnapshotSha256) && ['headless', 'bridge'].includes(runtime.mode), 'invalid_runtime_identity');
  check(isObject(binding.inputHashes) && Object.values(binding.inputHashes).every(isHash) && Array.isArray(binding.inputRefs), 'input_identity_mismatch');
  const inputs = Object.create(null);
  for (const ref of binding.inputRefs) {
    check(isObject(ref) && identifier(ref.assetId) && identifier(ref.version) && isHash(ref.sha256)
      && Object.keys(ref).sort().join(',') === 'assetId,sha256,version' && !Object.hasOwn(inputs, ref.assetId), 'input_identity_mismatch');
    inputs[ref.assetId] = ref.sha256;
  }
  check(stableJson(inputs) === stableJson(binding.inputHashes), 'input_identity_mismatch');
}

/** SQLite 是唯一操作状态账本；原生工程和质量结论不由本类代替。 */
export class TaskLedger {
  db: DatabaseSync;
  readOnly: boolean;
  constructor(file: string, options: { readOnly?: boolean } = {}) {
    this.readOnly = options.readOnly === true;
    this.db = new DatabaseSync(file, { readOnly: this.readOnly });
    try {
      this.db.exec('PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON;');
      if (this.readOnly) {
        this.db.exec('PRAGMA query_only=ON;');
        const version = (this.db.prepare('PRAGMA user_version').get() as Row).user_version;
        check(version === 1 || version === 2, 'ledger_schema_unsupported');
        this.verifySchema(version);
      } else {
        this.transaction(() => {
          const version = (this.db.prepare('PRAGMA user_version').get() as Row).user_version;
          check(version === 0 || version === 1 || version === 2, 'ledger_schema_unsupported');
          if (version > 0) {
            this.verifySchema(version);
            if (version === 1) { this.db.exec(RECOVERY_SCHEMA + ' PRAGMA user_version=2;'); }
            return;
          }
          check(!this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").get(), 'ledger_schema_unknown');
          this.db.exec(`
            CREATE TABLE tasks(task_id TEXT PRIMARY KEY, namespace TEXT NOT NULL, idem TEXT NOT NULL,
              identity_hash TEXT NOT NULL, binding TEXT NOT NULL, state TEXT NOT NULL, epoch INTEGER NOT NULL DEFAULT 0,
              owner TEXT, lease_until INTEGER, attempt_id TEXT, UNIQUE(namespace, idem)) STRICT;
            CREATE TABLE project_leases(project_key TEXT PRIMARY KEY, task_id TEXT NOT NULL UNIQUE REFERENCES tasks(task_id), output_root TEXT NOT NULL UNIQUE) STRICT;
            CREATE TABLE attempts(attempt_id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(task_id), epoch INTEGER NOT NULL,
              operation_key TEXT NOT NULL, state TEXT NOT NULL, pid INTEGER, receipt_sha256 TEXT, UNIQUE(task_id, operation_key)) STRICT;
            CREATE TABLE receipts(task_id TEXT NOT NULL REFERENCES tasks(task_id), attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
              kind TEXT NOT NULL, sha256 TEXT NOT NULL, summary TEXT NOT NULL, status TEXT NOT NULL, PRIMARY KEY(attempt_id, kind)) STRICT;
            ${RECOVERY_SCHEMA}
            PRAGMA user_version=2;
            PRAGMA application_id=${APPLICATION_ID};
          `);
        });
        this.db.exec('PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;');
      }
    } catch (error) { this.db.close(); throw error; }
  }
  private verifySchema(version: number) {
    check((this.db.prepare('PRAGMA application_id').get() as Row).application_id === APPLICATION_ID, 'ledger_schema_unknown');
    const expected: Record<string, string> = {
      tasks: 'task_id,namespace,idem,identity_hash,binding,state,epoch,owner,lease_until,attempt_id',
      project_leases: 'project_key,task_id,output_root',
      attempts: 'attempt_id,task_id,epoch,operation_key,state,pid,receipt_sha256',
      receipts: 'task_id,attempt_id,kind,sha256,summary,status',
    };
    if (version === 2) { expected.recovery_intents = 'intent_id,task_id,attempt_id,epoch,owner,lease_until,evidence_sha256,state,completion_sha256,reason'; }
    const tables = this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").all() as Row[];
    check(tables.map(row => row.name).join(',') === Object.keys(expected).sort().join(','), 'ledger_schema_unknown');
    for (const [name, columns] of Object.entries(expected)) {
      const actual = this.db.prepare('SELECT name FROM pragma_table_info(?)').all(name) as Row[];
      check(actual.map(row => row.name).join(',') === columns, 'ledger_schema_unknown');
    }
  }
  close() { this.db.close(); }
  private transaction<T>(operation: () => T): T {
    check(!this.readOnly, 'ledger_read_only'); this.db.exec('BEGIN IMMEDIATE');
    try { const result = operation(); this.db.exec('COMMIT'); return result; }
    catch (error) { this.db.exec('ROLLBACK'); throw error; }
  }
  private row(taskId: string): Row {
    const row = this.db.prepare('SELECT * FROM tasks WHERE task_id=?').get(taskId) as Row | undefined;
    check(row, 'task_missing'); return row;
  }
  getTask(taskId: string) {
    const row = this.row(taskId);
    const binding = JSON.parse(row.binding) as Binding; validate(binding);
    const { taskId: boundId, ...identity } = binding;
    check(boundId === row.task_id && sha256(stableJson(identity)) === row.identity_hash, 'ledger_identity_corrupt');
    check(['planned','blocked','ready','running','reconciling','verifying','review_ready','completed','failed','cancel_requested','cancelled'].includes(row.state)
      && Number.isSafeInteger(row.epoch) && row.epoch >= 0, 'ledger_state_corrupt');
    return { taskId: row.task_id, state: row.state as string, epoch: row.epoch as number,
      attemptId: row.attempt_id as string | null, binding };
  }
  register(binding: Binding) {
    validate(binding);
    binding = { ...binding, outputRoot: canonicalTarget(binding.outputRoot) };
    const { taskId, ...identity } = binding;
    const fingerprint = sha256(stableJson(identity));
    return this.transaction(() => {
      const old = this.db.prepare('SELECT task_id,identity_hash FROM tasks WHERE namespace=? AND idem=?').get(binding.namespace, binding.idempotencyKey) as Row | undefined;
      if (old) { check(old.identity_hash === fingerprint, 'idempotency_conflict'); return this.getTask(old.task_id); }
      check(!this.db.prepare('SELECT task_id FROM tasks WHERE task_id=?').get(taskId), 'task_identity_conflict');
      this.db.prepare('INSERT INTO tasks(task_id,namespace,idem,identity_hash,binding,state) VALUES(?,?,?,?,?,?)')
        .run(taskId, binding.namespace, binding.idempotencyKey, fingerprint, stableJson(binding), 'planned');
      return this.getTask(taskId);
    });
  }
  claim(taskId: string, owner: string, ttlMs: number, now = Date.now()): Lease {
    check(identifier(owner) && Number.isSafeInteger(ttlMs) && ttlMs > 0 && ttlMs <= 24 * 3600_000 && Number.isSafeInteger(now), 'invalid_lease');
    const result = this.transaction(() => {
      const row = this.row(taskId), binding = JSON.parse(row.binding) as Binding;
      if (row.state === 'running' && row.lease_until <= now) {
        // 超时仅撤销旧执行者，保留工程占用；不会自动启动第二次编辑。
        this.db.prepare("UPDATE tasks SET state='reconciling',epoch=epoch+1 WHERE task_id=?").run(taskId);
        this.db.prepare("UPDATE attempts SET state='unknown' WHERE attempt_id=?").run(row.attempt_id);
        return { error: 'outcome_unknown' };
      }
      check(row.state !== 'reconciling', 'outcome_unknown');
      check(row.state !== 'running', 'lease_busy');
      check(['planned', 'ready'].includes(row.state), 'invalid_task_state');
      check(binding.deadline > now, 'deadline_exceeded');
      const occupied = this.db.prepare('SELECT task_id FROM project_leases WHERE project_key=?').get(binding.projectKey);
      check(!occupied, 'project_busy');
      check(!this.db.prepare('SELECT task_id FROM project_leases WHERE output_root=?').get(binding.outputRoot), 'output_busy');
      const epoch = row.epoch + 1, attemptId = randomUUID(), expiresAt = Math.min(now + ttlMs, binding.deadline);
      this.db.prepare('INSERT INTO project_leases VALUES(?,?,?)').run(binding.projectKey, taskId, binding.outputRoot);
      this.db.prepare("UPDATE tasks SET state='running',epoch=?,owner=?,lease_until=?,attempt_id=? WHERE task_id=?")
        .run(epoch, owner, expiresAt, attemptId, taskId);
      return { taskId, attemptId, owner, epoch, expiresAt };
    });
    if ('error' in result) { throw new HarnessError(result.error); }
    return result;
  }
  private verifyLease(lease: Lease, now: number) {
    const row = this.row(lease.taskId);
    check(row.epoch === lease.epoch && row.owner === lease.owner && row.attempt_id === lease.attemptId, 'stale_epoch');
    check(row.state === 'running', 'invalid_task_state');
    check(row.lease_until > now, 'lease_expired'); return row;
  }
  beginAttempt(lease: Lease, operationKey: string, now = Date.now()) {
    check(identifier(operationKey), 'invalid_operation_key');
    return this.transaction(() => {
      this.verifyLease(lease, now);
      const old = this.db.prepare('SELECT * FROM attempts WHERE task_id=? AND operation_key=?').get(lease.taskId, operationKey) as Row | undefined;
      if (old) { check(old.attempt_id === lease.attemptId, 'outcome_unknown'); return { attemptId: old.attempt_id, fresh: false, state: old.state }; }
      this.db.prepare('INSERT INTO attempts(attempt_id,task_id,epoch,operation_key,state) VALUES(?,?,?,?,?)')
        .run(lease.attemptId, lease.taskId, lease.epoch, operationKey, 'intent');
      return { attemptId: lease.attemptId, fresh: true, state: 'intent' };
    });
  }
  markSubmitted(lease: Lease, pid: number, now = Date.now()) {
    check(Number.isSafeInteger(pid) && pid > 0, 'invalid_process_identity');
    this.transaction(() => {
      this.verifyLease(lease, now);
      const result = this.db.prepare("UPDATE attempts SET state='submitted',pid=? WHERE attempt_id=? AND state='intent'").run(pid, lease.attemptId);
      check(result.changes === 1, 'intent_missing');
    });
  }
  finishAttempt(lease: Lease, result: { outcome: 'succeeded' | 'failed' | 'unknown'; stopped: boolean; receiptSha256: string | null }, now = Date.now()) {
    check(['succeeded', 'failed', 'unknown'].includes(result.outcome) && typeof result.stopped === 'boolean'
      && (result.receiptSha256 === null || isHash(result.receiptSha256)), 'invalid_attempt_result');
    this.transaction(() => {
      this.verifyLease(lease, now);
      check(this.db.prepare('SELECT attempt_id FROM attempts WHERE attempt_id=?').get(lease.attemptId), 'intent_missing');
      const unknown = result.outcome === 'unknown' || !result.stopped;
      if (!unknown && result.outcome === 'succeeded') { check(isHash(result.receiptSha256), 'artifact_invalid'); }
      this.db.prepare('UPDATE attempts SET state=?,receipt_sha256=? WHERE attempt_id=?')
        .run(unknown ? 'unknown' : result.outcome, result.receiptSha256, lease.attemptId);
      this.db.prepare('UPDATE tasks SET state=?,epoch=epoch+? WHERE task_id=?')
        .run(unknown ? 'reconciling' : result.outcome === 'succeeded' ? 'verifying' : 'failed', unknown ? 1 : 0, lease.taskId);
      if (!unknown) { this.db.prepare('DELETE FROM project_leases WHERE task_id=?').run(lease.taskId); }
    });
  }
  listAttempts(taskId: string) {
    this.row(taskId); return this.db.prepare('SELECT * FROM attempts WHERE task_id=? ORDER BY rowid').all(taskId) as Row[];
  }
  verifyAttempt(taskId: string, attemptId: string) {
    const attempt = this.db.prepare('SELECT * FROM attempts WHERE attempt_id=? AND task_id=?').get(attemptId, taskId) as Row | undefined;
    check(attempt, 'attempt_task_mismatch'); return attempt;
  }
  recordReceipt(taskId: string, attemptId: string, kind: string, digest: string, summary: unknown, status: string) {
    check(identifier(kind) && isHash(digest) && ['linked', 'unknown', 'conflict', 'stale'].includes(status), 'invalid_receipt_record');
    return this.transaction(() => {
      this.verifyAttempt(taskId, attemptId);
      const old = this.db.prepare('SELECT * FROM receipts WHERE attempt_id=? AND kind=?').get(attemptId, kind) as Row | undefined;
      if (old) { check(old.sha256 === digest && old.summary === stableJson(summary) && old.status === status, 'receipt_conflict'); return; }
      this.db.prepare('INSERT INTO receipts VALUES(?,?,?,?,?,?)').run(taskId, attemptId, kind, digest, stableJson(summary), status);
    });
  }
  receipts(taskId: string, attemptId: string) {
    this.verifyAttempt(taskId, attemptId);
    return (this.db.prepare('SELECT * FROM receipts WHERE task_id=? AND attempt_id=? ORDER BY kind').all(taskId, attemptId) as Row[])
      .map(row => ({ kind: row.kind, sha256: row.sha256, status: row.status, summary: JSON.parse(row.summary) }));
  }
  /** 在原生停止和证据门禁之后取得恢复租约；意图先独立提交，仍保留工程占用。 */
  beginRecovery(taskId: string, expectedEpoch: number, evidenceSha256: string, owner: string, ttlMs = 30_000, now = Date.now()): RecoveryLease {
    check(Number.isSafeInteger(expectedEpoch) && isHash(evidenceSha256) && identifier(owner)
      && Number.isSafeInteger(ttlMs) && ttlMs > 0 && ttlMs <= 60_000, 'invalid_recovery_request');
    return this.transaction(() => {
      const row = this.row(taskId); this.getTask(taskId);
      check(row.epoch === expectedEpoch, 'stale_epoch');
      check(['running', 'reconciling'].includes(row.state) && typeof row.attempt_id === 'string', 'invalid_task_state');
      check(row.state !== 'running' || row.lease_until <= now, 'lease_busy');
      const occupied = this.db.prepare('SELECT * FROM project_leases WHERE task_id=?').get(taskId) as Row | undefined;
      check(occupied && occupied.project_key === JSON.parse(row.binding).projectKey, 'occupancy_missing');
      const pending = this.db.prepare("SELECT * FROM recovery_intents WHERE task_id=? AND state='pending' ORDER BY epoch DESC LIMIT 1").get(taskId) as Row | undefined;
      check(!pending || pending.lease_until <= now, 'recovery_busy');
      if (pending) { this.db.prepare("UPDATE recovery_intents SET state='abandoned',reason='recovery_lease_expired' WHERE intent_id=?").run(pending.intent_id); }
      const epoch = row.epoch + 1, recoveryId = randomUUID(), expiresAt = now + ttlMs;
      this.db.prepare('INSERT INTO recovery_intents(intent_id,task_id,attempt_id,epoch,owner,lease_until,evidence_sha256,state) VALUES(?,?,?,?,?,?,?,?)')
        .run(recoveryId, taskId, row.attempt_id, epoch, owner, expiresAt, evidenceSha256, 'pending');
      this.db.prepare("UPDATE tasks SET state='reconciling',epoch=?,owner=?,lease_until=? WHERE task_id=?").run(epoch, owner, expiresAt, taskId);
      return { taskId, attemptId: row.attempt_id, owner, epoch, expiresAt, recoveryId };
    });
  }
  private verifyRecovery(lease: RecoveryLease, now: number) {
    const row = this.row(lease.taskId);
    check(row.epoch === lease.epoch && row.owner === lease.owner && row.attempt_id === lease.attemptId, 'stale_epoch');
    check(row.state === 'reconciling' && row.lease_until > now, 'recovery_lease_expired');
    const intent = this.db.prepare("SELECT * FROM recovery_intents WHERE intent_id=? AND state='pending'").get(lease.recoveryId) as Row | undefined;
    check(intent && intent.task_id === lease.taskId && intent.attempt_id === lease.attemptId && intent.epoch === lease.epoch, 'recovery_intent_missing');
  }
  /** 仅将已重新核验的原执行收敛到 verifying；不重放、不作质量验收。 */
  finishRecovery(lease: RecoveryLease, evidenceSha256: string, deliverySha256: string, executionSha256: string, now = Date.now()) {
    check(isHash(evidenceSha256) && isHash(deliverySha256) && isHash(executionSha256), 'invalid_recovery_evidence');
    this.transaction(() => {
      this.verifyRecovery(lease, now);
      for (const [kind, digest] of [['delivery', deliverySha256], ['output-execution', executionSha256]]) {
        const receipt = this.db.prepare('SELECT * FROM receipts WHERE task_id=? AND attempt_id=? AND kind=?').get(lease.taskId, lease.attemptId, kind) as Row | undefined;
        check(receipt && receipt.status === 'linked' && receipt.sha256 === digest, 'recovery_evidence_missing');
      }
      this.db.prepare("UPDATE attempts SET state='succeeded',receipt_sha256=? WHERE attempt_id=?").run(deliverySha256, lease.attemptId);
      this.db.prepare("UPDATE tasks SET state='verifying',owner=NULL,lease_until=NULL WHERE task_id=?").run(lease.taskId);
      this.db.prepare("UPDATE recovery_intents SET state='applied',completion_sha256=? WHERE intent_id=?").run(evidenceSha256, lease.recoveryId);
      this.db.prepare('DELETE FROM project_leases WHERE task_id=?').run(lease.taskId);
    });
  }
  /** 恢复证据过期时撤销恢复租约，保留未知状态和工程占用。 */
  abandonRecovery(lease: RecoveryLease, reason: string, now = Date.now()) {
    check(identifier(reason), 'invalid_recovery_reason');
    this.transaction(() => {
      this.verifyRecovery(lease, now);
      this.db.prepare("UPDATE recovery_intents SET state='abandoned',reason=? WHERE intent_id=?").run(reason, lease.recoveryId);
      this.db.prepare('UPDATE tasks SET epoch=epoch+1,owner=NULL,lease_until=NULL WHERE task_id=?').run(lease.taskId);
    });
  }
  /** 只读返回恢复审计；V1 只读快照尚无该表时返回空数组。 */
  listRecoveryIntents(taskId: string) {
    this.row(taskId);
    if (!(this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='recovery_intents'").get())) { return []; }
    return this.db.prepare('SELECT * FROM recovery_intents WHERE task_id=? ORDER BY epoch').all(taskId) as Row[];
  }
}
