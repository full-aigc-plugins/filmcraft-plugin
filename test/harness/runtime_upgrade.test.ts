import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { RuntimeUpgrade } from '../../src/adapters/runtime_upgrade.ts';
import { fingerprintSkill } from '../../src/adapters/python_workflow.ts';
import { workspace, hash } from './fixtures.ts';
import { readFileSync } from 'node:fs';

function setup(t:any){
 const root=workspace(t),file=join(root,'state.sqlite'),db=new TaskLedger(file);db.close();
 // 授权/只读主题测试使用明确的合成锁，不把macOS发布制品当成Linux可执行证据。
 const skill=join(root,'synthetic-candidate');mkdirSync(join(skill,'scripts'),{recursive:true});
 const lock=JSON.parse(readFileSync(new URL('../../skills/filmcraft-use/scripts/runtime.lock.json',import.meta.url),'utf8'));
 const key=process.platform==='darwin'?'darwin-'+process.arch:process.platform+'-'+process.arch;
 lock.artifacts[key]={...Object.values(lock.artifacts)[0] as object};
 writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify(lock));
 const candidate=join(root,'candidate.json'),plan=join(root,'plan.json');
 writeFileSync(candidate,JSON.stringify({schema:'filmcraft-runtime-candidate/v1',skillDirectory:skill,
  sourceRevision:'a'.repeat(40),sourceTreeSha256:fingerprintSkill(skill)}));
 writeFileSync(plan,JSON.stringify({document:{name:'Probe',width:32,height:32,frameRate:{num:12,den:1}},operations:[],exports:{}}));
 const permissions={schema:'filmcraft-execution-permissions/v1' as const,readRoots:[root],writeRoots:[root]};
 const options={permissions,candidateFile:candidate,planFile:plan,ledgerFile:file,runtimeHome:join(root,'runtime'),python:process.env.FILMCRAFT_PYTHON??'python3'};
 return {root,file,candidate,plan,options,service:new RuntimeUpgrade(options)};
}
test('upgrade probe subject is read-only and binds ledger, runtime home, source and plan',t=>{
 const f=setup(t),before=readFileSync(f.file),subject=f.service.probeSubject();
 assert.deepEqual(readFileSync(f.file),before);assert.equal(existsSync(f.options.runtimeHome),false);
 assert.notEqual(new RuntimeUpgrade({...f.options,runtimeHome:join(f.root,'other')}).probeSubject().identitySha256,subject.identitySha256);
 writeFileSync(f.plan,readFileSync(f.plan,'utf8')+'\n');
 assert.notEqual(f.service.probeSubject().identitySha256,subject.identitySha256);
});
test('unauthorized runtime probe installs nothing and leaves ledger untouched',t=>{
 const f=setup(t),before=readFileSync(f.file);
 assert.throws(()=>f.service.probe({authorizationRef:'grant',authorizationScopeSha256:hash()}),/authorization_verifier_required/);
 assert.equal(existsSync(f.options.runtimeHome),false);assert.deepEqual(readFileSync(f.file),before);
});
test('runtime CLI subject does not create a grant, installation, or ledger writes',t=>{
 const f=setup(t),before=readFileSync(f.file),cli=new URL('../../src/cli/runtime.ts',import.meta.url).pathname;
 const permissionFile=join(f.root,'permissions.json');writeFileSync(permissionFile,JSON.stringify(f.options.permissions));
 const argv=[cli,'probe-subject','--candidate',f.candidate,'--plan',f.plan,'--ledger',f.file,'--runtime-home',f.options.runtimeHome,'--permissions',permissionFile];
 const r=spawnSync(process.execPath,argv,{encoding:'utf8'});assert.equal(r.status,0,r.stdout+r.stderr);
 assert.deepEqual(JSON.parse(r.stdout),f.service.probeSubject());assert.deepEqual(readFileSync(f.file),before);
 const run=spawnSync(process.execPath,[...argv.slice(0,1),'probe',...argv.slice(2),'--authorization-ref','grant','--authorization-scope-sha256',hash(),'--authorization-root',join(f.root,'grants')],{encoding:'utf8'});
 assert.equal(run.status,1);assert.equal(JSON.parse(run.stdout).error.code,'authorization_required');assert.equal(existsSync(f.options.runtimeHome),false);
});
test('source drift during authorization is refused before installing a runtime',async t=>{
 const f=setup(t);const {fixtureAuthorizer}=await import('./fixtures.ts');
 const service=new RuntimeUpgrade(f.options,(subject,request)=>{writeFileSync(f.plan,'{}');return fixtureAuthorizer(subject,request);});
 assert.throws(()=>service.probe({authorizationRef:'grant',authorizationScopeSha256:hash()}),/runtime_probe_changed/);
 assert.equal(existsSync(f.options.runtimeHome),false);
});
test('probe authorization binds another ledger and interpreter rather than trusting a reference',t=>{
 const f=setup(t),other=join(f.root,'other.sqlite'),db=new TaskLedger(other);db.close();
 assert.notEqual(new RuntimeUpgrade({...f.options,ledgerFile:other}).probeSubject().identitySha256,f.service.probeSubject().identitySha256);
 assert.notEqual(new RuntimeUpgrade({...f.options,python:process.execPath}).probeSubject().identitySha256,f.service.probeSubject().identitySha256);
});
test('capability refusal survives the Python preflight boundary as capability_missing',async t=>{
 const {mkdirSync}=await import('node:fs');const {PythonWorkflowRunner}=await import('../../src/adapters/python_workflow.ts');
 const f=setup(t),skill=join(f.root,'synthetic-skill'),scripts=join(skill,'scripts');mkdirSync(scripts,{recursive:true});
 const sources:{[key:string]:string}={
  'runtime.lock.json':readFileSync(new URL('../../skills/filmcraft-use/scripts/runtime.lock.json',import.meta.url),'utf8'),
  'commands.py':'import json\nreply_json=json.loads\ndef runtime_rows(*args): return []\ndef capability_snapshot(*args,**kwargs): return {}\n',
  'workflow.py':'def validate(*args): pass\ndef preflight_assets(*args): pass\n',
  'bootstrap.py':"def install(*args): return {'executable':'synthetic-no-native-process'}\n",
  'mcp_session.py':'class Session:\n def __init__(self,*args): pass\n def __enter__(self): return self\n def __exit__(self,*args): pass\n',
  'capabilities.py':"def enforce(*args): raise ValueError('capability_missing: synthetic-operation')\n"
 };
 for(const [name,data] of Object.entries(sources)){writeFileSync(join(scripts,name),data);}
 const runner=new PythonWorkflowRunner(null as any,null as any,{skillDirectory:skill,sourceRevision:'a'.repeat(40),runtimeHome:join(f.root,'unused-runtime'),pluginVersion:'synthetic',python:f.options.python});
 assert.throws(()=>runner.prepare(f.plan,join(f.root,'output')),(e:any)=>{
  assert.equal(e.code,'capability_missing');
  assert.equal(e.diagnostic?.schema,'filmcraft-capability-refusal/v1');
  assert.equal(e.diagnostic?.subject,'synthetic-operation');
  assert.equal(e.diagnostic?.status,'missing');
  return true;
 });
 assert.equal(existsSync(join(f.root,'output')),false);
});

test('an unavailable platform is rejected before authorization, installation or ledger changes',t=>{
 const f=setup(t),c=JSON.parse(readFileSync(f.candidate,'utf8')),p=join(c.skillDirectory,'scripts/runtime.lock.json');
 const lock=JSON.parse(readFileSync(p,'utf8'));lock.artifacts={};writeFileSync(p,JSON.stringify(lock));c.sourceTreeSha256=fingerprintSkill(c.skillDirectory);writeFileSync(f.candidate,JSON.stringify(c));
 const before=readFileSync(f.file);assert.throws(()=>f.service.probeSubject(),/unsupported_upgrade_platform/);
 assert.equal(existsSync(f.options.runtimeHome),false);assert.deepEqual(readFileSync(f.file),before);
});

// 安装维护也要绑定独立可信根，不能由已有升级引用或计划推导授权。
test('maintenance probe requires roots before opening a plan or invoking authorization',t=>{
 const f=setup(t);let queries=0;
 const service=new RuntimeUpgrade({...f.options,permissions:undefined,planFile:join(f.root,'absent')},()=>{queries++;throw new Error('unexpected_authorization');});
 assert.throws(()=>service.probe({authorizationRef:'grant',authorizationScopeSha256:hash()}),/execution_permissions_required/);
 assert.equal(queries,0);assert.equal(existsSync(f.options.runtimeHome),false);
});
test('maintenance probe roots bind exact authorization and reject outside plan and runtime',t=>{
 const f=setup(t),outside=workspace(t),subject=f.service.probeSubject();
 const expanded={...f.options.permissions,readRoots:[f.root,outside].sort()};
 assert.notEqual(new RuntimeUpgrade({...f.options,permissions:expanded}).probeSubject().identitySha256,subject.identitySha256);
 assert.throws(()=>new RuntimeUpgrade({...f.options,planFile:join(outside,'unread-plan.json')}).probeSubject(),/permission_read_denied/);
 assert.throws(()=>new RuntimeUpgrade({...f.options,runtimeHome:join(outside,'runtime')}).probeSubject(),/permission_write_denied/);
 assert.equal(existsSync(f.options.runtimeHome),false);
});
test('authorized maintenance passes its independent roots to native capability preflight',async t=>{
 const f=setup(t),{PythonWorkflowRunner}=await import('../../src/adapters/python_workflow.ts');
 const {fixtureAuthorizer}=await import('./fixtures.ts');let observed:any;
 const original=PythonWorkflowRunner.prototype.prepare;
 PythonWorkflowRunner.prototype.prepare=function(){
  observed=this.options.permissions;
  const c=JSON.parse(readFileSync(f.candidate,'utf8')),lock=JSON.parse(readFileSync(join(c.skillDirectory,'scripts/runtime.lock.json'),'utf8'));
  return {sourceTreeSha256:c.sourceTreeSha256,snapshot:{schema:'filmcraft-capability-snapshot/v1'},runtimeIdentity:{pluginId:'filmcraft',pluginVersion:'synthetic',cliVersion:lock.resolvedVersion,sha256:Object.values(lock.artifacts)[0].binarySha256,mode:'headless',capabilitySnapshotSha256:hash()}} as any;
 };
 try {
  const result=new RuntimeUpgrade(f.options,fixtureAuthorizer).probe({authorizationRef:'grant',authorizationScopeSha256:hash()});
  assert.deepEqual(observed,f.options.permissions);assert.match(result.request.executionPermissionsSha256,/^[a-f0-9]{64}$/);
  assert.equal(existsSync(f.options.runtimeHome),false);
 } finally {PythonWorkflowRunner.prototype.prepare=original;}
});
