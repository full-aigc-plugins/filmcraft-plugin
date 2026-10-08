#!/usr/bin/env python3
"""绑定真实固定宿主与全部安装字节的首次工作流准入验收。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_fixed_install import release_entry, owner_helper, verify_code_files
from media_matrix import digest

CASES = {'ungranted-exact-subject', 'actual-cli-authorized-native-create',
         'existing-valid-grant-idempotent-reuse', 'revoked-grant-refuses-even-reuse',
         'authorized-runtime-drift-before-registration', 'revocation-after-intent-before-spawn',
         'actual-native-revision-and-stale-source-conflict'}


def validate_report(report, expected, adapter_skill_sha256):
    if (report.get('schema') != 'filmcraft-workflow-admission-verification/v1'
            or report.get('result') != 'PASS' or report.get('layer') != 'actual-native'
            or report.get('pluginVersion') != expected['version']
            or report.get('sourceRevision') != expected['skillSourceSha']
            or report.get('skillSha256') != adapter_skill_sha256
            or report.get('skillHashAlgorithm') != 'path-nul-raw-bytes-nul'
            or report.get('installedSkillPreserved') is not True
            or report.get('fullV1') != 'NOT_PROVEN'
            or len(report.get('cases', [])) != len(CASES)
            or {row.get('id') for row in report.get('cases', [])} != CASES
            or any(row.get('status') != 'PASS' for row in report.get('cases', []))):
        raise ValueError('admission_identity_or_cases_incomplete')
    rows = {row['id']: row for row in report['cases']}
    if (rows['ungranted-exact-subject'].get('attempts') != 0
            or rows['ungranted-exact-subject'].get('outputExists') is not False
            or rows['actual-cli-authorized-native-create'].get('state') != 'verifying'
            or rows['actual-cli-authorized-native-create'].get('stopped') is not True
            or rows['existing-valid-grant-idempotent-reuse'].get('attempts') != 1
            or rows['revoked-grant-refuses-even-reuse'].get('originalPreserved') is not True
            or rows['authorized-runtime-drift-before-registration'].get('attempts') != 0
            or rows['revocation-after-intent-before-spawn'].get('nativeLaunched') is not False
            or rows['revocation-after-intent-before-spawn'].get('state') != 'failed'
            or rows['actual-native-revision-and-stale-source-conflict'].get('staleAttempts') != 0
            or rows['actual-native-revision-and-stale-source-conflict'].get('sourcePreserved') is not True):
        raise ValueError('admission_observations_incomplete')


def verify(host, repository, authority, ref, output, node, python):
    host = Path(host).resolve(); output = Path(output).absolute()
    if output.exists() or output.is_symlink(): raise ValueError('output_exists')
    expected = release_entry(repository, ref)
    receipt = json.loads((host / 'host-receipt.json').read_text())
    if receipt.get('result') != 'PASS' or receipt.get('plugin') != expected or receipt.get('loadingErrors') != 0:
        raise ValueError('fixed_host_mismatch')
    directories = {name: Path(path).resolve() for name, path in json.loads((host / 'installed-directories.private.json').read_text()).items()}
    if set(directories) != set(expected['skills']): raise ValueError('fixed_skill_inventory_mismatch')
    helper, identity = owner_helper(authority)
    if receipt.get('helper') != identity: raise ValueError('fixed_helper_identity_mismatch')
    def check_files():
        for path in directories.values():
            if not path.is_relative_to(host / 'host-config'): raise ValueError('fixed_skill_outside_host')
            helper.verify_installed_skill(path, expected)
            verify_code_files(path.parent.parent, expected['codeFilesSha256'])
    check_files()
    core = directories['filmcraft-use'].parent.parent
    result = subprocess.run([node, str(core / 'scripts/verify_workflow_admission.ts'), '--output', str(output), '--python', python],
                            capture_output=True, text=True, timeout=300)
    if result.returncode:
        if output.is_dir(): (output / 'failed.private.log').write_text(result.stdout + result.stderr)
        raise ValueError('fixed_native_admission_failed')
    check_files()
    adapter_digest = hashlib.sha256()
    skill = directories['filmcraft-use']
    for path in sorted((p for p in skill.rglob('*') if p.is_file() and '__pycache__' not in p.parts), key=lambda p: str(p)):
        adapter_digest.update(path.relative_to(skill).as_posix().encode() + b'\0')
        adapter_digest.update(path.read_bytes()); adapter_digest.update(b'\0')
    report = json.loads((output / 'report.json').read_text())
    validate_report(report, expected, adapter_digest.hexdigest())
    lock = json.loads((directories['filmcraft-use'] / 'scripts/runtime.lock.json').read_text())
    runtime = report.get('runtimeIdentity', {})
    artifact = lock['artifacts'][report['platform']]
    if runtime.get('sha256') != artifact['binarySha256'] or runtime.get('cliVersion') != lock['resolvedVersion']:
        raise ValueError('fixed_runtime_mismatch')
    report.update(layer='fixed-installed-native', plugin=expected, hostReceiptSha256=digest(host / 'host-receipt.json'),
                  skillVendorSha256=expected['skills']['filmcraft-use'],
                  skillVendorHashAlgorithm='vendor-path-nul-file-sha256-newline', installedSkillCount=len(directories), allInstalledSkillsUnchanged=True, allInstalledCodeUnchanged=True)
    (output / 'fixed-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('host', 'repository', 'authority', 'output'): parser.add_argument('--' + name, type=Path, required=True)
    for name in ('ref', 'node', 'python'): parser.add_argument('--' + name, required=True)
    report = verify(**vars(parser.parse_args()))
    print(json.dumps({'result': report['result'], 'cases': len(report['cases']), 'installedSkills': report['installedSkillCount']}))
