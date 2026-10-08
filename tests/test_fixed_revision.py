import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verify_fixed_revision import REQUIRED, validate_revision


def fixture():
    rows = {name: {'scenario': name, 'best': None, 'bestPreserved': True} for name in REQUIRED}
    rows['actual-native-scoped-revision'].update(loop={'reason': 'issues_resolved', 'rounds': 1, 'pending': None,
        'best': {'taskId': 'child'}, 'rootTaskId': 'root', 'unresolvedIssues': [], 'unresolvedQuality': [],
        'userAcceptance': 'NOT_RUN', 'creativeAcceptance': 'manual_review'}, sourceProjectPreserved=True,
        oldReviewRejected=True, authorizationRefReused=True, diff={'nonTargetsPreserved': True},
        candidateAttempts=1, sourceAttempts=1, sourceProjectSha256='a'*64, candidateProjectSha256='b'*64,
        rounds=[{'state': 'reviewed', 'intent': json.dumps({'compiled': {'sourceSha256': 'a'*64}})}])
    rows['actual-native-revision-budget-best'].update(loop={'state': 'stopped', 'reason': 'budget_revisions_exceeded',
        'best': {'taskId': 'root', 'projectSha256': 'a'*64}, 'rootTaskId': 'root', 'unresolvedIssues': ['reverse'],
        'userAcceptance': 'NOT_RUN'}, bestProjectSha256='a'*64, attempts=0, sourceProjectPreserved=True, authorizationRefReused=True)
    return {'result': 'PASS', 'allInstalledFilesUnchanged': True, 'resources': {'schemaVersion': 5}, 'matrix': list(rows.values())}


class FixedRevisionTests(unittest.TestCase):
    def test_synthetic_collector_fixture_only(self):
        self.assertEqual(len(validate_revision(fixture())), len(REQUIRED))

    def test_missing_case_old_schema_target_drift_replay_and_fabricated_best_rejected(self):
        for change in ('missing','schema','scope','replay','best','acceptance','source'):
            value=copy.deepcopy(fixture()); rows={r['scenario']:r for r in value['matrix']}
            native=rows['actual-native-scoped-revision']
            if change=='missing': value['matrix'].pop()
            if change=='schema': value['resources']['schemaVersion']=4
            if change=='scope': native['diff']['nonTargetsPreserved']=False
            if change=='replay': native['candidateAttempts']=2
            if change=='best': rows['revision-round_limit']['best']={'taskId':'unverified'}
            if change=='acceptance': native['loop']['userAcceptance']='PASS'
            if change=='source': native['sourceProjectSha256']='c'*64
            with self.subTest(change=change), self.assertRaises(ValueError): validate_revision(value)
