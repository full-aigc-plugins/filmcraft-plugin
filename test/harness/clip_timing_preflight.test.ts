import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync,readFileSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {PythonWorkflowRunner} from '../../src/adapters/python_workflow.ts';
import {workspace} from './fixtures.ts';
function prepare(t:any,detail:unknown){
 const root=workspace(t),skill=join(root,'synthetic-skill'),scripts=join(skill,'scripts');mkdirSync(scripts,{recursive:true});
 for(const [name,value] of Object.entries({
  'commands.py':'import json\nreply_json=json.loads\n',
  'workflow.py':'import json\ndef validate(*args):\n error=ValueError("ticks_require_decimal_string")\n error.clip_timing=json.loads('+JSON.stringify(JSON.stringify(detail))+')\n raise error\n',
  'capabilities.py':'# owned pre-install refusal fixture\n',
  'runtime.lock.json':readFileSync(new URL('../../skills/filmcraft-use/scripts/runtime.lock.json',import.meta.url),'utf8')})){writeFileSync(join(scripts,name),value);}
 const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({operations:[]}));
 const output=join(root,'delivery'),runtimeHome=join(root,'runtime');
 const runner=new PythonWorkflowRunner(null as any,null as any,{skillDirectory:skill,sourceRevision:'a'.repeat(40),pluginVersion:'synthetic',runtimeHome,python:process.env.FILMCRAFT_PYTHON??'python3'});
 return {run:()=>runner.prepare(plan,output),output,runtimeHome};
}
test('clip timing refusal preserves exact u64 target before native installation',t=>{
 const detail={reason:'ticks_require_decimal_string',clipIds:['18446744073709551615']},f=prepare(t,detail);
 assert.throws(f.run,(error:any)=>{assert.equal(error.code,'clip_timing_failed');assert.deepEqual(error.clipTiming,detail);return true;});
 assert.equal(existsSync(f.output),false);assert.equal(existsSync(f.runtimeHome),false);
});
test('clip timing refusal rejects path-shaped and expanded diagnostics',t=>{
 const f=prepare(t,{reason:'clip_out_of_range',clipIds:['11'],path:'/private/owned-secret'});
 assert.throws(f.run,(error:any)=>{assert.equal(error.code,'native_preflight_failed');assert.equal(error.clipTiming,undefined);assert.doesNotMatch(error.message,/owned-secret/);return true;});
});
test('clip diagnostic validation rejects unsafe values and preserves detached exact identity',async()=>{
 const {validateClipTiming}=await import('../../src/adapters/clip_refusal.ts');
 const detail={reason:'clip_out_of_range',clipIds:['11']};
 for(const value of [null,{}, {...detail,reason:[]},{...detail,reason:'available'},{...detail,clipIds:[]},
  {...detail,clipIds:[11]},{...detail,clipIds:['0']},{...detail,clipIds:['011']},
  {...detail,clipIds:['18446744073709551616']},{...detail,clipIds:['../private']},{...detail,path:'/private'}]){
  assert.equal(validateClipTiming(value),undefined);
 }
 const safe=validateClipTiming(detail)!;detail.clipIds[0]='22';assert.deepEqual(safe,{reason:'clip_out_of_range',clipIds:['11']});
});
test('malformed reason arrays fail closed across Python preflight',t=>{
 const f=prepare(t,{reason:[],clipIds:['11']});
 assert.throws(f.run,(error:any)=>{assert.equal(error.code,'native_preflight_failed');assert.equal(error.clipTiming,undefined);return true;});
});
