"""媒体测量必须覆盖时长、同步、尾部与像素；候选不能冒充固定安装。"""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


class NativeMediaMatrixTests(unittest.TestCase):
    def test_half_alpha_is_composited_in_linear_light_with_srgb_output(self):
        from verify_media_matrix import composite_channel
        self.assertEqual(composite_channel(255, 128), 188)
        self.assertEqual(composite_channel(220, 255), 220)
        self.assertEqual(composite_channel(255, 0), 0)
        self.assertNotEqual(composite_channel(255, 128), 128)

    def test_failure_diagnostics_are_allowed_but_never_success_manifest(self):
        from verify_media_matrix import rejection_gate
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, 'unclassified_failure_output'):
                rejection_gate(root)
            (root/'failure.json').write_text(json.dumps({'schema':'craft-failed-stage/v1',
                'status':'failed','replayAllowed':False,'acceptance':'not-a-successful-delivery'}))
            self.assertEqual(rejection_gate(root)['status'], 'failed')
            (root/'manifest.json').write_text('{"schema":"filmcraft-delivery/v1"}')
            with self.assertRaisesRegex(ValueError, 'failed_delivery_published'):
                rejection_gate(root)

    def test_audio_gate_refuses_bad_correlation_lag_missing_tail_and_nan(self):
        from verify_media_matrix import audio_gate
        good = {'correlation': 0.999, 'lagSeconds': 0.0, 'sampleCount': 544, 'rms': 0.2}
        audio_gate(good, required_samples=544, frame_seconds=1/12)
        for key, value in [('correlation', .97), ('correlation', float('nan')),
                           ('lagSeconds', .1), ('sampleCount', 543), ('rms', 0.0)]:
            row = dict(good, **{key: value})
            with self.subTest(row=row), self.assertRaises(ValueError):
                audio_gate(row, required_samples=544, frame_seconds=1/12)

    def test_pixel_gate_checks_all_frames_and_every_rgba_channel(self):
        from verify_media_matrix import pixel_gate
        rows = [{'frame': i, 'maximumChannelError': 3} for i in range(12)]
        pixel_gate(rows, 12)
        for broken in [rows[:-1], rows + [rows[0]], [dict(rows[0], maximumChannelError=4)]+rows[1:],
                       [dict(rows[0], maximumChannelError=float('nan'))]+rows[1:]]:
            with self.assertRaises(ValueError): pixel_gate(broken, 12)

    def test_source_and_candidate_checks_cannot_qualify_fixed_installation(self):
        from verify_media_matrix import summarize
        from media_matrix import CASES
        cases = {name: {'status': 'PASS', 'measurements': {'observed': True}} for name in CASES}
        report = summarize(cases, candidate=True, installation_preserved=True)
        self.assertEqual(report['result'], 'PASS')
        self.assertEqual(report['fixedInstallation'], 'NOT_RUN')
        self.assertEqual(report['fullV1'], 'NOT_PROVEN')
        self.assertEqual(summarize(cases, candidate=False, installation_preserved=False)['result'], 'FAIL')
        for mutation in ('missing', 'not-run', 'empty'):
            broken = copy.deepcopy(cases)
            if mutation == 'missing': broken.pop('vfr')
            if mutation == 'not-run': broken['vfr']['status'] = 'NOT_RUN'
            if mutation == 'empty': broken['vfr']['measurements'] = {}
            self.assertEqual(summarize(broken, candidate=True, installation_preserved=True)['result'], 'FAIL')

    def test_existing_output_is_refused_before_bootstrap_or_media_mutation(self):
        from verify_media_matrix import verify
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = root/'user.txt'; marker.write_text('preserve')
            with self.assertRaisesRegex(ValueError, 'output_exists'):
                verify(root, root, root, root, 'unused', 'unused')
            self.assertEqual(marker.read_text(), 'preserve')
