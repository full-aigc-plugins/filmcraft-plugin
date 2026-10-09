"""QA 专用：同一固定安装、授权根的空上下文拒绝批次；不接管用户实例。"""
import json
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


class EmptyBatch:
    """每个批次只启动一次；异常和未知结果后禁止继续借用。"""
    def __init__(self, commands, desktop, mode, work, runtime, permissions):
        self.commands, self.desktop, self.mode = commands, desktop, mode
        self.work, self.runtime, self.permissions = Path(work), Path(runtime), permissions
        self.owner = None
        self.identity = {}
        self.started = 0
        self.tainted = False
        self.cases = []
        self.pids = []
        self.begin = time.monotonic()
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            self.port = probe.getsockname()[1]

    def __enter__(self): return self

    def execute(self, plan, output):
        if self.tainted: raise RuntimeError('batch_stopped: no restart or replay')
        if len(plan.get('operations', [])) != 1:
            raise ValueError('empty_batch_requires_one_disabled_command')
        identifier = plan['operations'][0]['command']
        # 此专用借用器不允许任何编辑、重置、输入或输出副作用。
        row = next(row for row in self.commands.catalog()['commands'] if row['id'] == identifier)
        if row['enabledAtEmptySession']:
            raise ValueError('empty_batch_requires_disabled_command')
        output = Path(output)

        def installer(lock, home):
            if self.mode == 'bridge' and not self.identity:
                self.identity.update(self.commands.load('desktop').install(
                    json.loads((self.commands.ROOT / 'scripts/desktop.lock.json').read_text()), home))
            return self.commands.load('bootstrap').install(lock, home)

        def factory(argv):
            if self.owner is None:
                if self.mode == 'bridge':
                    candidate = self.desktop.OwnedSession(argv, self.identity, self.commands.DOMAIN,
                        output, self.port, permissions=self.permissions,
                        protected_roots=[str(self.commands.ROOT), str(self.runtime)])
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
                installer=installer, session_factory=factory, permissions=self.permissions,
                desktop_identity=self.identity if self.mode == 'bridge' else None,
                owned_bridge_port=self.port if self.mode == 'bridge' else None)
            if not expected_refusal(receipt):
                self.tainted = True
                raise RuntimeError('unexpected_empty_batch_result: ' + str(receipt.get('error', receipt['result'])))
            self.cases.append(identifier)
            return receipt
        except BaseException:
            self.tainted = True
            raise

    def __exit__(self, *args):
        try:
            if self.owner: self.owner.close()
        finally:
            process = (self.owner.session.process if self.mode == 'bridge' else self.owner.process) if self.owner else None
            proof = {'schema': 'filmcraft-owned-empty-batch/v1', 'mode': self.mode,
                'sessionsStarted': self.started, 'caseCount': len(self.cases), 'cases': self.cases,
                'pids': self.pids, 'singleProcessIdentity': bool(self.pids) and all(p == self.pids[0] for p in self.pids),
                'ownedProcessesStopped': process is None or process.poll() is not None,
                'desktopStopped': self.owner.stopped if self.owner and self.mode == 'bridge' else None,
                'listenerOwnedByPID': self.owner.listener_verified if self.owner and self.mode == 'bridge' else None,
                'tainted': self.tainted, 'elapsedSeconds': time.monotonic() - self.begin,
                'scope': 'QA disabled-command batch only; no general interactive session API'}
            self.commands.write(self.work / 'empty-batch-session.private.json', proof)
