#!/usr/bin/env python3
"""收集当前固定组合的分层证据；收集通过不等于缺失场景已通过。"""
import argparse
import hashlib
import json
from pathlib import Path,PurePosixPath
import re
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from release_evidence import LAYERS,trace_index,validate_checks,validate_trace
from verify_fixed_install import release_entry
ROOT=Path(__file__).resolve().parents[1]


def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def read(root,name):
 if not isinstance(name,str) or not name or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts:raise ValueError('evidence_path_invalid')
 root=Path(root).resolve(strict=True);path=root/name
 if not path.resolve().is_relative_to(root):raise ValueError('evidence_path_invalid')
 current=path
 while current!=root:
  if current.is_symlink():raise ValueError('evidence_path_invalid')
  current=current.parent
 try:data=path.read_bytes()
 except OSError as error:raise ValueError('evidence_missing') from error
 if len(data)>16*1024*1024:raise ValueError('evidence_too_large')
 return data


def verify_source_files(report,repository,commit,kind):
 if report.get('revision')!=commit or report.get('result')!='PASS':raise ValueError('source_report_identity_mismatch')
 prefixes=('scripts/','tests/','skills/','.github/') if kind=='source' else ('src/','scripts/','test/','tests/','.github/','openspec/')
 extras={'skill-suite.json','.claude-plugin/plugin.json'} if kind=='source' else {'package.json','plugin.json','skills.lock.json','docs/contracts-reference.json'}
 names=subprocess.check_output(['git','-C',str(repository),'ls-tree','-r','--name-only',commit],text=True).splitlines()
 wanted={name for name in names if name.startswith(prefixes) or name in extras}
 hashes=report.get('sourceFilesSha256',{})
 if set(hashes)!=wanted:raise ValueError('source_file_inventory_mismatch')
 for name,digest in hashes.items():
  data=subprocess.check_output(['git','-C',str(repository),'show',commit+':'+name])
  if sha(data)!=digest:raise ValueError('source_file_digest_mismatch')


def verify_check_logs(root,report):
 for check in report['checks']:
  if check.get('status')!='PASS' or 'log' in check and sha(read(root,check['log']))!=check['logSha256']:raise ValueError('check_log_changed_or_unexecuted')


def current_ci(repository,commit,workflow):
 result=json.loads(subprocess.check_output(['gh','run','list','--repo',repository,'--commit',commit,'--limit','30',
   '--json','databaseId,headSha,status,conclusion,workflowName,headBranch'],text=True))
 rows=[r for r in result if r['workflowName']==workflow]
 if not rows or any(r['headSha']!=commit or r['status']!='completed' or r['conclusion']!='success' for r in rows):raise ValueError('required_ci_not_complete_or_failed: '+workflow)
 for row in rows:
  detail=json.loads(subprocess.check_output(['gh','run','view',str(row['databaseId']),'--repo',repository,'--json','jobs,url'],text=True))
  if not detail['jobs'] or any(job['conclusion']!='success' for job in detail['jobs']):raise ValueError('required_ci_job_skipped_or_failed')
  row['url']=detail['url']
 return rows


def validate_current_inputs(source,source_ci,plugin_ci,host,native,capability,expected):
 source_report=json.loads(read(source_ci,'report.json'));plugin_report=json.loads(read(plugin_ci,'report.json'))
 verify_source_files(source_report,source,expected['skillSourceSha'],'source');verify_source_files(plugin_report,ROOT,expected['sha'],'plugin')
 policy=json.loads(subprocess.check_output(['git','-C',str(source),'show',expected['skillSourceSha']+':scripts/offline-test-policy.json']))
 rows=source_report.get('tests',[]);by_id={row['id']:row for row in rows};allowed={row['id']:row['reason'] for row in policy['environmentTests']}
 if len(rows)!=len(by_id) or not set(allowed).issubset(by_id) or any(by_id.get(name,{}).get('status')!='PASS' for name in policy['requiredTests']):raise ValueError('source_required_test_missing')
 if any(row['status'] not in ('PASS','NOT_RUN') or row['status']=='NOT_RUN' and allowed.get(row['id'])!=row.get('reason') for row in rows):raise ValueError('source_undeclared_skip')
 if {c['id'] for c in source_report['checks']}!={'metadata','links','resources-catalog-entry','offline-unit-scenario-contract-entry'} or len(source_report['checks'])!=4:raise ValueError('source_required_check_missing')
 validate_checks(plugin_report['checks']);verify_check_logs(source_ci,source_report);verify_check_logs(plugin_ci,plugin_report)
 host_report=json.loads(read(host,'host-receipt.json'));native_report=json.loads(read(native,'report.json'));cap_report=json.loads(read(capability,'report.json'))
 if host_report.get('result')!='PASS' or host_report.get('plugin')!=expected or host_report.get('loadingErrors')!=0:raise ValueError('host_current_identity_unconfirmed')
 if (native_report.get('result')!='PASS' or native_report.get('fixedPlugin')!=expected or not native_report.get('allInstalledFilesUnchanged')
   or native_report.get('testCounts',{}).get('skipped')!=0 or native_report.get('testCounts',{}).get('fail')!=0
   or native_report.get('native',{}).get('sourceRevision')!=expected['skillSourceSha']):raise ValueError('fixed_native_current_identity_unconfirmed')
 if cap_report.get('result')!='PASS' or cap_report.get('plugin')!=expected or not cap_report.get('installedFilesUnchanged'):raise ValueError('mode_current_identity_unconfirmed')
 for mode in ('headless','bridge'):
  if cap_report.get('modes',{}).get(mode,{}).get('reopen')!='PASS':raise ValueError('mode_reopen_unconfirmed')
 for name,digest in cap_report['artifacts'].items():
  if sha(read(capability,name))!=digest:raise ValueError('mode_artifact_changed')
 runtime=native_report['native']['runtimeIdentity']
 if runtime['pluginVersion']!=expected['version'] or cap_report['binding']['runtimeSha256']!=runtime['sha256'] or cap_report['binding']['sourceSha']!=expected['skillSourceSha']:raise ValueError('runtime_identity_mismatch')
 return source_report,plugin_report,host_report,native_report,cap_report


def verify(source,source_ci,plugin_ci,host,native,capability,ref,output,require_all=False):
 expected=release_entry(ROOT,ref)
 reports=validate_current_inputs(source,source_ci,plugin_ci,host,native,capability,expected)
 source_report,plugin_report,host_report,native_report,cap_report=reports
 ci={'source':current_ci('full-aigc-skills/filmcraft-skills',expected['skillSourceSha'],'Source offline contracts and distribution'),
     'plugin':current_ci('full-aigc-plugins/filmcraft-plugin',expected['sha'],'Skill snapshots and implementation units'),
     'documentation':current_ci('full-aigc-plugins/filmcraft-plugin',expected['sha'],'Documentation and specification integrity')}
 output=Path(output).absolute()
 if output.exists() or output.is_symlink():raise ValueError('release_output_exists')
 output.mkdir(parents=True,mode=0o700);(output/'logs').mkdir(mode=0o700);(output/'artifacts').mkdir(mode=0o700)
 identity={'pluginSha':expected['sha'],'skillSourceSha':expected['skillSourceSha'],'runtimeSha256':native_report['native']['runtimeIdentity']['sha256']}
 artifacts={}
 for name,root,report,logname in [('source',source_ci,source_report,'unittest.log'),('plugin',plugin_ci,plugin_report,'node.log'),
    ('host',host,host_report,None),('native',native,native_report,'native.log'),('modes',capability,cap_report,None)]:
  original_name='host-receipt.json' if name=='host' else 'report.json'
  data=read(root,original_name);path='artifacts/'+name+'.json';(output/path).write_bytes(data)
  log={'path':path,'sha256':sha(data)}
  if name in ('source','plugin'):
   for source_path in sorted(Path(root).rglob('*')):
    if not source_path.is_file():continue
    relative=str(source_path.relative_to(root));raw=read(root,relative);dest=output/'original'/name/relative
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
  if name=='modes':
   for relative in cap_report['artifacts']:
    raw=read(root,relative);dest=output/'original/modes'/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
  if logname:
   raw=read(root,logname);rawpath='logs/'+name+'-original.log';(output/rawpath).write_bytes(raw);log.update(rawPath=rawpath,rawSha256=sha(raw))
  artifacts[name]=log
 ci_data=encoded(ci);(output/'artifacts/ci.json').write_bytes(ci_data+b'\n');artifacts['ci']={'path':'artifacts/ci.json','sha256':sha(ci_data+b'\n')}
 groups=trace_index(ROOT);records=[];native_prefixes=('FC-AR-001-','FC-TX-002-','FC-TX-003-','FC-QA-001-','FC-QA-002-')
 for group in groups:
  for scenario in group['scenarios']:
   for layer in sorted(LAYERS):
    row={'scenario':scenario,'tasks':group['tasks'],'layer':layer,'identity':identity,'status':'NOT_RUN','executed':False,
         'reason':'No current independently sufficient evidence for this scenario at this layer; historical or aggregate totals do not promote it.',
         'host':'not-qualified','platform':'not-qualified','mode':'not-qualified'}
    proof=None
    if scenario.startswith('FC-RL-001-') and layer in ('source','ci'):
     proof='plugin' if layer=='source' else 'ci';row.update(host='python-unittest' if layer=='source' else 'github-actions',platform='linux-x86_64',mode='offline',
       expected='Mandatory layered gates and optimization trace rejection tests execute; no native promotion',actual='Current immutable CI artifacts and negative gates passed')
    elif layer=='fixed-install' and scenario.startswith(native_prefixes):
     proof='native';row.update(host=host_report['codexVersion'],platform=host_report['platform'],mode='headless',
       expected='Current installed regression verifies the named state/receipt/quality/revision boundary',actual='Installed test and implementation hashes unchanged; no skips; raw native/state log retained; bounded actual native plus explicitly synthetic state tests')
    elif layer=='fixed-install' and scenario.startswith('FC-RT-002-'):
     proof='modes';row.update(host=host_report['codexVersion'],platform=host_report['platform'],mode='headless+bridge',
       expected='Current capability and parameter/resource gates; native save/reopen in both declared modes',actual='Bounded current owned bridge/headless cases pass; controlled faults remain labeled; exhaustive commands and runtime upgrade NOT_RUN')
    elif scenario=='FC-RL-001-LAYERED-CI' and layer=='host':
     proof='host';row.update(host=host_report['codexVersion'],platform=host_report['platform'],mode='app-server-discovery',
       expected='Actual isolated current public tag install and 13 enabled skill discoveries with no load errors',actual='Actual app-server installation identity passed; model routing and other hosts remain NOT_RUN')
    if proof:
     row.pop('reason');row.update(status='PASS',executed=True,inputHashes={'evidenceInput':artifacts[proof]['sha256']},
       candidateSha256=native_report['native']['actualProjectSha256'] if proof=='native' else artifacts[proof]['sha256'])
     if proof=='native':row['inputHashes'].update({r['assetId']:r['sha256'] for r in native_report['native']['publicTasks'][0]['inputRefs']})
     if proof=='modes':row['inputHashes'].update({'nativeCases':cap_report['artifacts']['cases.json']})
     envelope={'identity':identity,**{key:row[key] for key in ('inputHashes','candidateSha256','host','platform','mode')},'artifact':artifacts[proof]}
     name='logs/'+sha(encoded([scenario,layer]))+'.json';data=encoded(envelope)+b'\n';(output/name).write_bytes(data)
     row['log']={'path':name,'sha256':sha(data),**{key:row[key] for key in ('identity','inputHashes','candidateSha256','host','platform','mode')}}
    records.append(row)
 counts=validate_trace(records,groups,identity,required_layers=LAYERS)
 for row in records:
  if row['status']=='NOT_RUN':continue
  envelope=json.loads(read(output,row['log']['path']))
  if sha(read(output,row['log']['path']))!=row['log']['sha256'] or any(envelope[key]!=row[key] for key in ('identity','inputHashes','candidateSha256','host','platform','mode')):raise ValueError('trace_log_changed')
  artifact=envelope['artifact']
  if sha(read(output,artifact['path']))!=artifact['sha256']:raise ValueError('trace_artifact_changed')
  if 'rawPath' in artifact and sha(read(output,artifact['rawPath']))!=artifact['rawSha256']:raise ValueError('trace_raw_log_changed')
 report={'schema':'filmcraft-layered-release-trace/v1','result':'PASS','scope':'collection integrity and explicit current layer results, not complete runtime/creative/V1 qualification',
   'identity':identity,'plugin':expected,'sourceCounts':source_report['counts'],'pluginNodeCounts':plugin_report['nodeCounts'],
   'fixedInstalledCounts':native_report['testCounts'],'index':groups,'records':records,'counts':counts,'ci':ci,
   'qualification':'NOT_PROVEN' if counts['notRun'] or counts['fail'] else 'PASS','realMedia':'NOT_RUN','fullV1':'INCOMPLETE',
   'otherHosts':'NOT_RUN','otherPlatforms':'NOT_RUN','completeCommandAcceptance':'NOT_PROVEN','creativeAcceptance':'manual_review','userAcceptance':'NOT_RUN',
   'artifacts':artifacts,'sourceFileManifestSha256':sha(encoded(source_report['sourceFilesSha256'])),
   'pluginFileManifestSha256':sha(encoded(plugin_report['sourceFilesSha256']))}
 (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 if require_all and report['qualification']!='PASS':raise ValueError('complete_release_not_qualified')
 return {'result':'PASS','qualification':report['qualification'],'counts':counts,'reportSha256':sha((output/'report.json').read_bytes())}


if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 for name in ('source','source-ci','plugin-ci','host','native','capability','output'):parser.add_argument('--'+name,type=Path,required=True)
 parser.add_argument('--ref',required=True);parser.add_argument('--require-all',action='store_true')
 print(json.dumps(verify(**vars(parser.parse_args()))))
