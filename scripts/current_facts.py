#!/usr/bin/env python3
"""从固定技能身份生成当前事实，保留历史记录和未验证状态。"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- FILMCRAFT_CURRENT_FACTS_START -->'
END = '<!-- FILMCRAFT_CURRENT_FACTS_END -->'


def read(root, relative):
    return json.loads((root / relative).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False).encode()).hexdigest()


def collect(root=ROOT):
    root = Path(root)
    manifest = read(root, 'plugin.json')
    sources = read(root, 'skills.lock.json')['sources']
    if manifest['name'] != 'filmcraft' or len(sources) != 1:
        raise ValueError('plugin_identity_mismatch')
    source = sources[0]
    plan = read(root, 'docs/skills-source-plan.json')
    if (plan['package'], plan['sourceRef'], plan['sourceSha']) != (source['package'], source['ref'], source['sha']):
        raise ValueError('source_plan_identity_mismatch')
    snapshot = read(root, 'docs/skills-source-suite.json')
    suite = snapshot['suite']
    if (snapshot['sourceRef'], snapshot['sourceSha'], suite['pluginId'], 'v' + suite['version']) != (
            source['ref'], source['sha'], manifest['name'], source['ref']):
        raise ValueError('source_suite_identity_mismatch')
    names = [entry['name'] for entry in suite['skills']]
    if names != source['skills'] or names != plan['skills'] or len(names) != len(set(names)):
        raise ValueError('skill_list_mismatch')
    if snapshot['suiteSha256'] != digest(suite):
        raise ValueError('source_suite_digest_mismatch')
    home = root / 'skills/filmcraft-use'
    runtime = read(home, 'scripts/runtime.lock.json')
    desktop = read(home, 'scripts/desktop.lock.json')
    coverage = read(home, 'references/command-coverage.json')
    commands = read(home, 'references/commands.json')
    binary = runtime['artifacts']['darwin-arm64']['binarySha256']
    if coverage['pluginId'] != manifest['name'] or coverage['runtimeSha256'] != binary:
        raise ValueError('catalog_runtime_mismatch')
    ids = [entry['id'] for entry in coverage['commands']]
    if len(ids) != len(set(ids)) or set(ids) != {entry['id'] for entry in commands['commands']}:
        raise ValueError('command_catalog_mismatch')
    if any(entry['ownerSkill'] not in names for entry in coverage['commands']):
        raise ValueError('command_owner_mismatch')
    for name in names:
        skill = root / 'skills' / name
        if (read(skill, 'scripts/runtime.lock.json') != runtime
                or read(skill, 'scripts/desktop.lock.json') != desktop):
            raise ValueError('standalone_runtime_drift: ' + name)
        text = (skill / 'SKILL.md').read_text()
        if not re.search(r'^name: ' + re.escape(name) + r'\s*$', text, re.M):
            raise ValueError('skill_name_mismatch: ' + name)
    if any(entry['commandCount'] != len(ids) for entry in suite['skills']
           if entry['kind'] in ('router', 'cli', 'setup')):
        raise ValueError('suite_command_count_mismatch')
    status = read(root, 'project-status.json')
    historical = read(root, 'runtime/filmcraft-cli.lock.json')
    return {
        'schema': 'filmcraft-current-facts/v1',
        'pluginId': manifest['name'], 'pluginVersion': manifest['version'],
        'sourcePackage': source['package'], 'sourceRef': source['ref'], 'sourceSha': source['sha'],
        'suiteSha256': snapshot['suiteSha256'], 'skillCount': len(names), 'commandCount': len(ids),
        'referenceCatalogIdentity': {
            'path': 'skills/filmcraft-use/references/commands.json',
            'version': commands['runtimeVersion'], 'binarySha256': commands['runtimeSha256'],
            'status': 'MATCH' if (commands['runtimeSha256'] == binary
                                  and commands['runtimeVersion'] == runtime['resolvedVersion']) else 'MISMATCH'},
        'activeRuntime': {'role': 'skill-execution-authority',
                          'path': 'skills/filmcraft-use/scripts/runtime.lock.json',
                          'version': runtime['resolvedVersion'], 'releaseRef': runtime['releaseRef'],
                          'platform': 'darwin-arm64', 'binarySha256': binary},
        'desktop': {'role': 'bridge-desktop-identity', 'version': desktop['version'],
                    'binarySha256': desktop['binarySha256']},
        'historicalRuntime': {'role': 'historical-bootstrap-baseline',
                              'path': 'runtime/filmcraft-cli.lock.json',
                              'version': historical['resolvedVersion']},
        'implementation': status['implementation'],
        'marketplaceEligible': status['marketplaceEligible'],
        'supportedPluginHosts': status['supportedPluginHosts'],
        'completeCommandAcceptance': status['completeCommandAcceptance'],
        # 既有报告有各自版本/范围；不能从历史证据指针推导当前组合完整通过。
        'currentQualification': 'NOT_PROVEN',
        'qualificationScope': 'full current plugin/skill/runtime/host combination',
        'historicalEvidenceReferences': sorted({value for key, value in status.items()
                                               if key.endswith('Evidence') and isinstance(value, str)}),
    }


def render(value, language):
    identity = (f"`{value['pluginVersion']}` / `{value['sourcePackage']}@{value['sourceRef']}`; "
                f"{value['skillCount']} / {value['commandCount']}")
    runtime = f"`{value['activeRuntime']['version']}` / `{value['desktop']['version']}`"
    if language == 'en':
        lines = ['Generated current facts: plugin / skill source; skills / discovered commands: ' + identity + '.',
                 'Execution CLI / bridge desktop: ' + runtime + '; root runtime lock is historical only.',
                 'Implementation: `' + value['implementation'] + '`; full current-combination qualification: `NOT_PROVEN`. '
                 'Discovery counts and historical reports do not imply current execution or release acceptance. '
                 '[Machine-readable identities and scope](docs/current-facts.json).',
                 'Reference catalog identity: `' + value['referenceCatalogIdentity']['status'] + '`; '
                 'a mismatch remains visible and does not override the execution runtime lock.']
    else:
        lines = ['生成的当前事实：插件 / 技能源；技能数 / 已发现命令数：' + identity + '。',
                 '执行 CLI / bridge 桌面：' + runtime + '；根运行时锁仅作历史基线。',
                 '实现状态：`' + value['implementation'] + '`；当前完整组合验收：`NOT_PROVEN`。'
                 '目录数量及历史报告不推导为当前执行或发行通过。'
                 '[机器可读身份与范围](docs/current-facts.json)。',
                 '参考目录身份：`' + value['referenceCatalogIdentity']['status'] + '`；'
                 '不一致须显式保留，不能覆盖实际执行运行时锁。']
    return START + '\n\n' + '\n\n'.join(lines) + '\n\n' + END


def update(check=False, root=ROOT):
    root = Path(root)
    value = collect(root)
    target = root / 'docs/current-facts.json'
    encoded = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    errors = []
    if check:
        if not target.is_file() or target.read_text() != encoded:
            errors.append('current_facts_snapshot_stale')
    else:
        target.write_text(encoded)
    for filename, language in (('README.md', 'en'), ('README.zh-CN.md', 'zh-CN')):
        path = root / filename
        text, generated = path.read_text(), render(value, language)
        if START in text or END in text:
            if text.count(START) != 1 or text.count(END) != 1:
                raise ValueError('duplicate_current_facts_markers: ' + filename)
            start, end = text.index(START), text.index(END) + len(END)
            if start >= end:
                raise ValueError('invalid_current_facts_markers: ' + filename)
            desired = text[:start] + generated + text[end:]
        else:
            first = text.index('\n') + 1
            desired = text[:first] + '\n' + generated + '\n' + text[first:]
        if check:
            if text != desired:
                errors.append('current_facts_readme_stale: ' + filename)
        else:
            path.write_text(desired)
    if errors:
        raise ValueError('; '.join(errors))
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        value = update(args.check)
        print(json.dumps({'status': 'passed', 'scope': 'current identity consistency only',
                          'skills': value['skillCount'], 'commands': value['commandCount']}))
    except (ValueError, KeyError, OSError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}))
        raise SystemExit(1)
