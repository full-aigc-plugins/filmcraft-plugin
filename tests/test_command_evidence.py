"""FC-CM-001：命令证据分维统计，目录发现不得升级执行或保全。"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommandEvidenceTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('command_evidence', ROOT / 'scripts/command_evidence.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.binding = {'pluginSha': 'a' * 40, 'sourceSha': 'b' * 40, 'runtimeSha256': 'c' * 64,
                        'runtimeVersion': '0.2.0-craft.4', 'platform': 'darwin-arm64', 'mode': 'headless'}
        self.rows = [{'id': 'example.edit', 'params': '{"time":ticks}', 'enabled': False},
                     {'id': 'example.inspect', 'params': '{}', 'enabled': True}]

    def build(self, observations=None, binding=None):
        return self.module.build(self.rows, self.binding,
            {'binding': binding or self.binding, 'observations': observations or []})

    def test_discovery_does_not_promote_other_dimensions(self):
        result = self.build()
        self.assertEqual(len(result['commands']), 2)
        for row in result['commands']:
            self.assertEqual(row['dimensions']['discovery']['status'], 'PASS')
            for dimension in self.module.DIMENSIONS[1:]:
                self.assertEqual(row['dimensions'][dimension]['status'], 'NOT_RUN')
        self.assertEqual(result['completeCommandAcceptance'], 'NOT_PROVEN')

    def test_positive_negative_and_persistence_are_independent(self):
        observation = {'command': 'example.edit', 'dimension': 'positiveExecution', 'status': 'PASS',
                       'evidence': 'actual-create', 'scope': 'actual command result, not persistence'}
        result = self.build([observation])
        row = result['commands'][0]['dimensions']
        self.assertEqual(row['positiveExecution']['status'], 'PASS')
        self.assertEqual(row['negativeRejection']['status'], 'NOT_RUN')
        self.assertEqual(row['reopen']['status'], 'NOT_RUN')
        self.assertEqual(result['summary']['positiveExecution']['PASS'], 1)
        self.assertEqual(result['summary']['reopen']['NOT_RUN'], 2)

    def test_stale_runtime_platform_mode_or_source_is_rejected(self):
        for field in self.binding:
            binding = dict(self.binding, **{field: 'other'})
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'command_evidence_binding_mismatch'):
                self.build(binding=binding)

    def test_unknown_command_dimension_and_duplicate_claim_are_rejected(self):
        valid = {'command': 'example.edit', 'dimension': 'reopen', 'status': 'PASS',
                 'evidence': 'actual-reopen', 'scope': 'native semantic comparison'}
        invalid = [dict(valid, command='invented'), dict(valid, dimension='all'),
                   dict(valid, dimension='discovery')]
        for claim in invalid:
            with self.subTest(claim=claim), self.assertRaisesRegex(ValueError, 'command_evidence_observation_invalid'):
                self.build([claim])
        with self.assertRaisesRegex(ValueError, 'command_evidence_duplicate_observation'):
            self.build([valid, valid])

    def test_pass_requires_evidence_and_not_applicable_requires_reason(self):
        valid = {'command': 'example.edit', 'dimension': 'parameterValidation', 'status': 'PASS',
                 'evidence': 'validation-case', 'scope': 'signed 64-bit tick fields only'}
        for claim in (dict(valid, evidence=''), dict(valid, scope=''), dict(valid, status='passed'),
                      dict(valid, status='N/A')):
            with self.subTest(claim=claim), self.assertRaisesRegex(ValueError, 'command_evidence_observation_invalid'):
                self.build([claim])

    def test_invalid_or_duplicate_discovery_rows_are_rejected(self):
        for rows in ([self.rows[0], self.rows[0]], [dict(self.rows[0], enabled='true')]):
            with self.subTest(rows=rows), self.assertRaisesRegex(ValueError, 'command_evidence_catalog_invalid'):
                self.module.build(rows, self.binding, {'binding': self.binding, 'observations': []})


if __name__ == '__main__':
    unittest.main()
