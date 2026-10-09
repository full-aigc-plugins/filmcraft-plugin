#!/usr/bin/env python3
"""任务级公开命令会话：JSONL逐计划回执，共享所属进程，不重启或重放。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import socket
import sys

sys.dont_write_bytecode = True


def load(name):
    spec = importlib.util.spec_from_file_location('filmcraft_task_' + name, Path(__file__).with_name(name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


class BorrowedSession:
    """单计划只借用连接；退出计划不结束任务。"""
    def __init__(self, owner): self.owner = owner
    def __enter__(self): return self.owner
    def __exit__(self, *args): pass


class TaskSession:
    """固定授权和安装身份的所属任务；各计划仍使用公开commands.execute。"""
    def __init__(self, work, runtime_home, permissions, mode='headless', protected_paths=(), commands=None):
        self.commands = commands or load('commands')
        guard = self.commands.load('execution_permissions')
        self.permissions = guard.validate(permissions)
        guard.ensure_available()
        if mode not in ('headless', 'bridge'): raise ValueError('invalid_mode')
        self.mode = mode
        self.work = Path(work).absolute()
        self.runtime = Path(runtime_home).resolve()
        guard.require_write(self.work, self.permissions)
        guard.require_write(self.work.parent, self.permissions)
        guard.require_write(self.runtime, self.permissions)
        if self.work.exists() or self.work.is_symlink(): raise ValueError('output_exists')
        if not self.work.parent.is_dir(): raise ValueError('output_parent_missing')
        self.protected = tuple(str(guard.require_read(p, self.permissions)) for p in protected_paths)
        if any(not Path(p).exists() for p in self.protected): raise ValueError('task_protected_path_missing')
        if any(self.work.resolve().is_relative_to(p) for p in (str(self.commands.ROOT), str(self.runtime), *self.protected)):
            raise ValueError('task_output_protected')
        self.binding = self._binding()
        self.owner = None
        self.installed = None
        self.desktop = {}
        self.started = 0
        self.pids = []
        self.plans = []
        self.stopped = False
        self.closed = False
        self.port = None
        if mode == 'bridge':
            with socket.socket() as probe:
                probe.bind(('127.0.0.1', 0)); self.port = probe.getsockname()[1]
        self.work.mkdir(mode=0o700)
        self._record()

    def _binding(self):
        return json.dumps({'mode': self.mode, 'work': str(self.work), 'runtime': str(self.runtime),
            'permissions': self.permissions, 'protected': self.protected,
            'modelData': os.environ.get('FILMCRAFT_DATA_DIR'),
            'files': {str(p.relative_to(self.commands.ROOT)): sha(p) for p in sorted(self.commands.ROOT.rglob('*'))
                if p.is_file() and '__pycache__' not in p.parts and
                (p.parent.name == 'scripts' or p.name == 'command-coverage.json')}}, sort_keys=True)

    def _processes(self):
        if self.owner is None: return []
        if self.mode == 'bridge': return [self.owner.session.process, self.owner.process]
        return [self.owner.process]

    def _assert_identity(self):
        if self._binding() != self.binding: raise ValueError('task_identity_changed')
        self.commands.load('execution_permissions').validate(self.permissions)
        if self.work.resolve() != self.work: raise ValueError('task_identity_changed')
        if self.installed and sha(self.installed['executable']) != self.installed['binarySha256']:
            raise ValueError('task_identity_changed')
        if self.desktop and sha(self.desktop['executable']) != self.desktop['binarySha256']:
            raise ValueError('task_identity_changed')
        if any(p.poll() is not None for p in self._processes()): raise RuntimeError('task_process_exited')

    def _install(self, lock, home):
        if self.installed is None:
            if self.mode == 'bridge':
                self.desktop.update(self.commands.load('desktop').install(
                    json.loads((self.commands.ROOT/'scripts/desktop.lock.json').read_text()), home))
            self.installed = self.commands.load('bootstrap').install(lock, home)
        return self.installed

    def _factory(self, argv):
        if self.owner is None:
            # 未声明只读模型库时，整个任务固定使用一个私有数据目录。
            if os.environ.get('FILMCRAFT_DATA_DIR') is None:
                index = argv.index('--data-dir')
                argv = [*argv[:index + 1], str(self.work/'.native-data'), *argv[index + 2:]]
            if self.mode == 'bridge':
                candidate = self.commands.load('desktop_session').OwnedSession(argv, self.desktop,
                    self.commands.DOMAIN, self.work, self.port, permissions=self.permissions,
                    protected_roots=[str(self.commands.ROOT), str(self.runtime), *self.protected])
                self.owner = candidate.__enter__()
            else:
                self.owner = self.commands.load('mcp_session').Session(argv, cwd=str(self.work))
            self.started += 1
        self._assert_identity()
        self.pids.append([p.pid for p in self._processes()])
        return BorrowedSession(self.owner)

    def execute(self, plan, name, inputs=None):
        """执行一个新阶段，返回完整公开回执；失败后整个任务停止。"""
        if self.closed or self.stopped: raise RuntimeError('task_session_stopped')
        try:
            self._assert_identity()
            if not isinstance(name, str) or not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]{0,63}', name):
                raise ValueError('invalid_task_stage_name')
            inputs = inputs if inputs is not None else {}
            if not isinstance(inputs, dict): raise ValueError('invalid_input_name')
            self.commands.validate(plan, inputs)
            hashes = {}
            for key, source in inputs.items():
                path = Path(source).resolve()
                if not path.is_relative_to(self.work) and not any(path.is_relative_to(p) for p in self.protected):
                    raise ValueError('task_input_not_protected')
                if Path(source).is_symlink() or not path.is_file(): raise ValueError('invalid_input_file')
                self.commands.load('execution_permissions').require_read(path, self.permissions)
                hashes[key] = sha(path)
            receipt = self.commands.execute(plan, self.work/name, runtime_home=self.runtime,
                mode=self.mode, connect='127.0.0.1:'+str(self.port) if self.port else None,
                installer=self._install, session_factory=self._factory, inputs=inputs,
                desktop_identity=self.desktop if self.mode=='bridge' else None,
                permissions=self.permissions, protected_paths=self.protected,
                owned_bridge_port=self.port)
            self.plans.append({'name': name, 'result': receipt['result'], 'planSha256':receipt['planSha256']})
            if any(sha(inputs[key]) != digest for key, digest in hashes.items()):
                self.stopped = True
                raise RuntimeError('task_source_changed')
            if receipt['result'] != 'PASS': self.stopped = True
            self._record()
            return receipt
        except KeyboardInterrupt:
            self.stopped = True
            stage = self.work/name
            journal = stage/'journal.json'
            if journal.is_file():
                receipt = self.commands.reply_json(journal.read_text())
                receipt['result'] = 'unknown'
                receipt['error'] = 'outcome_unknown: task_interrupted; request not replayed'
                if receipt.get('steps') and receipt['steps'][-1]['state'] == 'started':
                    receipt['steps'][-1]['state'] = 'unknown'
                self.commands.write(stage/'failure.json', receipt)
                self.commands.write(journal, receipt)
                self.plans.append({'name':name, 'result':'unknown', 'planSha256':receipt['planSha256']})
            self._record()
            raise
        except BaseException:
            self.stopped = True
            self._record()
            raise

    def _record(self):
        proof = {'schema':'filmcraft-task-session/v1', 'mode':self.mode,
            'identityBindingSha256': hashlib.sha256(self.binding.encode()).hexdigest(),
            'sessionsStarted':self.started, 'pids':self.pids,
            'singleProcessIdentity':bool(self.pids) and all(p == self.pids[0] for p in self.pids),
            'plans':self.plans, 'stopped':self.stopped, 'closed':self.closed,
            'ownedProcessesStopped':self.closed and all(p.poll() is not None for p in self._processes())}
        self.commands.write(self.work/'task-session.json', proof)

    def close(self):
        if self.closed: return
        try:
            if self.owner is not None: self.owner.close()
        finally:
            self.closed = True
            self._record()

    def __enter__(self):
        if self.closed or self.stopped: raise RuntimeError('task_session_stopped')
        return self

    def __exit__(self, *args): self.close()


def serve(session, incoming, outgoing):
    """逐行接收计划；EOF／close结束任务，任何错误停止消费后续行。"""
    def emit(value):
        outgoing.write(json.dumps(value, ensure_ascii=False, allow_nan=False)+'\n'); outgoing.flush()
    for line in incoming:
        if not line.strip(): continue
        try:
            request = session.commands.reply_json(line)
            if request == {'action':'close'}:
                session.close(); emit({'result':'CLOSED'}); return 0
            if (not isinstance(request,dict) or not {'name','plan'}.issubset(request)
                    or set(request) - {'name','plan','inputs'}): raise ValueError('invalid_task_request')
            receipt = session.execute(request['plan'],request['name'],request.get('inputs'))
            emit(receipt)
            if receipt['result'] != 'PASS': return 1
        except (ValueError, RuntimeError, OSError, TypeError) as error:
            session.stopped = True
            emit({'result':'FAIL','error':str(error)}); return 1
    return 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--runtime-home',type=Path,required=True)
    parser.add_argument('--mode',choices=['headless','bridge'],default='headless')
    parser.add_argument('--read-root',action='append',default=[])
    parser.add_argument('--write-root',action='append',default=[])
    parser.add_argument('--protect-input',action='append',default=[])
    args=parser.parse_args()
    try:
        permissions=load('execution_permissions').from_cli(args.read_root,args.write_root)
        with TaskSession(args.output,args.runtime_home,permissions,args.mode,args.protect_input) as session:
            print(json.dumps({'result':'READY','mode':args.mode,'scope':'task open; native process starts on first valid plan'}),flush=True)
            return serve(session,sys.stdin,sys.stdout)
    except KeyboardInterrupt:
        print(json.dumps({'result':'unknown','error':'task_interrupted; inspect journal and native files; no replay'}),flush=True)
        return 130
    except (ValueError,RuntimeError,OSError,TypeError) as error:
        print(json.dumps({'result':'FAIL','error':str(error)}),flush=True);return 1


if __name__ == '__main__': raise SystemExit(main())
