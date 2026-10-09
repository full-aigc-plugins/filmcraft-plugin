"""画面oracle必须识别错误色域混合、局部像素变化和形状损坏。"""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('effect_pixels',Path(__file__).resolve().parents[1]/'scripts/verify_effect_pixels.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class EffectPixelTests(unittest.TestCase):
    def test_half_opacity_is_straight_alpha_not_darkened_rgb(self):
        expected=bytes([230,85,39,128])*1024
        with self.assertRaisesRegex(ValueError,'pixel_frame_mismatch'):m.compare_frame(bytes([115,42,19,128])*1024,expected)
        with self.assertRaisesRegex(ValueError,'pixel_alpha_mismatch'):m.compare_frame(bytes([230,85,39,127])*1024,expected)

    def test_a_single_wrong_channel_cannot_hide_in_frame_average(self):
        expected=bytes([100])*4096;actual=bytearray(expected);actual[2046]=103
        with self.assertRaisesRegex(ValueError,'pixel_frame_mismatch'):m.compare_frame(actual,expected)

    def test_eight_bit_quantization_one_code_unit_is_explicit(self):
        self.assertEqual(m.compare_frame(bytes([101,101,101,100])*1024,bytes([100])*4096),1)
        with self.assertRaisesRegex(ValueError,'pixel_frame_mismatch'):m.compare_frame(bytes([102,102,102,100])*1024,bytes([100])*4096)

    def test_missing_or_extra_pixels_are_rejected(self):
        expected=bytes(4096)
        for actual in [bytes(4095),bytes(4097),b'']:
            with self.subTest(size=len(actual)),self.assertRaisesRegex(ValueError,'pixel_frame_shape_mismatch'):m.compare_frame(actual,expected)

    def test_correct_average_wrong_spatial_layout_is_rejected(self):
        expected=b''.join(bytes([80,80,80,255]) if x<24 else bytes([0,0,0,255]) for y in range(32) for x in range(32))
        swapped=b''.join(bytes([80,80,80,255]) if x>=8 else bytes([0,0,0,255]) for y in range(32) for x in range(32))
        self.assertEqual(sum(expected),sum(swapped))
        with self.assertRaisesRegex(ValueError,'pixel_frame_mismatch'):m.compare_frame(swapped,expected)

if __name__=='__main__':unittest.main()
