import { spawn, spawnSync } from 'node:child_process';
import { createHash, randomUUID } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync, realpathSync } from 'node:fs';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { Binding } from '../harness/task_ledger.ts';
import { TaskLedger } from '../harness/task_ledger.ts';
import { ReceiptIndex, readBoundFile } from '../artifacts/receipt_index.ts';
import { normalizePlan } from './plan_identity.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';
import { canonicalTarget } from '../support/paths.ts';

/** 自包含技能内容身份；不使用工作目录、mtime 或可变分支作为替代。 */
export function fingerprintSkill(directory: string) {
  const root = realpathSync(directory), files: string[] = [];
  function walk(path: string) {
    for (const name of readdirSync(path).sort()) {
      if (name === '__pycache__') { continue; }
      const file = join(path, name), info = lstatSync(file);
      check(!info.isSymbolicLink(), 'skill_link_rejected');
      if (info.isDirectory()) { walk(file); }
      else { check(info.isFile(), 'invalid_skill_file'); files.push(file); }
    }
  }
  walk(root); const digest = createHash('sha256');
  for (const file of files.sort()) { digest.update(relative(root, file).split(sep).join('/') + '\0'); digest.update(readFileSync(file)); digest.update('\0'); }
  return digest.digest('hex');
}
function stopped(pid: number) {
  try { process.kill(-pid, 0); return false; }
  catch (error: any) { return error.code === 'ESRCH'; }
}
export type WorkflowOptions = { python?: string; skillDirectory: string; sourceRevision: string; runtimeHome: string; pluginVersion: string };

/** 内部领域执行适配；宿主先验证授权范围。本适配不重试、不承担预算或用户接受。 */
export class PythonWorkflowRunner {
  ledger: TaskLedger;
  index: ReceiptIndex;
  options: WorkflowOptions;
  constructor(ledger: TaskLedger, index: ReceiptIndex, options: WorkflowOptions) {
    this.ledger = ledger; this.index = index; this.options = options;
  }
  prepare(planFile: string, outputRoot: string, source?: string) {
    check(process.platform !== 'win32', 'unsupported_runner_platform');
    check(/^[a-f0-9]{40}$/.test(this.options.sourceRevision), 'invalid_source_revision');
    const root = resolve(this.options.skillDirectory);
    check(!lstatSync(root).isSymbolicLink() && existsSync(join(root, 'scripts/capabilities.py')), 'capability_adapter_missing');
    const planIdentity = normalizePlan(planFile, this.options.python);
    const sourceTreeSha256 = fingerprintSkill(root);
    const script = fileURLToPath(new URL('../../scripts/native_preflight.py', import.meta.url));
    outputRoot = canonicalTarget(outputRoot);
    if (source) { source = realpathSync(source); }
    const projectKey = sha256(source ? join(realpathSync(source), 'project.fcproj') : outputRoot);
    const argv = ['-I', '-B', script, '--skill-dir', root, '--plan', resolve(planFile), '--output', outputRoot, '--runtime-home', resolve(this.options.runtimeHome)];
    if (source) { argv.push('--source', resolve(source)); }
    const result = spawnSync(this.options.python ?? process.env.FILMCRAFT_PYTHON ?? 'python3', argv,
      { encoding: 'utf8', timeout: 180_000, maxBuffer: 4 * 1024 * 1024, shell: false });
    check(!result.error && result.status === 0, 'native_preflight_failed', result.stderr.trim().slice(-2048));
    const preflight = parseJson(result.stdout);
    check(preflight.schema === 'filmcraft-native-preflight/v1' && isObject(preflight.inputHashes)
      && Object.values(preflight.inputHashes).every(isHash)
      && (preflight.projectRevision === null || isHash(preflight.projectRevision)), 'invalid_native_preflight');
    const snapshot = preflight.capabilitySnapshot;
    check(snapshot.schema === 'filmcraft-capability-snapshot/v1' && snapshot.mode === 'headless'
      && isHash(snapshot.runtime?.binarySha256), 'invalid_capability_snapshot');
    check(fingerprintSkill(root) === sourceTreeSha256, 'source_changed');
    return { planIdentity, snapshot, sourceTreeSha256, outputRoot, projectKey,
      inputHashes: preflight.inputHashes, projectRevision: preflight.projectRevision,
      runtimeIdentity: { pluginId: 'filmcraft', pluginVersion: this.options.pluginVersion,
        cliVersion: snapshot.runtime.version, sha256: snapshot.runtime.binarySha256,
        mode: 'headless', capabilitySnapshotSha256: sha256(stableJson(snapshot)) } };
  }
  async run(binding: Binding, planFile: string, source?: string) {
    binding = { ...binding, outputRoot: canonicalTarget(binding.outputRoot) };
    if (source) { source = realpathSync(source); }
    const prepared = this.prepare(planFile, binding.outputRoot, source);
    check(prepared.projectKey === binding.projectKey, 'project_identity_conflict');
    check(stableJson(prepared.inputHashes) === stableJson(binding.inputHashes), 'input_identity_conflict');
    check(prepared.projectRevision === binding.projectRevision, 'revision_conflict');
    check(prepared.planIdentity.canonicalPlanSha256 === binding.planHash
      && prepared.planIdentity.workflowPlanSha256 === binding.nativePlanHash, 'plan_identity_conflict');
    check(prepared.sourceTreeSha256 === binding.sourceTreeSha256
      && this.options.sourceRevision === binding.sourceRevision, 'source_identity_conflict');
    check(stableJson(prepared.runtimeIdentity) === stableJson(binding.runtimeIdentity), 'runtime_identity_conflict');
    const registered = this.ledger.register(binding);
    // 同一幂等身份已运行过时只返回原任务，不启动第二次 Python 原生执行。
    if (registered.state !== 'planned' && registered.state !== 'ready') {
      return { taskId: registered.taskId, state: registered.state, reused: true,
        attemptId: registered.attemptId, receipt: registered.attemptId ? this.index.collect(registered.taskId, registered.attemptId) : null };
    }
    const lease = this.ledger.claim(registered.taskId, randomUUID(), Math.min(3600_000, Math.max(1, binding.deadline - Date.now())));
    let launched = false;
    try {
      if (source) {
        check(isHash(binding.projectRevision)
          && sha256(readBoundFile(source, 'project.fcproj', 512 * 1024 * 1024)) === binding.projectRevision, 'revision_conflict');
      } else { check(binding.projectRevision === null, 'revision_conflict'); }
      check(normalizePlan(planFile, this.options.python).fileSha256 === prepared.planIdentity.fileSha256, 'plan_changed');
      check(fingerprintSkill(this.options.skillDirectory) === binding.sourceTreeSha256, 'source_changed');
      const attempt = this.ledger.beginAttempt(lease, 'workflow:' + binding.nativePlanHash);
      check(attempt.fresh, 'outcome_unknown');
      const argv = ['-I', '-B', join(resolve(this.options.skillDirectory), 'scripts/workflow.py'), resolve(planFile),
        '--output', binding.outputRoot, '--runtime-home', resolve(this.options.runtimeHome)];
      if (source) { argv.push('--source', resolve(source)); }
      const child = spawn(this.options.python ?? process.env.FILMCRAFT_PYTHON ?? 'python3', argv,
        { shell: false, detached: true, stdio: ['ignore', 'pipe', 'pipe'],
          env: { ...process.env, FILMCRAFT_EXECUTION_CONTEXT: JSON.stringify({ taskId: registered.taskId,
            attemptId: lease.attemptId, sourceRevision: binding.sourceRevision, sourceTreeSha256: binding.sourceTreeSha256 }) } });
      launched = true;
      let log = '', spawnError: Error | null = null;
      child.stdout.on('data', chunk => { if (log.length < 128 * 1024) { log += chunk; } });
      child.stderr.on('data', chunk => { if (log.length < 128 * 1024) { log += chunk; } });
      const ending = new Promise<{ code: number | null; signal: string | null }>(resolveExit => {
        child.on('error', error => { spawnError = error; });
        child.on('close', (code, signal) => resolveExit({ code, signal }));
      });
      if (child.pid) { this.ledger.markSubmitted(lease, child.pid); }
      const end = await ending;
      const stoppedConfirmed = child.pid ? stopped(child.pid) : spawnError !== null;
      let outcome: 'succeeded' | 'failed' | 'unknown' = 'unknown', receiptSha256: string | null = null;
      if (end.code === 0 && stoppedConfirmed) {
        const delivery = this.index.ingest(registered.taskId, lease.attemptId, 'delivery', 'manifest.json');
        receiptSha256 = delivery.sha256;
        const guard = '.filmcraft-execution-' + sha256(binding.outputRoot) + '.json';
        const execution = this.index.ingest(registered.taskId, lease.attemptId, 'output-execution', guard);
        outcome = delivery.status === 'linked' && execution.status === 'linked' ? 'succeeded' : 'unknown';
      } else if (existsSync(join(binding.outputRoot, 'failure.json'))) {
        const failure = this.index.ingest(registered.taskId, lease.attemptId, 'failed-stage', 'failure.json');
        receiptSha256 = failure.sha256;
        const raw = parseJson(readBoundFile(binding.outputRoot, 'failure.json').toString('utf8'));
        outcome = raw.outcome === 'failed' && stoppedConfirmed ? 'failed' : 'unknown';
      } else if (spawnError && !child.pid) { outcome = 'failed'; }
      this.ledger.finishAttempt(lease, { outcome, stopped: stoppedConfirmed, receiptSha256 });
      return { taskId: registered.taskId, attemptId: lease.attemptId, state: this.ledger.getTask(registered.taskId).state,
        reused: false, process: { pid: child.pid ?? null, stopped: stoppedConfirmed, exitCode: end.code, signal: end.signal },
        receipt: this.index.collect(registered.taskId, lease.attemptId) };
    } catch (error) {
      // 未发出进程前的冲突是已知拒绝；发出后的任何异常不能自动重放。
      if (!launched) {
        const attempts = this.ledger.listAttempts(registered.taskId);
        if (!attempts.some(item => item.attempt_id === lease.attemptId)) { this.ledger.beginAttempt(lease, 'workflow:' + binding.nativePlanHash); }
      }
      try { this.ledger.finishAttempt(lease, { outcome: launched ? 'unknown' : 'failed', stopped: !launched, receiptSha256: null }); }
      catch { /* 原 epoch/占用保留；不能用状态写入异常遮蔽原始错误。 */ }
      throw error;
    }
  }
}
