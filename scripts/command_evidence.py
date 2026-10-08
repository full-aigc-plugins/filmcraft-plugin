#!/usr/bin/env python3
"""投影版本绑定的逐命令证据；不将发现、代表执行或单一模式升级为完整验收。"""
import hashlib
import re

DIMENSIONS = ('discovery', 'parameterValidation', 'positiveExecution',
              'negativeRejection', 'reopen', 'nonTargetPreservation')
STATUSES = ('PASS', 'FAIL', 'NOT_RUN', 'N/A')


def build(rows, binding, evidence):
    """以实际目录和同一固定上下文的观察生成矩阵；观察是证据索引，不代替原始验证。"""
    fields = {'pluginSha', 'sourceSha', 'runtimeSha256', 'runtimeVersion', 'platform', 'mode'}
    if (not isinstance(binding, dict) or set(binding) != fields
            or any(not isinstance(value, str) or not value for value in binding.values())
            or not re.fullmatch('[a-f0-9]{40}', binding['pluginSha'])
            or not re.fullmatch('[a-f0-9]{40}', binding['sourceSha'])
            or not re.fullmatch('[a-f0-9]{64}', binding['runtimeSha256'])
            or binding['mode'] not in ('headless', 'bridge')
            or not isinstance(evidence, dict) or evidence.get('binding') != binding):
        raise ValueError('command_evidence_binding_mismatch')
    if (not isinstance(rows, list) or not rows or any(not isinstance(row, dict)
            or not isinstance(row.get('id'), str) or not row['id']
            or not isinstance(row.get('params'), str) or type(row.get('enabled')) is not bool for row in rows)
            or len({row['id'] for row in rows}) != len(rows)):
        raise ValueError('command_evidence_catalog_invalid')
    observations = evidence.get('observations')
    if not isinstance(observations, list):
        raise ValueError('command_evidence_observation_invalid')
    indexed = {row['id']: {'id': row['id'], 'parameterContractSha256': hashlib.sha256(row['params'].encode()).hexdigest(),
        'enabledAtDiscovery': row['enabled'], 'dimensions': {dimension:
            {'status': 'PASS', 'evidence': 'actual-native-catalog', 'scope': 'registry discovery only'}
            if dimension == 'discovery' else {'status': 'NOT_RUN', 'reason': 'no current-context observation'}
            for dimension in DIMENSIONS}} for row in rows}
    seen = set()
    for observation in observations:
        if (not isinstance(observation, dict)
                or set(observation) - {'command', 'dimension', 'status', 'evidence', 'scope', 'reason'}
                or not isinstance(observation.get('command'), str) or observation['command'] not in indexed
                or observation.get('dimension') not in DIMENSIONS[1:]
                or observation.get('status') not in STATUSES
                or not isinstance(observation.get('scope'), str) or not observation['scope']
                or (observation['status'] in ('PASS', 'FAIL') and
                    (not isinstance(observation.get('evidence'), str) or not observation['evidence']))
                or (observation['status'] in ('N/A', 'NOT_RUN') and
                    (not isinstance(observation.get('reason'), str) or not observation['reason']))):
            raise ValueError('command_evidence_observation_invalid')
        key = observation['command'], observation['dimension']
        if key in seen:
            raise ValueError('command_evidence_duplicate_observation')
        seen.add(key)
        indexed[key[0]]['dimensions'][key[1]] = {name: value for name, value in observation.items()
                                                if name not in ('command', 'dimension')}
    commands = list(indexed.values())
    summary = {dimension: {status: sum(row['dimensions'][dimension]['status'] == status for row in commands)
                           for status in STATUSES} for dimension in DIMENSIONS}
    return {'schema': 'filmcraft-command-dimensions/v1', 'binding': binding, 'commands': commands,
            'summary': summary, 'completeCommandAcceptance': 'NOT_PROVEN',
            'scope': 'separate dimensions in the bound context; PASS observations require their referenced raw evidence; no aggregate availability rate'}
