import {realpathSync} from 'node:fs';
import {basename,dirname,resolve} from 'node:path';
import {readBoundFile} from '../artifacts/receipt_index.ts';
import {check,isHash,isObject,parseJson} from '../support/json.ts';
import {fingerprintSkill} from './python_workflow.ts';
/** 候选仅提供可重新核验的技能源身份，不携带能力状态或许可。 */
export function readRuntimeCandidate(file:string){
 const path=resolve(file),value=parseJson(readBoundFile(dirname(path),basename(path)).toString('utf8'));
 check(isObject(value)&&Object.keys(value).sort().join(',')==='schema,skillDirectory,sourceRevision,sourceTreeSha256'
  &&value.schema==='filmcraft-runtime-candidate/v1'&&typeof value.skillDirectory==='string'
  &&typeof value.sourceRevision==='string'&&/^[a-f0-9]{40}$/.test(value.sourceRevision)&&isHash(value.sourceTreeSha256),'runtime_candidate_invalid');
 const skillDirectory=realpathSync(value.skillDirectory);
 check(fingerprintSkill(skillDirectory)===value.sourceTreeSha256,'runtime_candidate_changed');
 return {skillDirectory,sourceRevision:value.sourceRevision,sourceTreeSha256:value.sourceTreeSha256};
}
