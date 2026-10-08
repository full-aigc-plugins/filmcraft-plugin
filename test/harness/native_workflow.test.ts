import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync, writeFileSync, symlinkSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { PythonWorkflowRunner } from '../../src/adapters/python_workflow.ts';
import { publicTask } from '../../src/adapters/protocol_mapping.ts';
import { RecoveryService } from '../../src/harness/recovery.ts';
import { sha256 } from '../../src/support/json.ts';
import { binding, workspace } from './fixtures.ts';

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
      runtimeHome: join(process.env.HOME!, '.local/share/craft-runtimes'), pluginVersion: JSON.parse(readFileSync(new URL('../../plugin.json', import.meta.url), 'utf8')).version };
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
    const recovery = new RecoveryService(dbFile, lostBlobs), diagnosed = recovery.inspect(lostTask.taskId);
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
    if (process.env.FILMCRAFT_HARNESS_REPORT) {
      // 输出协议对象不含本机绝对路径，供固定所有者 schema 另行核验。
      const report = { schema: 'filmcraft-harness-native-candidate/v1', result: 'PASS', nodeVersion: process.version,
        scope: 'source candidate internal Node/SQLite adapter and actual Python workflow; not host, pinned install, quality or full Harness acceptance',
        sourceRevision, sourceTreeSha256: prepared.sourceTreeSha256, runtimeIdentity: prepared.runtimeIdentity,
        taskId: task.taskId, attemptId: made.attemptId, revisionAttemptId: revised.attemptId,
        createState: made.state, revisionState: revised.state, idempotentReuse: reused.reused,
        actualProjectSha256: originalHash, revisedProjectSha256: sha256(readFileSync(join(revisedOutput, 'project.fcproj'))),
        originalPreserved: true, outputParentAliasVerified: true, processesStopped: made.process?.stopped && revised.process?.stopped,
        receipts: db.receipts(task.taskId, made.attemptId!), publicArtifacts: receipt.outputRefs,
        publicTasks: [task, second].map(item => publicTask(db, item.taskId,
          { schemaVersion: 'filmcraft-native-workflow/v1', nativePlanHash: item.nativePlanHash },
          { currency: 'USD', maxMinorUnits: 0, maxRevisions: 1, maxExternalCalls: 0 })),
        recovery: { injected: 'receipt transfer lost after actual native export', inspection: diagnosed,
          state: repaired.state, attemptId: repaired.attemptId, recoveryId: repaired.recoveryId,
          replayed: repaired.replayed, readonlyFilesPreserved: true, nativeFilesPreserved: true,
          originalAttemptCount: db.listAttempts(lostTask.taskId).length, idempotentReuse: reusedLost.reused,
          intents: db.listRecoveryIntents(lostTask.taskId) },
        technicalAcceptance: receipt.technicalAcceptance, creativeAcceptance: receipt.creativeAcceptance,
        userAcceptance: receipt.userAcceptance, authScopeValidation: 'HOST_REQUIRED', budgetEnforcement: 'NOT_IMPLEMENTED' };
      writeFileSync(process.env.FILMCRAFT_HARNESS_REPORT, JSON.stringify(report, null, 2) + '\n');
    }
  });
