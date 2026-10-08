import { test } from 'node:test';
import assert from 'node:assert/strict';
import { nativeSnapshot, compileRevision, assertRevisionDiff } from '../../src/quality/native_revision_scope.ts';
import { hash } from './fixtures.ts';

function fixture(){
  const clip={id:9,item:8,start:0,duration:100,speed:1,reverse:false,gain_db:0,
    effects:[{effect:'time_remap',params:{speed:{value:{Float:100}}}}]};
  const project={format:'filmcraft.project',schema_version:12,project:{items:{
    '7':{id:7,kind:{Sequence:{video_tracks:[{id:1,items:[clip],name:'V1'},{id:2,items:[],name:'V2'}],audio_tracks:[]}}},
    '8':{id:8,kind:{Media:{media:{File:{path:'/original/still.png'}}}}}}}};
  const dependencies={still:{path:'still.png',sha256:hash()}};
  const before=nativeSnapshot(Buffer.from(JSON.stringify(project)),'/original',dependencies);
  const scope={ownerPlugin:'filmcraft',sequenceId:'7',trackId:'1',objectId:'9',startTick:'0',endTick:'100',
    fields:['/speed','/reverse','/duration','/effects/0/params/speed/value/Float'],dependencies:['still']};
  const issue={id:'speed',target:'7/1/9',command:'clip.speedDuration',params:{speed:200,reverse:false,ripple:false}};
  const compiled=compileRevision(before,before.sourceSha256,[scope],[issue]);
  const after=structuredClone(project),target=after.project.items['7'].kind.Sequence.video_tracks[0].items[0];
  target.speed=2;target.duration=50;target.effects[0].params.speed.value.Float=200;
  after.project.items['8'].kind.Media.media.File.path='/candidate/still.png';
  return {before,scope,issue,compiled,after,dependencies,project};
}
test('local scope compiles pinned source, target and no-ripple commands; relocation retains identity',()=>{
  const f=fixture(),after=nativeSnapshot(Buffer.from(JSON.stringify(f.after)),'/candidate',f.dependencies);
  assert.equal(f.compiled.plan.expectedProjectSha256,f.before.sourceSha256);
  assert.equal(f.compiled.plan.operations[1].params.params.ripple,false);
  const diff=assertRevisionDiff(f.compiled,after);assert.equal(diff.changes.length,3);assert.equal(diff.nonTargetsPreserved,true);
});
test('stale project and unknown target reject before a native plan can be used',()=>{
  const f=fixture();assert.throws(()=>compileRevision(f.before,hash('f'),[f.scope],[f.issue]),/revision_source_stale/);
  assert.throws(()=>compileRevision(f.before,f.before.sourceSha256,[f.scope],[{...f.issue,target:'7/2/9'}]),/revision_target_outside_scope/);
});
for(const change of ['field','track','dependency','interval','wrong-result'] as const){
  test('revision rejects '+change+' drift rather than approving the candidate',()=>{
    const f=fixture();const clip=f.after.project.items['7'].kind.Sequence.video_tracks[0].items[0];
    if(change==='field'){clip.gain_db=8;}
    if(change==='track'){f.after.project.items['7'].kind.Sequence.video_tracks[1].name='changed';}
    if(change==='dependency'){f.dependencies.still.sha256=hash('f');}
    if(change==='interval'){clip.start=90;}
    if(change==='wrong-result'){clip.speed=3;}
    const after=nativeSnapshot(Buffer.from(JSON.stringify(f.after)),'/candidate',f.dependencies);
    assert.throws(()=>assertRevisionDiff(f.compiled,after),/revision_(scope_violation|dependency_changed|time_outside_scope|target_not_applied)/);
  });
}
test('unsupported operation, ripple, owner, broad object field and dependency scope are refused',()=>{
  const f=fixture();
  for(const issue of [{...f.issue,command:'file.new'},{...f.issue,params:{...f.issue.params,ripple:true}},
    {...f.issue,params:{...f.issue.params,clips:[999]}}]){
    assert.throws(()=>compileRevision(f.before,f.before.sourceSha256,[f.scope],[issue]),/revision_/);
  }
  for(const scope of [{...f.scope,ownerPlugin:'effectcraft'},{...f.scope,fields:['/effects']},{...f.scope,dependencies:[]}]){
    assert.throws(()=>compileRevision(f.before,f.before.sourceSha256,[scope],[f.issue]),/revision_/);
  }
});
