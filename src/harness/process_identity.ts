import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { check, parseJson, stableJson } from '../support/json.ts';

export type ProcessIdentity = { pid: number; ppid: number; pgid: number; uid: number; started: string; boot: string; executable: string };
/** 内核出生时间与启动身份代替 PID 猜测；读不到身份时不提供停止能力。 */
export function processIdentity(pid: number, python = process.env.FILMCRAFT_PYTHON ?? 'python3'): ProcessIdentity | null {
  check(Number.isSafeInteger(pid) && pid > 0, 'invalid_process_identity');
  const script = fileURLToPath(new URL('../../scripts/process_identity.py', import.meta.url));
  const result = spawnSync(python, ['-I', '-B', script, String(pid)], { encoding: 'utf8', timeout: 5000, maxBuffer: 32 * 1024, shell: false });
  if (result.error || result.status !== 0) { return null; }
  try {
    const value = parseJson(result.stdout);
    check(value.pid === pid && [value.ppid,value.pgid,value.uid].every(Number.isSafeInteger)
      && typeof value.started === 'string' && typeof value.boot === 'string' && typeof value.executable === 'string', 'invalid_process_identity');
    return value;
  } catch { return null; }
}
export function sameProcess(a: ProcessIdentity, b: ProcessIdentity | null) {
  // 父进程退出后的 reparent 不改变出生身份。
  if (!b) { return false; }
  const { ppid: ignoredA, ...first } = a, { ppid: ignoredB, ...second } = b;
  return stableJson(first) === stableJson(second);
}
export function groupState(pgid: number): 'running' | 'stopped' | 'unknown' {
  try { process.kill(-pgid, 0); return 'running'; }
  catch (error: any) { return error.code === 'ESRCH' ? 'stopped' : 'unknown'; }
}
