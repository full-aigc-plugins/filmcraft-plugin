"""当前独立技能的固定CLI入口；编辑须独立根授权，模型维护使用单独精确入口。"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode = True
ALLOWED = {'exec', '--version', 'bench-decode', 'render', 'inspect', 'help', 'export', 'describe', 'import', 'mcp', 'commands', 'run', 'probe'}


def setup_failure(runtime_home):
    """安装器缺失时保留当前技能自身的恢复位置，不读取兄弟技能。"""
    return {'skill':'filmcraft-cli-setup', 'bootstrapScript':str(Path(__file__).with_name('bootstrap.py').resolve()),
            'runtimeHome':str(Path(runtime_home).expanduser().absolute()), 'automaticRetry':False}


def permissions_helper():
    spec = importlib.util.spec_from_file_location('raw_cli_permissions', Path(__file__).with_name('execution_permissions.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def safe_discovery(argv):
    """只豁免不消费工程／文件参数的精确发现形式，附加参数不能提升权限。"""
    return tuple(argv) in (('--version',), ('help',), ('commands',), ('commands', '--json'))


def option_paths(argv, name):
    """同时处理分隔与等号选项；保持原生相对路径相对于当前工作目录的语义。"""
    found = []
    for index, value in enumerate(argv):
        if value == name:
            if index + 1 >= len(argv): raise ValueError('invalid_native_path_option')
            found.append(Path(argv[index + 1]).resolve())
        elif value.startswith(name + '='):
            found.append(Path(value[len(name) + 1:]).resolve())
    return found


def model_maintenance(argv, helper, policy, runtime_home):
    """独立维护只接受固定模型下载操作和显式数据目录，不能混入工程或编辑参数。"""
    if len(argv) != 5 or argv[:2] != ['exec', 'transcript.downloadModel'] or argv[3] != '--data-dir':
        raise ValueError('invalid_model_maintenance_request')
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value: raise ValueError('invalid_model_maintenance_request')
            value[key] = item
        return value
    try: params = json.loads(argv[2], object_pairs_hook=unique)
    except (ValueError, TypeError): raise ValueError('invalid_model_maintenance_request') from None
    if not isinstance(params, dict) or set(params) != {'model'} or params['model'] not in ('whisper-tiny', 'whisper-base', 'whisper-small'):
        raise ValueError('invalid_model_maintenance_request')
    data = Path(argv[4])
    if (not data.is_absolute() or str(data.resolve()) != str(data) or any(ord(c) < 32 for c in str(data))):
        raise ValueError('invalid_model_maintenance_request')
    if not data.is_dir(): raise ValueError('model_maintenance_directory_required')
    helper.require_write(data, policy)
    for protected in (Path(__file__).resolve().parents[1], Path(runtime_home).resolve(), Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve()):
        if data.is_relative_to(protected): raise ValueError('model_maintenance_protected_directory')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-home', default=os.environ.get('CRAFT_RUNTIME_HOME', str(Path.home()/'.local/share/craft-runtimes')))
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--read-root', action='append', default=[])
    parser.add_argument('--write-root', action='append', default=[])
    parser.add_argument('--model-maintenance', action='store_true', help='独立维护：仅exec transcript.downloadModel JSON --data-dir ABSOLUTE_DIR；需要明确写入根')
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args(); argv = args.arguments
    if argv[:1] == ['--']: argv = argv[1:]
    if not argv or argv[0] not in ALLOWED: parser.error('unsupported_cli_subcommand: put the native subcommand first after --')
    installation_started = installation_completed = False
    try:
        helper = policy = None; protected = []; maintenance_data = None
        if not safe_discovery(argv) or args.read_root or args.write_root or args.model_maintenance:
            if not args.read_root or not args.write_root: raise ValueError('execution_permissions_required')
            helper = permissions_helper(); policy = helper.from_cli(args.read_root, args.write_root)
            helper.require_write(args.runtime_home, policy)
            if args.archive: helper.require_read(args.archive, policy)
            if args.model_maintenance:
                maintenance_data = model_maintenance(argv, helper, policy, args.runtime_home)
                helper.ensure_available()
            else:
                if argv[:2] == ['exec', 'transcript.downloadModel']: raise ValueError('model_maintenance_required')
                for name in ('--project', '--data-dir'):
                    for path in option_paths(argv, name):
                        helper.require_read(path, policy)
                        protected.append(str(path if name == '--project' else path/'models'))
                if argv[0] in ('run', 'import', 'probe', 'bench-decode') and len(argv) > 1 and not argv[1].startswith('-'):
                    path = helper.require_read(argv[1], policy); protected.append(str(path))
                model_data, explicit = helper.model_data_directory(Path.cwd(), policy)
                if explicit: protected.append(str(model_data))
                helper.ensure_available()
        installation_started = True
        path = Path(__file__).with_name('bootstrap.py')
        spec = importlib.util.spec_from_file_location('craft_bootstrap', path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        installed = module.install(json.loads(path.with_name('runtime.lock.json').read_text()), args.runtime_home, args.archive)
        installation_completed = True
        helper = helper or permissions_helper()
        command = [installed['executable'], *argv]
        if policy is not None:
            execution_policy = policy if maintenance_data is None else dict(policy, writeRoots=[str(maintenance_data)])
            command = helper.command(command, execution_policy, protected_roots=[str(Path(__file__).resolve().parents[1]), str(Path(args.runtime_home).resolve()), *protected], model_maintenance=maintenance_data is not None)
        # 模型维护仅开放出站网络，写根缩小到精确数据目录；编辑不获得这些权限。
        result = subprocess.run(command, env=helper.child_environment(), timeout=600)
        return result.returncode
    except (ValueError, OSError, ImportError, subprocess.SubprocessError) as error:
        reply = {'error':str(error), 'result':'unknown' if isinstance(error, subprocess.TimeoutExpired) else 'failed'}
        if installation_started and not installation_completed: reply['dependencySetup'] = setup_failure(args.runtime_home)
        print(json.dumps(reply)); return 1


if __name__ == '__main__': raise SystemExit(main())
