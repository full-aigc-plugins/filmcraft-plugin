"""逐场景验收门禁自身不得接受删行、身份拼接或接受状态升级。"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ArtifactContractTests(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('artifact_gate_test',ROOT/'scripts/verify_fixed_artifacts.py')
  self.gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.gate)
  self.report=json.loads((ROOT/'docs/evidence/filmcraft59-artifact-candidate-20261009/report.json').read_text())
  # 公共证据已脱敏，单元夹具明确重建自己的路径身份，不冒充原始私有字节。
  quality=next(r for r in self.report['cases'] if r['case']=='actual-quality-receipt-lineage')
  quality['binding']['outputRoot']='synthetic-test-output'
  quality['request']['subject']['bindingSha256']=self.gate.digest(quality['binding'])
  quality['receipt']['requestSha256']=self.gate.digest(quality['request'])
 def test_all_eight_scenarios_require_actual_assertion_rows(self):
  self.assertEqual(len(self.gate.contract(self.report)),8)
 def test_every_required_row_and_duplicate_is_rejected(self):
  for group in ('cases','lineage'):
   rows=self.report['cases'] if group=='cases' else self.report['lineage']['cases']
   for index in range(len(rows)):
    report=copy.deepcopy(self.report)
    target=report['cases'] if group=='cases' else report['lineage']['cases'];target.pop(index)
    with self.assertRaises(ValueError):self.gate.contract(report)
   report=copy.deepcopy(self.report);target=report['cases'] if group=='cases' else report['lineage']['cases'];target.append(target[0])
   with self.assertRaises(ValueError):self.gate.contract(report)
 def test_false_negatives_relocation_and_missing_dependency_cannot_pass(self):
  for case in self.report['cases']:
   fields=['status','nativeProjectPreserved','nativeProjectSha256','outputRefsCount'] if case['case'] in self.gate.NEGATIVE else (
    ['originalPathsUnavailable','sourcePreserved','pixelsUnchanged','fullDecode'] if case['case']=='actual-moved-source-relink' else (
    ['refused','sourcePreserved','successfulDeliveryExists'] if case['case']=='actual-missing-moved-dependency' else []))
   for key in fields:
    report=copy.deepcopy(self.report);row=next(r for r in report['cases'] if r['case']==case['case'])
    row[key]=not row[key] if isinstance(row[key],bool) else 'unverified'
    with self.assertRaises(ValueError):self.gate.contract(report)
 def test_quality_binding_and_public_artifacts_are_rechecked(self):
  for key in ['taskId','attemptId','projectSha256','candidateSha256','bindingSha256','executionSha256']:
   report=copy.deepcopy(self.report);quality=next(r for r in report['cases'] if r['case']=='actual-quality-receipt-lineage')
   quality['request']['subject'][key]='0'*64
   with self.assertRaises(ValueError):self.gate.contract(report)
  for mutate in [lambda r:r.update(publicArtifacts=[]),lambda r:r.update(technicalAcceptance='PASS'),
                 lambda r:r.update(originalsRestored=False),lambda r:r['publicArtifacts'][0].update(version='0'*64)]:
   report=copy.deepcopy(self.report);mutate(report)
   with self.assertRaises(ValueError):self.gate.contract(report)

if __name__=='__main__':unittest.main()
