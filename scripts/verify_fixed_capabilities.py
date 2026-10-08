#!/usr/bin/env python3
"""固定安装能力验收：真实会话与受控故障分开，未验平台和完整升级保持开放。"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(value, reason):
    if not value:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


def verify(host, authority, ref, output):
    fixed = load(ROOT / 'scripts/verify_fixed_install.py', 'fixed_capability_install')
    expected = fixed.release_entry(ROOT, ref)
    host_receipt = json.loads((host / 'host-receipt.json').read_text())
    require(host_receipt['result'] == 'PASS' and host_receipt['plugin'] == expected, 'fixed_host_mismatch')
    directories = json.loads((host / 'installed-directories.private.json').read_text())
    require(set(directories) == set(expected['skills']), 'installed_inventory_mismatch')
    helper, helper_identity = fixed.owner_helper(authority)
    require(host_receipt['helper'] == helper_identity, 'fixed_helper_mismatch')
    skill = Path(directories['filmcraft-use']).resolve()
    require(skill.is_relative_to((host / 'host-config').resolve()), 'installed_path_outside_host')
    for name, directory in directories.items():
        require(Path(directory).resolve() == skill.parent / name, 'installed_skill_path_mismatch')
        helper.verify_installed_skill(directory, expected)
    fixed.verify_code_files(skill.parent.parent, expected['codeFilesSha256'])
    require(not output.exists() and not output.is_symlink(), 'capability_output_exists')
    output.mkdir(mode=0o700)
    root = output / 'work'; root.mkdir(mode=0o700)
    commands = load(skill / 'scripts/commands.py', 'fixed_capability_commands')
    capabilities = commands.load('capabilities')
    desktop_module = commands.load('desktop')
    owned = commands.load('desktop_session')
    native_session = commands.load('mcp_session').Session
    catalog = commands.catalog()
    marker = root / 'non-target'; marker.write_bytes(b'preserve unrelated input')
    marker_hash = sha(marker)
    cases, traces, catalogs = [], {}, {}
    old_data = os.environ.get('FILMCRAFT_DATA_DIR')
    os.environ['FILMCRAFT_DATA_DIR'] = str(root / 'isolated-headless-data')

    def safe(value):
        text = json.dumps(value, ensure_ascii=False, allow_nan=False)
        return json.loads(text.replace(str(output.resolve()), '[TEST_ROOT]')
                              .replace(str(output), '[TEST_ROOT]').replace(str(Path.home()), '[USER_HOME]'))

    def save(name, value):
        (output / name).write_text(json.dumps(safe(value), ensure_ascii=False, indent=2) + '\n')

    def project_receipt(receipt, operations):
        # 保留原回执摘要；公开投影只列本计划和漂移命令，完整目录另存，不冒称原字节回执。
        result = copy.deepcopy(receipt)
        result['rawReceiptSha256'] = digest(receipt)
        snapshot = result.get('capabilitySnapshot')
        if snapshot:
            identifiers = {row['command'] for row in operations}
            result['fullSnapshotSha256'] = digest(snapshot)
            snapshot['commands'] = [row for row in snapshot['commands'] if row['id'] in identifiers
                                    or row['parameterStatus'] != 'match']
            result['projection'] = 'Only plan commands and contract differences; full native catalog in catalogs.json'
        return result

    try:
        # 公共子进程入口：畸形 requires 必须在安装、目录创建及桌面启动前拒绝。
        invalid = [None, [], {'mode': 'auto'}, {'runtimeSha256': 'x'},
                   {'resources': [{'kind': 'font', 'name': 'Arial', 'status': 'available'}]},
                   {'resources': [{'kind': 'invented', 'name': 'x'}]},
                   {'resources': [{'kind': 'font', 'name': 'Arial'}] * 2}]
        preflight = []
        for name, directory in sorted(directories.items()):
            for entry in ('commands', 'workflow', 'desktop'):
                for index, requires in enumerate(invalid):
                    plan = {'schema': 'craft-command-plan/v1', 'requires': requires, 'operations': [
                        {'command': 'file.newProject', 'params': {}}]}
                    if entry == 'workflow':
                        plan = {'document': {'name': 'Invalid', 'width': 32, 'height': 32,
                                            'frameRate': {'num': 12, 'den': 1}},
                                'requires': requires, 'operations': []}
                    plan_path = root / 'invalid.json'; plan_path.write_text(json.dumps(plan))
                    before = {p.relative_to(root).as_posix() for p in root.rglob('*')}
                    plan_hash = sha(plan_path)
                    destination, runtime = root / 'forbidden-output', root / 'forbidden-runtime'
                    argv = [sys.executable, '-I', '-B', str(Path(directory) / 'scripts' / (entry + '.py'))]
                    if entry != 'workflow': argv.append('run')
                    argv += [str(plan_path), '--output', str(destination), '--runtime-home', str(runtime)]
                    result = subprocess.run(argv, text=True, capture_output=True, timeout=20)
                    # desktop.py 的既有拒绝接口是 stderr + exit 1；不改写成命令入口的 JSON 协议。
                    reply = {'error': result.stderr.strip()} if entry == 'desktop' else json.loads(result.stdout)
                    require(result.returncode == 1 and 'invalid_capability_requirements' in reply.get('error', ''),
                            'invalid_requires_not_rejected: ' + entry)
                    require(not destination.exists() and not runtime.exists() and sha(plan_path) == plan_hash
                            and {p.relative_to(root).as_posix() for p in root.rglob('*')} == before,
                            'invalid_requires_side_effect')
                    preflight.append({'skill': name, 'entry': entry, 'case': index + 1,
                                      'planSha256': plan_hash, 'error': reply['error'],
                                      'outputCreated': False, 'runtimeCreated': False})
        save('preflight.json', preflight)
        print('fixed requires preflight:', len(preflight), flush=True)
        runtime_home = root / 'runtime'
        runtime = commands.load('bootstrap').install(json.loads((skill / 'scripts/runtime.lock.json').read_text()), runtime_home)
        require(runtime['binarySha256'] == catalog['runtimeSha256'], 'runtime_catalog_mismatch')
        desktop = desktop_module.install(json.loads((skill / 'scripts/desktop.lock.json').read_text()), runtime_home)
        binding = {'pluginSha': expected['sha'], 'sourceSha': expected['skillSourceSha'],
                   'runtimeSha256': runtime['binarySha256'], 'runtimeVersion': runtime['version'],
                   'desktopSha256': desktop['binarySha256'], 'desktopVersion': desktop['version'],
                   'platform': runtime['platform']}
        projects = {}

        def run_case(name, mode, plan, fault=None, desktop_identity='verified', inputs=None):
            destination = root / name
            events, sessions = [], []
            with socket.socket() as probe:
                probe.bind(('127.0.0.1', 0)); port = probe.getsockname()[1]

            class Trace:
                def __init__(self, argv):
                    self.inner = (owned.OwnedSession(argv, desktop, 'filmcraft', destination, port)
                                  if mode == 'bridge' else native_session(argv, timeout=900))
                    sessions.append(self)

                def __enter__(self):
                    self.inner.__enter__(); return self

                def __exit__(self, *args):
                    return self.inner.__exit__(*args)

                def request(self, method, params):
                    reply = self.inner.request(method, params)
                    event = {'method': method, 'params': copy.deepcopy(params), 'nativeReplySha256': digest(reply)}
                    altered = False
                    if params.get('name') == 'command_list':
                        rows = commands.parse_reply(reply)
                        if not params.get('arguments', {}).get('filter'):
                            catalogs.setdefault(mode, rows)
                        if (fault == 'late-contract' and params.get('arguments', {}).get('filter') == 'file.saveAs'):
                            rows = copy.deepcopy(rows)
                            for row in rows:
                                if row['id'] == 'file.saveAs': row['params'] = '{"newRequiredField":str}'
                            reply = {'content': [{'type': 'text', 'text': json.dumps(rows)}]}; altered = True
                        if params.get('arguments', {}).get('filter'): event['reply'] = copy.deepcopy(reply)
                    else:
                        event['reply'] = copy.deepcopy(reply)
                    if fault and fault.startswith('unknown-') and params.get('name') == 'command_run':
                        probe_id = {'codec': 'export.formats', 'font': 'fonts.list', 'model': 'transcript.models'}[fault[8:]]
                        if params.get('arguments', {}).get('id') == probe_id:
                            reply = {'content': [{'type': 'text', 'text': '{"unexpected":"controlled malformed probe"}'}]}
                            altered = True
                    if altered: event['deliveredFaultReply'] = copy.deepcopy(reply)
                    event['controlledFault'] = altered
                    events.append(event)
                    return reply

            receipt = commands.execute(plan, destination, runtime_home=runtime_home, mode=mode,
                connect='127.0.0.1:' + str(port) if mode == 'bridge' else None,
                session_factory=Trace, inputs=inputs,
                desktop_identity=desktop if desktop_identity == 'verified' else None)
            require(sha(marker) == marker_hash, 'non_target_changed')
            for path, original in projects.values(): require(sha(path) == original, 'original_project_changed')
            persisted = json.loads((destination / ('success.json' if receipt['result'] == 'PASS' else 'failure.json')).read_text())
            require(persisted == receipt, 'receipt_not_persisted')
            lifecycle = {'sessions': len(sessions), 'allNativeProcessesStopped': all(
                (s.inner.stopped if mode == 'bridge' else s.inner.process.poll() is not None) for s in sessions),
                'ownedListenerVerified': all(s.inner.listener_verified for s in sessions) if mode == 'bridge' else None}
            require(lifecycle['allNativeProcessesStopped'] and (mode != 'bridge' or lifecycle['ownedListenerVerified']),
                    'owned_process_lifecycle_failed')
            traces[name] = events
            row = {'case': name, 'mode': mode, 'binding': binding, 'plan': plan, 'planSha256': digest(plan),
                   'inputs': {k: sha(Path(v)) for k, v in (inputs or {}).items()},
                   'fault': fault, 'executionLayer': 'actual native plus controlled reply fault' if fault else 'actual native',
                   'receipt': project_receipt(receipt, plan['operations']), 'lifecycle': lifecycle,
                   'originalProjectsPreserved': True, 'nonTargetPreserved': True}
            cases.append(row)
            print(name, receipt['result'], receipt.get('error', ''), flush=True)
            return receipt, destination, events

        base = json.loads((skill / 'examples/desktop-first-use.json').read_text())
        for mode in ('headless', 'bridge'):
            created, directory, _ = run_case(mode + '-default', mode, base)
            require(created['result'] == 'PASS', 'default_plan_incompatible')
            project = directory / 'project.fcproj'
            require(project.is_file(), 'native_project_missing')
            projects[mode] = (project, sha(project))
            snapshot = created['capabilitySnapshot']
            correct = {'mode': mode, 'platform': runtime['platform'], 'runtimeVersion': runtime['version'],
                       'runtimeSha256': runtime['binarySha256'], 'parametersSha256': snapshot['parametersSha256']}
            if mode == 'bridge': correct['desktopSha256'] = desktop['binarySha256']
            reopen = {'schema': 'craft-command-plan/v1', 'requires': correct, 'operations': [
                {'command': 'file.open', 'params': {'path': {'$ref': 'original.path'}}},
                {'command': 'sequence.inspect', 'params': {}},
                {'command': 'file.saveAs', 'params': {'path': {'$output': 'roundtrip.fcproj'}}}]}
            opened, out, _ = run_case(mode + '-bound-reopen', mode, reopen, inputs={'original': project})
            require(opened['result'] == 'PASS', 'bound_reopen_failed')
            before = json.loads(project.read_text())['project']; after = json.loads((out / 'roundtrip.fcproj').read_text())['project']
            # Save As 的公开行为按文件名更新工程及根 bin 名称；其余工程字段逐项保全。
            require(before['name'] == before['root']['name'] == 'project'
                    and after['name'] == after['root']['name'] == 'roundtrip', 'save_as_name_mismatch')
            after['name'] = before['name']; after['root']['name'] = before['root']['name']
            require(before == after, 'native_reopen_project_changed')
            sequence = opened['steps'][1]['result']
            require((sequence['settings']['width'], sequence['settings']['height']) == (96, 64)
                    and sequence['settings']['frame_rate'] == {'num': 12, 'den': 1}, 'native_reopen_settings_changed')
            cases[-1]['nativeReopen'] = 'PASS'; cases[-1]['projectSemanticEquality'] = True
            cases[-1]['expectedSaveAsChanges'] = ['project.name', 'project.root.name']
            changes = {'mode': 'bridge' if mode == 'headless' else 'headless', 'platform': 'unsupported-platform',
                       'runtimeVersion': 'incompatible', 'runtimeSha256': '0' * 64, 'parametersSha256': '0' * 64}
            if mode == 'bridge': changes['desktopSha256'] = '0' * 64
            for key, value in changes.items():
                plan = copy.deepcopy(base); plan['requires'] = dict(correct, **{key: value})
                failed, _, events = run_case(mode + '-mismatch-' + key, mode, plan)
                require(failed['result'] == 'FAIL' and 'capability_identity_mismatch: ' + key in failed.get('error', '')
                        and failed['steps'] == [] and not any(e['params'].get('name') == 'command_run' for e in events),
                        'identity_mismatch_not_blocked')
            if mode == 'bridge':
                failed, _, events = run_case('bridge-unknown-desktop', mode, base, desktop_identity=None)
                require(failed['result'] == 'FAIL' and 'capability_unknown: desktop_identity' in failed.get('error', '')
                        and not any(e['params'].get('name') == 'command_run' for e in events), 'unknown_desktop_not_blocked')
            for kind in ('codec', 'font', 'model'):
                for status in ('missing', 'unknown'):
                    plan = copy.deepcopy(base)
                    plan['requires'] = {'resources': [{'kind': kind, 'name': 'missing-filmcraft-fixed-resource'}]}
                    fault = 'unknown-' + kind if status == 'unknown' else None
                    failed, destination, events = run_case(mode + '-' + status + '-' + kind, mode, plan, fault)
                    require(failed['result'] == 'FAIL' and 'capability_' + status in failed.get('error', '')
                            and failed['steps'] == [] and not (destination / 'project.fcproj').exists(), 'resource_gate_failed')
                    require(failed['capabilitySnapshot']['resources'][0]['status'] == status, 'resource_state_promoted')
                    require(all(e['params'].get('arguments', {}).get('id') in
                                ('export.formats', 'fonts.list', 'transcript.models')
                                for e in events if e['params'].get('name') == 'command_run'), 'resource_failure_edited')
            failed, destination, events = run_case(mode + '-late-contract', mode, base, 'late-contract')
            require(failed['result'] == 'FAIL' and 'capability_contract_drift' in failed.get('error', '')
                    and [s['state'] for s in failed['steps']] == ['succeeded', 'succeeded', 'blocked']
                    and not (destination / 'project.fcproj').exists()
                    and not any(e['params'].get('arguments', {}).get('id') == 'file.saveAs' for e in events),
                    'late_contract_edit_not_blocked')
            if mode == 'bridge':
                plan = copy.deepcopy(base)
                plan['operations'].append({'command': 'file.importImageSequence', 'params': {'path': 'unused.png'}})
                failed, _, events = run_case('bridge-real-parameter-drift', mode, plan)
                require(failed['result'] == 'FAIL' and 'capability_contract_drift: file.importImageSequence' in failed.get('error', '')
                        and failed['steps'] == [] and not any(e['params'].get('name') == 'command_run' for e in events),
                        'real_bridge_drift_not_blocked')
        # 真正下载并重探测使用隔离数据目录；不改用户的模型缓存。
        model_plan = {'schema': 'craft-command-plan/v1', 'operations': [
            {'command': 'transcript.models', 'params': {}, 'as': 'before'},
            {'command': 'transcript.downloadModel', 'params': {'model': 'whisper-tiny'}},
            {'command': 'transcript.models', 'params': {}, 'as': 'after'},
            {'command': 'transcript.generate', 'params': {'model': 'whisper-tiny', 'items': []}}]}
        model_receipt, _, model_events = run_case('headless-model-install-reprobe', 'headless', model_plan)
        first = model_receipt['steps'][0]['result']
        require(any(r['id'] == 'whisper-tiny' and r['installed'] is False for r in first['models']), 'model_cache_not_empty')
        require(len(model_receipt['steps']) == 4 and all(s['state'] == 'succeeded' for s in model_receipt['steps'][:3]),
                'model_download_or_reprobe_failed')
        require(model_receipt['steps'][3]['resourceCapabilities'][0]['status'] == 'available'
                and any(e['params'].get('arguments', {}).get('id') == 'transcript.generate' for e in model_events),
                'model_update_not_reprobed')
        require(model_receipt['steps'][3]['state'] == 'failed' and 'nothing to transcribe' in model_receipt.get('error', ''),
                'model_inference_scope_changed')
        cases[-1]['modelInstallReprobe'] = 'PASS'
        cases[-1]['modelInference'] = 'NOT_RUN: empty items intentionally exercises resource gate, not speech quality'
        for name, directory in directories.items(): helper.verify_installed_skill(directory, expected)
        fixed.verify_code_files(skill.parent.parent, expected['codeFilesSha256'])
        save('catalogs.json', catalogs); save('native-traces.json', traces); save('cases.json', cases)
        report = {'schema': 'filmcraft-fixed-capability-evidence/v1', 'result': 'PASS', 'task': '9.12',
                  'plugin': expected, 'helper': helper_identity, 'binding': binding,
                  'preflightCases': len(preflight), 'nativeCases': len(cases),
                  'modes': {mode: {'staticDiscovery': 'PASS', 'identityAndParameterGates': 'PASS',
                      'positiveExecution': 'PASS: default and bound reopen plans only',
                      'negativeExecution': 'PASS: identity/resources/late drift; controlled replies explicitly labeled',
                      'reopen': 'PASS', 'nonTargetPreservation': 'PASS', 'fullCommandAcceptance': 'NOT_PROVEN'}
                      for mode in ('headless', 'bridge')},
                  'resourceUpdate': 'PASS: actual isolated whisper-tiny download followed by fresh probe before dependent request',
                  'installedFilesUnchanged': True, 'completeRuntimeUpgrade': 'NOT_RUN',
                  'otherPlatforms': 'NOT_RUN', 'fullV1': 'INCOMPLETE',
                  'artifacts': {name: sha(output / name) for name in
                                ('preflight.json', 'catalogs.json', 'native-traces.json', 'cases.json')},
                  'producerSha256': sha(Path(__file__))}
        save('report.json', report)
        return report
    finally:
        if old_data is None: os.environ.pop('FILMCRAFT_DATA_DIR', None)
        else: os.environ['FILMCRAFT_DATA_DIR'] = old_data
        # 失败也保留已执行的真实证据，不在异常后编造总 PASS。
        save('catalogs.json', catalogs); save('native-traces.json', traces); save('cases.json', cases)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.host, args.authority, args.ref, args.output)
    print(json.dumps({'result': report['result'], 'preflightCases': report['preflightCases'],
                      'nativeCases': report['nativeCases'], 'task': report['task']}))
