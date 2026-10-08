"""恢复验收收集器：安装子进程切换目录不能改变报告目的地。"""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ['readonly-wal-and-missing-receipts', 'missing-and-damaged-ledgers', 'lost-reply-and-old-epoch',
             'expired-recovery-owner', 'repeat-repair', 'two-recovery-executors', 'host-exited-child-alive',
             'schema1-upgrade-rollback', 'schema2-upgrade-rollback', 'rollback-preserves-new-records',
             'inspection-concurrent-write', 'actual-native-repair-and-continuation',
             'actual-previous-version-downgrade-refusal', 'expired-revoked-authorization']


class FixedRecoveryTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('fixed_recovery_tested', ROOT / 'scripts/verify_fixed_recovery.py')
        self.verifier = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.verifier)

    def execute(self, root, output):
        entries = {}
        for host, version in [('new-host', 'v0.1.0-dev.47'), ('old-host', 'v0.1.0-dev.45')]:
            entry = {'version': version.removeprefix('v'), 'sha': 'a' * 40, 'skillSourceSha': 'b' * 40,
                     'skills': {'filmcraft-use': 'c' * 64}, 'codeFilesSha256': {}}
            entries[version] = entry
            path = root / host; skill = path / 'host-config/plugin/skills/filmcraft-use'; skill.mkdir(parents=True)
            (path / 'host-receipt.json').write_text(json.dumps({'result': 'PASS', 'plugin': entry,
                                                               'helper': {'fixture': True}, 'codexVersion': 'fixture'}))
            (path / 'installed-directories.private.json').write_text(json.dumps({'filmcraft-use': str(skill)}))
        helper = types.SimpleNamespace(verify_installed_skill=lambda *args: None)
        fixed = types.SimpleNamespace(owner_helper=lambda authority: (helper, {'fixture': True}),
                                      release_entry=lambda repository, ref: entries[ref], verify_code_files=lambda *args: None)
        protocol = types.SimpleNamespace(validate=lambda *args: {'validated': {'publicTasks': 3, 'publicArtifacts': 26}})
        def module(path, name): return fixed if name == 'recovery_fixed' else protocol
        def run(*args, **kwargs):
            # 模拟安装目录作为 cwd。证据必须仍写到调用者指定位置。
            env = kwargs['env']
            for key in ['TMPDIR', 'FILMCRAFT_HARNESS_REPORT', 'FILMCRAFT_RECOVERY_EVIDENCE', 'FILMCRAFT_NATIVE_RUNTIME_HOME']:
                self.assertTrue(Path(env[key]).is_absolute(), key + ' must survive child cwd changes')
            Path(env['FILMCRAFT_RECOVERY_EVIDENCE']).write_text('\n'.join(json.dumps({'scenario': name, 'before': {}, 'after': {}}) for name in SCENARIOS))
            Path(env['FILMCRAFT_HARNESS_REPORT']).write_text(json.dumps({'result': 'PASS', 'sourceRevision': 'b' * 40,
                'runtimeIdentity': {'pluginVersion': '0.1.0-dev.47'},
                'continuation': {'originalAttemptCount': 1, 'childAttemptCount': 1, 'reused': True}}))
            return types.SimpleNamespace(returncode=0, stdout='ℹ tests 1\nℹ pass 1\nℹ fail 0\nℹ skipped 0\n', stderr='')
        with patch.object(self.verifier, 'module', side_effect=module), patch.object(self.verifier.subprocess, 'run', side_effect=run):
            return self.verifier.verify(Path('new-host'), Path('old-host'), Path('authority'), 'v0.1.0-dev.47', output, 'python-fixture', 'node-fixture')

    def test_relative_output_remains_at_callers_location_after_installed_child_changes_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve(); previous = Path.cwd()
            try:
                os.chdir(root)
                result = self.execute(root, Path('acceptance'))
                self.assertEqual(result['result'], 'PASS')
                self.assertEqual(result['scenarios'], 14)
                self.assertEqual(json.loads((root / 'acceptance/report.json').read_text())['testCounts']['pass'], 1)
            finally: os.chdir(previous)

    def test_existing_evidence_directory_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve(); previous = Path.cwd()
            try:
                os.chdir(root); output = root / 'acceptance'; output.mkdir(); marker = output / 'original'; marker.write_text('preserve')
                with self.assertRaisesRegex(ValueError, 'recovery_output_exists'): self.execute(root, Path('acceptance'))
                self.assertEqual(marker.read_text(), 'preserve'); self.assertEqual(list(output.iterdir()), [marker])
            finally: os.chdir(previous)

    def test_dangling_output_symlink_cannot_redirect_evidence_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve(); previous = Path.cwd()
            try:
                os.chdir(root); output = root / 'acceptance'; target = root / 'user-owned-destination'
                output.symlink_to(target, target_is_directory=True)
                with self.assertRaisesRegex(ValueError, 'recovery_output_exists'): self.execute(root, Path('acceptance'))
                self.assertTrue(output.is_symlink()); self.assertFalse(target.exists())
            finally: os.chdir(previous)
