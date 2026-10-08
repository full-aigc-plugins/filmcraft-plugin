import { randomUUID } from 'node:crypto';
import { dirname } from 'node:path';
import { TaskLedger } from './task_ledger.ts';
import { forensicSnapshot } from './forensic_snapshot.ts';
import { ReceiptIndex, readBoundFile } from '../artifacts/receipt_index.ts';
import { check, HarnessError, parseJson, sha256, stableJson } from '../support/json.ts';

type ProcessObservation = { status: 'alive' | 'stopped' | 'unknown'; pid: number | null };
export type Inspection = {
  schema: string; taskId: string; observedAt: string; diagnosis: 'executed' | 'running' | 'failed' | 'unknown';
  task: { state: string; epoch: number; attemptId: string | null } | null;
  process: ProcessObservation; bindingSha256: string | null; contentSha256: string | null;
  evidenceSha256: string; receipts: { delivery: string | null; execution: string | null };
  replayAllowed: false; error: { code: string } | null;
};
export type RepairRequest = { expectedEpoch: number; inspectionSha256: string; authorizationRef: string; authorizationScopeSha256: string };
function processState(pid: unknown): ProcessObservation {
  if (!Number.isSafeInteger(pid) || (pid as number) <= 0 || globalThis.process.platform === 'win32') { return { status: 'unknown', pid: null }; }
  try { globalThis.process.kill(-(pid as number), 0); return { status: 'alive', pid: pid as number }; }
  catch (error: any) { return { status: error.code === 'ESRCH' ? 'stopped' : 'unknown', pid: pid as number }; }
}

/** 只读 inspect 与有副作用 repair 分离；修复原执行的状态，不重放原生命令。 */
export class RecoveryService {
  file: string;
  blobs: string;
  constructor(file: string, blobs: string) { this.file = file; this.blobs = blobs; }
  inspect(taskId: string): Inspection {
    const base = { schema: 'filmcraft-inspection/v1', taskId, task: null, process: { status: 'unknown', pid: null },
      bindingSha256: null, contentSha256: null, receipts: { delivery: null, execution: null }, replayAllowed: false };
    let core: any;
    try {
      core = forensicSnapshot(this.file, (db, ledgerIdentity) => {
        const task = db.getTask(taskId), attempt = task.attemptId ? db.verifyAttempt(taskId, task.attemptId) : null;
        const process = processState(attempt?.pid);
        const result = { ...base, ledgerIdentity, task: { state: task.state, epoch: task.epoch, attemptId: task.attemptId },
          process, bindingSha256: sha256(stableJson(task.binding)), diagnosis: 'unknown', error: null } as any;
        if (process.status === 'alive') { result.diagnosis = 'running'; return result; }
        if (!attempt || process.status !== 'stopped') { result.error = { code: 'process_identity_unknown' }; return result; }
        const index = new ReceiptIndex(db, this.blobs, { readOnly: true });
        try {
          const delivery = index.inspect(taskId, task.attemptId!, 'delivery', 'manifest.json');
          const name = '.filmcraft-execution-' + sha256(task.binding.outputRoot) + '.json';
          const execution = index.inspect(taskId, task.attemptId!, 'output-execution', name);
          const raw = parseJson(readBoundFile(dirname(task.binding.outputRoot), name).toString('utf8'));
          check(raw.ownerPid === attempt.pid, 'process_identity_conflict');
          check(delivery.status === 'linked' && execution.status === 'linked', 'recovery_evidence_unknown');
          const existing = db.receipts(taskId, task.attemptId!);
          if (existing.length) { check(index.collect(taskId, task.attemptId!).status === 'linked', 'recovery_evidence_stale'); }
          result.receipts = { delivery: delivery.sha256, execution: execution.sha256 };
          result.contentSha256 = sha256(stableJson({ bindingSha256: result.bindingSha256, attemptId: task.attemptId,
            process, delivery: delivery.sha256, execution: execution.sha256, files: delivery.summary.files }));
          result.diagnosis = 'executed';
        } catch (error: any) {
          result.error = { code: error instanceof HarnessError ? error.code : 'recovery_evidence_missing' };
          if (task.state === 'failed' && attempt.state === 'failed') { result.diagnosis = 'failed'; }
        }
        return result;
      });
    } catch (error: any) { core = { ...base, diagnosis: 'unknown', error: { code: error instanceof HarnessError ? error.code : 'ledger_unreadable' } }; }
    return { ...core, observedAt: new Date().toISOString(), evidenceSha256: sha256(stableJson(core)) };
  }
  repair(taskId: string, request: RepairRequest) {
    const before = this.inspect(taskId);
    check(before.evidenceSha256 === request.inspectionSha256, 'inspection_stale');
    check(before.task?.epoch === request.expectedEpoch, 'stale_epoch');
    check(before.diagnosis === 'executed' && before.process.status === 'stopped', 'outcome_unknown');
    const reused = forensicSnapshot(this.file, db => {
      const task = db.getTask(taskId), binding = task.binding;
      check(task.epoch === request.expectedEpoch && sha256(stableJson(binding)) === before.bindingSha256, 'stale_epoch');
      check(request.authorizationRef === binding.authorizationRef && request.authorizationScopeSha256 === binding.authorizationScopeSha256, 'authorization_required');
      if (task.state === 'verifying') {
        const index = new ReceiptIndex(db, this.blobs, { readOnly: true }), receipt = index.collect(taskId, task.attemptId!);
        check(receipt.status === 'linked', 'recovery_evidence_stale');
        const intents = db.listRecoveryIntents(taskId);
        return { taskId, attemptId: task.attemptId!, state: task.state, replayed: false, reused: true,
          recoveryId: intents.at(-1)?.intent_id ?? null, receipt };
      }
      return null;
    });
    if (reused) { return reused; }
    const db = new TaskLedger(this.file);
    let lease;
    try {
      const binding = db.getTask(taskId).binding;
      check(request.authorizationRef === binding.authorizationRef && request.authorizationScopeSha256 === binding.authorizationScopeSha256, 'authorization_required');
      lease = db.beginRecovery(taskId, request.expectedEpoch, before.evidenceSha256, randomUUID());
      const current = this.inspect(taskId);
      check(current.diagnosis === 'executed' && current.contentSha256 === before.contentSha256, 'recovery_evidence_stale');
      const index = new ReceiptIndex(db, this.blobs);
      const delivery = index.ingest(taskId, lease.attemptId, 'delivery', 'manifest.json');
      const execution = index.ingest(taskId, lease.attemptId, 'output-execution', '.filmcraft-execution-' + sha256(binding.outputRoot) + '.json');
      check(delivery.status === 'linked' && execution.status === 'linked'
        && delivery.sha256 === current.receipts.delivery && execution.sha256 === current.receipts.execution, 'recovery_evidence_stale');
      const final = this.inspect(taskId);
      check(final.diagnosis === 'executed' && final.contentSha256 === before.contentSha256, 'recovery_evidence_stale');
      db.finishRecovery(lease, final.evidenceSha256, delivery.sha256, execution.sha256);
      return { taskId, attemptId: lease.attemptId, state: db.getTask(taskId).state, replayed: false, reused: false, recoveryId: lease.recoveryId,
        receipt: index.collect(taskId, lease.attemptId) };
    } catch (error) {
      if (lease) { try { db.abandonRecovery(lease, error instanceof HarnessError ? error.code : 'recovery_failed'); } catch {} }
      throw error;
    } finally { db.close(); }
  }
}
