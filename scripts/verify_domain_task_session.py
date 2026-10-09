#!/usr/bin/env python3
"""固定安装公开JSONL：查询、示波器交付、字幕音画交付、返工和拒绝共享同一实例。"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import queue
import shutil
import struct
import subprocess
import sys
import threading
import wave


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['installed-plugin','runtime-home','reference-plan','orange','ffmpeg','ffprobe','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();root=a.output.resolve();root.mkdir(mode=0o700);fixture=root/'fixture';fixture.mkdir();skill=a.installed_plugin.resolve()/'skills/filmcraft-use';runtime=a.runtime_home.resolve();tick=254016000000
    shutil.copyfile(a.orange,fixture/'orange.png')
    subprocess.run([str(a.ffmpeg),'-v','error','-f','lavfi','-i','color=c=red:s=320x180:r=12:d=2','-c:v','libx264','-pix_fmt','yuv420p',str(fixture/'shot.mp4')],check=True)
    with wave.open(str(fixture/'voice.wav'),'wb') as stream:
        stream.setnchannels(1);stream.setsampwidth(2);stream.setframerate(48000)
        stream.writeframes(b''.join(struct.pack('<h',0 if n<24000 else int(6000*math.sin(2*math.pi*440*n/48000))) for n in range(96000)))
    hashes={f.name:sha(f) for f in fixture.iterdir()};q=queue.Queue();responses=[]
    argv=[sys.executable,'-I','-B','-u',str(skill/'scripts/task_session.py'),'--output',str(root/'task'),'--runtime-home',str(runtime),
          '--read-root',str(fixture),'--write-root',str(root),'--write-root',str(runtime),'--protect-input',str(fixture),'--mode','headless']
    with (root/'stderr.private.log').open('w') as errors:
        child=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,text=True,bufsize=1)
        def reader():
            for line in child.stdout:q.put(line)
            q.put(None)
        thread=threading.Thread(target=reader,daemon=True);thread.start()
        def receive():
            line=q.get(timeout=240)
            if line is None:raise RuntimeError('public_task_session_exited')
            value=json.loads(line);responses.append(value);return value
        def send(value):
            child.stdin.write(json.dumps(value,ensure_ascii=False)+'\n');child.stdin.flush();return receive()
        def command(name,ops):return send({'name':name,'plan':{'schema':'craft-command-plan/v1','operations':ops}})
        def op(name,params=None):return {'command':name,'params':params or {}}
        try:
            assert receive()['result']=='READY'
            assert command('before',[op('state.inspect')])['result']=='PASS'
            scope=json.loads(a.reference_plan.read_text());scope['assets']={'still':{'path':str(fixture/'orange.png'),'sha256':hashes['orange.png']}}
            assert send({'action':'workflow','name':'scopes','plan':scope})['result']=='PASS';print('scope delivery PASS',flush=True)
            plan=json.loads((skill/'examples/short-film.json').read_text());plan['assets']={key:{'path':str(fixture/file),'sha256':hashes[file]} for key,file in [('shot','shot.mp4'),('voice','voice.wav')]}
            first=send({'action':'workflow','name':'av','plan':plan});assert first['result']=='PASS';print('caption/audio delivery PASS',flush=True)
            source=root/'task/av';before_source={str(f.relative_to(source)):sha(f) for f in source.rglob('*') if f.is_file()}
            revision={'expectedProjectSha256':first['manifest']['files']['project.fcproj'],'assets':{},
                'operations':[{'command':'timeline.setTrack','params':{'track':'V1','name':'Owned revised track'}}],
                'frames':plan['frames'],'export':{'audioRequired':True}}
            assert send({'action':'workflow','name':'revision','plan':revision,'source':str(source)})['result']=='PASS';print('source revision PASS',flush=True)
            assert command('after',[op('state.inspect')])['result']=='PASS'
            refused=command('expected_refusal',[op('file.closeAllProjects',{'force':True}),op('scopes.read',{'seconds':0})]);assert refused['result']=='FAIL' and 'precondition_failed' in refused.get('error','')
            child.stdin.close();assert child.wait(timeout=30)==1
        finally:
            if child.poll() is None:
                child.stdin.close()
                try:child.wait(timeout=30)
                except subprocess.TimeoutExpired:child.terminate();child.wait(timeout=30)
            child.stdout.close();thread.join(timeout=5)
    (root/'responses.private.json').write_text(json.dumps(responses,ensure_ascii=False,indent=2)+'\n')
    proof=json.loads((root/'task/task-session.json').read_text());assert proof['sessionsStarted']==1 and proof['singleProcessIdentity'] and proof['stopped'] and proof['closed'] and proof['ownedProcessesStopped']
    assert [x['result'] for x in proof['plans']]==['PASS']*5+['FAIL']
    processes=[];deliveries=[]
    for name in ['scopes','av','revision']:
        delivery=root/'task'/name;manifest=json.loads((delivery/'manifest.json').read_text());assert all(sha(delivery/file)==digest for file,digest in manifest['files'].items())
        process=json.loads((delivery/'native-processes.json').read_text());assert process['editorPid']==proof['pids'][0][0] and process['borrowedTaskSession'] and process['editorRestartsForDelivery']==0
        assert all(c['subcommand'] in ['probe','bench-decode'] and c['completed'] for c in process['mediaHelperCalls']);processes.append({'stage':name,**process})
        deliveries.append({'stage':name,'files':len(manifest['files']),'manifestSha256':sha(delivery/'manifest.json'),'projectSha256':sha(delivery/'project.fcproj')})
    assert {str(f.relative_to(source)):sha(f) for f in source.rglob('*') if f.is_file()}==before_source
    assert {f.name:sha(f) for f in fixture.iterdir()}==hashes
    before=json.loads((source/'native.json').read_text())['sequence'];after=json.loads((root/'task/revision/native.json').read_text())['sequence']
    expected=copy.deepcopy(before);expected['video'][0]['name']='Owned revised track'
    assert {k:v for k,v in expected.items() if k not in ['selection','playhead']}=={k:v for k,v in after.items() if k not in ['selection','playhead']}
    for name in ['frame-0000.png','frame-0001.png','captions.srt']:assert (source/name).read_bytes()==(root/'task/revision'/name).read_bytes()
    independent=[]
    for name,frames,rate in [('scopes',216,'24/1'),('av',24,'12/1'),('revision',24,'12/1')]:
        delivery=root/'task'/name
        probe=json.loads(subprocess.check_output([str(a.ffprobe),'-v','error','-count_frames','-show_streams','-of','json',str(delivery/'film.mp4')]))
        video=next(x for x in probe['streams'] if x['codec_type']=='video');assert video['nb_read_frames']==str(frames) and video['avg_frame_rate']==rate
        row={'stage':name,'videoFrames':frames,'rate':rate,'videoSha256':sha(delivery/'film.mp4')}
        if name=='scopes':
            for file,pixel in [('frame-0000.png',[230,85,39,255]),('frame-0001.png',[0,0,0,255])]:
                raw=subprocess.check_output([str(a.ffmpeg),'-v','error','-i',str(delivery/file),'-frames:v','1','-f','rawvideo','-pix_fmt','rgba','-']);assert raw==bytes(pixel)*1024
            row['exactScopeRgbaPixels']=2048
        else:
            audio=next(x for x in probe['streams'] if x['codec_type']=='audio');assert abs(float(audio['start_time'])-float(video['start_time']))<1/12
            pcm=subprocess.check_output([str(a.ffmpeg),'-v','error','-i',str(delivery/'film.mp4'),'-map','0:a:0','-f','s16le','-ac','1','-ar','48000','-'])
            samples=struct.unpack('<'+str(len(pcm)//2)+'h',pcm)
            def rms(start,end):return math.sqrt(sum(x*x for x in samples[start:end])/(end-start))
            assert rms(0,18000)<10 and rms(30000,90000)>1000
            onset=next(n for n in range(0,len(samples)-480,480) if rms(n,n+480)>100);assert abs(onset/48000-.5)<=1/12
            pictures=[]
            for file in ['frame-0000.png','frame-0001.png']:
                raw=subprocess.check_output([str(a.ffmpeg),'-v','error','-i',str(delivery/file),'-frames:v','1','-f','rawvideo','-pix_fmt','rgba','-']);assert len(raw)==320*180*4;pictures.append(raw)
            changed=[n//4 for n in range(0,len(pictures[0]),4) if pictures[0][n:n+4]!=pictures[1][n:n+4]]
            assert changed and min(index//320 for index in changed)>100
            assert '00:00:01,000' in (delivery/'captions.srt').read_text() and 'First scene' in (delivery/'captions.srt').read_text()
            row.update(audioOnsetSeconds=onset/48000,earlySilenceRms=rms(0,18000),toneRms=rms(30000,90000),pcmSha256=hashlib.sha256(pcm).hexdigest(),captionChangedPixels=len(changed))
        independent.append(row)
    report={'schema':'filmcraft-fixed-domain-task-session/v1','result':'PASS','pluginVersion':json.loads((a.installed_plugin/'plugin.json').read_text())['version'],
        'driverSha256':sha(__file__),'taskScriptSha256':sha(skill/'scripts/task_session.py'),'workflowScriptSha256':sha(skill/'scripts/workflow.py'),
        'session':proof,'processes':processes,'deliveries':deliveries,'independentOutputChecks':independent,'sourceAndFixturePreserved':True,'completeRevisedSequenceEquality':True,
        'scope':'Independent public JSONL source entry only; five healthy stages plus final native disabled refusal, one editor, source revision/caption/audio/export. Plugin Harness prepare/run/continuation ownership still requires integration; task9.39 OPEN. No GUI/full commands/V1 qualification.'}
    (root/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS one editor / three deliveries / stopped refusal / cleanup',flush=True)


if __name__=='__main__':main()
