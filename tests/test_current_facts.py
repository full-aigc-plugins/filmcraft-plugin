"""FC-RL-001：当前事实从固定身份生成，历史报告不提升当前验收。"""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CurrentFactsTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((ROOT / 'scripts/current_facts.py').is_file(), 'current fact generator is missing')
        spec = importlib.util.spec_from_file_location('filmcraft_current_facts', ROOT / 'scripts/current_facts.py')
        self.facts = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.facts)

    def copy_inputs(self, target):
        for relative in ('plugin.json', 'skills.lock.json', 'project-status.json',
                         'docs/skills-source-plan.json', 'docs/skills-source-suite.json',
                         'runtime/filmcraft-cli.lock.json'):
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, path)
        shutil.copytree(ROOT / 'skills', target / 'skills', ignore=shutil.ignore_patterns('__pycache__'))

    def mutate(self, root, relative, edit):
        path = root / relative
        value = json.loads(path.read_text())
        edit(value)
        path.write_text(json.dumps(value))

    def test_generation_is_deterministic_and_does_not_promote_history(self):
        first = self.facts.collect(ROOT)
        self.assertEqual(first, self.facts.collect(ROOT))
        self.assertEqual(first['skillCount'], 13)
        self.assertEqual(first['commandCount'], 666)
        self.assertEqual(first['activeRuntime']['version'], '0.2.0-craft.4')
        self.assertEqual(first['historicalRuntime']['role'], 'historical-bootstrap-baseline')
        self.assertEqual(first['currentQualification'], 'NOT_PROVEN')
        self.assertEqual(first['implementation'], 'in-progress')

    def test_each_authority_drift_is_rejected(self):
        edits = [
            ('plugin.json', lambda x: x.update(name='foreign'), 'plugin_identity_mismatch'),
            ('docs/skills-source-plan.json', lambda x: x.update(sourceSha='0' * 40), 'source_plan_identity_mismatch'),
            ('docs/skills-source-suite.json', lambda x: x['suite'].update(version='0.0.0'), 'source_suite_identity_mismatch'),
            ('docs/skills-source-suite.json', lambda x: x['suite']['skills'].pop(), 'skill_list_mismatch'),
            ('skills/filmcraft-use/references/command-coverage.json', lambda x: x.update(runtimeSha256='0' * 64), 'catalog_runtime_mismatch'),
            ('skills/filmcraft-cli/scripts/runtime.lock.json', lambda x: x.update(resolvedVersion='0.0.0'), 'standalone_runtime_drift'),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_inputs(root)
            for relative, edit, error in edits:
                with self.subTest(file=relative):
                    path = root / relative
                    before = path.read_bytes()
                    self.mutate(root, relative, edit)
                    with self.assertRaisesRegex(ValueError, error):
                        self.facts.collect(root)
                    path.write_bytes(before)

    def test_historical_root_lock_does_not_select_active_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_inputs(root)
            before = self.facts.collect(root)
            self.mutate(root, 'runtime/filmcraft-cli.lock.json', lambda x: x.update(resolvedVersion='historical-only'))
            after = self.facts.collect(root)
            self.assertEqual(before['activeRuntime'], after['activeRuntime'])
            self.assertNotEqual(before['historicalRuntime'], after['historicalRuntime'])
            self.assertEqual(after['currentQualification'], 'NOT_PROVEN')

    def test_reference_metadata_drift_is_visible_without_relabeling_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_inputs(root)
            self.mutate(root, 'skills/filmcraft-use/references/commands.json',
                        lambda x: x.update(runtimeSha256='0' * 64))
            value = self.facts.collect(root)
            self.assertEqual(value['referenceCatalogIdentity']['status'], 'MISMATCH')
            self.assertEqual(value['referenceCatalogIdentity']['binarySha256'], '0' * 64)
            self.assertEqual(value['currentQualification'], 'NOT_PROVEN')

    def test_bilingual_rendering_and_generated_snapshot_are_current(self):
        value = self.facts.collect(ROOT)
        self.assertEqual(json.loads((ROOT / 'docs/current-facts.json').read_text()), value)
        for language in ('en', 'zh-CN'):
            rendered = self.facts.render(value, language)
            for expected in (value['pluginVersion'], value['sourceRef'], value['activeRuntime']['version'],
                             str(value['skillCount']), str(value['commandCount']), 'NOT_PROVEN'):
                self.assertIn(expected, rendered)
            filename = 'README.md' if language == 'en' else 'README.zh-CN.md'
            text = (ROOT / filename).read_text()
            self.assertEqual(text.count(self.facts.START), 1)
            self.assertIn(rendered, text)


if __name__ == '__main__':
    unittest.main()
