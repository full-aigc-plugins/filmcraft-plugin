"""完整反射命令接入受核验工作流；交付仍由原生保存、重开及依赖门禁决定。"""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('craft_native_commands', Path(__file__).with_name('commands.py'))
commands = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands)


def validate(params, allow_references=False):
    if not isinstance(params, dict) or set(params) != {'command', 'params'} or not isinstance(params['params'], dict):
        raise ValueError('invalid_native_operation')
    lock = json.loads(Path(__file__).with_name('runtime.lock.json').read_text())
    catalog = commands.catalog()
    if catalog['pluginId'] != commands.DOMAIN or catalog['runtimeSha256'] != lock['artifacts']['darwin-arm64']['binarySha256']:
        raise ValueError('native_catalog_identity_mismatch')
    if not isinstance(params['command'], str) or params['command'] not in {row['id'] for row in catalog['commands']}:
        raise ValueError('unknown_native_command')
    try:
        json.dumps(params['params'], allow_nan=False)
    except (ValueError, TypeError):
        raise ValueError('invalid_native_parameters') from None
    # 两类公开入口共享原生 tick 合同；解析后的参数在 execute 中再次核验。
    commands.validate_native_parameters(params['command'], params['params'],
                                        allow_references=allow_references)
    row = next(row for row in catalog['commands'] if row['id'] == params['command'])
    commands.validate_tick_parameters(params['command'], params['params'],
                                      allow_references=allow_references, contract=row)


def execute(session, params, state, receipts, stage):
    validate(params)
    identifier = params['command']
    rows = commands.runtime_rows(session)
    if not {row['id'] for row in commands.catalog()['commands']}.issubset({row['id'] for row in rows}):
        raise RuntimeError('native_registry_drift')
    row = next((row for row in rows if row['id'] == identifier), None)
    capabilities = commands.load('capabilities')
    expected = next(r for r in commands.catalog()['commands'] if r['id'] == identifier)
    check = capabilities.compare_command(expected, row)
    state.setdefault('commandCapabilities', []).append(check)
    capabilities.assert_command(check)
    if row is None or row.get('enabled') is not True:
        raise RuntimeError('precondition_failed: ' + identifier + ': ' + str(row.get('why', 'native_context_disabled') if row else 'native_command_missing'))
    needed = capabilities.infer_resources(identifier, params['params'])
    if needed:
        resources = commands.probe_required_resources(session, needed, rows)
        context = capabilities.snapshot({}, commands.catalog(), rows, 'headless', resources=resources)
        state.setdefault('resourceCapabilities', []).extend(resources)
        capabilities.enforce(context, {'resources': needed}, [identifier])
    tool, arguments = commands.native_call(identifier, params['params'])
    state['lastAttempt'] = {'tool': tool, 'arguments': arguments, 'phase': 'submitted'}
    reply = session.request('tools/call', {'name': tool, 'arguments': arguments})
    # 不先把原生JSON转成对象：重复键、非有限值或畸形回复保持unknown。
    result = commands.parse_reply(reply, Path(stage), len(receipts))
    state['lastAttempt']['phase'] = 'reply_received'
    receipts.append({'tool': tool, 'arguments': arguments, 'command': identifier, 'params': params['params'], 'nativeCommand': identifier, 'result': result})
    return result
