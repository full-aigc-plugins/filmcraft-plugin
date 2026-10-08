import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createReviewRequest, evaluateReview, reviewRequestHash } from '../../src/quality/review_contract.ts';
import { hash } from './fixtures.ts';

function fixture() {
  const subject = { taskId:'task',attemptId:'attempt',epoch:1,bindingSha256:hash(),candidateSha256:hash('b'),
    projectSha256:hash('c'),inputHashes:{input:hash('d')},executionSha256:hash('e'),
    files:{'film.mp4':{sha256:hash('f'),bytes:12},'project.fcproj':{sha256:hash('c'),bytes:10}} };
  const criteria={goal:{text:'A clear short film',constraints:['audible speech'],audioRequired:true},
    rubric:{id:'film-quality',version:'1',required:['decode','videoTiming','audioClipping','avSync','subtitleTiming','subtitleReadability','continuity','rhythm'],
      thresholds:{syncToleranceMs:50,clippingAmplitude:0.999,clippingFraction:0.001}},
    reviewer:{id:'independent-reviewer',kind:'external',version:'1',implementationSha256:hash('a')} };
  const request=createReviewRequest(subject,criteria);
  const result={engineering:{status:'PASS',reason:'independent project reopen',evidence:['native-reopen']},dimensions:Object.fromEntries(criteria.rubric.required.map(name=>[name,{status:'PASS',reason:'measured',evidence:['full-media']}]))};
  return {subject,criteria,request,result};
}
test('request binds candidate, project, input, goal, rubric, execution and reviewer identities without generator commentary',()=>{
  const {subject,criteria,request}=fixture();assert.equal(request.subject.candidateSha256,subject.candidateSha256);
  assert.equal(request.criteria.reviewer.id,criteria.reviewer.id);
  assert.throws(()=>createReviewRequest(subject,{...criteria,generatorRationale:'I made it perfect'}),/unexpected_review_field/);
  assert.throws(()=>createReviewRequest({...subject,generatorSelfScore:5},criteria),/unexpected_review_field/);
});
test('a high creative score cannot cover a real decode failure or manufacture user acceptance',()=>{
  const {request,result}=fixture();result.dimensions.decode.status='FAIL';result.dimensions.decode.reason='full media cannot decode';
  const report=evaluateReview(request,{...result,creativeScore:5});
  assert.equal(report.technicalAcceptance,'FAIL');assert.equal(report.decision,'blocked');assert.equal(report.userAcceptance,'NOT_RUN');
});
test('a known technical failure blocks even when the rubric did not request that dimension',()=>{
  const {request,result}=fixture();request.criteria.goal.audioRequired=false;request.criteria.rubric.required=['decode'];
  result.dimensions.avSync.status='FAIL';
  const report=evaluateReview(request,{...result,creativeScore:5,evidenceCapabilities:['full-video','native-reopen']});
  assert.equal(report.technicalAcceptance,'FAIL');assert.equal(report.decision,'blocked');
});
test('a static frame cannot pass synchronization, clipping, subtitle timing, continuity or rhythm',()=>{
  const {request,result}=fixture();
  const report=evaluateReview(request,{...result,evidenceCapabilities:['static-frame']});
  for(const name of ['avSync','audioClipping','subtitleTiming','subtitleReadability','continuity','rhythm']){
    assert.ok(['NOT_RUN','manual_review'].includes(report.dimensions[name].status),name);
  }
  assert.equal(report.decision,'manual_review');
});
test('missing temporal evidence is explicit and cannot become PASS from an empty required set',()=>{
  const {request}=fixture();const report=evaluateReview(request,{engineering:{status:'NOT_RUN',reason:'no native engine',evidence:[]},dimensions:{},evidenceCapabilities:[]});
  assert.equal(report.engineeringAcceptance,'NOT_RUN');assert.equal(report.technicalAcceptance,'NOT_RUN');
  assert.equal(report.creativeAcceptance,'manual_review');assert.equal(report.userAcceptance,'NOT_RUN');
});
test('even complete independent quality PASS is review-ready rather than user-accepted or completed',()=>{
  const {request,result}=fixture();const report=evaluateReview(request,{...result,evidenceCapabilities:['native-reopen','full-video','decoded-audio','caption-timeline','independent-creative-review','content-sync']});
  assert.equal(report.decision,'review_ready');assert.equal(report.userAcceptance,'NOT_RUN');
  assert.throws(()=>evaluateReview(request,{...result,userAcceptance:'PASS'}),/unexpected_review_field/);
});
for(const field of ['candidate','project','inputs','execution','goal','rubric','reviewer'] as const){
  test('changing '+field+' changes the review identity and invalidates the old request',()=>{
    const {subject,criteria,request}=fixture(), modified=structuredClone({subject,criteria});
    if(field==='candidate'){modified.subject.candidateSha256=hash('0');}
    if(field==='project'){modified.subject.projectSha256=hash('0');modified.subject.files['project.fcproj'].sha256=hash('0');}
    if(field==='inputs'){modified.subject.inputHashes.input=hash('0');}
    if(field==='execution'){modified.subject.executionSha256=hash('0');}
    if(field==='goal'){modified.criteria.goal.text='Different goal';}
    if(field==='rubric'){modified.criteria.rubric.version='2';}
    if(field==='reviewer'){modified.criteria.reviewer.version='2';}
    const next=createReviewRequest(modified.subject,modified.criteria,{requestId:request.requestId,createdAt:request.createdAt});
    assert.notEqual(reviewRequestHash(next),reviewRequestHash(request));
  });
}
