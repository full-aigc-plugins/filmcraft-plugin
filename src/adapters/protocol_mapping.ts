import type { TaskLedger } from '../harness/task_ledger.ts';
import { check, isObject, stableJson } from '../support/json.ts';

/** 公共预算的消费类型；限额由未来的宿主/预算控制器执行，本映射不授予权限。 */
export type PublicBudget = { currency: string; maxMinorUnits: number | null; maxRevisions: number | null; maxExternalCalls: number | null };

/** 将已登记领域身份映射到 ArtCraft 固定任务字段；不提供公共提交或授权接口。 */
export function publicTask(ledger: TaskLedger, taskId: string, payload: Record<string, unknown>, budget: PublicBudget) {
  const binding = ledger.getTask(taskId).binding;
  check(isObject(payload) && typeof payload.schemaVersion === 'string' && payload.schemaVersion.length > 0, 'payload_version_required');
  check(isObject(budget) && /^[A-Z]{3}$/.test(budget.currency), 'invalid_budget_mapping');
  for (const key of ['maxMinorUnits', 'maxRevisions', 'maxExternalCalls'] as const) {
    check(budget[key] === null || Number.isSafeInteger(budget[key]) && budget[key]! >= 0, 'invalid_budget_mapping');
  }
  const deadline = new Date(binding.deadline);
  check(Number.isFinite(deadline.getTime()), 'invalid_deadline');
  return { protocolVersion: 'craft-task/v1', taskId: binding.taskId, idempotencyKey: binding.idempotencyKey,
    planHash: binding.planHash, inputRefs: binding.inputRefs.map(ref => ({ ...ref })), expectedRevision: binding.projectRevision,
    runtimeIdentity: { ...binding.runtimeIdentity }, authorizationRef: binding.authorizationRef,
    budget: { currency: budget.currency, maxMinorUnits: budget.maxMinorUnits, maxRevisions: budget.maxRevisions, maxExternalCalls: budget.maxExternalCalls },
    deadline: deadline.toISOString(), payload: JSON.parse(stableJson(payload)) };
}
