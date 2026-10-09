"""复验固定安装的模型维护拒绝与实际 macOS 沙箱；原始日志仅写到指定私有输出。"""
from pathlib import Path
import argparse,sys
import hashlib,importlib.util,json,os,socket,subprocess,threading
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--installed-plugin',required=True,type=Path)
parser.add_argument('--output',required=True,type=Path)
args=parser.parse_args()
I=args.installed_plugin.resolve(strict=True)
R=args.output.resolve();R.mkdir(mode=0o700)
PYTHON=sys.executable
plugin=json.loads((I/'plugin.json').read_text());lock=json.loads((I/'skills.lock.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cases=[]; sandbox=[]
for skill in sorted((I/'skills').iterdir()):
 if not skill.is_dir():continue
 root=R/skill.name;root.mkdir();data=root/'data';data.mkdir();outside=root/'outside';outside.mkdir();cache=root/'never-installed'
 base=[PYTHON,'-I','-B',str(skill/'scripts/cli.py'),'--runtime-home',str(cache),'--read-root',str(root),'--write-root',str(root)]
 valid=['exec','transcript.downloadModel','{"model":"whisper-tiny"}','--data-dir',str(data)]
 vectors=[('missing-flag',[],valid,'model_maintenance_required'),('wrong-command',['--model-maintenance'],['exec','file.newProject','{}','--data-dir',str(data)],'invalid_model_maintenance_request'),('extra-project',['--model-maintenance'],valid+['--project',str(outside/'p.fcproj')],'invalid_model_maintenance_request'),('extra-param',['--model-maintenance'],['exec','transcript.downloadModel','{"model":"whisper-tiny","token":"OWNED_CANARY"}','--data-dir',str(data)],'invalid_model_maintenance_request'),('duplicate-model',['--model-maintenance'],['exec','transcript.downloadModel','{"model":"whisper-tiny","model":"whisper-base"}','--data-dir',str(data)],'invalid_model_maintenance_request'),('invalid-model',['--model-maintenance'],['exec','transcript.downloadModel','{"model":"OWNED_CANARY"}','--data-dir',str(data)],'invalid_model_maintenance_request'),('relative-data',['--model-maintenance'],valid[:-1]+['relative'],'invalid_model_maintenance_request'),('missing-data',['--model-maintenance'],valid[:-1]+[str(root/'absent')],'model_maintenance_directory_required'),('ungranted-skill',['--model-maintenance'],valid[:-1]+[str(skill)],'permission_write_denied'),('protected-runtime',['--model-maintenance'],valid[:-1]+[str(root)],None)]
 # Separate runtime-protected vector requires an existing runtime root under the grant.
 runtime_protected=root/'runtime';runtime_protected.mkdir()
 vectors[-1]=('protected-runtime',['--model-maintenance'],valid[:-1]+[str(runtime_protected)],'model_maintenance_protected_directory')
 for label,flags,args,expected in vectors:
  argv=base.copy()
  if label=='protected-runtime':argv[argv.index(str(cache))]=str(runtime_protected)
  p=subprocess.run([*argv,*flags,'--',*args],capture_output=True,text=True,timeout=30)
  (root/(label+'.private.txt')).write_text(p.stdout+p.stderr)
  assert p.returncode==1 and json.loads(p.stdout)['error']==expected,(skill.name,label,p.stdout,p.stderr)
  assert 'OWNED_CANARY' not in p.stdout+p.stderr
  assert not cache.exists() and not list(data.iterdir()) and not list(runtime_protected.iterdir())
  cases.append({'skill':skill.name,'case':label,'result':'PASS','error':expected,'beforeInstallation':True,'canaryEchoed':False})
 spec=importlib.util.spec_from_file_location('permission_'+skill.name.replace('-','_'),skill/'scripts/execution_permissions.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 protected=root/'protected';protected.mkdir();(protected/'keep').write_text('owned protected fixture')
 forbidden=outside/'keep';forbidden.write_text('owned outside fixture')
 policy=helper.from_cli([str(data)],[str(data)])
 for platform in ['linux','win32']:
  try:helper.command([PYTHON,'-V'],policy,platform=platform)
  except ValueError as e:assert str(e)=='execution_isolation_unavailable'
  else:raise AssertionError('unsupported platform executed')
 server=socket.socket();server.bind(('127.0.0.1',0));server.listen();server.settimeout(0.2);port=server.getsockname()[1];stop=threading.Event()
 def accept():
  while not stop.is_set():
   try:conn,_=server.accept();conn.close()
   except socket.timeout:continue
 t=threading.Thread(target=accept);t.start()
 try:
  for maintenance in [False,True]:
   target=data/('maintenance' if maintenance else 'editing')
   code='''import json,socket,sys\nfrom pathlib import Path\nr={}\nfor label,path in [("allowed",sys.argv[1]),("outside",sys.argv[2]),("protected",sys.argv[3])]:\n try:Path(path).write_text("owned probe");r[label]=True\n except PermissionError:r[label]=False\ntry:\n s=socket.create_connection(("127.0.0.1",int(sys.argv[4])),timeout=1);s.close();r["network"]=True\nexcept OSError:r["network"]=False\nprint(json.dumps(r))'''
   cmd=helper.command([PYTHON,'-I','-B','-c',code,str(target),str(outside/'created'),str(protected/'created'),str(port)],policy,protected_roots=[str(protected)],model_maintenance=maintenance)
   p=subprocess.run(cmd,env=helper.child_environment(),capture_output=True,text=True,timeout=10)
   (root/('maintenance' if maintenance else 'editing')).with_suffix('.private.txt').write_text(p.stdout+p.stderr)
   assert p.returncode==0,(skill.name,p.stdout,p.stderr)
   result=json.loads(p.stdout);assert result=={'allowed':True,'outside':False,'protected':False,'network':maintenance},(skill.name,maintenance,result)
   sandbox.append({'skill':skill.name,'mode':'maintenance' if maintenance else 'editing','result':'PASS','observed':result,'unsupportedPlatformsRefused':['linux','win32'],'helperSha256':sha(skill/'scripts/execution_permissions.py')})
 finally:stop.set();t.join();server.close()
 assert (protected/'keep').read_text()=='owned protected fixture' and forbidden.read_text()=='owned outside fixture'
 print(skill.name,'PASS',flush=True)
report={'schema':'filmcraft-fixed-maintenance-boundaries/v1','result':'PASS','pluginVersion':plugin['version'],'sourceLockSha256':sha(I/'skills.lock.json'),'publicRefusals':cases,'actualSystemSandbox':sandbox,'scope':'Actual frozen installed public CLI pre-install refusals plus actual macOS sandbox child-process file/network probes using installed helpers; loopback only, no external request or model download. These probes supplement rather than replace existing actual native CLI/model evidence.','driverSha256':sha(Path(__file__)),'fullFC_RL_002':'NOT_PROVEN'}
(R/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'result':'PASS','publicRefusals':len(cases),'actualSandboxCases':len(sandbox)}))
