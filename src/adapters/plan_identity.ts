import { childEnvironment } from '../support/process_environment.ts';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { check, parseJson, isHash } from '../support/json.ts';

/** 与既有 Python 网关共享摘要算法，不在 JavaScript 中舍入原生整数。 */
export function normalizePlan(path: string, python = process.env.FILMCRAFT_PYTHON ?? 'python3') {
  const helper = fileURLToPath(new URL('../../scripts/plan_identity.py', import.meta.url));
  const result = spawnSync(python, ['-I', '-B', helper, path], { encoding: 'utf8', timeout: 10_000, maxBuffer: 64 * 1024, shell: false, env: childEnvironment() });
  check(!result.error && result.status === 0, 'invalid_plan', result.stdout?.trim());
  const identity = parseJson(result.stdout);
  for (const key of ['fileSha256', 'commandPlanSha256', 'workflowPlanSha256', 'canonicalPlanSha256']) {
    check(isHash(identity[key]), 'invalid_plan_identity');
  }
  return identity as { fileSha256: string; commandPlanSha256: string; workflowPlanSha256: string; canonicalPlanSha256: string };
}
