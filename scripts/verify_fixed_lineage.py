#!/usr/bin/env python3
"""核验固定宿主快照后执行其自带 Node 原生血缘验收，公共报告脱敏。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def verify(host, authority, ref, output, python, node):
    fixed = module(ROOT / 'scripts/verify_fixed_install.py', 'lineage_fixed_install')
    expected = fixed.release_entry(ROOT, ref)
    receipt = json.loads((host / 'host-receipt.json').read_text())
    directories = json.loads((host / 'installed-directories.private.json').read_text())
    if receipt['result'] != 'PASS' or receipt['plugin'] != expected or set(directories) != set(expected['skills']):
        raise ValueError('fixed_host_mismatch')
    helper, identity = fixed.owner_helper(authority)
    if receipt['helper'] != identity: raise ValueError('fixed_helper_mismatch')
    skill = Path(directories['filmcraft-use']).resolve(); plugin = skill.parent.parent
    if not skill.is_relative_to((host / 'host-config').resolve()): raise ValueError('installed_path_outside_host')
    for name, directory in directories.items():
        if Path(directory).resolve() != skill.parent / name: raise ValueError('installed_skill_path_mismatch')
        helper.verify_installed_skill(directory, expected)
    fixed.verify_code_files(plugin, expected['codeFilesSha256'])
    if output.exists() or output.is_symlink(): raise ValueError('lineage_output_exists')
    output.mkdir(mode=0o700)
    result = subprocess.run([node, str(plugin / 'scripts/verify_fixed_lineage.ts'), '--output', str(output / 'work'),
        '--python', python, '--source', expected['skillSourceSha']], capture_output=True, text=True, timeout=900)
    def safe(text):
        return text.replace(str(output.resolve()), '[TEST_ROOT]').replace(str(output), '[TEST_ROOT]').replace(str(Path.home()), '[USER_HOME]')
    (output / 'native.log').write_text(safe(result.stdout + result.stderr))
    if result.returncode: raise ValueError('fixed_lineage_native_failed: see native.log')
    raw = json.loads((output / 'work/report.private.json').read_text())
    if (raw['result'] != 'PASS' or raw['sourceRevision'] != expected['skillSourceSha']
            or raw['pluginVersion'] != expected['version'] or not raw['installedSkillUnchanged']
            or len(raw['cases']) != 10): raise ValueError('lineage_result_mismatch')
    protocol = module(ROOT / 'scripts/validate_protocol_mapping.py', 'lineage_protocol_mapping')
    protocol_result = protocol.validate(output / 'work/report.private.json', authority)
    for name, directory in directories.items(): helper.verify_installed_skill(directory, expected)
    fixed.verify_code_files(plugin, expected['codeFilesSha256'])
    raw['fixedPlugin'] = expected; raw['host'] = {'codexVersion': receipt['codexVersion'], 'skillCount': len(directories)}
    raw['protocolValidation'] = protocol_result; raw['allInstalledFilesUnchanged'] = True
    raw['digestSemantics'] = 'Archived SHA256 covers original private CAS bytes, checked against actual records. Public projections are redacted and do not claim original-byte digests.'
    (output / 'report.json').write_text(safe(json.dumps(raw, ensure_ascii=False, indent=2)) + '\n')
    return {'result': 'PASS', 'nativeCases': len(raw['cases']), 'installedSkillsUnchanged': len(directories),
            'protocolObjects': protocol_result['validated'], 'reportSha256': hashlib.sha256((output / 'report.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--python', required=True)
    parser.add_argument('--node', required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.host, args.authority, args.ref, args.output, args.python, args.node)))
