import { requirePermissions, requireRead, requireWrite } from '../support/execution_permissions.ts';
import type { ExecutionPermissions } from '../support/execution_permissions.ts';
import { existsSync, readFileSync, realpathSync, statSync } from 'node:fs';
import { basename, delimiter, dirname, isAbsolute, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { TaskLedger } from '../harness/task_ledger.ts';
import { forensicSnapshot } from '../harness/forensic_snapshot.ts';
import { requireAuthorization } from '../harness/authorization.ts';
import type { AuthorizationRequest, Authorizer, AuthorizationSubject } from '../harness/authorization.ts';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { canonicalTarget } from '../support/paths.ts';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';
import { PythonWorkflowRunner } from './python_workflow.ts';
import { deploymentHistory, RuntimeDeployment } from './runtime_deployment.ts';
import type { DeploymentDescriptor } from './runtime_deployment.ts';
import {readRuntimeCandidate} from './runtime_candidate.ts';

export type UpgradeOptions={candidateFile:string;planFile:string;ledgerFile:string;runtimeHome:string;python?:string;permissions?:ExecutionPermissions};
function read(path:string){const p=resolve(path);return parseJson(readBoundFile(dirname(p),basename(p)).toString('utf8'));}
/** 两阶段宿主授权：安装/只读探测与发布选择分别绑定，回执本身不能授权任何动作。 */
export class RuntimeUpgrade{
 options:UpgradeOptions;authorize?:Authorizer;
 constructor(options:UpgradeOptions,authorize?:Authorizer){this.options={...options,permissions:options.permissions?requirePermissions(options.permissions):undefined};this.authorize=authorize;}
 private context(){
  const permissions=requirePermissions(this.options.permissions);
  requireRead(this.options.candidateFile,permissions);requireRead(this.options.planFile,permissions);
  requireRead(this.options.ledgerFile,permissions);requireWrite(this.options.runtimeHome,permissions);
  const c=readRuntimeCandidate(this.options.candidateFile),skill=c.skillDirectory;
  const lock=read(join(skill,'scripts/runtime.lock.json'));
  const platformKey=process.platform==='darwin'?'darwin-'+process.arch:process.platform+'-'+process.arch;
  const artifact=lock.artifacts?.[platformKey];
  check(artifact&&isHash(artifact.binarySha256)&&isHash(artifact.archiveSha256)&&typeof lock.resolvedVersion==='string','unsupported_upgrade_platform');
  const ledgerPath=realpathSync(this.options.ledgerFile),runtimeHome=canonicalTarget(this.options.runtimeHome);
  const state=forensicSnapshot(ledgerPath,l=>({schema:Number(l.db.prepare('PRAGMA user_version').get()!.user_version),generation:deploymentHistory(l.db).at(-1)?.generation??0}));
  check(state.schema===6,'runtime_state_incompatible');
  const selectedPython=this.options.python??process.env.FILMCRAFT_PYTHON??'python3';
  const executable=isAbsolute(selectedPython)?selectedPython:(process.env.PATH??'').split(delimiter).map(p=>join(p,selectedPython)).find(p=>existsSync(p)&&statSync(p).isFile());
  check(executable,'runtime_probe_interpreter_missing');const python=realpathSync(executable);
  const manifest=read(fileURLToPath(new URL('../../plugin.json',import.meta.url)));
  const identity={schema:'filmcraft-runtime-probe-request/v1',executionPermissionsSha256:sha256(stableJson(permissions)),ledgerPathSha256:sha256(ledgerPath),runtimeHomeSha256:sha256(runtimeHome),
   pythonPathSha256:sha256(python),pythonBinarySha256:sha256(readFileSync(python)),
   preflightSha256:sha256(readFileSync(fileURLToPath(new URL('../../scripts/native_preflight.py',import.meta.url)))),
   ledgerSchema:state.schema,generation:state.generation,sourceRevision:c.sourceRevision,sourceTreeSha256:c.sourceTreeSha256,
   skillPathSha256:sha256(skill),runtimeLockSha256:sha256(stableJson(lock)),planSha256:sha256(readFileSync(this.options.planFile)),
   pluginVersion:manifest.version,runtimeVersion:lock.resolvedVersion,runtimeSha256:artifact.binarySha256,mode:'headless'};
  return {identity,skill,ledgerPath,runtimeHome,python,permissions};
 }
 /** 只读返回安装/探测主题，不写账本、缓存、授权或媒体。 */
 probeSubject():AuthorizationSubject{return {action:'upgrade',identitySha256:sha256(stableJson(this.context().identity))};}
 private measure(context:ReturnType<RuntimeUpgrade['context']>){
  check(stableJson(this.context().identity)===stableJson(context.identity),'runtime_probe_changed');
  const runner=new PythonWorkflowRunner(null as any,null as any,{skillDirectory:context.skill,sourceRevision:context.identity.sourceRevision,
   pluginVersion:context.identity.pluginVersion,runtimeHome:context.runtimeHome,python:context.python,permissions:context.permissions});
  const prepared=runner.prepare(this.options.planFile,join(context.runtimeHome,'.probe-no-output'));
  check(stableJson(this.context().identity)===stableJson(context.identity),'runtime_probe_changed');
  const r=prepared.runtimeIdentity;
  check(r.cliVersion===context.identity.runtimeVersion&&r.sha256===context.identity.runtimeSha256&&r.mode==='headless','runtime_probe_changed');
  const descriptor:DeploymentDescriptor={sourceRevision:context.identity.sourceRevision,sourceTreeSha256:prepared.sourceTreeSha256,runtimeIdentity:r,ledgerSchemas:[6]};
  return {descriptor,snapshot:prepared.snapshot};
 }
 /** 显式授权后才允许固定安装器下载及运行只读 MCP 能力查询。 */
 probe(request:AuthorizationRequest){
  const context=this.context(),subject={action:'upgrade' as const,identitySha256:sha256(stableJson(context.identity))};
  requireAuthorization(this.authorize,request,subject);
  const measured=this.measure(context);requireAuthorization(this.authorize,request,subject);
  return {schema:'filmcraft-runtime-upgrade-probe/v1',request:context.identity,...measured};
 }
 private checked(probe:any){
  const context=this.context();
  check(isObject(probe)&&Object.keys(probe).sort().join(',')==='descriptor,request,schema,snapshot'
   &&probe.schema==='filmcraft-runtime-upgrade-probe/v1'&&stableJson(probe.request)===stableJson(context.identity)
   &&isObject(probe.snapshot)&&sha256(stableJson(probe.snapshot))===probe.descriptor?.runtimeIdentity?.capabilitySnapshotSha256,'runtime_probe_changed');
  return context;
 }
 /** 发布主题绑定探测原文、账本、当前代次、计划及回退目标。 */
 selectionSubject(probe:any,rollbackGeneration?:number):AuthorizationSubject{
  const context=this.checked(probe);check(rollbackGeneration===undefined||Number.isSafeInteger(rollbackGeneration)&&rollbackGeneration>0,'runtime_generation_invalid');
  return {action:rollbackGeneration===undefined?'upgrade':'rollback',identitySha256:sha256(stableJson({request:context.identity,probeSha256:sha256(stableJson(probe)),rollbackGeneration:rollbackGeneration??null}))};
 }
 /** 排空事务持有期间重新实测；篡改回执、探测漂移或授权撤销均不发布新选择。 */
 select(probe:any,request:AuthorizationRequest,rollbackGeneration?:number){
  requireWrite(this.options.ledgerFile,requirePermissions(this.options.permissions));
  const context=this.checked(probe),subject=this.selectionSubject(probe,rollbackGeneration);
  requireAuthorization(this.authorize,request,subject);
  const ledger=new TaskLedger(context.ledgerPath);
  try{
   let expectedInner:AuthorizationSubject;
   const service=new RuntimeDeployment(ledger,{expectedGeneration:context.identity.generation,
    authorize:(inner,grant)=>{
     check(stableJson(inner)===stableJson(expectedInner),'runtime_selection_subject_changed');
     const permitted=requireAuthorization(this.authorize,grant,subject);
     return {...permitted,subjectSha256:sha256(stableJson(inner))};
    },verifyCandidate:()=>{
     const measured=this.measure(context);
     check(stableJson(measured.descriptor)===stableJson(probe.descriptor)&&stableJson(measured.snapshot)===stableJson(probe.snapshot),'runtime_probe_changed');
     return measured.descriptor;
    }});
   if(rollbackGeneration===undefined){expectedInner=service.subject(probe.descriptor,'upgrade');return service.activate(probe.descriptor,request);}
   const target=service.history().find(row=>row.generation===rollbackGeneration);check(target,'runtime_generation_missing');
   expectedInner=service.subject(target.descriptor,'rollback');return service.rollback(rollbackGeneration,request);
  }finally{ledger.close();}
 }
}
