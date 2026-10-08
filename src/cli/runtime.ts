import {AssetPreflightRefusal} from '../adapters/asset_refusal.ts';
import { parseArgs } from 'node:util';
import { basename, dirname, resolve } from 'node:path';
import { RuntimeUpgrade } from '../adapters/runtime_upgrade.ts';
import { CapabilityRefusal } from '../adapters/capability_refusal.ts';
import { LocalAuthorizationStore } from '../harness/authorization.ts';
import { readBoundFile } from '../artifacts/receipt_index.ts';
import { check, HarnessError, parseJson } from '../support/json.ts';
/** 宿主运行时升级入口；仅使用已有私有授权，不自行创建许可或自动重试。 */
function main(){
 const {values:v,positionals:p}=parseArgs({allowPositionals:true,options:{help:{type:'boolean'},candidate:{type:'string'},plan:{type:'string'},ledger:{type:'string'},
  'runtime-home':{type:'string'},python:{type:'string'},probe:{type:'string'},generation:{type:'string'},'authorization-root':{type:'string'},'authorization-ref':{type:'string'},'authorization-scope-sha256':{type:'string'}}});
 if(v.help){console.log('node src/cli/runtime.ts probe-subject|probe|subject|activate|rollback --candidate FILE --plan FILE --ledger FILE --runtime-home DIR [--python FILE]\nprobe: --authorization-root DIR --authorization-ref REF --authorization-scope-sha256 SHA\nsubject/activate/rollback: --probe FILE [--generation INTEGER for rollback subject and rollback]\nactivate/rollback additionally require the existing exact private host grant. Probe and selection are separate grants; no edits are replayed.');return;}
 check(p.length===1&&['probe-subject','probe','subject','activate','rollback'].includes(p[0])&&v.candidate&&v.plan&&v.ledger&&v['runtime-home'],'invalid_runtime_arguments');
 const service=new RuntimeUpgrade({candidateFile:v.candidate,planFile:v.plan,ledgerFile:v.ledger,runtimeHome:v['runtime-home'],python:v.python},
  v['authorization-root']?new LocalAuthorizationStore(v['authorization-root']).authorize:undefined);
 if(p[0]==='probe-subject'){console.log(JSON.stringify(service.probeSubject()));return;}
 const grant={authorizationRef:v['authorization-ref']!,authorizationScopeSha256:v['authorization-scope-sha256']!};
 if(p[0]==='probe'){console.log(JSON.stringify(service.probe(grant)));return;}
 check(v.probe,'invalid_runtime_arguments');const path=resolve(v.probe),probe=parseJson(readBoundFile(dirname(path),basename(path)).toString('utf8'));
 const generation=v.generation===undefined?undefined:Number(v.generation);
 if(p[0]==='subject'){console.log(JSON.stringify(service.selectionSubject(probe,generation)));return;}
 check(p[0]==='rollback'?generation!==undefined:generation===undefined,'invalid_runtime_arguments');
 console.log(JSON.stringify(service.select(probe,grant,generation)));
}
try{main();}catch(error){console.log(JSON.stringify({schema:'filmcraft-runtime-upgrade-error/v1',replayAllowed:false,error:{code:error instanceof HarnessError?error.code:'runtime_upgrade_failed',...(error instanceof CapabilityRefusal&&error.diagnostic?{diagnostic:error.diagnostic}:{}),...(error instanceof AssetPreflightRefusal?{assetIssues:error.assetIssues}:{})}}));process.exitCode=1;}
