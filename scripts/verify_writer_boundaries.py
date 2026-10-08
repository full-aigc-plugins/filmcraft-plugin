#!/usr/bin/env python3
"""真实固定公开工作流的竞争、中断与桌面版本冲突；调度探针不替换原生实现。"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import signal
import socket
import sqlite3
import subprocess
import sys
import time
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_fixed_install import release_entry, owner_helper, verify_code_files
from verify_fixed_admission import verify as admission_verify

SCENARIOS = {'FC-TX-001-P', 'FC-TX-001-N', 'FC-TX-001-OUTPUT', 'FC-TX-001-INTERRUPT', 'FC-TX-001-HOST-ADMISSION'}


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


def validate_report(report):
    if (report.get('schema') != 'filmcraft-writer-boundaries/v1' or report.get('result') != 'PASS'
            or set(report.get('scenarios', {})) != SCENARIOS
            or any(r.get('status') != 'PASS' for r in report.get('scenarios', {}).values())
            or report.get('allInstalledSkillsUnchanged') is not True
            or report.get('allInstalledCodeUnchanged') is not True or report.get('fullV1') != 'NOT_PROVEN'):
        raise ValueError('writer_boundary_scenarios_incomplete')
    rows = report['scenarios']
    for key in ('FC-TX-001-P', 'FC-TX-001-HOST-ADMISSION'):
        row = rows[key]
        if (row.get('nativeCases') != 7 or not re.fullmatch('[a-f0-9]{64}', row.get('evidenceSha256', ''))
                or not re.fullmatch('[a-f0-9]{64}', row.get('runtimeIdentity', {}).get('sha256', ''))):
            raise ValueError('writer_admission_unconfirmed')
    expected_rejections = {'planHash': 'plan_identity_conflict', 'nativePlanHash': 'plan_identity_conflict',
        'inputHashes': 'input_identity_conflict', 'projectRevision': 'revision_conflict',
        'sourceTreeSha256': 'source_identity_conflict', 'sourceRevision': 'source_identity_conflict',
        'runtimeIdentity': 'runtime_identity_conflict'}
    rejections = rows['FC-TX-001-P'].get('bindingRejections', [])
    if (len(rejections) != len(expected_rejections) or {r.get('field') for r in rejections} != set(expected_rejections)
            or any(r.get('status') != 'PASS' or r.get('error') != expected_rejections[r['field']]
                   or r.get('nativeAttempts') != 0 or r.get('outputExists') is not False for r in rejections)):
        raise ValueError('writer_binding_rejections_incomplete')
    gui = rows['FC-TX-001-N']; race = rows['FC-TX-001-OUTPUT']; killed = rows['FC-TX-001-INTERRUPT']
    if (not re.fullmatch('[a-f0-9]{64}', gui.get('originalSha256', ''))
            or not re.fullmatch('[a-f0-9]{64}', gui.get('desktopSavedSha256', ''))
            or gui.get('error') != 'revision_conflict' or gui.get('sourcePreserved') is not True
            or gui.get('originalSha256') == gui.get('desktopSavedSha256')
            or gui.get('nativeAttempts') != 0 or gui.get('ownedDesktopStopped') is not True
            or gui.get('listenerOwnedByPID') is not True): raise ValueError('writer_gui_conflict_unconfirmed')
    if (race.get('error') != 'output_execution_conflict' or race.get('competitorNativeSessions') != 0
            or race.get('ownerNativeSessions') != 1 or race.get('differentTargetCompletedWhileOwnerHeld') is not True
            or race.get('existingUserDirectoryPreserved') is not True): raise ValueError('writer_competition_unconfirmed')
    if (killed.get('error') != 'output_execution_reconciling' or killed.get('retryNativeSessions') != 0
            or killed.get('recordState') not in ('running', 'reconciling')
            or killed.get('checkpointPreserved') is not True or killed.get('checkpointReopened') is not True
            or killed.get('automaticCleanup') is not False): raise ValueError('writer_interruption_unconfirmed')


def verify(host, repository, authority, ref, output, desktop_home, node, python):
    host = host.resolve(); output = output.absolute()
    if output.exists() or output.is_symlink(): raise ValueError('output_exists')
    expected = release_entry(repository, ref); receipt = json.loads((host / 'host-receipt.json').read_text())
    if receipt.get('result') != 'PASS' or receipt.get('plugin') != expected: raise ValueError('fixed_host_mismatch')
    dirs = {k: Path(v).resolve() for k, v in json.loads((host / 'installed-directories.private.json').read_text()).items()}
    helper, identity = owner_helper(authority)
    if receipt.get('helper') != identity or set(dirs) != set(expected['skills']): raise ValueError('fixed_host_inventory_mismatch')
    def intact():
        for path in dirs.values():
            if not path.is_relative_to(host / 'host-config'): raise ValueError('installed_path_outside_host')
            helper.verify_installed_skill(path, expected); verify_code_files(path.parent.parent, expected['codeFilesSha256'])
    intact(); skill = dirs['filmcraft-use']; core = skill.parent.parent
    worker = Path(__file__).with_name('probe_workflow_writer.py')
    output.mkdir(mode=0o700); scenarios = {}; processes = []; logs = []
    def progress(): (output / 'progress.json').write_text(json.dumps(scenarios, indent=2) + '\n')
    admission = admission_verify(host, repository, authority, ref, output / 'admission', node, python)
    for key in ('FC-TX-001-P', 'FC-TX-001-HOST-ADMISSION'):
        scenarios[key] = {'status': 'PASS', 'nativeCases': len(admission['cases']),
                          'evidenceSha256': sha(output / 'admission/fixed-report.json'), 'runtimeIdentity': admission['runtimeIdentity']}
    progress()
    # 每项绑定维度使用真实已批准请求，再由原生预检拒绝错误身份，不能只验证哈希计算。
    base_binding = json.loads((output / 'admission/create.binding.json').read_text())
    binding_cases = []
    variants = [('planHash', 'plan_identity_conflict'), ('nativePlanHash', 'plan_identity_conflict'),
                ('inputHashes', 'input_identity_conflict'), ('projectRevision', 'revision_conflict'),
                ('sourceTreeSha256', 'source_identity_conflict'), ('sourceRevision', 'source_identity_conflict'),
                ('runtimeIdentity', 'runtime_identity_conflict')]
    for field, expected_error in variants:
        folder = output / ('identity-' + field); folder.mkdir()
        task = json.loads(json.dumps(base_binding)); target = folder / 'refused'
        task.update(taskId='identity-' + field, idempotencyKey='identity-' + field,
                    outputRoot=str(target), projectKey=hashlib.sha256(str(target).encode()).hexdigest())
        if field == 'inputHashes':
            task['inputHashes'] = {k: '0' * 64 for k in task['inputHashes']}
            for row in task['inputRefs']: row['sha256'] = '0' * 64
        elif field == 'runtimeIdentity': task['runtimeIdentity']['cliVersion'] = 'wrong-but-well-formed'
        else: task[field] = '0' * (40 if field == 'sourceRevision' else 64)
        binding_path = folder / 'binding.private.json'; binding_path.write_text(json.dumps(task))
        resources = output / 'admission/resources.json'
        subject_run = subprocess.run([node, str(core / 'src/cli/workflow.ts'), 'subject', '--binding', str(binding_path), '--resources', str(resources)], capture_output=True, text=True, timeout=30)
        assert subject_run.returncode == 0, subject_run.stderr
        subject = json.loads(subject_run.stdout); grants = folder / 'grants'; grants.mkdir(mode=0o700)
        grant = {'schema': 'filmcraft-local-authorization/v1', 'authorizationRef': task['authorizationRef'],
                 'authorizationScopeSha256': task['authorizationScopeSha256'], 'expiresAt': int(time.time() * 1000) + 600000,
                 'revoked': False, 'subjects': [hashlib.sha256(json.dumps(subject, sort_keys=True, separators=(',', ':')).encode()).hexdigest()]}
        grant_file = grants / (hashlib.sha256(task['authorizationRef'].encode()).hexdigest() + '.json')
        grant_file.write_text(json.dumps(grant)); grant_file.chmod(0o600); db_path = folder / 'ledger.sqlite'
        request = subprocess.run([node, str(core / 'src/cli/workflow.ts'), 'run', '--binding', str(binding_path),
            '--plan', str(output / 'admission/plan.json'), '--resources', str(resources), '--ledger', str(db_path),
            '--blobs', str(folder / 'blobs'), '--authorization-root', str(grants),
            '--runtime-home', str(output / 'admission/fresh-runtime'), '--python', python], capture_output=True, text=True, timeout=180)
        rejected = json.loads(request.stdout)
        assert request.returncode == 1 and rejected['error']['code'] == expected_error, request.stdout + request.stderr
        with sqlite3.connect('file:' + str(db_path) + '?mode=ro', uri=True) as db: count = db.execute('SELECT count(*) FROM attempts').fetchone()[0]
        assert count == 0 and not target.exists()
        binding_cases.append({'field': field, 'status': 'PASS', 'error': expected_error, 'nativeAttempts': count, 'outputExists': False})
    scenarios['FC-TX-001-P']['bindingRejections'] = binding_cases; progress()
    plan = output / 'admission/plan.json'; runtime = output / 'admission/fresh-runtime'
    lock = json.loads((skill / 'scripts/runtime.lock.json').read_text())
    installed = load(skill / 'scripts/bootstrap.py', 'writer_bootstrap').install(lock, runtime)
    commands = load(skill / 'scripts/commands.py', 'writer_commands')
    def command(session, identifier, params):
        name, arguments = commands.native_call(identifier, params)
        return commands.parse_reply(session.request('tools/call', {'name': name, 'arguments': arguments}))
    def trace_rows(path): return [json.loads(s) for s in path.read_text().splitlines()] if path.exists() else []
    def sessions(path): return sum(r['kind'] == 'native-session-start' for r in trace_rows(path))
    def start(name, target, pause='none'):
        folder = output / name; folder.mkdir(); trace = folder / 'trace.private.jsonl'; log = (folder / 'worker.private.log').open('w'); logs.append(log)
        barrier = folder / 'barrier.private.json'; release = folder / 'release'
        command = [python, '-I', '-B', str(worker), '--skill', str(skill), '--plan', str(plan), '--output', str(target),
                   '--runtime-home', str(runtime), '--trace', str(trace), '--barrier', str(barrier), '--release', str(release), '--pause', pause]
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        processes.append(child); return child, trace, barrier, release, folder
    def barrier_ready(child, file):
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            if child.poll() is not None: raise ValueError('owner_ended_before_barrier')
            if file.exists(): return json.loads(file.read_text())
            time.sleep(.05)
        raise TimeoutError('writer_barrier_timeout')
    def done(row):
        child, trace, barrier, release, folder = row
        code = child.wait(timeout=180); logs[-1].flush()
        return code, (folder / 'worker.private.log').read_text()
    try:
        competition = output / 'competition'; competition.mkdir(); alias = output / 'competition-alias'; alias.symlink_to(competition, target_is_directory=True)
        owner = start('owner', competition / 'shared', 'start'); info = barrier_ready(owner[0], owner[2])
        second = start('competitor', alias / 'shared'); code, text = done(second)
        assert code != 0 and 'output_execution_conflict' in text and sessions(second[1]) == 0
        other = start('different-target', competition / 'independent'); other_code, other_text = done(other)
        assert other_code == 0, other_text
        assert owner[0].poll() is None and not owner[3].exists()
        owner[3].touch(); owner_code, owner_text = done(owner); assert owner_code == 0, owner_text
        user = competition / 'user'; user.mkdir(); (user / 'keep').write_bytes(b'owned-user-data')
        before = sha(user / 'keep'); rejected = start('existing-user', user); user_code, user_text = done(rejected)
        assert user_code != 0 and 'output_exists' in user_text and sha(user / 'keep') == before and sessions(rejected[1]) == 0
        assert sorted(p.name for p in user.iterdir()) == ['keep']
        assert not (competition / ('.filmcraft-execution-' + hashlib.sha256(str(user).encode()).hexdigest() + '.json')).exists()
        scenarios['FC-TX-001-OUTPUT'] = {'status': 'PASS', 'error': 'output_execution_conflict', 'canonicalParentAlias': True,
            'competitorNativeSessions': sessions(second[1]), 'ownerNativeSessions': sessions(owner[1]),
            'differentTargetCompletedWhileOwnerHeld': True, 'existingUserDirectoryPreserved': True,
            'ownerProjectSha256': sha(competition / 'shared/project.fcproj'),
            'independentProjectSha256': sha(competition / 'independent/project.fcproj'),
            'ownerTraceSha256': sha(owner[1]), 'competitorTraceSha256': sha(second[1])}; progress()
        interrupted = output / 'interrupted'; interrupted.mkdir(); target = interrupted / 'delivery'
        killed = start('killed-owner', target, 'save'); saved = barrier_ready(killed[0], killed[2]); checkpoint = Path(saved['checkpoint'])
        assert checkpoint.is_relative_to(output) and sha(checkpoint) == saved['checkpointSha256']
        killed[0].kill(); killed[0].wait(timeout=10)
        record = target.parent / ('.filmcraft-execution-' + hashlib.sha256(str(target).encode()).hexdigest() + '.json')
        persisted = json.loads(record.read_text()); assert persisted['state'] in ('running', 'reconciling')
        expected_plan = json.loads(plan.read_text())
        assert persisted['identity']['planHash'] == hashlib.sha256(json.dumps(expected_plan, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
        assert persisted['identity']['inputHashes'] == {k: v['sha256'] for k, v in expected_plan['assets'].items()}
        assert persisted['identity']['runtimeSha256'] == installed['binarySha256']
        assert persisted['identity']['projectRevision'] is None
        retry = start('retry-after-kill', target); retry_code, retry_text = done(retry)
        assert retry_code != 0 and 'output_execution_reconciling' in retry_text and sessions(retry[1]) == 0
        assert sha(checkpoint) == saved['checkpointSha256']
        mcp = load(skill / 'scripts/mcp_session.py', 'checkpoint_reopen')
        with mcp.Session([installed['executable'], '--project', str(checkpoint), 'mcp']) as session:
            inspection = command(session, 'project.inspect', {})
        assert isinstance(inspection, dict)
        scenarios['FC-TX-001-INTERRUPT'] = {'status': 'PASS', 'error': 'output_execution_reconciling',
            'recordState': persisted['state'], 'persistedIdentity': persisted['identity'], 'retryNativeSessions': sessions(retry[1]), 'checkpointPreserved': True,
            'checkpointReopened': True, 'checkpointSha256': sha(checkpoint), 'guardSha256': sha(record),
            'automaticCleanup': False, 'ownerKilledAfterActualNativeSave': True,
            'nativeStopAtOwnerDeath': 'NOT_ASSUMED', 'readonlyReopenInspectionSha256': hashlib.sha256(json.dumps(inspection, sort_keys=True).encode()).hexdigest()}; progress()
        # 仅清理本探针已知所有者进程组，不清理原工程、登记或失败暂存。
        try:
            if os.getpgid(saved['nativePid']) == killed[0].pid:
                args = subprocess.run(['/bin/ps', '-p', str(saved['nativePid']), '-o', 'command='], capture_output=True, text=True, timeout=3)
                if args.returncode == 0 and args.stdout.strip().startswith(installed['executable'] + ' '):
                    os.killpg(killed[0].pid, signal.SIGTERM)
        except ProcessLookupError: pass
        import shutil
        gui_source = output / 'gui-source'; shutil.copytree(output / 'admission/created', gui_source)
        original = sha(gui_source / 'project.fcproj'); revision = json.loads(plan.read_text()); revision.pop('document'); revision.pop('assets')
        revision['expectedProjectSha256'] = original; revision['operations'] = []
        revision_file = output / 'gui-revision.json'; revision_file.write_text(json.dumps(revision))
        binding_file = output / 'gui-binding.private.json'; resources_file = output / 'admission/resources.json'
        prepare = r"""
import {readFileSync,writeFileSync} from 'node:fs';import {join} from 'node:path';import {pathToFileURL} from 'node:url';
const [core,plan,source,out,runtime,bindingFile,policyFile]=process.argv.slice(1);
const {PythonWorkflowRunner}=await import(pathToFileURL(join(core,'src/adapters/python_workflow.ts')).href);
const {executionSubject}=await import(pathToFileURL(join(core,'src/harness/workflow_admission.ts')).href);
const manifest=JSON.parse(readFileSync(join(core,'plugin.json'))),lock=JSON.parse(readFileSync(join(core,'skills.lock.json')));
const runner=new PythonWorkflowRunner(null,null,{skillDirectory:join(core,'skills/filmcraft-use'),sourceRevision:lock.sources[0].sha,pluginVersion:manifest.version,runtimeHome:runtime,python:process.env.WRITER_QA_PYTHON});
const p=runner.prepare(plan,out,source);const binding={taskId:'gui-stale',namespace:'writer-boundary-QA',idempotencyKey:'gui-stale',planHash:p.planIdentity.canonicalPlanSha256,nativePlanHash:p.planIdentity.workflowPlanSha256,inputHashes:p.inputHashes,inputRefs:Object.entries(p.inputHashes).map(([assetId,sha256])=>({assetId,version:'synthetic-v1',sha256})),projectRevision:p.projectRevision,projectKey:p.projectKey,outputRoot:p.outputRoot,sourceRevision:lock.sources[0].sha,sourceTreeSha256:p.sourceTreeSha256,runtimeIdentity:p.runtimeIdentity,authorizationRef:'writer-QA',authorizationScopeSha256:'a'.repeat(64),deadline:Date.now()+600000};
writeFileSync(bindingFile,JSON.stringify(binding));console.log(JSON.stringify(executionSubject(binding,JSON.parse(readFileSync(policyFile)))));
"""
        prepared = subprocess.run([node, '--input-type=module', '-e', prepare, str(core), str(revision_file), str(gui_source), str(output / 'gui-refused'), str(runtime), str(binding_file), str(resources_file)],
                                  env={**os.environ, 'WRITER_QA_PYTHON': python}, capture_output=True, text=True, timeout=180)
        assert prepared.returncode == 0, prepared.stderr
        subject = json.loads(prepared.stdout); binding = json.loads(binding_file.read_text()); grants = output / 'gui-grants'; grants.mkdir(mode=0o700)
        grant = {'schema': 'filmcraft-local-authorization/v1', 'authorizationRef': binding['authorizationRef'],
                 'authorizationScopeSha256': binding['authorizationScopeSha256'], 'expiresAt': int(time.time() * 1000) + 600000,
                 'revoked': False, 'subjects': [hashlib.sha256(json.dumps(subject, sort_keys=True, separators=(',', ':')).encode()).hexdigest()]}
        grant_path = grants / (hashlib.sha256(binding['authorizationRef'].encode()).hexdigest() + '.json'); grant_path.write_text(json.dumps(grant)); grant_path.chmod(0o600)
        desktop = load(skill / 'scripts/desktop.py', 'writer_desktop'); desktop_lock = json.loads((skill / 'scripts/desktop.lock.json').read_text())
        desktop_identity = desktop.inspect(desktop_home / 'filmcraft-desktop' / desktop_lock['version'], desktop_lock)
        gui_dir = output / 'owned-gui'; gui_dir.mkdir(); ds = load(skill / 'scripts/desktop_session.py', 'writer_desktop_session')
        with socket.socket() as probe: probe.bind(('127.0.0.1', 0)); port = probe.getsockname()[1]
        commands = load(skill / 'scripts/commands.py', 'writer_commands')
        owned = ds.OwnedSession(commands.backend_argv(installed['executable'], gui_dir, 'bridge', '127.0.0.1:' + str(port)), desktop_identity, 'filmcraft', gui_dir, port)
        with owned as gui:
            command(gui.session, 'file.open', {'path': str(gui_source / 'project.fcproj')})
            command(gui.session, 'file.newSequence', {'name': 'External desktop change', 'width': 32, 'height': 32, 'fps': 12, 'video': 1, 'audio': 1})
            command(gui.session, 'file.save', {'path': str(gui_source / 'project.fcproj')})
            after_desktop = sha(gui_source / 'project.fcproj'); assert after_desktop != original
        ledger = output / 'gui-ledger.sqlite'
        attempted = subprocess.run([node, str(core / 'src/cli/workflow.ts'), 'run', '--binding', str(binding_file), '--plan', str(revision_file),
            '--resources', str(resources_file), '--source', str(gui_source), '--ledger', str(ledger), '--blobs', str(output / 'gui-blobs'),
            '--authorization-root', str(grants), '--runtime-home', str(runtime), '--python', python], capture_output=True, text=True, timeout=180)
        result = json.loads(attempted.stdout); assert attempted.returncode == 1 and result['error']['code'] == 'revision_conflict', attempted.stdout + attempted.stderr
        with sqlite3.connect('file:' + str(ledger) + '?mode=ro', uri=True) as db: attempts = db.execute('SELECT count(*) FROM attempts').fetchone()[0]
        assert attempts == 0 and sha(gui_source / 'project.fcproj') == after_desktop and not (output / 'gui-refused').exists()
        scenarios['FC-TX-001-N'] = {'status': 'PASS', 'error': 'revision_conflict', 'originalSha256': original,
            'desktopSavedSha256': after_desktop, 'sourcePreserved': True, 'nativeAttempts': attempts,
            'desktopVersion': desktop_lock['version'], 'desktopBinarySha256': desktop_lock['binarySha256'],
            'ownedDesktopStopped': owned.stopped, 'listenerOwnedByPID': owned.listener_verified,
            'interaction': 'actual signed desktop state edited and saved through its owned loopback bridge; no claim of manual UI clicks'}; progress()
        intact()
        report = {'schema': 'filmcraft-writer-boundaries/v1', 'result': 'PASS', 'plugin': expected,
            'hostReceiptSha256': sha(host / 'host-receipt.json'), 'runtimeIdentity': admission['runtimeIdentity'],
            'platform': sys.platform + '-' + os.uname().machine, 'scenarios': scenarios,
            'allInstalledSkillsUnchanged': True, 'allInstalledCodeUnchanged': True, 'fullV1': 'NOT_PROVEN',
            'verifierFilesSha256': {p.name: sha(p) for p in (Path(__file__), worker)},
            'scope': 'all FC-TX-001 scenarios on fixed macOS arm64 Codex/headless and owned signed desktop bridge; other platforms/hosts and full V1 remain open',
            'faultInjection': 'QA Session subclass delegates every native request to original Session; scheduling pauses only, actual owner SIGKILL after native save; payload files and installer not patched'}
        validate_report(report); (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n'); return report
    finally:
        for child in processes:
            if child.poll() is None:
                child.terminate()
                try: child.wait(timeout=10)
                except subprocess.TimeoutExpired: child.kill(); child.wait(timeout=10)
        for log in logs: log.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('host', 'repository', 'authority', 'output', 'desktop-home'): p.add_argument('--' + name, type=Path, required=True)
    for name in ('ref', 'node', 'python'): p.add_argument('--' + name, required=True)
    r = verify(**vars(p.parse_args())); print(json.dumps({'result': r['result'], 'scenarios': len(r['scenarios'])}))
