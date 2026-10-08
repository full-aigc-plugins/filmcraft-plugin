import { writeFileSync } from 'node:fs';
import { qualityFixture } from '../test/harness/quality_fixtures.ts';
import { publicTask } from '../src/adapters/protocol_mapping.ts';

// 合成领域映射对象仅用于公共schema回归；不代表原生媒体或宿主通过。
const cleanup:(()=>void)[]=[];
try{
  const fixture=qualityFixture({after:(fn:()=>void)=>cleanup.push(fn)} as any);
  const task=publicTask(fixture.db,fixture.task.taskId,{schemaVersion:'filmcraft-native-workflow/v1'},
    {currency:'USD',maxMinorUnits:0,maxRevisions:1,maxExternalCalls:0});
  const receipt=fixture.service.index.collect(fixture.task.taskId,fixture.db.getTask(fixture.task.taskId).attemptId!);
  if(receipt.status!=='linked'){throw new Error('synthetic_mapping_unlinked');}
  writeFileSync(process.argv[2],JSON.stringify({source:'synthetic protocol mapping fixture; no runtime acceptance',
    publicTasks:[task],publicArtifacts:receipt.outputRefs},null,2)+'\n',{flag:'wx'});
}finally{for(const fn of cleanup.reverse()){fn();}}
