#!/usr/bin/env python3
"""以独立FFmpeg／ffprobe逐样本验证原生clip.audioGain导出；不启动FilmCraft。"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('audit','ffmpeg','ffprobe','output'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();audit=args.audit.resolve(strict=True);output=args.output.resolve()
    if output.exists():raise ValueError('output_exists')
    report=json.loads((audit/'report.json').read_text());assert report['result']=='PASS'
    results=[]
    def samples(path):
        probe=json.loads(subprocess.check_output([str(args.ffprobe),'-v','error','-show_streams','-show_format','-of','json',str(path)]))
        streams=probe['streams'];assert len(streams)==1
        stream=streams[0];assert stream['codec_type']=='audio' and stream['channels']==2 and int(stream['sample_rate'])==48000
        assert abs(float(probe['format']['duration'])-.25)<=1/48000
        data=subprocess.check_output([str(args.ffmpeg),'-v','error','-nostdin','-i',str(path),'-map','0:a:0','-f','f32le','-acodec','pcm_f32le','-'])
        values=struct.unpack('<'+str(len(data)//4)+'f',data)
        assert len(values)==24000 and all(math.isfinite(v) for v in values)
        return values,{'fileSha256':sha(path),'pcmSha256':hashlib.sha256(data).hexdigest(),'frames':12000,'channels':2,'sampleRate':48000}
    for mode in ('headless','bridge'):
        baseline,identity=samples(audit/mode/'create/baseline.wav')
        changed,changed_identity=samples(audit/mode/'create/gain.wav')
        restored,restored_identity=samples(audit/mode/'revision/restored.wav')
        assert max(abs(v) for v in baseline)>.01
        ratio=10**(-3/20);error=max(abs(a-b*ratio) for a,b in zip(changed,baseline))
        assert error<=3/32768
        measured=20*math.log10(math.sqrt(sum(v*v for v in changed)/sum(v*v for v in baseline)))
        assert abs(measured+3)<.02 and restored==baseline
        results.append({'mode':mode,'command':'clip.audioGain','result':'PASS','expectedDb':-3,'measuredDb':measured,
            'everySampleCompared':True,'maxAbsoluteSampleError':error,'tolerance':3/32768,'restoredSamplesIdentical':True,
            'baseline':identity,'changed':changed_identity,'restored':restored_identity})
    result={'schema':'filmcraft-clip-gain-pcm/v1','result':'PASS','results':results,'sourceAuditSha256':sha(audit/'report.json'),
        'driverSha256':sha(Path(__file__)),'tools':{name:{'sha256':sha(path),'version':subprocess.check_output([str(path),'-version'],text=True).splitlines()[0]}
            for name,path in [('ffmpeg',args.ffmpeg),('ffprobe',args.ffprobe)]},
        'scope':'Six original procedural tone native WAV outputs, full stereo24000samples per file. Not video/interpolation/field-processing algorithm or creative qualification.'}
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('PASS native gain -3dB/all stereo samples/exact restored PCM',flush=True)


if __name__=='__main__':main()
