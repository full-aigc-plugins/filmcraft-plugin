import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync,readFileSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {PythonWorkflowRunner} from '../../src/adapters/python_workflow.ts';
import {workspace} from './fixtures.ts';
function prepare(t:any,issues:unknown){
 const root=workspace(t),skill=join(root,'synthetic-skill'),scripts=join(skill,'scripts');mkdirSync(scripts,{recursive:true});
 const sources:Record<string,string>={
  'commands.py':'import json\nreply_json=json.loads\n',
  'workflow.py':'import json\ndef validate(*args): pass\ndef preflight_assets(*args):\n error=ValueError("asset_digest_mismatch: first")\n error.asset_issues=json.loads('+JSON.stringify(JSON.stringify(issues))+')\n raise error\n',
  'capabilities.py':'# synthetic pre-install refusal fixture\n',
  'runtime.lock.json':readFileSync(new URL('../../skills/filmcraft-use/scripts/runtime.lock.json',import.meta.url),'utf8')};
 for(const [name,value] of Object.entries(sources)){writeFileSync(join(scripts,name),value);}
 const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({operations:[]}));
 const output=join(root,'delivery'),runtimeHome=join(root,'runtime');
 const runner=new PythonWorkflowRunner(null as any,null as any,{skillDirectory:skill,sourceRevision:'a'.repeat(40),pluginVersion:'synthetic',runtimeHome,python:process.env.FILMCRAFT_PYTHON??'python3'});
 return {run:()=>runner.prepare(plan,output),output,runtimeHome};
}
test('asset issue list crosses Python preflight without native installation or local paths',t=>{
 const issues=[{alias:'first',origin:'source',reason:'missing_file'},{alias:'second',origin:'plan',reason:'digest_mismatch'}];
 const f=prepare(t,issues);assert.throws(f.run,(error:any)=>{assert.equal(error.code,'asset_preflight_failed');assert.deepEqual(error.assetIssues,issues);return true;});
 assert.equal(existsSync(f.output),false);assert.equal(existsSync(f.runtimeHome),false);
});
test('malformed asset issue diagnostics cannot become public refusal details',t=>{
 const f=prepare(t,[{alias:'first',origin:'plan',reason:'missing_file',path:'/private/owned-secret'}]);
 assert.throws(f.run,(error:any)=>{assert.equal(error.code,'native_preflight_failed');assert.equal(error.assetIssues,undefined);assert.doesNotMatch(error.message,/owned-secret/);return true;});
 assert.equal(existsSync(f.output),false);assert.equal(existsSync(f.runtimeHome),false);
});

test('asset issue validator refuses paths, open fields, unsupported states and non-list values',async()=>{
 const {validateAssetIssues}=await import('../../src/adapters/asset_refusal.ts');
 const row={alias:'first',origin:'plan',reason:'missing_file'};
 for(const value of [[],null,[{...row,alias:'../private'}],[{...row,origin:'remote'}],[{...row,reason:'available'}],[{...row,path:'/private'}]]){
  assert.equal(validateAssetIssues(value),undefined);
 }
});
test('validated safe issues are detached from mutable native reply data',async()=>{
 const {validateAssetIssues}=await import('../../src/adapters/asset_refusal.ts');
 const rows=[{alias:'first',origin:'source',reason:'missing_file'}],safe=validateAssetIssues(rows)!;
 rows[0].alias='changed';assert.equal(safe[0].alias,'first');
});

test('existing long registered aliases remain valid across asset preflight',t=>{
 const issues=[{alias:'a'.repeat(300),origin:'plan',reason:'missing_file'}],f=prepare(t,issues);
 assert.throws(f.run,(error:any)=>{assert.equal(error.code,'asset_preflight_failed');assert.deepEqual(error.assetIssues,issues);return true;});
});
