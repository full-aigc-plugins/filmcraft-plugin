#!/usr/bin/env python3
"""固定安装的27标记／2序列设置命令，共享所属实例并逐字段验证保存返工。"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def assert_sequence(actual, expected, saved_project=None):
    """固定craft.5查询省略comment；评论必须由真实保存工程独立验证。"""
    actual_view, expected_view = copy.deepcopy(actual), copy.deepcopy(expected)
    for value in (actual_view, expected_view):
        value.pop('playhead', None); value.pop('selection', None)
    for marker in expected_view['markers']: marker.pop('comment')
    assert actual_view == expected_view, 'sequence fields mismatch'
    if expected['markers']:
        assert saved_project is not None, 'serialized marker metadata required'
        markers = saved_project['project']['items'][str(expected['id'])]['kind']['Sequence']['markers']
        assert markers == expected['markers'], 'serialized marker fields mismatch'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('installed-plugin', 'runtime-home', 'timeline-audit', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--plugin-sha', required=True)
    parser.add_argument('--source-sha', required=True)
    args = parser.parse_args()
    root = args.output.resolve(); root.mkdir(mode=0o700)
    audit = args.timeline_audit.resolve(strict=True)
    runtime = args.runtime_home.resolve(strict=True)
    scripts = args.installed_plugin.resolve(strict=True) / 'skills/filmcraft-use/scripts'
    commands = load(scripts / 'commands.py', 'marker_commands')
    desktop = load(scripts / 'desktop_session.py', 'marker_desktop')
    helper = load(Path(__file__).with_name('verify_installed_timeline_edits.py'), 'marker_helper')
    owner_path = Path(__file__).with_name('owned_empty_batch.py')
    shared = load(owner_path, 'marker_shared')
    owner_hash = helper.digest(owner_path)
    matrix_builder = load(Path(__file__).with_name('command_evidence.py'), 'marker_matrix')
    op, write, sha, view = helper.op, helper.write, helper.digest, helper.view
    F = helper.FRAME
    results = []
    for mode in ('headless', 'bridge'):
        work = root / mode; work.mkdir()
        source = audit / mode / 'fixture/baseline.fcproj'
        source_hash = sha(source)
        project = json.loads(source.read_text())
        base = json.loads((audit / mode / 'fixture-receipt.private.json').read_text())['steps'][-2]['result']
        policy = commands.load('execution_permissions').from_cli([str(root), str(audit)], [str(work), str(runtime)])
        tested = set(); assertions = []
        with shared.OwnedBatch(commands, desktop, mode, work, runtime, policy, protected_paths=[audit]) as session:
            def execute(operations, name, inputs=None, refuse=False):
                plan = {'schema': 'craft-command-plan/v1', 'operations': operations}
                write(work / (name + '-plan.private.json'), plan)
                receipt = session.execute(plan, work / name, inputs=inputs, expect_refusal=refuse)
                write(work / (name + '-receipt.private.json'), receipt)
                return receipt

            def suite(next_id):
                operations = []; expected = {}; count = [0]
                def capture(value, playhead=None):
                    alias = 'check_' + str(count[0]); count[0] += 1
                    operations.append(op('sequence.inspect', alias=alias))
                    expected[alias] = (copy.deepcopy(value), playhead)
                    if value['markers']: operations.append(op('file.saveAs', {'path': {'$output': alias + '.fcproj'}}))
                def patched(**fields):
                    value = copy.deepcopy(base); value.update(fields); return value
                def mutation(identifier, params, after, setup=(), before=None):
                    tested.add(identifier); before = before or base
                    operations.extend(setup)
                    operations.append(op(identifier, params))
                    capture(after)
                    operations.append(op('edit.undo')); capture(before)
                    operations.append(op('edit.redo')); capture(after)
                    operations.append(op('edit.undo')); capture(before)
                    operations.extend(op('edit.undo') for _ in setup if _['command'].startswith('markers.'))
                    capture(base)
                def navigation(identifier, frame, setup, before, params=None):
                    tested.add(identifier); operations.extend(setup)
                    operations.extend([op('playhead.set', {'frame': 36}), op(identifier, params)])
                    capture(before, frame * F)
                    operations.extend(op('edit.undo') for _ in setup)
                    capture(base)
                def mark(identifier, frame): return op(identifier, {'time': frame * F, 'target': 'program'})
                marks = [mark('markers.markIn', 24), mark('markers.markOut', 72)]
                marked = patched(**{'in': 24 * F, 'out': 72 * F})
                sides = [('VideoIn', 'videoIn', 24), ('VideoOut', 'videoOut', 72),
                         ('AudioIn', 'audioIn', 36), ('AudioOut', 'audioOut', 84)]
                splits = [mark('markers.markSplit' + suffix, frame) for suffix, _, frame in sides]
                split_state = patched(split={key: frame * F for _, key, frame in sides})
                for identifier, key, frame in [('markers.markIn', 'in', 24), ('markers.markOut', 'out', 72)]:
                    mutation(identifier, {'time': frame * F, 'target': 'program'}, patched(**{key: frame * F}))
                for suffix, key, frame in sides:
                    value = copy.deepcopy(base); value['split'][key] = frame * F
                    mutation('markers.markSplit' + suffix, {'time': frame * F, 'target': 'program'}, value)
                mutation('markers.markClip', {}, patched(**{'in': 48 * F, 'out': 95 * F}),
                         [op('playhead.set', {'frame': 60})])
                selected = [item['clip'] for item in base['video'][0]['items'][:2]]
                mutation('markers.markSelection', {}, patched(**{'in': 0, 'out': 95 * F}),
                         [op('timeline.select', {'clips': selected, 'add': False, 'toggle': False})])
                all_marks = copy.deepcopy(marked); all_marks['split'] = split_state['split']
                for identifier in ('markers.clearIn', 'markers.clearOut', 'markers.clearInOut'):
                    after = copy.deepcopy(all_marks)
                    if identifier != 'markers.clearOut':
                        after['in'] = None; after['split']['videoIn'] = None; after['split']['audioIn'] = None
                    if identifier != 'markers.clearIn':
                        after['out'] = None; after['split']['videoOut'] = None; after['split']['audioOut'] = None
                    mutation(identifier, {}, after, marks + splits, all_marks)
                def marker(identifier=next_id, frame=24, duration=0, kind='Comment', name='Owned marker', comment='Owned comment', color='Green'):
                    return {'id': identifier, 'start': frame * F, 'duration': duration * F,
                            'kind': kind, 'name': name, 'comment': comment, 'color': color}
                for identifier, kind, duration in [('markers.add', 'Comment', 3), ('markers.addRange', 'Comment', 6),
                        ('markers.addChapter', 'Chapter', 0), ('markers.addFlashCue', 'FlashCue', 0)]:
                    params = {'time': 24 * F, 'name': 'Owned marker', 'comment': 'Owned comment', 'color': 'Green'}
                    if kind == 'Comment': params['durationFrames'] = duration
                    mutation(identifier, params, patched(markers=[marker(duration=duration, kind=kind)]))
                mutation('markers.addRangeInOut', {'name': 'Owned marker', 'comment': 'Owned comment', 'color': 'Green'},
                         dict(copy.deepcopy(marked), markers=[marker(duration=49)]), marks, marked)
                seed = op('markers.add', {'time': 24 * F, 'name': 'Owned marker', 'comment': 'Owned comment', 'color': 'Green'})
                seeded = patched(markers=[marker()])
                mutation('markers.edit', {'marker': next_id, 'name': 'Revised marker', 'comment': 'Revised comment', 'color': 'Rose', 'durationFrames': 7},
                         patched(markers=[marker(duration=7, name='Revised marker', comment='Revised comment', color='Rose')]), [seed], seeded)
                mutation('markers.clearCurrent', {}, base, [seed, op('playhead.set', {'frame': 24})], seeded)
                mutation('markers.clearAll', {}, base, [seed], seeded)
                for identifier, frame in [('markers.goToIn', 24), ('markers.goToOut', 72)]:
                    navigation(identifier, frame, marks, marked)
                for suffix, _, frame in sides:
                    navigation('markers.goToSplit' + suffix, frame, splits, split_state, {'target': 'program'})
                marker_setup = [op('markers.add', {'time': n * F, 'name': 'Owned marker', 'comment': 'Owned comment', 'color': 'Green'}) for n in (24, 48, 72)]
                marker_state = patched(markers=[marker(identifier=next_id + i, frame=n) for i, n in enumerate((24, 48, 72))])
                navigation('markers.goNext', 48, marker_setup, marker_state)
                navigation('markers.goPrev', 24, marker_setup, marker_state)
                settings = copy.deepcopy(base); settings['name'] = 'Changed sequence'
                settings['settings'].update(width=64, height=48, sample_rate=44100, audio_master='Mono')
                mutation('sequence.settings', {'name': 'Changed sequence', 'width': 64, 'height': 48, 'fps': 24, 'sampleRate': 44100, 'mix': 'Mono'}, settings)
                colored = copy.deepcopy(base); colored['settings']['color'] = {'working': 'Rec2100Pq', 'wide_gamut': True, 'auto_tone_map': False}
                colored['settings']['working_space'] = 'Rec. 2100 PQ'
                mutation('sequence.colorSettings', {'workingSpace': 'rec2100-pq', 'wideGamut': True, 'autoToneMap': False}, colored)
                return operations, expected

            def validate(receipt, expected, phase):
                operations = json.loads((work / (phase + '-plan.private.json')).read_text())['operations']
                checked = 0
                for operation, step in zip(operations, receipt['steps']):
                    if operation.get('as') in expected:
                        value, playhead = expected[operation['as']]
                        serialized = json.loads((work / phase / (operation['as'] + '.fcproj')).read_text()) if value['markers'] else None
                        try: assert_sequence(step['result'], value, serialized)
                        except AssertionError as error: raise AssertionError((mode, phase, operation['as'], str(error))) from error
                        if playhead is not None: assert step['result']['playhead'] == playhead
                        checked += 1
                assert checked == len(expected)
                assertions.append({'phase': phase, 'fullSequenceComparisons': checked})

            operations, expected = suite(project['project']['next_id'])
            persistent = [op('markers.add', {'time': 5 * helper.TICKS, 'name': 'Persistent marker', 'comment': 'Kept', 'color': 'Green', 'durationFrames': 3}),
                          op('markers.markIn', {'time': 24 * F, 'target': 'program'}), op('markers.markOut', {'time': 72 * F, 'target': 'program'}),
                          op('sequence.settings', {'width': 64, 'height': 48, 'name': 'Changed sequence', 'sampleRate': 44100, 'mix': 'Mono'}),
                          op('sequence.colorSettings', {'workingSpace': 'rec2100-pq', 'wideGamut': True, 'autoToneMap': False}), op('sequence.inspect', alias='persisted')]
            first = execute([op('file.open', {'path': {'$ref': 'original.path'}})] + operations +
                [op('file.saveAs', {'path': {'$output': 'preserved.fcproj'}})] + persistent +
                [op('file.saveAs', {'path': {'$output': 'changed.fcproj'}})], 'create', {'original': source})
            validate(first, expected, 'create')
            assert helper.project(work / 'create/preserved.fcproj') == helper.project(source)
            changed = work / 'create/changed.fcproj'; changed_hash = sha(changed)
            persisted = first['steps'][-2]['result']
            persisted_expected = copy.deepcopy(base); persisted_expected['name'] = 'Changed sequence'
            persisted_expected['settings'].update(width=64, height=48, sample_rate=44100, audio_master='Mono', working_space='Rec. 2100 PQ',
                color={'working': 'Rec2100Pq', 'wide_gamut': True, 'auto_tone_map': False})
            persisted_expected.update({'in': 24 * F, 'out': 72 * F, 'markers': [{'id': project['project']['next_id'], 'start': 5 * helper.TICKS,
                'duration': 3 * F, 'kind': 'Comment', 'name': 'Persistent marker', 'comment': 'Kept', 'color': 'Green'}]})
            assert_sequence(persisted, persisted_expected, json.loads(changed.read_text()))
            changed_expected = helper.project(source)
            seq_item = changed_expected['project']['items'][str(base['id'])]
            seq_item['name'] = persisted_expected['name']
            q = seq_item['kind']['Sequence']; q['settings'] = persisted_expected['settings']; q['markers'] = persisted_expected['markers']
            q['mark_in'] = persisted_expected['in']; q['mark_out'] = persisted_expected['out']
            changed_expected['project']['next_id'] += 1
            assert helper.project(changed) == changed_expected
            session.reset(work / 'reset-revision')
            operations, expected = suite(project['project']['next_id'] + 1)
            restore = [op('markers.clearAll'), op('markers.clearInOut'),
                       op('sequence.settings', {'width': 32, 'height': 32, 'name': base['name'], 'sampleRate': 48000, 'mix': 'Stereo'}),
                       op('sequence.colorSettings', {'workingSpace': 'rec709', 'wideGamut': False, 'autoToneMap': True})]
            revised = execute([op('file.open', {'path': {'$ref': 'original.path'}}), op('sequence.inspect', alias='reopened')] + restore + operations +
                              [op('file.saveAs', {'path': {'$output': 'restored.fcproj'}})], 'revision', {'original': changed})
            assert_sequence(revised['steps'][1]['result'], persisted_expected, json.loads(changed.read_text()))
            validate(revised, expected, 'revision')
            whole_expected = helper.project(source); whole_expected['project']['next_id'] += 1
            assert helper.project(work / 'revision/restored.fcproj') == whole_expected
            assert sha(source) == source_hash and sha(changed) == changed_hash
            session.reset(work / 'reset-negatives')
            negatives = []
            for index, identifier in enumerate(sorted(tested)):
                invalid = {'schema': 'craft-command-plan/v1', 'operations': [op(identifier, {'UNDEFINED_MARKER_FIELD': True})]}
                destination = work / ('invalid-' + str(index))
                try: commands.execute(invalid, destination, runtime_home=runtime, permissions=policy)
                except ValueError as error: assert str(error) == 'invalid_native_parameters', (identifier, str(error))
                else: raise AssertionError('undefined parameter accepted: ' + identifier)
                assert not destination.exists()
                row = next(r for r in commands.catalog()['commands'] if r['id'] == identifier)
                if not row['enabledAtEmptySession']:
                    execute([op(identifier, {'marker': 16} if identifier == 'markers.edit' else {})], 'negative-' + str(index), refuse=True)
                negatives.append({'command': identifier, 'unknownParameterRejectedBeforeOutput': True,
                                  'emptyContextBlocked': not row['enabledAtEmptySession']})
            discovery = execute([op('command.list')], 'discovery')
            rows = discovery['steps'][0]['result']
            binding = {'pluginSha': args.plugin_sha, 'sourceSha': args.source_sha, 'runtimeSha256': first['runtimeSha256'],
                       'runtimeVersion': '0.2.0-craft.5', 'platform': 'darwin-arm64', 'mode': mode}
            scopes = {'parameterValidation': 'Literal documented program-target params pass; undefined field refused before output/native install.',
                      'positiveExecution': 'Full persistent sequence fields compared after29 commands; transient selection/playhead excluded except exact navigation. Frozen inspect omits comment; all nonempty marker snapshots independently saved and serialized metadata compared.',
                      'negativeRejection': 'All29 undefined-field refusals; commands disabled in empty native context also publicly blocked.',
                      'reopen': 'All29 re-executed after actual saved project reopen and explicit local revision; persisted marker/in-out/settings asserted.',
                      'nonTargetPreservation': 'Whole sequence after each change/undo/redo; whole project preserved before durable edit. Final explicit revision differs only by declared one-step ID allocator advancement; source hashes unchanged.'}
            observations = [{'command': command, 'dimension': dimension, 'status': 'PASS', 'evidence': 'observations.json', 'scope': scope}
                            for command in sorted(tested) for dimension, scope in scopes.items()]
            matrix = matrix_builder.build(rows, binding, {'binding': binding, 'observations': observations}); write(work / 'matrix.json', matrix)
            write(work / 'observations.json', {'binding': binding, 'commands': sorted(tested), 'assertions': assertions,
                'negatives': negatives, 'sourceProjectSha256': source_hash, 'changedProjectSha256': changed_hash,
                'sourceInputsPreserved': True, 'transientSuiteWholeProjectPreserved': True, 'declaredFinalAllocatorAdvance': 1,
                'finalProjectOtherwiseExactBaseline': True, 'receipts': {name: sha(work / (name + '-receipt.private.json')) for name in ['create', 'revision']},
                'artifacts': {name: sha(work / name) for name in ['create/preserved.fcproj', 'create/changed.fcproj', 'revision/restored.fcproj']}})
        proof = json.loads((work / 'owned-batch-session.private.json').read_text())
        assert proof['sessionsStarted'] == 1 and proof['singleProcessIdentity'] and proof['ownedProcessesStopped'] and not proof['tainted']
        if mode == 'bridge': assert proof['desktopStopped'] and proof['listenerOwnedByPID']
        assert len(tested) == 29
        results.append({'mode': mode, 'result': 'PASS', 'commands': len(tested), 'matrixSha256': sha(work / 'matrix.json'),
            'observationsSha256': sha(work / 'observations.json'), 'sessionSha256': sha(work / 'owned-batch-session.private.json')})
        print(mode, 'PASS29 markers/settings', flush=True)
    assert sha(owner_path) == owner_hash
    write(root / 'report.json', {'schema': 'filmcraft-fixed-markers-settings-audit/v1', 'result': 'PASS', 'results': results,
        'driverSha256': sha(Path(__file__)), 'sessionHelperSha256': owner_hash, 'fullCommandAcceptance': 'NOT_PROVEN', 'remainingTask': '8.3'})


if __name__ == '__main__': main()
