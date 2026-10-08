import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync, symlinkSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { PythonWorkflowRunner } from '../../src/adapters/python_workflow.ts';
import { publicTask } from '../../src/adapters/protocol_mapping.ts';
import { LocalAuthorizationStore } from '../../src/harness/authorization.ts';
import { ContinuationService, continuationSubject } from '../../src/harness/continuation.ts';
import { RecoveryService } from '../../src/harness/recovery.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { binding, workspace, captureEvidence } from './fixtures.ts';

test('actual Python native workflow binds SQL attempts, preserves original project and does not repeat a completed attempt',
  { skip: process.env.FILMCRAFT_NATIVE_HARNESS !== '1', timeout: 240_000 }, async t => {
    assert.ok(process.env.FILMCRAFT_NATIVE_SKILL, 'explicit source candidate skill required');
    const root = workspace(t), python = process.env.FILMCRAFT_PYTHON ?? 'python3';
    const skill = process.env.FILMCRAFT_NATIVE_SKILL!, image = join(root, 'still.png');
    const picture = spawnSync(python, ['-c', 'from PIL import Image; import sys; Image.new("RGBA",(32,32),(239,91,54,255)).save(sys.argv[1])', image]);
    assert.equal(picture.status, 0, picture.stderr?.toString());
    const plan = JSON.parse(readFileSync(join(skill, 'examples/native-workflow.json'), 'utf8'));
    const imageHash = sha256(readFileSync(image)); plan.assets = { still: { path: image, sha256: imageHash } };
    const planFile = join(root, 'plan.json'); writeFileSync(planFile, JSON.stringify(plan));
    const dbFile = join(root, 'ledger.sqlite'), db = new TaskLedger(dbFile); t.after(() => db.close());
    const index = new ReceiptIndex(db, join(root, 'blobs'));
    const sourceRevision = process.env.FILMCRAFT_NATIVE_SOURCE_REVISION!;
    assert.match(sourceRevision, /^[a-f0-9]{40}$/);
    const options = { python, skillDirectory: skill, sourceRevision,
      runtimeHome: process.env.FILMCRAFT_NATIVE_RUNTIME_HOME ?? join(process.env.HOME!, '.local/share/craft-runtimes'), pluginVersion: JSON.parse(readFileSync(new URL('../../plugin.json', import.meta.url), 'utf8')).version };
    const alias = join(root, 'parent-alias'); symlinkSync(root, alias);
    const runner = new PythonWorkflowRunner(db, index, options), output = join(alias, 'delivery');
    const prepared = runner.prepare(planFile, output);
    const task = binding(root, { planHash: prepared.planIdentity.canonicalPlanSha256,
      projectKey: prepared.projectKey, outputRoot: output,
      nativePlanHash: prepared.planIdentity.workflowPlanSha256, sourceRevision,
      sourceTreeSha256: prepared.sourceTreeSha256, runtimeIdentity: prepared.runtimeIdentity,
      inputHashes: { still: imageHash }, inputRefs: [{ assetId: 'still', version: 'fixture-v1', sha256: imageHash }] });
    const wrongHash = '0'.repeat(64);
    await assert.rejects(runner.run({ ...task, taskId: 'bad-input', idempotencyKey: 'bad-input',
      inputHashes: { still: wrongHash }, inputRefs: [{ assetId: 'still', version: 'wrong', sha256: wrongHash }] }, planFile), /input_identity_conflict/);
    assert.throws(() => db.getTask('bad-input'), /task_missing/);
    const made = await runner.run(task, planFile);
    assert.equal(made.state, 'verifying'); assert.equal(made.process?.stopped, true);
    assert.equal(made.receipt?.status, 'linked'); assert.ok(made.receipt!.outputRefs.length > 0);
    assert.equal(made.receipt?.technicalAcceptance, 'NOT_RUN');
    const project = join(output, 'project.fcproj'), originalHash = sha256(readFileSync(project));
    const reused = await runner.run(task, planFile);
    assert.equal(reused.reused, true); assert.equal(reused.attemptId, made.attemptId);
    assert.equal(db.listAttempts(task.taskId).length, 1);
    const revisionPlan = { ...plan, expectedProjectSha256: originalHash };
    delete revisionPlan.document; delete revisionPlan.assets;
    revisionPlan.operations = [{ command: 'timeline.select', params: { clips: { $ref: 'clip.clips' }, add: false, toggle: false } }, plan.operations.at(-1)];
    revisionPlan.operations[1].params.params.speed = 200;
    const revisionFile = join(root, 'revision.json'); writeFileSync(revisionFile, JSON.stringify(revisionPlan));
    const revisedOutput = join(root, 'revised'), revision = runner.prepare(revisionFile, revisedOutput, output);
    const second = { ...task, taskId: 'revision-1', idempotencyKey: 'revision-request', outputRoot: revisedOutput,
      projectKey: revision.projectKey,
      planHash: revision.planIdentity.canonicalPlanSha256, nativePlanHash: revision.planIdentity.workflowPlanSha256,
      runtimeIdentity: revision.runtimeIdentity, projectRevision: originalHash };
    const revised = await runner.run(second, revisionFile, output);
    assert.equal(revised.state, 'verifying'); assert.equal(revised.receipt?.status, 'linked');
    assert.notEqual(sha256(readFileSync(join(revisedOutput, 'project.fcproj'))), originalHash);
    assert.equal(sha256(readFileSync(project)), originalHash);
    const receipt = index.collect(task.taskId, made.attemptId!);
    assert.equal(receipt.status, 'linked'); assert.equal(receipt.state, 'verifying');
    // 真实原生导出结束后丢失回执交接：不再启动原生工作流，只修复原尝试状态。
    const lostOutput = join(root, 'lost-reply'), lostPrepared = runner.prepare(planFile, lostOutput);
    const lostTask = { ...task, taskId: 'lost-reply', idempotencyKey: 'lost-reply-request', outputRoot: lostOutput,
      projectKey: lostPrepared.projectKey, runtimeIdentity: lostPrepared.runtimeIdentity };
    const lostBlobs = join(root, 'lost-blobs'), lostIndex = new ReceiptIndex(db, lostBlobs);
    const ingest = lostIndex.ingest.bind(lostIndex); let injected = false;
    lostIndex.ingest = (...args) => { if (!injected) { injected = true; throw new Error('injected_receipt_reply_lost'); } return ingest(...args); };
    const lostRunner = new PythonWorkflowRunner(db, lostIndex, options);
    await assert.rejects(lostRunner.run(lostTask, planFile), /injected_receipt_reply_lost/);
    assert.equal(db.getTask(lostTask.taskId).state, 'reconciling');
    function nativeFiles() {
      const hashes: Record<string, string> = {};
      function walk(path: string) { for (const file of readdirSync(path, { withFileTypes: true })) {
        const name = join(path, file.name); if (file.isDirectory()) { walk(name); } else { hashes[name] = sha256(readFileSync(name)); }
      } }
      walk(lostOutput);
      const guard = join(root, '.filmcraft-execution-' + sha256(lostOutput) + '.json');
      hashes[guard] = sha256(readFileSync(guard)); return hashes;
    }
    const nativeBefore = nativeFiles(), readonlyBefore = { ...nativeBefore };
    for (const suffix of ['', '-wal', '-shm']) {
      if (existsSync(dbFile + suffix)) { readonlyBefore[dbFile + suffix] = sha256(readFileSync(dbFile + suffix)); }
    }
    const diagnosed = new RecoveryService(dbFile, lostBlobs).inspect(lostTask.taskId);
    const grantRoot = join(root, 'host-grants'); mkdirSync(grantRoot, { mode: 0o700 });
    const grantFile = join(grantRoot, sha256(lostTask.authorizationRef) + '.json');
    const grant = { schema: 'filmcraft-local-authorization/v1', authorizationRef: lostTask.authorizationRef,
      authorizationScopeSha256: lostTask.authorizationScopeSha256, expiresAt: Date.now() + 300_000, revoked: false,
      subjects: [sha256(stableJson({ action: 'repair', identitySha256: diagnosed.bindingSha256 }))] };
    const writeGrant = () => writeFileSync(grantFile, JSON.stringify(grant), { mode: 0o600 }); writeGrant();
    const localAuthorizer = new LocalAuthorizationStore(grantRoot).authorize;
    const recovery = new RecoveryService(dbFile, lostBlobs, { authorize: localAuthorizer });
    assert.equal(diagnosed.diagnosis, 'executed');
    for (const [file, digest] of Object.entries(readonlyBefore)) { assert.equal(sha256(readFileSync(file)), digest, 'diagnosis changed original data'); }
    const repaired = recovery.repair(lostTask.taskId, { expectedEpoch: diagnosed.task!.epoch,
      inspectionSha256: diagnosed.evidenceSha256, authorizationRef: lostTask.authorizationRef,
      authorizationScopeSha256: lostTask.authorizationScopeSha256 });
    assert.equal(repaired.state, 'verifying'); assert.equal(repaired.replayed, false);
    assert.equal(repaired.receipt.status, 'linked'); assert.deepEqual(nativeFiles(), nativeBefore);
    assert.equal(db.listAttempts(lostTask.taskId).length, 1);
    assert.equal(db.listRecoveryIntents(lostTask.taskId)[0].state, 'applied');
    const reusedLost = await lostRunner.run(lostTask, planFile);
    assert.equal(reusedLost.reused, true); assert.equal(reusedLost.attemptId, repaired.attemptId);
    // 明确剩余计划独立继续：原尝试已经修复，只有新子任务执行原生返工。
    const continuationFile = join(root, 'continue.json'), continuationOutput = join(root, 'continued');
    const continuationPlan = { ...revisionPlan, expectedProjectSha256: sha256(readFileSync(join(lostOutput, 'project.fcproj'))) };
    writeFileSync(continuationFile, JSON.stringify(continuationPlan));
    const continuationPrepared = runner.prepare(continuationFile, continuationOutput, lostOutput);
    const continuationTask = { ...task, taskId: 'continue-1', idempotencyKey: 'continue-request',
      outputRoot: continuationOutput, projectKey: continuationPrepared.projectKey,
      projectRevision: continuationPrepared.projectRevision,
      planHash: continuationPrepared.planIdentity.canonicalPlanSha256, nativePlanHash: continuationPrepared.planIdentity.workflowPlanSha256,
      runtimeIdentity: continuationPrepared.runtimeIdentity };
    const continuationService = new ContinuationService(dbFile, lostBlobs, { authorize: localAuthorizer });
    const continuationRequest = () => { const current = recovery.inspect(lostTask.taskId); return {
      expectedEpoch: current.task!.epoch, inspectionSha256: current.evidenceSha256,
      authorizationRef: lostTask.authorizationRef, authorizationScopeSha256: lostTask.authorizationScopeSha256 }; };
    const oldRequest = continuationRequest(), originalLost = nativeFiles();
    const origin = recovery.inspect(lostTask.taskId);
    grant.subjects.push(sha256(stableJson(continuationSubject(lostTask.taskId, repaired.attemptId,
      origin.contentSha256, continuationTask, sha256(readFileSync(continuationFile)))))); writeGrant();
    const continued = await continuationService.continue(lostTask.taskId, oldRequest, continuationTask, continuationFile, options);
    assert.equal(continued.task.state, 'verifying'); assert.equal(continued.originalReplayed, false);
    assert.equal(continued.continuation.state, 'applied');
    assert.equal(db.listAttempts(lostTask.taskId).length, 1); assert.equal(db.listAttempts(continuationTask.taskId).length, 1);
    assert.equal(db.listContinuations(lostTask.taskId).length, 1);
    assert.deepEqual(nativeFiles(), originalLost);
    await assert.rejects(continuationService.continue(lostTask.taskId, oldRequest, continuationTask, continuationFile, options), /inspection_stale/);
    const reusedContinuation = await continuationService.continue(lostTask.taskId, continuationRequest(), continuationTask, continuationFile, options);
    assert.equal(reusedContinuation.intentReused, true); assert.equal(reusedContinuation.task.reused, true);
    assert.equal(db.listAttempts(continuationTask.taskId).length, 1); assert.equal(db.listContinuations(lostTask.taskId).length, 1);
    const childBindingFile = join(root, 'child-binding.json'); writeFileSync(childBindingFile, JSON.stringify(continuationTask));
    const cliRequest = continuationRequest();
    const cliContinue = spawnSync(process.execPath, [new URL('../../src/cli/recovery.ts', import.meta.url).pathname, 'continue',
      '--ledger', dbFile, '--blobs', lostBlobs, '--task', lostTask.taskId,
      '--expected-epoch', String(cliRequest.expectedEpoch), '--inspection-sha256', cliRequest.inspectionSha256,
      '--authorization-ref', lostTask.authorizationRef, '--authorization-scope-sha256', lostTask.authorizationScopeSha256,
      '--authorization-root', grantRoot, '--child-binding', childBindingFile, '--plan', continuationFile,
      '--runtime-home', options.runtimeHome, '--python', python], { encoding: 'utf8', timeout: 180_000 });
    assert.equal(cliContinue.status, 0, cliContinue.stdout + cliContinue.stderr);
    assert.equal(JSON.parse(cliContinue.stdout).task.reused, true);
    assert.equal(db.listAttempts(continuationTask.taskId).length, 1);
    captureEvidence('actual-native-repair-and-continuation', 'actual Python/native create, lost reply, repair and continued editing; actual private host grants', { nativeBefore, nativeAfter: nativeFiles(), originalAttempts: db.listAttempts(lostTask.taskId), childAttempts: db.listAttempts(continuationTask.taskId), recoveryIntents: db.listRecoveryIntents(lostTask.taskId), continuationIntents: db.listContinuations(lostTask.taskId), readonlyFilesPreserved: true, originalReplayed: false, quality: 'NOT_RUN' });
    if (process.env.FILMCRAFT_HARNESS_REPORT) {
      // 输出协议对象不含本机绝对路径，供固定所有者 schema 另行核验。
      const report = { schema: 'filmcraft-harness-native-candidate/v1', result: 'PASS', nodeVersion: process.version,
        scope: 'internal Node/SQLite adapter and actual Python workflow; installation layer verified separately by caller; not quality or full Harness acceptance',
        sourceRevision, sourceTreeSha256: prepared.sourceTreeSha256, runtimeIdentity: prepared.runtimeIdentity,
        taskId: task.taskId, attemptId: made.attemptId, revisionAttemptId: revised.attemptId,
        createState: made.state, revisionState: revised.state, idempotentReuse: reused.reused,
        actualProjectSha256: originalHash, revisedProjectSha256: sha256(readFileSync(join(revisedOutput, 'project.fcproj'))),
        originalPreserved: true, outputParentAliasVerified: true, processesStopped: made.process?.stopped && revised.process?.stopped,
        receipts: db.receipts(task.taskId, made.attemptId!), publicArtifacts: [...receipt.outputRefs, ...continued.task.receipt!.outputRefs],
        publicTasks: [task, second, continuationTask].map(item => publicTask(db, item.taskId,
          { schemaVersion: 'filmcraft-native-workflow/v1', nativePlanHash: item.nativePlanHash },
          { currency: 'USD', maxMinorUnits: 0, maxRevisions: 1, maxExternalCalls: 0 })),
        recovery: { injected: 'receipt transfer lost after actual native export', inspection: diagnosed,
          state: repaired.state, attemptId: repaired.attemptId, recoveryId: repaired.recoveryId,
          replayed: repaired.replayed, readonlyFilesPreserved: true, nativeFilesPreserved: true,
          originalAttemptCount: db.listAttempts(lostTask.taskId).length, idempotentReuse: reusedLost.reused,
          intents: db.listRecoveryIntents(lostTask.taskId) },
        continuation: { state: continued.task.state, originalReplayed: false, originalAttemptCount: db.listAttempts(lostTask.taskId).length,
          childAttemptCount: db.listAttempts(continuationTask.taskId).length, intentCount: db.listContinuations(lostTask.taskId).length,
          reused: reusedContinuation.task.reused, intent: db.listContinuations(lostTask.taskId)[0] },
        technicalAcceptance: receipt.technicalAcceptance, creativeAcceptance: receipt.creativeAcceptance,
        userAcceptance: receipt.userAcceptance, recoveryAuthorization: 'actual private LocalAuthorizationStore for repair and continuation; existing scoped grant reused', authScopeValidation: 'general workflow admission HOST_REQUIRED', budgetEnforcement: 'NOT_IMPLEMENTED' };
      writeFileSync(process.env.FILMCRAFT_HARNESS_REPORT, JSON.stringify(report, null, 2) + '\n');
    }
  });
