#!/usr/bin/env python3
"""固定安装的时间线编辑、音量和导航双上下文验收；不替代完整666命令资格。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

TICKS = 254016000000
FRAME = TICKS // 24


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def op(command, params=None, alias=None):
    value = {'command': command, 'params': params or {}}
    if alias:
        value['as'] = alias
    return value


def view(sequence):
    value = copy.deepcopy(sequence)
    # 两个会话字段有单独精确断言；其余序列字段均保持逐项比较。
    value.pop('playhead', None)
    value.pop('selection', None)
    return value


def project(path):
    value = json.loads(path.read_text())
    value['project']['name'] = 'Owned edit'
    value['project']['root']['name'] = 'Owned edit'
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
    commands = load(skill / 'scripts/commands.py', 'fixed_edit_commands')
    desktop = load(skill / 'scripts/desktop_session.py', 'fixed_edit_desktop')
    matrices = load(Path(__file__).with_name('command_evidence.py'), 'edit_evidence')
    reports = []
    for mode in ('headless', 'bridge'):
        work = root / mode
        work.mkdir()
        permissions = commands.load('execution_permissions').from_cli([str(root)], [str(work), str(runtime)])

        def execute(operations, label, inputs=None):
            plan = {'schema': 'craft-command-plan/v1', 'operations': operations}
            write(work / (label + '-plan.private.json'), plan)
            output = work / label
            if mode == 'headless':
                receipt = commands.execute(plan, output, runtime_home=runtime, permissions=permissions, inputs=inputs)
            else:
                receipt = desktop.run(plan, output, runtime_home=runtime, permissions=permissions, inputs=inputs)
                proof = json.loads((output / 'desktop-session.json').read_text())
                assert proof['ownedProcessesStopped'] and proof['listenerOwnedByPID'] and proof['sessionsStarted'] == 1
            write(work / (label + '-receipt.private.json'), receipt)
            return receipt

        fixture = [op('file.newProject', {'name': 'Owned edit'}),
                   op('file.newSequence', {'name': 'Owned edit', 'width': 32, 'height': 32, 'fps': 24, 'video': 3, 'audio': 2}),
                   op('file.newColorMatte', {'color': '#e65527', 'seconds': 20}, 'matte')]
        for n in range(3):
            fixture.append(op('timeline.place', {'item': {'$ref': 'matte.item'}, 'track': 'V1',
                'time': 2 * n * TICKS, 'sourceIn': 2 * TICKS, 'duration': 2 * TICKS, 'insert': False}))
        fixture += [op('timeline.place', {'item': {'$ref': 'matte.item'}, 'track': 'V2',
            'time': 8 * TICKS, 'sourceIn': 4 * TICKS, 'duration': 2 * TICKS, 'insert': False}),
            op('file.newBarsAndTone', {'seconds': 4}, 'tone'),
            op('timeline.place', {'item': {'$ref': 'tone.item'}, 'track': 'V3', 'audioTrack': 'A1',
                'time': 12 * TICKS, 'duration': 2 * TICKS, 'insert': False}),
            op('sequence.inspect'), op('file.saveAs', {'path': {'$output': 'baseline.fcproj'}})]
        made = execute(fixture, 'fixture')
        assert made['result'] == 'PASS', made.get('error')
        baseline = made['steps'][-2]['result']
        original = work / 'fixture/baseline.fcproj'
        original_hash = digest(original)
        baseline_project = project(original)
        isolated = baseline['video'][1]['items'][0]['clip']
        middle = baseline['video'][0]['items'][1]['clip']
        audio = baseline['audio'][0]['items'][0]['clip']
        cases = []

        def changed(kind, amount):
            expected = copy.deepcopy(baseline)
            item = expected['video'][1]['items'][0]
            if kind == 'nudge':
                item['start'] += amount * FRAME
                item['startFrame'] += amount
            elif kind == 'track':
                expected['video'][1]['items'].clear()
                expected['video'][amount]['items'].append(item)
                expected['video'][amount]['items'].sort(key=lambda clip: clip['start'])
            elif kind == 'slip':
                item['sourceIn'] += amount * FRAME
            elif kind == 'slide':
                left, mid, right = expected['video'][0]['items']
                left['duration'] += amount * FRAME
                left['durationFrames'] += amount
                mid['start'] += amount * FRAME
                mid['startFrame'] += amount
                right['start'] += amount * FRAME
                right['startFrame'] += amount
                right['sourceIn'] += amount * FRAME
                right['duration'] -= amount * FRAME
                right['durationFrames'] -= amount
            else:
                volume = next(effect for effect in expected['audio'][0]['items'][0]['effects'] if effect['effect'] == 'volume')
                volume['params']['level']['value'] = 'Float(' + str(float(amount)) + ')'
            return expected

        for suffix, amount in [('Left', -1), ('Right', 1), ('Left5', -5), ('Right5', 5)]:
            cases.append(('timeline.nudge' + suffix, {}, isolated, changed('nudge', amount)))
        for suffix, destination in [('Up', 2), ('Down', 0)]:
            cases.append(('timeline.nudge' + suffix, {}, isolated, changed('track', destination)))
        for suffix, amount in [('Left', 1), ('Right', -1), ('Left5', 5), ('Right5', -5)]:
            cases.append(('timeline.slip' + suffix, {}, isolated, changed('slip', amount)))
        for suffix, amount in [('Left', -1), ('Right', 1), ('Left5', -5), ('Right5', 5)]:
            cases.append(('timeline.slide' + suffix, {}, middle, changed('slide', amount)))
        cases += [('timeline.slip', {'clip': isolated, 'deltaFrames': 3}, isolated, changed('slip', 3)),
                  ('timeline.slide', {'clip': middle, 'deltaFrames': 2}, middle, changed('slide', 2))]
        for name, amount in [('volumeUp', 1), ('volumeDown', -1), ('volumeUpMany', 6), ('volumeDownMany', -6),
                             ('nudgeVolumeUp1', 1), ('nudgeVolumeUp3', 3), ('nudgeVolumeDown1', -1), ('nudgeVolumeDown3', -3)]:
            cases.append(('clip.' + name, {}, audio, changed('volume', amount)))
        navigation = [('playhead.set', {'frame': 60}, 60), ('playhead.step', {'frames': -7}, 53),
                      ('playhead.stepForward', {}, 61), ('playhead.stepBack', {}, 59),
                      ('playhead.stepForward5', {}, 65), ('playhead.stepBack5', {}, 55),
                      ('playhead.nextEdit', {}, 96), ('playhead.prevEdit', {}, 48),
                      ('playhead.nextEditAnyTrack', {}, 96), ('playhead.prevEditAnyTrack', {}, 48),
                      ('playhead.start', {}, 0), ('playhead.end', {}, 336),
                      ('playhead.selectedClipStart', {}, 48), ('playhead.selectedClipEnd', {}, 95)]
        select = [('timeline.select', {'clips': [isolated], 'add': False, 'toggle': False}, isolated),
                  ('timeline.selectClipAtPlayhead', {}, middle),
                  ('timeline.selectNextClip', {}, baseline['video'][0]['items'][2]['clip']),
                  ('timeline.selectPrevClip', {}, baseline['video'][0]['items'][0]['clip'])]
        tested = [case[0] for case in cases + navigation + select] + ['edit.undo', 'edit.redo']
        assert len(tested) == len(set(tested)) == 44
        expectations = {}

        def inspect(alias, expected, state=None):
            expectations[alias] = (expected, state)
            return op('sequence.inspect', alias=alias)

        def select_clip(clip):
            return op('timeline.select', {'clips': [clip], 'add': False, 'toggle': False})

        def suite():
            operations = []
            for index, (identifier, params, clip, expected) in enumerate(cases):
                label = 'edit_' + str(index)
                operations += [select_clip(clip), op(identifier, params), inspect(label, expected),
                    op('edit.undo'), inspect(label + '_undo', baseline), op('edit.redo'),
                    inspect(label + '_redo', expected), op('edit.undo'), inspect(label + '_restored', baseline)]
            for index, (identifier, params, frame) in enumerate(navigation):
                operations += [select_clip(middle), op('playhead.set', {'frame': 60}), op(identifier, params),
                    inspect('navigation_' + str(index), baseline, ('playhead', frame * FRAME))]
            for index, (identifier, params, clip) in enumerate(select):
                operations += [select_clip(middle), op('playhead.set', {'frame': 60}), op(identifier, params),
                    inspect('selection_' + str(index), baseline, ('selection', [clip]))]
            return operations

        def validate(receipt, operations):
            assert receipt['result'] == 'PASS', receipt.get('error')
            assert len(receipt['steps']) == len(operations) and all(step['state'] == 'succeeded' for step in receipt['steps'])
            values = {operation['as']: step['result'] for operation, step in zip(operations, receipt['steps']) if operation.get('as')}
            for alias, (expected, state) in expectations.items():
                actual = values[alias]
                assert view(actual) == view(expected), (mode, alias, 'sequence mismatch')
                if state:
                    assert actual[state[0]] == state[1], (mode, alias, state, actual[state[0]])

        operations = [op('file.open', {'path': {'$ref': 'original.path'}})] + suite()
        operations += [op('file.saveAs', {'path': {'$output': 'preserved.fcproj'}}), select_clip(isolated),
            op('timeline.nudgeRight'), select_clip(audio), op('clip.volumeUp'),
            op('file.saveAs', {'path': {'$output': 'changed.fcproj'}})]
        edited = execute(operations, 'edit', {'original': original})
        validate(edited, operations)
        assert project(work / 'edit/preserved.fcproj') == baseline_project and digest(original) == original_hash
        source = work / 'edit/changed.fcproj'
        source_hash = digest(source)
        expected_persisted = changed('nudge', 1)
        expected_persisted['audio'] = changed('volume', 1)['audio']
        revision_ops = [op('file.open', {'path': {'$ref': 'original.path'}}), inspect('persisted', expected_persisted),
            select_clip(isolated), op('timeline.nudgeLeft'), select_clip(audio), op('clip.volumeDown')] + suite()
        revision_ops += [op('file.saveAs', {'path': {'$output': 'restored.fcproj'}})]
        revised = execute(revision_ops, 'revision', {'original': source})
        validate(revised, revision_ops)
        assert project(work / 'revision/restored.fcproj') == baseline_project
        assert digest(source) == source_hash and digest(original) == original_hash
        negatives = []
        parameters = {case[0]: case[1] for case in cases + navigation + select}
        batch_module = load(Path(__file__).with_name('owned_empty_batch.py'), 'owned_empty_batch')
        with batch_module.EmptyBatch(commands, desktop, mode, work, runtime, permissions) as batch:
            for index, identifier in enumerate(tested):
                plan = {'schema': 'craft-command-plan/v1', 'operations': [op(identifier, parameters.get(identifier, {}))]}
                write(work / ('negative-' + str(index) + '-plan.private.json'), plan)
                refused = batch.execute(plan, work / ('negative-' + str(index)))
                write(work / ('negative-' + str(index) + '-receipt.private.json'), refused)
                assert refused['result'] == 'FAIL' and len(refused['steps']) == 1, (identifier, refused.get('error'))
                assert refused['steps'][0]['state'] == 'blocked' and refused['error'].startswith('precondition_failed: '), (identifier, refused.get('error'))
                negatives.append({'command': identifier, 'result': 'PASS', 'error': 'precondition_failed',
                                  'editingRequestSent': False, 'receiptSha256': digest(work / ('negative-' + str(index) + '-receipt.private.json'))})
                if (index + 1) % 10 == 0:
                    print(mode, 'negative contexts', index + 1, '/', len(tested), flush=True)
        found = execute([op('command.list')], 'discovery')
        assert found['result'] == 'PASS'
        rows = found['steps'][0]['result']
        binding = {'pluginSha': args.plugin_sha, 'sourceSha': args.source_sha,
                   'runtimeSha256': edited['runtimeSha256'], 'runtimeVersion': '0.2.0-craft.5',
                   'platform': 'darwin-arm64', 'mode': mode}
        scope = {'parameterValidation': 'Declared literal valid params accepted in actual native execution; not exhaustive invalid-type coverage.',
                 'positiveExecution': 'Exact tick/frame navigation, target identity, slip/slide geometry, track transfer and dB values asserted; all non-target sequence fields compared.',
                 'negativeRejection': 'Actual empty native session reports disabled; public adapter blocks before command_run.',
                 'reopen': 'Saved nudge+volume changes persist; explicit scoped reverse revision and all44 command behaviors repeated after reopen.',
                 'nonTargetPreservation': 'Full sequence compared after every mutation/undo/redo; whole serialized project restored, original inputs hashed unchanged. Only save-as project/root names normalized.'}
        observations = [{'command': identifier, 'dimension': dimension, 'status': 'PASS',
                         'evidence': 'edit-observations.json', 'scope': text}
                        for identifier in tested for dimension, text in scope.items()]
        matrix = matrices.build(rows, binding, {'binding': binding, 'observations': observations})
        write(work / 'matrix.json', matrix)
        observation = {'binding': binding, 'commands': tested, 'sequenceAssertionsPerFinalPhase': len(expectations),
                       'mutatingCommands': 24, 'navigationCommands': 14, 'selectionCommands': 4,
                       'undoRedoVerified': True, 'originalProjectSha256': original_hash, 'changedProjectSha256': source_hash,
                       'originalAndChangedInputsPreserved': True, 'wholeProjectRestored': True,
                       'negativeContexts': negatives, 'receipts': {label: digest(work / (label + '-receipt.private.json')) for label in ('fixture', 'edit', 'revision')},
                       'artifacts': {name: digest(work / name) for name in ('fixture/baseline.fcproj', 'edit/preserved.fcproj', 'edit/changed.fcproj', 'revision/restored.fcproj')},
                       'scope': 'Actual native headless and owned signed desktop bridge; no GUI gestures, media decode/render, creative or full666 qualification.'}
        write(work / 'edit-observations.json', observation)
        reports.append({'mode': mode, 'result': 'PASS', 'commands': 44, 'negativeContexts': 44,
                        'matrixSha256': digest(work / 'matrix.json'), 'observationsSha256': digest(work / 'edit-observations.json')})
        print(mode, 'PASS44 edit/navigation/selection/undo-redo commands', flush=True)
    write(root / 'report.json', {'schema': 'filmcraft-installed-timeline-edit-audit/v1', 'result': 'PASS',
                                'driverSha256': digest(Path(__file__)), 'results': reports,
                                'remainingTask': '8.3', 'fullCommandAcceptance': 'NOT_PROVEN'})


if __name__ == '__main__':
    main()
