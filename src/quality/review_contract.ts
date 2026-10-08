import { randomUUID } from 'node:crypto';
import { check, isHash, isObject, sha256, stableJson } from '../support/json.ts';

export const DIMENSIONS = ['decode','videoTiming','audioClipping','avSync','subtitleTiming','subtitleReadability','continuity','rhythm'] as const;
export type Dimension = typeof DIMENSIONS[number];
export type ReviewStatus = 'PASS' | 'FAIL' | 'NOT_RUN' | 'manual_review';
export type Finding = { status: ReviewStatus; reason: string; evidence: string[]; metrics?: Record<string,unknown> };
export type ReviewerIdentity = { id: string; kind: 'host' | 'external' | 'manual'; version: string; implementationSha256: string };
export type ReviewCriteria = { goal: { text: string; constraints: string[]; audioRequired: boolean;
    expectedDurationMs?:number; syncMarkers?:{kind:'flash-pulse';expectedEvents:number} };
  rubric: { id: string; version: string; required: Dimension[]; thresholds: { syncToleranceMs: number; clippingAmplitude: number; clippingFraction: number } };
  reviewer: ReviewerIdentity };
export type ReviewSubject = { taskId: string; attemptId: string; epoch: number; bindingSha256: string; candidateSha256: string;
  projectSha256: string; inputHashes: Record<string,string>; executionSha256: string;
  files: Record<string,{sha256:string;bytes:number}> };
export type ReviewRequest = { schema: 'filmcraft-review-request/v1'; requestId: string; createdAt: number; subject: ReviewSubject; criteria: ReviewCriteria };
export type Assessment = { engineering: Finding; dimensions: Partial<Record<Dimension,Finding>>; creativeScore?: number; evidenceCapabilities?: string[] };
const capabilities = ['static-frame','native-reopen','full-video','decoded-audio','caption-timeline','independent-creative-review','content-sync'];
const technical: Dimension[] = ['decode','videoTiming','audioClipping','avSync','subtitleTiming'];
const creative: Dimension[] = ['subtitleReadability','continuity','rhythm'];
function exact(value: unknown, required: string[], optional: string[] = []) {
  check(isObject(value) && required.every(key=>Object.hasOwn(value,key))
    && Object.keys(value).every(key=>required.includes(key)||optional.includes(key)), 'unexpected_review_field');
}
function text(value: unknown, limit = 4096) { return typeof value === 'string' && value.length > 0 && value.length <= limit; }
export function validateCriteria(criteria: ReviewCriteria) {
  exact(criteria,['goal','rubric','reviewer']); exact(criteria.goal,['text','constraints','audioRequired'],['expectedDurationMs','syncMarkers']);
  check(text(criteria.goal.text) && Array.isArray(criteria.goal.constraints) && criteria.goal.constraints.length <= 64
    && criteria.goal.constraints.every(item=>text(item)) && typeof criteria.goal.audioRequired === 'boolean','invalid_review_goal');
  if(criteria.goal.expectedDurationMs!==undefined){check(Number.isFinite(criteria.goal.expectedDurationMs)&&criteria.goal.expectedDurationMs>0,'invalid_review_goal');}
  if(criteria.goal.syncMarkers!==undefined){exact(criteria.goal.syncMarkers,['kind','expectedEvents']);
    check(criteria.goal.syncMarkers.kind==='flash-pulse'&&Number.isSafeInteger(criteria.goal.syncMarkers.expectedEvents)
      &&criteria.goal.syncMarkers.expectedEvents>0&&criteria.goal.syncMarkers.expectedEvents<=1000,'invalid_review_goal');}
  exact(criteria.rubric,['id','version','required','thresholds']);
  check(text(criteria.rubric.id,128) && text(criteria.rubric.version,128) && Array.isArray(criteria.rubric.required)
    && criteria.rubric.required.includes('decode') && new Set(criteria.rubric.required).size===criteria.rubric.required.length
    && criteria.rubric.required.every(name=>DIMENSIONS.includes(name)),'invalid_review_rubric');
  check(!criteria.goal.audioRequired||criteria.rubric.required.includes('audioClipping'),'invalid_review_rubric');
  const thresholds=criteria.rubric.thresholds;exact(thresholds,['syncToleranceMs','clippingAmplitude','clippingFraction']);
  check(Number.isFinite(thresholds.syncToleranceMs) && thresholds.syncToleranceMs>=0 && thresholds.syncToleranceMs<=1000
    && Number.isFinite(thresholds.clippingAmplitude) && thresholds.clippingAmplitude>0 && thresholds.clippingAmplitude<=1
    && Number.isFinite(thresholds.clippingFraction) && thresholds.clippingFraction>=0 && thresholds.clippingFraction<=1,'invalid_review_rubric');
  exact(criteria.reviewer,['id','kind','version','implementationSha256']);
  check(text(criteria.reviewer.id,128) && text(criteria.reviewer.version,128)
    && ['host','external','manual'].includes(criteria.reviewer.kind) && isHash(criteria.reviewer.implementationSha256),'invalid_reviewer_identity');
}
export function createReviewRequest(subject: ReviewSubject, criteria: ReviewCriteria, identity: {requestId?:string;createdAt?:number} = {}): ReviewRequest {
  validateCriteria(criteria);exact(subject,['taskId','attemptId','epoch','bindingSha256','candidateSha256','projectSha256','inputHashes','executionSha256','files']);
  check(text(subject.taskId,256) && text(subject.attemptId,256) && Number.isSafeInteger(subject.epoch) && subject.epoch>0
    && ['bindingSha256','candidateSha256','projectSha256','executionSha256'].every(key=>isHash((subject as any)[key]))
    && isObject(subject.inputHashes) && Object.values(subject.inputHashes).every(isHash) && isObject(subject.files),'invalid_review_subject');
  check(Object.keys(subject.files).length>0 && Object.keys(subject.files).length<=50_000,'invalid_review_subject');
  for(const [name,file] of Object.entries(subject.files)){
    exact(file,['sha256','bytes']);check(name.length<=4096 && !name.startsWith('/') && !name.includes('\\')
      && name.split('/').every(part=>part!==''&&part!=='.'&&part!=='..')
      && isHash(file.sha256) && Number.isSafeInteger(file.bytes) && file.bytes>=0,'invalid_review_subject');
  }
  check(subject.files['project.fcproj']?.sha256===subject.projectSha256,'invalid_review_subject');
  const requestId=identity.requestId??randomUUID(),createdAt=identity.createdAt??Date.now();
  check(text(requestId,256)&&Number.isSafeInteger(createdAt),'invalid_review_request');
  return JSON.parse(stableJson({schema:'filmcraft-review-request/v1',requestId,createdAt,subject,criteria}));
}
export function reviewRequestHash(request: ReviewRequest) {
  check(request.schema==='filmcraft-review-request/v1','invalid_review_request');
  exact(request,['schema','requestId','createdAt','subject','criteria']);
  createReviewRequest(request.subject,request.criteria,{requestId:request.requestId,createdAt:request.createdAt});
  return sha256(stableJson(request));
}
function finding(value: Finding) {
  exact(value,['status','reason','evidence'],['metrics']);
  check(['PASS','FAIL','NOT_RUN','manual_review'].includes(value.status)&&text(value.reason)
    && Array.isArray(value.evidence)&&value.evidence.length<=256&&value.evidence.every(item=>text(item,256))
    && (value.status!=='PASS'||value.evidence.length>0) && (value.metrics===undefined||isObject(value.metrics)), 'invalid_review_finding');
  stableJson(value);return JSON.parse(stableJson(value)) as Finding;
}
function aggregate(values: Finding[], missing: ReviewStatus): ReviewStatus {
  if(values.some(value=>value.status==='FAIL')){return 'FAIL';}
  if(!values.length){return missing;}
  if(values.some(value=>value.status==='manual_review')){return 'manual_review';}
  if(values.some(value=>value.status==='NOT_RUN')){return missing;}
  return 'PASS';
}
/** 门禁只计算独立评审结果；高分、缺失证据或静态帧不代替技术及用户接受。 */
export function evaluateReview(request: ReviewRequest, assessment: Assessment) {
  reviewRequestHash(request);exact(assessment,['engineering','dimensions'],['creativeScore','evidenceCapabilities']);
  check(isObject(assessment.dimensions)&&Object.keys(assessment.dimensions).every(name=>DIMENSIONS.includes(name as Dimension)),'invalid_review_finding');
  if(assessment.creativeScore!==undefined){check(Number.isFinite(assessment.creativeScore)&&assessment.creativeScore>=0&&assessment.creativeScore<=5,'invalid_review_score');}
  const supplied=assessment.evidenceCapabilities??[];
  check(Array.isArray(supplied)&&new Set(supplied).size===supplied.length&&supplied.every(item=>capabilities.includes(item)),'invalid_review_capability');
  const evidence=new Set(supplied),engineering=finding(assessment.engineering),dimensions:Record<string,Finding>={};
  if(engineering.status==='PASS'&&!evidence.has('native-reopen')){
    engineering.status='NOT_RUN';engineering.reason='Independent native reopen evidence is missing';
  }
  const requirements:Record<Dimension,string[]>={decode:['full-video'],videoTiming:['full-video'],audioClipping:['decoded-audio'],
    avSync:['full-video','decoded-audio','content-sync'],subtitleTiming:['full-video','caption-timeline'],
    subtitleReadability:['full-video','caption-timeline','independent-creative-review'],continuity:['full-video','independent-creative-review'],
    rhythm:['full-video','decoded-audio','independent-creative-review']};
  for(const name of DIMENSIONS){
    const value=assessment.dimensions[name]?finding(assessment.dimensions[name]!):{
      status:creative.includes(name)?'manual_review':'NOT_RUN',reason:'Independent evidence or capability is missing',evidence:[]} as Finding;
    if(value.status==='PASS'&&!requirements[name].every(item=>evidence.has(item))){
      value.status=creative.includes(name)?'manual_review':'NOT_RUN';value.reason='Required temporal/audio/independent evidence is missing';
    }
    dimensions[name]=value;
  }
  const required=request.criteria.rubric.required;
  const technicalAcceptance=technical.some(name=>dimensions[name].status==='FAIL')?'FAIL'
    :aggregate(technical.filter(name=>required.includes(name)).map(name=>dimensions[name]),'NOT_RUN');
  const creativeAcceptance=aggregate(creative.filter(name=>required.includes(name)).map(name=>dimensions[name]),'manual_review');
  const engineeringAcceptance=engineering.status;
  const decision=engineeringAcceptance==='FAIL'||technicalAcceptance==='FAIL'?'blocked'
    :engineeringAcceptance==='PASS'&&technicalAcceptance==='PASS'&&creativeAcceptance==='PASS'?'review_ready':'manual_review';
  return {requestSha256:reviewRequestHash(request),engineering,dimensions,engineeringAcceptance,technicalAcceptance,creativeAcceptance,
    userAcceptance:'NOT_RUN' as const,creativeScore:assessment.creativeScore??null,decision};
}
