"""固定准入报告不可用候选版本、缺失场景或计数替代。"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fixed_admission', ROOT / 'scripts/verify_fixed_admission.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


class FixedAdmissionTests(unittest.TestCase):
    def test_exact_candidate_observations_validate_only_their_original_identity(self):
        report = json.loads((ROOT / 'docs/evidence/filmcraft55-admission-candidate-20261009/report.json').read_text())
        expected = {'version': report['pluginVersion'], 'skillSourceSha': report['sourceRevision'],
                    'skills': {'filmcraft-use': report['skillSha256']}}
        module.validate_report(report, expected)
        with self.assertRaisesRegex(ValueError, 'identity_or_cases'):
            module.validate_report(report, {**expected, 'version': 'foreign'})
        edits = [lambda r: r['cases'].pop(), lambda r: r.update(installedSkillPreserved=False),
                 lambda r: r['cases'][0].update(outputExists=True),
                 lambda r: r['cases'][1].update(stopped=False),
                 lambda r: r['cases'][2].update(attempts=2),
                 lambda r: r['cases'][5].update(nativeLaunched=True),
                 lambda r: r['cases'][6].update(sourcePreserved=False),
                 lambda r: r.update(fullV1='PASS')]
        for edit in edits:
            value = copy.deepcopy(report); edit(value)
            with self.assertRaises(ValueError): module.validate_report(value, expected)


if __name__ == '__main__': unittest.main()
