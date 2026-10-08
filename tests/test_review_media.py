"""独立测量的确定性边界；真实媒体另在明确启用的原生验收执行。"""
import array
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import hashlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("review_media", ROOT / "scripts/review_media.py")
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)


class ReviewMediaTests(unittest.TestCase):
    def test_request_digest_uses_frozen_wire_bytes_not_python_number_rendering(self):
        with tempfile.TemporaryDirectory() as home:
            root = Path(home)
            # JS emits 1e-7 while Python emits 1e-07; the original request is authoritative.
            raw = b'{"criteria":{"rubric":{"thresholds":{"clippingFraction":1e-7}}}}\n'
            (root / "request.json").write_bytes(raw)
            (root / "tools.json").write_text("{}")
            result = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "scripts/review_media.py"),
                                     "--request", str(root / "request.json"), "--tools", str(root / "tools.json"),
                                     "--artifacts", str(root)], capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout)["requestSha256"], hashlib.sha256(raw[:-1]).hexdigest())

    def test_opposite_stereo_polarity_cannot_hide_channel_clipping(self):
        with tempfile.TemporaryDirectory() as home:
            root = Path(home); (root / "film.mp4").write_bytes(b"controlled-fixture")
            request = {"criteria": {"goal": {"audioRequired": True}, "rubric": {"thresholds": {
                "clippingAmplitude": .999, "clippingFraction": .001, "syncToleranceMs": 50}}}}
            def tool(argv, *args):
                if "-show_streams" in argv:
                    return 0, json.dumps({"streams": [{"codec_type": "video"}, {"codec_type": "audio", "channels": 2}],
                                          "format": {"duration": "1"}}).encode(), ""
                if "-show_frames" in argv:
                    return 0, b'{"frames":[{"best_effort_timestamp_time":"0"},{"best_effort_timestamp_time":"0.5"}]}', ""
                if "f32le" in argv:
                    values = [0.] * 960 if "-ac" in argv else [1., -1.] * 480
                    return 0, array.array("f", values).tobytes(), ""
                return 0, b"", ""
            with patch.object(media, "run", side_effect=tool):
                result = media.measure(request, root, {"ffmpeg": "ffmpeg", "ffprobe": "ffprobe"})
            self.assertEqual(result["dimensions"]["audioClipping"]["status"], "FAIL")

    def test_subtitle_outside_duration_fails_and_empty_timeline_is_not_run(self):
        with tempfile.TemporaryDirectory() as home:
            path = Path(home) / "captions.srt"
            path.write_text("1\n00:00:00,500 --> 00:00:02,000\n字幕\n")
            self.assertEqual(media.caption_times(path, 1)["status"], "FAIL")
            path.write_text("")
            self.assertEqual(media.caption_times(path, 1)["status"], "NOT_RUN")

    def test_missing_tools_leave_technical_and_creative_unconfirmed(self):
        value = media.measure({}, Path("."), {})
        self.assertEqual(value["dimensions"]["avSync"]["status"], "NOT_RUN")
        self.assertEqual(value["dimensions"]["rhythm"]["status"], "manual_review")
        self.assertEqual(value["engineering"]["status"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
