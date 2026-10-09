#!/usr/bin/env python3
"""固定安装公开入口的读取根与平台拒绝审计；平台覆盖为分支模拟，不是目标系统验收。"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--installed-plugin',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
I=args.installed_plugin.resolve(strict=True);R=args.output.resolve();R.mkdir(mode=0o700);rows=[]
def write(p,value):p.write_text(json.dumps(value)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for skill in sorted((I/'skills').iterdir()):
 if not skill.is_dir():continue
 root=R/skill.name;root.mkdir();allowed=root/'allowed';allowed.mkdir();outside=root/'outside';outside.mkdir();missing=allowed/'never-installed';destination=allowed/'never-output';readlink=root/'linked-root';readlink.symlink_to(allowed,target_is_directory=True)
 source=outside/'source';source.mkdir();(source/'manifest.json').write_text('not JSON');(source/'project.fcproj').write_text('not a project')
 sourceLink=allowed/'source-link';sourceLink.symlink_to(source,target_is_directory=True)
 manifestLink=allowed/'manifest-link';manifestLink.mkdir();(manifestLink/'manifest.json').symlink_to(source/'manifest.json');(manifestLink/'project.fcproj').write_text('not a project')
 projectLink=allowed/'project-link';projectLink.mkdir();(projectLink/'manifest.json').write_text('not JSON');(projectLink/'project.fcproj').symlink_to(source/'project.fcproj')
 workflow=allowed/'workflow.json';write(workflow,{'document':{'name':'Owned boundary','width':32,'height':32,'frameRate':{'num':12,'den':1}},'operations':[],'frames':[]})
 revision=allowed/'revision.json';write(revision,{'operations':[],'expectedProjectSha256':'0'*64,'frames':[]})
 commands=allowed/'commands.json';write(commands,{'schema':'craft-command-plan/v1','operations':[{'command':'project.inspect','params':{}}]})
 invalid=outside/'invalid.json';invalid.write_text('not JSON');rootFile=root/'not-directory';rootFile.write_text('owned fixture')
 snapshots={p: digest(p) for p in [source/'manifest.json',source/'project.fcproj',workflow,revision,commands,invalid]}
 def argv(entry,plan=None,extra=(),read=None):
  flags=['--runtime-home',str(missing),'--read-root',str(allowed) if read is None else read,'--write-root',str(allowed)]
  if entry=='workflow':return [str(skill/'scripts/workflow.py'),str(plan or workflow),'--output',str(destination),*flags,*extra]
  if entry in ('commands','desktop'):return [str(skill/'scripts'/(entry+'.py')),'run',str(plan or commands),'--output',str(destination),*flags,*extra]
  return [str(skill/'scripts/cli.py'),*flags,'--','exec','project.inspect','{}',*extra]
 def check(label,entry,arguments,error,platform=None):
  if platform:
   code='import argparse,importlib.util,json,pathlib,platform,runpy,shutil,tempfile,subprocess,sys;sys.platform=sys.argv[1];sys.argv=sys.argv[2:];runpy.run_path(sys.argv[0],run_name="__main__")'
   command=[sys.executable,'-I','-B','-c',code,platform,*arguments]
  else:command=[sys.executable,'-I','-B',*arguments]
  env=dict(os.environ);env.pop('FILMCRAFT_DATA_DIR',None)
  done=subprocess.run(command,capture_output=True,text=True,timeout=25,env=env);output=done.stdout+done.stderr
  log=root/(label+'-'+entry+('.'+platform if platform else '')+'.private.txt');log.write_text(output)
  assert done.returncode==1 and error in output,(skill.name,label,entry,platform,done.returncode,output)
  assert not missing.exists() and not destination.exists(),(skill.name,label,'side effect')
  assert str(outside) not in output and str(source) not in output
  assert all(digest(p)==before for p,before in snapshots.items())
  rows.append({'skill':skill.name,'entry':entry,'case':label,'result':'PASS','error':error,'beforeRuntimeInstallation':True,'outputCreated':False,'inputFixturesPreserved':True,'privateOutsidePathEchoed':False,'simulatedPlatform':platform,'logSha256':digest(log)})
 for label,path in [('source-outside',source),('source-link',sourceLink),('manifest-link',manifestLink),('project-link',projectLink)]:check(label,'workflow',argv('workflow',revision,extra=['--source',str(path)]),'permission_read_denied')
 for entry in ('workflow','commands','desktop'):check('outside-malformed-plan',entry,argv(entry,invalid),'permission_read_denied')
 for entry in ('commands','desktop'):check('outside-input',entry,argv(entry,extra=['--input','unused='+str(invalid)]),'permission_read_denied')
 check('outside-project','cli',argv('cli',extra=['--project',str(invalid)]),'permission_read_denied')
 for label,value in [('relative-root','owned-relative'),('symlink-root',str(readlink)),('broad-root','/Users'),('missing-root',str(root/'absent-root')),('file-root',str(rootFile))]:
  for entry in ('workflow','commands','desktop','cli'):check(label,entry,argv(entry,read=value),'invalid_execution_permissions')
 for platform in ('linux','win32'):
  for entry in ('workflow','commands','desktop','cli'):check('unsupported-platform',entry,argv(entry),'execution_isolation_unavailable',platform=platform)
 print(skill.name,'PASS',flush=True)
report={'schema':'filmcraft-installed-read-boundaries/v1','result':'PASS','pluginVersion':json.loads((I/'plugin.json').read_text())['version'],'sourceLockSha256':digest(I/'skills.lock.json'),'driverSha256':digest(Path(__file__)),'cases':rows,'scope':'Actual installed public entry preflight on macOS with malformed/outside inputs; unsupported-platform cases simulate sys.platform after importing standard dependencies. No native target Linux/Windows execution is claimed. Refusals precede installation and output creation.','fullFC_RL_002':'NOT_PROVEN'};write(R/'report.json',report);print(json.dumps({'result':'PASS','cases':len(rows)}))
