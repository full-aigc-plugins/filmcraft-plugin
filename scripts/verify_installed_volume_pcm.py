#!/usr/bin/env python3
"""将固定安装的八种音量快捷命令导出为WAV，以独立FFmpeg解码逐样本验证dB倍率。"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import subprocess


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installed-plugin', type=Path, required=True)
    parser.add_argument('--runtime-home', type=Path, required=True)
    parser.add_argument('--timeline-audit', type=Path, required=True)
    parser.add_argument('--ffmpeg', type=Path, required=True)
    parser.add_argument('--ffprobe', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    root.mkdir(mode=0o700)
    installed = args.installed_plugin.resolve(strict=True)
    skill = installed / 'skills/filmcraft-use'
    runtime = args.runtime_home.resolve(strict=True)
    audit = args.timeline_audit.resolve(strict=True)
    commands = load(skill / 'scripts/commands.py', 'volume_pcm_commands')
    desktop = load(skill / 'scripts/desktop_session.py', 'volume_pcm_desktop')
    helper = load(Path(__file__).with_name('verify_installed_timeline_edits.py'), 'volume_pcm_helper')
    changes = [('clip.volumeUp', 1), ('clip.volumeDown', -1), ('clip.volumeUpMany', 6), ('clip.volumeDownMany', -6),
               ('clip.nudgeVolumeUp1', 1), ('clip.nudgeVolumeUp3', 3), ('clip.nudgeVolumeDown1', -1), ('clip.nudgeVolumeDown3', -3)]
    results = []
    for mode in ('headless', 'bridge'):
        work = root / mode
        work.mkdir()
        source = audit / mode / 'fixture/baseline.fcproj'
        before = sha(source)
        original = json.loads((audit / mode / 'fixture-receipt.private.json').read_text())
        audio_clip = original['steps'][-2]['result']['audio'][0]['items'][0]['clip']
        policy = commands.load('execution_permissions').from_cli([str(root), str(audit)], [str(work), str(runtime)])

        def export(name):
            return helper.op('file.exportMedia', {'path': {'$output': name + '.wav'}, 'format': 'wav',
                'range': 'custom', 'startSeconds': 12, 'endSeconds': 12.25, 'wait': True})

        operations = [helper.op('file.open', {'path': {'$ref': 'original.path'}}), export('baseline')]
        for index, (identifier, db) in enumerate(changes):
            operations += [helper.op('timeline.select', {'clips': [audio_clip], 'add': False, 'toggle': False}),
                helper.op(identifier), export('gain-' + str(index)), helper.op('edit.undo')]
        operations += [export('restored'), helper.op('file.saveAs', {'path': {'$output': 'preserved.fcproj'}})]
        plan = {'schema': 'craft-command-plan/v1', 'operations': operations}
        write(work / 'plan.private.json', plan)
        output = work / 'delivery'
        if mode == 'headless':
            receipt = commands.execute(plan, output, runtime_home=runtime, permissions=policy, inputs={'original': source})
        else:
            receipt = desktop.run(plan, output, runtime_home=runtime, permissions=policy, inputs={'original': source})
            proof = json.loads((output / 'desktop-session.json').read_text())
            assert proof['ownedProcessesStopped'] and proof['listenerOwnedByPID'] and proof['sessionsStarted'] == 1
        write(work / 'receipt.private.json', receipt)
        assert receipt['result'] == 'PASS', receipt.get('error')
        assert sha(source) == before and helper.project(output / 'preserved.fcproj') == helper.project(source)

        def samples(name):
            path = output / (name + '.wav')
            info = json.loads(subprocess.check_output([str(args.ffprobe), '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
            stream = info['streams'][0]
            assert len(info['streams']) == 1 and stream['codec_type'] == 'audio'
            assert stream['channels'] == 2 and int(stream['sample_rate']) == 48000
            assert abs(float(info['format']['duration']) - .25) <= 1 / 48000
            raw = subprocess.check_output([str(args.ffmpeg), '-v', 'error', '-nostdin', '-i', str(path), '-map', '0:a:0', '-f', 'f32le', '-acodec', 'pcm_f32le', '-'])
            values = struct.unpack('<' + str(len(raw) // 4) + 'f', raw)
            assert len(values) == 12000 * 2 and all(math.isfinite(value) for value in values)
            return values, {'sha256': sha(path), 'codec': stream['codec_name'], 'frames': 12000, 'channels': 2,
                            'sampleRate': 48000, 'pcmSha256': hashlib.sha256(raw).hexdigest()}

        baseline, identity = samples('baseline')
        assert max(abs(value) for value in baseline) > .01
        rows = []
        for index, (identifier, db) in enumerate(changes):
            measured, artifact = samples('gain-' + str(index))
            ratio = 10 ** (db / 20)
            error = max(abs(actual - expected * ratio) for actual, expected in zip(measured, baseline))
            # PCM16的基准和增益文件各自量化；容差明确覆盖两次量化，且远小于最小1dB变化。
            assert error <= 3 / 32768, (mode, identifier, error)
            rms_ratio = math.sqrt(sum(value * value for value in measured) / sum(value * value for value in baseline))
            assert abs(20 * math.log10(rms_ratio) - db) < .02
            rows.append({'command': identifier, 'result': 'PASS', 'expectedDb': db,
                         'measuredDb': 20 * math.log10(rms_ratio), 'maxAbsoluteSampleError': error,
                         'tolerance': 3 / 32768, 'everySampleCompared': True, 'artifact': artifact})
        restored, restored_identity = samples('restored')
        assert restored == baseline
        observations = {'result': 'PASS', 'mode': mode, 'sourceProjectSha256': before,
            'sourcePreserved': True, 'wholeProjectPreserved': True, 'baseline': identity,
            'restored': restored_identity, 'restoredSamplesIdentical': True, 'commands': rows,
            'receiptSha256': sha(work / 'receipt.private.json'), 'runtimeSha256': receipt['runtimeSha256'],
            'scope': 'Full two-channel .25s native WAV exports of original procedural bars/tone fixture, external FFmpeg/ffprobe oracle, no external media, not perceptual/creative quality.'}
        write(work / 'pcm-observations.json', observations)
        results.append({'mode': mode, 'result': 'PASS', 'commands': 8, 'nativeWavOutputs': 10,
                        'observationsSha256': sha(work / 'pcm-observations.json')})
        print(mode, 'PASS8 volume commands/all stereo samples/native WAV', flush=True)
    write(root / 'report.json', {'schema': 'filmcraft-installed-volume-pcm-audit/v1', 'result': 'PASS',
        'driverSha256': sha(Path(__file__)), 'results': results,
        'measurementTools': {name: {'sha256': sha(path), 'version': subprocess.check_output([str(path), '-version'], text=True).splitlines()[0]}
                             for name, path in [('ffmpeg', args.ffmpeg), ('ffprobe', args.ffprobe)]},
        'fullCommandAcceptance': 'NOT_PROVEN', 'remainingTask': '8.3'})


if __name__ == '__main__':
    main()
