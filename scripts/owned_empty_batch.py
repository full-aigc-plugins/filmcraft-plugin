"""QA专用所属会话；连续计划和空上下文批次共享连接，不接管用户实例。"""
import json
import hashlib
import os
from pathlib import Path
import socket
import time


class BorrowedSession:
    """借用连接，生命周期由批次所有者负责。"""
    def __init__(self, owner): self.owner = owner
    def __enter__(self): return self.owner
    def __exit__(self, *args): pass


def expected_refusal(receipt):
    return (receipt.get('result') == 'FAIL'
            and receipt.get('error', '').startswith('precondition_failed: ')
            and len(receipt.get('steps', [])) == 1
            and receipt['steps'][0].get('state') == 'blocked')


class OwnedBatch:
    """每个批次只启动一次；异常和未知结果后禁止继续借用。"""
    def __init__(self, commands, desktop, mode, work, runtime, permissions, protected_paths=()):
        self.commands, self.desktop, self.mode = commands, desktop, mode
        self.work, self.runtime, self.permissions = Path(work), Path(runtime), permissions
        self.protected_paths = tuple(str(Path(p).resolve()) for p in protected_paths)
        self.identity_binding = self.binding()
        self.owner = None
        self.identity = {}
        self.runtime_sha256 = None
        self.started = 0
        self.tainted = False
        self.cases = []
        self.pids = []
        self.begin = time.monotonic()
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            self.port = probe.getsockname()[1]

    def __enter__(self): return self

    def binding(self):
        return json.dumps({'mode': self.mode, 'runtime': str(self.runtime),
            'permissions': self.permissions, 'protectedPaths': self.protected_paths,
            'modelData': os.environ.get('FILMCRAFT_DATA_DIR'),
            'installedContracts': {str(p.relative_to(self.commands.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [self.commands.ROOT / 'scripts/runtime.lock.json', self.commands.ROOT / 'scripts/desktop.lock.json',
                          self.commands.ROOT / 'scripts/commands.py', self.commands.ROOT / 'references/command-coverage.json']}
                if getattr(self.commands, 'ROOT', None) else None}, sort_keys=True)

    def reset(self, output):
        receipt = self.execute({'schema': 'craft-command-plan/v1', 'operations': [
            {'command': 'file.closeAllProjects', 'params': {'force': True}},
            {'command': 'state.inspect', 'params': {}}]}, output)
        state = receipt['steps'][-1]['result']
        if not isinstance(state, dict) or 'active_sequence' not in state or state['active_sequence'] is not None:
            self.tainted = True
            raise RuntimeError('batch_reset_failed: active_sequence remains')
        return receipt

    def execute(self, plan, output, inputs=None, expect_refusal=False):
        if self.tainted: raise RuntimeError('batch_stopped: no restart or replay')
        if self.binding() != self.identity_binding:
            self.tainted = True
            raise ValueError('batch_identity_changed')
        output = Path(output)
        for source in (inputs or {}).values():
            canonical = Path(source).resolve()
            if not canonical.is_relative_to(self.work.resolve()) and not any(
                    canonical.is_relative_to(root) for root in self.protected_paths):
                self.tainted = True
                raise ValueError('batch_external_input_not_protected')

        def installer(lock, home):
            if self.mode == 'bridge' and not self.identity:
                self.identity.update(self.commands.load('desktop').install(
                    json.loads((self.commands.ROOT / 'scripts/desktop.lock.json').read_text()), home))
            installed = self.commands.load('bootstrap').install(lock, home)
            if self.runtime_sha256 is not None and installed['binarySha256'] != self.runtime_sha256:
                raise ValueError('batch_identity_changed: runtime binary')
            self.runtime_sha256 = installed['binarySha256']
            return installed

        def factory(argv):
            if self.owner is None:
                if self.mode == 'bridge':
                    candidate = self.desktop.OwnedSession(argv, self.identity, self.commands.DOMAIN,
                        output, self.port, permissions=self.permissions,
                        protected_roots=[str(self.commands.ROOT), str(self.runtime), *self.protected_paths])
                    self.owner = candidate.__enter__()
                else:
                    self.owner = self.commands.load('mcp_session').Session(argv, cwd=str(output))
                self.started += 1
            process = self.owner.session.process if self.mode == 'bridge' else self.owner.process
            if process.poll() is not None: raise RuntimeError('batch_process_exited')
            self.pids.append({'mcp': process.pid, 'desktop': self.owner.process.pid if self.mode == 'bridge' else None})
            return BorrowedSession(self.owner)

        try:
            receipt = self.commands.execute(plan, output, runtime_home=self.runtime,
                mode=self.mode, connect='127.0.0.1:' + str(self.port) if self.mode == 'bridge' else None,
                installer=installer, session_factory=factory, permissions=self.permissions, inputs=inputs,
                protected_paths=self.protected_paths,
                desktop_identity=self.identity if self.mode == 'bridge' else None,
                owned_bridge_port=self.port if self.mode == 'bridge' else None)
            if not (expected_refusal(receipt) if expect_refusal else receipt.get('result') == 'PASS'):
                self.tainted = True
                raise RuntimeError('unexpected_empty_batch_result: ' + str(receipt.get('error', receipt['result'])))
            self.cases.append({'commands': [op['command'] for op in plan['operations']], 'expectedRefusal': expect_refusal})
            return receipt
        except BaseException:
            self.tainted = True
            raise

    def __exit__(self, *args):
        try:
            if self.owner: self.owner.close()
        finally:
            process = (self.owner.session.process if self.mode == 'bridge' else self.owner.process) if self.owner else None
            proof = {'schema': 'filmcraft-owned-plan-batch/v1', 'mode': self.mode,
                'identityBindingSha256': hashlib.sha256(self.identity_binding.encode()).hexdigest(),
                'runtimeSha256': self.runtime_sha256, 'sessionsStarted': self.started, 'caseCount': len(self.cases), 'cases': self.cases,
                'pids': self.pids, 'singleProcessIdentity': bool(self.pids) and all(p == self.pids[0] for p in self.pids),
                'ownedProcessesStopped': process is None or process.poll() is not None,
                'desktopStopped': self.owner.stopped if self.owner and self.mode == 'bridge' else None,
                'listenerOwnedByPID': self.owner.listener_verified if self.owner and self.mode == 'bridge' else None,
                'tainted': self.tainted, 'elapsedSeconds': time.monotonic() - self.begin,
                'scope': 'QA owned continuous plans within fixed permissions; no general interactive session API'}
            self.commands.write(self.work / 'owned-batch-session.private.json', proof)


class EmptyBatch(OwnedBatch):
    """保留旧的空会话专用入口，禁止有副作用命令。"""
    def execute(self, plan, output):
        if self.tainted: raise RuntimeError('batch_stopped: no restart or replay')
        if len(plan.get('operations', [])) != 1:
            raise ValueError('empty_batch_requires_one_disabled_command')
        identifier = plan['operations'][0]['command']
        row = next(row for row in self.commands.catalog()['commands'] if row['id'] == identifier)
        if row['enabledAtEmptySession']:
            raise ValueError('empty_batch_requires_disabled_command')
        return super().execute(plan, output, expect_refusal=True)

    def __exit__(self, *args):
        super().__exit__(*args)
        (self.work / 'owned-batch-session.private.json').replace(self.work / 'empty-batch-session.private.json')
