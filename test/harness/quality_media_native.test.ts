import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { createReviewRequest, evaluateReview, reviewRequestHash } from '../../src/quality/review_contract.ts';
import { reviewerIdentity } from '../../src/quality/review_service.ts';
import { sha256, stableJson } from '../../src/support/json.ts';
import { captureEvidence, hash, workspace } from './fixtures.ts';

test('actual temporal/audio fixtures detect synchronization, per-channel clipping and decode failure',
  {skip:!process.env.FILMCRAFT_QUALITY_TOOLS,timeout:120_000},t=>{
    const root=workspace(t),tools=JSON.parse(process.env.FILMCRAFT_QUALITY_TOOLS!);
    assert.ok(tools.ffmpeg&&tools.ffprobe,'explicit existing measurement tools required');
    const command={id:'filmcraft-independent-media',version:'1',executable:process.env.FILMCRAFT_PYTHON!,
      script:new URL('../../scripts/review_media.py',import.meta.url).pathname,tools};
    assert.ok(command.executable,'explicit Python path required');
    const criteria={goal:{text:'Controlled two-flash two-pulse calibration',constraints:['2 seconds','generated calibration, no external assets'],
      audioRequired:true,expectedDurationMs:2000,syncMarkers:{kind:'flash-pulse',expectedEvents:2}},
      rubric:{id:'temporal-calibration',version:'1',required:['decode','videoTiming','audioClipping','avSync','subtitleTiming','subtitleReadability','continuity','rhythm'],
        thresholds:{syncToleranceMs:50,clippingAmplitude:.999,clippingFraction:.001}},reviewer:reviewerIdentity(command)};
    function measure(name:string,options:{delay?:number;clipped?:boolean;broken?:boolean;noAudio?:boolean;badSubtitle?:boolean;noTools?:boolean}={}){
      const folder=join(root,name);mkdirSync(folder);const film=join(folder,'film.mp4');
      const delay=options.delay??0;
      const source=options.clipped?'aevalsrc=1|-1:s=48000:d=2'
        :`aevalsrc=0.4*between(t\\,${.48+delay}\\,${.54+delay})+0.4*between(t\\,${1.48+delay}\\,${1.54+delay}):s=48000:d=2`;
      const args=['-v','error','-nostdin','-f','lavfi','-i','color=c=black:s=32x32:r=25:d=2'];
      if(!options.noAudio){args.push('-f','lavfi','-i',source);}
      args.push('-vf','drawbox=color=white:t=fill:enable=between(t\\,0.48\\,0.56)+between(t\\,1.48\\,1.56)',
        '-c:v','libx264','-pix_fmt','yuv420p','-c:a','pcm_f32le','-f','matroska',film);
      if(options.broken){writeFileSync(film,'corrupt media fixture');}
      else{const generated=spawnSync(tools.ffmpeg,args,{encoding:'utf8',timeout:20_000});assert.equal(generated.status,0,generated.stderr);}
      const captions=`1\n00:00:00,480 --> 00:00:0${options.badSubtitle?'3':'1'},000\nCalibration 字幕\n`;
      writeFileSync(join(folder,'captions.srt'),captions);writeFileSync(join(folder,'project.fcproj'),'no native project in this media-only fixture');
      const files=Object.fromEntries(['film.mp4','captions.srt','project.fcproj'].map(file=>{
        const data=readFileSync(join(folder,file));return [file,{sha256:sha256(data),bytes:data.length}];}));
      const request=createReviewRequest({taskId:name,attemptId:'calibration',epoch:1,bindingSha256:hash(),
        candidateSha256:sha256(stableJson(files)),projectSha256:files['project.fcproj'].sha256,inputHashes:{},executionSha256:hash('b'),files},criteria);
      writeFileSync(join(folder,'request.json'),stableJson(request)+'\n');writeFileSync(join(folder,'tools.json'),stableJson(options.noTools?{}:tools));
      const measured=spawnSync(command.executable,['-I','-B',command.script,'--request',join(folder,'request.json'),
        '--artifacts',folder,'--tools',join(folder,'tools.json')],{encoding:'utf8',timeout:60_000});
      assert.equal(measured.status,0,measured.stderr);const wire=JSON.parse(measured.stdout);
      assert.equal(wire.requestSha256,reviewRequestHash(request));
      const result=evaluateReview(request,wire.assessment);
      captureEvidence('quality-media-'+name,'actual generated calibration media, external Python and ffmpeg/ffprobe; not user footage',
        {inputRecipe:{video:'32x32/25fps/2s, white at 0.48 and 1.48s',audio:source,...options},files,
          reviewer:criteria.reviewer,assessment:wire.assessment,result,provenance:'repository-generated procedural calibration; no third-party media'});
      return result;
    }
    const aligned=measure('aligned');assert.equal(aligned.technicalAcceptance,'PASS');assert.equal(aligned.dimensions.avSync.status,'PASS');
    assert.equal(aligned.creativeAcceptance,'manual_review');assert.equal(aligned.userAcceptance,'NOT_RUN');
    const shifted=measure('shifted',{delay:.2});assert.equal(shifted.dimensions.avSync.status,'FAIL');assert.equal(shifted.decision,'blocked');
    const clipped=measure('stereo-clipped',{clipped:true});assert.equal(clipped.dimensions.audioClipping.status,'FAIL');assert.equal(clipped.decision,'blocked');
    const broken=measure('broken',{broken:true});assert.equal(broken.dimensions.decode.status,'FAIL');assert.equal(broken.decision,'blocked');
    const absent=measure('missing-audio',{noAudio:true});assert.equal(absent.dimensions.audioClipping.status,'FAIL');
    const subtitles=measure('bad-subtitle',{badSubtitle:true});assert.equal(subtitles.dimensions.subtitleTiming.status,'FAIL');
    const unavailable=measure('missing-tools',{noTools:true});assert.equal(unavailable.technicalAcceptance,'NOT_RUN');assert.equal(unavailable.decision,'manual_review');
  });
