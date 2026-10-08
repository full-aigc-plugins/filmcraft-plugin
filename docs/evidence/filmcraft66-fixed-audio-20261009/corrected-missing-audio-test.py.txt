"""实际无音轨输出必须失败并保留原生诊断交付。"""
import importlib.util
import array
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get('CRAFT_MISSING_AUDIO_FIRST_USE') == '1', 'requires public runtime and ffmpeg')
class MissingAudioFirstUseTests(unittest.TestCase):
    def test_required_audio_failure_preserves_movie_project_and_input(self):
        source = Path(os.environ.get('CRAFT_INSTALLED_MISSING_AUDIO_SKILL_ROOT', ROOT / 'skills/filmcraft-cli-audio'))
        with tempfile.TemporaryDirectory(prefix='filmcraft-missing-audio-') as temporary:
            root = Path(temporary)
            skill = root / '.agents/skills/filmcraft-cli-audio'
            shutil.copytree(source, skill, ignore=shutil.ignore_patterns('__pycache__'))
            spec = importlib.util.spec_from_file_location('missing_audio_workflow', skill / 'scripts/workflow.py')
            workflow = importlib.util.module_from_spec(spec); spec.loader.exec_module(workflow)
            skill_hashes = {str(p.relative_to(skill)): workflow.sha(p) for p in skill.rglob('*') if p.is_file()}
            shot = root / 'silent-shot.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=red:s=320x180:r=12:d=1', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(shot)], check=True)
            source_sha = workflow.sha(shot)
            plan = {'document': {'name': 'Missing audio', 'width': 320, 'height': 180, 'frameRate': {'num': 12, 'den': 1}}, 'assets': {'shot': {'path': str(shot), 'sha256': source_sha}}, 'operations': [{'command': 'asset.import', 'params': {'asset': 'shot'}, 'as': 'shot'}, {'command': 'timeline.place', 'params': {'item': {'$ref': 'shot.item'}, 'track': 'V1', 'time': '0', 'sourceIn': '0', 'duration': str(workflow.TICKS), 'insert': False}}], 'frames': ['0'], 'export': {'audioRequired': True}}
            runtime, output = root / 'empty-runtime', root / 'required'
            self.assertFalse(runtime.exists())
            planfile = root / 'required-plan.json'; planfile.write_text(json.dumps(plan))
            arguments = [sys.executable, '-I', '-B', str(skill / 'scripts/workflow.py'), str(planfile), '--output', str(output), '--runtime-home', str(runtime)]
            result = subprocess.run(arguments, capture_output=True, text=True, timeout=180)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout), {'error': 'export_audio_missing'})
            failure = json.loads((output / 'failure.json').read_text())
            self.assertEqual(failure['schema'], 'craft-failed-stage/v1')
            self.assertEqual(failure['status'], 'failed')
            self.assertEqual(failure['error'], 'export_audio_missing')
            self.assertEqual(failure['outcome'], 'failed')
            self.assertFalse(failure['replayAllowed'])
            stage = (output / failure['stage']).resolve()
            self.assertTrue(stage.is_relative_to(root.resolve()))
            self.assertEqual(json.loads((stage / 'failure.json').read_text()), failure)
            self.assertIn('checkpoint.fcproj', failure['files'])
            for name, entry in failure['files'].items():
                self.assertEqual(workflow.sha(stage / name), entry['sha256'])
                self.assertEqual((stage / name).stat().st_size, entry['bytes'])
            self.assertFalse((output / 'manifest.json').exists())
            for filename in ('project.fcproj', 'film.mp4', 'frame-0000.png'): self.assertTrue((output / filename).is_file())
            probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-of', 'json', str(output / 'film.mp4')]))
            self.assertTrue(any(s['codec_type'] == 'audio' for s in probe['streams']))
            check = json.loads((output / 'audio-check.json').read_text())
            self.assertEqual(check['sourceAliases'], [])
            self.assertTrue(check['required'])
            self.assertTrue(check['exportedAudio'])
            raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(output / 'film.mp4'), '-map', '0:a:0', '-f', 'f32le', '-'])
            samples = array.array('f', raw)
            self.assertGreater(len(samples), 0)
            self.assertEqual(max(abs(x) for x in samples), 0)
            self.assertEqual(next(s['nb_read_frames'] for s in probe['streams'] if s['codec_type'] == 'video'), '12')
            diagnostics = {str(p.relative_to(output)): workflow.sha(p) for p in output.rglob('*') if p.is_file()}
            # 失败目录不能在重试时覆盖，诊断文件全部保留。
            with self.assertRaisesRegex(ValueError, 'output_exists'):
                workflow.execute(plan, output, runtime_home=runtime)
            for name, sha in diagnostics.items(): self.assertEqual(workflow.sha(output / name), sha)
            for name, entry in failure['files'].items():
                self.assertEqual(workflow.sha(stage / name), entry['sha256'])
            optional = json.loads(json.dumps(plan)); optional['export']['audioRequired'] = False
            delivered = workflow.execute(optional, root / 'optional', runtime_home=runtime)
            self.assertTrue((root / 'optional/manifest.json').is_file())
            # 用户提供的有意静音 WAV 有真实源音轨，不能按零波形误拒绝。
            silent_voice = root / 'silent-voice.wav'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', '1', '-c:a', 'pcm_s16le', str(silent_voice)], check=True)
            intentional = json.loads(json.dumps(plan))
            intentional['assets']['silentVoice'] = {'path': str(silent_voice), 'sha256': workflow.sha(silent_voice)}
            intentional['operations'] += [{'command': 'asset.import', 'params': {'asset': 'silentVoice'}, 'as': 'silentVoice'}, {'command': 'timeline.place', 'params': {'item': {'$ref': 'silentVoice.item'}, 'track': 'A1', 'audioTrack': 'A1', 'time': '0', 'sourceIn': '0', 'duration': str(workflow.TICKS), 'insert': False}}]
            workflow.execute(intentional, root / 'intentional-silence', runtime_home=runtime)
            self.assertTrue((root / 'intentional-silence/manifest.json').is_file())
            self.assertEqual(json.loads((root / 'intentional-silence/audio-check.json').read_text())['sourceAliases'], ['silentVoice'])
            self.assertEqual(workflow.sha(shot), source_sha)
            for name, sha in skill_hashes.items(): self.assertEqual(workflow.sha(skill / name), sha)
            self.assertFalse(list(skill.rglob('*.pyc')))
            if os.environ.get('CRAFT_MISSING_AUDIO_EVIDENCE'):
                proof = {'schema': 'filmcraft-missing-audio-first-use/v1', 'scope': 'single audio skill copied alone; default public empty runtime install; real no-source-audio movie with automatic silent AAC', 'publicWorkflowExitCode': result.returncode, 'failure': failure, 'audioCheck': check, 'decodedPeakAmplitude': 0, 'failedOutputFiles': diagnostics, 'failedOutputProbe': probe, 'successManifestAbsent': True, 'repeatPreservedDiagnostics': True, 'explicitOptionalAudioPassed': True, 'intentionalSilentSourceAudioPassed': True, 'optionalOutputFiles': delivered['files'], 'runtimeSha256': delivered['runtimeSha256'], 'sourceInputSha256': source_sha, 'skillFilesPreserved': True}
                with Path(os.environ['CRAFT_MISSING_AUDIO_EVIDENCE']).open('x') as stream: json.dump(proof, stream, indent=2)
