#!/usr/bin/env python3
"""由真实固定宿主快照执行七类媒体矩阵，绑定公开运行时与全部安装文件。"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_fixed_install import release_entry, owner_helper, verify_code_files
from verify_media_matrix import audio_gate, pixel_gate
from media_matrix import CASES, digest


def validate_fixed_media(host, report, expected):
    """逐维验收；不从安装成功或候选总体 PASS 推导媒体资格。"""
    if (host.get('schema')!='filmcraft-fixed-host-verification/v1' or host.get('result')!='PASS'
            or host.get('loadingErrors')!=0 or any(host.get('plugin',{}).get(k)!=expected[k] for k in ('ref','sha'))
            or report.get('result')!='PASS' or report.get('layer')!='native-matrix' or not report.get('installationPreserved')
            or set(report.get('cases',{}))!=set(CASES)
            or any(r.get('status')!='PASS' or not r.get('measurements') for r in report.get('cases',{}).values())):
        raise ValueError('fixed_media_identity_or_matrix_incomplete')
    rows={k:v['measurements'] for k,v in report['cases'].items()}
    vfr=rows['vfr'];long=rows['long-audio-tail'];alpha=rows['transparent-sequence'];fonts=rows['font-change'];move=rows['dependency-move']
    if (vfr.get('videoFrames')!=36 or vfr.get('sourceFrames')!=54 or len(vfr.get('frameAlignment',[]))!=3
            or not vfr.get('fullDecode') or abs(vfr.get('durationSeconds',0)-3)>1/12
            or len(vfr.get('audio',[]))!=1 or len(vfr.get('sourceFrameIntervals',[]))<2):
        raise ValueError('fixed_vfr_measurements_missing')
    audio_gate(vfr['audio'][0],22400,1/12)
    if long.get('sourceSamplesPerChannel')!=8698144 or not long.get('fullDecode') or long.get('pcm',{}).get('decodedSamplesPerChannel')!=8698144:
        raise ValueError('fixed_audio_tail_missing')
    for codec in ('pcm','aac'):
        tails=long.get(codec,{}).get('tail',[])
        if len(tails)!=2 or {r.get('channel') for r in tails}!={0,1}:raise ValueError('fixed_audio_channels_missing')
        for row in tails:audio_gate(row,544,1/12)
    pixel_gate(alpha.get('pixels',[]),12)
    if not alpha.get('fullDecode') or alpha.get('videoFrames')!=12 or alpha.get('halfAlphaRedExpected')!=188:
        raise ValueError('fixed_alpha_decode_missing')
    if (fonts.get('changedPixels',0)<=0 or len(fonts.get('fonts',[]))!=2 or len(fonts.get('deliveries',[]))!=2
            or any(not r.get('licenseSha256') or not r.get('fontSha256') for r in fonts['fonts'])):
        raise ValueError('fixed_font_identity_missing')
    for rejection in (rows['bad-file'],rows['missing-font'],move.get('missingDependency',{})):
        if (not rejection.get('refused') or rejection.get('successfulDeliveryExists') is not False
                or not rejection.get('sourcePreserved')):raise ValueError('fixed_failure_path_unconfirmed')
    if (not move.get('sourceDirectoryUnavailable') or not move.get('relinkedPixelsUnchanged')
            or not move.get('fullDecode') or len(move.get('collectedAssetSha256',{}))!=2):
        raise ValueError('fixed_relink_unconfirmed')


def verify(host, repository, authority, ref, fixtures, output, upstream, ffmpeg, ffprobe):
    host=Path(host).resolve();output=Path(output).absolute()
    if output.exists() or output.is_symlink():raise ValueError('output_exists')
    receipt=json.loads((host/'host-receipt.json').read_text());expected=release_entry(repository,ref)
    if receipt.get('result')!='PASS' or receipt.get('plugin')!=expected:raise ValueError('fixed_host_mismatch')
    directories={name:Path(path).resolve() for name,path in json.loads((host/'installed-directories.private.json').read_text()).items()}
    if set(directories)!=set(expected['skills']):raise ValueError('fixed_skill_inventory_mismatch')
    helper,identity=owner_helper(authority)
    if receipt['helper']!=identity:raise ValueError('fixed_helper_identity_mismatch')
    for name,path in directories.items():
        if not path.is_relative_to(host/'host-config'):raise ValueError('fixed_skill_outside_host')
        helper.verify_installed_skill(path,expected);verify_code_files(path.parent.parent,expected['codeFilesSha256'])
    skill=directories['filmcraft-use'];core=skill.parent.parent
    spec=importlib.util.spec_from_file_location('installed_media_matrix',core/'scripts/verify_media_matrix.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    report=module.verify(skill,fixtures,output,output/'fresh-public-runtime',ffmpeg,ffprobe,upstream=upstream)
    for path in directories.values():helper.verify_installed_skill(path,expected);verify_code_files(core,expected['codeFilesSha256'])
    lock=json.loads((skill/'scripts/runtime.lock.json').read_text());artifact=lock['artifacts'][report['runtime']['platform']]
    if report['runtime']['binarySha256']!=artifact['binarySha256'] or report['runtime']['version']!=lock['resolvedVersion']:
        raise ValueError('fixed_runtime_identity_mismatch')
    validate_fixed_media(receipt,report,expected)
    report.update(fixedInstallation='PASS',hostReceiptSha256=digest(host/'host-receipt.json'),plugin=expected,
                  allInstalledSkillsUnchanged=True,installedSkillCount=len(directories),scope='seven real-derived/synthetic media cases in actual isolated fixed Codex installation; bounded platform/codec scope; full V1 remains open')
    (output/'fixed-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('host','repository','authority','fixtures','output','upstream'):p.add_argument('--'+name,type=Path,required=True)
    for name in ('ref','ffmpeg','ffprobe'):p.add_argument('--'+name,required=True)
    r=verify(**vars(p.parse_args()));print(json.dumps({'result':r['result'],'fixedInstallation':r['fixedInstallation'],'skills':r['installedSkillCount']}))
