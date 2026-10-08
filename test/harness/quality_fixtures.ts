import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { TaskLedger } from '../../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../../src/artifacts/receipt_index.ts';
import { normalizePlan } from '../../src/adapters/plan_identity.ts';
import { ReviewService, reviewerIdentity } from '../../src/quality/review_service.ts';
import { reviewRequestHash } from '../../src/quality/review_contract.ts';
import type { ReviewCriteria, Assessment } from '../../src/quality/review_contract.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { binding, hash, workspace } from './fixtures.ts';

// 此 fixture 只证明 SQL/回执/隔离/失效规则，不声称合成字节是原生工程或视频。
export function qualityFixture(t:Parameters<typeof workspace>[0],projectBytes?:Buffer) {
  const root=workspace(t),output=join(root,'delivery');mkdirSync(output);mkdirSync(join(output,'assets'));
  const media=Buffer.from('synthetic input; not real media'),mediaHash=sha256(media);
  const snapshot={schema:'filmcraft-capability-snapshot/v1',mode:'headless',fixture:true};
  const files:Record<string,Buffer>={
    'plan.json':Buffer.from(JSON.stringify({assets:{still:{path:'input.png',sha256:mediaHash}}})),
    'project.fcproj':projectBytes??Buffer.from('synthetic project'), 'film.mp4':Buffer.from('synthetic film'),
    'assets/still.png':media,'exchange-loss.json':Buffer.from('{}'),
    'capabilities.json':Buffer.from(JSON.stringify({...snapshot,commandChecks:[],resourceChecks:[]})),
    'generator-private.txt':Buffer.from('generator self defense must not enter review'),
  };
  for(const [name,bytes] of Object.entries(files)){writeFileSync(join(output,name),bytes);}
  const identity=normalizePlan(join(output,'plan.json')),base=binding(root);
  const task={...base,planHash:identity.canonicalPlanSha256,nativePlanHash:identity.workflowPlanSha256,
    inputHashes:{still:mediaHash},inputRefs:[{assetId:'still',version:'fixture-v1',sha256:mediaHash}],
    runtimeIdentity:{...base.runtimeIdentity,capabilitySnapshotSha256:sha256(stableJson(snapshot))}};
  writeFileSync(join(output,'manifest.json'),JSON.stringify({schema:'filmcraft-delivery/v1',runtimeSha256:task.runtimeIdentity.sha256,
    sourceProjectSha256:null,assets:{still:{path:'assets/still.png',sha256:mediaHash}},
    files:Object.fromEntries(Object.entries(files).map(([name,bytes])=>[name,sha256(bytes)]))}));
  const db=new TaskLedger(join(root,'ledger.sqlite'));t.after(()=>db.close());db.register(task);
  const lease=db.claim(task.taskId,'worker',60_000);db.beginAttempt(lease,'native');db.markSubmitted(lease,123456);
  const index=new ReceiptIndex(db,join(root,'blobs')),execution='.filmcraft-execution-'+sha256(output)+'.json';
  writeFileSync(join(root,execution),JSON.stringify({schema:'filmcraft-output-execution/v1',targetHash:sha256(output),state:'finished',ownerPid:123456,
    context:{taskId:task.taskId,attemptId:lease.attemptId,sourceRevision:task.sourceRevision,sourceTreeSha256:task.sourceTreeSha256},
    identity:{planHash:task.nativePlanHash,inputHashes:task.inputHashes,projectRevision:null,runtimeSha256:task.runtimeIdentity.sha256}}));
  const linked=index.ingest(task.taskId,lease.attemptId,'delivery','manifest.json');
  index.ingest(task.taskId,lease.attemptId,'output-execution',execution);
  db.finishAttempt(lease,{outcome:'succeeded',stopped:true,receiptSha256:linked.sha256});
  const service=new ReviewService(db,index,join(root,'quality'));
  const criteria:ReviewCriteria={goal:{text:'明确的目标',constraints:['保留字幕'],audioRequired:false},
    rubric:{id:'test',version:'1',required:['decode','continuity'],thresholds:{syncToleranceMs:50,clippingAmplitude:.999,clippingFraction:1e-7}},
    reviewer:{id:'host-reviewer',kind:'host',version:'1',implementationSha256:hash()}};
  const assessment:Assessment={engineering:{status:'PASS',reason:'synthetic reopen',evidence:['fixture']},
    dimensions:{decode:{status:'PASS',reason:'synthetic decode',evidence:['fixture']},continuity:{status:'PASS',reason:'synthetic review',evidence:['fixture']}},
    evidenceCapabilities:['native-reopen','full-video','independent-creative-review']};
  const create=()=>service.create(task.taskId,criteria);
  const verify=(request:any)=>()=>({requestSha256:reviewRequestHash(request),reviewer:criteria.reviewer,contextId:'independent-host-context',
    independence:'host' as const,observedFiles:Object.fromEntries(Object.entries(request.subject.files).map(([name,file]:[string,any])=>[name,file.sha256]))});
  return {root,output,db,task,service,criteria,assessment,create,verify};
}
