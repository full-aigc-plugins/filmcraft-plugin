#!/usr/bin/env python3
"""固定安装的27条轨道目标命令验收；真实headless/所属桌面桥，不替代全命令资格。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def normalized_project(path):
    value = json.loads(path.read_text())
    value['project']['name'] = 'Owned project'
    value['project']['root']['name'] = 'Owned project'
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installed-plugin', type=Path, required=True)
    parser.add_argument('--runtime-home', type=Path, required=True)
    parser.add_argument('--plugin-sha', required=True)
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    installed = args.installed_plugin.resolve(strict=True)
    skill = installed / 'skills/filmcraft-use'
    runtime = args.runtime_home.resolve(strict=True)
    root = args.output.resolve()
    root.mkdir(mode=0o700)
    commands = load(skill / 'scripts/commands.py', 'fixed_target_commands')
    desktop = load(skill / 'scripts/desktop_session.py', 'fixed_target_desktop')
    matrix_builder = load(Path(__file__).with_name('command_evidence.py'), 'target_evidence')
    toggles = ['timeline.toggleTarget' + kind + str(n) for kind in ('V', 'A') for n in range(1, 9)]
    all_targets = ['timeline.toggleAllVideoTargets', 'timeline.toggleAllAudioTargets']
    sources = ['timeline.toggleAllSourceVideo', 'timeline.toggleAllSourceAudio']
    moves = ['timeline.moveVideoTargetsUp', 'timeline.moveVideoTargetsDown',
             'timeline.moveAudioTargetsUp', 'timeline.moveAudioTargetsDown']
    persistent = ['timeline.toggleMuteTargetedAudio', 'timeline.toggleSoloTargetedAudio',
                  'timeline.toggleOutputTargetedVideo']
    tested = toggles + all_targets + sources + moves + persistent
    catalog = commands.catalog()['commands']
    assert len(tested) == len(set(tested)) == 27
    assert all(next(row for row in catalog if row['id'] == q)['params'] == '{}' for q in tested)
    base = copy.deepcopy(json.loads((skill / 'examples/commands-advanced.json').read_text())['operations'][:6])
    base[1]['params'].update(video=8, audio=8)
    modes = []
    for mode in ('headless', 'bridge'):
        work = root / mode
        work.mkdir()
        policy = commands.load('execution_permissions').from_cli([str(root)], [str(work), str(runtime)])

        def execute(operations, label, inputs=None):
            plan = {'schema': 'craft-command-plan/v1', 'operations': operations}
            write(work / (label + '-plan.private.json'), plan)
            output = work / label
            if mode == 'headless':
                receipt = commands.execute(plan, output, runtime_home=runtime, permissions=policy, inputs=inputs)
            else:
                receipt = desktop.run(plan, output, runtime_home=runtime, permissions=policy, inputs=inputs)
                proof = json.loads((output / 'desktop-session.json').read_text())
                assert proof['ownedProcessesStopped'] and proof['listenerOwnedByPID'] and proof['sessionsStarted'] == 1
            write(work / (label + '-receipt.private.json'), receipt)
            return receipt

        expectations = {}

        def op(command, params=None, alias=None, expected=None):
            value = {'command': command, 'params': params or {}}
            if alias:
                value['as'] = alias
                if expected is not None:
                    expectations[alias] = expected
            return value

        def suite():
            operations = []
            for identifier in toggles:
                kind, number = identifier[-2], int(identifier[-1])
                operations += [op(identifier, alias=identifier.replace('.', '_') + '_off', expected=('target-off', kind, number)),
                               op(identifier, alias=identifier.replace('.', '_') + '_on', expected=('all-on',))]
            for identifier, kind in zip(all_targets, ('V', 'A')):
                operations += [op(identifier, alias=kind + '_all_off', expected=('kind-off', kind)),
                               op(identifier, alias=kind + '_all_on', expected=('all-on',))]
            for identifier, kind in zip(sources, ('V', 'A')):
                operations += [op(identifier, alias=kind + '_source_off', expected=('source-off', kind)),
                               op(identifier, alias=kind + '_source_on', expected=('all-on',))]
            operations += [op(all_targets[0]), op(toggles[0]),
                           op(moves[0], alias='video_up', expected=('one-target', 'V', 2)),
                           op(moves[1], alias='video_down', expected=('one-target', 'V', 1)), op(all_targets[0]),
                           op(all_targets[1]), op(toggles[9]),
                           op(moves[2], alias='audio_up', expected=('one-target', 'A', 1)),
                           op(moves[3], alias='audio_down', expected=('one-target', 'A', 2)), op(all_targets[1])]
            for identifier, kind, field, changed in zip(persistent, ('audio', 'audio', 'video'), ('muted', 'solo', 'enabled'), (True, True, False)):
                operations += [op(identifier), op('sequence.inspect', alias=field + '_changed', expected=('track-flags', kind, field, changed)),
                               op(identifier), op('sequence.inspect', alias=field + '_restored', expected=('track-flags', kind, field, not changed))]
            return operations

        def validate(receipt, operations):
            assert receipt['result'] == 'PASS', receipt.get('error')
            assert len(receipt['steps']) == len(operations)
            values = {operation['as']: step['result'] for operation, step in zip(operations, receipt['steps']) if 'as' in operation}
            seq = values['baseline']
            videos = [track['id'] for track in seq['video']]
            audios = [track['id'] for track in seq['audio']]
            assert len(videos) == len(audios) == 8
            all_ids = set(videos + audios)
            for alias, expected in expectations.items():
                actual = values[alias]
                category, *detail = expected
                if category == 'track-flags':
                    kind, field, changed = detail
                    reference = copy.deepcopy(seq)
                    for track in reference[kind]:
                        track[field] = changed
                    assert actual == reference, (mode, alias, actual)
                    continue
                target = all_ids.copy()
                video_dest, audio_dest = videos[0], audios[0]
                if category in ('target-off', 'kind-off', 'one-target'):
                    kind = detail[0]
                    ids = videos if kind == 'V' else audios
                    target -= set(ids) if category != 'target-off' else {ids[detail[1] - 1]}
                    if category == 'one-target':
                        target.add(ids[detail[1] - 1])
                elif category == 'source-off':
                    if detail[0] == 'V':
                        video_dest = None
                    else:
                        audio_dest = None
                assert set(actual['targeted']) == target, (mode, alias, actual)
                assert actual['videoDest'] == video_dest and actual['audioDest'] == audio_dest
            assert all(step['state'] == 'succeeded' for step in receipt['steps'])
            return seq

        common = [op('sequence.inspect', alias='baseline')] + suite()
        create_ops = base + [op('file.saveAs', {'path': {'$output': 'before.fcproj'}})] + common
        create_ops += [op('file.saveAs', {'path': {'$output': 'preserved.fcproj'}})]
        create_ops += [op(q) for q in persistent] + [op('file.saveAs', {'path': {'$output': 'changed.fcproj'}})]
        created = execute(create_ops, 'create')
        validate(created, create_ops)
        before = normalized_project(work / 'create/before.fcproj')
        assert normalized_project(work / 'create/preserved.fcproj') == before
        source = work / 'create/changed.fcproj'
        source_digest = digest(source)
        reopen_ops = [op('file.open', {'path': {'$ref': 'original.path'}}), op('sequence.inspect', alias='persisted')]
        reopen_ops += [op(q) for q in persistent] + common + [op('file.saveAs', {'path': {'$output': 'roundtrip.fcproj'}})]
        reopened = execute(reopen_ops, 'reopen', {'original': source})
        validate(reopened, reopen_ops)
        persisted = reopened['steps'][1]['result']
        assert all(track['muted'] and track['solo'] for track in persisted['audio'])
        assert all(not track['enabled'] for track in persisted['video'])
        assert normalized_project(work / 'reopen/roundtrip.fcproj') == before
        assert digest(source) == source_digest
        negatives = []
        for index, identifier in enumerate(tested):
            refused = execute([op(identifier)], 'negative-' + str(index))
            assert refused['result'] == 'FAIL' and len(refused['steps']) == 1, (identifier, refused.get('error'), refused.get('steps'))
            assert refused['steps'][0]['state'] == 'blocked' and 'precondition_failed: ' + identifier + ':' in refused['error'], (identifier, refused.get('error'), refused.get('steps'))
            assert not list((work / ('negative-' + str(index))).glob('*.fcproj'))
            negatives.append({'command': identifier, 'status': 'PASS', 'error': 'precondition_failed',
                              'context': 'empty native session; missing active sequence', 'editingRequestSent': False,
                              'receiptSha256': digest(work / ('negative-' + str(index) + '-receipt.private.json'))})
        rows = next(step['result'] for step in execute([op('command.list')], 'discovery')['steps'])
        binding = {'pluginSha': args.plugin_sha, 'sourceSha': args.source_sha,
                   'runtimeSha256': created['runtimeSha256'],
                   'runtimeVersion': json.loads((skill / 'scripts/runtime.lock.json').read_text())['resolvedVersion'],
                   'platform': 'darwin-arm64', 'mode': mode}
        observations = []
        scopes = {'parameterValidation': 'Exact empty params accepted in actual native context.',
                  'positiveExecution': 'Every target/source/move return identity and all track-flag changes asserted in populated eight-video/eight-audio sequence.',
                  'negativeRejection': 'Actual empty native session reports command disabled; public adapter blocks before editing request.',
                  'reopen': 'All27 commands reexecuted and asserted after reopening changed project; mute/solo/output persist and restore correctly. Targeting is session state, not claimed persisted.',
                  'nonTargetPreservation': 'Whole serialized project equal after paired operations and reopen/restore; only expected save-as project/root names normalized. Original input hash unchanged.'}
        for identifier in tested:
            for dimension, scope in scopes.items():
                observations.append({'command': identifier, 'dimension': dimension, 'status': 'PASS',
                                     'evidence': 'target-observations.json', 'scope': scope})
        matrix = matrix_builder.build(rows, binding, {'binding': binding, 'observations': observations})
        write(work / 'matrix.json', matrix)
        observation = {'binding': binding, 'commands': tested, 'semanticAssertions': len(expectations),
                       'populatedTracks': {'video': 8, 'audio': 8}, 'wholeProjectPreserved': True,
                       'sourceProjectPreserved': True, 'persistentMuteSoloOutputReopened': True,
                       'negativeCases': negatives, 'createReceiptSha256': digest(work / 'create-receipt.private.json'),
                       'reopenReceiptSha256': digest(work / 'reopen-receipt.private.json'),
                       'scope': 'Actual commands through native MCP and signed owned desktop bridge, not GUI mouse/keyboard gestures, rendering or creative acceptance.'}
        write(work / 'target-observations.json', observation)
        modes.append({'mode': mode, 'result': 'PASS', 'commands': 27, 'negativeCases': 27,
                      'matrixSha256': digest(work / 'matrix.json'), 'observationsSha256': digest(work / 'target-observations.json')})
        print(mode, 'PASS27 commands/create+reopen+disabled contexts', flush=True)
    write(root / 'report.json', {'schema': 'filmcraft-target-command-contexts/v1', 'result': 'PASS',
                                'driverSha256': digest(Path(__file__)), 'results': modes,
                                'fullCommandAcceptance': 'NOT_PROVEN', 'remainingTask': '8.3'})


if __name__ == '__main__':
    main()
