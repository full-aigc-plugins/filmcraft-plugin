#!/usr/bin/env python3
"""只读校验领域映射报告；公共 schema 仅从固定 ArtCraft Git 对象读取，不复制。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from contract_reference import validate_reference


def validate(report_path, authority):
    """返回固定协议身份与各公共对象检查结果；不改源码、账本或报告。"""
    reference = json.loads((Path(__file__).resolve().parents[1] / 'docs/contracts-reference.json').read_text())
    errors = validate_reference(reference, authority)
    if errors:
        raise ValueError('; '.join(errors))
    try:
        import jsonschema
    except ImportError as error:
        raise ValueError('jsonschema unavailable; protocol verification NOT_RUN') from error
    data = report_path.read_bytes()
    if len(data) > 16 * 1024 * 1024:
        raise ValueError('report too large')
    report = json.loads(data)
    counts = {}
    for name, key in [('publicTasks', 'taskSchema'), ('publicArtifacts', 'artifactSchema')]:
        objects = report.get(name)
        if not isinstance(objects, list) or not objects:
            raise ValueError('nonempty mapping objects required: ' + name)
        item = reference['files'][key]
        schema_bytes = subprocess.check_output(['git', 'show', reference['source']['sha'] + ':' + item['path']], cwd=authority)
        if hashlib.sha256(schema_bytes).hexdigest() != item['sha256']:
            raise ValueError('fixed schema digest mismatch')
        schema = json.loads(schema_bytes)
        jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        for index, value in enumerate(objects):
            problems = sorted(validator.iter_errors(value), key=lambda error: str(error.json_path))
            if problems:
                raise ValueError(f'{name}[{index}] {problems[0].json_path}: {problems[0].message}')
        counts[name] = len(objects)
    return {'status': 'passed', 'scope': 'fixed owner schema mapping only; no host, budget or quality acceptance',
            'authority': reference['source'], 'schemaSha256': {key: reference['files'][key]['sha256'] for key in ('taskSchema', 'artifactSchema')},
            'validated': counts}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--authority', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.report, args.authority)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        result = {'status': 'failed', 'error': str(error)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result['status'] != 'passed')
