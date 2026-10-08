#!/usr/bin/env python3
"""复验固定安装身份；篡改只发生于临时复制件，公开报告不含安装路径。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def tree_hash(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if '.git' in relative.parts:
            continue
        if path.is_symlink():
            raise ValueError('installed_symlink')
        if path.is_file():
            digest.update(relative.as_posix().encode() + b'\0')
            digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode() + b'\n')
    return digest.hexdigest()


def verify(host, authority, ref, output):
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ValueError('identity_output_exists')
    verifier = module('fixed_install', ROOT / 'scripts/verify_fixed_install.py')
    expected = verifier.release_entry(ROOT, ref)
    receipt = json.loads((host / 'host-receipt.json').read_text())
    if receipt['result'] != 'PASS' or receipt['plugin'] != expected:
        raise ValueError('fixed_host_receipt_identity_mismatch')
    directories = json.loads((host / 'installed-directories.private.json').read_text())
    if set(directories) != set(expected['skills']):
        raise ValueError('fixed_install_inventory_mismatch')
    installed = Path(directories['filmcraft-use']).resolve().parent.parent
    if not installed.is_relative_to((host / 'host-config').resolve()):
        raise ValueError('fixed_install_outside_isolation')
    helper, helper_identity = verifier.owner_helper(authority)
    if receipt['helper'] != helper_identity:
        raise ValueError('fixed_helper_identity_mismatch')
    before = tree_hash(installed)
    for name, directory in directories.items():
        if Path(directory).resolve() != installed / 'skills' / name:
            raise ValueError('fixed_skill_path_mismatch')
        helper.verify_installed_skill(directory, expected)
    verifier.verify_code_files(installed, expected['codeFilesSha256'])
    facts = module('installed_current_facts', installed / 'scripts/current_facts.py')
    current = facts.update(check=True, root=installed)
    if current != facts.collect(installed):
        raise ValueError('current_facts_nondeterministic')
    if (current['pluginVersion'] != expected['version'] or current['sourceSha'] != expected['skillSourceSha']
            or current['sourceRef'] != expected['skillSourceRef']
            or current['referenceCatalogIdentity']['status'] != 'MATCH'
            or current['currentQualification'] != 'NOT_PROVEN'
            or current['implementation'] != 'in-progress' or current['marketplaceEligible']):
        raise ValueError('current_facts_acceptance_mismatch')
    cases = []
    edits = [
        ('plugin.json', lambda x: x.update(version='0.0.0')),
        ('skills.lock.json', lambda x: x['sources'][0].update(sha='0' * 40)),
        ('skills.lock.json', lambda x: x['sources'][0].update(ref='v0.1.0-dev.0')),
        ('skills/filmcraft-use/scripts/runtime.lock.json', lambda x: x.update(resolvedVersion='0.0.0')),
        ('skills/filmcraft-use/references/commands.json', lambda x: x.update(runtimeSha256='0' * 64)),
        ('docs/skills-source-suite.json', lambda x: x['suite'].update(version='0.0.0')),
        ('docs/current-facts.json', lambda x: x.update(pluginVersion='0.0.0')),
    ]
    with tempfile.TemporaryDirectory(prefix='filmcraft-identity-copy-') as temporary:
        copy = Path(temporary) / 'plugin'
        shutil.copytree(installed, copy, ignore=shutil.ignore_patterns('.git'))
        facts.update(root=copy)
        generated = tree_hash(copy)
        facts.update(root=copy)
        if generated != tree_hash(copy) or generated != before:
            raise ValueError('generated_documents_nondeterministic')
        for index, (relative, edit) in enumerate(edits):
            path = copy / relative
            original = path.read_bytes()
            value = json.loads(original); edit(value)
            path.write_text(json.dumps(value))
            rejected = None
            try:
                helper.verify_installed_skill(copy / 'skills/filmcraft-use', expected)
                facts.update(check=True, root=copy)
            except ValueError as error:
                rejected = str(error)
            finally:
                path.write_bytes(original)
            if rejected is None:
                raise ValueError('tamper_not_rejected: ' + relative)
            cases.append({'case': index + 1, 'file': relative, 'result': 'REJECTED', 'reason': rejected})
        path = copy / 'runtime/filmcraft-cli.lock.json'
        value = json.loads(path.read_text()); value['resolvedVersion'] = 'historical-only'
        path.write_text(json.dumps(value))
        historical = facts.collect(copy)
        if historical['activeRuntime'] != current['activeRuntime'] or historical['currentQualification'] != 'NOT_PROVEN':
            raise ValueError('historical_runtime_promoted')
    old_data = subprocess.check_output(['git', '-C', str(ROOT), 'show',
        'v0.1.0-dev.42:docs/current-facts.json'], timeout=45)
    old = json.loads(old_data)
    if old['referenceCatalogIdentity']['status'] != 'MISMATCH' or old['currentQualification'] != 'NOT_PROVEN':
        raise ValueError('historical_snapshot_rewritten')
    after = tree_hash(installed)
    if before != after:
        raise ValueError('installed_package_modified')
    report = {'schema': 'filmcraft-fixed-identity-live/v1', 'result': 'PASS', 'plugin': expected,
        'helper': helper_identity, 'currentFacts': current, 'tamperCases': cases,
        'deterministicGeneration': 'PASS', 'historicalRuntimeIgnored': 'PASS',
        'historical42': {'sha256': hashlib.sha256(old_data).hexdigest(), 'catalogIdentity': 'MISMATCH',
                         'currentQualification': 'NOT_PROVEN'},
        'installedTreeBefore': before, 'installedTreeAfter': after,
        'notAccepted': ['complete V1', 'automatic model routing', 'all command/mode/platform acceptance']}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.host, args.authority, args.ref, args.output)
    print(json.dumps({'result': result['result'], 'tamperCases': len(result['tamperCases']),
                      'installedFilesUnchanged': True}))
