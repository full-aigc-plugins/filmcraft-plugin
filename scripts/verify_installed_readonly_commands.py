#!/usr/bin/env python3
"""固定安装的只读查询上下文验收；不把十五条查询升级为666命令完整验收。"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,os,subprocess,sys
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--installed-plugin',type=Path,required=True)
parser.add_argument('--runtime-home',type=Path,required=True)
parser.add_argument('--plugin-sha',required=True)
parser.add_argument('--source-sha',required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();I=args.installed_plugin.resolve(strict=True);S=I/'skills/filmcraft-use';R=args.output.resolve();R.mkdir(mode=0o700);runtime=args.runtime_home.resolve(strict=True)
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def skill(name):return load(S/'scripts'/(name+'.py'),'fixed_query_'+name)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
queries=['jobs.list','perf.stats','source.inspect','command.list','project.inspect','state.inspect','history.list','mediaCache.info','lut.list','presets.list','export.formats','export.queue.list','transcript.models','project.columns.list','project.viewPreset.list']
commands=skill('commands');catalog=commands.catalog();models=R/'models';models.mkdir();os.environ['FILMCRAFT_DATA_DIR']=str(models)
assert len(catalog['commands'])==666 and all(next(r for r in catalog['commands'] if r['id']==q)['params']=='{}' for q in queries)
projectbase=json.loads((S/'examples/commands-advanced.json').read_text())['operations'][:6]
results=[]
def inspect_queries(receipt,phase):
 assert receipt['result']=='PASS',receipt.get('error')
 found={s['command']:s['result'] for s in receipt['steps'] if s['command'] in queries}
 assert set(found)==set(queries)
 assert found['jobs.list']==[]
 assert isinstance(found['perf.stats']['decode'],dict)
 assert found['source.inspect']=={'item':None}
 actual={r['id']:r['params'] for r in found['command.list']};expected={r['id']:r['params'] for r in catalog['commands']}
 assert set(actual)==set(expected)
 assert all(actual[q]==expected[q] for q in queries)
 assert found['project.inspect']['dirty'] is False and found['project.inspect']['activeSequence'] is not None
 assert len(found['project.inspect']['root']['children'])==3
 assert found['state.inspect']['active_sequence']==found['project.inspect']['activeSequence']
 assert isinstance(found['history.list']['undo'],list) and found['history.list']['redo']==[]
 assert found['mediaCache.info']['policy']=='never' and found['mediaCache.info']['bytes']==0
 assert len(found['lut.list']['builtin'])>=1 and all('ref' in r for r in found['lut.list']['builtin'])
 assert len(found['presets.list']['presets'])>=1 and all('name' in r for r in found['presets.list']['presets'])
 assert any(r['id']=='h264' and r['video'] for r in found['export.formats'])
 assert found['export.queue.list']=={'items':[],'running':False}
 assert {r['id'] for r in found['transcript.models']['models']}=={'whisper-tiny','whisper-base','whisper-small'}
 assert all(r['installed'] is False for r in found['transcript.models']['models'])
 assert Path(found['transcript.models']['dir']).resolve()==models/'models'
 assert any(r['name']=='Name' and r['shown'] for r in found['project.columns.list']['available'])
 assert [r['slot'] for r in found['project.viewPreset.list']['presets']]==list(range(1,11))
 return found
helper_path=Path(__file__).with_name('owned_empty_batch.py');helper_hash=sha(helper_path)
shared=load(helper_path,'query_owned_batch')
for mode in ['headless','bridge']:
 root=R/mode;root.mkdir();policy=skill('execution_permissions').from_cli([str(R)],[str(root),str(runtime)])
 with shared.OwnedBatch(commands,skill('desktop_session'),mode,root,runtime,policy) as session:
  def execute(ops,out,inputs=None):
   plan={'schema':'craft-command-plan/v1','operations':ops};write(root/(out.name+'-plan.private.json'),plan)
   if session.owner is not None: session.reset(root/('reset-'+out.name))
   result=session.execute(plan,out,inputs=inputs)
   write(root/(out.name+'-receipt.private.json'),result)
   return result
  ops=projectbase+[{'command':'file.saveAs','params':{'path':{'$output':'before.fcproj'}}}]+[{'command':q,'params':{}} for q in queries]+[{'command':'file.saveAs','params':{'path':{'$output':'after.fcproj'}}}]
  out=root/'create';created=execute(ops,out);found=inspect_queries(created,'created')
  before=json.loads((out/'before.fcproj').read_text());after=json.loads((out/'after.fcproj').read_text())
  assert before['project']['name']==before['project']['root']['name']=='before'
  assert after['project']['name']==after['project']['root']['name']=='after'
  normalized=copy.deepcopy(after);normalized['project']['name']='before';normalized['project']['root']['name']='before';assert before==normalized
  source=out/'after.fcproj';sourcehash=sha(source)
  reopened=execute([{'command':'file.open','params':{'path':{'$ref':'original.path'}}}]+[{'command':q,'params':{}} for q in queries]+[{'command':'file.saveAs','params':{'path':{'$output':'roundtrip.fcproj'}}}],root/'reopen',inputs={'original':source})
  again=inspect_queries(reopened,'reopened');roundtrip=json.loads((root/'reopen/roundtrip.fcproj').read_text());roundtrip['project']['name']='after';roundtrip['project']['root']['name']='after';assert roundtrip==after and sha(source)==sourcehash
  refusals=[]
  for q in queries:
   plan={'schema':'craft-command-plan/v1','operations':[{'command':q,'params':{'UNDEFINED_QUERY_FIELD':'OWNED_QUERY_CANARY'}}]};pf=root/'invalid.json';write(pf,plan);destination=root/'forbidden';cache=root/'not-installed'
   done=subprocess.run([sys.executable,'-I','-B',str(S/'scripts/commands.py'),'run',str(pf),'--output',str(destination),'--runtime-home',str(cache),'--read-root',str(root),'--write-root',str(root)],capture_output=True,text=True,timeout=20)
   assert done.returncode==1 and json.loads(done.stdout)['error']=='invalid_native_parameters' and 'OWNED_QUERY_CANARY' not in done.stdout+done.stderr
   assert not destination.exists() and not cache.exists();refusals.append({'command':q,'error':'invalid_native_parameters','beforeInstallation':True})
  actualrows=found['command.list'];binding={'pluginSha':args.plugin_sha,'sourceSha':args.source_sha,'runtimeSha256':created['runtimeSha256'],'runtimeVersion':json.loads((S/'scripts/runtime.lock.json').read_text())['resolvedVersion'],'platform':sys.platform+'-arm64','mode':mode}
  observations=[]
  for q in queries:
   for dimension,scope in [('parameterValidation','Exact empty parameter object accepted in actual native context; unknown top-level field rejected before installation.'),('positiveExecution','Read-only result semantics asserted in populated two-color/two-clip project.'),('negativeRejection','Installed public adapter rejects undefined parameter without installation/output; native-context negatives remain outside this scope.'),('reopen','Query result semantics asserted after actual native project reopen.'),('nonTargetPreservation','Entire serialized project equal before/after and after reopen after only expected save-as project names normalized; original input hash preserved.')]:
    observations.append({'command':q,'dimension':dimension,'status':'PASS','evidence':'readonly-observations.json','scope':scope})
  matrix=load(Path(__file__).with_name('command_evidence.py'),'query_evidence').build(actualrows,binding,{'binding':binding,'observations':observations});write(root/'matrix.json',matrix)
  observation={'binding':binding,'queries':[{'command':q,'result':'PASS','createdResultSha256':digest(found[q]),'reopenedResultSha256':digest(again[q])} for q in queries],'parameterRefusals':refusals,'sourceProjectSha256':sourcehash,'projectPreserved':True,'normalization':'Only project.name and project.root.name, known native save-as filename behavior. No timeline/media/effect/settings normalization.','catalogContractDrift':[{'command':r['id'],'expected':next(e['params'] for e in catalog['commands'] if e['id']==r['id']),'actual':r['params']} for r in found['command.list'] if r['params']!=next(e['params'] for e in catalog['commands'] if e['id']==r['id'])],'modelCapabilityAvailable':found['transcript.models']['available'],'modelsRemainEmpty':not list(models.iterdir()),'ownedDesktopStopped':None,'rawCreateReceiptSha256':sha(root/'create-receipt.private.json'),'rawReopenReceiptSha256':sha(root/'reopen-receipt.private.json'),'desktopSha256':session.identity['binarySha256'] if mode=='bridge' else None}
  write(root/'readonly-observations.json',observation);results.append({'mode':mode,'result':'PASS','queries':len(queries),'nativeQueryCalls':len(queries)*2,'matrixSha256':sha(root/'matrix.json'),'observationsSha256':sha(root/'readonly-observations.json')});print(mode,'PASS15 queries,15 reopened,15 refusals',flush=True)
 proof=json.loads((root/'owned-batch-session.private.json').read_text())
 assert proof['sessionsStarted']==1 and proof['singleProcessIdentity'] and proof['ownedProcessesStopped'] and not proof['tainted']
 if mode=='bridge': assert proof['desktopStopped'] and proof['listenerOwnedByPID']
 observation['ownedDesktopStopped']=proof['desktopStopped']
 write(root/'readonly-observations.json',observation)
 results[-1]['observationsSha256']=sha(root/'readonly-observations.json')
 results[-1]['sessionProofSha256']=sha(root/'owned-batch-session.private.json')
assert sha(helper_path)==helper_hash,'QA helper changed during verification'
write(R/'report.json',{'schema':'filmcraft-readonly-command-contexts/v1','result':'PASS','driverSha256':sha(Path(__file__)), 'sessionHelperSha256':helper_hash,'results':results,'fullCommandAcceptance':'NOT_PROVEN','remainingTask':'8.3','scope':'Fifteen read-only commands in two contexts, separate six-dimension matrices over all666rows; other commands unexecuted in this audit. No GUI gesture, visual creative quality or ASR inference claim.'})
