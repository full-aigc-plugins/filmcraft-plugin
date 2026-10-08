#!/usr/bin/env python3
"""在隔离 Codex 配置验证单个固定 FilmCraft；复用固定 ArtCraft 宿主读取和技能核验。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import types

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/full-aigc-plugins/filmcraft-plugin.git'


def validate_ref(ref):
    if not isinstance(ref, str) or not re.fullmatch(r'v0\.1\.0-dev\.\d+', ref):
        raise ValueError('immutable_filmcraft_ref_required')


def remote_commit(text, ref):
    """同时支持轻量与附注标签，比较解引用提交而非标签对象。"""
    validate_ref(ref)
    tag, rows = 'refs/tags/' + ref, {}
    for line in text.splitlines():
        pair = line.split()
        if (len(pair) != 2 or not re.fullmatch('[a-f0-9]{40}', pair[0])
                or pair[1] not in (tag, tag + '^{}') or pair[1] in rows):
            raise ValueError('remote_tag_invalid')
        rows[pair[1]] = pair[0]
    if tag not in rows:
        raise ValueError('remote_tag_invalid')
    return rows.get(tag + '^{}', rows[tag])


def entry_from_objects(manifest_data, lock_data, commit, ref):
    validate_ref(ref)
    manifest, lock = json.loads(manifest_data), json.loads(lock_data)
    if not isinstance(manifest, dict) or not isinstance(lock, dict):
        raise ValueError('fixed_install_identity_invalid')
    sources = lock.get('sources', []) if isinstance(lock, dict) else []
    source = sources[0] if isinstance(sources, list) and len(sources) == 1 else {}
    if not isinstance(source, dict):
        raise ValueError('fixed_install_identity_invalid')
    names = source.get('skills', []) if isinstance(source, dict) else []
    hashes = source.get('sha256', {}) if isinstance(source, dict) else {}
    if (not isinstance(manifest, dict) or manifest.get('name') != 'filmcraft'
            or manifest.get('version') != ref.removeprefix('v') or lock.get('version') != 1
            or not isinstance(commit, str) or not re.fullmatch('[a-f0-9]{40}', commit)
            or source.get('package') != 'filmcraft-skills'
            or source.get('repo') != 'https://github.com/full-aigc-skills/filmcraft-skills.git'
            or not isinstance(source.get('sha'), str) or not re.fullmatch('[a-f0-9]{40}', source['sha'])
            or not isinstance(source.get('ref'), str) or not re.fullmatch(r'v0\.1\.0-dev\.\d+', source['ref'])
            or not isinstance(names, list) or not names or any(not isinstance(name, str)
                or not re.fullmatch(r'filmcraft-[a-z0-9]+(?:-[a-z0-9]+)*', name) for name in names)
            or len(set(names)) != len(names) or not isinstance(hashes, dict) or set(hashes) != set(names)
            or 'filmcraft-use' not in names or any(not isinstance(value, str)
                or not re.fullmatch('[a-f0-9]{64}', value) for value in hashes.values())):
        raise ValueError('fixed_install_identity_invalid')
    return {'repository': REPOSITORY, 'version': manifest['version'], 'ref': ref, 'sha': commit,
            'skillSourceSha': source['sha'], 'skillSourceRef': source['ref'],
            'pluginManifestSha256': hashlib.sha256(manifest_data).hexdigest(),
            'skillSha256': hashes['filmcraft-use'], 'skills': hashes}


def release_entry(repository, ref):
    validate_ref(ref)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repository), *args], timeout=45)
    commit = git('rev-parse', 'refs/tags/' + ref + '^{commit}').decode().strip()
    result = entry_from_objects(git('show', commit + ':plugin.json'), git('show', commit + ':skills.lock.json'), commit, ref)
    names = git('ls-tree', '-r', '--name-only', commit, '--', 'src', 'scripts', 'package.json').decode().splitlines()
    result['codeFilesSha256'] = {name: hashlib.sha256(git('show', commit + ':' + name)).hexdigest() for name in names}
    return result


def owner_helper(authority):
    """只读取已锁定提交的共享实现，不依赖所有者工作树内容。"""
    reference = json.loads((ROOT / 'docs/contracts-reference.json').read_text())
    spec = importlib.util.spec_from_file_location('filmcraft_contract_reference', ROOT / 'scripts/contract_reference.py')
    contract = importlib.util.module_from_spec(spec); spec.loader.exec_module(contract)
    if contract.validate_reference(reference, authority):
        raise ValueError('fixed_host_helper_authority_invalid')
    commit = reference['source']['sha']
    data = subprocess.check_output(['git', '-C', str(authority), 'show', commit + ':scripts/verify_codex_host.py'], timeout=45)
    module = types.ModuleType('filmcraft_pinned_host_helper')
    exec(compile(data, commit + '/verify_codex_host.py', 'exec'), module.__dict__)
    return module, {'commit': commit, 'path': 'scripts/verify_codex_host.py', 'sha256': hashlib.sha256(data).hexdigest()}


def verify_code_files(directory, expected):
    root = Path(directory).resolve()
    for name, digest in expected.items():
        path = root / name
        if (not path.resolve().is_relative_to(root) or not path.is_file()
                or path.is_symlink() or any(p.is_symlink() for p in path.parents if p.is_relative_to(root))
                or path.stat().st_size > 16 * 1024 * 1024
                or hashlib.sha256(path.read_bytes()).hexdigest() != digest):
            raise ValueError('installed_code_identity_mismatch')


def verify(codex, repository, authority, ref, output):
    validate_ref(ref)
    root = Path(output).absolute()
    if root.exists() or root.is_symlink():
        raise ValueError('fixed_install_output_exists')
    expected = release_entry(repository, ref)
    remote = subprocess.check_output(['git', 'ls-remote', REPOSITORY, 'refs/tags/' + ref,
                                      'refs/tags/' + ref + '^{}'], text=True, timeout=45)
    if remote_commit(remote, ref) != expected['sha']:
        raise ValueError('fixed_install_remote_commit_mismatch')
    helper, helper_identity = owner_helper(authority)
    codex = str(Path(codex).resolve(strict=True))
    root.mkdir(mode=0o700)
    home = root / 'host-config'; home.mkdir(mode=0o700)
    environment = {**os.environ, 'CODEX_HOME': str(home)}
    def run(*args):
        result = subprocess.run([codex, *args], cwd=root, env=environment, capture_output=True, text=True, timeout=180)
        if result.returncode:
            (root / 'host-command-error.private.log').write_text(result.stdout + '\n' + result.stderr)
            raise RuntimeError('fixed_host_command_failed: ' + args[0])
        return result.stdout
    version = run('--version').strip()
    market = root / 'market'; manifest = market / '.agents/plugins/marketplace.json'
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({'name': 'filmcraft-fixed-verification', 'description': 'Isolated fixed development verification',
        'owner': {'name': 'Full AIGC Plugins'}, 'plugins': [{'name': 'filmcraft',
        'source': {'source': 'url', 'url': REPOSITORY, 'ref': ref},
        'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_USE'},
        'version': expected['version'], 'category': 'Creativity'}]}))
    run('plugin', 'marketplace', 'add', str(market), '--json')
    run('plugin', 'add', 'filmcraft@filmcraft-fixed-verification', '--json')
    initialization, response = helper.discover(codex, root, environment)
    rows = response.get('data', [])
    if any(row.get('errors') for row in rows):
        raise ValueError('fixed_host_skill_loading_errors')
    found = [skill for row in rows for skill in row.get('skills', []) if skill.get('name', '').startswith('filmcraft:')]
    if ({skill['name'] for skill in found} != {'filmcraft:' + name for name in expected['skills']}
            or len(found) != len(expected['skills'])):
        raise ValueError('fixed_host_inventory_mismatch')
    directories, skills = {}, []
    for skill in found:
        directory = Path(skill['path']).resolve().parent
        if not skill.get('enabled') or not directory.is_relative_to(home.resolve()):
            raise ValueError('fixed_host_skill_outside_isolation')
        helper.verify_installed_skill(directory, expected)
        verify_code_files(directory.parent.parent, expected['codeFilesSha256'])
        directories[directory.name] = str(directory)
        skills.append({'name': skill['name'], 'sha256': expected['skills'][directory.name], 'enabled': True})
    receipt = {'schema': 'filmcraft-fixed-host-verification/v1', 'result': 'PASS',
        'codexVersion': version, 'userAgent': initialization.get('userAgent'), 'platform': os.uname().sysname.lower() + '-' + os.uname().machine,
        'plugin': expected, 'helper': helper_identity, 'skills': sorted(skills, key=lambda value: value['name']),
        'loadingErrors': 0, 'scope': 'fixed public-tag isolated install, executable files, immutable skill identities and real app-server discovery',
        'notAccepted': ['model dispatch and routing accuracy', 'native workflow execution', 'other hosts/platforms', 'complete V1']}
    (root / 'installed-directories.private.json').write_text(json.dumps(directories, indent=2) + '\n')
    (root / 'host-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', required=True)
    parser.add_argument('--repository', type=Path, default=ROOT)
    parser.add_argument('--authority', type=Path, required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(verify(arguments.codex, arguments.repository, arguments.authority, arguments.ref, arguments.output), ensure_ascii=False))
