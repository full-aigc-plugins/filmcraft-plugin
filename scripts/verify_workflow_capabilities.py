#!/usr/bin/env python3
"""固定领域工作流的能力门禁与失败阶段验收；原生回复故障明确标注。"""
import argparse
import copy
import json
from pathlib import Path
import sys
import types

sys.dont_write_bytecode = True
from verify_fixed_capabilities import ROOT, digest, load, require, sha


def verify(host, authority, ref, output):
    fixed = load(ROOT / 'scripts/verify_fixed_install.py', 'workflow_fixed_install')
    expected = fixed.release_entry(ROOT, ref)
    receipt = json.loads((host / 'host-receipt.json').read_text())
    require(receipt['result'] == 'PASS' and receipt['plugin'] == expected, 'fixed_host_mismatch')
    directories = json.loads((host / 'installed-directories.private.json').read_text())
    require(set(directories) == set(expected['skills']), 'installed_inventory_mismatch')
    helper, helper_identity = fixed.owner_helper(authority)
    require(receipt['helper'] == helper_identity, 'fixed_helper_mismatch')
    skill = Path(directories['filmcraft-use']).resolve()
    require(skill.is_relative_to((host / 'host-config').resolve()), 'installed_path_outside_host')
    for name, directory in directories.items():
        require(Path(directory).resolve() == skill.parent / name, 'installed_skill_path_mismatch')
        helper.verify_installed_skill(directory, expected)
    fixed.verify_code_files(skill.parent.parent, expected['codeFilesSha256'])
    require(not output.exists() and not output.is_symlink(), 'capability_output_exists')
    output.mkdir(mode=0o700)
    root = output / 'work'; root.mkdir(mode=0o700)
    workflow = load(skill / 'scripts/workflow.py', 'fixed_capability_workflow')
    commands = workflow.native_module().commands
    original_load = workflow.load_module
    native_session = workflow.load_module('mcp_session').Session
    from PIL import Image
    image = root / 'still.png'; Image.new('RGB', (32, 32), '#ff0000').save(image)
    image_hash = sha(image)
    plan = json.loads((skill / 'examples/native-workflow.json').read_text())
    plan['assets'] = {'still': {'path': str(image), 'sha256': image_hash}}
    cases, events = [], {}
    source_files = None

    def save(name, value):
        text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)
        text = text.replace(str(output.resolve()), '[TEST_ROOT]').replace(str(output), '[TEST_ROOT]')
        text = text.replace(str(Path.home()), '[USER_HOME]')
        (output / name).write_text(text + '\n')

    def tree(directory):
        return {p.relative_to(directory).as_posix(): sha(p) for p in sorted(directory.rglob('*')) if p.is_file()}

    def run(name, current, fault=None, source=None):
        trace = []; events[name] = trace
        class Session(native_session):
            def request(self, method, params):
                result = super().request(method, params)
                event = {'method': method, 'params': copy.deepcopy(params), 'nativeReplySha256': digest(result)}
                if params.get('name') == 'command_run': event['reply'] = copy.deepcopy(result)
                if fault and params.get('name') == 'command_run':
                    identifier = {'codec': 'export.formats', 'font': 'fonts.list', 'model': 'transcript.models'}[fault]
                    if params.get('arguments', {}).get('id') == identifier:
                        result = {'content': [{'type': 'text', 'text': '{"unexpected":"controlled malformed probe"}'}]}
                        event['deliveredFaultReply'] = copy.deepcopy(result)
                trace.append(event)
                return result
        workflow.load_module = lambda name: types.SimpleNamespace(Session=Session) if name == 'mcp_session' else original_load(name)
        destination = root / name
        error, result = None, None
        try:
            result = workflow.execute(current, destination, runtime_home=root / 'runtime',
                                      data_dir=root / 'native-data', source=source)
        except (ValueError, RuntimeError) as problem:
            error = str(problem)
        require(sha(image) == image_hash, 'source_media_changed')
        if source_files is not None: require(tree(root / 'default') == source_files, 'source_delivery_changed')
        evidence = json.loads((destination / 'capabilities.json').read_text()) if not error else None
        failure = json.loads((destination / 'failure.json').read_text()) if error else None
        if error:
            stage = (destination / failure['stage']).resolve()
            evidence = json.loads((stage / 'capabilities.json').read_text())
            require(failure['files']['capabilities.json']['sha256'] == sha(stage / 'capabilities.json')
                    and failure['replayAllowed'] is False, 'failure_evidence_not_retained')
        snapshot = evidence['snapshot'] if 'snapshot' in evidence else evidence
        require(snapshot['runtime']['binarySha256'] == commands.catalog()['runtimeSha256']
                and snapshot['mode'] == 'headless', 'workflow_snapshot_identity_mismatch')
        case = {'case': name, 'plan': current, 'planSha256': digest(current), 'fault': fault,
                'executionLayer': 'actual native plus controlled reply fault' if fault else 'actual native',
                'result': 'FAIL' if error else 'PASS', 'error': error, 'capabilityEvidenceSha256': digest(evidence),
                'snapshot': {k: v for k, v in snapshot.items() if k != 'commands'},
                'failure': failure, 'sourceMediaPreserved': True, 'originalDeliveryPreserved': source_files is not None,
                'artifactHashes': tree(destination)}
        cases.append(case)
        print(name, case['result'], error or '', flush=True)
        return result, case, trace

    try:
        delivered, _, _ = run('default', plan)
        require(delivered is not None, 'default_workflow_failed')
        source_files = tree(root / 'default')
        snapshot = json.loads((root / 'default/capabilities.json').read_text())
        snapshot = snapshot.get('snapshot', snapshot)
        binding = {'pluginSha': expected['sha'], 'sourceSha': expected['skillSourceSha'],
                   'runtimeSha256': snapshot['runtime']['binarySha256'],
                   'runtimeVersion': snapshot['runtime']['version'], 'platform': snapshot['runtime']['platform'], 'mode': 'headless'}
        correct = {'mode': 'headless', 'platform': binding['platform'], 'runtimeVersion': binding['runtimeVersion'],
                   'runtimeSha256': binding['runtimeSha256'], 'parametersSha256': snapshot['parametersSha256']}
        bound = copy.deepcopy(plan); bound['requires'] = correct
        delivered, _, _ = run('bound', bound)
        require(delivered is not None, 'bound_workflow_failed')
        revision = {'expectedProjectSha256': sha(root / 'default/project.fcproj'), 'requires': correct,
                    'operations': [{'command': 'native.command', 'params': {'command': 'sequence.inspect', 'params': {}}}],
                    'frames': ['0'], 'export': {'audioRequired': False}}
        revised, _, _ = run('revision', revision, source=root / 'default')
        require(revised is not None and revised['sourceProjectSha256'] == revision['expectedProjectSha256'], 'revision_failed')
        for key, value in {'platform': 'unsupported-platform', 'runtimeVersion': 'incompatible',
                           'runtimeSha256': '0' * 64, 'parametersSha256': '0' * 64}.items():
            changed = copy.deepcopy(plan); changed['requires'] = {key: value}
            _, case, trace = run('mismatch-' + key, changed)
            require('capability_identity_mismatch: ' + key in (case['error'] or ''), 'workflow_identity_not_blocked')
            require(all(e['params'].get('arguments', {}).get('id') == 'export.formats'
                        for e in trace if e['params'].get('name') == 'command_run'), 'identity_failure_edited')
        for kind in ('codec', 'font', 'model'):
            for status in ('missing', 'unknown'):
                changed = copy.deepcopy(plan)
                changed['requires'] = {'resources': [{'kind': kind, 'name': 'missing-filmcraft-fixed-resource'}]}
                _, case, trace = run(status + '-' + kind, changed, kind if status == 'unknown' else None)
                require('capability_' + status in (case['error'] or '')
                        and case['snapshot']['resources'][0]['status'] == status, 'workflow_resource_not_blocked')
                require(all(e['params'].get('arguments', {}).get('id') in ('export.formats', 'fonts.list', 'transcript.models')
                            for e in trace if e['params'].get('name') == 'command_run'), 'resource_failure_edited')
        for name, directory in directories.items(): helper.verify_installed_skill(directory, expected)
        fixed.verify_code_files(skill.parent.parent, expected['codeFilesSha256'])
        save('cases.json', cases); save('native-traces.json', events)
        report = {'schema': 'filmcraft-fixed-workflow-capability-evidence/v1', 'result': 'PASS', 'task': '9.12',
                  'plugin': expected, 'binding': binding, 'nativeCases': len(cases), 'defaultAndBoundPlans': 'PASS',
                  'revisionAndSourcePreservation': 'PASS', 'resources': 'PASS: missing and controlled unknown, three kinds',
                  'installedFilesUnchanged': True, 'bridge': 'N/A: domain workflow is explicitly headless',
                  'otherPlatforms': 'NOT_RUN', 'fullV1': 'INCOMPLETE', 'producerSha256': sha(Path(__file__)),
                  'artifacts': {name: sha(output / name) for name in ('cases.json', 'native-traces.json')}}
        save('report.json', report)
        return report
    finally:
        workflow.load_module = original_load
        save('cases.json', cases); save('native-traces.json', events)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.host, args.authority, args.ref, args.output)
    print(json.dumps({'result': result['result'], 'nativeCases': result['nativeCases']}))
