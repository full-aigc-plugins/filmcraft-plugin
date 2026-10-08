"""原生工作流失败暂存保留；绝不移动含绝对依赖的未知结果工程。"""
from contextlib import contextmanager
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import tempfile


def _write_record(path, value):
    """只在本次拥有的目录内原子写入诊断。"""
    temporary = path.with_name(path.name + '.writing')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(temporary, path)


def claim_output(output, state):
    """创建并绑定本次输出目录身份；发生目录竞争时不覆盖。"""
    output.mkdir(mode=0o700)
    identity = output.stat()
    state['output'] = True
    state['outputIdentity'] = (identity.st_dev, identity.st_ino)


@contextmanager
def preserved_stage(output, prefix, state=None):
    """成功清理暂存；异常时保留原路径、摘要和回执，不改变原异常。"""
    output = Path(output).absolute()
    state = state if state is not None else {}
    stage = Path(tempfile.mkdtemp(prefix=prefix, dir=output.parent))
    try:
        yield str(stage)
    except BaseException as error:
        # 子会话先退出，文件位置不改变；不能将未知结果解释成未执行。
        try:
            operations = state.get('operations', [])
            _write_record(stage / 'recovery-operations.json', operations)
            diagnostic = getattr(error, 'clip_timing', None)
            if (isinstance(diagnostic, dict) and set(diagnostic) == {'reason', 'clipIds'}
                    and isinstance(diagnostic['reason'], str)
                    and diagnostic['reason'] in {'ticks_require_decimal_string', 'ticks_out_of_range',
                                                 'ticks_not_exact', 'clip_out_of_range', 'invalid_clip_speed'}
                    and isinstance(diagnostic['clipIds'], list) and diagnostic['clipIds']
                    and all(isinstance(value, str) and re.fullmatch(r'[1-9][0-9]{0,19}', value)
                            and int(value) <= 2**64-1 for value in diagnostic['clipIds'])):
                # 单独诊断文件参与原失败回执摘要，不增加 craft-failed-stage/v1 字段。
                _write_record(stage / 'clip-timing.json', diagnostic)
            if 'capabilitySnapshot' in state:
                # 独立诊断文件沿用领域快照，不扩充公共失败回执的协议字段。
                capabilities = dict(state['capabilitySnapshot'],
                                    resourceChecks=state.get('resourceCapabilities', []),
                                    commandChecks=state.get('commandCapabilities', []))
                _write_record(stage / 'capabilities.json', capabilities)
            files = {}
            for path in sorted(stage.rglob('*')):
                if path.is_file() and not path.is_symlink() and path.name != 'failure.json':
                    files[path.relative_to(stage).as_posix()] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
            record = {'schema': 'craft-failed-stage/v1', 'status': 'failed',
                      'outcome': 'outcome_unknown' if 'outcome_unknown:' in str(error) else 'failed',
                      'error': str(error), 'stage': os.path.relpath(stage, output),
                      'files': files, 'completedOperations': len(operations), 'lastAttempt': state.get('lastAttempt'), 'replayAllowed': False,
                      'acceptance': 'not-a-successful-delivery', 'recovery': 'verify hashes and reopen original project in a new read-only session before any explicit revision'}
            _write_record(stage / 'failure.json', record)
            # 目录竞争时不写他人目录；暂存中的诊断仍可读取。
            if not output.exists() and not output.is_symlink():
                try:
                    claim_output(output, state)
                except FileExistsError:
                    pass
            if (state.get('outputIdentity') and output.is_dir() and not output.is_symlink()
                    and (output.stat().st_dev, output.stat().st_ino) == state['outputIdentity']):
                _write_record(output / 'failure.json', record)
        except (OSError, ValueError, TypeError):
            # 诊断写入失败也不删除工程或遮蔽原始异常。
            pass
        raise
    else:
        if stage.exists():
            shutil.rmtree(stage)
