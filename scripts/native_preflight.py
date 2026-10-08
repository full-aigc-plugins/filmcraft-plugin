#!/usr/bin/env python3
"""复用独立技能源做只读能力预检；不创建工程、不调用编辑指令。"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


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
        load('capabilities').enforce(snapshot, requirements, requested)
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
        print(json.dumps({'schema': 'filmcraft-native-preflight-error/v1', 'error': {'code': code}}))
        sys.exit(1)
