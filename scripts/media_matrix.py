#!/usr/bin/env python3
"""准备来源绑定的媒体输入；仅证明 fixture 准备，不声明原生验收通过。"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess

CASES = {
    'vfr': {'presentationTimestamps': 'strictly increasing with multiple frame intervals',
            'nativeDuration': 'within one output frame of requested duration',
            'avSync': 'compare decoded source and output audio/video timestamps; not lip-sync approval'},
    'long-audio-tail': {'duration': '181.211333333 seconds at 48000 Hz',
                        'tailSamples': 'nonzero valid samples in final non-frame-aligned source interval',
                        'audioPreserved': 'last544 source samples remain nonzero; normalized decoded tail correlation >=0.98 after codec alignment, lag <=1 output frame'},
    'font-change': {'fontIdentity': 'font bytes and license bound; installed native font discovery required',
                    'pixels': 'native rendered caption changes when supported font changes; no silent fallback'},
    'transparent-sequence': {'alpha': 'opaque, half-alpha and transparent input pixels measured',
                            'pixels': 'native PNG composite matches expected background and half-alpha blend within3 of255 per channel'},
    'bad-file': {'rejection': 'corrupt media cannot produce a successful native delivery'},
    'missing-font': {'rejection': 'unavailable font rejected explicitly before successful caption delivery'},
    'dependency-move': {'reopen': 'collected project reopens after source directory becomes unavailable',
                        'bytes': 'all collected dependencies retain input digests',
                        'missingDependency': 'removing a required collected dependency refuses successful delivery'},
}


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def validate_provenance(row):
    if row.get('provenance') not in ('real-source', 'real-derived', 'synthetic', 'font'):
        raise ValueError('provenance_missing')
    if any(not row.get(key) for key in ('source', 'license', 'attribution', 'recipe')):
        raise ValueError('source_license_or_recipe_missing')
    if row['provenance'] == 'synthetic' and row.get('realCapture'):
        raise ValueError('synthetic_real_claim')
    if not isinstance(row.get('parents'), list):
        raise ValueError('parents_missing')


def validate_parent_graph(inputs):
    visiting, visited = set(), set()
    def visit(name):
        if name not in inputs:
            raise ValueError('parent_missing')
        if name in visiting:
            raise ValueError('parent_cycle')
        if name in visited:
            return
        visiting.add(name)
        for parent in inputs[name]['parents']:
            visit(parent)
        visiting.remove(name)
        visited.add(name)
    for name in inputs:
        visit(name)


def validate(manifest, root):
    root = Path(root).resolve()
    if manifest.get('schema') != 'filmcraft-media-fixtures/v1' or manifest.get('nativeAcceptance') != 'NOT_RUN':
        raise ValueError('fixture_preparation_cannot_claim_native_pass')
    inputs = manifest.get('inputs', {})
    if not inputs:
        raise ValueError('inputs_missing')
    for row in inputs.values():
        validate_provenance(row)
        name = PurePosixPath(row.get('path', ''))
        path = root / name
        if not str(name) or name.is_absolute() or '..' in name.parts or not path.resolve().is_relative_to(root):
            raise ValueError('input_path_escape')
        current = path
        while current != root:
            if current.is_symlink():
                raise ValueError('input_symlink')
            current = current.parent
        if not path.is_file() or path.stat().st_size != row.get('bytes') or digest(path) != row.get('sha256'):
            raise ValueError('input_digest_mismatch')
    validate_parent_graph(inputs)
    cases = manifest.get('cases', {})
    if set(cases) != set(CASES):
        raise ValueError('matrix_case_missing_or_unknown')
    for name, row in cases.items():
        if row.get('expected') != CASES[name] or not row.get('knownFailure') or row.get('nativeStatus') != 'NOT_RUN':
            raise ValueError('observable_expectation_or_known_failure_missing')
        if not row.get('inputs') or not set(row['inputs']).issubset(inputs):
            raise ValueError('case_input_missing')
    return {'result': 'PASS', 'scope': 'fixture provenance, input bytes and expected boundaries only',
            'cases': len(cases), 'inputs': len(inputs), 'nativeAcceptance': 'NOT_RUN',
            'creativeAcceptance': 'manual_review', 'userAcceptance': 'NOT_RUN'}


def prepare(film, font, font_license, output, ffmpeg, ffprobe):
    # 发布源文件摘要来自已完成下载的实际字节；不能给任意输入套用官方来源标签。
    for path, expected in (
        (film, 'efa9062d9cdb7a338e40ad530dfdf234806743f29ae6a1a136b97ece4e588e8f'),
        (font, 'bfb7bb691513f12e734dc346c03a03f784912432d7e3fa8e56efcf906fe86b3d'),
        (font_license, 'cee9892f9f0cc8fe882c9e9537ee6a89621d86ee7ceaf70b02e2b2b1c25c061a'),
    ):
        if not Path(path).is_file() or digest(path) != expected:
            raise ValueError('registered_source_digest_mismatch')
    output = Path(output).absolute()
    if output.exists():
        raise ValueError('output_exists')
    output.mkdir(parents=True, mode=0o700)
    inputs, commands = {}, []
    film_url = 'https://download.blender.org/demo/movies/ToS/tears_of_steel_720p.mov'
    font_url = 'https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf'
    def add(name, path, provenance, source, license_name, attribution, parents, recipe):
        inputs[name] = {'path': str(path.relative_to(output)), 'sha256': digest(path), 'bytes': path.stat().st_size,
            'provenance': provenance, 'source': source, 'license': license_name, 'attribution': attribution,
            'parents': parents, 'recipe': recipe, 'realCapture': provenance == 'real-source'}
    for src, name in ((film, 'source-film.mov'), (font, 'NotoSans.ttf'), (font_license, 'OFL.txt')):
        shutil.copyfile(src, output / name)
    credit = '(CC) Blender Foundation | mango.blender.org; Tears of Steel (2012), director Ian Hubert'
    add('source-film', output/'source-film.mov', 'real-source', film_url, 'CC-BY-3.0', credit, [], ['original movie download, including original credit scroll'])
    add('font', output/'NotoSans.ttf', 'font', font_url, 'OFL-1.1', 'The Noto Project Authors', [], ['unchanged font download'])
    add('font-license', output/'OFL.txt', 'font', 'https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt',
        'OFL-1.1', 'The Noto Project Authors', [], ['unchanged accompanying font license'])
    def transform(name, filename, args):
        destination = output/filename
        command = [ffmpeg, '-v', 'error', '-nostdin', *args, str(destination)]
        result = subprocess.run(command, capture_output=True, timeout=180)
        commands.append({'case': name, 'exitCode': result.returncode, 'stderr': result.stderr.decode('utf-8', 'replace')})
        if result.returncode:
            raise ValueError('fixture_transform_failed: '+name)
        add(name, destination, 'real-derived', film_url, 'CC-BY-3.0', credit, ['source-film'],
            [str(arg).replace(str(output), '[FIXTURE_ROOT]') for arg in args])
    transform('vfr', 'vfr.mkv', ['-ss', '30', '-i', str(output/'source-film.mov'), '-t', '3',
        '-vf', "scale=320:180,select='if(lt(t,1.5),1,not(mod(n,2)))'", '-fps_mode', 'vfr',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le'])
    transform('long-audio', 'long-tail.wav', ['-ss', '30', '-i', str(output/'source-film.mov'),
        '-t', '181.211333333333', '-vn', '-ar', '48000', '-c:a', 'pcm_s16le'])
    # alpha 校准是明确的合成输入，与真实拍摄视频分开，不提升为真实透明摄影。
    from PIL import Image
    for index in range(12):
        image = Image.new('RGBA', (32, 18), (0, 0, 0, 0))
        for y in range(2, 12):
            for x in range(2, 12):
                image.putpixel((x, y), (index*20, 0, 0, 255))
        image.putpixel((15, 5), (255, 0, 0, 128))
        path = output/f'alpha-{index:03}.png'; image.save(path)
        add('alpha-'+str(index), path, 'synthetic', 'repository-generated alpha calibration', 'Apache-2.0',
            'FilmCraft contributors', [], ['32x18 RGBA; opaque variable red square, half-alpha red at15,5; transparent background'])
    bad = output/'corrupt.mov'; bad.write_bytes(b'FilmCraft deliberate corrupt movie fixture\x00\xff')
    add('bad-file', bad, 'synthetic', 'repository-generated corrupt bytes', 'Apache-2.0', 'FilmCraft contributors', [], ['deliberately invalid movie bytes'])
    by_case = {'vfr': ['vfr'], 'long-audio-tail': ['long-audio'], 'font-change': ['font', 'font-license', 'vfr'],
        'transparent-sequence': ['alpha-'+str(i) for i in range(12)], 'bad-file': ['bad-file'],
        'missing-font': ['font', 'vfr'], 'dependency-move': ['vfr', 'long-audio']}
    failures = {'vfr': 'CFR assumption drops or repeats source timestamp intervals',
        'long-audio-tail': 'frame-rounded duration truncates the last valid 48000Hz samples',
        'font-change': 'same pixels after actual font substitution or a silently unavailable requested font',
        'transparent-sequence': 'alpha discarded or half-alpha composited as opaque',
        'bad-file': 'invalid bytes accepted as successful media import/export',
        'missing-font': 'FilmCraft-Deliberately-Missing-Font-53 silently substitutes another font',
        'dependency-move': 'old absolute source path still required; missing collected dependency accepted'}
    manifest = {'schema': 'filmcraft-media-fixtures/v1', 'nativeAcceptance': 'NOT_RUN', 'inputs': inputs,
        'cases': {name: {'inputs': by_case[name], 'expected': expected, 'knownFailure': failures[name],
                         'nativeStatus': 'NOT_RUN'} for name, expected in CASES.items()},
        'notes': ['Real movie-derived VFR is an intentional retiming, not original variable-rate camera capture.',
                  'All binary inputs and derivatives remain private; no source footage is committed or published.',
                  'Synthetic alpha and corrupt bytes remain separately labeled; font download is not installation.',
                  'Retain source attribution, source link, license and change description for any later reuse.']}
    probe = subprocess.check_output([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_frames',
        '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(output/'vfr.mkv')])
    pts = [float(row['best_effort_timestamp_time']) for row in json.loads(probe)['frames']]
    intervals = sorted({round(b-a, 3) for a, b in zip(pts, pts[1:])})
    if len(intervals) < 2 or min(intervals) <= 0:
        raise ValueError('fixture_not_vfr')
    import wave
    import array
    import math
    with wave.open(str(output/'long-tail.wav')) as audio:
        frames, rate, channels = audio.getnframes(), audio.getframerate(), audio.getnchannels()
        audio.setpos(frames-544)
        tail = array.array('h', audio.readframes(544))
    import sys
    if sys.byteorder != 'little':
        tail.byteswap()
    tail_rms = math.sqrt(sum((sample/32768)**2 for sample in tail)/len(tail))
    if rate != 48000 or frames != 8698144:
        raise ValueError('audio_sample_count_mismatch')
    if tail_rms <= 0.0001:
        raise ValueError('audio_tail_has_no_observable_signal')
    manifest['measurements'] = {'vfrFrames': len(pts), 'vfrIntervalsSeconds': intervals,
        'audioSamplesPerChannel': frames, 'audioRate': rate, 'audioDurationSeconds': frames/rate,
        'audioChannels': channels, 'tailSamplesPerChannel': 544, 'tailRms': tail_rms,
        'timestampProbeSha256': hashlib.sha256(probe).hexdigest()}
    (output/'timestamp-probe.json').write_bytes(probe)
    report = validate(manifest, output)
    (output/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    report.update(manifestSha256=digest(output/'manifest.json'), measurements=manifest['measurements'], commands=commands)
    (output/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('film', 'font', 'font-license', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    for name in ('ffmpeg', 'ffprobe'):
        parser.add_argument('--'+name, required=True)
    print(json.dumps(prepare(**vars(parser.parse_args())), ensure_ascii=False))
