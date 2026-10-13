"""验证登记的 RGBA 动画序列；不执行渲染或修改源素材。"""
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import struct
import zlib


def rgba_facts(path):
    spec = importlib.util.spec_from_file_location('craft_sequence_png', Path(__file__).with_name('png_inspection.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    facts = module.inspect_png(path)
    data = path.read_bytes()
    if data[24:29] != bytes([8, 6, 0, 0, 0]):
        raise ValueError('sequence_rgba8_required')
    compressed, at = [], 8
    while at < len(data):
        size = struct.unpack_from('>I', data, at)[0]
        if data[at+4:at+8] == b'IDAT':
            compressed.append(data[at+8:at+8+size])
        at += size+12
    # inspect_png 已约束解压尺寸及文件结构；这里还原滤波后像素以核验实际 alpha。
    decoder = zlib.decompressobj()
    scan = decoder.decompress(b''.join(compressed), (facts['width']*4+1)*facts['height']+1)
    pixels = hashlib.sha256(); minimum, maximum = 255, 0
    for row in module.rgba8_rows(scan, facts['width'], facts['height']):
        alpha=row[3::4]
        minimum=min(minimum,min(alpha));maximum=max(maximum,max(alpha))
        pixels.update(row)
    return dict(facts, alphaExtrema=[minimum, maximum], rgbaSha256=pixels.hexdigest())



def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('sequence_duplicate_field')
        result[key] = value
    return result


def validate_sequence(path, expected_digest):
    path = Path(path)
    if (path.name != 'sequence.json' or path.is_symlink() or path.parent.is_symlink()
            or not path.is_file() or path.stat().st_size > 4*1024*1024
            or not isinstance(expected_digest, str) or not re.fullmatch(r'[a-f0-9]{64}', expected_digest)
            or digest(path) != expected_digest):
        raise ValueError('sequence_manifest_digest_mismatch')
    manifest = json.loads(path.read_text(), object_pairs_hook=unique_fields)
    fields = {'schema','encoding','width','height','bitDepth','channels','alphaRepresentation','colorSpace',
              'frameRate','frameCount','durationTicks','timeBase','frames'}
    segmented = isinstance(manifest, dict) and manifest.get('schema') == 'filmcraft-collected-sequence/v1'
    if segmented:
        fields |= {'segments', 'sourceSequenceSha256'}
    if not isinstance(manifest, dict) or set(manifest) != fields:
        raise ValueError('sequence_manifest_invalid')
    for key, value in {'schema':'filmcraft-collected-sequence/v1' if segmented else 'craft-image-sequence/v1','encoding':'png','bitDepth':8,'channels':'rgba',
                       'alphaRepresentation':'straight-png','colorSpace':'unknown'}.items():
        if type(manifest[key]) is not type(value) or manifest[key] != value:
            raise ValueError('sequence_manifest_invalid')
    width, height, count = (manifest[k] for k in ('width','height','frameCount'))
    if any(type(v) is not int or v <= 0 for v in (width,height,count)) or max(width,height)>16384:
        raise ValueError('sequence_dimensions_invalid')
    if count>10000 or count*width*height*4>(64*1024**3 if segmented else 512*1024*1024):
        raise ValueError('sequence_frame_budget_exceeded')
    if segmented:
        validate_collected_segments(manifest)
    rate = manifest['frameRate']
    if (not isinstance(rate, dict) or set(rate) != {'num','den'}
            or any(type(v) is not int or not 0<v<=2**31-1 for v in rate.values())):
        raise ValueError('sequence_rate_invalid')
    rational = Fraction(rate['num'],rate['den'])
    if not 1<=rational<=240 or (rational.numerator,rational.denominator)!=(rate['num'],rate['den']):
        raise ValueError('sequence_rate_invalid')
    timebase = manifest['timeBase']
    if (not isinstance(timebase,dict) or set(timebase)!={'num','den'} or any(type(v) is not int for v in timebase.values())
            or manifest['durationTicks'] != str(count) or timebase != {'num':rate['den'],'den':rate['num']}):
        raise ValueError('sequence_timing_mismatch')
    records = manifest['frames']
    if not isinstance(records,list) or len(records)!=count:
        raise ValueError('sequence_frame_set_mismatch')
    expected = [f'frame_{index:05d}.png' for index in range(count)]
    if sorted(p.name for p in path.parent.iterdir()) != sorted(expected+['sequence.json']):
        raise ValueError('sequence_frame_set_mismatch')
    if any(not isinstance(frame,dict) or type(frame.get('bytes')) is not int or not 0<frame['bytes']<=64*1024*1024 for frame in records):
        raise ValueError('sequence_frame_metadata_mismatch')
    if sum(frame['bytes'] for frame in records)>(2*1024**3 if segmented else 512*1024*1024):
        raise ValueError('sequence_frame_budget_exceeded')
    if segmented and any(sum(f['bytes'] for f in records[s['firstFrame']:s['firstFrame']+s['frameCount']])>512*1024*1024 for s in manifest['segments']):
        raise ValueError('sequence_frame_budget_exceeded')
    for index, (name, record) in enumerate(zip(expected,records)):
        frame = path.parent/name
        if frame.is_symlink() or not frame.is_file():
            raise ValueError('sequence_frame_invalid')
        extrema = record.get('alphaExtrema')
        if not isinstance(extrema,list) or len(extrema)!=2 or any(type(v) is not int or not 0<=v<=255 for v in extrema):
            raise ValueError('sequence_frame_metadata_mismatch')
        if frame.stat().st_size!=record['bytes'] or digest(frame)!=record.get('sha256'):
            raise ValueError('sequence_frame_digest_mismatch')
        facts = rgba_facts(frame)
        actual = {'index':index,'location':name,'sha256':digest(frame),'bytes':frame.stat().st_size,
                  'alphaExtrema':facts['alphaExtrema'],'rgbaSha256':facts['rgbaSha256']}
        if (facts['width'],facts['height'])!=(width,height) or record!=actual or type(record.get('index')) is not int:
            raise ValueError('sequence_frame_metadata_mismatch')
    if digest(path)!=expected_digest:
        raise ValueError('sequence_manifest_changed')
    return manifest


def validate_collected_segments(manifest):
    """领域收集清单按原段范围保留资源边界及不可变来源摘要。"""
    if not isinstance(manifest.get('sourceSequenceSha256'), str) or not re.fullmatch(r'[a-f0-9]{64}', manifest['sourceSequenceSha256']):
        raise ValueError('sequence_segment_source_invalid')
    segments = manifest.get('segments')
    if not isinstance(segments, list) or not 1 <= len(segments) <= 10000:
        raise ValueError('sequence_segment_ranges_invalid')
    first = 0
    for part in segments:
        if (not isinstance(part, dict) or set(part) != {'firstFrame','frameCount','sourceSha256'}
                or type(part['firstFrame']) is not int or part['firstFrame'] != first
                or type(part['frameCount']) is not int or part['frameCount'] <= 0
                or part['frameCount']*manifest['width']*manifest['height']*4 > 512*1024*1024
                or not isinstance(part['sourceSha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', part['sourceSha256'])):
            raise ValueError('sequence_segment_ranges_invalid')
        first += part['frameCount']
    if first != manifest['frameCount']:
        raise ValueError('sequence_segment_ranges_invalid')


def _validate_segmented_source(path, expected_digest):
    """只消费 verified 生产检查点；逐段实际校验，绝不执行其中的参数。"""
    path = Path(path)
    if path.name != 'segments.json' or any(p.is_symlink() for p in [path,*path.parents]) or not path.is_file() or path.stat().st_size > 4*1024*1024 or digest(path) != expected_digest:
        raise ValueError('sequence_segment_digest_mismatch')
    value = json.loads(path.read_text(), object_pairs_hook=unique_fields)
    if not isinstance(value, dict) or set(value) != {'schema','state','binding','frameCount','frameRate','segments'} or value['schema'] != 'craft-segmented-render-checkpoint/v1' or value['state'] != 'verified':
        raise ValueError('sequence_segment_checkpoint_invalid')
    binding = value['binding']
    if not isinstance(binding, dict) or set(binding) != {'projectSha256','runtimeSha256','composition','chunkBytes','parts'}:
        raise ValueError('sequence_segment_binding_invalid')
    if any(not isinstance(binding[k],str) or not re.fullmatch(r'[a-f0-9]{64}',binding[k]) for k in ['projectSha256','runtimeSha256']):
        raise ValueError('sequence_segment_binding_invalid')
    comp = binding['composition']
    if not isinstance(comp, dict) or any(type(comp.get(k)) is not int or not 1 <= comp[k] <= 16384 for k in ['width','height']):
        raise ValueError('sequence_segment_dimensions_invalid')
    rate = Fraction(str(comp['frameRate']))
    if (not isinstance(value['frameRate'], dict) or set(value['frameRate']) != {'num','den'}
            or any(type(v) is not int for v in value['frameRate'].values())
            or value['frameRate'] != {'num':rate.numerator,'den':rate.denominator} or not 1 <= rate <= 240):
        raise ValueError('sequence_segment_timing_invalid')
    if type(binding['chunkBytes']) is not int or not 0 < binding['chunkBytes'] <= 512*1024*1024:
        raise ValueError('sequence_segment_budget_invalid')
    count = value['frameCount']
    if type(count) is not int or not 0 < count <= 10000 or count*comp['width']*comp['height']*4 > 64*1024**3:
        raise ValueError('sequence_segment_budget_invalid')
    duration = Fraction(str(comp['duration']))
    if duration <= 0 or -(-(duration*rate).numerator//(duration*rate).denominator) != count:
        raise ValueError('sequence_segment_timing_invalid')
    parts = value['segments']
    if not isinstance(parts, list) or not 1 <= len(parts) <= 10000 or not isinstance(binding['parts'], list) or len(binding['parts']) != len(parts):
        raise ValueError('sequence_segment_ranges_invalid')
    result, first, total = [], 0, 0
    for index, part in enumerate(parts):
        if not isinstance(part, dict) or set(part) != {'firstFrame','frameCount','start','end','location','sha256'}:
            raise ValueError('sequence_segment_ranges_invalid')
        size = part['frameCount']
        if type(part['firstFrame']) is not int or part['firstFrame'] != first or type(size) is not int or size <= 0 or first+size > count or size*comp['width']*comp['height']*4 > binding['chunkBytes']:
            raise ValueError('sequence_segment_ranges_invalid')
        for key, frame in [('start',first),('end',first+size)]:
            time = Fraction(frame,1)/rate
            if part[key] != {'num':time.numerator,'den':time.denominator} or any(type(x) is not int for x in part[key].values()):
                raise ValueError('sequence_segment_timing_invalid')
        if binding['parts'][index] != {k:part[k] for k in ['firstFrame','frameCount','start','end']} or part['location'] != f'segment_{index:05d}/sequence.json':
            raise ValueError('sequence_segment_ranges_invalid')
        child = path.parent/part['location']
        manifest = validate_sequence(child, part['sha256'])
        if manifest['schema'] != 'craft-image-sequence/v1' or (manifest['width'],manifest['height'],manifest['frameCount'],manifest['frameRate']) != (comp['width'],comp['height'],size,value['frameRate']):
            raise ValueError('sequence_segment_child_mismatch')
        if any(f['alphaExtrema'][0] == 255 for f in manifest['frames']):
            raise ValueError('sequence_segment_transparency_missing')
        total += sum(f['bytes'] for f in manifest['frames'])
        if total > 2*1024**3:
            raise ValueError('sequence_segment_budget_invalid')
        result.append((part, manifest))
        first += size
    if first != count or digest(path) != expected_digest:
        raise ValueError('sequence_segment_ranges_invalid')
    return value, result


def validate_segmented_source(path, expected_digest):
    """畸形绑定统一为领域拒绝，避免把缺字段报告成成功或未分类异常。"""
    try:
        return _validate_segmented_source(path, expected_digest)
    except (KeyError, TypeError, AttributeError, ZeroDivisionError) as error:
        raise ValueError('sequence_segment_checkpoint_invalid') from error


def copy_segmented_sequence(path, expected_digest, destination):
    """在暂存目录按全局索引收集，转换摘要显式保留在领域清单中。"""
    path, destination = Path(path), Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError('sequence_output_exists')
    source, segments = validate_segmented_source(path, expected_digest)
    first = segments[0][1]
    manifest = {k:v for k,v in first.items() if k not in {'frames','schema','frameCount','durationTicks'}}
    manifest.update(schema='filmcraft-collected-sequence/v1', frameCount=source['frameCount'], durationTicks=str(source['frameCount']),
                    sourceSequenceSha256=expected_digest, segments=[], frames=[])
    destination.mkdir()
    try:
        for part, child in segments:
            manifest['segments'].append({'firstFrame':part['firstFrame'],'frameCount':part['frameCount'],'sourceSha256':part['sha256']})
            for frame in child['frames']:
                index = part['firstFrame']+frame['index']
                name = f'frame_{index:05d}.png'
                shutil.copyfile((path.parent/part['location']).parent/frame['location'], destination/name)
                manifest['frames'].append(dict(frame, index=index, location=name))
        target = destination/'sequence.json'
        target.write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
        validate_sequence(target, digest(target))
        if digest(path) != expected_digest:
            raise ValueError('sequence_segment_digest_mismatch')
        return target
    except BaseException:
        shutil.rmtree(destination)
        raise


def copy_sequence(path, expected_digest, destination):
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError('sequence_output_exists')
    manifest = validate_sequence(path, expected_digest)
    source = Path(path).parent
    destination.mkdir()
    try:
        for record in manifest['frames']:
            shutil.copyfile(source/record['location'],destination/record['location'])
        shutil.copyfile(path,destination/'sequence.json')
        validate_sequence(destination/'sequence.json',expected_digest)
    except BaseException:
        shutil.rmtree(destination)
        raise
    return destination/'sequence.json'
