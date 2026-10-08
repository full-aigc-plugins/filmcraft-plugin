import {test} from 'node:test';
import assert from 'node:assert/strict';
import {CapabilityRefusal,validateCapabilityDiagnostic} from '../../src/adapters/capability_refusal.ts';

const diagnostic=()=>({schema:'filmcraft-capability-refusal/v1',subject:'runtimeVersion',status:'mismatch',
  expected:'0.2.0-craft.4',observed:'0.2.0-craft.5',snapshot:{mode:'headless',platform:'darwin-arm64',
    runtimeVersion:'0.2.0-craft.5',runtimeSha256:'a'.repeat(64),parametersSha256:'b'.repeat(64),catalogSha256:'c'.repeat(64)}});
test('capability diagnostic preserves a cloned safe difference, not caller mutation',()=>{
 const value=diagnostic(),error=new CapabilityRefusal('capability_identity_mismatch',value);
 assert.deepEqual(error.diagnostic,value);value.subject='changed';assert.equal(error.diagnostic?.subject,'runtimeVersion');
});
test('capability diagnostic rejects path, extra field, malformed hash, and inconsistent status',()=>{
 for(const value of [{...diagnostic(),subject:'/private/secret'}, {...diagnostic(),observed:'/tmp/secret'},
  {...diagnostic(),stack:'unrelated text'}, {...diagnostic(),snapshot:{...diagnostic().snapshot,platform:'C:\\secret'}},
  {...diagnostic(),snapshot:{...diagnostic().snapshot,runtimeSha256:'bad'}},
  {...diagnostic(),snapshot:{...diagnostic().snapshot,path:'/private'}}]){
  assert.equal(validateCapabilityDiagnostic(value),undefined);
  assert.equal(new CapabilityRefusal('capability_identity_mismatch',value).diagnostic,undefined);
 }
 assert.equal(new CapabilityRefusal('capability_missing',diagnostic()).diagnostic,undefined);
});
