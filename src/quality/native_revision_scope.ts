import { resolve } from 'node:path';
import { check, isHash, isObject, parseJson, sha256, stableJson } from '../support/json.ts';

export type RevisionScope={ownerPlugin:'filmcraft';sequenceId:string;trackId:string;objectId:string;
  startTick:string;endTick:string;fields:string[];dependencies:string[]};
export type RevisionIssue={id:string;target:string;command:'clip.speedDuration'|'clip.audioGain';params:Record<string,unknown>};
export type NativeSnapshot={sourceSha256:string;project:any;dependencyHashes:Record<string,string>};
export type CompiledRevision={sourceSha256:string;base:NativeSnapshot;targets:RevisionScope[];issues:RevisionIssue[];
  plan:{expectedProjectSha256:string;operations:any[];frames:string[];export:{audioRequired:boolean}}};
function exact(value:unknown,keys:string[]){check(isObject(value)&&Object.keys(value).sort().join(',')===[...keys].sort().join(','),'revision_scope_invalid');}
function identifier(value:unknown){return typeof value==='string'&&/^(0|[1-9][0-9]{0,19})$/.test(value);}
function tick(value:unknown){check((typeof value==='number'&&Number.isSafeInteger(value)||typeof value==='string')&&/^[0-9]+$/.test(String(value)),'revision_scope_invalid');return BigInt(String(value));}
function targetKey(scope:RevisionScope){return [scope.sequenceId,scope.trackId,scope.objectId].join('/');}
function clipIn(project:any,scope:RevisionScope){
  const item=project.project?.items?.[scope.sequenceId],sequence=item?.kind?.Sequence;
  check(sequence&&String(item.id)===scope.sequenceId,'revision_target_outside_scope');
  const tracks=[...(sequence.video_tracks??[]),...(sequence.audio_tracks??[])];
  const matches=tracks.filter(track=>String(track.id)===scope.trackId);check(matches.length===1,'revision_target_outside_scope');
  const clips=(matches[0].items??[]).filter((clip:any)=>String(clip.id)===scope.objectId);
  check(clips.length===1,'revision_target_outside_scope');return clips[0];
}
function leaf(object:any,path:string){
  check(typeof path==='string'&&/^\/(?:[A-Za-z0-9_]+\/)*[A-Za-z0-9_]+$/.test(path),'revision_field_scope_invalid');
  const names=path.slice(1).split('/');check(!names.some(name=>['__proto__','prototype','constructor'].includes(name)),'revision_field_scope_invalid');
  let parent=object;for(const name of names.slice(0,-1)){check(parent&&Object.hasOwn(parent,name),'revision_field_scope_invalid');parent=parent[name];}
  const key=names.at(-1)!;check(parent&&Object.hasOwn(parent,key)&&(!isObject(parent[key])&&!Array.isArray(parent[key])),'revision_field_scope_invalid');
  return {parent,key,value:parent[key]};
}
function within(clip:any,scope:RevisionScope){
  const start=tick(clip.start),duration=tick(clip.duration);
  check(duration>0n&&start>=tick(scope.startTick)&&start+duration<=tick(scope.endTick),'revision_time_outside_scope');
}
/** 只规范化同摘要且确实被打包的File路径；其它工程结构保持完整以便差异核验。 */
export function nativeSnapshot(bytes:Buffer,root:string,dependencies:Record<string,{path:string;sha256:string}>):NativeSnapshot{
  const project=parseJson(bytes.toString('utf8'));
  check(project.format==='filmcraft.project'&&project.schema_version===12&&isObject(project.project?.items),'revision_project_unsupported');
  const byPath=new Map<string,string>();const dependencyHashes:Record<string,string>={};
  for(const [name,value] of Object.entries(dependencies)){
    check(name.length>0&&typeof value.path==='string'&&isHash(value.sha256),'revision_dependency_changed');
    const path=resolve(root,value.path);check(!byPath.has(path)||byPath.get(path)===value.sha256,'revision_dependency_changed');
    byPath.set(path,value.sha256);dependencyHashes[name]=value.sha256;
  }
  for(const item of Object.values(project.project.items) as any[]){
    const file=item.kind?.Media?.media?.File;
    if(file&&typeof file.path==='string'){
      const digest=byPath.get(resolve(root,file.path));if(digest){file.path={packagedSha256:digest};}
    }
  }
  return {sourceSha256:sha256(bytes),project,dependencyHashes};
}
/** 将结构化问题编译为固定clip的原生计划，禁止ripple、新依赖及任意命令。 */
export function compileRevision(base:NativeSnapshot,expectedSourceSha256:string,scopes:RevisionScope[],issues:RevisionIssue[],audioRequired=false):CompiledRevision{
  check(isHash(expectedSourceSha256)&&base.sourceSha256===expectedSourceSha256,'revision_source_stale');
  check(Array.isArray(scopes)&&scopes.length>0&&scopes.length<=128&&Array.isArray(issues)&&issues.length>0&&issues.length<=128,'revision_scope_invalid');
  const all=new Map<string,RevisionScope>();
  for(const scope of scopes){
    exact(scope,['ownerPlugin','sequenceId','trackId','objectId','startTick','endTick','fields','dependencies']);
    check(scope.ownerPlugin==='filmcraft'&&[scope.sequenceId,scope.trackId,scope.objectId].every(identifier)
      &&tick(scope.endTick)>tick(scope.startTick)&&Array.isArray(scope.fields)&&scope.fields.length>0
      &&new Set(scope.fields).size===scope.fields.length&&Array.isArray(scope.dependencies)
      &&new Set(scope.dependencies).size===scope.dependencies.length,'revision_scope_invalid');
    const key=targetKey(scope);check(!all.has(key),'revision_scope_invalid');all.set(key,scope);
    const clip=clipIn(base.project,scope);within(clip,scope);
    const timeIndex=(clip.effects??[]).findIndex((effect:any)=>effect.effect==='time_remap');
    const editable=['/speed','/reverse','/duration','/gain_db',`/effects/${timeIndex}/params/speed/value/Float`];
    for(const field of scope.fields){check(editable.includes(field),'revision_field_scope_invalid');leaf(clip,field);}
    check(scope.dependencies.every(name=>Object.hasOwn(base.dependencyHashes,name)),'revision_dependency_changed');
    const referenced=base.project.project.items[String(clip.item)]?.kind?.Media?.media?.File?.path?.packagedSha256;
    check(isHash(referenced)&&scope.dependencies.some(name=>base.dependencyHashes[name]===referenced),'revision_dependency_changed');
  }
  const operations:any[]=[],targets:RevisionScope[]=[],ids=new Set();
  for(const issue of issues){
    exact(issue,['id','target','command','params']);check(typeof issue.id==='string'&&issue.id.length>0&&issue.id.length<=256
      &&!ids.has(issue.id)&&isObject(issue.params),'revision_issue_invalid');ids.add(issue.id);
    const scope=all.get(issue.target);check(scope&&!targets.some(value=>targetKey(value)===issue.target),'revision_target_outside_scope');targets.push(scope);
    const id=Number(scope.objectId);check(Number.isSafeInteger(id),'revision_native_id_unsupported');
    const params=issue.params;
    if(issue.command==='clip.speedDuration'){
      exact(params,['speed','reverse','ripple']);check(typeof params.speed==='number'&&Number.isFinite(params.speed)&&params.speed>0&&params.speed<=10000
        &&typeof params.reverse==='boolean'&&params.ripple===false,'revision_issue_invalid');
      check(['/speed','/reverse','/duration'].every(field=>scope.fields.includes(field)),'revision_field_scope_invalid');
    }else{
      check(issue.command==='clip.audioGain','revision_command_unsupported');exact(params,['mode','db','relative']);
      check(params.mode==='set'&&params.relative===false&&typeof params.db==='number'&&Number.isFinite(params.db)&&Math.abs(params.db)<=120
        &&scope.fields.includes('/gain_db'),'revision_issue_invalid');
    }
    operations.push({command:'timeline.select',params:{clips:[id],add:false,toggle:false}});
    operations.push({command:'native.command',params:{command:issue.command,params:{...params,...(issue.command==='clip.speedDuration'?{clips:[id]}:{})}}});
  }
  return JSON.parse(stableJson({sourceSha256:base.sourceSha256,base,targets,issues,
    plan:{expectedProjectSha256:base.sourceSha256,operations,frames:['0'],export:{audioRequired}}}));
}
/** 完整语义差异只允许当前轮目标叶字段；依赖、其它轨道和对象不能被掩盖。 */
export function assertRevisionDiff(compiled:CompiledRevision,after:NativeSnapshot){
  check(stableJson(compiled.base.dependencyHashes)===stableJson(after.dependencyHashes),'revision_dependency_changed');
  const before=structuredClone(compiled.base.project),candidate=structuredClone(after.project),changes:any[]=[];
  for(const scope of compiled.targets){
    const original=clipIn(before,scope),modified=clipIn(candidate,scope);within(modified,scope);
    const issue=compiled.issues.find(value=>value.target===targetKey(scope))!;
    if(issue.command==='clip.speedDuration'){
      check(modified.speed===Number(issue.params.speed)/100&&modified.reverse===issue.params.reverse,'revision_target_not_applied');
    }else{check(modified.gain_db===issue.params.db,'revision_target_not_applied');}
    for(const field of scope.fields){
      const left=leaf(original,field),right=leaf(modified,field);
      if(stableJson(left.value)!==stableJson(right.value)){changes.push({target:targetKey(scope),field,before:left.value,after:right.value});}
      left.parent[left.key]='__scoped_leaf__';right.parent[right.key]='__scoped_leaf__';
    }
  }
  check(stableJson(before)===stableJson(candidate),'revision_scope_violation');
  return {changes,nonTargetsPreserved:true,dependenciesPreserved:true,sourceSha256:compiled.sourceSha256,candidateSha256:after.sourceSha256};
}
/** 已满足的结构化问题只从当前原生字段计算，不使用生成器自评。 */
export function appliedIssueIds(snapshot:NativeSnapshot,scopes:RevisionScope[],issues:RevisionIssue[]){
  return issues.filter(issue=>{
    const scope=scopes.find(value=>targetKey(value)===issue.target);check(scope,'revision_target_outside_scope');
    const clip=clipIn(snapshot.project,scope);
    return issue.command==='clip.speedDuration'?clip.speed===Number(issue.params.speed)/100&&clip.reverse===issue.params.reverse
      :clip.gain_db===issue.params.db;
  }).map(issue=>issue.id);
}
