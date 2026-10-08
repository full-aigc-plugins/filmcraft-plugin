import { DEPLOYMENT_SCHEMA, assertRuntimeSelection, deploymentHistory } from '../adapters/runtime_deployment.ts';
import { existsSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { randomUUID } from 'node:crypto';
import { isAbsolute, normalize } from 'node:path';
import { check, HarnessError, isHash, isObject, sha256, stableJson } from '../support/json.ts';
import { canonicalTarget } from '../support/paths.ts';
import { RESOURCE_SCHEMA } from './resource_schema.ts';
import { ResourceController } from './resources.ts';
import { REVISION_SCHEMA, verifyRevisionIntegrity } from '../quality/revision_schema.ts';

/** 仅为 ArtCraft 公共 runtimeIdentity 的领域消费类型，规范仍在固定所有者引用。 */
export type RuntimeIdentity = { pluginId: string; pluginVersion: string; cliVersion: string; sha256: string; mode: string; capabilitySnapshotSha256: string };
export type Binding = {
  taskId: string; namespace: string; idempotencyKey: string; planHash: string; nativePlanHash: string;
  inputHashes: Record<string, string>; inputRefs: { assetId: string; version: string; sha256: string }[];
  projectRevision: string | null; projectKey: string; outputRoot: string;
  sourceRevision: string; sourceTreeSha256: string; runtimeIdentity: RuntimeIdentity;
  authorizationRef: string; authorizationScopeSha256: string; deadline: number; executionPermissionsSha256?: string;
};
export type Lease = { taskId: string; attemptId: string; owner: string; epoch: number; expiresAt: number };
export type RecoveryLease = Lease & { recoveryId: string };
type Row = Record<string, any>;
export const APPLICATION_ID = 0x46434c47;
export const RECOVERY_SCHEMA = `CREATE TABLE recovery_intents(intent_id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(task_id),
  attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id), epoch INTEGER NOT NULL, owner TEXT NOT NULL, lease_until INTEGER NOT NULL,
  evidence_sha256 TEXT NOT NULL, state TEXT NOT NULL, completion_sha256 TEXT, reason TEXT, UNIQUE(task_id,epoch)) STRICT;`;
export const CONTINUATION_SCHEMA = `CREATE TABLE continuation_intents(intent_id TEXT PRIMARY KEY,
  parent_task_id TEXT NOT NULL REFERENCES tasks(task_id), parent_attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
  parent_epoch INTEGER NOT NULL, child_task_id TEXT NOT NULL UNIQUE REFERENCES tasks(task_id),
  binding_sha256 TEXT NOT NULL, evidence_sha256 TEXT NOT NULL, state TEXT NOT NULL, UNIQUE(parent_task_id,child_task_id)) STRICT;`;
function identifier(value: unknown) { return typeof value === 'string' && value.length > 0 && value.length <= 256; }
function validate(binding: Binding) {
  check(isObject(binding), 'invalid_task_binding');
  for (const key of ['taskId', 'namespace', 'idempotencyKey', 'authorizationRef'] as const) {
    check(identifier(binding[key]), 'invalid_task_binding', key);
  }
  for (const key of ['planHash', 'nativePlanHash', 'projectKey', 'sourceTreeSha256', 'authorizationScopeSha256'] as const) {
    check(isHash(binding[key]), 'invalid_task_binding', key);
  }
  check(binding.executionPermissionsSha256 === undefined || isHash(binding.executionPermissionsSha256), 'invalid_task_binding');
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
    const existed = existsSync(file);
    this.readOnly = options.readOnly === true;
    this.db = new DatabaseSync(file, { readOnly: this.readOnly });
    try {
      this.db.exec('PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON;');
      if (this.readOnly) {
        this.db.exec('PRAGMA query_only=ON;');
        const version = (this.db.prepare('PRAGMA user_version').get() as Row).user_version;
        check([1, 2, 3, 4, 5, 6].includes(version), 'ledger_schema_unsupported');
        this.verifySchema(version);
      } else {
        this.transaction(() => {
          const version = (this.db.prepare('PRAGMA user_version').get() as Row).user_version;
          check([0, 1, 2, 3, 4, 5, 6].includes(version), 'ledger_schema_unsupported');
          if (version > 0) {
            this.verifySchema(version);
            check(version === 6, 'ledger_upgrade_required');
            return;
          }
          check(!existed, 'ledger_schema_unknown');
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
            ${CONTINUATION_SCHEMA}
            ${RESOURCE_SCHEMA}
            ${REVISION_SCHEMA}
            ${DEPLOYMENT_SCHEMA}
            PRAGMA user_version=6;
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
    if (version >= 2) { expected.recovery_intents = 'intent_id,task_id,attempt_id,epoch,owner,lease_until,evidence_sha256,state,completion_sha256,reason'; }
    if (version >= 3) { expected.continuation_intents = 'intent_id,parent_task_id,parent_attempt_id,parent_epoch,child_task_id,binding_sha256,evidence_sha256,state'; }
    if (version >= 4) {
      expected.resource_scopes = 'scope_id,limits,deadline,state,reason,created_at';
      expected.task_resources = 'task_id,scope_id,allocation,state,reserved_at,consumed,process_identity';
      expected.cancel_intents = 'task_id,scope_id,request,created_at,diagnosis';
    }
    if(version>=5){
      expected.revision_loops='loop_id,root_task_id,policy_sha256,definition,state,reason,generation,created_at';
      expected.revision_rounds='loop_id,round_no,child_task_id,intent_sha256,intent,state,result,result_sha256';
    }
    if(version>=6){expected.runtime_deployments='generation,descriptor,descriptor_sha256,action,authorization_ref,created_at';}
    const tables = this.db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").all() as Row[];
    check(tables.map(row => row.name).join(',') === Object.keys(expected).sort().join(','), 'ledger_schema_unknown');
    check(!this.db.prepare("SELECT name FROM sqlite_master WHERE type IN ('view','trigger')").get(), 'ledger_schema_unknown');
    for (const [name, columns] of Object.entries(expected)) {
      const actual = this.db.prepare('SELECT name,type,"notnull",pk FROM pragma_table_info(?)').all(name) as Row[];
      check(actual.map(row => row.name).join(',') === columns, 'ledger_schema_unknown');
      const strict = this.db.prepare('SELECT strict FROM pragma_table_list WHERE name=?').get(name) as Row;
      check(strict?.strict === 1, 'ledger_schema_unknown');
      const nullable: Record<string, string[]> = { tasks: ['owner','lease_until','attempt_id'], attempts: ['pid','receipt_sha256'],
        recovery_intents: ['completion_sha256','reason'], resource_scopes: ['reason'], task_resources: ['consumed','process_identity'],
        revision_loops:['reason'],revision_rounds:['result','result_sha256'] };
      const primary: Record<string, string[]> = { tasks: ['task_id'], project_leases: ['project_key'], attempts: ['attempt_id'],
        receipts: ['attempt_id','kind'], recovery_intents: ['intent_id'], continuation_intents: ['intent_id'],
        resource_scopes: ['scope_id'], task_resources: ['task_id'], cancel_intents: ['task_id'],revision_loops:['loop_id'],revision_rounds:['loop_id','round_no'],runtime_deployments:['generation'] };
      for (const column of actual) {
        const integer = ['epoch','lease_until','pid','parent_epoch','deadline','created_at','reserved_at','generation','round_no'].includes(column.name);
        check(column.type === (integer ? 'INTEGER' : 'TEXT')
          && column.notnull === (nullable[name]?.includes(column.name) ? 0 : 1)
          && column.pk === Math.max(0, primary[name].indexOf(column.name) + 1), 'ledger_schema_unknown');
      }
      const unique: Record<string, string[]> = {
        tasks: ['task_id', 'namespace,idem'], project_leases: ['project_key', 'task_id', 'output_root'],
        attempts: ['attempt_id', 'task_id,operation_key'], receipts: ['attempt_id,kind'],
        recovery_intents: ['intent_id', 'task_id,epoch'], continuation_intents: ['intent_id', 'child_task_id', 'parent_task_id,child_task_id'],
        resource_scopes: ['scope_id'], task_resources: ['task_id'], cancel_intents: ['task_id'],
        revision_loops:['loop_id','root_task_id'],revision_rounds:['loop_id,round_no','child_task_id'],runtime_deployments:[],
      };
      const indices = this.db.prepare('SELECT name FROM pragma_index_list(?) WHERE "unique"=1').all(name) as Row[];
      const constraints = indices.map(index => (this.db.prepare('SELECT name FROM pragma_index_info(?) ORDER BY seqno')
        .all(index.name) as Row[]).map(column => column.name).join(',')).sort();
      check(stableJson(constraints) === stableJson(unique[name].sort()), 'ledger_schema_unknown');
      const foreign: Record<string, string[]> = {
        tasks: [], project_leases: ['task_id:tasks:task_id'], attempts: ['task_id:tasks:task_id'],
        receipts: ['task_id:tasks:task_id','attempt_id:attempts:attempt_id'],
        recovery_intents: ['task_id:tasks:task_id','attempt_id:attempts:attempt_id'],
        continuation_intents: ['parent_task_id:tasks:task_id','parent_attempt_id:attempts:attempt_id','child_task_id:tasks:task_id'],
        resource_scopes: ['scope_id:tasks:task_id'], task_resources: ['task_id:tasks:task_id','scope_id:resource_scopes:scope_id'],
        cancel_intents: ['task_id:tasks:task_id','scope_id:resource_scopes:scope_id'],
        revision_loops:['root_task_id:tasks:task_id'],revision_rounds:['loop_id:revision_loops:loop_id','child_task_id:tasks:task_id'],runtime_deployments:[],
      };
      const keys = (this.db.prepare('SELECT "from","table","to" FROM pragma_foreign_key_list(?)').all(name) as Row[])
        .map(key => key.from + ':' + key.table + ':' + key.to).sort();
      check(stableJson(keys) === stableJson(foreign[name].sort()), 'ledger_schema_unknown');
    }
  }
  /** 全表逻辑检查用于隔离诊断和升级预检；不修改旧结构或记录。 */
  verifyIntegrity() {
    const tasks = this.db.prepare('SELECT task_id FROM tasks').all() as Row[];
    for (const row of tasks) {
      const task = this.getTask(row.task_id);
      if (task.attemptId && task.state !== 'running') { this.verifyAttempt(task.taskId, task.attemptId); }
    }
    for (const row of this.db.prepare('SELECT * FROM attempts').all() as Row[]) {
      const task = this.getTask(row.task_id);
      check(identifier(row.operation_key) && Number.isSafeInteger(row.epoch) && row.epoch > 0 && row.epoch <= task.epoch
        && ['intent','submitted','unknown','succeeded','failed'].includes(row.state)
        && (row.pid === null || Number.isSafeInteger(row.pid) && row.pid > 0), 'ledger_state_corrupt');
    }
    for (const row of this.db.prepare('SELECT * FROM project_leases').all() as Row[]) {
      const task = this.getTask(row.task_id);
      check(row.project_key === task.binding.projectKey && row.output_root === task.binding.outputRoot
        && ['running','reconciling','cancel_requested'].includes(task.state), 'ledger_occupancy_corrupt');
    }
    for (const row of tasks) {
      const task = this.getTask(row.task_id);
      if (['running','reconciling','cancel_requested'].includes(task.state)) {
        check(this.db.prepare('SELECT task_id FROM project_leases WHERE task_id=?').get(task.taskId), 'ledger_occupancy_corrupt');
      }
    }
    for (const row of this.db.prepare('SELECT * FROM receipts').all() as Row[]) {
      this.verifyAttempt(row.task_id, row.attempt_id);
      check(['command','delivery','failed-stage','output-execution'].includes(row.kind) && isHash(row.sha256)
        && ['linked','unknown','conflict','stale'].includes(row.status) && isObject(JSON.parse(row.summary)), 'ledger_receipt_corrupt');
    }
    if (Number(this.db.prepare('PRAGMA user_version').get()!.user_version) >= 4) { new ResourceController(this).verifyIntegrity(); }
    if (Number(this.db.prepare('PRAGMA user_version').get()!.user_version) >= 5) { verifyRevisionIntegrity(this.db); }
    if (Number(this.db.prepare('PRAGMA user_version').get()!.user_version) >= 6) { deploymentHistory(this.db); }
  }
  close() { this.db.close(); }
  /** 预检只核验已选身份；最终注册与领取在同一写事务内复查。 */
  assertRuntime(binding: Pick<Binding,'sourceRevision'|'sourceTreeSha256'|'runtimeIdentity'>){assertRuntimeSelection(this.db,binding);}
  /** 同账本资源控制器使用同一原子事务；禁止在回调内启动原生副作用。 */
  transaction<T>(operation: () => T): T {
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
      this.assertRuntime(binding);
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
      this.assertRuntime(binding);
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
      new ResourceController(this).assertDispatch(taskId, now);
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
      this.verifyLease(lease, now);this.assertRuntime(this.getTask(lease.taskId).binding);
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
  /** 先登记新任务与继续意图；只接受已确认的原工程，不重用原生尝试。 */
  beginContinuation(parentId: string, expectedEpoch: number, evidenceSha256: string, child: Binding,
    onIntent?:(intentId:string,reused:boolean)=>void) {
    validate(child); child = { ...child, outputRoot: canonicalTarget(child.outputRoot) };
    check(parentId !== child.taskId && isHash(evidenceSha256), 'invalid_continuation');
    return this.transaction(() => {
      const parent = this.getTask(parentId);
      check(parent.epoch === expectedEpoch && parent.state === 'verifying' && parent.attemptId, 'stale_epoch');
      const childHash = sha256(stableJson(child));
      const existing = this.db.prepare('SELECT * FROM continuation_intents WHERE child_task_id=?').get(child.taskId) as Row | undefined;
      if (existing) {
        check(existing.parent_task_id === parentId && existing.parent_attempt_id === parent.attemptId
          && existing.binding_sha256 === childHash, 'continuation_conflict');
        this.getTask(child.taskId);onIntent?.(existing.intent_id,true); return { intentId: existing.intent_id, reused: true };
      }
      check(!this.db.prepare('SELECT task_id FROM tasks WHERE task_id=? OR (namespace=? AND idem=?)')
        .get(child.taskId, child.namespace, child.idempotencyKey), 'continuation_conflict');
      const { taskId, ...identity } = child;
      this.db.prepare('INSERT INTO tasks(task_id,namespace,idem,identity_hash,binding,state) VALUES(?,?,?,?,?,?)')
        .run(taskId, child.namespace, child.idempotencyKey, sha256(stableJson(identity)), stableJson(child), 'planned');
      const intentId = randomUUID();
      this.db.prepare('INSERT INTO continuation_intents VALUES(?,?,?,?,?,?,?,?)')
        .run(intentId, parentId, parent.attemptId, parent.epoch, taskId, childHash, evidenceSha256, 'pending');
      onIntent?.(intentId,false);
      return { intentId, reused: false };
    });
  }
  /** 原子登记继续执行的观察状态；不把未知结果提升为完成。 */
  observeContinuation(intentId: string) {
    return this.transaction(() => {
      const row = this.db.prepare('SELECT * FROM continuation_intents WHERE intent_id=?').get(intentId) as Row | undefined;
      check(row, 'continuation_missing'); const child = this.getTask(row.child_task_id);
      const state = child.state === 'verifying' ? 'applied' : child.state === 'failed' ? 'failed' : 'pending';
      if (row.state !== state) { this.db.prepare('UPDATE continuation_intents SET state=? WHERE intent_id=?').run(state, intentId); }
      return { intentId, state, childTaskId: child.taskId, childAttemptId: child.attemptId };
    });
  }
  listContinuations(parentId: string) {
    this.getTask(parentId);
    return this.db.prepare('SELECT * FROM continuation_intents WHERE parent_task_id=? ORDER BY rowid').all(parentId) as Row[];
  }

}
