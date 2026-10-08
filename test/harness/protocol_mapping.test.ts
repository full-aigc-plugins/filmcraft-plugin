import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { publicTask } from '../../src/adapters/protocol_mapping.ts';
import { binding, workspace } from './fixtures.ts';

test('public task mapping uses registered identity and keeps internal fields in the domain ledger', t => {
  const root = workspace(t), db = new TaskLedger(join(root, 'ledger.sqlite')); t.after(() => db.close());
  const task = binding(root); db.register(task);
  const budget = { currency: 'USD', maxMinorUnits: 0, maxRevisions: 2, maxExternalCalls: 0 };
  const payload = { schemaVersion: 'filmcraft-native-workflow/v1', nativePlanHash: task.nativePlanHash };
  const mapped = publicTask(db, task.taskId, payload, budget);
  assert.equal(mapped.protocolVersion, 'craft-task/v1'); assert.equal(mapped.planHash, task.planHash);
  assert.equal(mapped.expectedRevision, null); assert.equal(mapped.deadline, new Date(task.deadline).toISOString());
  assert.equal(Object.hasOwn(mapped, 'namespace'), false); assert.equal(Object.hasOwn(mapped, 'sourceTreeSha256'), false);
  assert.deepEqual(mapped.runtimeIdentity, task.runtimeIdentity); assert.deepEqual(mapped.payload, payload);
  assert.throws(() => publicTask(db, 'missing', payload, budget), /task_missing/);
  assert.throws(() => publicTask(db, task.taskId, {}, budget), /payload_version_required/);
  assert.throws(() => publicTask(db, task.taskId, payload, { ...budget, maxRevisions: -1 }), /invalid_budget_mapping/);
  assert.equal(db.getTask(task.taskId).state, 'planned');
});
