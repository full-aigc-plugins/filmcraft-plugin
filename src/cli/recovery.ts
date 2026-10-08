import { parseArgs } from 'node:util';
import { RecoveryService } from '../harness/recovery.ts';
import { check, HarnessError } from '../support/json.ts';

/** 显式区分只读诊断与账本修复；不提供删除锁或重放编辑的快捷入口。 */
function main() {
  const { values, positionals } = parseArgs({ allowPositionals: true, options: {
    ledger: { type: 'string' }, blobs: { type: 'string' }, task: { type: 'string' }, help: { type: 'boolean' },
    'expected-epoch': { type: 'string' }, 'inspection-sha256': { type: 'string' },
    'authorization-ref': { type: 'string' }, 'authorization-scope-sha256': { type: 'string' },
  } });
  if (values.help) {
    console.log('node src/cli/recovery.ts inspect|reconcile|repair --ledger FILE --blobs DIRECTORY --task ID\n'
      + 'inspect and reconcile are read-only. repair additionally requires --expected-epoch, --inspection-sha256, --authorization-ref and --authorization-scope-sha256.');
    return;
  }
  const action = positionals[0];
  check(positionals.length === 1 && ['inspect', 'reconcile', 'repair'].includes(action)
    && values.ledger && values.blobs && values.task, 'invalid_recovery_arguments');
  const service = new RecoveryService(values.ledger, values.blobs);
  if (action !== 'repair') {
    const report = service.inspect(values.task); console.log(JSON.stringify(report));
    process.exitCode = report.diagnosis === 'unknown' ? 2 : 0; return;
  }
  check(values['expected-epoch'] !== undefined && /^[0-9]+$/.test(values['expected-epoch'])
    && Number.isSafeInteger(Number(values['expected-epoch'])) && values['inspection-sha256']
    && values['authorization-ref'] && values['authorization-scope-sha256'], 'invalid_recovery_arguments');
  const report = service.repair(values.task, { expectedEpoch: Number(values['expected-epoch']),
    inspectionSha256: values['inspection-sha256'], authorizationRef: values['authorization-ref'],
    authorizationScopeSha256: values['authorization-scope-sha256'] });
  console.log(JSON.stringify(report));
}
try { main(); }
catch (error) {
  console.log(JSON.stringify({ schema: 'filmcraft-recovery-error/v1', replayAllowed: false,
    error: { code: error instanceof HarnessError ? error.code : 'recovery_failed' } }));
  process.exitCode = 1;
}
