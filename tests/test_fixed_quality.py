import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_fixed_quality import validate_quality


def fixture():
    def result(status, dimension=None):
        return {"engineeringAcceptance": "PASS", "technicalAcceptance": status, "creativeAcceptance": "manual_review",
                "userAcceptance": "NOT_RUN", "decision": "blocked" if status == "FAIL" else "manual_review",
                "dimensions": {dimension: {"status": status}} if dimension else {}}
    rows = [{"scenario": "actual-native-independent-quality", "result": result("PASS"), "originalProjectPreserved": True,
             "receipt": {"context": {"source": "external-process", "pid": 1}}}]
    for name, dimension, status in [("aligned", None, "PASS"), ("shifted", "avSync", "FAIL"),
                                    ("stereo-clipped", "audioClipping", "FAIL"), ("broken", "decode", "FAIL"),
                                    ("missing-audio", "audioClipping", "FAIL"), ("bad-subtitle", "subtitleTiming", "FAIL"),
                                    ("missing-tools", None, "NOT_RUN")]:
        rows.append({"scenario": "quality-media-" + name, "result": result(status, dimension), "files": {"film.mp4": {}},
                     "reviewer": {"implementationSha256": "a" * 64}})
    return {"result": "PASS", "allInstalledFilesUnchanged": True, "matrix": rows}


class FixedQualityTests(unittest.TestCase):
    def test_complete_collector_fixture_is_synthetic_not_native_proof(self):
        self.assertEqual(len(validate_quality(fixture())), 8)

    def test_missing_measurement_forged_process_or_user_acceptance_refused(self):
        for change in ("missing", "process", "acceptance", "measurement", "identity"):
            value = copy.deepcopy(fixture())
            if change == "missing": value["matrix"].pop()
            if change == "process": value["matrix"][0]["receipt"]["context"]["pid"] = 0
            if change == "acceptance": value["matrix"][0]["result"]["userAcceptance"] = "PASS"
            if change == "measurement": value["matrix"][2]["result"]["dimensions"]["avSync"]["status"] = "PASS"
            if change == "identity": value["allInstalledFilesUnchanged"] = False
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_quality(value)


if __name__ == "__main__":
    unittest.main()
