"""批量负向验收的生命周期与未知结果回归。"""
import importlib.util
from pathlib import Path
import unittest


def module():
    path = Path(__file__).resolve().parents[1] / 'scripts/owned_empty_batch.py'
    spec = importlib.util.spec_from_file_location('empty_batch_test', path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class LifecycleTests(unittest.TestCase):
    def test_borrow_does_not_close_owner(self):
        class Owner:
            closed = False
            def close(self): self.closed = True
        owner = Owner()
        with module().BorrowedSession(owner) as borrowed:
            self.assertIs(borrowed, owner)
        self.assertFalse(owner.closed)

    def test_only_expected_precondition_failure_allows_next_case(self):
        check = module().expected_refusal
        self.assertTrue(check({'result': 'FAIL', 'error': 'precondition_failed: timeline.nudgeLeft',
                              'steps': [{'state': 'blocked'}]}))
        for receipt in ({'result': 'unknown'}, {'result': 'PASS'},
                        {'result': 'FAIL', 'error': 'outcome_unknown', 'steps': [{'state': 'unknown'}]}):
            self.assertFalse(check(receipt))


class StopTests(unittest.TestCase):
    def test_tainted_batch_never_creates_replacement_session(self):
        batch = module().EmptyBatch(None, None, 'headless', '.', '.', None)
        batch.tainted = True
        with self.assertRaisesRegex(RuntimeError, 'batch_stopped'):
            batch.execute({'operations': []}, 'unused')
        self.assertEqual(batch.started, 0)
        self.assertIsNone(batch.owner)

    def test_actual_unknown_receipt_taints_batch_and_stops_next_request(self):
        class Commands:
            calls = 0
            def catalog(self): return {'commands': [{'id': 'timeline.nudgeLeft', 'enabledAtEmptySession': False}]}
            def execute(self, *args, **kwargs):
                self.calls += 1
                return {'result': 'unknown', 'error': 'outcome_unknown', 'steps': [{'state': 'unknown'}]}
        commands = Commands()
        batch = module().EmptyBatch(commands, None, 'headless', '.', '.', None)
        plan = {'operations': [{'command': 'timeline.nudgeLeft'}]}
        with self.assertRaisesRegex(RuntimeError, 'unexpected_empty_batch_result'):
            batch.execute(plan, 'unused')
        self.assertTrue(batch.tainted)
        with self.assertRaisesRegex(RuntimeError, 'batch_stopped'):
            batch.execute(plan, 'unused-again')
        self.assertEqual(commands.calls, 1)
        self.assertEqual(batch.started, 0)

    def test_enabled_command_is_rejected_before_installation(self):
        class Commands:
            def catalog(self): return {'commands': [{'id': 'file.newProject', 'enabledAtEmptySession': True}]}
        batch = module().EmptyBatch(Commands(), None, 'headless', '.', '.', None)
        with self.assertRaisesRegex(ValueError, 'requires_disabled'):
            batch.execute({'operations': [{'command': 'file.newProject'}]}, 'unused')
        self.assertEqual(batch.started, 0)


if __name__ == '__main__': unittest.main()
