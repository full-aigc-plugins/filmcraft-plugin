import { existsSync, lstatSync, readdirSync, statfsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import type { TaskLedger } from './task_ledger.ts';
import { check, HarnessError, isObject, stableJson } from '../support/json.ts';

export type ResourceAmounts = { timeMs: number; diskBytes: number; outputBytes: number; slots: number; revisions: number };
export type ResourcePolicy = { limits?: ResourceAmounts; allocation: ResourceAmounts };
const fields = ['timeMs', 'diskBytes', 'outputBytes', 'slots', 'revisions'] as const;
const errors = { timeMs: 'budget_time_exceeded', diskBytes: 'budget_disk_exceeded', outputBytes: 'budget_output_exceeded',
  slots: 'budget_concurrency_exceeded', revisions: 'budget_revisions_exceeded' };
export function validateAmounts(value: unknown): asserts value is ResourceAmounts {
  check(isObject(value) && Object.keys(value).sort().join(',') === [...fields].sort().join(',')
    && fields.every(key => Number.isSafeInteger(value[key]) && value[key] >= 0)
    && value.timeMs > 0 && value.slots > 0, 'invalid_resource_budget');
}
function freeBytes(path: string) {
  while (!existsSync(path)) { const parent = dirname(path); check(parent !== path, 'disk_probe_failed'); path = parent; }
  const stat = statfsSync(path, { bigint: true });
  return Number(stat.bavail * stat.bsize);
}
/** 计量真实输出字节；链接、特殊文件或不可读目录不能作为已确认的低占用。 */
export function outputBytes(path: string): number {
  if (!existsSync(path)) { return 0; }
  const info = lstatSync(path); check(!info.isSymbolicLink(), 'output_measurement_unknown');
  if (info.isFile()) { check(Number.isSafeInteger(info.size), 'output_measurement_unknown'); return info.size; }
  check(info.isDirectory(), 'output_measurement_unknown');
  let size = 0;
  for (const name of readdirSync(path)) { size += outputBytes(join(path, name)); check(Number.isSafeInteger(size), 'output_measurement_unknown'); }
  return size;
}

/** 持久预留先于原生执行；重启读取同一记录，不释放未知尝试或删除部分产物。 */
export class ResourceController {
  ledger: TaskLedger;
  freeBytes: (path: string) => number;
  constructor(ledger: TaskLedger, probes: { freeBytes?: (path: string) => number } = {}) {
    this.ledger = ledger; this.freeBytes = probes.freeBytes ?? freeBytes;
  }
  /** 隔离恢复前验证预算账目结构与任务归属；损坏数据不能当作剩余额度。 */
  verifyIntegrity() {
    try {
      for (const scope of this.ledger.db.prepare('SELECT * FROM resource_scopes').all() as any[]) {
        const root = this.ledger.getTask(scope.scope_id); validateAmounts(JSON.parse(scope.limits));
        check(['active','halted','cancel_requested'].includes(scope.state)
          && Number.isSafeInteger(scope.deadline) && scope.deadline === root.binding.deadline
          && Number.isSafeInteger(scope.created_at)
          && (scope.reason === null || typeof scope.reason === 'string' && scope.reason.length <= 256), 'ledger_resource_corrupt');
        const snapshot = this.snapshot(scope.scope_id);
        for (const row of snapshot.reservations) {
          const task = this.ledger.getTask(row.task_id), allocation = JSON.parse(row.allocation);
          check(Number.isSafeInteger(row.reserved_at) && row.reserved_at >= scope.created_at, 'ledger_resource_corrupt');
          if (row.state === 'settled') {
            const consumed = JSON.parse(row.consumed);
            check(isObject(consumed) && Object.keys(consumed).sort().join(',') === [...fields].sort().join(',')
              && fields.every(key => Number.isSafeInteger(consumed[key]) && consumed[key] >= 0)
              && consumed.slots === 0 && consumed.revisions === allocation.revisions
              && ['verifying','failed','cancelled','completed'].includes(task.state), 'ledger_resource_corrupt');
          } else { check(row.consumed === null, 'ledger_resource_corrupt'); }
          if (row.process_identity !== null) {
            const process = JSON.parse(row.process_identity), attempt = this.ledger.verifyAttempt(row.task_id, process.attemptId);
            check(attempt.pid === process.identity?.pid && attempt.epoch === process.epoch
              && process.attemptId === task.attemptId && process.identity.pgid === process.identity.pid
              && typeof process.identity.started === 'string' && typeof process.identity.boot === 'string'
              && typeof process.identity.executable === 'string' && typeof process.stopSupported === 'boolean', 'ledger_resource_corrupt');
          }
        }
      }
      for (const intent of this.ledger.db.prepare('SELECT * FROM cancel_intents').all() as any[]) {
        const snapshot = this.snapshot(intent.task_id);
        check(snapshot.scopeId === intent.scope_id && snapshot.state === 'cancel_requested'
          && Number.isSafeInteger(intent.created_at) && ['requested','not_started','running','stopped','unknown'].includes(intent.diagnosis)
          && isObject(JSON.parse(intent.request)), 'ledger_resource_corrupt');
      }
    } catch { throw new HarnessError('ledger_resource_corrupt'); }
  }
  snapshot(taskId: string) {
    const row = this.ledger.db.prepare('SELECT scope_id FROM task_resources WHERE task_id=?').get(taskId);
    const scopeId = String(row?.scope_id ?? taskId);
    const scope = this.ledger.db.prepare('SELECT * FROM resource_scopes WHERE scope_id=?').get(scopeId) as any;
    check(scope, 'budget_required'); validateAmounts(JSON.parse(scope.limits));
    const reservations = this.ledger.db.prepare('SELECT * FROM task_resources WHERE scope_id=? ORDER BY rowid').all(scopeId) as any[];
    for (const reservation of reservations) {
      validateAmounts(JSON.parse(reservation.allocation));
      check(['reserved','settled'].includes(reservation.state), 'ledger_resource_corrupt');
    }
    return { scopeId, limits: JSON.parse(scope.limits) as ResourceAmounts, deadline: scope.deadline as number,
      state: scope.state as string, reason: scope.reason as string | null, reservations };
  }
  reserve(taskId: string, policy?: ResourcePolicy, parentId?: string, now = Date.now()) {
    if (policy) { validateAmounts(policy.allocation); if (policy.limits) { validateAmounts(policy.limits); } }
    const result = this.ledger.transaction(() => {
      const task = this.ledger.getTask(taskId);
      const old = this.ledger.db.prepare('SELECT * FROM task_resources WHERE task_id=?').get(taskId) as any;
      if (old) {
        check(!policy || old.allocation === stableJson(policy.allocation), 'budget_identity_conflict');
        const snap = this.snapshot(taskId);
        check(!parentId || this.snapshot(parentId).scopeId === snap.scopeId, 'budget_identity_conflict');
        check(!policy?.limits || stableJson(snap.limits) === stableJson(policy.limits), 'budget_identity_conflict');
        if (old.state === 'reserved' && ['planned','ready'].includes(task.state)
          && (now >= Math.min(snap.deadline, task.binding.deadline) || now >= old.reserved_at + JSON.parse(old.allocation).timeMs)) {
          this.ledger.db.prepare("UPDATE resource_scopes SET state='halted',reason='budget_time_exceeded' WHERE scope_id=?").run(snap.scopeId);
          return { error: 'budget_time_exceeded' };
        }
        return { scopeId: snap.scopeId, reused: true };
      }
      check(policy, 'budget_required');
      let scopeId = taskId;
      if (parentId) { scopeId = this.snapshot(parentId).scopeId; }
      else if (!this.ledger.db.prepare('SELECT scope_id FROM resource_scopes WHERE scope_id=?').get(scopeId)) {
        check(policy.limits, 'budget_required');
        this.ledger.db.prepare('INSERT INTO resource_scopes VALUES(?,?,?,?,?,?)')
          .run(scopeId, stableJson(policy.limits), task.binding.deadline, 'active', null, now);
      }
      const scope = this.snapshot(scopeId);
      check(scope.state === 'active', scope.reason ?? 'cancel_requested');
      check(!parentId || !policy.limits || stableJson(policy.limits) === stableJson(scope.limits), 'budget_identity_conflict');
      const deadline = Math.min(task.binding.deadline, scope.deadline);
      // 合计仍未确认的完整预留与已确认消费。输出/磁盘保守保留，修订轮数永不回退。
      const used: ResourceAmounts = { timeMs: 0, diskBytes: 0, outputBytes: 0, slots: 0, revisions: 0 };
      for (const record of scope.reservations) {
        const allocated = JSON.parse(record.allocation), consumed = record.consumed ? JSON.parse(record.consumed) : null;
        for (const field of fields) {
          used[field] += record.state === 'reserved' ? allocated[field]
            : field === 'slots' ? 0 : field === 'revisions' ? allocated[field] : consumed[field];
          check(Number.isSafeInteger(used[field]), 'ledger_resource_corrupt');
        }
      }
      let reason: string | null = deadline <= now || policy.allocation.timeMs > deadline - now ? 'budget_time_exceeded' : null;
      for (const field of fields) {
        if (!reason && policy.allocation[field] > scope.limits[field] - used[field]) { reason = errors[field]; }
      }
      // 同一文件系统上其它活动任务的磁盘预留也不能重复分配。
      const held = this.ledger.db.prepare("SELECT allocation FROM task_resources WHERE state='reserved'").all() as any[];
      const heldBytes = held.reduce((total, row) => total + JSON.parse(row.allocation).diskBytes, 0);
      if (!reason && this.freeBytes(task.binding.outputRoot) < heldBytes + policy.allocation.diskBytes) { reason = 'disk_space_insufficient'; }
      if (reason) {
        this.ledger.db.prepare('UPDATE resource_scopes SET reason=?,state=? WHERE scope_id=?')
          .run(reason, reason === 'budget_concurrency_exceeded' ? 'active' : 'halted', scopeId);
        return { error: reason };
      }
      this.ledger.db.prepare('INSERT INTO task_resources VALUES(?,?,?,?,?,?,?)')
        .run(taskId, scopeId, stableJson(policy.allocation), 'reserved', now, null, null);
      return { scopeId, reused: false };
    });
    if ('error' in result) { throw new HarnessError(result.error!); }
    return result;
  }
  /** 调度门禁可在 TaskLedger 自有事务中调用；旧无资源记录仅供原账本兼容读取。 */
  assertDispatch(taskId: string, now = Date.now()) {
    if (!this.ledger.db.prepare('SELECT task_id FROM task_resources WHERE task_id=?').get(taskId)) { return; }
    const snap = this.snapshot(taskId), record = snap.reservations.find(row => row.task_id === taskId)!;
    check(snap.state === 'active', snap.reason ?? 'cancel_requested');
    check(record.state === 'reserved' && snap.deadline > now
      && record.reserved_at + JSON.parse(record.allocation).timeMs > now, 'budget_time_exceeded');
  }
  halt(taskId: string, reason: string) {
    check(Object.values(errors).includes(reason) || ['disk_space_insufficient','output_measurement_unknown'].includes(reason), 'invalid_budget_reason');
    this.ledger.transaction(() => {
      const snap = this.snapshot(taskId);
      this.ledger.db.prepare("UPDATE resource_scopes SET state=CASE WHEN state='cancel_requested' THEN state ELSE 'halted' END,reason=? WHERE scope_id=?")
        .run(reason, snap.scopeId);
    });
  }
  observe(taskId: string, bytes: number, now = Date.now()) {
    check(Number.isSafeInteger(bytes) && bytes >= 0, 'output_measurement_unknown');
    const snap = this.snapshot(taskId), record = snap.reservations.find(row => row.task_id === taskId);
    check(record, 'budget_required'); const allocated = JSON.parse(record.allocation);
    const deadline = Math.min(snap.deadline, this.ledger.getTask(taskId).binding.deadline);
    const reason = now >= deadline || now - record.reserved_at >= allocated.timeMs ? 'budget_time_exceeded'
      : bytes > allocated.outputBytes ? 'budget_output_exceeded' : bytes > allocated.diskBytes ? 'budget_disk_exceeded' : null;
    if (reason) { this.halt(taskId, reason); } return reason;
  }
  settle(taskId: string, result: { stopped: boolean; outputBytes: number }, now = Date.now()) {
    check(result.stopped, 'native_stop_unconfirmed');
    check(Number.isSafeInteger(result.outputBytes) && result.outputBytes >= 0, 'output_measurement_unknown');
    this.ledger.transaction(() => {
      const task = this.ledger.getTask(taskId);
      check(['verifying','failed','cancelled','completed'].includes(task.state), 'native_stop_unconfirmed');
      const snap = this.snapshot(taskId), row = snap.reservations.find(item => item.task_id === taskId)!;
      if (row.state === 'settled') { return; }
      const allocation = JSON.parse(row.allocation);
      const consumed = { timeMs: Math.max(0, now - row.reserved_at), diskBytes: result.outputBytes,
        outputBytes: result.outputBytes, slots: 0, revisions: allocation.revisions };
      this.ledger.db.prepare("UPDATE task_resources SET state='settled',consumed=? WHERE task_id=?").run(stableJson(consumed), taskId);
      const reason = consumed.timeMs > allocation.timeMs ? 'budget_time_exceeded'
        : consumed.outputBytes > allocation.outputBytes ? 'budget_output_exceeded'
          : consumed.diskBytes > allocation.diskBytes ? 'budget_disk_exceeded' : null;
      if (reason && snap.state !== 'cancel_requested') {
        this.ledger.db.prepare("UPDATE resource_scopes SET state='halted',reason=? WHERE scope_id=?").run(reason, snap.scopeId);
      }
    });
  }
}
