#!/usr/bin/env python3
"""固定所有者schema正例与映射漂移负例，合成对象不升级为原生通过。"""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_protocol_mapping import validate


def verify(node,authority,output):
 output=Path(output)
 if output.exists() or output.is_symlink():raise ValueError('protocol_output_exists')
 output.mkdir(mode=0o700);fixture=output/'fixture.json'
 subprocess.run([node,str(Path(__file__).resolve().parent/'protocol_fixture.ts'),str(fixture)],check=True)
 good=validate(fixture,authority);original=json.loads(fixture.read_text());refused=[]
 for name in ('task-version','artifact-hash','runtime-identity'):
  value=copy.deepcopy(original)
  if name=='task-version':value['publicTasks'][0]['protocolVersion']='craft-task/v99'
  if name=='artifact-hash':value['publicArtifacts'][0]['sha256']='invalid'
  if name=='runtime-identity':del value['publicTasks'][0]['runtimeIdentity']['sha256']
  path=output/(name+'.json');path.write_text(json.dumps(value))
  try:validate(path,authority)
  except ValueError:refused.append(name)
  else:raise ValueError('protocol_drift_accepted: '+name)
 report={'result':'PASS','scope':'synthetic domain mapping and fixed owner schema regression; not native acceptance','mapping':good,'driftRefused':refused}
 (output/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report


if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--node',required=True);parser.add_argument('--authority',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
 print(json.dumps(verify(**vars(parser.parse_args()))))
