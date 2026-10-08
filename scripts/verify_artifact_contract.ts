/** 固定安装内执行产物合同；使用自造素材，保留失败与原始回执，不提升创作接受。 */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { TaskLedger } from '../src/harness/task_ledger.ts';
import { ReceiptIndex } from '../src/artifacts/receipt_index.ts';
import { PythonWorkflowRunner } from '../src/adapters/python_workflow.ts';
import { publicTask } from '../src/adapters/protocol_mapping.ts';
import { ReviewService, reviewerIdentity } from '../src/quality/review_service.ts';
import { reviewRequestHash } from '../src/quality/review_contract.ts';
import { parseJson, sha256, stableJson } from '../src/support/json.ts';

const args = Object.fromEntries(Array.from({length:(process.argv.length-2)/2},(_,i)=>
  [process.argv[2+2*i].replace(/^--/,''),process.argv[3+2*i]]));
const plugin=resolve(dirname(fileURLToPath(import.meta.url)),'..'),root=resolve(args.output);
mkdirSync(root,{mode:0o700});
const lineageRoot=join(root,'lineage');
const child=spawnSync(process.execPath,[join(plugin,'scripts/verify_fixed_lineage.ts'),'--output',lineageRoot,
  '--python',args.python,'--source',args.source],{encoding:'utf8',timeout:900_000});
writeFileSync(join(root,'lineage.log'),child.stdout+child.stderr);
assert.equal(child.status,0,'lineage prerequisite failed; original log retained');
const lineage=parseJson(readFileSync(join(lineageRoot,'report.private.json'),'utf8'));
assert.equal(lineage.result,'PASS');assert.equal(lineage.cases.length,10);
const db=new TaskLedger(join(lineageRoot,'ledger.sqlite')),index=new ReceiptIndex(db,join(lineageRoot,'blobs'));
const task=db.getTask('create'),attempt=task.attemptId!,output=join(lineageRoot,'delivery');
const manifestFile=join(output,'manifest.json'),lossFile=join(output,'exchange-loss.json');
const manifestBytes=readFileSync(manifestFile),lossBytes=readFileSync(lossFile);
const projectHash=sha256(readFileSync(join(output,'project.fcproj')));
const cases:any[]=[],publicTasks=[...lineage.publicTasks],publicArtifacts=[...lineage.publicArtifacts];
function tree(path:string):Record<string,string>{
 const files:Record<string,string>={};
 function walk(at:string){for(const entry of readdirSync(at,{withFileTypes:true})){
  const file=join(at,entry.name);if(entry.isDirectory()){walk(file);}else{files[relative(path,file)]=sha256(readFileSync(file));}
 }}walk(path);return files;
}
try{
 assert.equal(index.collect('create',attempt).status,'linked');
 try{
  for(const [name,mutate,expected] of [
   ['missing-report-identity',(_r:any,m:any)=>{delete m.lossReport;},'unknown'],
   ['wrong-native-hash',(r:any)=>{r.native.sha256='0'.repeat(64);},'conflict'],
   ['wrong-inspection-hash',(r:any)=>{r.inspection.sha256='0'.repeat(64);},'conflict'],
   ['wrong-export-hash',(r:any)=>{r.outputs[0].sha256='0'.repeat(64);},'conflict'],
   ['lossy-native-substitute',(r:any)=>{r.outputs[0].nativeSubstitute=true;},'conflict'],
   ['font-fidelity-promotion',(r:any)=>{r.outputs[0].changes.find((x:any)=>x.code==='font-appearance').status='observed';},'conflict'],
   ['effect-fidelity-promotion',(r:any)=>{r.outputs[0].changes.find((x:any)=>x.code==='effect-keyframe-parameters').status='observed';},'conflict'],
   ['omitted-export',(r:any)=>{r.outputs.pop();},'conflict'],
   ['duplicate-export',(r:any)=>{r.outputs.push(structuredClone(r.outputs[0]));},'conflict'],
   ['broken-report',(_r:any,m:any)=>{m.brokenFixture=true;},'conflict'],
   ['wrong-report-declaration',(_r:any,m:any)=>{m.wrongDeclaration=true;},'conflict'],
   ['missing-report-file',(_r:any,m:any)=>{m.missingFile=true;},'stale'],
  ] as const){
   const loss=parseJson(lossBytes.toString()),manifest=parseJson(manifestBytes.toString());mutate(loss,manifest);
   const bytes=Buffer.from(manifest.brokenFixture?'{broken-json':JSON.stringify(loss));delete manifest.brokenFixture;
   const missingFile=manifest.missingFile;delete manifest.missingFile;
   manifest.files['exchange-loss.json']=sha256(bytes);if(manifest.lossReport){manifest.lossReport.sha256=manifest.wrongDeclaration?'0'.repeat(64):sha256(bytes);}
   delete manifest.wrongDeclaration;
   writeFileSync(lossFile,bytes);writeFileSync(manifestFile,JSON.stringify(manifest));
   if(missingFile){unlinkSync(lossFile);assert.throws(()=>index.inspect('create',attempt,'delivery','manifest.json'),/ENOENT/);}
   const status=missingFile?index.collect('create',attempt).status:index.inspect('create',attempt,'delivery','manifest.json').status;
   assert.equal(status,expected,name);
   assert.equal(index.collect('create',attempt).outputRefs.length,0);
   assert.equal(sha256(readFileSync(join(output,'project.fcproj'))),projectHash);
   cases.push({case:name,result:'PASS',status,nativeProjectPreserved:true,outputRefsCount:0,nativeProjectSha256:projectHash,
     layer:'modified receipts of actual native synthetic-media execution; no native replay'});
  }
 }finally{writeFileSync(manifestFile,manifestBytes);writeFileSync(lossFile,lossBytes);}
 assert.equal(index.collect('create',attempt).status,'linked');
 const native=join(lineageRoot,'runtime/filmcraft',task.binding.runtimeIdentity.cliVersion,'filmcraft-cli');
 const command={id:'artifact-independent-media',version:'1',executable:args.python,script:join(plugin,'scripts/review_media.py'),
   tools:{ffmpeg:args.ffmpeg,ffprobe:args.ffprobe,native}};
 const quality=new ReviewService(db,index,join(root,'quality'));
 const criteria={goal:{text:'Owned synthetic orange still; verify linkage and decode',constraints:[],audioRequired:false},
   rubric:{id:'artifact-lineage',version:'1',required:['decode'],thresholds:{syncToleranceMs:50,clippingAmplitude:.999,clippingFraction:.001}},
   reviewer:reviewerIdentity(command)};
 const created=quality.create('create',criteria),reviewed=quality.runExternal(created.requestRef,command);
 const evaluation=quality.readCurrent(created.requestRef,reviewed.receiptRef,criteria);
 assert.equal(evaluation.engineeringAcceptance,'PASS');assert.equal(evaluation.dimensions.decode.status,'PASS');
 assert.equal(evaluation.userAcceptance,'NOT_RUN');
 const qReceipt=parseJson(readFileSync(join(root,'quality',reviewed.receiptRef),'utf8'));
 assert.equal(qReceipt.requestSha256,reviewRequestHash(created.request));assert.equal(qReceipt.context.source,'external-process');
 assert.equal(created.request.subject.taskId,'create');assert.equal(created.request.subject.attemptId,attempt);
 assert.equal(created.request.subject.projectSha256,projectHash);
 assert.equal(created.request.subject.bindingSha256,sha256(stableJson(task.binding)));
 cases.push({case:'actual-quality-receipt-lineage',result:'PASS',requestRef:created.requestRef,receiptRef:reviewed.receiptRef,
   request:created.request,receipt:qReceipt,evaluation,binding:task.binding,attempt:db.verifyAttempt('create',attempt),state:db.getTask('create').state});
 const image=join(lineageRoot,'still.png'),parkedImage=join(lineageRoot,'unavailable-original-still.png');
 const moved=join(root,'moved-source'),parked=join(lineageRoot,'unavailable-original-delivery');
 cpSync(output,moved,{recursive:true});const movedBefore=tree(moved);
 renameSync(output,parked);renameSync(image,parkedImage);
 try{
  assert.equal(existsSync(output),false);assert.equal(existsSync(image),false);
  const revisionFile=join(root,'move-plan.json'),revisionOutput=join(root,'relinked');
  writeFileSync(revisionFile,JSON.stringify({expectedProjectSha256:projectHash,operations:[],frames:['0'],export:{audioRequired:false}}));
  const runner=new PythonWorkflowRunner(db,index,{python:args.python,skillDirectory:join(plugin,'skills/filmcraft-use'),
   sourceRevision:args.source,pluginVersion:lineage.pluginVersion,runtimeHome:join(lineageRoot,'runtime'),
   resources:{limits:{timeMs:900_000,diskBytes:128_000_000,outputBytes:128_000_000,slots:1,revisions:1},
    allocation:{timeMs:300_000,diskBytes:64_000_000,outputBytes:64_000_000,slots:1,revisions:1}}});
  const prepared=runner.prepare(revisionFile,revisionOutput,moved);
  const binding={...task.binding,taskId:'artifact-move',idempotencyKey:'artifact-move',outputRoot:prepared.outputRoot,
   projectKey:prepared.projectKey,projectRevision:prepared.projectRevision,planHash:prepared.planIdentity.canonicalPlanSha256,
   nativePlanHash:prepared.planIdentity.workflowPlanSha256,sourceTreeSha256:prepared.sourceTreeSha256,
   inputHashes:prepared.inputHashes,runtimeIdentity:prepared.runtimeIdentity,deadline:Date.now()+900_000};
  const result=await runner.run(binding,revisionFile,moved);assert.equal(result.state,'verifying');assert.equal(result.process!.stopped,true);
  const collected=index.collect(binding.taskId,result.attemptId!);assert.equal(collected.status,'linked');
  const revisedManifest=parseJson(readFileSync(join(revisionOutput,'manifest.json'),'utf8'));
  assert.equal(sha256(readFileSync(join(revisionOutput,'frame-0000.png'))),movedBefore['frame-0000.png']);
  assert.deepEqual(tree(moved),movedBefore);assert.equal(stableJson(prepared.inputHashes),stableJson(task.binding.inputHashes));
  assert.ok(readFileSync(join(revisionOutput,'decode.txt'),'utf8').includes('frames in'));
  publicTasks.push(publicTask(db,binding.taskId,{schemaVersion:'filmcraft-native-workflow/v1'},
    {currency:'USD',maxMinorUnits:0,maxRevisions:1,maxExternalCalls:0}));publicArtifacts.push(...collected.outputRefs);
  cases.push({case:'actual-moved-source-relink',result:'PASS',originalPathsUnavailable:true,sourcePreserved:true,
    pixelsUnchanged:true,fullDecode:true,inputHashes:prepared.inputHashes,projectSha256:revisedManifest.files['project.fcproj'],
    sourceProjectSha256:projectHash,collection:collected});
  const broken=join(root,'missing-dependency');cpSync(revisionOutput,broken,{recursive:true});
  const missing=join(broken,revisedManifest.assets.still.path);unlinkSync(missing);
  const brokenBefore=tree(broken),badFile=join(root,'missing-plan.json'),badOutput=join(root,'must-not-deliver');
  writeFileSync(badFile,JSON.stringify({expectedProjectSha256:revisedManifest.files['project.fcproj'],operations:[]}));
  assert.throws(()=>runner.prepare(badFile,badOutput,broken),/asset_digest_mismatch/);
  assert.deepEqual(tree(broken),brokenBefore);assert.equal(existsSync(badOutput),false);
  cases.push({case:'actual-missing-moved-dependency',result:'PASS',refused:true,sourcePreserved:true,successfulDeliveryExists:false});
 }finally{renameSync(parked,output);renameSync(parkedImage,image);}
 assert.equal(sha256(readFileSync(manifestFile)),sha256(manifestBytes));assert.equal(sha256(readFileSync(lossFile)),sha256(lossBytes));
 assert.equal(sha256(readFileSync(join(output,'project.fcproj'))),projectHash);assert.equal(index.collect('create',attempt).status,'linked');
 const report={schema:'filmcraft-artifact-contract-native/v1',result:'PASS',pluginVersion:lineage.pluginVersion,
  sourceRevision:args.source,runtimeIdentity:lineage.runtimeIdentity,lineage,cases,publicTasks,publicArtifacts,
  originalsRestored:true,nativeProjectPreserved:true,technicalAcceptance:'NOT_RUN',creativeAcceptance:'manual_review',
  userAcceptance:'NOT_RUN',otherPlatforms:'NOT_RUN',fullV1:'INCOMPLETE'};
 writeFileSync(join(root,'report.private.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({result:'PASS',lineageCases:10,artifactCases:cases.length,publicTasks:publicTasks.length,publicArtifacts:publicArtifacts.length}));
}finally{db.close();}
