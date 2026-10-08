#!/usr/bin/env python3
"""仅计算计划身份，兼容既有 Python 入口的摘要；不执行原生操作。"""
import hashlib
import json
from pathlib import Path
import sys


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate_json_key')
        result[key] = value
    return result


def identity(path):
    data = Path(path).read_bytes()
    if len(data) > 16 * 1024 * 1024:
        raise ValueError('plan_too_large')
    plan = json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))
    if not isinstance(plan, dict):
        raise ValueError('plan_object_required')
    def digest(value):
        return hashlib.sha256(value).hexdigest()
    return {'schema': 'filmcraft-plan-identity/v1', 'fileSha256': digest(data),
            'commandPlanSha256': digest(json.dumps(plan, sort_keys=True, allow_nan=False).encode()),
            'workflowPlanSha256': digest(json.dumps(plan, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()),
            'canonicalPlanSha256': digest(json.dumps(plan, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode())}


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('one_plan_file_required')
        print(json.dumps(identity(sys.argv[1])))
    except (ValueError, OSError, RecursionError) as error:
        print(json.dumps({'error': 'invalid_plan', 'detail': str(error)}))
        raise SystemExit(1)
