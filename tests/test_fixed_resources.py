"""汇总器负例只验证拒绝逻辑；不作为固定宿主或原生验收。"""
import json
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from verify_fixed_resources import REQUIRED, validate_resources


def fixture():
    return {"result": "PASS", "allInstalledFilesUnchanged": True,
            "matrix": [{"scenario": value} for value in REQUIRED],
            "native": {"resources": {"schemaVersion": 4, "sharedScope": "parent", "parentTaskId": "parent",
                       "childTaskId": "child", "reservations": [
                           {"task_id": name, "scope_id": "parent", "state": "settled",
                            "allocation": json.dumps({"revisions": int(name == "child")})} for name in ("parent", "child")],
                       "outputLimit": {"state": "failed", "reason": "budget_output_exceeded", "bytes": 2,
                                       "dependencyAttempts": 0, "partialProjectPreserved": True},
                       "cancellation": {"state": "cancelled", "attempts": 1, "stopped": True,
                                        "authorization": "actual private host LocalAuthorizationStore"}}}}


class FixedResourceCollectorTests(unittest.TestCase):
    def test_complete_fixture_is_accepted_only_as_collector_unit_input(self):
        self.assertEqual(validate_resources(fixture())["sharedScope"], "parent")

    def test_matrix_gap_identity_drift_and_unconfirmed_stop_cannot_pass(self):
        cases = []
        row = fixture(); row["matrix"] = []; cases.append(row)
        row = fixture(); row["allInstalledFilesUnchanged"] = False; cases.append(row)
        row = fixture(); row["native"]["resources"]["cancellation"]["stopped"] = False; cases.append(row)
        row = fixture(); row["native"]["resources"]["sharedScope"] = "new-budget"; cases.append(row)
        row = fixture(); row["native"]["resources"]["reservations"][1]["state"] = "reserved"; cases.append(row)
        row = fixture(); row["native"]["resources"]["outputLimit"]["dependencyAttempts"] = 1; cases.append(row)
        row = fixture(); row["native"]["resources"]["reservations"][1]["allocation"] = '{"revisions":0}'; cases.append(row)
        for row in cases:
            with self.subTest(row=row), self.assertRaises(ValueError):
                validate_resources(row)


if __name__ == "__main__":
    unittest.main()
