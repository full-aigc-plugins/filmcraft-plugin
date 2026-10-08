#!/usr/bin/env python3
"""固定公开安装的受限修订、独立重评与最佳候选保全验收。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from verify_fixed_quality import verify as quality_verify

REQUIRED = {'actual-native-scoped-revision', 'actual-native-revision-budget-best',
            'revision-policy-restart', 'revision-scope-rejection', 'revision-failure-limit',
            'revision-stagnation_limit', 'revision-round_limit', 'revision-criteria-invalidated',
            'schema4-upgrade-rollback'}


def validate_revision(report):
    if (report.get('result') != 'PASS' or not report.get('allInstalledFilesUnchanged')
            or report.get('resources', {}).get('schemaVersion') not in (5, 6)):
        raise ValueError('fixed_revision_install_unqualified')
    rows = {row['scenario']: row for row in report.get('matrix', [])}
    if not REQUIRED.issubset(rows): raise ValueError('revision_matrix_incomplete')
    native = rows['actual-native-scoped-revision']; loop = native['loop']
    if (loop['reason'] != 'issues_resolved' or loop['rounds'] != 1 or loop['pending'] is not None
            or loop['best']['taskId'] == loop['rootTaskId'] or loop['unresolvedIssues'] or loop['unresolvedQuality']
            or loop['userAcceptance'] != 'NOT_RUN' or loop['creativeAcceptance'] != 'manual_review'
            or not native['sourceProjectPreserved'] or not native['oldReviewRejected'] or not native['authorizationRefReused']
            or not native['diff']['nonTargetsPreserved']
            or native['candidateAttempts'] != 1 or native['sourceAttempts'] != 1
            or native['sourceProjectSha256'] == native['candidateProjectSha256']
            or len(native['rounds']) != 1 or native['rounds'][0]['state'] != 'reviewed'):
        raise ValueError('native_revision_unconfirmed')
    intent = json.loads(native['rounds'][0]['intent'])
    if intent['compiled']['sourceSha256'] != native['sourceProjectSha256']:
        raise ValueError('native_revision_source_unconfirmed')
    budget = rows['actual-native-revision-budget-best']; stopped = budget['loop']
    if (stopped['state'] != 'stopped' or stopped['reason'] != 'budget_revisions_exceeded'
            or stopped['best']['taskId'] != stopped['rootTaskId'] or not stopped['unresolvedIssues']
            or stopped['best']['projectSha256'] != budget['bestProjectSha256'] or budget['attempts'] != 0
            or not budget['sourceProjectPreserved'] or not budget['authorizationRefReused']
            or stopped['userAcceptance'] != 'NOT_RUN'):
        raise ValueError('revision_budget_best_unconfirmed')
    for name in ('revision-stagnation_limit', 'revision-round_limit', 'revision-criteria-invalidated'):
        if rows[name]['best'] is not None: raise ValueError('revision_unverified_best')
    if not rows['revision-scope-rejection']['bestPreserved'] or not rows['revision-failure-limit']['bestPreserved']:
        raise ValueError('revision_best_lost')
    return [rows[name] for name in sorted(REQUIRED)]


def verify(host, previous_host, authority, ref, output, python, node, ffmpeg, ffprobe):
    previous = os.environ.get('FILMCRAFT_REVISION_NATIVE')
    os.environ['FILMCRAFT_REVISION_NATIVE'] = '1'
    try:
        quality_verify(host, previous_host, authority, ref, output, python, node, ffmpeg, ffprobe)
    finally:
        if previous is None: os.environ.pop('FILMCRAFT_REVISION_NATIVE', None)
        else: os.environ['FILMCRAFT_REVISION_NATIVE'] = previous
    original = (output / 'report.json').read_bytes(); report = json.loads(original)
    revision = validate_revision(report)
    (output / 'quality-report.json').write_bytes(original)
    report.update(schema='filmcraft-fixed-revision-acceptance/v1', revision=revision,
                  qualityReportSha256=hashlib.sha256(original).hexdigest(),
                  scope='FC-QA-002 tasks9.25-9.27; bounded speed/gain compiler and POSIX installed native proof; full V1, creative and user acceptance remain open')
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return {'result': 'PASS', 'tests': report['testCounts'], 'revisionScenarios': len(REQUIRED),
            'reportSha256': hashlib.sha256((output / 'report.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['host', 'previous-host', 'authority', 'output', 'ffmpeg', 'ffprobe']:
        parser.add_argument('--' + name, type=Path, required=True)
    for name in ['ref', 'python', 'node']: parser.add_argument('--' + name, required=True)
    print(json.dumps(verify(**vars(parser.parse_args()))))
