import type { TaskLedger, Lease } from './task_ledger.ts';
import { ResourceController, outputBytes } from './resources.ts';
import { groupState, processIdentity, sameProcess } from './process_identity.ts';
import type { ProcessIdentity } from './process_identity.ts';
import { requireAuthorization } from './authorization.ts';
import type { Authorizer, AuthorizationRequest } from './authorization.ts';
import { check, sha256, stableJson } from '../support/json.ts';

/** 一个授权取消整个共享预算域；主题绑定不可变根任务、预算与截止时间。 */
export function cancellationSubject(ledger: TaskLedger, taskId: string) {
  const scope = new ResourceController(ledger).snapshot(taskId);
  return { action: 'cancel' as const, identitySha256: sha256(stableJson({ scopeId: scope.scopeId,
    limits: scope.limits, deadline: scope.deadline, root: ledger.getTask(scope.scopeId).binding })) };
}

/** 取消先记账，停止仅针对内核出生身份一致的本任务进程组；原生产物永不删除。 */
export class CancellationService {
  ledger: TaskLedger;
  authorize?: Authorizer;
  python?: string;
  constructor(ledger: TaskLedger, options: { authorize?: Authorizer; python?: string } = {}) {
    this.ledger = ledger; this.authorize = options.authorize; this.python = options.python;
  }
  bindProcess(lease: Lease, pid: number, stopSupported: boolean) {
    const identity = processIdentity(pid, this.python);
    if (!identity) { return false; }
    check(identity.ppid === process.pid && identity.pgid === pid
      && (process.getuid === undefined || identity.uid === process.getuid()), 'process_identity_unowned');
    this.ledger.transaction(() => {
      const task = this.ledger.getTask(lease.taskId), attempt = this.ledger.verifyAttempt(lease.taskId, lease.attemptId);
      check(task.epoch === lease.epoch && task.state === 'running' && task.attemptId === lease.attemptId
        && attempt.pid === pid && attempt.state === 'submitted', 'stale_epoch');
      const value = stableJson({ attemptId: lease.attemptId, epoch: lease.epoch, identity, stopSupported });
      const old = this.ledger.db.prepare('SELECT process_identity FROM task_resources WHERE task_id=?').get(lease.taskId);
      check(old && (old.process_identity === null || old.process_identity === value), 'process_identity_conflict');
      this.ledger.db.prepare('UPDATE task_resources SET process_identity=? WHERE task_id=?').run(value, lease.taskId);
    });
    return true;
  }
  request(taskId: string, request: AuthorizationRequest) {
    const resources = new ResourceController(this.ledger), scope = resources.snapshot(taskId);
    const subject = cancellationSubject(this.ledger, taskId), root = this.ledger.getTask(scope.scopeId);
    check(request.authorizationRef === root.binding.authorizationRef
      && request.authorizationScopeSha256 === root.binding.authorizationScopeSha256, 'authorization_required');
    requireAuthorization(this.authorize, request, subject);
    this.ledger.transaction(() => {
      requireAuthorization(this.authorize, request, subject);
      this.ledger.db.prepare("UPDATE resource_scopes SET state='cancel_requested',reason='cancel_requested' WHERE scope_id=?").run(scope.scopeId);
      for (const row of resources.snapshot(taskId).reservations) {
        const task = this.ledger.getTask(row.task_id);
        this.ledger.db.prepare('INSERT OR IGNORE INTO cancel_intents VALUES(?,?,?,?,?)')
          .run(task.taskId, scope.scopeId, stableJson(request), Date.now(), 'requested');
        if (['planned','ready','blocked'].includes(task.state) && task.attemptId === null) {
          this.ledger.db.prepare("UPDATE tasks SET state='cancelled',epoch=epoch+1 WHERE task_id=?").run(task.taskId);
          this.ledger.db.prepare("UPDATE cancel_intents SET diagnosis='not_started' WHERE task_id=?").run(task.taskId);
        } else if (['running','reconciling'].includes(task.state)) {
          // 撤销执行者提交权；仅取消服务在确认停止后可释放工程占用。
          this.ledger.db.prepare("UPDATE tasks SET state='cancel_requested',epoch=epoch+1,owner=NULL,lease_until=NULL WHERE task_id=?").run(task.taskId);
        }
      }
    });
    for (const row of resources.snapshot(taskId).reservations) {
      const task = this.ledger.getTask(row.task_id);
      if (task.state === 'cancelled') { resources.settle(task.taskId, { stopped: true, outputBytes: outputBytes(task.binding.outputRoot) }); }
    }
    return { scopeId: scope.scopeId, state: 'cancel_requested' };
  }
  reconcile(taskId: string, options: { signal?: boolean } = {}) {
    const task = this.ledger.getTask(taskId), resources = new ResourceController(this.ledger);
    const intent = this.ledger.db.prepare('SELECT * FROM cancel_intents WHERE task_id=?').get(taskId) as any;
    check(intent, 'cancel_request_missing');
    if (task.state === 'cancelled') {
      check(['stopped','not_started'].includes(intent.diagnosis), 'native_stop_unconfirmed');
      resources.settle(taskId, { stopped: true, outputBytes: outputBytes(task.binding.outputRoot) });
      return { taskId, state: 'cancelled', process: 'stopped', signalled: false };
    }
    check(task.state === 'cancel_requested', 'invalid_task_state');
    const reservation = resources.snapshot(taskId).reservations.find(row => row.task_id === taskId)!;
    const bound = reservation.process_identity ? JSON.parse(reservation.process_identity) as {
      attemptId: string; epoch: number; identity: ProcessIdentity; stopSupported: boolean } : null;
    let status: 'running' | 'stopped' | 'unknown' = 'unknown', signalled = false;
    if (bound && bound.attemptId === task.attemptId) {
      const attempt = this.ledger.verifyAttempt(taskId, bound.attemptId);
      check(attempt.pid === bound.identity.pid && attempt.epoch === bound.epoch
        && Number.isSafeInteger(bound.identity.pid) && bound.identity.pid > 0 && bound.identity.pgid === bound.identity.pid
        && (process.getuid === undefined || bound.identity.uid === process.getuid()), 'process_identity_conflict');
      status = groupState(bound.identity.pgid);
      if (status !== 'stopped') {
        const current = processIdentity(bound.identity.pid, this.python);
        if (!sameProcess(bound.identity, current)) { status = 'unknown'; }
        else if (options.signal && bound.stopSupported) {
          requireAuthorization(this.authorize, JSON.parse(intent.request), cancellationSubject(this.ledger, taskId));
          // 不升级到 SIGKILL；身份不可读、权限不足、回复丢失均保留未确认状态。
          if (sameProcess(bound.identity, processIdentity(bound.identity.pid, this.python))) {
            try { process.kill(-bound.identity.pgid, 'SIGTERM'); signalled = true; }
            catch { /* 下一次观察确认；发送失败本身不证明已终止。 */ }
          }
          status = groupState(bound.identity.pgid);
        }
      }
    }
    this.ledger.transaction(() => {
      const current = this.ledger.getTask(taskId);
      check(current.epoch === task.epoch && current.attemptId === task.attemptId && current.state === 'cancel_requested', 'stale_epoch');
      this.ledger.db.prepare('UPDATE cancel_intents SET diagnosis=? WHERE task_id=?').run(status, taskId);
      if (status === 'stopped') {
        this.ledger.db.prepare("UPDATE tasks SET state='cancelled' WHERE task_id=?").run(taskId);
        this.ledger.db.prepare("UPDATE attempts SET state='failed' WHERE attempt_id=?").run(task.attemptId);
        this.ledger.db.prepare('DELETE FROM project_leases WHERE task_id=?').run(taskId);
      }
    });
    if (status === 'stopped') { resources.settle(taskId, { stopped: true, outputBytes: outputBytes(task.binding.outputRoot) }); }
    return { taskId, state: this.ledger.getTask(taskId).state, process: status, signalled };
  }
}
