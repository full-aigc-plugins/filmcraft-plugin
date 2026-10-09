#!/usr/bin/env python3
"""固定安装十五条片段属性命令的完整工程／重开／共享会话验收。"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def normalized_project(value):
    result = copy.deepcopy(value)
    result['project']['name'] = 'Owned properties'
    result['project']['root']['name'] = 'Owned properties'
    return result


def assert_project(actual, expected):
    """仅消除已知saveAs工程名称；整个工程和所有未修改字段必须相等。"""
    assert normalized_project(actual) == normalized_project(expected), 'complete project mismatch'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('installed-plugin', 'runtime-home', 'timeline-audit', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--plugin-sha', required=True); parser.add_argument('--source-sha', required=True)
    args = parser.parse_args()
    root = args.output.resolve(); root.mkdir(mode=0o700)
    audit = args.timeline_audit.resolve(strict=True); runtime = args.runtime_home.resolve(strict=True)
    scripts = args.installed_plugin.resolve(strict=True) / 'skills/filmcraft-use/scripts'
    commands = load(scripts / 'commands.py', 'property_commands'); desktop = load(scripts / 'desktop_session.py', 'property_desktop')
    helper = load(Path(__file__).with_name('verify_installed_timeline_edits.py'), 'property_helper')
    owner_path = Path(__file__).with_name('owned_empty_batch.py'); owner_hash = helper.digest(owner_path)
    shared = load(owner_path, 'property_shared'); matrix_builder = load(Path(__file__).with_name('command_evidence.py'), 'property_matrix')
    op, write, sha = helper.op, helper.write, helper.digest
    results = []
    for mode in ('headless', 'bridge'):
        work = root / mode; work.mkdir()
        source = audit / mode / 'fixture/baseline.fcproj'; source_hash = sha(source)
        base = json.loads(source.read_text())
        snapshot = json.loads((audit / mode / 'fixture-receipt.private.json').read_text())['steps'][-2]['result']
        seq_id = str(snapshot['id']); next_id = base['project']['next_id']
        target = snapshot['video'][1]['items'][0]['clip']; audio = snapshot['audio'][0]['items'][0]['clip']
        linked_video = snapshot['video'][2]['items'][0]['clip']; pair = [item['clip'] for item in snapshot['video'][0]['items'][:2]]
        def item(project, clip):
            q = project['project']['items'][seq_id]['kind']['Sequence']
            return next(i for track in q['video_tracks'] + q['audio_tracks'] for i in track['items'] if i['id'] == clip)
        def patch(clip=target, **fields):
            value = copy.deepcopy(base); item(value, clip).update(fields); return value
        def select(clips): return op('timeline.select', {'clips': clips, 'add': False, 'toggle': False})
        grouped = copy.deepcopy(base)
        for clip in pair: item(grouped, clip)['group'] = next_id
        grouped['project']['next_id'] += 1
        ungrouped = copy.deepcopy(grouped)
        for clip in pair: item(ungrouped, clip)['group'] = None
        unlinked = copy.deepcopy(base)
        for clip in (audio, linked_video): item(unlinked, clip)['link'] = None
        speed = patch(speed=2.0, reverse=True, duration=item(base, target)['duration'] // 2, time_interpolation='opticalFlow')
        cases = [
            ('clip.rename', {'clip': target, 'name': 'Revised clip'}, patch(name='Revised clip'), [target], None),
            ('clip.speedDuration', {'clips': [target], 'speed': 200, 'reverse': True, 'ripple': False, 'interpolation': 'opticalFlow'}, speed, [target], None),
            ('clip.enable', {'clips': [target]}, patch(enabled=False), [target], None),
            ('clip.frameHoldOptions', {'clips': [target], 'enabled': True, 'holdOn': 'in', 'holdFilters': True}, patch(frame_hold=item(base, target)['source_in'], hold_filters=True), [target], None),
            ('clip.frameHold', {'clips': [target], 'time': item(base, target)['start']}, patch(frame_hold=item(base, target)['source_in']), [target], None),
            ('clip.fieldOptions', {'clips': [target], 'processing': 'alwaysDeinterlace', 'reverseFieldDominance': True}, patch(field_options={'processing': 'alwaysDeinterlace', 'reverseFieldDominance': True}), [target], None),
            ('clip.timeInterpolation.frameSampling', {'clips': [target]}, base, [target], op('clip.timeInterpolation.frameBlending', {'clips': [target]})),
            ('clip.timeInterpolation.frameBlending', {'clips': [target]}, patch(time_interpolation='frameBlending'), [target], None),
            ('clip.timeInterpolation.opticalFlow', {'clips': [target]}, patch(time_interpolation='opticalFlow'), [target], None),
            ('clip.setTimeInterpolation', {'clips': [target], 'mode': 'frameBlending'}, patch(time_interpolation='frameBlending'), [target], None),
            ('clip.audioGain', {'mode': 'set', 'db': -3}, patch(audio, gain_db=-3.0), [audio], None),
            ('clip.scaleToFrameSize', {}, patch(scale_to_frame=True), [target], None),
            ('clip.group', {}, grouped, pair, None),
            ('clip.ungroup', {}, ungrouped, pair, op('clip.group')),
            ('clip.link', {'clips': [linked_video, audio]}, unlinked, [linked_video, audio], None),
        ]
        expectations = {}; counts = []
        policy = commands.load('execution_permissions').from_cli([str(root), str(audit)], [str(work), str(runtime)])
        with shared.OwnedBatch(commands, desktop, mode, work, runtime, policy, protected_paths=[audit]) as session:
            def execute(operations, phase, inputs=None, refusal=False):
                plan = {'schema': 'craft-command-plan/v1', 'operations': operations}; write(work / (phase + '-plan.private.json'), plan)
                receipt = session.execute(plan, work / phase, inputs=inputs, expect_refusal=refusal)
                write(work / (phase + '-receipt.private.json'), receipt); return receipt
            def suite():
                operations = []; expected = {}
                def capture(value):
                    name = 'check_' + str(len(expected)) + '.fcproj'
                    operations.append(op('file.saveAs', {'path': {'$output': name}})); expected[name] = copy.deepcopy(value)
                for identifier, params, after, clips, setup in cases:
                    operations.append(select(clips)); before = base
                    if setup:
                        operations.append(setup)
                        before = grouped if identifier == 'clip.ungroup' else patch(time_interpolation='frameBlending')
                    operations.append(op(identifier, params)); capture(after)
                    operations.append(op('edit.undo')); capture(before)
                    operations.append(op('edit.redo')); capture(after)
                    operations.append(op('edit.undo')); capture(before)
                    if setup: operations.append(op('edit.undo'))
                    capture(base)
                return operations, expected
            def validate(phase, expected):
                for name, value in expected.items():
                    try: assert_project(json.loads((work / phase / name).read_text()), value)
                    except AssertionError as error: raise AssertionError((mode, phase, name, str(error))) from error
                counts.append({'phase': phase, 'fullProjectComparisons': len(expected)})
            def export(name):
                return op('file.exportMedia', {'path': {'$output': name + '.wav'}, 'format': 'wav',
                    'range': 'custom', 'startSeconds': 12, 'endSeconds': 12.25, 'wait': True})
            persistent = [select([target]), op('clip.rename', {'clip': target, 'name': 'Revised clip'}),
                op('clip.speedDuration', {'clips': [target], 'speed': 200, 'reverse': True, 'ripple': False, 'interpolation': 'opticalFlow'}),
                op('clip.enable', {'clips': [target]}), op('clip.frameHoldOptions', {'clips': [target], 'enabled': True, 'holdOn': 'in', 'holdFilters': True}),
                op('clip.fieldOptions', {'clips': [target], 'processing': 'alwaysDeinterlace', 'reverseFieldDominance': True}),
                op('clip.scaleToFrameSize'), select([audio]), op('clip.audioGain', {'mode': 'set', 'db': -3})]
            operations, expected = suite()
            first = execute([op('file.open', {'path': {'$ref': 'original.path'}}), export('baseline')] + operations +
                [op('file.saveAs', {'path': {'$output': 'preserved.fcproj'}})] + persistent +
                [export('gain'), op('file.saveAs', {'path': {'$output': 'changed.fcproj'}})], 'create', {'original': source})
            validate('create', expected); assert_project(json.loads((work / 'create/preserved.fcproj').read_text()), base)
            changed = work / 'create/changed.fcproj'; changed_hash = sha(changed)
            persisted = copy.deepcopy(speed)
            item(persisted, target).update(name='Revised clip', enabled=False,
                frame_hold=item(base, target)['source_in'] + item(base, target)['duration'] - helper.FRAME, hold_filters=True,
                field_options={'processing': 'alwaysDeinterlace', 'reverseFieldDominance': True}, scale_to_frame=True)
            item(persisted, audio)['gain_db'] = -3.0
            assert_project(json.loads(changed.read_text()), persisted)
            session.reset(work / 'reset-revision')
            restore = [select([target]), op('clip.rename', {'clip': target, 'name': item(base, target)['name']}),
                op('clip.speedDuration', {'clips': [target], 'speed': 100, 'reverse': False, 'ripple': False, 'interpolation': 'frameSampling'}),
                op('clip.enable', {'clips': [target]}), op('clip.frameHoldOptions', {'clips': [target], 'enabled': False, 'holdOn': 'in'}),
                op('clip.fieldOptions', {'clips': [target], 'processing': 'none', 'reverseFieldDominance': False}), op('clip.scaleToFrameSize'),
                select([audio]), op('clip.audioGain', {'mode': 'set', 'db': 0})]
            operations, expected = suite()
            execute([op('file.open', {'path': {'$ref': 'original.path'}}), op('file.saveAs', {'path': {'$output': 'reopened.fcproj'}})] + restore + operations +
                [export('restored'), op('file.saveAs', {'path': {'$output': 'restored.fcproj'}})], 'revision', {'original': changed})
            assert_project(json.loads((work / 'revision/reopened.fcproj').read_text()), persisted)
            validate('revision', expected); assert_project(json.loads((work / 'revision/restored.fcproj').read_text()), base)
            assert sha(source) == source_hash and sha(changed) == changed_hash
            session.reset(work / 'reset-negatives'); negatives = []
            for index, (identifier, params, *_rest) in enumerate(cases):
                invalid = {'schema': 'craft-command-plan/v1', 'operations': [op(identifier, {'UNDEFINED_PROPERTY_FIELD': True})]}
                destination = work / ('invalid-' + str(index))
                try: commands.execute(invalid, destination, runtime_home=runtime, permissions=policy)
                except ValueError as error: assert str(error) == 'invalid_native_parameters'
                else: raise AssertionError('unknown parameter accepted')
                assert not destination.exists()
                row = next(r for r in commands.catalog()['commands'] if r['id'] == identifier)
                if not row['enabledAtEmptySession']: execute([op(identifier, params)], 'negative-' + str(index), refusal=True)
                negatives.append({'command': identifier, 'unknownParameterRejected': True, 'emptyContextBlocked': not row['enabledAtEmptySession']})
            rows = execute([op('command.list')], 'discovery')['steps'][0]['result']
            binding = {'pluginSha': args.plugin_sha, 'sourceSha': args.source_sha, 'runtimeSha256': first['runtimeSha256'],
                'runtimeVersion': '0.2.0-craft.5', 'platform': 'darwin-arm64', 'mode': mode}
            scopes = {'parameterValidation': 'Literal documented params accepted; undefined field rejected before output.',
                'positiveExecution': 'Every serialized project field compared after15 commands and undo/redo; defaults omission, exact duration/source hold, link/group allocator and gain asserted.',
                'negativeRejection': 'All15 unknown-field refusals; actual empty-native disabled commands publicly blocked.',
                'reopen': 'Actual persistent property combination saved and reopened; explicit restore and all15 cases rerun after reopen.',
                'nonTargetPreservation': 'Entire project equal to explicit target-patched expectations at75 checkpoints each phase; after transient edits and final revision exact baseline, original input hashes unchanged.'}
            observations = [{'command': identifier, 'dimension': dimension, 'status': 'PASS', 'evidence': 'observations.json', 'scope': scope}
                for identifier, *_rest in cases for dimension, scope in scopes.items()]
            write(work / 'matrix.json', matrix_builder.build(rows, binding, {'binding': binding, 'observations': observations}))
            write(work / 'observations.json', {'binding': binding, 'commands': [c[0] for c in cases], 'assertions': counts, 'negatives': negatives,
                'sourceProjectSha256': source_hash, 'changedProjectSha256': changed_hash, 'wholeProjectAndInputsPreserved': True,
                'receipts': {name: sha(work / (name + '-receipt.private.json')) for name in ['create', 'revision']},
                'artifacts': {name: sha(work / name) for name in ['create/preserved.fcproj','create/changed.fcproj','revision/reopened.fcproj','revision/restored.fcproj',
                    'create/baseline.wav','create/gain.wav','revision/restored.wav']},
                'renderScope': 'Native WAV outputs generated; independent PCM measurements separate. No moving-video or optical-flow/field-processing algorithm qualification.'})
        proof = json.loads((work / 'owned-batch-session.private.json').read_text())
        assert proof['sessionsStarted'] == 1 and proof['singleProcessIdentity'] and proof['ownedProcessesStopped'] and not proof['tainted']
        if mode == 'bridge': assert proof['desktopStopped'] and proof['listenerOwnedByPID']
        results.append({'mode': mode, 'result': 'PASS', 'commands': len(cases), 'observationsSha256': sha(work / 'observations.json'),
            'matrixSha256': sha(work / 'matrix.json'), 'sessionSha256': sha(work / 'owned-batch-session.private.json')})
        print(mode, 'PASS15 clip properties / complete serialized project', flush=True)
    assert sha(owner_path) == owner_hash
    write(root / 'report.json', {'schema': 'filmcraft-fixed-clip-properties/v1', 'result': 'PASS', 'results': results,
        'driverSha256': sha(Path(__file__)), 'sessionHelperSha256': owner_hash, 'fullCommandAcceptance': 'NOT_PROVEN', 'remainingTask': '8.3'})


if __name__ == '__main__': main()
