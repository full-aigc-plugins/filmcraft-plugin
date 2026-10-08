"""固定 FilmCraft 安装验证：标签解析与写入前身份拒绝。"""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FixedInstallTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('filmcraft_fixed_install', ROOT / 'scripts/verify_fixed_install.py')
        self.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.verifier)

    def test_remote_annotated_and_lightweight_tags_resolve_to_the_commit(self):
        tag = 'refs/tags/v0.1.0-dev.42'
        self.assertEqual(self.verifier.remote_commit('a' * 40 + '\t' + tag + '\n', 'v0.1.0-dev.42'), 'a' * 40)
        text = 'a' * 40 + '\t' + tag + '\n' + 'b' * 40 + '\t' + tag + '^{}\n'
        self.assertEqual(self.verifier.remote_commit(text, 'v0.1.0-dev.42'), 'b' * 40)

    def test_ambiguous_missing_or_malformed_tag_results_are_rejected(self):
        tag = 'refs/tags/v0.1.0-dev.42'
        for text in ('', 'bad\t' + tag, 'a' * 40 + '\t' + tag + '^{}',
                     'a' * 40 + '\t' + tag + '\n' + 'b' * 40 + '\t' + tag,
                     'a' * 40 + '\trefs/heads/main'):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'remote_tag_invalid'):
                self.verifier.remote_commit(text, 'v0.1.0-dev.42')

    def test_tagged_entry_binds_manifest_source_and_all_skill_digests(self):
        with tempfile.TemporaryDirectory(prefix='fixed tag fixture ') as temporary:
            repo = Path(temporary)
            for name in ('plugin.json', 'skills.lock.json', 'package.json'):
                (repo / name).write_bytes((ROOT / name).read_bytes())
            (repo / 'src').mkdir(); (repo / 'src/runtime.ts').write_text('export const test = true;\n')
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), '-c', 'user.name=Fixture',
                    '-c', 'user.email=fixture@example.invalid', *args], stderr=subprocess.DEVNULL).decode().strip()
            git('init'); git('add', '.'); git('commit', '-m', 'fixture')
            version = json.loads((repo / 'plugin.json').read_text())['version']
            git('tag', '-a', 'v' + version, '-m', 'fixture')
            entry = self.verifier.release_entry(repo, 'v' + version)
            self.assertEqual(entry['sha'], git('rev-parse', 'HEAD'))
            self.assertEqual(entry['version'], version)
            self.assertEqual(entry['skillSourceRef'], json.loads((repo / 'skills.lock.json').read_text())['sources'][0]['ref'])
            self.assertEqual(len(entry['skills']), 13)
            self.assertIn('src/runtime.ts', entry['codeFilesSha256'])

    def test_malformed_source_objects_are_rejected_as_identity_errors(self):
        manifest = (ROOT / 'plugin.json').read_bytes()
        ref = 'v' + json.loads(manifest)['version']
        for lock in (None, [], {'version': 1, 'sources': [None]}, {'version': 1, 'sources': ['foreign']}):
            with self.subTest(lock=lock), self.assertRaisesRegex(ValueError, 'fixed_install_identity_invalid'):
                self.verifier.entry_from_objects(manifest, json.dumps(lock).encode(), 'a' * 40, ref)

    def test_invalid_or_mutable_ref_fails_before_output_or_host_configuration(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'verification'
            for ref in ('main', 'latest', 'v0.1.0-dev.42^{commit}', '../escape'):
                with self.subTest(ref=ref), self.assertRaisesRegex(ValueError, 'immutable_filmcraft_ref_required'):
                    self.verifier.verify('/nonexistent-codex', ROOT, ROOT, ref, target)
                self.assertFalse(target.exists())

    def test_existing_output_is_not_reused_or_modified(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary); marker = target / 'user-data'; marker.write_bytes(b'preserve')
            with self.assertRaisesRegex(ValueError, 'fixed_install_output_exists'):
                self.verifier.verify('/nonexistent-codex', ROOT, ROOT, 'v0.1.0-dev.42', target)
            self.assertEqual(marker.read_bytes(), b'preserve')
            self.assertEqual(list(target.iterdir()), [marker])

    def test_foreign_manifest_or_missing_source_digest_is_rejected(self):
        manifest = (ROOT / 'plugin.json').read_bytes()
        lock = json.loads((ROOT / 'skills.lock.json').read_text())
        broken = json.loads(manifest); broken['name'] = 'foreign'
        with self.assertRaisesRegex(ValueError, 'fixed_install_identity_invalid'):
            self.verifier.entry_from_objects(json.dumps(broken).encode(), json.dumps(lock).encode(), 'a' * 40,
                                             'v' + broken['version'])
        lock['sources'][0]['sha256'].pop(next(iter(lock['sources'][0]['sha256'])))
        with self.assertRaisesRegex(ValueError, 'fixed_install_identity_invalid'):
            self.verifier.entry_from_objects(manifest, json.dumps(lock).encode(), 'a' * 40,
                                             'v' + json.loads(manifest)['version'])

    def test_installed_executable_content_and_path_escape_are_rejected_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'plugin'; (root / 'src').mkdir(parents=True)
            path = root / 'src/runtime.ts'; original = b'export const value = 1;\n'; path.write_bytes(original)
            expected = {'src/runtime.ts': hashlib.sha256(original).hexdigest()}
            self.verifier.verify_code_files(root, expected)
            path.write_bytes(b'changed runtime')
            with self.assertRaisesRegex(ValueError, 'installed_code_identity_mismatch'):
                self.verifier.verify_code_files(root, expected)
            self.assertEqual(path.read_bytes(), b'changed runtime')
            external = Path(temporary) / 'external.ts'; external.write_bytes(original)
            path.unlink(); path.symlink_to(external)
            with self.assertRaisesRegex(ValueError, 'installed_code_identity_mismatch'):
                self.verifier.verify_code_files(root, expected)
            self.assertTrue(path.is_symlink())
            self.assertEqual(external.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
