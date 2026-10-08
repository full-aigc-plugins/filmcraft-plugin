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
