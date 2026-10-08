#!/usr/bin/env python3
"""固定宿主内逐场景验收产物合同；保留原字节与脱敏投影的区别。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NEGATIVE = {'missing-report-identity': 'unknown', 'wrong-native-hash': 'conflict',
 'wrong-inspection-hash': 'conflict', 'wrong-export-hash': 'conflict', 'lossy-native-substitute': 'conflict',
 'font-fidelity-promotion': 'conflict', 'effect-fidelity-promotion': 'conflict', 'omitted-export': 'conflict',
 'duplicate-export': 'conflict', 'broken-report': 'conflict', 'wrong-report-declaration': 'conflict', 'missing-report-file': 'stale'}
LINEAGE = {'actual-create-and-attempt-context', 'idempotent-no-native-replay', 'actual-candidate-digest-change',
 'same-kind-conflict-original-CAS', 'cross-attempt-relabel-with-same-PID', 'missing-execution-receipt',
 'legacy-missing-context', 'actual-command-v1-mapping', 'actual-failed-stage-v1-mapping', 'actual-partial-receipt-handoff-repair'}

def check(value, reason):
 if not value: raise ValueError(reason)

def digest(value):
 return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def contract(report):
 check(report.get('schema') == 'filmcraft-artifact-contract-native/v1' and report.get('result') == 'PASS'
       and report.get('originalsRestored') is True and report.get('nativeProjectPreserved') is True, 'artifact_originals_unconfirmed')
 check(report.get('technicalAcceptance') == 'NOT_RUN' and report.get('userAcceptance') == 'NOT_RUN'
       and report.get('fullV1') == 'INCOMPLETE', 'artifact_acceptance_promoted')
 lineage = report['lineage']; rows = lineage['cases']
 check(len(rows) == len(LINEAGE) and {r['case'] for r in rows} == LINEAGE
       and all(r['result'] == 'PASS' for r in rows), 'artifact_lineage_incomplete')
 check(lineage.get('inputPreserved') is True and lineage.get('originalProjectPreserved') is True
       and lineage.get('installedSkillUnchanged') is True, 'artifact_lineage_preservation_missing')
 check({r['kind'] for r in lineage['archived']} == {'command','delivery','failed-stage','output-execution'}
       and all(r.get('originalBytesPreserved') is True for r in lineage['archived']), 'artifact_original_CAS_missing')
 required = set(NEGATIVE) | {'actual-quality-receipt-lineage', 'actual-moved-source-relink', 'actual-missing-moved-dependency'}
 rows = report['cases']; names = [r['case'] for r in rows]
 check(len(names) == len(set(names)) and set(names) == required and all(r['result'] == 'PASS' for r in rows), 'artifact_cases_incomplete')
 rows = {r['case']:r for r in rows}
 for name, status in NEGATIVE.items():
  row = rows[name]
  check(row.get('status') == status and row.get('nativeProjectPreserved') is True
        and row.get('outputRefsCount') == 0, 'artifact_negative_not_refused:' + name)
 quality = rows['actual-quality-receipt-lineage']; request = quality['request']; receipt = quality['receipt']; evaluation = quality['evaluation']
 check(quality['state'] == 'verifying' and receipt['requestSha256'] == digest(request)
       and receipt['requestRef'] == quality['requestRef'] and receipt['context']['source'] == 'external-process'
       and receipt['context']['exitCode'] == 0 and receipt['context']['pid'] > 0
       and receipt['reviewer'] == request['criteria']['reviewer'], 'artifact_quality_identity_mismatch')
 subject = request['subject']; expected = lineage['observations'][0]; binding = quality['binding']
 check(subject['bindingSha256'] == digest(binding) and subject['candidateSha256'] == digest(subject['files'])
       and subject['executionSha256'] == digest({'attempt':quality['attempt'],'runtime':binding['runtimeIdentity'],
        'sourceRevision':binding['sourceRevision'],'sourceTreeSha256':binding['sourceTreeSha256']})
       and binding['sourceRevision'] == report['sourceRevision'] and binding['sourceTreeSha256'] == lineage['sourceTreeSha256']
       and binding['runtimeIdentity'] == report['runtimeIdentity']
       and binding['planHash'] == lineage['publicTasks'][0]['planHash']
       and binding['inputHashes'] == subject['inputHashes'], 'artifact_quality_binding_mismatch')
 check(subject['taskId'] == expected['taskId'] and subject['attemptId'] == expected['attemptId']
       and subject['projectSha256'] == subject['files']['project.fcproj']['sha256']
       and subject['projectSha256'] == rows['actual-moved-source-relink']['sourceProjectSha256']
       and all(re.fullmatch('[a-f0-9]{64}', subject[k]) for k in ('candidateSha256','bindingSha256','executionSha256')),
       'artifact_quality_subject_mismatch')
 check(all(rows[name].get('nativeProjectSha256') == subject['projectSha256'] for name in NEGATIVE), 'artifact_negative_project_mismatch')
 check(evaluation['engineeringAcceptance'] == 'PASS' and evaluation['dimensions']['decode']['status'] == 'PASS'
       and evaluation['userAcceptance'] == 'NOT_RUN' and evaluation['creativeAcceptance'] == 'manual_review', 'artifact_quality_promoted_or_missing')
 move = rows['actual-moved-source-relink']
 check(all(move.get(k) is True for k in ('originalPathsUnavailable','sourcePreserved','pixelsUnchanged','fullDecode'))
       and move['inputHashes'] == subject['inputHashes'] and move['collection']['status'] == 'linked'
       and move['collection']['outputRefs'], 'artifact_relocation_unconfirmed')
 missing = rows['actual-missing-moved-dependency']
 check(missing.get('refused') is True and missing.get('sourcePreserved') is True
       and missing.get('successfulDeliveryExists') is False, 'artifact_missing_dependency_accepted')
 check({task['taskId'] for task in report['publicTasks']} == {'create','artifact-move'}
       and len(report['publicArtifacts']) > 0, 'artifact_public_mapping_empty')
 for producer in ('create','artifact-move'):
  check({'project.fcproj','film.mp4','exchange-loss.json','native.json'}.issubset(
   {artifact['location'] for artifact in report['publicArtifacts'] if artifact['producerTaskId'] == producer}), 'artifact_public_outputs_missing')
 for artifact in report['publicArtifacts']:
  check(artifact['version'] == artifact['sha256'] and artifact['nativeProjectRef']['sha256']
        and artifact['lossReportRef']['sha256'] and artifact['producerTaskId']
        and all(dep['packaged'] for dep in artifact['dependencies']), 'artifact_public_mapping_incomplete')
 return {'FC-AR-001-P': ['actual-create-and-attempt-context','actual-moved-source-relink','actual-missing-moved-dependency'],
  'FC-AR-001-N': ['actual-candidate-digest-change'],
  'FC-AR-001-RECEIPT-LINEAGE': ['actual-command-v1-mapping','actual-failed-stage-v1-mapping','actual-quality-receipt-lineage'],
  'FC-AR-001-RECEIPT-MISMATCH': ['same-kind-conflict-original-CAS','cross-attempt-relabel-with-same-PID','missing-execution-receipt'],
  'FC-AR-001-LEGACY-MAPPING': ['legacy-missing-context','actual-partial-receipt-handoff-repair'],
  'FC-AR-002-P': ['actual-create-and-attempt-context','actual-quality-receipt-lineage'],
  'FC-AR-002-N': ['lossy-native-substitute','effect-fidelity-promotion'],
  'FC-AR-002-BOUND-LOSS-REPORT': list(NEGATIVE)}

def module(path, name):
 spec=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value

def verify(host, authority, ref, output, python, node, ffmpeg, ffprobe):
 fixed=module(ROOT/'scripts/verify_fixed_install.py','artifacts_fixed_install');expected=fixed.release_entry(ROOT,ref)
 receipt=json.loads((host/'host-receipt.json').read_text());directories=json.loads((host/'installed-directories.private.json').read_text())
 check(receipt['result']=='PASS' and receipt['plugin']==expected and set(directories)==set(expected['skills']), 'artifact_fixed_host_mismatch')
 helper,identity=fixed.owner_helper(authority);check(receipt['helper']==identity,'artifact_owner_mismatch')
 skill=Path(directories['filmcraft-use']).resolve();plugin=skill.parent.parent
 check(skill.is_relative_to((host/'host-config').resolve()),'artifact_host_escape')
 def unchanged():
  for name,path in directories.items():
   check(Path(path).resolve()==skill.parent/name,'artifact_installed_path_mismatch');helper.verify_installed_skill(path,expected)
  fixed.verify_code_files(plugin,expected['codeFilesSha256'])
 unchanged();check(not output.exists() and not output.is_symlink(),'artifact_output_exists');output.mkdir(mode=0o700)
 result=subprocess.run([node,str(plugin/'scripts/verify_artifact_contract.ts'),'--output',str(output/'work'),
  '--python',python,'--source',expected['skillSourceSha'],'--ffmpeg',ffmpeg,'--ffprobe',ffprobe],capture_output=True,text=True,timeout=1200)
 def safe(text):return text.replace(str(output.resolve()),'[TEST_ROOT]').replace(str(Path.home()),'[USER_HOME]')
 (output/'native-log.txt').write_text(safe(result.stdout+result.stderr))
 check(result.returncode==0,'artifact_fixed_native_failed: see native-log.txt')
 report=json.loads((output/'work/report.private.json').read_text());scenarios=contract(report)
 check(report['pluginVersion']==expected['version'] and report['sourceRevision']==expected['skillSourceSha'],'artifact_fixed_execution_identity_mismatch')
 protocol=module(ROOT/'scripts/validate_protocol_mapping.py','artifact_protocol').validate(output/'work/report.private.json',authority)
 unchanged();report.update(fixedPlugin=expected,host={'codexVersion':receipt['codexVersion'],'platform':receipt['platform'],'skillCount':len(directories)},
  allInstalledFilesUnchanged=True,scenarios=scenarios,protocolValidation=protocol,
  digestSemantics='Archived digests cover original private CAS bytes verified by the native producer. Redacted public projections are not the original bytes.')
 (output/'report.json').write_text(safe(json.dumps(report,ensure_ascii=False,indent=2))+'\n')
 return {'result':'PASS','scenarios':len(scenarios),'artifactCases':len(report['cases']),'lineageCases':len(report['lineage']['cases']),
  'installedSkillsUnchanged':len(directories),'protocolObjects':protocol['validated']}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('host','authority','output'):p.add_argument('--'+name,type=Path,required=True)
 for name in ('ref','python','node','ffmpeg','ffprobe'):p.add_argument('--'+name,required=True)
 print(json.dumps(verify(**vars(p.parse_args()))))
