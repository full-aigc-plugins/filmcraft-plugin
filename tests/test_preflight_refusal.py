"""预检拒绝必须指出安全差异，不回显任意原生文本或本地资源路径。"""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('preflight_refusal', Path(__file__).resolve().parents[1] / 'scripts/native_preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class RefusalTests(unittest.TestCase):
    def test_identity_difference_retains_observed_and_expected(self):
        value = preflight.refusal_diagnostic(ValueError('capability_identity_mismatch: runtimeVersion'),
            {'mode': 'headless', 'runtime': {'version': '0.2.0-craft.5', 'platform': 'darwin-arm64'}},
            {'runtimeVersion': '0.2.0-craft.4'})
        self.assertEqual((value['subject'], value['status'], value['expected'], value['observed']),
                         ('runtimeVersion', 'mismatch', '0.2.0-craft.4', '0.2.0-craft.5'))

    def test_command_drift_reports_hashes_without_parameter_text(self):
        value = preflight.refusal_diagnostic(ValueError('capability_contract_drift: clip.trim'),
            {'commands': [{'id': 'clip.trim', 'expectedParametersSha256': 'a' * 64,
                           'observedParametersSha256': 'b' * 64, 'params': '/private/unrelated'}]}, {})
        self.assertEqual((value['expected'], value['observed']), ('a' * 64, 'b' * 64))
        self.assertNotIn('/private', str(value))

    def test_unknown_paths_and_untrusted_snapshot_values_are_redacted(self):
        value = preflight.refusal_diagnostic(ValueError('capability_unknown: model:/private/secret/model'),
            {'runtime': {'version': '/private/secret', 'binarySha256': 'not-a-hash'}}, {})
        self.assertEqual(value['subject'], 'redacted')
        self.assertIsNone(value['snapshot']['runtimeVersion'])
        self.assertIsNone(value['snapshot']['runtimeSha256'])
        self.assertNotIn('/private', str(value))
