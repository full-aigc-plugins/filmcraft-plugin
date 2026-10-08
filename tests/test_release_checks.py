"""分层CI门禁负例不替代固定安装验收。"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

class ReleaseGateTests(unittest.TestCase):
 def test_required_ci_uses_mandatory_release_entry_and_protocol_mapping(self):
  workflow=(ROOT/'.github/workflows/implementation.yml').read_text()
  self.assertIn('scripts/check_release.py',workflow)
  self.assertNotIn('hashFiles',workflow)
  self.assertNotIn('continue-on-error',workflow)
  from release_evidence import validate_workflow
  validate_workflow(workflow,'scripts/check_release.py')
  for bad in (workflow.replace('    runs-on:',"    if: hashFiles('package.json') != ''\n    runs-on:"),workflow.replace('run: python3 -I -B scripts/check_release.py','run: true')):
   with self.assertRaises(ValueError):validate_workflow(bad,'scripts/check_release.py')
 def test_skipped_required_gate_or_wrong_source_identity_cannot_pass(self):
  from release_evidence import validate_checks
  rows=[{'id':name,'status':'PASS','executed':True} for name in ('python','node','fixed-source','metadata','protocol')]
  validate_checks(rows)
  for change in ('missing','skip','not-executed','duplicate'):
   value=copy.deepcopy(rows)
   if change=='missing':value.pop()
   if change=='skip':value[0]['status']='NOT_RUN'
   if change=='not-executed':value[1]['executed']=False
   if change=='duplicate':value.append(value[0])
   with self.subTest(change=change),self.assertRaises(ValueError):validate_checks(value)
 def test_optimization_index_comes_from_current_specs_and_tasks(self):
  from release_evidence import trace_index
  groups=trace_index(ROOT);self.assertEqual(len(groups),11)
  self.assertIn('FC-RL-001-LAYERED-CI',{s for g in groups for s in g['scenarios']})
 def test_missing_scenario_stale_log_and_unexecuted_host_are_rejected(self):
  from release_evidence import validate_trace
  identity={'pluginSha':'a'*40,'skillSourceSha':'b'*40,'runtimeSha256':'c'*64}
  groups=[{'scenarios':['FC-TEST-001-CASE'],'tasks':['9.1','9.2','9.3']}]
  row={'scenario':'FC-TEST-001-CASE','layer':'host','status':'PASS','identity':identity,'executed':True,
       'host':'test-host','platform':'darwin-arm64','mode':'headless','inputHashes':{'input':'d'*64},'candidateSha256':'e'*64,
       'expected':'host discovers current plugin','actual':'discovered','log':{'identity':identity,'sha256':'f'*64,'path':'host.log'}}
  row['log'].update(candidateSha256=row['candidateSha256'],inputHashes=row['inputHashes'],host=row['host'],platform=row['platform'],mode=row['mode'])
  validate_trace([row],groups,identity)
  for change in ('missing','log','candidate-log','input-log','unexecuted','identity','platform','media'):
   value=copy.deepcopy([row])
   if change=='missing':value=[]
   if change=='log':value[0]['log']['identity']['pluginSha']='0'*40
   if change=='candidate-log':value[0]['log']['candidateSha256']='0'*64
   if change=='input-log':value[0]['log']['inputHashes']={'input':'0'*64}
   if change=='unexecuted':value[0]['executed']=False
   if change=='identity':value[0]['identity']['skillSourceSha']='0'*40
   if change=='platform':value[0]['platform']=''
   if change=='media':value[0]['layer']='real-media';value[0]['mediaProvenance']='synthetic'
   with self.subTest(change=change),self.assertRaises(ValueError):validate_trace(value,groups,identity)
  value=copy.deepcopy(row);value.update(status='NOT_RUN',executed=False,reason='no current host observation');value.pop('log')
  validate_trace([value],groups,identity)

 def test_layer_collector_rejects_stale_file_manifest_and_missing_raw_logs(self):
  from collect_release_layers import verify_source_files,verify_check_logs,read
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'unit.log').write_text('actual test output')
   import hashlib
   digest=hashlib.sha256((root/'unit.log').read_bytes()).hexdigest()
   report={'checks':[{'id':'python','status':'PASS','log':'unit.log','logSha256':digest}]}
   verify_check_logs(root,report)
   (root/'unit.log').write_text('changed candidate log')
   with self.assertRaises(ValueError):verify_check_logs(root,report)
   with self.assertRaises(ValueError):read(root,'../outside')
   (root/'unit.log').unlink()
   with self.assertRaises(ValueError):verify_check_logs(root,report)
   with self.assertRaises(ValueError):verify_source_files({'revision':'old','result':'PASS'},ROOT,'a'*40,'plugin')
