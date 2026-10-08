"""真实媒体矩阵的来源、内容与预期必须完整，准备通过不等于原生导出通过。"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


class MediaMatrixTests(unittest.TestCase):
    def test_preparer_refuses_substituted_download_before_creating_output(self):
        from media_matrix import prepare
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            substituted = root / 'movie'; substituted.write_bytes(b'not the licensed movie')
            output = root / 'output'
            with self.assertRaisesRegex(ValueError, 'registered_source_digest_mismatch'):
                prepare(substituted, substituted, substituted, output, 'unused', 'unused')
            self.assertFalse(output.exists())

    def test_all_required_cases_and_each_expected_observation_are_mandatory(self):
        from media_matrix import CASES, validate
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'sample').write_bytes(b'fixture')
            digest = hashlib.sha256(b'fixture').hexdigest()
            manifest = {'schema': 'filmcraft-media-fixtures/v1', 'nativeAcceptance': 'NOT_RUN',
                        'inputs': {'sample': {'path': 'sample', 'sha256': digest, 'bytes': 7,
                            'provenance': 'real-derived', 'source': 'https://example.org/movie',
                            'license': 'CC-BY-3.0', 'attribution': 'Movie creator',
                            'parents': [], 'recipe': ['documented transformation']}},
                        'cases': {name: {'inputs': ['sample'], 'expected': dict(expected),
                            'knownFailure': 'deliberate invalid boundary', 'nativeStatus': 'NOT_RUN'}
                            for name, expected in CASES.items()}}
            validate(manifest, root)
            for mutation in ('case', 'expected', 'source', 'license', 'digest', 'escape', 'parent', 'native-pass'):
                bad = copy.deepcopy(manifest)
                if mutation == 'case': bad['cases'].pop(next(iter(CASES)))
                if mutation == 'expected': bad['cases'][next(iter(CASES))]['expected'] = {}
                if mutation in ('source', 'license'): bad['inputs']['sample'].pop(mutation)
                if mutation == 'digest': bad['inputs']['sample']['sha256'] = '0' * 64
                if mutation == 'escape': bad['inputs']['sample']['path'] = '../sample'
                if mutation == 'parent': bad['inputs']['sample']['parents'] = ['missing']
                if mutation == 'native-pass': bad['nativeAcceptance'] = 'PASS'
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    validate(bad, root)

    def test_synthetic_input_cannot_be_promoted_to_real_capture(self):
        from media_matrix import validate_provenance
        row = {'provenance': 'synthetic', 'source': 'repository-generated calibration',
               'license': 'Apache-2.0', 'attribution': 'FilmCraft contributors',
               'parents': [], 'recipe': ['color source'], 'realCapture': False}
        validate_provenance(row)
        row['realCapture'] = True
        with self.assertRaisesRegex(ValueError, 'synthetic_real_claim'):
            validate_provenance(row)

    def test_dependency_cycle_is_rejected(self):
        from media_matrix import validate_parent_graph
        with self.assertRaisesRegex(ValueError, 'parent_cycle'):
            validate_parent_graph({'a': {'parents': ['b']}, 'b': {'parents': ['a']}})
