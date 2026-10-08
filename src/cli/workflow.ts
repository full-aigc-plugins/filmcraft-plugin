import { parseArgs } from 'node:util';
import { CapabilityRefusal } from '../adapters/capability_refusal.ts';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readBoundFile, ReceiptIndex } from '../artifacts/receipt_index.ts';
import { LocalAuthorizationStore, requireAuthorization } from '../harness/authorization.ts';
import { WorkflowAdmission, executionSubject } from '../harness/workflow_admission.ts';
import { TaskLedger } from '../harness/task_ledger.ts';
import { check, HarnessError, parseJson } from '../support/json.ts';

/** 宿主首次执行入口；授权记录只能由宿主维护，本入口不创建许可。 */
async function main() {
  const { values, positionals } = parseArgs({ allowPositionals: true, options: {
    help: { type: 'boolean' }, binding: { type: 'string' }, plan: { type: 'string' }, source: { type: 'string' },
    resources: { type: 'string' }, ledger: { type: 'string' }, blobs: { type: 'string' }, 'authorization-root': { type: 'string' },
    'runtime-home': { type: 'string' }, python: { type: 'string' },
  } });
  if (values.help) {
    console.log('node src/cli/workflow.ts subject|run --binding FILE [--resources FILE]\n'
      + 'subject: read-only authorization subject; never creates a grant.\n'
      + 'run: --resources FILE --plan FILE --ledger FILE --blobs DIRECTORY --authorization-root DIRECTORY --runtime-home DIRECTORY [--source DELIVERY] [--python FILE].\n'
      + 'Trusted host grants must already authorize the exact subject. Unknown outcomes are never replayed.');
    return;
  }
  check(positionals.length === 1 && ['subject','run'].includes(positionals[0]) && values.binding, 'invalid_workflow_arguments');
  const path = resolve(values.binding), binding = parseJson(readBoundFile(dirname(path), basename(path)).toString('utf8'));
  const resourcePath = values.resources ? resolve(values.resources) : null;
  const resources = resourcePath ? parseJson(readBoundFile(dirname(resourcePath), basename(resourcePath)).toString('utf8')) : undefined;
  const subject = executionSubject(binding, resources);
  if (positionals[0] === 'subject') { console.log(JSON.stringify(subject)); return; }
  check(values.resources && values.plan && values.ledger && values.blobs && values['authorization-root'] && values['runtime-home'], 'invalid_workflow_arguments');
  const authorize = new LocalAuthorizationStore(values['authorization-root']).authorize;
  // 在创建或打开有副作用的账本前先拒绝未授权请求。
  requireAuthorization(authorize, binding, subject);
  const root = fileURLToPath(new URL('../../', import.meta.url));
  const manifest = parseJson(readBoundFile(root, 'plugin.json').toString('utf8'));
  const lock = parseJson(readBoundFile(root, 'skills.lock.json').toString('utf8'));
  const db = new TaskLedger(values.ledger);
  try {
    const service = new WorkflowAdmission(db, new ReceiptIndex(db, values.blobs), {
      skillDirectory: join(root, 'skills/filmcraft-use'), sourceRevision: lock.sources[0].sha,
      resources, pluginVersion: manifest.version, runtimeHome: values['runtime-home'], python: values.python,
    }, authorize);
    console.log(JSON.stringify(await service.run(binding, values.plan, values.source)));
  } finally { db.close(); }
}
try { await main(); }
catch (error) {
  console.log(JSON.stringify({ schema: 'filmcraft-workflow-admission-error/v1', replayAllowed: false,
    error: { code: error instanceof HarnessError ? error.code : 'workflow_admission_failed',
      ...(error instanceof CapabilityRefusal&&error.diagnostic?{diagnostic:error.diagnostic}:{}) } }));
  process.exitCode = 1;
}
