#!/usr/bin/env python3
"""执行来源绑定的真实媒体矩阵；候选、原生与宿主资格保持分层。"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from media_matrix import CASES, digest, validate

TICKS = 254016000000


def composite_channel(value, alpha):
    """独立 sRGB 解码、线性 over-black 合成再编码；不复用被测原生实现。"""
    normalized = value / 255
    linear = normalized / 12.92 if normalized <= .04045 else ((normalized + .055) / 1.055) ** 2.4
    mixed = linear * alpha / 255
    encoded = 12.92 * mixed if mixed <= .0031308 else 1.055 * mixed ** (1/2.4) - .055
    return round(encoded * 255)


def rejection_gate(home):
    """保留有明确失败身份的诊断目录，拒绝任何成功交付清单。"""
    home = Path(home)
    if not home.exists(): return None
    if (home/'manifest.json').exists(): raise ValueError('failed_delivery_published')
    failure = home/'failure.json'
    if not failure.is_file(): raise ValueError('unclassified_failure_output')
    row = json.loads(failure.read_text())
    if (row.get('schema'), row.get('status'), row.get('replayAllowed'), row.get('acceptance')) != (
            'craft-failed-stage/v1', 'failed', False, 'not-a-successful-delivery'):
        raise ValueError('unclassified_failure_output')
    return row


def audio_gate(row, required_samples, frame_seconds):
    """拒绝低保真、越界偏移、缺尾部采样及非有限的测量。"""
    if (any(type(row.get(k)) not in (int, float) or not math.isfinite(row[k]) for k in ('correlation', 'lagSeconds', 'rms'))
            or row['correlation'] < .98 or abs(row['lagSeconds']) > frame_seconds
            or type(row.get('sampleCount')) is not int or row['sampleCount'] < required_samples or row['rms'] <= .0001):
        raise ValueError('audio_fidelity_failed')


def pixel_gate(rows, frame_count):
    """全帧检查透明合成，不能用一个像素或一个截图代替完整校准帧。"""
    if (len(rows) != frame_count or {x.get('frame') for x in rows} != set(range(frame_count))
            or any(type(x.get('maximumChannelError')) is not int or not 0 <= x['maximumChannelError'] <= 3 for x in rows)):
        raise ValueError('alpha_pixel_fidelity_failed')


def summarize(cases, candidate, installation_preserved):
    passed = (set(cases) == set(CASES) and installation_preserved
              and all(row.get('status') == 'PASS' and row.get('measurements') for row in cases.values()))
    return {'result': 'PASS' if passed else 'FAIL', 'cases': cases,
            'layer': 'private-native-candidate' if candidate else 'native-matrix',
            'installationPreserved': installation_preserved,
            'fixedInstallation': 'NOT_RUN' if candidate else 'HOST_BINDING_REQUIRED',
            'otherPlatforms': 'NOT_RUN', 'creativeAcceptance': 'manual_review',
            'userAcceptance': 'NOT_RUN', 'fullV1': 'NOT_PROVEN'}


def load(skill, name):
    spec = importlib.util.spec_from_file_location('matrix_' + name, Path(skill)/'scripts'/(name+'.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def tree_hashes(root):
    return {p.relative_to(root).as_posix(): digest(p) for p in sorted(Path(root).rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def verify(skill, fixtures, output, runtime_home, ffmpeg, ffprobe, candidate_archive=None, candidate_receipt=None, upstream=None):
    """核对输入后执行实际公开工作流；本地候选仅修改私有副本的运行时锁。"""
    output = Path(output).absolute()
    if output.exists() or output.is_symlink(): raise ValueError('output_exists')
    skill, fixtures = Path(skill).resolve(), Path(fixtures).resolve()
    manifest_path = fixtures/'manifest.json'; manifest = json.loads(manifest_path.read_text())
    validate(manifest, fixtures)
    if bool(candidate_archive) != bool(candidate_receipt): raise ValueError('candidate_pair_required')
    original_hashes = tree_hashes(skill)
    output.mkdir(parents=True, mode=0o700)
    copied = output/'skill'; shutil.copytree(skill, copied, ignore=shutil.ignore_patterns('__pycache__'))
    lock_path = copied/'scripts/runtime.lock.json'; lock = json.loads(lock_path.read_text())
    candidate = candidate_archive is not None
    if candidate:
        receipt = json.loads(Path(candidate_receipt).read_text())
        if digest(candidate_archive) != receipt['archiveSha256']: raise ValueError('candidate_archive_digest_mismatch')
        lock.update(resolvedVersion=receipt['runtimeVersion'], releaseRef='runtime-v'+receipt['runtimeVersion'])
        artifact = lock['artifacts']['darwin-arm64']
        artifact.update({key:receipt[key] for key in ('archiveSha256','binarySha256','provenanceSha256','versionOutput')})
        artifact['url'] = lock['repository']+'/releases/download/'+lock['releaseRef']+'/'+receipt['archive']
        lock_path.write_text(json.dumps(lock, indent=2)+'\n')
    copied_hashes = tree_hashes(copied)
    bootstrap = load(copied, 'bootstrap'); workflow = load(copied, 'workflow')
    installed = bootstrap.install(lock, runtime_home, archive=candidate_archive)
    cli = installed['executable']; calls = []; cases = {}
    # 测量依赖仅用于原生矩阵，不是普通单元门禁的依赖。
    import numpy as np
    from PIL import Image

    def external(args, timeout=300):
        result = subprocess.run([str(x) for x in args], capture_output=True, timeout=timeout)
        calls.append({'argv':[str(x).replace(str(output),'[OUTPUT]').replace(str(fixtures),'[FIXTURES]').replace(str(Path.home()),'[USER_HOME]') for x in args],
                      'exitCode':result.returncode,'stdoutSha256':hashlib.sha256(result.stdout).hexdigest(),
                      'stderr':result.stderr.decode(errors='replace').replace(str(output),'[OUTPUT]').replace(str(Path.home()),'[USER_HOME]')})
        if result.returncode: raise ValueError('external_failed: '+str(args[0])+': '+calls[-1]['stderr'])
        return result.stdout

    def native(project, *args):
        return external([cli, '--data-dir', output/'data', '--project', project, *args])

    def execute(plan, name, source=None):
        return workflow.execute(plan, output/name, runtime_home=runtime_home, source=source, data_dir=output/'data')

    def plan_for(assets, durations, width=320, height=180):
        plan = {'document':{'name':'Media matrix','width':width,'height':height,'frameRate':{'num':12,'den':1}},
                'assets':{},'operations':[],'frames':['0'], 'export':{'audioRequired':False}}
        for alias, path, track in assets:
            plan['assets'][alias]={'path':str(path),'sha256':digest(path)}
            plan['operations'] += [{'command':'asset.import','params':{'asset':alias},'as':alias},
                {'command':'timeline.place','params':{'item':{'$ref':alias+'.item'},'track':track,'audioTrack':'A1','time':'0','sourceIn':'0','duration':str(durations[alias]),'insert':False}}]
        return plan

    def probe(path):
        return json.loads(external([ffprobe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',path]))

    def decode_audio(path, rate, channels):
        data = external([ffmpeg,'-v','error','-i',path,'-vn','-ar',str(rate),'-ac',str(channels),'-f','f32le','-'])
        return np.frombuffer(data,dtype='<f4').reshape((-1,channels)).astype(np.float64)

    def audio_measure(reference, actual, rate, start, end, tail=None):
        rows=[];search=math.ceil(rate/12)
        for channel in range(reference.shape[1]):
            x=reference[start:end,channel];x=x-x.mean();xx=float(np.dot(x,x));best=(-2.0,None)
            for lag in range(-search,search+1):
                if start+lag<0 or end+lag>len(actual):continue
                y=actual[start+lag:end+lag,channel]; y=y-y.mean()
                denominator=math.sqrt(xx*float(np.dot(y,y)))
                score=float(np.dot(x,y)/denominator) if denominator else 0.0
                if score>best[0]:best=(score,lag)
            if best[1] is None:raise ValueError('audio_alignment_missing')
            lag=best[1]; n=tail or end-start; x=reference[end-n:end,channel];y=actual[end-n+lag:end+lag,channel]
            centered_x=x-x.mean();centered_y=y-y.mean();den=float(np.linalg.norm(centered_x)*np.linalg.norm(centered_y))
            row={'channel':channel,'correlation':float(np.dot(centered_x,centered_y)/den) if den else 0.0,
                 'alignmentCorrelation':best[0],'lagSeconds':lag/rate,'sampleCount':len(y),'rms':float(np.sqrt(np.mean(y*y)))}
            audio_gate(row,n,1/12);rows.append(row)
        return rows

    def delivery_facts(name, duration, width, height):
        home=output/name; saved=digest(home/'project.fcproj')
        json.loads(native(home/'project.fcproj','inspect'))
        if digest(home/'project.fcproj')!=saved:raise ValueError('reopen_mutated_project')
        movie=home/'film.mp4'; p=probe(movie)
        video=next(row for row in p['streams'] if row['codec_type']=='video')
        if (video['width'],video['height'],video['avg_frame_rate'])!=(width,height,'12/1'):raise ValueError('video_shape_mismatch')
        if int(video['nb_read_frames']) != math.ceil(duration*12):raise ValueError('video_frame_count_mismatch')
        observed=float(p['format']['duration'])
        if abs(observed-duration)>1/12:raise ValueError('duration_mismatch')
        external([ffmpeg,'-v','error','-i',movie,'-f','null','-'])
        return {'projectSha256':saved,'movieSha256':digest(movie),'durationSeconds':observed,
                'requestedSeconds':duration,'videoFrames':int(video['nb_read_frames']),'fullDecode':True}

    def vfr():
        path=fixtures/'vfr.mkv'; p=plan_for([('video',path,'V1')],{'video':3*TICKS});p['export']['audioRequired']=True
        p['frames']=['0',str(TICKS*3//2),str(TICKS*35//12)]
        execute(p,'vfr');facts=delivery_facts('vfr',3,320,180)
        reference=decode_audio(path,8000,1);actual=decode_audio(output/'vfr/film.mp4',8000,1)
        facts['audio']=audio_measure(reference,actual,8000,800, min(len(reference),len(actual))-800)
        source_probe=json.loads(external([ffprobe,'-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',path]))
        pts=[float(row['best_effort_timestamp_time']) for row in source_probe['frames']]
        if any(b<=a for a,b in zip(pts,pts[1:])) or len({round(b-a,3) for a,b in zip(pts,pts[1:])})<2:raise ValueError('not_vfr')
        stream_probe=probe(output/'vfr/film.mp4');starts={r['codec_type']:float(r.get('start_time',0)) for r in stream_probe['streams']}
        if abs(starts['video']-starts['audio'])>1/12:raise ValueError('av_stream_start_mismatch')
        decoded=external([ffmpeg,'-v','error','-i',path,'-an','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
        frames=np.frombuffer(decoded,dtype=np.uint8).reshape((-1,180,320,3));observations=[]
        for n,t in enumerate([0,1.5,35/12]):
            with Image.open(output/'vfr'/f'frame-{n:04}.png') as image:preview=np.asarray(image.convert('RGB')).astype(np.int16)
            possible=[i for i,v in enumerate(pts) if abs(v-t)<=1/12+.001]
            comparisons=[(float(np.mean(np.abs(frames[i].astype(np.int16)-preview))),i) for i in possible]
            error,index=min(comparisons)
            if error>5:raise ValueError('vfr_frame_alignment_failed: '+str(error))
            observations.append({'requestedSeconds':t,'sourcePts':pts[index],'meanChannelError':error})
        facts.update(sourceFrames=len(pts),sourceFrameIntervals=sorted({round(b-a,3) for a,b in zip(pts,pts[1:])}),streamStarts=starts,frameAlignment=observations)
        return facts

    def long_tail():
        path=fixtures/'long-tail.wav';count=manifest['measurements']['audioSamplesPerChannel'];duration=count/48000
        p=plan_for([('audio',path,'A1')],{'audio':count*TICKS//48000},32,18);p['export']['audioRequired']=True
        execute(p,'long-audio-tail');facts=delivery_facts('long-audio-tail',duration,32,18)
        wave=output/'long-audio-tail/native.wav'
        native(output/'long-audio-tail/project.fcproj','export',wave,'--preset','Waveform Audio 48 kHz 24-bit')
        reference=decode_audio(path,48000,2);facts['sourceSamplesPerChannel']=len(reference)
        if len(reference)!=count:raise ValueError('source_sample_count_mismatch')
        for name,target in [('pcm',wave),('aac',output/'long-audio-tail/film.mp4')]:
            actual=decode_audio(target,48000,2)
            facts[name]={'decodedSamplesPerChannel':len(actual),'tail':audio_measure(reference,actual,48000,count-12000,count,tail=544),'sha256':digest(target)}
        return facts

    def font_change():
        if upstream is None:raise ValueError('font_source_repository_required')
        fonts=json.loads(external([cli,'exec','fonts.list','{"system":true}']));families={r['family'] for r in fonts}
        wanted=['Inter','Noto Serif'];identity=[]
        for family,filename in zip(wanted,['Inter-Regular.ttf','NotoSerif-Regular.ttf']):
            if family not in families:raise ValueError('required_native_font_missing: '+family)
            data=external(['git','-C',upstream,'show',lock['upstreamCommit']+':assets/fonts/'+filename])
            license_file='OFL-'+('Inter' if family=='Inter' else 'NotoSerif')+'.txt'
            license_data=external(['git','-C',upstream,'show',lock['upstreamCommit']+':assets/fonts/'+license_file])
            installed_license=Path(cli).parent/('LICENSE-'+license_file)
            if not installed_license.is_file() or installed_license.read_bytes()!=license_data:raise ValueError('font_license_mismatch')
            identity.append({'licenseSha256':hashlib.sha256(license_data).hexdigest(),'licenseSource':lock['upstreamRepository']+'/blob/'+lock['upstreamCommit']+'/assets/fonts/'+license_file,'family':family,'origin':'runtime-bundled','fontSha256':hashlib.sha256(data).hexdigest(),
                             'license':'OFL-1.1','upstreamCommit':lock['upstreamCommit'],'binarySha256':installed['binarySha256']})
        p=plan_for([('video',fixtures/'vfr.mkv','V1')],{'video':3*TICKS})
        p['operations'] += [{'command':'captions.newTrack','params':{'format':'Subtitle'}},
            {'command':'captions.setStyle','params':{'track':'C1','font':wanted[0],'size':84,'margin':.02}},
            {'command':'caption.add','params':{'track':'C1','text':'FilmCraft exact font WWW iii','startTicks':'0','durationTicks':str(TICKS)}}]
        first=execute(p,'font-first');change={'expectedProjectSha256':first['files']['project.fcproj'],'operations':[
            {'command':'captions.setStyle','params':{'track':'C1','font':wanted[1]}}],'frames':['0'],'export':{'audioRequired':False}}
        execute(change,'font-second',source=output/'font-first')
        before=np.asarray(Image.open(output/'font-first/frame-0000.png').convert('RGB'));after=np.asarray(Image.open(output/'font-second/frame-0000.png').convert('RGB'))
        changed=int(np.count_nonzero(np.any(before!=after,axis=2)))
        if not changed:raise ValueError('font_pixels_unchanged')
        styles=[]
        for name,family in [('font-first',wanted[0]),('font-second',wanted[1])]:
            facts=delivery_facts(name,3,320,180);cap=json.loads((output/name/'captions.json').read_text())['tracks'][0]
            if cap['style']['font']!=family:raise ValueError('persisted_font_mismatch')
            styles.append({'font':family,**facts})
        return {'fonts':identity,'discovered':wanted,'changedPixels':changed,'deliveries':styles,
                'downloadedNotoSans':'not installed or claimed as rendered; bundled fonts used without global installation'}

    def transparent_sequence():
        home=output/'alpha-input';home.mkdir();seq=load(copied,'sequence_assets');records=[]
        for i in range(12):
            target=home/f'frame_{i:05}.png';shutil.copyfile(fixtures/f'alpha-{i:03}.png',target);facts=seq.rgba_facts(target)
            records.append({'index':i,'location':target.name,'bytes':target.stat().st_size,'sha256':digest(target),
                            'alphaExtrema':facts['alphaExtrema'],'rgbaSha256':facts['rgbaSha256']})
        descriptor={'schema':'craft-image-sequence/v1','encoding':'png','width':32,'height':18,'bitDepth':8,'channels':'rgba',
                    'alphaRepresentation':'straight-png','colorSpace':'unknown','frameRate':{'num':12,'den':1},'frameCount':12,
                    'durationTicks':'12','timeBase':{'num':1,'den':12},'frames':records}
        path=home/'sequence.json';path.write_text(json.dumps(descriptor,indent=2)+'\n')
        p=plan_for([],{},32,18);p['assets']={'alpha':{'kind':'image-sequence','path':str(path),'sha256':digest(path)}}
        p['operations']=[{'command':'asset.import','params':{'asset':'alpha'},'as':'alpha'},
            {'command':'timeline.place','params':{'item':{'$ref':'alpha.item'},'track':'V1','time':'0','sourceIn':'0','duration':str(TICKS),'insert':False}}]
        p['frames']=[str(i*TICKS//12) for i in range(12)];execute(p,'transparent-sequence')
        rows=[]
        for i in range(12):
            src=np.asarray(Image.open(home/f'frame_{i:05}.png')).astype(np.int32)
            # 原生 Program 在场景线性光中合成，再输出 sRGB；阈值仍为 3/255。
            expected=np.empty((18,32,3),dtype=np.int16)
            for y in range(18):
                for x in range(32):
                    for channel in range(3):expected[y,x,channel]=composite_channel(int(src[y,x,channel]),int(src[y,x,3]))
            actual=np.asarray(Image.open(output/'transparent-sequence'/f'frame-{i:04}.png').convert('RGBA')).astype(np.int16)
            maximum=max(int(np.max(np.abs(actual[:,:,:3]-expected))),int(np.max(np.abs(actual[:,:,3]-255))))
            rows.append({'frame':i,'maximumChannelError':maximum})
        pixel_gate(rows,12)
        return {'provenance':'synthetic','compositeModel':'straight sRGB decoded to linear light; over black; sRGB RGBA8 output',
                'halfAlphaRedExpected':188,'pixels':rows,**delivery_facts('transparent-sequence',1,32,18)}

    def refused(plan, name, expected, source=None):
        before=tree_hashes(source) if source else None
        try:execute(plan,name,source=source)
        except (ValueError, RuntimeError) as error:
            if expected not in str(error):raise
            failure=rejection_gate(output/name)
            if source and tree_hashes(source)!=before:raise ValueError('rejection_mutated_source')
            return {'refused':True,'error':str(error).replace(str(output),'[OUTPUT]'),
                    'failureReceiptSha256':digest(output/name/'failure.json') if failure else None,
                    'successfulDeliveryExists':False,'sourcePreserved':True}
        raise ValueError('invalid_input_accepted')

    def bad_file():
        p=plan_for([('bad',fixtures/'corrupt.mov','V1')],{'bad':TICKS})
        return refused(p,'bad-file','unsupported media')

    def missing_font():
        p=plan_for([('video',fixtures/'vfr.mkv','V1')],{'video':3*TICKS})
        p['operations'] += [{'command':'captions.newTrack','params':{'format':'Subtitle'}},
            {'command':'captions.setStyle','params':{'track':'C1','font':'FilmCraft-Deliberately-Missing-Font-53'}}]
        return refused(p,'missing-font','missing_font')

    def dependency_move():
        inputs=output/'move-inputs';inputs.mkdir()
        for name in ['vfr.mkv','long-tail.wav']:shutil.copyfile(fixtures/name,inputs/name)
        p=plan_for([('video',inputs/'vfr.mkv','V1'),('audio',inputs/'long-tail.wav','A1')],{'video':3*TICKS,'audio':3*TICKS});p['export']['audioRequired']=True
        first=execute(p,'move-original');moved=output/'moved';(output/'move-original').rename(moved);inputs.rename(output/'unavailable-original-inputs')
        revision={'expectedProjectSha256':first['files']['project.fcproj'],'operations':[],'frames':['0'],'export':{'audioRequired':True}}
        second=execute(revision,'dependency-move',source=moved)
        for alias in first['assets']:
            if first['assets'][alias]['sha256']!=second['assets'][alias]['sha256']:raise ValueError('collected_dependency_changed')
        if (moved/'frame-0000.png').read_bytes()!=(output/'dependency-move/frame-0000.png').read_bytes():raise ValueError('moved_frame_changed')
        # 只删除本矩阵新建交付的副本；不操作登记输入或原始交付。
        broken=output/'missing-dependency';shutil.copytree(output/'dependency-move',broken)
        missing=broken/second['assets']['audio']['path'];missing.unlink()
        failed=refused({'expectedProjectSha256':second['files']['project.fcproj'],'operations':[]},'missing-dependency-output','asset_digest_mismatch',source=broken)
        return {'sourceDirectoryUnavailable':not inputs.exists(),'collectedAssetSha256':{k:v['sha256'] for k,v in second['assets'].items()},
                'relinkedPixelsUnchanged':True,'missingDependency':failed,**delivery_facts('dependency-move',3,320,180)}

    functions={'vfr':vfr,'long-audio-tail':long_tail,'font-change':font_change,'transparent-sequence':transparent_sequence,
               'bad-file':bad_file,'missing-font':missing_font,'dependency-move':dependency_move}
    for name, action in functions.items():
        try:cases[name]={'status':'PASS','measurements':action()}
        except Exception as error:cases[name]={'status':'FAIL','error':str(error).replace(str(output),'[OUTPUT]').replace(str(fixtures),'[FIXTURES]').replace(str(Path.home()),'[USER_HOME]')}
        (output/'progress.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    preserved=tree_hashes(skill)==original_hashes and tree_hashes(copied)==copied_hashes
    validate(manifest,fixtures)
    report=summarize(cases,candidate,preserved)
    report.update(schema='filmcraft-native-media-matrix/v1',fixtureManifestSha256=digest(manifest_path),
                  runtime={k:installed[k] for k in ['version','versionOutput','platform','binarySha256']},
                  skillFilesSha256=original_hashes,executedSkillFilesSha256=copied_hashes,
                  verifierFilesSha256={p.name:digest(p) for p in [Path(__file__),Path(__file__).with_name('media_matrix.py')]},
                  inputSha256={k:v['sha256'] for k,v in manifest['inputs'].items()},calls=calls)
    (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('skill','fixtures','output','runtime-home'):parser.add_argument('--'+name,type=Path,required=True)
    for name in ('candidate-archive','candidate-receipt','upstream'):parser.add_argument('--'+name,type=Path)
    for name in ('ffmpeg','ffprobe'):parser.add_argument('--'+name,required=True)
    result=verify(**vars(parser.parse_args()));print(json.dumps({'result':result['result'],'cases':{k:v['status'] for k,v in result['cases'].items()},'fixedInstallation':result['fixedInstallation']}))
    raise SystemExit(result['result']!='PASS')
