"""通过FilmCraft原生命令校正SRT恒定偏移；保留输入及非目标轨道。"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

TICKS_PER_MS = 254016000
STAMP = r'(\d{2,}):([0-5]\d):([0-5]\d)[,.](\d{3})'


def parse_cues(text, vtt=False):
    text = text.lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')
    if vtt:
        if not text.startswith('WEBVTT\n'):raise ValueError('Missing WEBVTT header')
        text = text.split('\n',1)[1]
    result=[]
    for block in re.split(r'\n[ \t]*\n',text.strip('\n')):
        lines=block.split('\n')
        if lines and lines[0].isdigit():lines=lines[1:]
        match=re.fullmatch(STAMP+r'\s+-->\s+'+STAMP,lines[0]) if lines else None
        if not match or len(lines)<2 or not '\n'.join(lines[1:]).strip():raise ValueError('Invalid subtitle cue')
        def ms(fields):
            h,m,s,sub=map(int,fields);return ((h*60+m)*60+s)*1000+sub
        start,end=ms(match.groups()[:4]),ms(match.groups()[4:])
        if start>=end:raise ValueError('Subtitle start must precede end')
        result.append({'startMs':start,'endMs':end,'text':'\n'.join(lines[1:])})
    if not result or len(result)>5000:raise ValueError('Expected1..5000 cues')
    return result


def validate_offset(cues, offset):
    if isinstance(offset,bool) or not isinstance(offset,int):raise ValueError('Offset must be integer milliseconds')
    for cue in cues:
        if cue['startMs']+offset<0:raise ValueError('Offset would cross timeline zero')
        if max(cue['endMs'],cue['endMs']+offset)*TICKS_PER_MS>2**63-1:raise ValueError('Tick range overflow')


def repair_steps(cues, imported):
    if len(cues)!=len(imported):raise ValueError('Import changed cue count')
    steps=[]
    for original, actual in zip(cues,imported):
        if original['text']!=actual['text']:raise ValueError('Import changed caption text')
        # 先恢复结束，再恢复开始，避免极短字幕的临时负时长。
        for edge, source, field in [('out','endMs','end'),('in','startMs','start')]:
            delta=original[source]*TICKS_PER_MS-actual[field]
            if delta:steps.append({'id':'captions.trim','params':{'caption':actual['id'],'edge':edge,'delta':delta}})
    return steps


def verify_track(cues, captions, offset):
    if len(cues)!=len(captions):raise ValueError('Reopened cue count differs')
    for original, actual in zip(cues,captions):
        if actual['text']!=original['text'] or any(actual[field]!=(original[key]+offset)*TICKS_PER_MS for field,key in [('start','startMs'),('end','endMs')]):
            raise ValueError('Caption text, precision or duration changed')


def verify_protected_tracks(before, after, target):
    # C1/C2是随插入位置变化的显示序号，不是轨道内容或稳定身份。
    def content(track):return {k:v for k,v in track.items() if k!='label'}
    if [content(t) for t in after if t['id']!=target]!=[content(t) for t in before]:
        raise ValueError('Non-target caption tracks changed')


def execute(cli, *args):
    process=subprocess.run([str(cli),*map(str,args)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if process.returncode:raise RuntimeError(process.stderr or process.stdout)
    return process.stdout


def media_relinks(cli, project):
    """用原生命令读取媒体路径，仅在工程副本中重链接到同一个文件。"""
    listing=json.loads(execute(cli,'--project',str(project),'exec','project.items',json.dumps({'recursive':True})))
    rows=listing if isinstance(listing,list) else listing.get('rows',[])
    steps=[]
    for row in rows:
        item=row.get('item',row.get('id'))
        if item is None:continue
        metadata=json.loads(execute(cli,'--project',str(project),'exec','metadata.get',json.dumps({'item':item})))
        paths=[field['value'] for field in metadata.get('fields',[]) if field['name']=='File Path' and field.get('value')]
        if not paths:continue
        path=Path(paths[0])
        resolved=(path if path.is_absolute() else project.parent/path).resolve(strict=True)
        steps.append({'id':'media.relink','params':{'item':item,'path':str(resolved),'relinkOthers':False,'alignTimecode':False}})
    return steps


def sync(cli, source, output, offset, project=None, fps=25, language="zh"):
    source=Path(source).resolve(strict=True);output=Path(output).resolve()
    cues=parse_cues(source.read_text(encoding='utf-8-sig'));validate_offset(cues,offset)
    if not math.isfinite(fps) or not 1<=fps<=240:raise ValueError('Invalid frame rate')
    if output.exists():raise ValueError('Output directory must not exist')
    inputs=[source]+([Path(project).resolve(strict=True)] if project else [])
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    baseline=json.loads(execute(cli,'--project',str(inputs[1]),'exec','captions.list'))['tracks'] if project else []
    timeline=json.loads(execute(cli,'--project',str(inputs[1]),'inspect','sequence')) if project else None
    if timeline and timeline['duration']>0 and max(c['endMs']+offset for c in cues)*TICKS_PER_MS>timeline['duration']:
        raise ValueError('Shifted captions exceed existing sequence duration')
    output.mkdir(parents=True)
    def batch(name, steps, before, after):
        script=output/(name+'.jsonl');script.write_text(''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in steps),encoding='utf-8')
        args=(['--project',str(before)] if before else [])+['--save-as',str(after),'run',str(script)]
        text=execute(cli,*args);(output/(name+'-result.jsonl')).write_text(text,encoding='utf-8')
        rows=[json.loads(line) for line in text.splitlines() if line.strip()]
        if len(rows)!=len(steps) or not all(v.get('ok') for v in rows):raise ValueError('Incomplete native command results')
        return rows
    initial=output/'imported.fcproj';steps=media_relinks(cli,inputs[1]) if project else [{'id':'file.newSequence','params':{'name':'Subtitle sync','width':320,'height':180,'fps':fps}}]
    steps += [{'id':'captions.import','params':{'path':str(source),'name':'Synced subtitles'}},{'id':'captions.list','params':{}}]
    rows=batch('import',steps,inputs[1] if project else None,initial)
    track_id=next(row['result']['track'] for row in rows if row['id']=='captions.import')
    tracks=rows[-1]['result']['tracks'];target=next(row for row in tracks if row['id']==track_id)
    repair=repair_steps(cues,target['captions']);repaired=output/'precise.fcproj'
    correction=repair+[{'id':'captions.setTrack','params':{'track':track_id,'language':language}},{'id':'captions.list','params':{'track':track_id}}]
    result=batch('restore-precision',correction,initial,repaired)
    current=result[-1]['result']['tracks'][0]['captions'];verify_track(cues,current,0)
    final=output/'synced.fcproj'
    batch('shift',[{'id':'captions.move','params':{'captions':[v['id'] for v in current],'delta':offset*TICKS_PER_MS}}],repaired,final)
    # 新进程读取已保存工程，再导出；不能用旧的内存状态冒充重开。
    reopened=json.loads(execute(cli,'--project',str(final),'exec','captions.list'))['tracks']
    target=next(row for row in reopened if row['id']==track_id);verify_track(cues,target['captions'],offset)
    verify_protected_tracks(baseline,reopened,track_id)
    if timeline:
        after=json.loads(execute(cli,'--project',str(final),'inspect','sequence'))
        if any(after[k]!=timeline[k] for k in ['video','audio','markers','settings','in','out','split','duration']):
            raise ValueError('Non-caption timeline content changed')
    for extension in ['srt','vtt']:
        path=output/('synced.'+extension)
        execute(cli,'--project',str(final),'exec','captions.export',json.dumps({'track':track_id,'path':str(path),'format':extension}))
        exported=parse_cues(path.read_text(encoding='utf-8-sig'),vtt=extension=='vtt')
        expected=[dict(cue,startMs=cue['startMs']+offset,endMs=cue['endMs']+offset) for cue in cues]
        if exported!=expected:raise ValueError('Export lost text or timing precision')
    for path,digest in hashes.items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise ValueError('Input changed during execution')
    result={'sourceSha256':hashes[str(source)],'offsetMs':offset,'cueCount':len(cues),'targetTrack':track_id,
            'precisionRepairOperations':len(repair),'nonTargetTracksUnchanged':True,'inputHashesUnchanged':True,'mediaTimelineUnchanged':bool(project),
            'sourceProjectSha256':hashes[str(inputs[1])] if project else None,
            'project':'synced.fcproj','exports':['synced.srt','synced.vtt'],'asrPerformed':False}
    (output/'manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli',required=True);parser.add_argument('--input',required=True)
    parser.add_argument('--output',required=True);parser.add_argument('--offset-ms',required=True,type=int)
    parser.add_argument('--project');parser.add_argument('--fps',type=float,default=25);parser.add_argument('--language',default='zh')
    args=parser.parse_args();print(json.dumps(sync(args.cli,args.input,args.output,args.offset_ms,args.project,args.fps,args.language)))
