import{mkdirSync,readFileSync,writeFileSync,existsSync}from'node:fs';
import{spawnSync}from'node:child_process';
import{resolve,join}from'node:path';
import{pathToFileURL}from'node:url';
const plugin=process.cwd(),work=resolve('../../.local/filmcraft-recovery-01a11a34-20261008'),source=resolve('../../full-aigc-skills-repositories/filmcraft-skills');
const{PythonWorkflowRunner,fingerprintSkill}=await import(pathToFileURL(join(plugin,'src/adapters/python_workflow.ts')));
const out=join(work,'source48-actual-asset-issues');mkdirSync(out);const rows=[];
const issues=[{alias:'missingOne',origin:'plan',reason:'missing_file'},{alias:'missingTwo',origin:'plan',reason:'missing_file'},{alias:'changed',origin:'plan',reason:'digest_mismatch'}];
const suite=JSON.parse(readFileSync(join(source,'skill-suite.json')));
for(const{name}of suite.skills){
 const own=join(out,name);mkdirSync(own);const changed=join(own,'changed.png');writeFileSync(changed,'owned changed fixture');
 const plan=join(own,'plan.json'),output=join(own,'delivery'),runtimeHome=join(own,'runtime');
 writeFileSync(plan,JSON.stringify({document:{name:'Test',width:32,height:32,frameRate:{num:12,den:1}},operations:[],assets:{missingOne:{path:join(own,'missing-one.png'),sha256:'a'.repeat(64)},missingTwo:{path:join(own,'missing-two.wav'),sha256:'b'.repeat(64)},changed:{path:changed,sha256:'c'.repeat(64)}}}));
 const skill=join(source,'skills',name),before=fingerprintSkill(skill),runner=new PythonWorkflowRunner(null,null,{skillDirectory:skill,sourceRevision:'4e955df5a4d5d95e6ef27723223d3fafb0109dec',pluginVersion:'0.1.0-dev.65',runtimeHome,python:'[PYTHON]'});
 let caught;try{runner.prepare(plan,output);}catch(e){caught=e;}
 if(caught?.code!=='asset_preflight_failed'||JSON.stringify(caught.assetIssues)!==JSON.stringify(issues)){throw new Error('harness list mismatch:'+name+':'+caught);}
 const result=spawnSync('[PYTHON]',['-I','-B',join(skill,'scripts/workflow.py'),plan,'--output',output,'--runtime-home',runtimeHome],{encoding:'utf8',timeout:20000});
 const reply=JSON.parse(result.stdout);if(result.status!==1||JSON.stringify(reply.assetIssues)!==JSON.stringify(issues)||existsSync(output)||existsSync(runtimeHome)||fingerprintSkill(skill)!==before){throw new Error('public refusal boundary:'+name);}
 rows.push({skill:name,result:'PASS',sourceTreeSha256:before,issues:reply.assetIssues,harnessCode:caught.code,outputCreated:false,runtimeCreated:false,skillPreserved:true});
}
writeFileSync(join(out,'report.json'),JSON.stringify({schema:'filmcraft-source-actual-asset-issues/v1',result:'PASS',sourceRevision:'4e955df5a4d5d95e6ef27723223d3fafb0109dec',pluginCandidate:'0.1.0-dev.65',scope:'Actual source48 each13 skill public workflow CLI and new Harness preflight with owned missing/digest fixtures; no native installation, fixed plugin or creative acceptance.',rows},null,2)+'\n');console.log('PASS13 public CLI and13 Harness asset issue refusals; no installation/output, all skill bytes unchanged');
