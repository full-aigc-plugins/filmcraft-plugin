import {AssetPreflightRefusal} from '../adapters/asset_refusal.ts';
import {ClipTimingRefusal} from '../adapters/clip_refusal.ts';
import { parseArgs } from 'node:util';
import {existsSync} from 'node:fs';
import {readRuntimeCandidate} from '../adapters/runtime_candidate.ts';
import {RuntimeDeployment} from '../adapters/runtime_deployment.ts';
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
    'runtime-home': { type: 'string' }, python: { type: 'string' }, candidate: {type:'string'},
  } });
  if (values.help) {
    console.log('node src/cli/workflow.ts subject|run --binding FILE [--resources FILE]\n'
      + 'subject: read-only authorization subject; never creates a grant.\n'
      + 'run: --resources FILE --plan FILE --ledger FILE --blobs DIRECTORY --authorization-root DIRECTORY --runtime-home DIRECTORY [--source DELIVERY] [--python FILE] [--candidate FILE].\n'
      + 'A retained candidate must match the binding and an already activated ledger selection; it cannot authorize or activate itself.\n'
      + 'Trusted host grants must already authorize the exact subject. Unknown outcomes are never replayed.');
    return;
  }
  check(positionals.length === 1 && ['subject','run'].includes(positionals[0]) && values.binding, 'invalid_workflow_arguments');
  const path = resolve(values.binding), binding = parseJson(readBoundFile(dirname(path), basename(path)).toString('utf8'));
  const resourcePath = values.resources ? resolve(values.resources) : null;
  const resources = resourcePath ? parseJson(readBoundFile(dirname(resourcePath), basename(resourcePath)).toString('utf8')) : undefined;
  const candidate=values.candidate?readRuntimeCandidate(values.candidate):null;
  if(candidate){check(candidate.sourceRevision===binding.sourceRevision&&candidate.sourceTreeSha256===binding.sourceTreeSha256,'runtime_candidate_binding_mismatch');}
  const subject = executionSubject(binding, resources);
  if (positionals[0] === 'subject') { console.log(JSON.stringify(subject)); return; }
  check(values.resources && values.plan && values.ledger && values.blobs && values['authorization-root'] && values['runtime-home'], 'invalid_workflow_arguments');
  const authorize = new LocalAuthorizationStore(values['authorization-root']).authorize;
  // 在创建或打开有副作用的账本前先拒绝未授权请求。
  requireAuthorization(authorize, binding, subject);
  const root = fileURLToPath(new URL('../../', import.meta.url));
  const manifest = parseJson(readBoundFile(root, 'plugin.json').toString('utf8'));
  const lock = parseJson(readBoundFile(root, 'skills.lock.json').toString('utf8'));
  if(candidate){check(existsSync(values.ledger),'runtime_selection_required');}
  const db = new TaskLedger(values.ledger);
  try {
    if(candidate){
      check(new RuntimeDeployment(db).current(),'runtime_selection_required');
      db.assertRuntime(binding);
      check(binding.runtimeIdentity.pluginVersion===manifest.version,'runtime_selection_mismatch');
    }
    const service = new WorkflowAdmission(db, new ReceiptIndex(db, values.blobs), {
      skillDirectory: candidate?.skillDirectory??join(root, 'skills/filmcraft-use'), sourceRevision: candidate?.sourceRevision??lock.sources[0].sha,
      resources, pluginVersion: manifest.version, runtimeHome: values['runtime-home'], python: values.python,
    }, authorize);
    console.log(JSON.stringify(await service.run(binding, values.plan, values.source)));
  } finally { db.close(); }
}
try { await main(); }
catch (error) {
  console.log(JSON.stringify({ schema: 'filmcraft-workflow-admission-error/v1', replayAllowed: false,
    error: { code: error instanceof HarnessError ? error.code : 'workflow_admission_failed',
      ...(error instanceof CapabilityRefusal&&error.diagnostic?{diagnostic:error.diagnostic}:{}),...(error instanceof AssetPreflightRefusal?{assetIssues:error.assetIssues}:{}),...(error instanceof ClipTimingRefusal?{clipTiming:error.clipTiming}:{}) } }));
  process.exitCode = 1;
}
