#!/usr/bin/env python3
"""复用独立技能源做只读能力预检；不创建工程、不调用编辑指令。"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path


def refusal_diagnostic(error, snapshot, requires):
    """仅投影安全身份、状态和摘要；拒绝文本及完整参数文档不属于公共诊断。"""
    def token(value):
        return value if isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_.:@+\-]{1,128}', value) else None
    def digest(value):
        return value if isinstance(value, str) and re.fullmatch(r'[a-f0-9]{64}', value) else None
    code, _, raw = str(error).partition(': ')
    subject = token(raw) or 'redacted'
    runtime = snapshot.get('runtime', {})
    desktop = snapshot.get('desktop', {})
    actual = {'mode': snapshot.get('mode'), 'platform': runtime.get('platform'),
              'runtimeVersion': runtime.get('version'), 'runtimeSha256': runtime.get('binarySha256'),
              'desktopSha256': desktop.get('binarySha256'), 'parametersSha256': snapshot.get('parametersSha256')}
    expected, observed = None, None
    if subject in actual:
        expected, observed = token(requires.get(subject)), token(actual[subject])
    elif subject.startswith(('codec:', 'font:', 'model:')):
        kind, name = subject.split(':', 1)
        rows = snapshot.get('resources', [])
        row = next((r for r in rows if r.get('kind') == kind and r.get('name') == name), {})
        expected, observed = 'available', token(row.get('status')) or 'unknown'
    else:
        row = next((r for r in snapshot.get('commands', []) if r.get('id') == subject), {})
        expected = digest(row.get('expectedParametersSha256'))
        observed = digest(row.get('observedParametersSha256'))
    return {'schema': 'filmcraft-capability-refusal/v1', 'subject': subject,
            'status': {'capability_missing': 'missing', 'capability_unknown': 'unknown',
                       'capability_contract_drift': 'drift', 'capability_identity_mismatch': 'mismatch'}[code],
            'expected': expected, 'observed': observed,
            'snapshot': {'mode': actual['mode'] if actual['mode'] in ('headless', 'bridge') else None,
                         'platform': token(actual['platform']), 'runtimeVersion': token(actual['runtimeVersion']),
                         'runtimeSha256': digest(actual['runtimeSha256']),
                         'parametersSha256': digest(actual['parametersSha256']),
                         'catalogSha256': digest(snapshot.get('catalogSha256'))}}


def valid_asset_issues(value):
    """仅允许安全别名与封闭的来源/原因；不将路径或任意异常文本传给宿主。"""
    if not isinstance(value, list) or not value:
        return None
    for row in value:
        if (not isinstance(row, dict) or set(row) != {'alias', 'origin', 'reason'}
                or not isinstance(row['alias'], str)
                or not re.fullmatch(r'[a-zA-Z][\w-]*', row['alias'])
                or row['origin'] not in ('plan', 'source')
                or row['reason'] not in ('missing_file', 'digest_mismatch', 'invalid_path')):
            return None
    return [dict(row) for row in value]


def valid_clip_timing(value):
    """片段身份保留完整 u64 十进制字符串，拒绝路径、扩展字段及未知原因。"""
    if (not isinstance(value, dict) or set(value) != {'reason', 'clipIds'}
            or not isinstance(value['reason'], str)
            or value['reason'] not in {'ticks_require_decimal_string', 'ticks_out_of_range',
                                       'ticks_not_exact', 'clip_out_of_range', 'invalid_clip_speed'}
            or not isinstance(value['clipIds'], list) or not value['clipIds']
            or not all(isinstance(v, str) and re.fullmatch(r'[1-9][0-9]{0,19}', v)
                       and int(v) <= 2**64-1 for v in value['clipIds'])):
        return None
    return {'reason': value['reason'], 'clipIds': list(value['clipIds'])}


def inspect(skill, plan_path, output, runtime_home, source=None):
    def load(name):
        path = skill / 'scripts' / (name + '.py')
        spec = importlib.util.spec_from_file_location('filmcraft_preflight_' + name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    commands = load('commands')
    plan = commands.reply_json(plan_path.read_text())
    workflow = load('workflow')
    prior = commands.reply_json((source / 'manifest.json').read_text()) if source else {}
    project_revision = hashlib.sha256((source / 'project.fcproj').read_bytes()).hexdigest() if source else None
    workflow.validate(plan, prior.get('assets', {}))
    workflow.preflight_assets(plan.get('assets', {}), prior.get('assets', {}), source)
    installed = load('bootstrap').install(json.loads((skill / 'scripts/runtime.lock.json').read_text()), runtime_home)
    requirements = dict(plan.get('requires', {}))
    resources = list(requirements.get('resources', []))
    if {'kind': 'codec', 'name': 'h264'} not in resources:
        resources.append({'kind': 'codec', 'name': 'h264'})
    requirements['resources'] = resources
    argv = [installed['executable']] + (['--project', str(source / 'project.fcproj')] if source else []) + ['mcp']
    with load('mcp_session').Session(argv) as session:
        rows = commands.runtime_rows(session)
        snapshot = commands.capability_snapshot(session, installed, rows, requires=requirements)
        requested = [item['params']['command'] for item in plan['operations'] if item['command'] == 'native.command']
        try:
            load('capabilities').enforce(snapshot, requirements, requested)
        except (ValueError, RuntimeError) as error:
            if str(error).split(':', 1)[0] in {'capability_missing', 'capability_unknown', 'capability_contract_drift', 'capability_identity_mismatch'}:
                error.capability_diagnostic = refusal_diagnostic(error, snapshot, requirements)
            raise
    inputs = {name: asset['sha256'] for name, asset in {**prior.get('assets', {}), **plan.get('assets', {})}.items()}
    if source and hashlib.sha256((source / 'project.fcproj').read_bytes()).hexdigest() != project_revision:
        raise ValueError('revision_conflict')
    return {'schema': 'filmcraft-native-preflight/v1', 'capabilitySnapshot': snapshot,
            'inputHashes': inputs, 'projectRevision': project_revision}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-dir', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--runtime-home', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.skill_dir, args.plan, args.output, args.runtime_home, args.source), ensure_ascii=False))
    except Exception as error:
        # 仅传播明确的能力拒绝码；不把本地路径、堆栈或任意原生文本当成公共错误合同。
        code = str(error).split(':', 1)[0]
        if code not in {'capability_missing', 'capability_unknown', 'capability_contract_drift', 'capability_identity_mismatch'}:
            code = 'native_preflight_failed'
        failure = {'code': code}
        if code != 'native_preflight_failed':
            failure['diagnostic'] = getattr(error, 'capability_diagnostic', None) or refusal_diagnostic(error, {}, {})
        issues = valid_asset_issues(getattr(error, 'asset_issues', None))
        if issues:
            failure = {'code': 'asset_preflight_failed', 'assetIssues': issues}
        clip_timing = valid_clip_timing(getattr(error, 'clip_timing', None))
        if clip_timing:
            failure = {'code': 'clip_timing_failed', 'clipTiming': clip_timing}
        print(json.dumps({'schema': 'filmcraft-native-preflight-error/v1', 'error': failure}))
        sys.exit(1)
