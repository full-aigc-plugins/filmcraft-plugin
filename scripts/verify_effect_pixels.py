#!/usr/bin/env python3
"""独立FFmpeg解码真实PNG，逐像素验证位置与直通RGBA透明度，而非只检查文件存在。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compare_frame(actual, expected, tolerance=1):
    if len(actual)!=32*32*4 or len(expected)!=len(actual):raise ValueError('pixel_frame_shape_mismatch')
    if actual[3::4]!=expected[3::4]:raise ValueError('pixel_alpha_mismatch')
    error=max(abs(a-b) for a,b in zip(actual,expected))
    if error>tolerance:raise ValueError('pixel_frame_mismatch')
    return error


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit',type=Path,required=True);p.add_argument('--ffmpeg',type=Path,required=True);p.add_argument('--ffprobe',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();root=a.audit.resolve();producer=json.loads((root/'report.json').read_text());assert producer['result']=='PASS'
    results=[];all_frames={}
    for mode in ['headless','bridge']:
        work=root/mode;observed=json.loads((work/'observations.json').read_text());frames={};images=[]
        for label,row in observed['renderImages'].items():
            file=work/row['path'];assert sha(file)==row['sha256']
            metadata=json.loads(subprocess.check_output([str(a.ffprobe),'-v','error','-show_streams','-of','json',str(file)]))
            streams=metadata['streams'];assert len(streams)==1 and streams[0]['codec_name']=='png' and streams[0]['width']==streams[0]['height']==32
            raw=subprocess.check_output([str(a.ffmpeg),'-v','error','-i',str(file),'-frames:v','1','-f','rawvideo','-pix_fmt','rgba','-'])
            assert len(raw)==32*32*4;frames[label]=raw;images.append({'label':label,'fileSha256':sha(file),'rgbaSha256':hashlib.sha256(raw).hexdigest(),'pixels':1024})
        # 夹具ColorMatte为sRGB (230,85,39)，不能以错误的基准输出自证正确。
        pixel=bytes([230,85,39,255]);base=pixel*(32*32)
        compare_frame(frames['baseline'],base)
        half=(pixel[:3]+bytes([128]))*(32*32)
        shifted=b''.join(base[(y*32+x+8)*4:(y*32+x+8)*4+4] if x<24 else bytes(4) for y in range(32) for x in range(32))
        expected={'baseline':base,'shifted':shifted,'linear_start':base,'linear_half':half,'linear_end':bytes(len(base)),
            'hold_half':base,'reopened_half':half,'revised_half':base,'restored':base}
        assert set(frames)==set(expected)
        errors={label:compare_frame(frames[label],value) for label,value in expected.items()}
        queries=[]
        for phase in ['create','revision']:
            receipt=json.loads((work/(phase+'-receipt.private.json')).read_text())
            rows=next(s['result'] for s in receipt['steps'] if s.get('command')=='effects.list')
            assert isinstance(rows,list) and rows and all(r['kind']=='Video' for r in rows)
            assert len({r['id'] for r in rows})==len(rows)
            gaussian=next(r for r in rows if r['id']=='gaussian_blur');info={r['id']:r for r in gaussian['paramInfo']}
            assert info['blurriness']['default']=={'Float':0.0} and info['dimensions']['default']=={'Choice':0} and info['repeat_edge']['default']=={'Bool':False}
            assert set(gaussian['params'])==set(info)
            queries.append({'phase':phase,'effects':len(rows),'gaussianDefaults':'PASS','receiptSha256':sha(work/(phase+'-receipt.private.json'))})
        results.append({'mode':mode,'result':'PASS','images':images,'queries':queries,'maxChannelError':max(errors.values()),'baselineRgba':list(pixel),
            'expectedHalfRgba':list(half[:4]),'actualHalfRgba':list(frames['linear_half'][:4]),'comparisons':errors,'rgbaSamplesCompared':len(base)*len(expected)})
        all_frames[mode]=frames
    assert all(all_frames['headless'][label]==all_frames['bridge'][label] for label in all_frames['headless'])
    report={'schema':'filmcraft-effect-pixels/v1','result':'PASS','sourceAuditSha256':sha(root/'report.json'),'driverSha256':sha(__file__),'results':results,
        'tools':{name:{'binarySha256':sha(binary),'version':subprocess.check_output([str(binary),'-version'],text=True).splitlines()[0]} for name,binary in [('ffmpeg',a.ffmpeg),('ffprobe',a.ffprobe)]},
        'scope':'18 actual native PNGs/18432 pixels decoded. All RGBA channels compared: integer8px motion and transparent exposed region, straight-alpha PNG opacity100/50/0 (alpha255/128/0), hold, saved/reopened keyframes, revised endpoint and baseline restore. RGB tolerance1 code unit; alpha exact. Headless/bridge decoded bytes equal. No Bezier/easing visual algorithm or all-effects/GUI/full V1 qualification.'}
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS18 native PNGs / full pixels / saved-reopened revision')


if __name__=='__main__':main()
