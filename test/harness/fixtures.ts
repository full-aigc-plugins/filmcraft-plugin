import { appendFileSync } from 'node:fs';
import { sha256, stableJson } from '../../src/support/json.ts';
import { mkdtempSync, realpathSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

export const hash = (letter = 'a') => letter.repeat(64);
export function workspace(t: { after: (fn: () => void) => void }) {
  const root = realpathSync(mkdtempSync(join(tmpdir(), 'filmcraft-harness-')));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  return root;
}
export function binding(root: string, extra = {}) {
  return {
    taskId: 'task-1', namespace: 'local-host', idempotencyKey: 'request-1',
    planHash: hash(), nativePlanHash: hash('b'), inputHashes: {}, inputRefs: [],
    projectRevision: null, projectKey: hash('c'), outputRoot: join(root, 'delivery'),
    sourceRevision: 'd'.repeat(40), sourceTreeSha256: hash('e'),
    runtimeIdentity: { pluginId: 'filmcraft', pluginVersion: '0.1.0-dev.41',
      cliVersion: '0.2.0-craft.4', sha256: hash('f'), mode: 'headless', capabilitySnapshotSha256: hash('a') },
    authorizationRef: 'grant-1', authorizationScopeSha256: hash('b'),
    deadline: Date.now() + 3600_000, ...extra,
  };
}

/** 仅供合成测试的可信宿主授权；实际使用 LocalAuthorizationStore 或宿主自己的查询器。 */
export function fixtureAuthorizer(subject: any, request: any) {
  return { ...request, expiresAt: Date.now() + 60_000, subjectSha256: sha256(stableJson(subject)) };
}

/** 私有逐场景取证；无配置时不写文件，不替代行为断言。 */
export function captureEvidence(scenario: string, layer: string, data: Record<string, unknown>) {
  const file = process.env.FILMCRAFT_RECOVERY_EVIDENCE;
  if (file) { appendFileSync(file, JSON.stringify({ scenario, layer, ...data }) + '\n', { mode: 0o600 }); }
}

/** 合成清单夹具的损失报告；仅测试身份门禁，不证明真实媒体或原生重开。 */
export function syntheticExchangeLoss(files: Record<string, Buffer | string>) {
  return { schema: 'craft-exchange-loss/v1', pluginId: 'filmcraft',
    native: { location: 'project.fcproj', sha256: sha256(files['project.fcproj']) },
    inspection: { location: 'native.json', sha256: sha256(files['native.json']) },
    outputs: files['film.mp4'] ? [{ location: 'film.mp4', sha256: sha256(files['film.mp4']), format: 'mp4', role: 'derivative', nativeSubstitute: false,
      changes: ['native-editing-model', 'editable-layers-paths-text', 'effect-keyframe-parameters', 'alpha-channel', 'editable-timeline'].map(code =>
        ({ code, status: 'lost', reason: 'synthetic format-loss fixture' })).concat([{ code: 'font-appearance', status: 'unknown', reason: 'not compared' }]),
      observations: {}, warnings: [] }] : [], acceptance: 'technical-observations-only' };
}
