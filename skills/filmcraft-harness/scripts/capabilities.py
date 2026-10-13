"""记录实际运行上下文和原生参数原文；未知能力不提升为可用。"""
import hashlib
import json
import re


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def validate_requirements(value):
    fields = {'mode', 'platform', 'runtimeVersion', 'runtimeSha256', 'desktopSha256',
              'parametersSha256', 'resources'}
    if not isinstance(value, dict) or set(value) - fields:
        raise ValueError('invalid_capability_requirements')
    for key, item in value.items():
        if key == 'resources':
            if (not isinstance(item, list) or len(item) > 100
                    or any(not isinstance(r, dict) or set(r) != {'kind', 'name'}
                           or r['kind'] not in ('codec', 'model', 'font')
                           or not isinstance(r['name'], str) or not r['name'].strip()
                           or len(r['name']) > 256 for r in item)):
                raise ValueError('invalid_capability_requirements: resources')
            if len({(r['kind'], r['name']) for r in item}) != len(item):
                raise ValueError('invalid_capability_requirements: duplicate_resource')
        elif not isinstance(item, str) or not item.strip():
            raise ValueError('invalid_capability_requirements: ' + key)
        elif key == 'mode' and item not in ('headless', 'bridge'):
            raise ValueError('invalid_capability_requirements: mode')
        elif key.endswith('Sha256') and not re.fullmatch('[a-f0-9]{64}', item):
            raise ValueError('invalid_capability_requirements: ' + key)
    return value


def compare_command(expected, observed):
    identifier = expected['id']
    known = isinstance(expected.get('params'), str)
    available = isinstance(observed, dict) and observed.get('id') == identifier
    documented = available and isinstance(observed.get('params'), str)
    status = ('missing' if not available else 'unknown' if not known or not documented
              else 'match' if expected['params'] == observed['params'] else 'drift')
    return {'id': identifier, 'discovery': 'PASS' if available else 'NOT_RUN',
            'parameterStatus': status,
            'expectedParametersSha256': digest(expected['params']) if known else None,
            'observedParametersSha256': digest(observed['params']) if documented else None,
            'enabled': observed.get('enabled') if available and type(observed.get('enabled')) is bool else None,
            'execution': 'NOT_RUN', 'negativeExecution': 'NOT_RUN',
            'reopen': 'NOT_RUN', 'nonTargetPreservation': 'NOT_RUN'}


def assert_command(row):
    codes = {'missing': 'capability_missing', 'unknown': 'capability_unknown',
             'drift': 'capability_contract_drift'}
    if row['parameterStatus'] != 'match':
        raise ValueError(codes[row['parameterStatus']] + ': ' + row['id'])


def snapshot(installed, expected, rows, mode, desktop=None, resources=None):
    if mode not in ('headless', 'bridge'):
        raise ValueError('invalid_capability_mode')
    current = {r['id']: r for r in rows}
    if len(current) != len(rows):
        raise ValueError('capability_registry_duplicate')
    docs = [{'id': row['id'], 'params': row.get('params')} for row in sorted(rows, key=lambda r: r['id'])]
    # 身份由自带安装器实际核验后返回；没有身份字段时保留 unknown。
    identity = {key: installed.get(key) for key in ('version', 'versionOutput', 'platform', 'binarySha256')}
    desktop_record = ({'status': 'verified', 'version': desktop['version'],
                       'binarySha256': desktop['binarySha256']}
                      if isinstance(desktop, dict) and isinstance(desktop.get('version'), str)
                      and desktop['version'].strip() and isinstance(desktop.get('binarySha256'), str)
                      and re.fullmatch('[a-f0-9]{64}', desktop['binarySha256'])
                      else {'status': 'unknown'})
    return {'schema': 'filmcraft-capability-snapshot/v1', 'pluginId': expected['pluginId'],
            'runtime': identity, 'mode': mode, 'desktop': desktop_record,
            'parametersSha256': digest(docs), 'catalogSha256': digest(rows),
            'parameterRepresentation': 'verbatim native documentation; not JSON Schema',
            'commands': [compare_command(row, current.get(row['id'])) for row in expected['commands']],
            'resources': resources or [], 'scope': 'discovery and prerequisites only; execution remains separately verified'}


def enforce(value, requires, identifiers):
    validate_requirements(requires)
    actual = {'mode': value['mode'], 'platform': value['runtime'].get('platform'),
              'runtimeVersion': value['runtime'].get('version'),
              'runtimeSha256': value['runtime'].get('binarySha256'),
              'desktopSha256': value['desktop'].get('binarySha256'),
              'parametersSha256': value['parametersSha256']}
    if value['mode'] == 'bridge' and value['desktop']['status'] != 'verified':
        raise ValueError('capability_unknown: desktop_identity')
    for key in set(requires) - {'resources'}:
        if actual[key] is None:
            raise ValueError('capability_unknown: ' + key)
        if actual[key] != requires[key]:
            raise ValueError('capability_identity_mismatch: ' + key)
    commands = {row['id']: row for row in value['commands']}
    for identifier in identifiers:
        if identifier not in commands:
            raise ValueError('capability_missing: ' + identifier)
        assert_command(commands[identifier])
    resources = {(r['kind'], r['name']): r for r in value['resources']}
    for required in requires.get('resources', []):
        row = resources.get((required['kind'], required['name']))
        status = row.get('status') if row else 'unknown'
        if status != 'available':
            code = 'capability_missing' if status == 'missing' else 'capability_unknown'
            raise ValueError(code + ': ' + required['kind'] + ':' + required['name'])


def probe_resources(requirements, query):
    """仅调用已核实的三种原生只读发现接口，不下载模型或修改工程。"""
    validate_requirements({'resources': requirements})
    commands = {'codec': 'export.formats', 'font': 'fonts.list', 'model': 'transcript.models'}
    replies, results = {}, []
    for requirement in requirements:
        identifier = commands[requirement['kind']]
        if identifier not in replies:
            try:
                replies[identifier] = query(identifier)
            except (ValueError, RuntimeError, OSError, TimeoutError):
                replies[identifier] = None
        reply, status = replies[identifier], 'unknown'
        kind, name = requirement['kind'], requirement['name']
        if kind == 'codec' and isinstance(reply, list) and all(
                isinstance(row, dict) and isinstance(row.get('id'), str)
                and type(row.get('available')) is bool for row in reply) and len({row['id'] for row in reply}) == len(reply):
            rows = [row for row in reply if row['id'] == name]
            status = 'available' if len(rows) == 1 and rows[0]['available'] else 'missing'
        elif kind == 'font' and isinstance(reply, list) and all(
                isinstance(row, dict) and isinstance(row.get('family'), str)
                and isinstance(row.get('styles'), list)
                and all(isinstance(style, str) and style.strip() for style in row['styles'])
                for row in reply) and len({row['family'] for row in reply}) == len(reply):
            status = 'available' if any(row['family'] == name for row in reply) else 'missing'
        elif kind == 'model' and isinstance(reply, dict) and type(reply.get('available')) is bool:
            rows = reply.get('models')
            if isinstance(rows, list) and all(isinstance(row, dict) and isinstance(row.get('id'), str)
                                            and type(row.get('installed')) is bool for row in rows) and len({row['id'] for row in rows}) == len(rows):
                found = [row for row in rows if row['id'] == name]
                status = 'available' if reply['available'] and len(found) == 1 and found[0]['installed'] else 'missing'
        results.append({**requirement, 'status': status, 'probeCommand': identifier,
                        'probeSha256': digest(reply),
                        'scope': 'native discovery only; font appearance, model inference and codec output not qualified'})
    return results


def infer_resources(identifier, params):
    """解析已获得实际值的原生参数；不猜测尚未解析的引用或隐式预设。"""
    if identifier == 'transcript.generate':
        name = params.get('model', 'whisper-base')
        return [{'kind': 'model', 'name': name}] if isinstance(name, str) else []
    if identifier == 'captions.setStyle' and isinstance(params.get('font'), str):
        return [{'kind': 'font', 'name': params['font']}]
    if identifier == 'file.exportMedia':
        settings = params.get('settings') if isinstance(params.get('settings'), dict) else {}
        name = params.get('format', settings.get('format'))
        return [{'kind': 'codec', 'name': name}] if isinstance(name, str) else []
    return []
