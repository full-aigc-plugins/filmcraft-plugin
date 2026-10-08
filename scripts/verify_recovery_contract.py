#!/usr/bin/env python3
"""逐项验证 FC-TX-002 固定安装恢复报告；不以行名或测试总数代替行为证据。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MAPPING = {
    'P': ['actual-native-repair-and-continuation', 'lost-reply-and-old-epoch'],
    'N': ['actual-native-repair-and-continuation', 'readonly-wal-and-missing-receipts'],
    'READONLY-INSPECT': ['readonly-wal-and-missing-receipts', 'missing-and-damaged-ledgers', 'host-exited-child-alive', 'actual-native-repair-and-continuation'],
    'RESUME-GATE': ['lost-reply-and-old-epoch', 'expired-revoked-authorization', 'actual-native-repair-and-continuation'],
    'FORENSIC-SNAPSHOT': ['readonly-wal-and-missing-receipts', 'inspection-concurrent-write'],
    'REPAIR-FENCING': ['two-recovery-executors', 'expired-recovery-owner', 'lost-reply-and-old-epoch'],
    'REPAIR-REUSE': ['repeat-repair', 'actual-native-repair-and-continuation'],
    'STATE-COMPATIBILITY': ['schema1-upgrade-rollback', 'schema2-upgrade-rollback', 'missing-and-damaged-ledgers', 'actual-previous-version-downgrade-refusal'],
    'EXPLICIT-CONTINUATION': ['actual-native-repair-and-continuation'],
    'BACKED-MIGRATION': ['schema1-upgrade-rollback', 'schema2-upgrade-rollback', 'rollback-preserves-new-records'],
}


def require(condition, code):
    if not condition:
        raise ValueError('recovery_contract_' + code)


def contract(report):
    """校验原始实际执行报告的行为字段并返回十个规范场景的证据映射。"""
    try:
        require(report['schema'] == 'filmcraft-fixed-recovery-acceptance/v1' and report['result'] == 'PASS'
                and report['allInstalledFilesUnchanged'] is True, 'fixed_report')
        counts = report['testCounts']
        require(counts['tests'] > 0 and counts['tests'] == counts['pass'] and counts['fail'] == 0
                and counts['skipped'] == 0, 'test_counts')
        rows = {row['scenario']: row for row in report['matrix']}
        require(len(rows) == len(report['matrix']), 'duplicate_rows')
        require(set(sum(MAPPING.values(), [])).issubset(rows), 'missing_rows')
        for row in rows.values():
            require(isinstance(row['layer'], str) and bool(row['layer']), 'evidence_layer')
        readonly = ['readonly-wal-and-missing-receipts', 'missing-and-damaged-ledgers', 'repeat-repair',
                    'host-exited-child-alive', 'rollback-preserves-new-records',
                    'actual-previous-version-downgrade-refusal', 'expired-revoked-authorization']
        for name in readonly:
            row = rows[name]
            require(bool(row['before']) and row['before'] == row['after'], 'original_files_' + name)
        unknown = rows['readonly-wal-and-missing-receipts']['inspection']
        require(unknown['diagnosis'] == 'unknown' and unknown['replayAllowed'] is False
                and unknown['task']['state'] == 'reconciling', 'unknown_replay')
        require(rows['missing-and-damaged-ledgers']['result'] == 'unknown', 'damaged_ledger')
        lost = rows['lost-reply-and-old-epoch']
        require(lost['inspection']['diagnosis'] == 'executed' and lost['inspection']['process']['status'] == 'stopped'
                and lost['result']['replayed'] is False and lost['result']['state'] == 'verifying'
                and len(lost['attempts']) == 1 and len(lost['intents']) == 1
                and lost['intents'][0]['state'] == 'applied', 'lost_reply_repair')
        concurrent = rows['two-recovery-executors']
        require(concurrent['results'].count('APPLIED') == 1 and len(concurrent['results']) == 2
                and len(concurrent['attempts']) == 1
                and sum(x['state'] == 'applied' for x in concurrent['intents']) == 1
                and concurrent['state']['state'] == 'verifying', 'concurrent_repair')
        expired = rows['expired-recovery-owner']
        require(expired['currentEpoch'] > expired['oldEpoch']
                and any(x['state'] == 'abandoned' and x['reason'] == 'recovery_lease_expired' for x in expired['intents']), 'expired_fence')
        repeated = rows['repeat-repair']
        require(repeated['result']['reused'] is True and repeated['result']['replayed'] is False
                and repeated['result']['state'] == 'verifying' and len(repeated['intents']) == 1, 'repair_reuse')
        host = rows['host-exited-child-alive']
        require(host['hostExitCode'] == 0 and host['childPid'] > 0 and host['occupancy'] == 1
                and host['observation']['diagnosis'] == 'running'
                and host['observation']['process']['status'] == 'alive'
                and host['observation']['replayAllowed'] is False, 'live_child')
        require(rows['inspection-concurrent-write']['refused'] == 'ledger_changed', 'snapshot_drift')
        require(set(rows['expired-revoked-authorization']['errors']) == {'authorization_expired', 'authorization_required'}, 'authorization')
        for version in (1, 2):
            migration = rows[f'schema{version}-upgrade-rollback']; manifest = migration['manifest']
            require(migration['recordsPreserved'] is True and migration['logicalBeforeSha256'] == migration['logicalAfterSha256']
                    and manifest['complete'] is True and manifest['fromVersion'] == version
                    and manifest['toVersion'] >= 3 and bool(migration['originalAttemptId'])
                    and {'database.sqlite', 'database.sqlite-wal', 'shm.audit'}.issubset(manifest['files']), 'backed_migration')
        require(rows['rollback-preserves-new-records']['refused'] == 'rollback_changes_conflict', 'rollback_records')
        require(rows['actual-previous-version-downgrade-refusal']['error'] == 'ledger_schema_unsupported', 'downgrade')
        native = rows['actual-native-repair-and-continuation']
        require(bool(native['nativeBefore']) and native['nativeBefore'] == native['nativeAfter']
                and native['readonlyFilesPreserved'] is True and native['originalReplayed'] is False
                and len(native['originalAttempts']) == 1 and len(native['childAttempts']) == 1
                and len(native['recoveryIntents']) == 1 and native['recoveryIntents'][0]['state'] == 'applied'
                and len(native['continuationIntents']) == 1 and native['continuationIntents'][0]['state'] == 'applied'
                and native['originalAttempts'][0]['attempt_id'] != native['childAttempts'][0]['attempt_id'], 'native_continuation')
        continuation = report['native']['continuation']
        require(continuation['originalAttemptCount'] == 1 and continuation['childAttemptCount'] == 1
                and continuation['reused'] is True, 'continuation_reuse')
        return {'FC-TX-002-' + name: {'status': 'PASS', 'matrixRows': sources,
                    'layers': sorted({rows[source]['layer'] for source in sources})}
                for name, sources in MAPPING.items()}
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError('recovery_contract_evidence_missing') from error


def verify(report_path, ref, output, repository=ROOT):
    """绑定固定标签、原始报告及已安装测试源码；拒绝旧版本报告和缺失规范场景。"""
    data = report_path.read_bytes(); report = json.loads(data)
    spec = importlib.util.spec_from_file_location('contract_fixed', ROOT / 'scripts/verify_fixed_install.py')
    fixed = importlib.util.module_from_spec(spec); spec.loader.exec_module(fixed)
    expected = fixed.release_entry(repository, ref)
    verifier_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    require(expected['codeFilesSha256'].get('scripts/verify_recovery_contract.py') == verifier_hash, 'verifier_identity')
    fixed.verify_code_files(ROOT, expected['codeFilesSha256'])
    require(report['fixedPlugin'] == expected, 'release_identity')
    require(report['native']['sourceRevision'] == expected['skillSourceSha']
            and report['native']['runtimeIdentity']['pluginVersion'] == expected['version'], 'native_identity')
    tests = subprocess.check_output(['git', '-C', str(repository), 'ls-tree', '-r', '--name-only', expected['sha'], '--', 'test/harness'], text=True).splitlines()
    hashes = {name: hashlib.sha256(subprocess.check_output(['git', '-C', str(repository), 'show', expected['sha'] + ':' + name])).hexdigest()
              for name in tests if name.endswith('.ts')}
    require(report['testFilesSha256'] == hashes, 'installed_test_identity')
    scenarios = contract(report)
    text = (ROOT / 'openspec/changes/establish-v1-plugin/specs/task-execution/spec.md').read_text()
    section = text.split('### Requirement: FC-TX-002 ', 1)[1].split('### Requirement: FC-TX-003 ', 1)[0]
    require(set(re.findall(r'#### Scenario: (FC-TX-002-[A-Z-]+)', section)) == set(scenarios), 'spec_coverage')
    require(not output.exists() and not output.is_symlink(), 'output_exists')
    value = {'schema': 'filmcraft-recovery-contract/v1', 'result': 'PASS', 'fixedPlugin': expected,
             'sourceReportSha256': hashlib.sha256(data).hexdigest(), 'scenarios': scenarios,
             'testCounts': report['testCounts'], 'runtimeIdentity': report['native']['runtimeIdentity'],
             'verifierSha256': verifier_hash,
             'platform': platform.system() + '-' + platform.machine(), 'fullV1': 'NOT_PROVEN',
             'scope': 'All FC-TX-002 scenarios in recorded fixed installation; real native lost handoff/continuation, actual SQLite and controlled process faults are separate layers; other hosts/platforms and native binary upgrades remain open'}
    output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return {'result': 'PASS', 'scenarios': len(scenarios), 'reportSha256': hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', dest='report_path', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--repository', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, required=True)
    print(json.dumps(verify(**vars(parser.parse_args()))))
