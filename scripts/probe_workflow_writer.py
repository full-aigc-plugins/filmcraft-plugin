#!/usr/bin/env python3
"""仅用于QA的确定性调度探针；真实公共工作流与原生会话不替换。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import os
import sys
import time
sys.dont_write_bytecode = True


def command_identity(name, arguments):
    return arguments.get('id') if name == 'command_run' else name


def run(skill, plan, output, runtime_home, trace, barrier, release, pause):
    def load(name):
        spec = importlib.util.spec_from_file_location('writer_probe_' + name, skill / 'scripts' / (name + '.py'))
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
    workflow = load('workflow'); original_load = workflow.load_module
    original_session = load('mcp_session')
    def record(kind, **fields):
        with trace.open('a') as stream:
            stream.write(json.dumps({'kind': kind, 'ownerPid': os.getpid(), **fields}) + '\n'); stream.flush(); os.fsync(stream.fileno())
    def wait(phase, session, checkpoint=None):
        info = {'phase': phase, 'ownerPid': os.getpid(), 'nativePid': session.process.pid}
        if checkpoint:
            path = Path(checkpoint); info.update(checkpoint=str(path), checkpointSha256=hashlib.sha256(path.read_bytes()).hexdigest())
        pending = barrier.with_suffix('.tmp'); pending.write_text(json.dumps(info)); pending.replace(barrier)
        deadline = time.monotonic() + 90
        while not release.exists():
            if time.monotonic() > deadline: raise TimeoutError('QA_barrier_timeout')
            time.sleep(.05)
    class ObservedSession(original_session.Session):
        def __init__(self, argv, *args, **kwargs):
            record('native-session-start')
            super().__init__(argv, *args, **kwargs)
            record('native-session-initialized', nativePid=self.process.pid)
            if pause == 'start': wait('real-native-initialized', self)
        def request(self, method, params):
            result = super().request(method, params)
            if method == 'tools/call':
                name = params.get('name'); arguments = params.get('arguments', {})
                command = command_identity(name, arguments)
                record('native-reply', command=command, responseSha256=hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest())
                if pause == 'save' and command == 'file.saveAs' and not result.get('isError'):
                    wait('actual-native-checkpoint-saved', self, arguments['params']['path'])
            return result
    def instrument(name):
        if name == 'mcp_session':
            original_session.Session = ObservedSession; return original_session
        return original_load(name)
    workflow.load_module = instrument
    try:
        result = workflow.execute(json.loads(plan.read_text()), output, runtime_home)
        record('public-workflow-success'); print(json.dumps({'result': 'PASS'})); return result
    except Exception as error:
        record('public-workflow-refused', error=str(error)); raise


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for key in ('skill', 'plan', 'output', 'runtime-home', 'trace', 'barrier', 'release'):
        p.add_argument('--' + key, type=Path, required=True)
    p.add_argument('--pause', choices=('none', 'start', 'save'), default='none')
    args = vars(p.parse_args())
    run(**args)
