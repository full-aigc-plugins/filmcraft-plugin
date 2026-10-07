#!/usr/bin/env python3
"""原生时间线、素材收集、字幕与局部修订的独立执行入口。"""
import argparse
import sys
sys.dont_write_bytecode = True
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

TICKS = 254016000000
def exchange_report(root,outputs,warnings):
    spec=importlib.util.spec_from_file_location('craft_exchange_loss',Path(__file__).with_name('exchange_loss.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.write_report(root,outputs,warnings)

ALLOWED = {'native.command', 'asset.import', 'timeline.place', 'timeline.trim', 'timeline.move',
           'timeline.setTrack', 'timeline.select', 'clip.replaceFromBin',
           'captions.newTrack', 'captions.setStyle', 'caption.add',
           'captions.setText', 'captions.delete', 'captions.setTrack', 'mixer.setStrip',
           'effects.toggleAnimation', 'effects.setParam', 'lumetri.setInputLut'}

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def resolve(value, bindings):
    if isinstance(value, dict):
        if set(value) == {'$ref'}:
            try:
                parts = value['$ref'].split('.')
                result = bindings[parts[0]]
                for field in parts[1:]:
                    result = result[int(field)] if isinstance(result, list) else result[field]
                return result
            except (KeyError, IndexError, TypeError, ValueError, AttributeError):
                raise ValueError('unresolved_reference: ' + str(value['$ref'])) from None
        return {key: resolve(item, bindings) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve(item, bindings) for item in value]
    return value


def load_module(name):
    spec = importlib.util.spec_from_file_location('craft_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ticks(value):
    if not isinstance(value, str) or not re.fullmatch(r'0|[1-9][0-9]*', value):
        raise ValueError('ticks_require_decimal_string')
    number = int(value)
    if number > 2**63 - 1:
        raise ValueError('ticks_out_of_range')
    return number


def source_range_valid(clip, probe, frame_rate):
    """核验真实源消耗；仅允许正常速率纯音频的原生尾部帧填充。"""
    speed = clip.get('speed')
    if type(speed) not in (int, float) or not math.isfinite(speed) or speed == 0:
        raise ValueError('invalid_clip_speed')
    start, duration = clip['sourceIn'], clip['duration']
    available = ticks(probe['duration'])
    if start < 0 or start >= available or duration <= 0:
        return False
    consumed = Fraction(duration) * abs(Fraction(str(speed)))
    if start + consumed <= available:
        return True
    if speed != 1 or probe.get('kind') != 'AudioOnly' or not probe.get('audio') or probe.get('video'):
        return False
    # 与引擎 FrameRate::snap_nearest / make_track_item 保持整数语义；中点取较早帧。
    num, den = frame_rate['num'], frame_rate['den']
    if type(num) is not int or type(den) is not int or num <= 0 or den <= 0:
        return False
    unit = TICKS * den
    remaining = available - start
    frame = remaining * num // unit
    lower, upper = frame * unit // num, (frame + 1) * unit // num
    snapped = lower if remaining - lower <= upper - remaining else upper
    return duration == max(snapped, unit // num)


def precise(value):
    """将检查结果中的时间字段转为十进制字符串，保留对象 ID。"""
    if isinstance(value, list):
        return [precise(x) for x in value]
    if isinstance(value, dict):
        return {k: str(v) if k in {'start', 'duration', 'sourceIn', 'time', 'in', 'out', 'playhead', 'end'} and type(v) is int else precise(v) for k, v in value.items()}
    return value


def explicit_clip(value):
    return ((type(value) is int and 0 < value <= 2**64-1)
            or (isinstance(value, dict) and set(value) == {'$ref'}
                and isinstance(value['$ref'], str)
                and re.fullmatch(r'[a-zA-Z][\w-]*(?:\.[a-zA-Z0-9_-]+)+', value['$ref']) is not None))


def finite_parameter(value):
    if type(value) in (int, float):
        return abs(value) <= sys.float_info.max and math.isfinite(value)
    if type(value) in (str, bool):
        return True
    return isinstance(value, list) and bool(value) and all(finite_parameter(v) for v in value)


def native_module():
    spec = importlib.util.spec_from_file_location('craft_native_workflow', Path(__file__).with_name('native_workflow.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def validate(plan, prior_assets=None):
    if not isinstance(plan, dict) or not isinstance(plan.get('operations'), list):
        raise ValueError('operations_required')
    if not isinstance(plan.get('assets', {}), dict):
        raise ValueError('invalid_assets')
    aliases = set()
    for item in plan['operations']:
        if not isinstance(item, dict):
            raise ValueError('invalid_operation')
        if item.get('command') == 'native.command':
            native_module().validate(item.get('params'))
        if item.get('command') not in ALLOWED:
            raise ValueError('unsupported_command')
        alias = item.get('as')
        if alias is not None:
            if alias in aliases:
                raise ValueError('duplicate_alias')
            if not isinstance(alias, str) or not re.fullmatch(r'[a-zA-Z][\w-]*', alias):
                raise ValueError('invalid_alias')
            aliases.add(alias)
        if not isinstance(item.get('params', {}), dict):
            raise ValueError('invalid_params')
        if item['command'] in ('effects.toggleAnimation', 'effects.setParam'):
            params = item.get('params', {})
            required = {'clip', 'effect', 'param'}
            allowed = required | {'mask'}
            if item['command'] == 'effects.setParam':
                required |= {'value'}; allowed |= {'value', 'time'}
            effect = params.get('effect')
            if (not required <= set(params) or set(params)-allowed
                    or not explicit_clip(params.get('clip'))
                    or not ((isinstance(effect, str) and effect.strip()) or (type(effect) is int and effect >= 0))
                    or not isinstance(params.get('param'), str) or not params['param'].strip()
                    or ('mask' in params and (type(params['mask']) is not int or params['mask'] < 0))
                    or ('value' in required and not finite_parameter(params['value']))):
                raise ValueError('invalid_effect_params')
            if 'time' in params:
                ticks(params['time'])
        if item['command'] == 'lumetri.setInputLut':
            params = item.get('params', {})
            if (set(params) != {'clip', 'asset'} or not explicit_clip(params.get('clip'))
                    or not isinstance(params.get('asset'), str)):
                raise ValueError('invalid_lut_params')
            registered = {**(prior_assets or {}), **plan.get('assets', {})}.get(params['asset'])
            if registered is None:
                if prior_assets is not None or 'expectedProjectSha256' not in plan:
                    raise ValueError('registered_lut_required')
            elif not isinstance(registered, dict) or registered.get('kind') != 'lut':
                raise ValueError('registered_lut_required')
        if item['command'] == 'asset.import':
            registered = {**(prior_assets or {}), **plan.get('assets', {})}.get(item.get('params', {}).get('asset'))
            if isinstance(registered, dict) and registered.get('kind') == 'lut':
                raise ValueError('lut_is_not_media')
        if item['command'] == 'mixer.setStrip':
            params = item.get('params', {})
            # 首版仅允许显式音轨的静态增益，避免混入录音或总线重路由操作。
            value = params.get('volumeDb')
            if (set(params) != {'strip', 'volumeDb'}
                    or not isinstance(params.get('strip'), str)
                    or not re.fullmatch(r'A[1-9][0-9]*', params['strip'])
                    or type(value) not in (int, float)
                    or abs(value) > sys.float_info.max or not math.isfinite(value)):
                raise ValueError('invalid_track_gain')
    if not isinstance(plan.get('assets',{}),dict):
        raise ValueError('invalid_assets')
    for asset in plan.get('assets',{}).values():
        if (not isinstance(asset,dict) or set(asset)-{'path','sha256','kind'}
                or asset.get('kind') not in (None,'image-sequence','segmented-image-sequence','lut')):
            raise ValueError('invalid_asset_registration')
    for time in plan.get('frames', ['0']):
        ticks(time)
    if 'document' in plan:
        doc = plan['document']
        if set(doc) != {'name', 'width', 'height', 'frameRate'}:
            raise ValueError('invalid_document')
        if any(type(doc[k]) is not int or not 0 < doc[k] <= 16384 for k in ('width', 'height')):
            raise ValueError('invalid_document_size')
        rate = doc['frameRate']
        if set(rate) != {'num', 'den'} or any(type(rate[k]) is not int or rate[k] <= 0 for k in rate) or not 1 <= Fraction(rate['num'], rate['den']) <= 240:
            raise ValueError('invalid_frame_rate')
    if set(plan.get('export', {})) - {'audioRequired', 'burnCaptions'} or any(type(value) is not bool for value in plan.get('export', {}).values()):
        raise ValueError('invalid_export')


def export_settings(plan, caption_state):
    """有可见字幕轨时默认烧录；仅接受显式布尔值关闭烧录。"""
    return {'burnCaptions': plan.get('export', {}).get('burnCaptions', any(track['enabled'] for track in caption_state['tracks']))}


def run(cli, argv, cwd=None):
    result = subprocess.run([cli] + argv, capture_output=True, text=True, timeout=180, cwd=cwd)
    if result.returncode:
        raise RuntimeError('cli_failed: ' + result.stdout[-2000:] + result.stderr[-2000:])
    return result.stdout


def preflight_assets(new_assets, prior_assets, source):
    """在运行时安装与暂存执行前校验素材；复制时再次校验以检测并发变化。"""
    for registered, group in ((True, prior_assets), (False, new_assets)):
        for alias, asset in group.items():
            kind = asset.get('kind')
            if not re.fullmatch(r'[a-zA-Z][\w-]*', alias) or not re.fullmatch(r'[a-f0-9]{64}', asset['sha256']):
                raise ValueError('invalid_asset')
            path = source / asset['path'] if registered else Path(asset['path'])
            if registered:
                if path.is_symlink() or (kind == 'image-sequence' and path.parent.is_symlink()):
                    raise ValueError('invalid_asset_path')
                path = path.resolve()
                if not path.is_relative_to(source):
                    raise ValueError('invalid_asset_path')
            if kind == 'image-sequence':
                load_module('sequence_assets').validate_sequence(path, asset['sha256'])
            elif kind == 'segmented-image-sequence':
                load_module('sequence_assets').validate_segmented_source(path, asset['sha256'])
            else:
                if kind not in (None, 'lut'):
                    raise ValueError('unsupported_asset_kind')
                if kind == 'lut' and path.suffix.lower() not in ('.cube', '.3dl'):
                    raise ValueError('unsupported_lut_format')
                if path.is_symlink() or not path.is_file() or sha(path) != asset['sha256']:
                    raise ValueError('asset_digest_mismatch: ' + alias)


def execute(plan, output, runtime_home=None, source=None):
    validate(plan)
    output = Path(output).absolute()
    output = output.parent.resolve()/output.name
    if output.exists() or output.is_symlink():
        raise ValueError('output_exists')
    source_project, source_hash, prior = None, None, {}
    bindings, assets = {}, {}
    if source:
        source = Path(source).resolve()
        source_project = source / 'project.fcproj'
        if source_project.is_symlink():
            raise ValueError('invalid_source')
        prior = json.loads((source / 'manifest.json').read_text())
        source_hash = sha(source_project)
        if source_hash != prior['files']['project.fcproj'] or source_hash != plan.get('expectedProjectSha256'):
            raise ValueError('revision_conflict')
        if 'document' in plan:
            raise ValueError('revision_cannot_recreate_document')
        bindings = prior['bindings']
    elif 'document' not in plan:
        raise ValueError('document_required')
    validate(plan, prior.get('assets', {}))
    preflight_assets(plan.get('assets', {}), prior.get('assets', {}), source)
    installed = load_module('bootstrap').install(
        json.loads(Path(__file__).with_name('runtime.lock.json').read_text()),
        runtime_home or os.environ.get('CRAFT_RUNTIME_HOME', str(Path.home() / '.local/share/craft-runtimes')))
    cli = installed['executable']
    output.parent.mkdir(parents=True, exist_ok=True)
    recovery_state = {}
    execution_identity = {'planHash': hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest(),
                          'inputHashes': {name: asset['sha256'] for name, asset in plan.get('assets', {}).items()},
                          'projectRevision': source_hash, 'runtimeSha256': installed['binarySha256']}
    with load_module('output_guard').claim(output, execution_identity), load_module('preserved_stage').preserved_stage(output, '.filmcraft-', recovery_state) as temporary:
        stage = Path(temporary)
        media = stage / 'assets'
        media.mkdir()
        receipts = []
        recovery_state['operations'] = receipts
        def copy_asset(alias, path, digest, kind=None):
            if not re.fullmatch(r'[a-zA-Z][\w-]*', alias) or not re.fullmatch(r'[a-f0-9]{64}', digest):
                raise ValueError('invalid_asset')
            if kind == 'image-sequence':
                return load_module('sequence_assets').copy_sequence(path, digest, media / alias)
            if kind == 'segmented-image-sequence':
                return load_module('sequence_assets').copy_segmented_sequence(path, digest, media / alias)
            if kind not in (None, 'lut'):
                raise ValueError('unsupported_asset_kind')
            if kind == 'lut' and Path(path).suffix.lower() not in ('.cube', '.3dl'):
                raise ValueError('unsupported_lut_format')
            path = Path(path)
            if path.is_symlink() or not path.is_file() or sha(path) != digest:
                raise ValueError('asset_digest_mismatch: ' + alias)
            target = media / (alias + path.suffix.lower())
            if target.exists():
                raise ValueError('duplicate_asset')
            shutil.copyfile(path, target)
            if sha(target) != digest:
                raise ValueError('asset_changed_during_copy')
            return target
        for alias, asset in prior.get('assets', {}).items():
            registered = source / asset['path']
            if registered.is_symlink() or (asset.get('kind')=='image-sequence' and registered.parent.is_symlink()):
                raise ValueError('invalid_asset_path')
            path = registered.resolve()
            if not path.is_relative_to(source):
                raise ValueError('invalid_asset_path')
            target = copy_asset(alias, path, asset['sha256'], asset.get('kind'))
            assets[alias] = dict(asset, staging=str(target))
            if asset.get('kind') == 'image-sequence':
                descriptor = load_module('sequence_assets').validate_sequence(target, asset['sha256'])
                assets[alias]['sequenceMetadata'] = {k:v for k,v in descriptor.items() if k!='frames'}
                assets[alias]['sequenceStaging'] = str(target)
                assets[alias]['staging'] = str(target.parent/descriptor['frames'][0]['location'])
        for alias, asset in plan.get('assets', {}).items():
            if alias in assets:
                raise ValueError('asset_alias_exists')
            target = copy_asset(alias, asset['path'], asset['sha256'], asset.get('kind'))
            if asset.get('kind') in ('image-sequence','segmented-image-sequence'):
                target_sha = sha(target)
                descriptor = load_module('sequence_assets').validate_sequence(target, target_sha)
                assets[alias] = {'kind':'image-sequence', 'sha256':target_sha,
                                'sequenceMetadata':{k:v for k,v in descriptor.items() if k!='frames'},
                                'sequenceStaging':str(target), 'staging':str(target.parent/descriptor['frames'][0]['location'])}
                if asset.get('kind') == 'segmented-image-sequence':
                    assets[alias]['sourceSequenceSha256'] = asset['sha256']
            elif asset.get('kind') == 'lut':
                assets[alias] = {'kind':'lut', 'sha256':asset['sha256'], 'staging':str(target)}
            else:
                probe = json.loads(run(cli, ['probe', str(target)]))
                assets[alias] = {'sha256': asset['sha256'], 'probe': precise(probe), 'staging': str(target)}
        argv = [cli] + (['--project', str(source_project)] if source_project else []) + ['mcp']
        with load_module('mcp_session').Session(argv) as session:
            def call(name, args):
                recovery_state['lastAttempt'] = {'tool': name, 'arguments': args, 'phase': 'submitted'}
                result = session.request('tools/call', {'name': name, 'arguments': args})
                recovery_state['lastAttempt']['phase'] = 'reply_received'
                if result.get('isError'):
                    raise RuntimeError('command_failed: ' + name + ': ' + json.dumps(result['content']))
                content = [x['text'] for x in result.get('content', []) if x.get('type') == 'text']
                if len(content) != 1:
                    raise RuntimeError('unexpected_result')
                value = json.loads(content[0])
                receipts.append({'tool': name, 'arguments': args, 'result': value})
                return value
            def command(identifier, params):
                return call('command_run', {'id': identifier, 'params': params})
            def sequence_probe(asset):
                # 核验原生实际媒体属性；不能把单张图片 probe 伪装为序列。
                command('project.select', {'items':[asset['item']]})
                properties = command('file.mediaProperties', {'items':[asset['item']]})
                metadata = asset['sequenceMetadata']; rate = metadata['frameRate']
                if len(properties)!=1:
                    raise ValueError('sequence_native_properties_mismatch')
                actual = properties[0]; video = actual.get('video', {})
                expected_ticks = TICKS*metadata['frameCount']*rate['den']//rate['num']
                if (actual.get('type')!='ImageSequence' or actual.get('offline')
                        or actual.get('duration',{}).get('ticks')!=expected_ticks
                        or video.get('frameRate')!=float(Fraction(rate['num'],rate['den']))
                        or (video.get('width'),video.get('height'))!=(metadata['width'],metadata['height'])
                        or video.get('alpha') is not True):
                    raise ValueError('sequence_native_properties_mismatch')
                return {'kind':actual['type'], 'duration':str(actual['duration']['ticks']), 'audio':None,
                        'video':{'width':video['width'],'height':video['height'],'frame_rate':rate,'has_alpha':video['alpha']},
                        'nativeProperties':precise({k:v for k,v in actual.items() if k!='path'})}
            if not source_project:
                doc = plan['document']
                command('file.newProject', {'name': doc['name']})
                rate = doc['frameRate']
                bindings['sequence'] = command('file.newSequence', {'name': doc['name'], 'width': doc['width'], 'height': doc['height'], 'fps': float(Fraction(rate['num'], rate['den']))})
            else:
                # 即使原目录已移动，也只对摘要一致的包内素材进行原生重关联。
                for asset in assets.values():
                    if 'item' in asset:
                        command('media.relink', {'item': asset['item'], 'path': asset['staging'], 'relinkOthers': False})
                        if asset.get('kind')=='image-sequence':
                            asset['probe'] = sequence_probe(asset)
            for operation in plan['operations']:
                identifier = operation['command']
                params = resolve(operation.get('params', {}), bindings)
                if identifier in ('effects.setParam', 'effects.toggleAnimation'):
                    validate({'operations':[{'command':identifier, 'params':params}]})
                if identifier == 'lumetri.setInputLut' and not (type(params['clip']) is int and 0 < params['clip'] <= 2**64-1):
                    raise ValueError('invalid_lut_params')
                if identifier == 'native.command':
                    result = native_module().execute(session, params, recovery_state, receipts, stage)
                elif identifier == 'asset.import':
                    asset = assets[params['asset']]
                    if 'item' in asset:
                        raise ValueError('asset_already_imported')
                    if asset.get('kind')=='image-sequence':
                        rate = asset['sequenceMetadata']['frameRate']
                        imported = command('file.importImageSequence', {'path':asset['staging'],'frameRate':rate})
                        details = imported.get('imageSequences', [])
                        if (imported.get('frameRate')!=rate or len(details)!=1
                                or details[0].get('frames')!=asset['sequenceMetadata']['frameCount'] or details[0].get('missing')):
                            raise ValueError('sequence_native_import_mismatch')
                    else:
                        imported = command('file.import', {'paths': [asset['staging']]})
                    if imported['errors'] or len(imported['items']) != 1:
                        raise ValueError('import_failed')
                    asset['item'] = imported['items'][0]
                    if asset.get('kind')=='image-sequence':
                        asset['probe'] = sequence_probe(asset)
                    result = {'item': asset['item']}
                elif identifier == 'lumetri.setInputLut':
                    asset = assets[params['asset']]
                    result = command(identifier, {'clip':params['clip'], 'path':asset['staging']})
                elif identifier == 'timeline.place':
                    asset = next((x for x in assets.values() if x.get('item') == params.get('item')), None)
                    if not asset or any(k in params for k in ('seconds', 'frame')):
                        raise ValueError('registered_asset_and_ticks_required')
                    start = ticks(params.get('time', '0'))
                    source_in = ticks(params.get('sourceIn', '0'))
                    available = ticks(asset['probe']['duration'])
                    duration = ticks(params.get('duration', str(available - source_in)))
                    if duration <= 0 or source_in + duration > available:
                        raise ValueError('clip_out_of_range')
                    result = command(identifier, dict(params, time=start, sourceIn=source_in, duration=duration))
                elif identifier == 'caption.add':
                    start = ticks(params['startTicks'])
                    duration = ticks(params['durationTicks'])
                    sequence = call('sequence_inspect', {})
                    if duration <= 0 or start + duration > sequence['duration']:
                        raise ValueError('caption_out_of_range')
                    result = command('captions.add', {'track': params.get('track', 'C1'), 'text': params['text'], 'time': start, 'durationSeconds': duration / TICKS})
                else:
                    if identifier == 'clip.replaceFromBin':
                        if not params.get('clips'):
                            raise ValueError('explicit_clips_required')
                        command('timeline.select', {'clips': params['clips'], 'add': False, 'toggle': False})
                        command('project.select', {'items': [params['item']]})
                    if identifier == 'captions.setStyle' and 'font' in params:
                        fonts = command('fonts.list', {'system': True})
                        if params['font'] not in {x['family'] for x in fonts}:
                            raise ValueError('missing_font: ' + params['font'])
                    if identifier == 'effects.setParam' and 'time' in params:
                        params['time'] = ticks(params['time'])
                    if identifier == 'timeline.trim':
                        value = params.get('delta')
                        if not isinstance(value, str) or not re.fullmatch(r'-?(0|[1-9][0-9]*)', value):
                            raise ValueError('ticks_require_decimal_string')
                        params['delta'] = int(value)
                    if identifier == 'timeline.move':
                        for move in params.get('moves', []):
                            move['time'] = ticks(move['time'])
                    result = command(identifier, params)
                if operation.get('as'):
                    if operation['as'] in bindings:
                        raise ValueError('alias_already_exists')
                    bindings[operation['as']] = result
            sequence = call('sequence_inspect', {})
            if plan.get('document') and sequence['settings']['frame_rate'] != plan['document']['frameRate']:
                raise ValueError('frame_rate_not_preserved')
            if sequence['duration'] <= 0:
                raise ValueError('empty_sequence')
            for track in sequence['video'] + sequence['audio']:
                for clip in track['items']:
                    asset = next((x for x in assets.values() if x.get('item') == clip['item']), None)
                    if not asset or not source_range_valid(clip, asset['probe'], sequence['settings']['frame_rate']):
                        raise ValueError('clip_out_of_range: ' + str(clip['clip']))
            caption_state = command('captions.list', {})
            families = {x['family'] for x in command('fonts.list', {'system': True})}
            for track in caption_state['tracks']:
                if track['style']['font'] not in families:
                    raise ValueError('missing_font: ' + track['style']['font'])
                for caption in track['captions']:
                    if caption['start'] < 0 or caption['end'] > sequence['duration'] or caption['end'] <= caption['start']:
                        raise ValueError('caption_out_of_range')
            for time in plan.get('frames', ['0']):
                if ticks(time) >= sequence['duration']:
                    raise ValueError('frame_out_of_range')
            command('file.saveAs', {'path': str(stage / 'checkpoint.fcproj')})
            if source_project and sha(source_project) != source_hash:
                raise ValueError('revision_conflict')
            # 原生收集必须使用最终目录：引擎保存绝对素材引用。失败目录保留诊断，不作为交付。
            load_module('preserved_stage').claim_output(output, recovery_state)
            try:
                collected = command('file.projectManager', {'destination': str(output), 'mode': 'collect', 'projectName': 'project', 'excludeUnused': False, 'includeProxies': False, 'wait': True})
                by_item = {x['item']: x for x in collected['files']}
                for alias, asset in assets.items():
                    if asset.get('kind') == 'lut':
                        directory = output / 'luts'; directory.mkdir(exist_ok=True)
                        target = directory / (alias + Path(asset['staging']).suffix.lower())
                        shutil.copyfile(asset['staging'], target)
                        if sha(target) != asset['sha256']:
                            raise ValueError('collected_asset_mismatch')
                        asset['path'] = str(target.relative_to(output))
                        del asset['staging']
                        continue
                    if 'item' not in asset:
                        raise ValueError('asset_not_imported: ' + alias)
                    entry = by_item[asset['item']]; target = Path(entry['to'])
                    if asset.get('kind')=='image-sequence':
                        descriptor = load_module('sequence_assets').validate_sequence(Path(asset['sequenceStaging']),asset['sha256'])
                        files = entry.get('sequenceFiles', [])
                        if len(files)!=descriptor['frameCount']:
                            raise ValueError('collected_sequence_mismatch')
                        for frame, expected in zip(files,descriptor['frames']):
                            actual = Path(frame['to'])
                            if (actual.parent!=target.parent or actual.name!=expected['location']
                                    or not actual.is_relative_to(output) or actual.is_symlink() or sha(actual)!=expected['sha256']):
                                raise ValueError('collected_sequence_mismatch')
                        target = target.parent/'sequence.json'
                        shutil.copyfile(asset['sequenceStaging'],target)
                        load_module('sequence_assets').validate_sequence(target,asset['sha256'])
                        del asset['sequenceStaging']
                    if not target.is_relative_to(output) or sha(target) != asset['sha256']:
                        raise ValueError('collected_asset_mismatch')
                    asset['path'] = str(target.relative_to(output))
                    del asset['staging']
                reopened = json.loads(run(cli, ['--project', str(output / 'project.fcproj'), 'inspect']))
                captions = json.loads(run(cli, ['--project', str(output / 'project.fcproj'), 'exec', 'captions.list']))
                # 选择状态属于会话，不是原生工程持久化内容。
                if {k: v for k, v in reopened['sequence'].items() if k != 'selection'} != {k: v for k, v in sequence.items() if k != 'selection'}:
                    raise ValueError('sequence_roundtrip_mismatch')
                for index, time in enumerate(plan.get('frames', ['0'])):
                    run(cli, ['--project', str(output / 'project.fcproj'), 'render', '--seconds', str(ticks(time) / TICKS), '--out', str(output / f'frame-{index:04d}.png')])
                run(cli, ['--project', str(output / 'project.fcproj'), 'export', str(output / 'film.mp4'), '--format', 'h264', '--settings', json.dumps(export_settings(plan, captions))])
                exported = json.loads(run(cli, ['probe', str(output / 'film.mp4')]))
                if not exported.get('video') or any(exported['video'][key] != sequence['settings'][key] for key in ('width', 'height')) or exported['video']['frame_rate'] != sequence['settings']['frame_rate']:
                    raise ValueError('export_video_mismatch')
                if abs(exported['duration'] - sequence['duration']) > TICKS * sequence['settings']['frame_rate']['den'] // sequence['settings']['frame_rate']['num']:
                    raise ValueError('export_duration_mismatch')
                # 导出器可能自动产生静音 AAC；源时间线必须真实引用有音频流的素材。
                audio_items = {clip['item'] for track in reopened['sequence']['audio'] for clip in track['items']}
                audio_sources = [alias for alias, asset in assets.items() if asset.get('item') in audio_items and asset['probe'].get('audio')]
                audio_check = {'schema': 'filmcraft-audio-check/v1', 'required': plan.get('export', {}).get('audioRequired', True), 'sourceAliases': audio_sources, 'exportedAudio': exported.get('audio')}
                (output / 'audio-check.json').write_text(json.dumps(audio_check, ensure_ascii=False, indent=2) + '\n')
                (output / 'export-probe.json').write_text(json.dumps(precise(exported), ensure_ascii=False, indent=2) + '\n')
                if audio_check['required'] and (not exported.get('audio') or not audio_sources):
                    raise ValueError('export_audio_missing')
                decoded = run(cli, ['bench-decode', str(output / 'film.mp4'), '--frames', str(sequence['durationFrames'])])
                if not re.search(r'\b' + str(sequence['durationFrames']) + r' frames in ', decoded):
                    raise ValueError('export_decode_incomplete')
                if captions['tracks']:
                    run(cli, ['--project', str(output / 'project.fcproj'), 'exec', 'captions.export', json.dumps({'path': str(output / 'captions.srt'), 'format': 'srt'})])
                if source_project and sha(source_project) != source_hash:
                    raise ValueError('revision_conflict')
                for name, value in [('plan.json', plan), ('native.json', precise(reopened)), ('captions.json', precise(captions)), ('export-probe.json', precise(exported)), ('operations.json', precise(receipts))]:
                    (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
                (output / 'decode.txt').write_text(decoded)
                exchange_report(output,[f'frame-{index:04d}.png' for index,_ in enumerate(plan.get('frames',['0']))]+['film.mp4']+(['captions.srt'] if captions['tracks'] else []),{})
                manifest = {'schema': 'filmcraft-delivery/v1', 'sourceProjectSha256': source_hash, 'runtimeSha256': installed['binarySha256'], 'bindings': bindings, 'assets': assets, 'files': {str(p.relative_to(output)): sha(p) for p in output.rglob('*') if p.is_file()}, 'lossReport': {'path':'exchange-loss.json','sha256':sha(output/'exchange-loss.json')}, 'acceptance': 'requires-domain-and-visual-review', 'relocation': 'Use workflow --source; hashes checked before native media.relink.'}
                (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
                return manifest
            except BaseException as error:
                (output / 'failure.json').write_text(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False) + '\n')
                raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--runtime-home', type=Path)
    parser.add_argument('--asset', action='append', default=[], help='name=/absolute/path; calculates input digest')
    parser.add_argument('--lut-asset', action='append', default=[], help='name=/absolute/path/grade.cube; registers hashed LUT dependency')
    parser.add_argument('--sequence-asset', action='append', default=[], help='name=/absolute/path/sequence.json; registers complete image sequence')
    parser.add_argument('--segmented-sequence-asset', action='append', default=[], help='name=/absolute/path/segments.json; registers verified segmented producer checkpoint')
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text())
        for assignment in args.asset:
            alias, path = assignment.split('=', 1)
            kind = plan.get('assets',{}).get(alias,{}).get('kind')
            plan.setdefault('assets', {})[alias] = dict({'path': path, 'sha256': sha(path)}, **({'kind':kind} if kind else {}))
        for assignment in args.lut_asset:
            alias, path = assignment.split('=', 1)
            plan.setdefault('assets', {})[alias] = {'kind':'lut','path':path,'sha256':sha(path)}
        for assignment in args.sequence_asset:
            alias, path = assignment.split('=', 1)
            plan.setdefault('assets', {})[alias] = {'kind':'image-sequence','path':path,'sha256':sha(path)}
        for assignment in args.segmented_sequence_asset:
            alias, path = assignment.split('=', 1)
            plan.setdefault('assets', {})[alias] = {'kind':'segmented-image-sequence','path':path,'sha256':sha(path)}
        print(json.dumps(execute(plan, args.output, args.runtime_home, args.source), ensure_ascii=False))
    except (ValueError, KeyError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        raise SystemExit(1)

if __name__ == '__main__':
    main()
