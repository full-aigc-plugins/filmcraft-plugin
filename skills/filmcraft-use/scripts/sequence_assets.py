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
    stride, previous, offset = facts['width']*4, bytearray(facts['width']*4), 0
    pixels = hashlib.sha256(); minimum, maximum = 255, 0
    for _ in range(facts['height']):
        filtering = scan[offset]; row = bytearray(scan[offset+1:offset+1+stride]); offset += stride+1
        for x in range(stride):
            left = row[x-4] if x >= 4 else 0; above = previous[x]; corner = previous[x-4] if x >= 4 else 0
            predictor = left+above-corner
            distances = [abs(predictor-left), abs(predictor-above), abs(predictor-corner)]
            paeth = (left, above, corner)[distances.index(min(distances))]
            value = (0, left, above, (left+above)//2, paeth)[filtering]
            row[x] = (row[x]+value) & 255
        minimum = min(minimum, min(row[3::4])); maximum = max(maximum, max(row[3::4]))
        pixels.update(row); previous = row
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
    if not isinstance(manifest, dict) or set(manifest) != fields:
        raise ValueError('sequence_manifest_invalid')
    for key, value in {'schema':'craft-image-sequence/v1','encoding':'png','bitDepth':8,'channels':'rgba',
                       'alphaRepresentation':'straight-png','colorSpace':'unknown'}.items():
        if type(manifest[key]) is not type(value) or manifest[key] != value:
            raise ValueError('sequence_manifest_invalid')
    width, height, count = (manifest[k] for k in ('width','height','frameCount'))
    if any(type(v) is not int or v <= 0 for v in (width,height,count)) or max(width,height)>16384:
        raise ValueError('sequence_dimensions_invalid')
    if count>10000 or count*width*height*4>512*1024*1024:
        raise ValueError('sequence_frame_budget_exceeded')
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
    if sum(frame['bytes'] for frame in records)>512*1024*1024:
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
