#!/usr/bin/env python3
"""固定公开标签安装的恢复矩阵、原生继续、旧版降级拒绝与公共协议验收。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def verify(host, previous_host, authority, ref, output, python, node):
    fixed = module(ROOT / 'scripts/verify_fixed_install.py', 'recovery_fixed')
    helper, helper_identity = fixed.owner_helper(authority)
    def install_identity(path, version):
        receipt = json.loads((path / 'host-receipt.json').read_text())
        expected = fixed.release_entry(ROOT, version)
        directories = json.loads((path / 'installed-directories.private.json').read_text())
        if (receipt['result'] != 'PASS' or receipt['plugin'] != expected or receipt['helper'] != helper_identity
                or set(directories) != set(expected['skills'])):
            raise ValueError('fixed_host_mismatch')
        skill = Path(directories['filmcraft-use']).resolve()
        if not skill.is_relative_to((path / 'host-config').resolve()): raise ValueError('installed_path_outside_host')
        for name, directory in directories.items():
            if Path(directory).resolve() != skill.parent / name: raise ValueError('installed_skill_path_mismatch')
            helper.verify_installed_skill(directory, expected)
        fixed.verify_code_files(skill.parent.parent, expected['codeFilesSha256'])
        return receipt, expected, skill.parent.parent
    receipt, expected, plugin = install_identity(host, ref)
    old_receipt, old_expected, old_plugin = install_identity(previous_host, 'v0.1.0-dev.45')
    tests = sorted((plugin / 'test/harness').glob('*.ts')); test_hashes = {}
    for path in tests:
        relative = str(path.relative_to(plugin))
        data = subprocess.check_output(['git', '-C', str(ROOT), 'show', expected['sha'] + ':' + relative])
        if path.read_bytes() != data: raise ValueError('installed_test_identity_mismatch')
        test_hashes[relative] = hashlib.sha256(data).hexdigest()
    if output.exists() or output.is_symlink(): raise ValueError('recovery_output_exists')
    output.mkdir(mode=0o700); temporary = output / 'private-tmp'; temporary.mkdir(mode=0o700)
    native = output / 'native.private.json'; matrix = output / 'matrix.private.jsonl'
    environment = {**os.environ, 'TMPDIR': str(temporary.resolve()), 'FILMCRAFT_NATIVE_HARNESS': '1',
        'FILMCRAFT_NATIVE_SKILL': str(plugin / 'skills/filmcraft-use'), 'FILMCRAFT_NATIVE_SOURCE_REVISION': expected['skillSourceSha'],
        'FILMCRAFT_PYTHON': python, 'FILMCRAFT_NATIVE_RUNTIME_HOME': str(output / 'runtime'),
        'FILMCRAFT_PREVIOUS_CORE': str(old_plugin), 'FILMCRAFT_HARNESS_REPORT': str(native),
        'FILMCRAFT_RECOVERY_EVIDENCE': str(matrix)}
    result = subprocess.run([node, '--test', '--test-concurrency=1', *[str(p) for p in tests if p.name.endswith('.test.ts')]],
        cwd=plugin, env=environment, capture_output=True, text=True, timeout=900)
    def safe(text):
        for path, label in [(output.resolve(), '[TEST_ROOT]'), (host.resolve(), '[FIXED_HOST]'),
                            (previous_host.resolve(), '[PREVIOUS_HOST]'), (Path.home(), '[USER_HOME]')]:
            text = text.replace(str(path), label)
        return re.sub(r'(?:/private)?/var/folders/[^\s"\']+', '[TEMP_PATH]', text)
    log = result.stdout + result.stderr
    (output / 'native.log').write_text(safe(log))
    if result.returncode: raise ValueError('fixed_recovery_tests_failed: see native.log')
    counts = {}
    for key in ['tests', 'pass', 'fail', 'skipped']:
        found = re.search(r'(?:# |ℹ )' + key + r' (\d+)', log)
        if not found: raise ValueError('missing_test_counts')
        counts[key] = int(found.group(1))
    if counts['fail'] or counts['skipped'] or counts['tests'] != counts['pass']: raise ValueError('recovery_test_not_passed')
    rows = [json.loads(line) for line in matrix.read_text().splitlines()]
    required = {'readonly-wal-and-missing-receipts','missing-and-damaged-ledgers','lost-reply-and-old-epoch',
        'expired-recovery-owner','repeat-repair','two-recovery-executors','host-exited-child-alive',
        'schema1-upgrade-rollback','schema2-upgrade-rollback','rollback-preserves-new-records','inspection-concurrent-write',
        'actual-native-repair-and-continuation','actual-previous-version-downgrade-refusal','expired-revoked-authorization'}
    if not required.issubset({row['scenario'] for row in rows}): raise ValueError('recovery_matrix_incomplete')
    readonly = {'readonly-wal-and-missing-receipts','missing-and-damaged-ledgers','repeat-repair',
                'host-exited-child-alive','rollback-preserves-new-records','actual-previous-version-downgrade-refusal','expired-revoked-authorization'}
    for row in rows:
        if row['scenario'] in readonly and row['before'] != row['after']: raise ValueError('original_files_changed')
    native_result = json.loads(native.read_text())
    if (native_result['result'] != 'PASS' or native_result['sourceRevision'] != expected['skillSourceSha']
            or native_result['runtimeIdentity']['pluginVersion'] != expected['version']
            or native_result['continuation']['originalAttemptCount'] != 1
            or native_result['continuation']['childAttemptCount'] != 1
            or not native_result['continuation']['reused']): raise ValueError('native_continuation_mismatch')
    protocol = module(ROOT / 'scripts/validate_protocol_mapping.py', 'recovery_protocol').validate(native, authority)
    install_identity(host, ref); install_identity(previous_host, 'v0.1.0-dev.45')
    report = {'schema': 'filmcraft-fixed-recovery-acceptance/v1', 'result': 'PASS', 'fixedPlugin': expected,
        'previousFixedPlugin': old_expected, 'codexVersion': receipt['codexVersion'], 'helper': helper_identity,
        'executionLayer': 'actual installed public-tag test and implementation files; fresh native runtime',
        'testFilesSha256': test_hashes, 'testCounts': counts, 'matrix': rows, 'native': native_result,
        'protocolValidation': protocol, 'allInstalledFilesUnchanged': True,
        'technicalAcceptance': 'NOT_RUN', 'creativeAcceptance': 'NOT_RUN', 'userAcceptance': 'NOT_RUN', 'fullV1': 'INCOMPLETE',
        'scope': 'FC-TX-002 recovery tasks 9.16-9.18; state schema1/2 to3 and compatible rollback only; not runtime upgrade or complete Harness',
        'digestSemantics': 'Original private file digests were asserted in actual runs. Public projections are redacted; their own evidence hashes are recorded separately.'}
    (output / 'report.json').write_text(safe(json.dumps(report, ensure_ascii=False, indent=2)) + '\n')
    return {'result': 'PASS', 'tests': counts, 'scenarios': len(rows), 'protocol': protocol['validated'],
            'reportSha256': hashlib.sha256((output / 'report.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['host', 'previous-host', 'authority', 'output']: parser.add_argument('--' + name, type=Path, required=True)
    for name in ['ref', 'python', 'node']: parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.host, args.previous_host, args.authority, args.ref, args.output, args.python, args.node)))
