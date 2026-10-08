import type { Binding } from './task_ledger.ts';
import { TaskLedger } from './task_ledger.ts';
import type { Authorizer, AuthorizationSubject } from './authorization.ts';
import { requireAuthorization } from './authorization.ts';
import { ReceiptIndex } from '../artifacts/receipt_index.ts';
import type { ResourcePolicy } from './resources.ts';
import type { WorkflowOptions } from '../adapters/python_workflow.ts';
import { PythonWorkflowRunner } from '../adapters/python_workflow.ts';
import { canonicalTarget } from '../support/paths.ts';
import { parseJson, sha256, stableJson } from '../support/json.ts';

/** 首次宿主执行主体：绑定完整任务，而非仅验证可复制的授权引用。 */
export function executionSubject(binding: Binding, resources?: ResourcePolicy): AuthorizationSubject {
  return { action: 'execute', identitySha256: sha256(stableJson({ ...binding,
    outputRoot: canonicalTarget(binding.outputRoot), executionResources: resources ?? null })) };
}

/** 宿主首次执行准入；可信查询器来自宿主，不能来自计划或素材元数据。 */
export class WorkflowAdmission {
  private ledger: TaskLedger;
  private index: ReceiptIndex;
  private options: WorkflowOptions;
  private authorize?: Authorizer;
  constructor(ledger: TaskLedger, index: ReceiptIndex, options: WorkflowOptions, authorize?: Authorizer) {
    this.ledger = ledger; this.index = index; this.options = options; this.authorize = authorize;
  }

  /** 使用当前授权提交已绑定计划；门禁失败不启动原生编辑，不自动扩大授权。 */
  async run(binding: Binding, planFile: string, source?: string) {
    // 持有独立快照，防止调用方在授权查询中修改已批准的任务对象。
    const current: Binding = parseJson(stableJson({ ...binding, outputRoot: canonicalTarget(binding.outputRoot) }));
    const options = { ...this.options, resources: this.options.resources
      ? parseJson(stableJson(this.options.resources)) : undefined };
    const subject = Object.freeze(executionSubject(current, options.resources));
    const request = Object.freeze({ authorizationRef: current.authorizationRef,
      authorizationScopeSha256: current.authorizationScopeSha256 });
    const permitted = () => requireAuthorization(this.authorize, request, subject);
    permitted();
    const runner = new PythonWorkflowRunner(this.ledger, this.index, { ...options, beforeDispatch: () => {
      permitted();
      options.beforeDispatch?.();
      permitted();
    } });
    return runner.run(current, planFile, source);
  }
}
