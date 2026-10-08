import { RecoveryService } from './recovery.ts';
import type { RepairRequest } from './recovery.ts';
import { forensicSnapshot } from './forensic_snapshot.ts';
import { TaskLedger } from './task_ledger.ts';
import type { Binding } from './task_ledger.ts';
import { requireAuthorization } from './authorization.ts';
import type { Authorizer } from './authorization.ts';
import { PythonWorkflowRunner } from '../adapters/python_workflow.ts';
import type { WorkflowOptions } from '../adapters/python_workflow.ts';
import { ReceiptIndex, readBoundFile } from '../artifacts/receipt_index.ts';
import { normalizePlan } from '../adapters/plan_identity.ts';
import { canonicalTarget } from '../support/paths.ts';
import { check, sha256, stableJson } from '../support/json.ts';

/** 宿主可用当前诊断与计划构建授权主题；计算摘要本身不授予权限。 */
export function continuationSubject(parentId: string, parentAttemptId: string | null,
  parentContentSha256: string | null, child: Binding, planFileSha256: string) {
  return { action: 'continue' as const, identitySha256: sha256(stableJson({ parentId, parentAttemptId,
    parentContentSha256, child, planFileSha256 })) };
}

/** 明确的剩余计划以新任务继续；原未知尝试绝不重放，状态修复必须先独立完成。 */
export class ContinuationService {
  file: string;
  blobs: string;
  authorize?: Authorizer;
  constructor(file: string, blobs: string, options: { authorize?: Authorizer } = {}) {
    this.file = file; this.blobs = blobs; this.authorize = options.authorize;
  }
  async continue(parentId: string, request: RepairRequest, child: Binding, planFile: string, options: WorkflowOptions) {
    const recovery = new RecoveryService(this.file, this.blobs), before = recovery.inspect(parentId);
    check(before.evidenceSha256 === request.inspectionSha256, 'inspection_stale');
    check(before.task?.epoch === request.expectedEpoch, 'stale_epoch');
    check(before.diagnosis === 'executed' && before.process.status === 'stopped'
      && before.task.state === 'verifying', 'continuation_source_unconfirmed');
    const parent = forensicSnapshot(this.file, db => db.getTask(parentId));
    check(parent.binding.authorizationRef === request.authorizationRef
      && parent.binding.authorizationScopeSha256 === request.authorizationScopeSha256, 'authorization_required');
    child = { ...child, outputRoot: canonicalTarget(child.outputRoot) };
    const projectHash = sha256(readBoundFile(parent.binding.outputRoot, 'project.fcproj', 512 * 1024 * 1024));
    check(child.taskId !== parentId && child.outputRoot !== parent.binding.outputRoot
      && child.projectRevision === projectHash, 'invalid_continuation');
    const identity = normalizePlan(planFile, options.python);
    check(identity.canonicalPlanSha256 === child.planHash && identity.workflowPlanSha256 === child.nativePlanHash, 'plan_identity_conflict');
    const subject = continuationSubject(parentId, parent.attemptId, before.contentSha256, child, identity.fileSha256);
    const permitted = () => requireAuthorization(this.authorize, child, subject);
    permitted();
    const db = new TaskLedger(this.file);
    try {
      const current = recovery.inspect(parentId);
      check(current.evidenceSha256 === before.evidenceSha256, 'inspection_stale');
      const intent = db.beginContinuation(parentId, request.expectedEpoch, before.evidenceSha256, child);
      const runner = new PythonWorkflowRunner(db, new ReceiptIndex(db, this.blobs), { ...options, beforeDispatch: permitted });
      const result = await runner.run(child, planFile, parent.binding.outputRoot);
      const audit = db.observeContinuation(intent.intentId);
      return { parentTaskId: parentId, parentAttemptId: parent.attemptId, originalReplayed: false,
        intentId: intent.intentId, intentReused: intent.reused, continuation: audit, task: result,
        technicalAcceptance: 'NOT_RUN', creativeAcceptance: 'NOT_RUN', userAcceptance: 'NOT_RUN' };
    } finally { db.close(); }
  }
}
