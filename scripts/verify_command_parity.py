#!/usr/bin/env python3
"""FC-CM-001 固定安装验收：真实入口副作用边界、精确整数和分维证据。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import types

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BAD = ('254016000000', True, False, 1.5, 2 ** 63, -(2 ** 63) - 1)
GOOD = (2 ** 53 + 1, 2 ** 63 - 1, -(2 ** 63))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def native(operation):
    return {'command': 'native.command', 'params': operation}


def verify(host, authority, ref, output):
    fixed = load(ROOT / 'scripts/verify_fixed_install.py', 'fixed_install')
    expected = fixed.release_entry(ROOT, ref)
    require(not output.exists() and not output.is_symlink(), 'parity_output_exists')
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
    output.mkdir(mode=0o700)
    commands = load(skill / 'scripts/commands.py', 'installed_commands')
    workflow = load(skill / 'scripts/workflow.py', 'installed_workflow')
    catalog = commands.catalog()
    require(workflow.ticks(str(2 ** 53 + 1)) == 2 ** 53 + 1, 'domain_tick_conversion_lost_precision')
    observations, validations, events, literal_results, reference_results = [], [], [], [], []
    def observe(command, dimension, evidence, scope):
        # 多个真实场景可以共同支持同一维度；索引不重复写同一单元格。
        if not any(row['command'] == command and row['dimension'] == dimension for row in observations):
            observations.append({'command': command, 'dimension': dimension, 'status': 'PASS',
                                 'evidence': evidence, 'scope': scope})
    for row in catalog['commands']:
        fields = sorted(set(re.findall(r'"([A-Za-z][A-Za-z0-9_]*)"\s*:\s*ticks?\b', row['params'])))
        if row['id'] == 'transcript.set':
            fields = ['transcript.words.start', 'transcript.words.end']
        if not fields:
            continue
        for field in fields:
            for value in BAD + GOOD:
                params = {field: value}
                if field.startswith('transcript.'):
                    params = {'item': 1, 'transcript': {'words': [{'text': 'exact', 'start': 0, 'end': 1}]}}
                    params['transcript']['words'][0][field.rsplit('.', 1)[1]] = value
                operation = {'command': row['id'], 'params': params}
                for entry in ('commands', 'workflow'):
                    error = None
                    try:
                        if entry == 'commands':
                            commands.validate({'schema': 'craft-command-plan/v1', 'operations': [operation]})
                        else:
                            workflow.validate({'operations': [native(operation)]})
                    except ValueError as problem:
                        error = str(problem)
                    valid = type(value) is int and -(2 ** 63) <= value < 2 ** 63
                    require(error is None if valid else error and 'invalid_tick_parameter' in error,
                            'parameter_entry_parity_failed: ' + row['id'])
                    require(json.loads(json.dumps(operation)) == operation, 'json_integer_precision_lost')
                    validations.append({'command': row['id'], 'field': field, 'entry': entry,
                                        'value': value, 'result': 'ACCEPTED' if valid else 'REJECTED', 'error': error})
        observe(row['id'], 'parameterValidation', 'parameter-validation.json',
                'All documented tick fields: signed 64-bit type/range and exact JSON integers; other parameter types are NOT_RUN')
        observe(row['id'], 'negativeRejection', 'parameter-validation.json',
                'Adapter preflight rejects malformed tick values in both entries; not native context rejection')
    print('fixed tick validation cases:', len(validations), flush=True)
    with tempfile.TemporaryDirectory(prefix='filmcraft-fixed-parity-') as temporary:
        root = Path(temporary)
        marker = root / 'non-target'; marker.write_bytes(b'preserve unrelated input')
        marker_hash = sha(marker)
        operations = [{'command': 'multicam.cutToCamera', 'params': {'camera': 2, 'time': value}} for value in BAD]
        for field in ('start', 'end'):
            for value in ('0', True, 0.0, 2 ** 63):
                operation = {'command': 'transcript.set', 'params': {'item': 1, 'transcript': {
                    'words': [{'text': 'invalid', 'start': 0, 'end': 1}]}}}
                operation['params']['transcript']['words'][0][field] = value
                operations.append(operation)
        for name, directory in sorted(directories.items()):
            for entry in ('commands', 'workflow'):
                for index, operation in enumerate(operations):
                    plan = {'schema': 'craft-command-plan/v1', 'operations': [operation]} if entry == 'commands' else {
                        'document': {'name': 'Invalid', 'width': 32, 'height': 32, 'frameRate': {'num': 12, 'den': 1}},
                        'operations': [native(operation)]}
                    plan_path = root / 'invalid-plan.json'; write(plan_path, plan)
                    plan_hash = sha(plan_path)
                    destination, runtime = root / 'forbidden-output', root / 'forbidden-runtime'
                    before = set(root.rglob('*'))
                    argv = [sys.executable, '-I', '-B', str(Path(directory) / 'scripts' / (entry + '.py'))]
                    if entry == 'commands': argv.append('run')
                    argv += [str(plan_path), '--output', str(destination), '--runtime-home', str(runtime)]
                    result = subprocess.run(argv, capture_output=True, text=True, timeout=20)
                    reply = json.loads(result.stdout)
                    require(result.returncode == 1 and 'invalid_tick_parameter' in reply.get('error', ''), 'literal_not_rejected')
                    require(not destination.exists() and not runtime.exists() and set(root.rglob('*')) == before,
                            'literal_failure_had_filesystem_side_effect')
                    require(sha(marker) == marker_hash and sha(plan_path) == plan_hash, 'literal_input_changed')
                    literal_results.append({'skill': name, 'entry': entry, 'case': index + 1,
                        'command': operation['command'], 'planSha256': plan_hash, 'error': reply['error'],
                        'runtimeCreated': False, 'outputCreated': False, 'filesUnchanged': True})
                wrong = {'operations': []} if entry == 'commands' else {'schema': 'craft-command-plan/v1', 'operations': []}
                write(plan_path, wrong)
                result = subprocess.run(argv, capture_output=True, text=True, timeout=20)
                reply = json.loads(result.stdout)
                prefix = 'invalid_command_plan' if entry == 'commands' else 'invalid_workflow_plan'
                require(result.returncode == 1 and prefix in reply.get('error', '')
                        and not destination.exists() and not runtime.exists(), 'wrong_plan_entry_not_rejected')
                literal_results.append({'skill': name, 'entry': entry, 'case': 'wrong-plan-type',
                    'planSha256': sha(plan_path), 'error': reply['error'], 'runtimeCreated': False, 'outputCreated': False})
            print('literal CLI cases passed:', name, flush=True)
        runtime = root / 'runtime'
        installed = commands.load('bootstrap').install(json.loads((skill / 'scripts/runtime.lock.json').read_text()), runtime)
        require(installed['binarySha256'] == catalog['runtimeSha256'], 'runtime_catalog_mismatch')
        actual_session = commands.load('mcp_session').Session
        class TracedSession(actual_session):
            def request(self, method, params):
                event = {'method': method, 'params': copy.deepcopy(params)}
                events.append(event)
                result = super().request(method, params)
                event['result'] = copy.deepcopy(result)
                return result
        with TracedSession([installed['executable'], 'mcp']) as session:
            rows = commands.runtime_rows(session)
        require({row['id']: row['params'] for row in rows} ==
                {row['id']: row['params'] for row in catalog['commands']}, 'live_catalog_drift')
        plan = json.loads((skill / 'examples/commands-advanced.json').read_text())
        precise = {'command': 'transcript.set', 'params': {'item': {'$ref': 'red.item'}, 'transcript': {
            'language': 'en', 'speakers': [{'name': 'Fixture'}],
            'words': [{'text': 'exact', 'start': 2 ** 53 + 1, 'end': 2 ** 53 + 2, 'speaker': 0}]}}}
        plan['operations'][-1:-1] = [precise, {'command': 'source.open', 'params': {'item': {'$ref': 'red.item'}}},
            {'command': 'transcript.inspect', 'params': {}, 'as': 'transcript'}]
        created = commands.execute(plan, root / 'create', runtime_home=runtime, session_factory=TracedSession)
        require(created['result'] == 'PASS', 'native_create_failed: ' + str(created.get('error')))
        item = next(step['result']['item'] for step, operation in zip(created['steps'], plan['operations']) if operation.get('as') == 'red')
        project = root / 'create/project.fcproj'; project_hash = sha(project)
        # transcript.inspect 是音轨上的派生视图；JSON 工程才是逐媒体原始 ticks 的事实源。
        transcript = json.loads(project.read_text())['project']['transcripts'][str(item)]
        require(transcript['words'][0]['start'] == 2 ** 53 + 1 and
                transcript['words'][0]['end'] == 2 ** 53 + 2, 'native_transcript_precision_lost')
        reopen = {'schema': 'craft-command-plan/v1', 'operations': [
            {'command': 'file.open', 'params': {'path': {'$ref': 'original.path'}}},
            {'command': 'source.open', 'params': {'item': item}},
            {'command': 'transcript.inspect', 'params': {}}, {'command': 'sequence.inspect', 'params': {}},
            {'command': 'file.saveAs', 'params': {'path': {'$output': 'roundtrip.fcproj'}}}]}
        opened = commands.execute(reopen, root / 'reopen', runtime_home=runtime,
                                  session_factory=TracedSession, inputs={'original': project})
        require(opened['result'] == 'PASS', 'native_reopen_failed')
        roundtrip = root / 'reopen/roundtrip.fcproj'
        require(json.loads(roundtrip.read_text())['project']['transcripts'][str(item)] == transcript,
                'reopened_transcript_precision_lost')
        saved_sequence = next(step['result'] for step in created['steps'] if step['command'] == 'sequence.inspect')
        # 选择状态属于会话，不是工程持久化字段；与公开工作流的重开合同一致。
        persisted = lambda value: {key: child for key, child in value.items() if key != 'selection'}
        write(output / 'native-sequence-comparison.json', {'before': saved_sequence, 'after': opened['steps'][3]['result'],
              'excludedSessionFields': ['selection']})
        require(persisted(opened['steps'][3]['result']) == persisted(saved_sequence), 'reopened_sequence_changed')
        require(sha(project) == project_hash, 'original_project_changed')
        # 工作流公开入口复用同一真实 Session，仅记录请求，不替换原生返回值。
        original_load = workflow.load_module
        workflow.load_module = lambda name: types.SimpleNamespace(Session=TracedSession) if name == 'mcp_session' else original_load(name)
        from PIL import Image
        image = root / 'still.png'; Image.new('RGB', (32, 32), '#ff0000').save(image)
        image_hash = sha(image)
        workflow_plan = json.loads((skill / 'examples/native-workflow.json').read_text())
        workflow_plan['assets'] = {'still': {'path': str(image), 'sha256': image_hash}}
        workflow_precise = copy.deepcopy(precise); workflow_precise['params']['item'] = {'$ref': 'still.item'}
        workflow_plan['operations'] += [native(workflow_precise),
            native({'command': 'source.open', 'params': {'item': {'$ref': 'still.item'}}}),
            dict(native({'command': 'transcript.inspect', 'params': {}}), **{'as': 'transcript'})]
        delivered = workflow.execute(workflow_plan, root / 'workflow', runtime_home=runtime)
        workflow_item = delivered['bindings']['still']['item']
        words = json.loads((root / 'workflow/project.fcproj').read_text())['project']['transcripts'][str(workflow_item)]['words']
        require(words[0]['start'] == 2 ** 53 + 1 and words[0]['end'] == 2 ** 53 + 2,
                'workflow_transcript_precision_lost')
        require(sha(image) == image_hash, 'workflow_input_changed')
        # 非法引用取自真实 sequence.inspect 返回的名称，依赖编辑必须未提交。
        for entry in ('commands', 'workflow'):
            for case in ('multicam.cutToCamera', 'transcript.set', 'whole-parameters'):
                identifier = 'multicam.cutToCamera' if case == 'whole-parameters' else case
                invalid = {'command': identifier, 'params': {'camera': 2, 'time': {'$ref': 'before.name'}}} if identifier.startswith('multicam') else {
                    'command': identifier, 'params': {'item': item, 'transcript': {'words': [
                        {'text': 'invalid', 'start': {'$ref': 'before.name'}, 'end': 1}]}}}
                if case == 'whole-parameters':
                    invalid['params'] = {'$ref': 'before.name'}
                inspect = {'command': 'sequence.inspect', 'params': {}}
                event_start = len(events)
                if entry == 'commands':
                    failure_plan = {'schema': 'craft-command-plan/v1', 'operations': [reopen['operations'][0],
                        dict(inspect, **{'as': 'before'}), invalid, {'command': 'file.saveAs', 'params': {'path': {'$output': 'forbidden.fcproj'}}}]}
                    failed = commands.execute(failure_plan, root / ('invalid-' + entry + '-' + case), runtime_home=runtime,
                        session_factory=TracedSession, inputs={'original': project})
                    error = failed.get('error', '')
                    require(failed['result'] == 'FAIL', 'reference_not_failed')
                else:
                    failure_plan = copy.deepcopy(workflow_plan)
                    failure_plan['operations'] = failure_plan['operations'][:2] + [
                        dict(native(inspect), **{'as': 'before'}), native(invalid)]
                    try:
                        workflow.execute(failure_plan, root / ('invalid-' + entry + '-' + case), runtime_home=runtime)
                        raise ValueError('reference_not_failed')
                    except ValueError as problem:
                        error = str(problem)
                relevant = events[event_start:]
                calls = [event['params'].get('arguments', {}).get('id') for event in relevant
                         if event['method'] == 'tools/call' and event['params'].get('name') == 'command_run']
                expected_error = ('invalid_command_parameters' if entry == 'commands' else 'invalid_native_operation') if case == 'whole-parameters' else 'invalid_tick_parameter'
                require(expected_error in error and identifier not in calls and 'file.saveAs' not in calls,
                        'invalid_reference_submitted_dependent_edit')
                require(sha(project) == project_hash and sha(image) == image_hash, 'reference_input_changed')
                reference_results.append({'entry': entry, 'command': identifier, 'case': case, 'error': error,
                    'eventStart': event_start, 'eventEnd': len(events), 'dependentCommandRequests': 0,
                    'originalProjectPreserved': True, 'inputPreserved': True})
        for identifier in {step['command'] for step in created['steps'] + opened['steps'] if step.get('command')}:
            observe(identifier, 'positiveExecution', 'native-create-reopen.json', 'Actual command execution with real replies')
        for identifier in ('file.newSequence', 'timeline.place',
                           'clip.speedDuration', 'sequence.applyVideoTransition', 'transcript.set', 'file.saveAs'):
            observe(identifier, 'reopen', 'native-create-reopen.json', 'Persisted sequence, speeds, transition and exact transcript compared after native reopen')
            observe(identifier, 'nonTargetPreservation', 'native-create-reopen.json', 'Reopen preserves original saved project bytes and compares sequence state; broader revisions NOT_RUN')
        payload = {'created': created, 'opened': opened, 'workflow': delivered, 'projectSha256': project_hash,
                   'roundtripProjectSha256': sha(roundtrip), 'persistedTranscript': transcript,
                   'stillSha256': image_hash, 'originalPreserved': True, 'exactTick': 2 ** 53 + 1}
        def safe(value):
            if isinstance(value, str):
                value = value.replace(str(root), '[TEST_ROOT]')
                return re.sub(r'/(?:Users|home)/[A-Za-z0-9_.-]+', '[USER_HOME]', value)
            if isinstance(value, dict): return {key: safe(child) for key, child in value.items()}
            if isinstance(value, list): return [safe(child) for child in value]
            return value
        write(output / 'native-create-reopen.json', safe(payload))
        write(output / 'native-events.json', safe(events))
    for directory in directories.values(): helper.verify_installed_skill(directory, expected)
    binding = {'pluginSha': expected['sha'], 'sourceSha': expected['skillSourceSha'],
               'runtimeSha256': installed['binarySha256'], 'runtimeVersion': installed['version'],
               'platform': installed['platform'], 'mode': 'headless'}
    matrix = load(ROOT / 'scripts/command_evidence.py', 'command_evidence').build(
        rows, binding, {'binding': binding, 'observations': observations})
    write(output / 'actual-catalog.json', rows)
    write(output / 'parameter-validation.json', validations)
    write(output / 'literal-cli.json', literal_results)
    write(output / 'reference-rejection.json', reference_results)
    write(output / 'command-matrix.json', matrix)
    report = {'schema': 'filmcraft-fixed-command-parity/v1', 'result': 'PASS', 'plugin': expected,
        'binding': binding, 'helper': helper_identity, 'literalCliCases': len(literal_results),
        'parameterCases': len(validations), 'referenceCases': len(reference_results),
        'installedSkillsPreserved': len(directories), 'matrixSummary': matrix['summary'],
        'producerSha256': sha(Path(__file__)), 'matrixProducerSha256': sha(ROOT / 'scripts/command_evidence.py'),
        'files': {path.name: sha(path) for path in sorted(output.iterdir()) if path.is_file()},
        'notAccepted': ['all command contexts and parameter types', 'bridge', 'other platforms',
                        'automatic host routing', 'full V1']}
    write(output / 'report.json', report)
    print(json.dumps({'result': 'PASS', 'literalCliCases': len(literal_results),
                      'parameterCases': len(validations), 'referenceCases': len(reference_results)}))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    verify(args.host, args.authority, args.ref, args.output)
