"""可信调用方的目录策略与 macOS 原生进程隔离；不接受计划中的授权。"""
import json
import os
from pathlib import Path
import sys

SCHEMA = 'filmcraft-execution-permissions/v1'
BROAD_ROOTS = {'/', '/Users', '/Volumes', '/System', '/Library', '/private', '/private/tmp',
               '/private/var', '/private/var/folders', '/System/Volumes', '/System/Volumes/Data', '/opt', '/usr'}
ENVIRONMENT_KEYS = {'PATH', 'HOME', 'TMPDIR', 'LANG', 'LC_ALL', 'LC_CTYPE'}


def validate(policy):
    """核对独立可信策略的规范真实根；未知字段、链接授权与无限根均拒绝。"""
    if not isinstance(policy, dict) or set(policy) != {'schema', 'readRoots', 'writeRoots'} or policy.get('schema') != SCHEMA:
        raise ValueError('invalid_execution_permissions')
    result = {'schema': SCHEMA}
    for key in ('readRoots', 'writeRoots'):
        roots = policy[key]
        if not isinstance(roots, list) or not 1 <= len(roots) <= 64:
            raise ValueError('invalid_execution_permissions')
        normalized = []
        for value in roots:
            if (not isinstance(value, str) or not value or len(value) > 4096
                    or any(ord(char) < 32 for char in value) or not Path(value).is_absolute()):
                raise ValueError('invalid_execution_permissions')
            path = Path(value)
            try:
                if path.is_symlink() or not path.is_dir():
                    raise ValueError('invalid_execution_permissions')
                canonical = str(path.resolve(strict=True))
            except OSError:
                raise ValueError('invalid_execution_permissions') from None
            if canonical != str(path) or canonical in BROAD_ROOTS:
                raise ValueError('invalid_execution_permissions')
            normalized.append(canonical)
        result[key] = sorted(set(normalized))
    return result


def require_read(path, policy):
    """读取前核对真实路径；不读取拒绝目标，也不在诊断中回显路径。"""
    canonical = Path(path).resolve()
    value = validate(policy)
    if not any(canonical.is_relative_to(root) for root in value['readRoots'] + value['writeRoots']):
        raise ValueError('permission_read_denied')
    return canonical


def require_write(path, policy):
    """写入前核对真实父路径，包括尚不存在的目标及指向根外的父链接。"""
    canonical = Path(path).resolve()
    value = validate(policy)
    if not any(canonical.is_relative_to(root) for root in value['writeRoots']):
        raise ValueError('permission_write_denied')
    return canonical


def child_environment(environment=None):
    """本地编辑不消费云端密钥；仅传递必要运行环境，不按秘密关键词猜测。"""
    environment = os.environ if environment is None else environment
    result = {key: value for key, value in environment.items() if key in ENVIRONMENT_KEYS and isinstance(value, str)}
    data = environment.get('FILMCRAFT_DATA_DIR')
    if isinstance(data, str) and Path(data).is_absolute() and not any(ord(char) < 32 for char in data):
        result['FILMCRAFT_DATA_DIR'] = data
    return result


def command(argv, policy, platform=None, protected_roots=(), control_port=None, graphics=False):
    """构造实际系统隔离命令；缺少支持时拒绝，不回退无隔离执行。"""
    policy = validate(policy)
    if (sys.platform if platform is None else platform) != 'darwin' or not Path('/usr/bin/sandbox-exec').is_file():
        raise ValueError('execution_isolation_unavailable')
    if (not isinstance(argv, list) or not argv or not all(isinstance(arg, str) and '\0' not in arg for arg in argv)
            or not Path(argv[0]).is_absolute() or not Path(argv[0]).is_file()):
        raise ValueError('invalid_isolated_command')
    executable = Path(argv[0]).resolve(strict=True)
    # 系统与解释器是可信执行依赖；用户媒体仅能来自声明根。
    dependencies = ['/System/Library', '/System/Cryptexes', '/System/Volumes/Preboot', '/usr/lib', '/usr/share', '/usr/bin', '/usr/sbin', '/usr/libexec', '/bin', '/sbin', '/Library/Apple', '/Library/Fonts',
                    '/private/etc', '/private/var/db/timezone', sys.prefix, sys.base_prefix, str(executable.parent)]
    read_roots = sorted(set(dependencies + policy['readRoots'] + policy['writeRoots']))
    def subpath(path):
        return '(subpath ' + json.dumps(str(path), ensure_ascii=False) + ')'
    rules = ['(version 1)', '(deny default)', '(allow process*)', '(allow sysctl-read)',
             '(allow mach-lookup)', '(allow file-read-metadata)',
             # dyld 打开根目录本身；literal 不授予其子目录或文件内容权限。
             '(allow file-read-data (literal "/"))',
             '(allow file-read* ' + ' '.join(subpath(path) for path in read_roots) + ')',
             '(allow file-map-executable ' + ' '.join(subpath(path) for path in dependencies) + ')',
             '(allow file-read-data (literal "/dev/null") (literal "/dev/random") (literal "/dev/urandom") (literal "/dev/zero"))',
             '(allow file-write* ' + ' '.join(subpath(path) for path in policy['writeRoots']) + ')',
             '(allow file-write-data (literal "/dev/null"))']
    if graphics:
        rules.extend(['(allow iokit-open)', '(allow iokit-get-properties)'])
    if control_port is not None:
        if type(control_port) is not int or not 1 <= control_port <= 65535:
            raise ValueError('invalid_execution_permissions')
        endpoint = json.dumps('localhost:' + str(control_port))
        rules.append('(allow network* (local ip ' + endpoint + ') (remote ip ' + endpoint + '))')
    # 即使调用方授权了包含缓存的工作根，编辑进程也不得修改已锁定执行文件。
    protected = {str(executable.parent), str(Path(sys.prefix).resolve()), str(Path(sys.base_prefix).resolve())}
    for root in protected_roots:
        if not isinstance(root, str) or not Path(root).is_absolute() or '\0' in root:
            raise ValueError('invalid_execution_permissions')
        protected.add(str(Path(root).resolve()))
    rules.append('(deny file-write* ' + ' '.join(subpath(path) for path in sorted(protected)) + ')')
    return ['/usr/bin/sandbox-exec', '-p', '\n'.join(rules), *argv]


def from_cli(read_roots, write_roots):
    """仅接受可信命令行的独立根授权；计划不能提供或扩大策略。"""
    if not read_roots or not write_roots:
        raise ValueError('execution_permissions_required')
    return validate({'schema': SCHEMA, 'readRoots': read_roots, 'writeRoots': write_roots})


def workflow_paths(plan, output, policy, source=None, data_dir=None):
    """在读取素材／源清单与创建输出前检查工作流显式文件位置。"""
    policy = validate(policy)
    require_write(output, policy)
    # 临时工程和持久锁与目标同父目录，父目录也须有明确写入权限。
    require_write(Path(output).parent, policy)
    if source is not None:
        require_read(source, policy)
        require_read(Path(source) / 'manifest.json', policy)
        require_read(Path(source) / 'project.fcproj', policy)
    if isinstance(plan, dict) and isinstance(plan.get('assets', {}), dict):
        for asset in plan.get('assets', {}).values():
            if isinstance(asset, dict) and isinstance(asset.get('path'), str):
                require_read(asset['path'], policy)
    if data_dir is not None:
        require_read(data_dir, policy)
    return policy


def ensure_available():
    """编辑前拒绝不具备实际进程目录隔离的平台。"""
    if sys.platform != 'darwin' or not Path('/usr/bin/sandbox-exec').is_file():
        raise ValueError('execution_isolation_unavailable')


def model_data_directory(output, policy=None):
    """选择宿主显式只读模型目录；未声明时使用本次私有数据目录。"""
    configured = os.environ.get('FILMCRAFT_DATA_DIR')
    if configured is None:
        return Path(output).resolve() / '.native-data', False
    if (not isinstance(configured, str) or not Path(configured).is_absolute()
            or any(ord(char) < 32 for char in configured)):
        raise ValueError('invalid_execution_permissions')
    path = Path(configured).resolve()
    if policy is not None:
        require_read(path, policy)
    return path, True
