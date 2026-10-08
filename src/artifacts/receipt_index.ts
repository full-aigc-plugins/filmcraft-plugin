import { constants, openSync, closeSync, existsSync, fstatSync, lstatSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import type { TaskLedger, Binding } from '../harness/task_ledger.ts';
import { exchangeLossStatus } from './exchange_loss.ts';
import { normalizePlan } from '../adapters/plan_identity.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';

export type ReceiptKind = 'command' | 'delivery' | 'failed-stage' | 'output-execution';
type Status = 'linked' | 'unknown' | 'conflict' | 'stale';
type Observation = { status: Status; sha256: string; kind: ReceiptKind; summary: Record<string, any>; bytes: Buffer };

/** 读取受控根中的普通文件；拒绝路径与链接逃逸，摘要始终覆盖原字节。 */
export function readBoundFile(root: string, name: string, limit = 16 * 1024 * 1024): Buffer {
  check(typeof name === 'string' && name.length > 0 && !isAbsolute(name) && !name.includes('\\')
    && name.split('/').every(part => part !== '' && part !== '.' && part !== '..'), 'unsafe_receipt_path');
  const base = resolve(root);
  check(!lstatSync(base).isSymbolicLink() && lstatSync(base).isDirectory(), 'unsafe_receipt_path');
  let current = base;
  for (const part of name.split('/')) {
    current = join(current, part); check(!lstatSync(current).isSymbolicLink(), 'unsafe_receipt_path');
  }
  const canonical = realpathSync(current), bound = realpathSync(base), rel = relative(bound, canonical);
  check(rel !== '..' && !rel.startsWith('..' + sep) && !isAbsolute(rel), 'unsafe_receipt_path');
  const fd = openSync(current, constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    const before = fstatSync(fd);
    check(before.isFile() && before.size <= limit, 'invalid_receipt_file');
    const bytes = readFileSync(fd), after = fstatSync(fd);
    check(before.dev === after.dev && before.ino === after.ino && before.size === bytes.length
      && before.size === after.size && before.mtimeMs === after.mtimeMs && before.ctimeMs === after.ctimeMs, 'receipt_changed');
    return bytes;
  } finally { closeSync(fd); }
}
function refs(binding: Binding) { return binding.inputRefs.map(ref => ({ ...ref })); }
function assetId(taskId: string, path: string) { return 'filmcraft:' + sha256(taskId + '\0' + path); }

/** 显式旧格式映射与原字节内容寻址；关联不拥有任务完成状态。 */
export class ReceiptIndex {
  ledger: TaskLedger;
  blobs: string;
  readOnly: boolean;
  constructor(ledger: TaskLedger, blobs: string, options: { readOnly?: boolean } = {}) {
    this.ledger = ledger; this.blobs = resolve(blobs);
    this.readOnly = options.readOnly === true;
    if (!this.readOnly) { mkdirSync(this.blobs, { recursive: true, mode: 0o700 }); }
    if (existsSync(this.blobs)) { check(!lstatSync(this.blobs).isSymbolicLink(), 'unsafe_blob_path'); }
  }
  blobPath(digest: string) { check(isHash(digest), 'invalid_receipt_digest'); return join(this.blobs, digest); }
  private inputStatus(actual: unknown, expected: Record<string, string>) {
    if (!isObject(actual)) { return 'unknown'; }
    const projected = Object.create(null);
    for (const [name, entry] of Object.entries(actual)) {
      if (!isObject(entry) || !isHash(entry.sha256)) { return 'unknown'; }
      projected[name] = entry.sha256;
    }
    return stableJson(projected) === stableJson(expected) ? 'match' : 'conflict';
  }
  inspect(taskId: string, attemptId: string, kind: ReceiptKind, path: string): Observation {
    check(['command', 'delivery', 'failed-stage', 'output-execution'].includes(kind), 'unsupported_receipt_kind');
    const attempt = this.ledger.verifyAttempt(taskId, attemptId);
    const binding = this.ledger.getTask(taskId).binding;
    let root = binding.outputRoot;
    if (kind === 'output-execution') {
      const expected = '.filmcraft-execution-' + sha256(binding.outputRoot) + '.json';
      check(path === expected, 'unsafe_receipt_path'); root = dirname(root);
    }
    const bytes = readBoundFile(root, path), raw = parseJson(bytes.toString('utf8'));
    check(isObject(raw), 'invalid_receipt_object');
    const summary: Record<string, any> = { path, format: raw.schema ?? 'unknown',
      taskId, attemptId, sourceRevision: binding.sourceRevision, sourceTreeSha256: binding.sourceTreeSha256,
      planHash: binding.planHash, nativePlanHash: binding.nativePlanHash,
      technicalAcceptance: 'NOT_RUN', creativeAcceptance: 'NOT_RUN', userAcceptance: 'NOT_RUN' };
    const results: string[] = [];
    function compare(key: string, actual: unknown, expected: unknown) {
      const result = actual === undefined ? 'unknown' : stableJson(actual) === stableJson(expected) ? 'match' : 'conflict';
      summary[key] = result; results.push(result);
    }
    if (kind === 'command') {
      check(raw.schema === 'craft-command-receipt/v1', 'unsupported_receipt_format');
      compare('nativePlanIdentity', raw.planSha256, binding.nativePlanHash);
      compare('runtimeIdentity', raw.runtimeSha256, binding.runtimeIdentity.sha256);
      compare('modeIdentity', raw.mode, binding.runtimeIdentity.mode);
      summary.inputIdentity = this.inputStatus(raw.inputs, binding.inputHashes); results.push(summary.inputIdentity);
      summary.nativeOutcome = typeof raw.result === 'string' ? raw.result : 'unknown';
      if (raw.result !== 'PASS') { results.push('unknown'); }
    } else if (kind === 'delivery') {
      check(raw.schema === 'filmcraft-delivery/v1', 'unsupported_receipt_format');
      compare('runtimeIdentity', raw.runtimeSha256, binding.runtimeIdentity.sha256);
      compare('projectRevision', raw.sourceProjectSha256, binding.projectRevision);
      summary.inputIdentity = this.inputStatus(raw.assets, binding.inputHashes); results.push(summary.inputIdentity);
      check(isObject(raw.files) && Object.keys(raw.files).length <= 50_000, 'invalid_delivery_files');
      const files = Object.create(null);
      for (const [name, digest] of Object.entries(raw.files)) {
        check(isHash(digest), 'invalid_delivery_digest');
        const content = readBoundFile(root, name, name.endsWith('.json') ? 16 * 1024 * 1024 : 512 * 1024 * 1024);
        check(sha256(content) === digest, 'artifact_invalid', name);
        files[name] = { sha256: digest, bytes: content.length };
      }
      summary.files = files;
      let loss: unknown;
      if (Object.hasOwn(files, 'exchange-loss.json')) {
        try { loss = parseJson(readBoundFile(root, 'exchange-loss.json').toString('utf8')); }
        catch { loss = null; }
      }
      const packagedInputs = new Set<string>();
      summary.dependencies = [];
      for (const [name, asset] of Object.entries(raw.assets) as [string, any][]) {
        const ref = binding.inputRefs.find(input => input.assetId === name);
        if (!ref) { results.push('unknown'); continue; }
        const packaged = typeof asset.path === 'string' && Object.hasOwn(files, asset.path)
          && files[asset.path].sha256 === ref.sha256;
        if (packaged) { packagedInputs.add(asset.path); }
        summary.dependencies.push({ assetRef: { ...ref }, kind: asset.kind === 'lut' ? 'lut' : 'media',
          packaged, missingReason: packaged ? null : 'dependency packaging not verified' });
        if (!packaged) { results.push('unknown'); }
      }
      summary.exchangeLossIdentity = exchangeLossStatus(raw.lossReport, loss, files, packagedInputs);
      results.push(summary.exchangeLossIdentity);
      if (Object.hasOwn(files, 'plan.json')) {
        const identity = normalizePlan(join(root, 'plan.json'));
        compare('publicPlanIdentity', identity.canonicalPlanSha256, binding.planHash);
        compare('nativePlanIdentity', identity.workflowPlanSha256, binding.nativePlanHash);
      } else { results.push('unknown'); summary.nativePlanIdentity = 'unknown'; }
      summary.capabilityIdentity = 'unknown';
      if (Object.hasOwn(files, 'capabilities.json')) {
        const snapshot = parseJson(readBoundFile(root, 'capabilities.json').toString('utf8'));
        delete snapshot.commandChecks; delete snapshot.resourceChecks;
        compare('capabilityIdentity', sha256(stableJson(snapshot)), binding.runtimeIdentity.capabilitySnapshotSha256);
      } else { results.push('unknown'); }
      check(Object.hasOwn(files, 'project.fcproj'), 'native_project_missing');
    } else if (kind === 'failed-stage') {
      check(raw.schema === 'craft-failed-stage/v1', 'unsupported_receipt_format');
      // 老失败记录没有计划/运行时身份，保留关联与原始失败，不补造身份或成功产物。
      summary.nativeOutcome = raw.outcome ?? 'unknown'; summary.replayAllowed = false;
      summary.planIdentity = 'unknown'; results.push('unknown');
    } else {
      check(raw.schema === 'filmcraft-output-execution/v1', 'unsupported_receipt_format');
      // 核对账本已提交的进程与 guard 原所有者；进程匹配仅是尝试身份的一部分。
      if (Number.isSafeInteger(attempt.pid) && attempt.pid > 0) {
        compare('attemptProcessIdentity', raw.ownerPid, attempt.pid);
      } else { summary.attemptProcessIdentity = 'unknown'; results.push('unknown'); }
      // PID 可被系统复用；新受控执行的上下文须逐项匹配，旧格式缺失字段不补造。
      const context = isObject(raw.context) ? raw.context : {};
      for (const [key, expected] of Object.entries({ taskId, attemptId, sourceRevision: binding.sourceRevision,
        sourceTreeSha256: binding.sourceTreeSha256 })) { compare('executionContext.' + key, context[key], expected); }
      compare('targetIdentity', raw.targetHash, sha256(binding.outputRoot));
      const identity = isObject(raw.identity) ? raw.identity : {};
      compare('nativePlanIdentity', identity.planHash, binding.nativePlanHash);
      // 旧输出执行记录只登记本轮 plan.assets；继承素材由源工程摘要和交付清单另行绑定。
      const plan = parseJson(readBoundFile(binding.outputRoot, 'plan.json').toString('utf8'));
      compare('compiledPlanIdentity', normalizePlan(join(binding.outputRoot, 'plan.json')).workflowPlanSha256, binding.nativePlanHash);
      const declared = isObject(plan.assets) ? plan.assets : {}, nativeInputs = Object.create(null);
      for (const [name, asset] of Object.entries(declared)) {
        check(isObject(asset) && isHash(asset.sha256), 'invalid_native_input_identity'); nativeInputs[name] = asset.sha256;
      }
      compare('inputIdentity', identity.inputHashes, nativeInputs);
      compare('projectRevision', identity.projectRevision, binding.projectRevision);
      compare('runtimeIdentity', identity.runtimeSha256, binding.runtimeIdentity.sha256);
      summary.nativeOutcome = raw.state ?? 'unknown';
      if (raw.state !== 'finished') { results.push('unknown'); }
    }
    const status = results.includes('conflict') ? 'conflict' : results.includes('unknown') ? 'unknown' : 'linked';
    return { status, sha256: sha256(bytes), kind, summary, bytes };
  }
  ingest(taskId: string, attemptId: string, kind: ReceiptKind, path: string) {
    check(!this.readOnly, 'receipt_index_read_only');
    const observation = this.inspect(taskId, attemptId, kind, path);
    const location = this.blobPath(observation.sha256);
    try { writeFileSync(location, observation.bytes, { flag: 'wx', mode: 0o600 }); }
    catch (error: any) {
      if (error.code !== 'EEXIST') { throw error; }
      check(sha256(readBoundFile(this.blobs, observation.sha256)) === observation.sha256, 'blob_conflict');
    }
    this.ledger.recordReceipt(taskId, attemptId, kind, observation.sha256, observation.summary, observation.status);
    return { kind, status: observation.status, sha256: observation.sha256 };
  }
  collect(taskId: string, attemptId: string) {
    this.ledger.verifyAttempt(taskId, attemptId);
    const task = this.ledger.getTask(taskId), records = this.ledger.receipts(taskId, attemptId);
    let status: Status = records.length ? 'linked' : 'unknown';
    const kinds = new Set(records.map(record => record.kind));
    const missingReceiptKinds = kinds.has('delivery') || kinds.has('output-execution')
      ? ['delivery', 'output-execution'].filter(kind => !kinds.has(kind)) : [];
    if (missingReceiptKinds.length) { status = 'unknown'; }
    const evidenceRefs = [], outputRefs = [];
    for (const record of records) {
      try {
        const current = this.inspect(taskId, attemptId, record.kind as ReceiptKind, record.summary.path);
        const archived = readBoundFile(this.blobs, record.sha256);
        if (current.sha256 !== record.sha256 || sha256(archived) !== record.sha256) { status = 'stale'; continue; }
        if (record.status === 'conflict' || current.status === 'conflict') { status = 'conflict'; }
        else if ((record.status !== 'linked' || current.status !== 'linked') && status === 'linked') { status = 'unknown'; }
        evidenceRefs.push({ assetId: 'receipt:' + record.kind, version: record.sha256, sha256: record.sha256, location: record.summary.path });
        if (record.kind === 'delivery' && record.status === 'linked' && current.status === 'linked') {
          const files = current.summary.files;
          const native = files['project.fcproj'];
          for (const [path, file] of Object.entries(files) as [string, any][]) {
            outputRefs.push({ protocolVersion: 'craft-artifact/v1', assetId: assetId(taskId, path),
              version: file.sha256, sha256: file.sha256, bytes: file.bytes,
              // 格式识别与技术核验尚未执行时使用诚实的二进制类型，不猜测媒体属性。
              mediaType: 'application/octet-stream', producerTaskId: taskId, sourceRefs: refs(task.binding),
              nativeProjectRef: { assetId: assetId(taskId, 'project.fcproj'), version: native.sha256, sha256: native.sha256, location: 'project.fcproj' },
              renditions: [], dependencies: current.summary.dependencies, technicalMetadata: {},
              lossReportRef: files['exchange-loss.json'] ? { assetId: assetId(taskId, 'exchange-loss.json'),
                version: files['exchange-loss.json'].sha256, sha256: files['exchange-loss.json'].sha256, location: 'exchange-loss.json' } : null,
              evidenceRefs: [{ assetId: 'receipt:' + record.kind, version: record.sha256, sha256: record.sha256, location: record.summary.path }], location: path });
          }
        }
      } catch { status = 'stale'; }
    }
    // 任一冲突或过期不能混合成可消费产物；不更改账本任务或质量状态。
    return { taskId, attemptId, state: task.state, runtimeIdentity: task.binding.runtimeIdentity,
      status, missingReceiptKinds, outputRefs: status === 'linked' ? outputRefs : [], evidenceRefs,
      technicalAcceptance: 'NOT_RUN', creativeAcceptance: 'NOT_RUN', userAcceptance: 'NOT_RUN',
      error: status === 'linked' ? null : { code: status === 'conflict' ? 'receipt_conflict' : status === 'stale' ? 'artifact_invalid' : 'outcome_unknown' } };
  }
}
