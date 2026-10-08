"""恢复合同证据必须覆盖每个场景；历史报告仅作为校验器单元输入。"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


class RecoveryContractTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('recovery_contract_tested', ROOT / 'scripts/verify_recovery_contract.py')
        self.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.verifier)
        self.report = json.loads((ROOT / 'docs/evidence/filmcraft48-fixed-recovery-20261008/fixed-acceptance.json').read_text())

    def test_all_ten_contract_scenarios_map_to_actual_assertion_rows(self):
        value = self.verifier.contract(self.report)
        self.assertEqual(len(value), 10)
        self.assertTrue(all(row['status'] == 'PASS' and row['matrixRows'] for row in value.values()))

    def test_missing_or_duplicate_rows_and_changed_original_bytes_are_rejected(self):
        for index in range(len(self.report['matrix'])):
            value = copy.deepcopy(self.report)
            value['matrix'].pop(index)
            with self.assertRaises(ValueError):
                self.verifier.contract(value)
        value = copy.deepcopy(self.report)
        value['matrix'].append(value['matrix'][0])
        with self.assertRaises(ValueError): self.verifier.contract(value)
        value = copy.deepcopy(self.report)
        row = next(x for x in value['matrix'] if x['scenario'] == 'repeat-repair')
        row['after']['user-file'] = '0' * 64
        with self.assertRaises(ValueError): self.verifier.contract(value)

    def test_counts_replay_fences_processes_backups_and_continuation_are_required(self):
        cases = [lambda r: r['testCounts'].update(skipped=1),
                 lambda r: r.update(allInstalledFilesUnchanged=False)]
        mutations = [('actual-native-repair-and-continuation', 'originalReplayed', True),
                     ('actual-native-repair-and-continuation', 'nativeAfter', {}),
                     ('actual-native-repair-and-continuation', 'childAttempts', []),
                     ('two-recovery-executors', 'results', ['APPLIED', 'APPLIED']),
                     ('expired-recovery-owner', 'currentEpoch', 0),
                     ('host-exited-child-alive', 'occupancy', 0),
                     ('inspection-concurrent-write', 'refused', 'ignored'),
                     ('schema1-upgrade-rollback', 'logicalAfterSha256', '0' * 64),
                     ('schema2-upgrade-rollback', 'manifest', {}),
                     ('expired-revoked-authorization', 'errors', []),
                     ('actual-previous-version-downgrade-refusal', 'error', 'ignored')]
        for name, key, changed in mutations:
            def change(r, name=name, key=key, changed=changed):
                next(x for x in r['matrix'] if x['scenario'] == name)[key] = changed
            cases.append(change)
        for mutate in cases:
            value = copy.deepcopy(self.report); mutate(value)
            with self.assertRaises(ValueError): self.verifier.contract(value)

    def test_cli_consumes_the_documented_report_argument_and_rejects_mutable_refs(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'contract.json'
            result = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'scripts/verify_recovery_contract.py'),
                '--report', str(ROOT / 'docs/evidence/filmcraft48-fixed-recovery-20261008/fixed-acceptance.json'),
                '--ref', 'main', '--output', str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('immutable_filmcraft_ref_required', result.stderr)
            self.assertFalse(output.exists())
