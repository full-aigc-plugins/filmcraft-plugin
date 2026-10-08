#!/usr/bin/env python3
"""固定旧核心与当前源码／安装副本的实际运行时切换验收；输出包含私有路径，不直接公开。"""
import argparse,hashlib,json,struct,subprocess,time,zlib
from pathlib import Path
parser=argparse.ArgumentParser(description='实际运行时版本切换、独立原生交付、回退及拒绝场景；不代替固定安装资格。')
for key in ['output','previous-core','node','python','ffmpeg']:parser.add_argument('--'+key,required=True)
parser.add_argument('--runtime-home')
parser.add_argument('--require-diagnostics', action='store_true')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1];WORK=Path(args.output).absolute()
if WORK.exists() or WORK.is_symlink():raise ValueError('runtime_transition_output_exists')
WORK.mkdir(mode=0o700)
NODE=str(Path(args.node).resolve(strict=True));PYTHON=str(Path(args.python).resolve(strict=True))
CLI=ROOT/'src/cli/runtime.ts'; RUNTIME=Path(args.runtime_home).absolute() if args.runtime_home else WORK/'runtime'; LEDGER=WORK/'state.sqlite'; GRANTS=WORK/'grants';GRANTS.mkdir(mode=0o700)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(argv,stdin=None,expect=0):
 p=subprocess.run([str(x) for x in argv],input=stdin,cwd=ROOT,capture_output=True,text=True,timeout=240)
 if p.returncode!=expect:raise RuntimeError(json.dumps({'argv':[str(x) for x in argv],'exit':p.returncode,'out':p.stdout[-5000:],'err':p.stderr[-3000:]}))
 return json.loads(p.stdout)
def nodejs(code,*args):return run([NODE,'--input-type=module','-',*args],code)
nodejs("import {TaskLedger} from './src/harness/task_ledger.ts';const db=new TaskLedger(process.argv[2]);db.close();console.log('{}');",LEDGER)
image=WORK/'still.png'
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
image.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',32,32,8,6,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+bytes([239,91,54,255])*32)*32))+chunk(b'IEND',b''))
plan=json.loads((ROOT/'skills/filmcraft-use/examples/native-workflow.json').read_text());plan['assets']={'still':{'path':str(image),'sha256':sha(image)}}
PLAN=WORK/'plan.json';PLAN.write_text(json.dumps(plan))
oldroot=Path(args.previous_core).resolve(strict=True);oldskill=oldroot/'skills/filmcraft-use'
if json.loads((oldroot/'plugin.json').read_text())['version']!='0.1.0-dev.45':raise ValueError('previous_fixed45_required')
oldlock=json.loads((oldroot/'skills.lock.json').read_text());newlock=json.loads((ROOT/'skills.lock.json').read_text())
GRANT_REF='owned-runtime-upgrade61';SCOPE=hashlib.sha256(str(WORK).encode()).hexdigest();subjects=[]
def grant(subject):
 h=hashlib.sha256(json.dumps(subject,separators=(',',':'),sort_keys=True).encode()).hexdigest();subjects.append(h)
 p=GRANTS/(hashlib.sha256(GRANT_REF.encode()).hexdigest()+'.json')
 p.write_text(json.dumps({'schema':'filmcraft-local-authorization/v1','authorizationRef':GRANT_REF,'authorizationScopeSha256':SCOPE,'subjects':subjects,'expiresAt':int(time.time()*1000)+1800000,'revoked':False}));p.chmod(0o600)
def candidate(skill,source,name):
 tree=nodejs("import {fingerprintSkill} from './src/adapters/python_workflow.ts';console.log(JSON.stringify({sha:fingerprintSkill(process.argv[2])}));",skill)['sha']
 p=WORK/(name+'.candidate.json');p.write_text(json.dumps({'schema':'filmcraft-runtime-candidate/v1','skillDirectory':str(skill),'sourceRevision':source,'sourceTreeSha256':tree}));return p,tree
OLD,OLD_TREE=candidate(oldskill,oldlock['sources'][0]['sha'],'old');NEW,NEW_TREE=candidate(ROOT/'skills/filmcraft-use',newlock['sources'][0]['sha'],'new')
flags=['--ledger',LEDGER,'--runtime-home',RUNTIME,'--plan',PLAN,'--python',PYTHON]
auth=['--authorization-root',GRANTS,'--authorization-ref',GRANT_REF,'--authorization-scope-sha256',SCOPE]
phases=[]
def select(c,name,generation=None):
 args=[*flags,'--candidate',c]
 s=run([NODE,CLI,'probe-subject',*args]);grant(s)
 measured=run([NODE,CLI,'probe',*args,*auth]);proof=WORK/(name+'.probe.json');proof.write_text(json.dumps(measured))
 extra=['--generation',str(generation)] if generation else []
 subject=run([NODE,CLI,'subject',*args,'--probe',proof,*extra]);grant(subject)
 result=run([NODE,CLI,'rollback' if generation else 'activate',*args,'--probe',proof,*extra,*auth])
 phases.append({'name':name,'probe':measured,'subject':subject,'result':result});return result
old=select(OLD,'old');assert old['generation']==1
oldversion=old['descriptor']['runtimeIdentity']['cliVersion']; oldbinary=RUNTIME/'filmcraft'/oldversion/'filmcraft-cli';oldbinarysha=sha(oldbinary)
new=select(NEW,'new');assert new['generation']==2;newversion=new['descriptor']['runtimeIdentity']['cliVersion'];assert oldversion!=newversion
prepared=nodejs("import {TaskLedger} from './src/harness/task_ledger.ts';import{PythonWorkflowRunner}from'./src/adapters/python_workflow.ts';import{binding}from'./test/harness/fixtures.ts';import{readFileSync}from'node:fs';import{join}from'node:path';const root=process.argv[2],db=new TaskLedger(join(root,'state.sqlite'));const lock=JSON.parse(readFileSync('skills.lock.json','utf8')),manifest=JSON.parse(readFileSync('plugin.json','utf8'));const runner=new PythonWorkflowRunner(db,null,{skillDirectory:join(process.cwd(),'skills/filmcraft-use'),sourceRevision:lock.sources[0].sha,pluginVersion:manifest.version,runtimeHome:join(root,'runtime'),python:process.argv[3]});const p=runner.prepare(join(root,'plan.json'),join(root,'delivery'));const b=binding(root,{planHash:p.planIdentity.canonicalPlanSha256,nativePlanHash:p.planIdentity.workflowPlanSha256,outputRoot:p.outputRoot,projectKey:p.projectKey,projectRevision:p.projectRevision,inputHashes:p.inputHashes,inputRefs:Object.entries(p.inputHashes).map(([assetId,sha256])=>({assetId,sha256,version:sha256})),sourceRevision:lock.sources[0].sha,sourceTreeSha256:p.sourceTreeSha256,runtimeIdentity:p.runtimeIdentity});console.log(JSON.stringify(b));db.close();",WORK,PYTHON)
BINDING=WORK/'binding.json';BINDING.write_text(json.dumps(prepared));resources=WORK/'resources.json';resources.write_text(json.dumps({'limits':{'timeMs':1800000,'diskBytes':512000000,'outputBytes':512000000,'slots':2,'revisions':2},'allocation':{'timeMs':300000,'diskBytes':64000000,'outputBytes':64000000,'slots':1,'revisions':0}}))
workflow=ROOT/'src/cli/workflow.ts';sub=run([NODE,workflow,'subject','--binding',BINDING,'--resources',resources]);
# 执行 grant 使用绑定内引用；仍由实际私有 LocalAuthorizationStore 校验。
executionfile=GRANTS/(hashlib.sha256(prepared['authorizationRef'].encode()).hexdigest()+'.json');executionfile.write_text(json.dumps({'schema':'filmcraft-local-authorization/v1','authorizationRef':prepared['authorizationRef'],'authorizationScopeSha256':prepared['authorizationScopeSha256'],'subjects':[hashlib.sha256(json.dumps(sub,separators=(',',':'),sort_keys=True).encode()).hexdigest()],'expiresAt':int(time.time()*1000)+1800000,'revoked':False}));executionfile.chmod(0o600)
workflowargs=[NODE,workflow,'run','--binding',BINDING,'--resources',resources,'--plan',PLAN,'--ledger',LEDGER,'--blobs',WORK/'blobs','--authorization-root',GRANTS,'--runtime-home',RUNTIME,'--python',PYTHON]
created=run(workflowargs);assert created['state']=='verifying';
decoded=subprocess.run([str(Path(args.ffmpeg).resolve(strict=True)),'-v','error','-i',str(WORK/'delivery/film.mp4'),'-f','null','-'],capture_output=True,text=True,timeout=120);assert decoded.returncode==0,decoded.stderr
project=WORK/'delivery/project.fcproj';projectsha=sha(project)
back=select(OLD,'rollback',1);assert back['generation']==3
refused=run(workflowargs,expect=1);assert refused['error']['code']=='runtime_selection_mismatch';assert sha(project)==projectsha and sha(oldbinary)==oldbinarysha
history=nodejs("import{TaskLedger}from'./src/harness/task_ledger.ts';import{RuntimeDeployment}from'./src/adapters/runtime_deployment.ts';import{fingerprintSkill}from'./src/adapters/python_workflow.ts';const db=new TaskLedger(process.argv[2]);console.log(JSON.stringify({history:new RuntimeDeployment(db).history(),attempts:db.listAttempts('task-1'),oldTree:fingerprintSkill(process.argv[3]),newTree:fingerprintSkill(process.argv[4])}));db.close();",LEDGER,oldskill,ROOT/'skills/filmcraft-use');assert len(history['attempts'])==1 and history['oldTree']==OLD_TREE and history['newTree']==NEW_TREE
report={'schema':'filmcraft-native-runtime-transition-candidate/v1','result':'PASS','phases':phases,'oldVersion':oldversion,'newVersion':newversion,'oldBinaryPreserved':True,'oldBinarySha256':oldbinarysha,'projectPreservedAfterRollback':True,'independentFullDecode':'PASS','projectSha256':projectsha,'newWorkflow':created,'staleWorkflowRefusal':refused,'history':history,'scope':'Actual source candidate CLI, private host grants, owned synthetic input; not fixed plugin installation, full FC-RT-002 qualification or other-platform/creative/user acceptance'}
# 真实能力缺失与过期探测均保持原选择；不以成功下载证明可执行。
missing=json.loads(PLAN.read_text());missing['requires']={'resources':[{'kind':'codec','name':'missing-owned-runtime61-codec'}]};missingplan=WORK/'missing-codec.plan.json';missingplan.write_text(json.dumps(missing))
missingargs=[*flags,'--candidate',NEW];missingargs[missingargs.index('--plan')+1]=missingplan
subject=run([NODE,CLI,'probe-subject',*missingargs]);grant(subject)
missingresult=run([NODE,CLI,'probe',*missingargs,*auth],expect=1);assert missingresult['error']['code']=='capability_missing'
diagnosticresult=None
if args.require_diagnostics:
 diagnostic=missingresult['error']['diagnostic'];assert diagnostic['subject']=='codec:missing-owned-runtime61-codec' and diagnostic['status']=='missing' and diagnostic['observed']=='missing'
 mismatch=json.loads(PLAN.read_text());mismatch['requires']={'runtimeVersion':'0.0.0-incompatible'};mismatchplan=WORK/'version-mismatch.plan.json';mismatchplan.write_text(json.dumps(mismatch))
 mismatchargs=[*flags,'--candidate',NEW];mismatchargs[mismatchargs.index('--plan')+1]=mismatchplan
 subject=run([NODE,CLI,'probe-subject',*mismatchargs]);grant(subject)
 diagnosticresult=run([NODE,CLI,'probe',*mismatchargs,*auth],expect=1)
 error=diagnosticresult['error'];assert error['code']=='capability_identity_mismatch'
 diagnostic=error['diagnostic'];assert diagnostic['subject']=='runtimeVersion' and diagnostic['status']=='mismatch' and diagnostic['expected']=='0.0.0-incompatible' and diagnostic['observed']==newversion
 assert diagnostic['snapshot']['runtimeSha256']==new['descriptor']['runtimeIdentity']['sha256']
stale=run([NODE,CLI,'activate',*flags,'--candidate',NEW,'--probe',WORK/'new.probe.json',*auth],expect=1);assert stale['error']['code']=='runtime_probe_changed'
# 篡改回执即使获得相应主题许可，仍须与真实重新探测一致。
args=[*flags,'--candidate',NEW];subj=run([NODE,CLI,'probe-subject',*args]);grant(subj);fresh=run([NODE,CLI,'probe',*args,*auth]);fresh['descriptor']['runtimeIdentity']['sha256']='0'*64
forged=WORK/'forged.probe.json';forged.write_text(json.dumps(fresh));subj=run([NODE,CLI,'subject',*args,'--probe',forged]);grant(subj)
forgedresult=run([NODE,CLI,'activate',*args,'--probe',forged,*auth],expect=1);assert forgedresult['error']['code']=='runtime_probe_changed'
# 当前真实账本中存在一个受控未提交计划时，切换在原生重新探测前拒绝。
fresh=run([NODE,CLI,'probe',*args,*auth]);freshfile=WORK/'busy.probe.json';freshfile.write_text(json.dumps(fresh))
nodejs("import{TaskLedger}from'./src/harness/task_ledger.ts';import{RuntimeDeployment}from'./src/adapters/runtime_deployment.ts';import{readFileSync}from'node:fs';const db=new TaskLedger(process.argv[2]),old=new RuntimeDeployment(db).current().descriptor,b=JSON.parse(readFileSync(process.argv[3],'utf8'));db.register({...b,taskId:'pending-owned-fixture',idempotencyKey:'pending-owned-fixture',outputRoot:process.argv[4],sourceRevision:old.sourceRevision,sourceTreeSha256:old.sourceTreeSha256,runtimeIdentity:old.runtimeIdentity});db.close();console.log('{}');",LEDGER,BINDING,WORK/'pending-output')
subj=run([NODE,CLI,'subject',*args,'--probe',freshfile]);grant(subj)
busy=run([NODE,CLI,'activate',*args,'--probe',freshfile,*auth],expect=1);assert busy['error']['code']=='runtime_not_drained'
assert sha(project)==projectsha and sha(oldbinary)==oldbinarysha
report['negativeCases']={'missingCodec':missingresult,'staleProbe':stale,'forgedProbe':forgedresult,'pendingPlan':busy};report['finalSelectionGeneration']=nodejs("import{TaskLedger}from'./src/harness/task_ledger.ts';import{RuntimeDeployment}from'./src/adapters/runtime_deployment.ts';const db=new TaskLedger(process.argv[2]);console.log(JSON.stringify({generation:new RuntimeDeployment(db).current().generation}));db.close();",LEDGER)['generation'];assert report['finalSelectionGeneration']==3
if diagnosticresult:report['negativeCases']['versionDiagnostic']=diagnosticresult
(WORK/'report.private.json').write_text(json.dumps(report,indent=2));print(json.dumps({'result':'PASS','old':oldversion,'new':newversion,'generations':3,'attempts':1,'negativeCases':len(report['negativeCases'])}))
