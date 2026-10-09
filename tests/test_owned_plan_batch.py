"""同一所属实例的连续计划、拒绝与权限身份边界。"""
import importlib.util
from pathlib import Path
import unittest


def module():
    spec = importlib.util.spec_from_file_location('owned_plan_test', Path(__file__).resolve().parents[1] / 'scripts/owned_empty_batch.py')
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class PlanBatchTests(unittest.TestCase):
    def test_successful_plan_can_continue_without_replacing_owner(self):
        class Commands:
            calls = 0
            def execute(self, *args, **kwargs):
                self.calls += 1
                return {'result': 'PASS', 'steps': []}
        commands = Commands()
        batch = module().OwnedBatch(commands, None, 'headless', '.', '.', None)
        batch.execute({'operations': []}, 'one')
        batch.execute({'operations': []}, 'two')
        self.assertEqual(commands.calls, 2)
        self.assertFalse(batch.tainted)

    def test_unknown_stops_continuous_plans(self):
        class Commands:
            calls = 0
            def execute(self, *args, **kwargs):
                self.calls += 1
                return {'result': 'unknown', 'error': 'outcome_unknown', 'steps': []}
        commands = Commands()
        batch = module().OwnedBatch(commands, None, 'headless', '.', '.', None)
        with self.assertRaisesRegex(RuntimeError, 'unexpected'):
            batch.execute({'operations': []}, 'one')
        with self.assertRaisesRegex(RuntimeError, 'batch_stopped'):
            batch.execute({'operations': []}, 'two')
        self.assertEqual(commands.calls, 1)

    def test_external_input_requires_startup_protection(self):
        class Commands:
            def execute(self, *args, **kwargs): raise AssertionError('must not execute')
        batch = module().OwnedBatch(Commands(), None, 'headless', '/owned-work', '.', None)
        with self.assertRaisesRegex(ValueError, 'external_input_not_protected'):
            batch.execute({'operations': []}, 'one', inputs={'source': '/external/original.fcproj'})
        self.assertTrue(batch.tainted)

    def test_policy_mutation_refused_before_execution(self):
        class Commands:
            def execute(self, *args, **kwargs): raise AssertionError('must not execute')
        policy = {'readRoots': ['original'], 'writeRoots': ['original']}
        batch = module().OwnedBatch(Commands(), None, 'headless', '.', '.', policy)
        policy['writeRoots'].append('expanded')
        with self.assertRaisesRegex(ValueError, 'batch_identity_changed'):
            batch.execute({'operations': []}, 'one')


if __name__ == '__main__': unittest.main()
