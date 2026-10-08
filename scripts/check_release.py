#!/usr/bin/env python3
"""插件源码强制检查：不把普通CI的环境跳过提升为安装／原生验收。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from release_evidence import validate_checks,trace_index,validate_workflow
ROOT=Path(__file__).resolve().parents[1]


def verify(authority,node,output):
 output=Path(output).absolute()
 if output.exists() or output.is_symlink():raise ValueError('output_exists')
 output.mkdir(parents=True,mode=0o700);checks=[]
 report={'schema':'filmcraft-plugin-source-checks/v1','result':'FAIL','layer':'source','scope':'source tests and fixed protocol mapping only; no native/host/platform acceptance',
         'revision':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'checks':checks,
         'native':'NOT_RUN','host':'NOT_RUN','realMedia':'NOT_RUN','platformAcceptance':'NOT_RUN'}
 tracked=subprocess.check_output(['git','-C',str(ROOT),'ls-files','--cached','--others','--exclude-standard','-z'])
 report['sourceFilesSha256']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(set(tracked.decode().split('\0')))
  if name and (ROOT/name).is_file() and (name.startswith(('src/','scripts/','test/','tests/','.github/','openspec/')) or name in ('package.json','plugin.json','skills.lock.json','docs/contracts-reference.json'))}
 def run(name,commands):
  chunks=[];passed=True
  for command in commands:
   result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True);chunks.append(result.stdout+result.stderr)
   if result.returncode:passed=False;break
  data='\n'.join(chunks).replace(str(ROOT),'[PLUGIN_ROOT]').replace(str(Path.home()),'[USER_HOME]')
  data=re.sub(r'(?:/private)?/var/folders/[^\s"\']+','[TEMP_PATH]',data);log=output/(name+'.log');log.write_text(data)
  check={'id':name,'status':'PASS' if passed else 'FAIL','executed':True,'commands':[[str(x).replace(str(ROOT),'[PLUGIN_ROOT]').replace(str(authority),'[AUTHORITY]').replace(str(output),'[OUTPUT]') for x in c] for c in commands],
         'log':log.name,'logSha256':hashlib.sha256(log.read_bytes()).hexdigest()};checks.append(check)
  if not passed:raise ValueError(name+'_failed')
  return data
 try:
  validate_workflow((ROOT/'.github/workflows/implementation.yml').read_text(),'scripts/check_release.py')
  run('metadata',[[sys.executable,'-I','-B','scripts/current_facts.py','--check'],[sys.executable,'-I','-B','scripts/validate_docs.py']])
  run('fixed-source',[[sys.executable,'-I','-B','scripts/vendor/skill_vendor.py','check']])
  python_log=run('python',[[sys.executable,'-m','unittest','discover','-s','tests','-v']])
  if not re.search(r'Ran [1-9][0-9]* tests',python_log) or re.search(r'\bskipped=|\.\.\. skipped',python_log):raise ValueError('required_python_skipped')
  node_log=run('node',[[node,'--test','--test-reporter=tap','--test-concurrency=1',*[str(x) for x in sorted((ROOT/'test/harness').glob('*.test.ts'))]]])
  counts={}
  for key in ('tests','pass','fail','skipped'):
   match=re.search(r'(?:# |ℹ )'+key+r' (\d+)',node_log)
   if not match:raise ValueError('node_counts_missing')
   counts[key]=int(match[1])
  # 三个原生/时序媒体/上一实际安装核心用例可在普通CI缺环境，但逐条保留NOT_RUN。
  allowed={'actual Python native workflow binds SQL attempts, preserves original project and does not repeat a completed attempt',
           'actual temporal/audio fixtures detect synchronization, per-channel clipping and decode failure',
           'the actual previous installed dev45 core refuses schema6 without editing current state'}
  observed=re.findall(r'^ok \d+ - (.*?) # SKIP(?: .*)?$',node_log,re.M)
  if counts['fail'] or counts['tests']<1 or counts['pass']+counts['skipped']!=counts['tests']:raise ValueError('node_test_gate_failed')
  if len(observed)!=counts['skipped'] or not set(observed).issubset(allowed):raise ValueError('undeclared_node_skip')
  report['nodeCounts']=counts;report['nodeEnvironmentNotRun']=observed
  run('protocol',[[sys.executable,'-I','-B','scripts/verify_protocol_gate.py','--node',node,'--authority',str(authority),'--output',str(output/'protocol')]])
  report['optimizationIndex']=trace_index(ROOT);validate_checks(checks);report['result']='PASS'
 except Exception as error:report['error']=str(error).replace(str(ROOT),'[PLUGIN_ROOT]')
 finally:(output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report


if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--authority',type=Path,required=True);parser.add_argument('--node',default='node');parser.add_argument('--output',type=Path,required=True)
 result=verify(**vars(parser.parse_args()));print(json.dumps({'result':result['result'],'node':result.get('nodeCounts'),'error':result.get('error')}));raise SystemExit(result['result']!='PASS')
