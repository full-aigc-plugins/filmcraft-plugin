import { realpathSync } from 'node:fs';
import type { DatabaseSync } from 'node:sqlite';
import type { TaskLedger, Binding } from '../harness/task_ledger.ts';
import type { AuthorizationRequest, Authorizer } from '../harness/authorization.ts';
import { requireAuthorization } from '../harness/authorization.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';

/** schema6 持久保存选择历史；原生制品仍由固定技能安装器保留在独立版本目录。 */
export const DEPLOYMENT_SCHEMA=`CREATE TABLE runtime_deployments(generation INTEGER PRIMARY KEY NOT NULL,
 descriptor TEXT NOT NULL, descriptor_sha256 TEXT NOT NULL, action TEXT NOT NULL,
 authorization_ref TEXT NOT NULL, created_at INTEGER NOT NULL) STRICT;`;
export type DeploymentDescriptor={sourceRevision:string;sourceTreeSha256:string;runtimeIdentity:Binding['runtimeIdentity'];ledgerSchemas:number[]};
function valid(value:DeploymentDescriptor){
 check(isObject(value)&&Object.keys(value).sort().join(',')==='ledgerSchemas,runtimeIdentity,sourceRevision,sourceTreeSha256'
  &&/^[a-f0-9]{40}$/.test(value.sourceRevision)&&isHash(value.sourceTreeSha256)
  &&Array.isArray(value.ledgerSchemas)&&value.ledgerSchemas.length>0
  &&value.ledgerSchemas.every(n=>Number.isSafeInteger(n)&&n>0),'runtime_descriptor_invalid');
 const r=value.runtimeIdentity;
 check(isObject(r)&&r.pluginId==='filmcraft'&&typeof r.pluginVersion==='string'&&typeof r.cliVersion==='string'
  &&isHash(r.sha256)&&isHash(r.capabilitySnapshotSha256)&&['headless','bridge'].includes(r.mode)
  &&Object.keys(r).sort().join(',')==='capabilitySnapshotSha256,cliVersion,mode,pluginId,pluginVersion,sha256','runtime_descriptor_invalid');
}
/** 诊断与提交均核验完整历史；破坏记录不能使旧执行器获得默认许可。 */
export function deploymentHistory(db:DatabaseSync){
 const rows=db.prepare('SELECT * FROM runtime_deployments ORDER BY generation').all() as any[];
 return rows.map((row,index)=>{
  const descriptor=parseJson(row.descriptor);valid(descriptor);
  check(row.generation===index+1&&sha256(row.descriptor)===row.descriptor_sha256
   &&['upgrade','rollback'].includes(row.action)&&typeof row.authorization_ref==='string'
   &&Number.isSafeInteger(row.created_at),'runtime_history_corrupt');return {...row,descriptor};
 });
}
/** 计划能力快照随输入而变；执行选择绑定二进制、模式及技能源，而非某个旧计划快照。 */
export function assertRuntimeSelection(db:DatabaseSync,binding:Pick<Binding,'sourceRevision'|'sourceTreeSha256'|'runtimeIdentity'>){
 const rows=deploymentHistory(db),active=rows.at(-1);if(!active){return;}
 const expected=active.descriptor;
 const identity=(r:Binding['runtimeIdentity'])=>({pluginId:r.pluginId,pluginVersion:r.pluginVersion,cliVersion:r.cliVersion,sha256:r.sha256,mode:r.mode});
 check(expected.sourceRevision===binding.sourceRevision&&expected.sourceTreeSha256===binding.sourceTreeSha256
  &&stableJson(identity(expected.runtimeIdentity))===stableJson(identity(binding.runtimeIdentity)),'runtime_selection_mismatch');
}
/** 授权主题绑定完整候选与当前代次；事务排空后才发布选择，旧制品不删除。 */
export class RuntimeDeployment{
 ledger:TaskLedger;authorize?:Authorizer;verifyCandidate?:(descriptor:DeploymentDescriptor)=>DeploymentDescriptor;expectedGeneration?:number;
 constructor(ledger:TaskLedger,options:{authorize?:Authorizer;verifyCandidate?:(descriptor:DeploymentDescriptor)=>DeploymentDescriptor;expectedGeneration?:number}={}){
  this.ledger=ledger;this.authorize=options.authorize;this.verifyCandidate=options.verifyCandidate;this.expectedGeneration=options.expectedGeneration;
 }
 history(){return deploymentHistory(this.ledger.db);}
 current(){return this.history().at(-1)??null;}
 /** 授权主题绑定规范账本路径，不能把相同候选的许可用于另一个账本。 */
 subject(descriptor:DeploymentDescriptor,action:'upgrade'|'rollback'){
  valid(descriptor);const file=this.ledger.db.prepare('PRAGMA database_list').all().find(row=>row.name==='main')!.file;
  return {action,identitySha256:sha256(stableJson({ledgerPathSha256:sha256(realpathSync(String(file))),generation:this.current()?.generation??0,descriptor}))};
 }
 private select(descriptor:DeploymentDescriptor,request:AuthorizationRequest,action:'upgrade'|'rollback'){
  descriptor=parseJson(stableJson(descriptor));valid(descriptor);
  return this.ledger.transaction(()=>{
   const current=this.current(),schema=Number(this.ledger.db.prepare('PRAGMA user_version').get()!.user_version);
   check(this.expectedGeneration===undefined||this.expectedGeneration===(current?.generation??0),'runtime_generation_stale');
   check(descriptor.ledgerSchemas.includes(schema),'runtime_state_incompatible');
   const subject=this.subject(descriptor,action);
   requireAuthorization(this.authorize,request,subject);
   // 超时不等于停止；未知 attempt、持久工程占用和未提交计划都必须先处理。
   check(!this.ledger.db.prepare("SELECT task_id FROM tasks WHERE state NOT IN ('verifying','review_ready','completed','failed','cancelled')").get()
    &&!this.ledger.db.prepare('SELECT task_id FROM project_leases').get()
    &&!this.ledger.db.prepare("SELECT attempt_id FROM attempts WHERE state IN ('intent','submitted','unknown')").get()
    &&!this.ledger.db.prepare("SELECT task_id FROM task_resources WHERE state!='settled'").get(),'runtime_not_drained');
   if(this.verifyCandidate){
    const measured=this.verifyCandidate(parseJson(stableJson(descriptor)));valid(measured);
    const base=(d:DeploymentDescriptor)=>({...d,runtimeIdentity:{...d.runtimeIdentity,capabilitySnapshotSha256:null}});
    check(stableJson(base(measured))===stableJson(base(descriptor)),'runtime_probe_changed');
    descriptor=parseJson(stableJson(measured));
   }
   requireAuthorization(this.authorize,request,subject);
   const generation=(current?.generation??0)+1,data=stableJson(descriptor);
   this.ledger.db.prepare('INSERT INTO runtime_deployments VALUES(?,?,?,?,?,?)')
    .run(generation,data,sha256(data),action,request.authorizationRef,Date.now());
   return this.current()!;
  });
 }
 /** 激活经过宿主核验并授权的固定候选；本方法不下载或自行推断兼容性。 */
 activate(descriptor:DeploymentDescriptor,request:AuthorizationRequest){return this.select(descriptor,request,'upgrade');}
 /** 回退仅使用持久历史原文，并重新检查当前 schema、排空状态及宿主授权。 */
 rollback(generation:number,request:AuthorizationRequest){
  check(Number.isSafeInteger(generation)&&generation>0,'runtime_generation_invalid');
  const target=this.history().find(row=>row.generation===generation);check(target,'runtime_generation_missing');
  return this.select(target.descriptor,request,'rollback');
 }
}
