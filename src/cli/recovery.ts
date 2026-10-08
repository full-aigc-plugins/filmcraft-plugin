import { validatePermissions } from '../support/execution_permissions.ts';
import { parseArgs } from 'node:util';
import { dirname, basename, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { LocalAuthorizationStore } from '../harness/authorization.ts';
import { RecoveryService } from '../harness/recovery.ts';
import { ContinuationService } from '../harness/continuation.ts';
import { StateMaintenance } from '../harness/state_maintenance.ts';
import { TaskLedger } from '../harness/task_ledger.ts';
import { CancellationService } from '../harness/cancellation.ts';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { check, HarnessError, parseJson } from '../support/json.ts';

/** 只读诊断、状态修复、原生继续及状态维护各走独立门禁。 */
async function main() {
  const { values, positionals } = parseArgs({ allowPositionals: true, options: {
    ledger: { type: 'string' }, blobs: { type: 'string' }, task: { type: 'string' }, help: { type: 'boolean' },
    'authorization-root': { type: 'string' }, 'expected-epoch': { type: 'string' }, 'inspection-sha256': { type: 'string' },
    'authorization-ref': { type: 'string' }, 'authorization-scope-sha256': { type: 'string' }, backup: { type: 'string' },
    'child-binding': { type: 'string' }, plan: { type: 'string' }, 'runtime-home': { type: 'string' }, python: { type: 'string' },
    permissions: { type: 'string' }, signal: { type: 'boolean' },
  } });
  if (values.help) {
    console.log('node src/cli/recovery.ts inspect|reconcile|repair|continue|upgrade|rollback|cancel|cancel-reconcile --ledger FILE\n'
      + 'inspect/reconcile: read-only; --blobs DIRECTORY --task ID.\n'
      + 'repair/continue: additionally --expected-epoch --inspection-sha256 --authorization-ref --authorization-scope-sha256 --authorization-root.\n'
      + 'continue: additionally --permissions FILE --child-binding FILE --plan FILE --runtime-home DIRECTORY [--python FILE]. Original task must be independently repaired to verifying.\n'
      + 'upgrade/rollback: --backup DIRECTORY --authorization-ref --authorization-scope-sha256 --authorization-root.\n'
      + 'cancel: --task ID --authorization-ref --authorization-scope-sha256 --authorization-root. Persists the request only.\n'
      + 'cancel-reconcile: --task ID [--signal --authorization-root DIRECTORY] [--python FILE]. Signals only identity-bound supported process groups. Private host grants are never created by this CLI.');
    return;
  }
  const action = positionals[0];
  check(positionals.length === 1 && ['inspect','reconcile','repair','continue','upgrade','rollback','cancel','cancel-reconcile'].includes(action)
    && values.ledger, 'invalid_recovery_arguments');
  const authorize = !['inspect','reconcile'].includes(action) && values['authorization-root']
    ? new LocalAuthorizationStore(values['authorization-root']).authorize : undefined;
  const authorization = { authorizationRef: values['authorization-ref']!, authorizationScopeSha256: values['authorization-scope-sha256']! };
  if (action === 'cancel' || action === 'cancel-reconcile') {
    check(values.task, 'invalid_recovery_arguments');
    const db = new TaskLedger(values.ledger);
    try {
      const cancellation = new CancellationService(db, { authorize, python: values.python });
      console.log(JSON.stringify(action === 'cancel' ? cancellation.request(values.task, authorization)
        : cancellation.reconcile(values.task, { signal: values.signal })));
    } finally { db.close(); }
    return;
  }
  if (action === 'upgrade' || action === 'rollback') {
    check(values.backup && authorization.authorizationRef && authorization.authorizationScopeSha256, 'invalid_recovery_arguments');
    const service = new StateMaintenance(values.ledger, { authorize });
    console.log(JSON.stringify(action === 'upgrade' ? service.upgrade(values.backup, authorization) : service.rollback(values.backup, authorization)));
    return;
  }
  check(values.blobs && values.task, 'invalid_recovery_arguments');
  const service = new RecoveryService(values.ledger, values.blobs, { authorize });
  if (action === 'inspect' || action === 'reconcile') {
    const report = service.inspect(values.task); console.log(JSON.stringify(report));
    process.exitCode = report.diagnosis === 'unknown' ? 2 : 0; return;
  }
  check(values['expected-epoch'] !== undefined && /^[0-9]+$/.test(values['expected-epoch'])
    && Number.isSafeInteger(Number(values['expected-epoch'])) && values['inspection-sha256']
    && authorization.authorizationRef && authorization.authorizationScopeSha256, 'invalid_recovery_arguments');
  const request = { ...authorization, expectedEpoch: Number(values['expected-epoch']), inspectionSha256: values['inspection-sha256'] };
  if (action === 'repair') { console.log(JSON.stringify(service.repair(values.task, request))); return; }
  check(values['child-binding'] && values.plan && values['runtime-home'], 'invalid_recovery_arguments');
  const bindingPath = resolve(values['child-binding']), child = parseJson(readBoundFile(dirname(bindingPath), basename(bindingPath)).toString('utf8'));
  const plugin = fileURLToPath(new URL('../../', import.meta.url));
  const manifest = parseJson(readBoundFile(plugin, 'plugin.json').toString('utf8'));
  const lock = parseJson(readBoundFile(plugin, 'skills.lock.json').toString('utf8'));
  const permissionPath=values.permissions?resolve(values.permissions):null;
  const permissions=permissionPath?validatePermissions(parseJson(readBoundFile(dirname(permissionPath),basename(permissionPath)).toString('utf8'))):undefined;
  const report = await new ContinuationService(values.ledger, values.blobs, { authorize }).continue(values.task, request,
    child, values.plan, { skillDirectory: join(plugin, 'skills/filmcraft-use'), sourceRevision: lock.sources[0].sha,
      permissions, pluginVersion: manifest.version, runtimeHome: values['runtime-home'], python: values.python });
  console.log(JSON.stringify(report));
}
try { await main(); }
catch (error) {
  console.log(JSON.stringify({ schema: 'filmcraft-recovery-error/v1', replayAllowed: false,
    error: { code: error instanceof HarnessError ? error.code : 'recovery_failed' } }));
  process.exitCode = 1;
}
