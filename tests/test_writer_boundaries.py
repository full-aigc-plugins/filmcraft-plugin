"""TX-001逐场景证据门禁；原生探针不能靠计数或整体PASS关闭任务。"""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


class WriterBoundaryTests(unittest.TestCase):
    def test_filmcraft_native_command_route_detects_save_checkpoint(self):
        probe = load('probe_workflow_writer')
        self.assertEqual(probe.command_identity('command_run', {'id': 'file.saveAs', 'params': {'path': 'x'}}), 'file.saveAs')
        self.assertEqual(probe.command_identity('sequence_inspect', {}), 'sequence_inspect')
        self.assertIsNone(probe.command_identity('command_run', {}))

    def test_all_five_observable_scenarios_are_required(self):
        module = load('verify_writer_boundaries')
        admission = {'status': 'PASS', 'nativeCases': 7, 'evidenceSha256': 'a' * 64, 'runtimeIdentity': {'sha256': 'b' * 64}}
        report = {'schema': 'filmcraft-writer-boundaries/v1', 'result': 'PASS', 'fullV1': 'NOT_PROVEN',
                  'allInstalledSkillsUnchanged': True, 'allInstalledCodeUnchanged': True, 'scenarios': {
            'FC-TX-001-P': copy.deepcopy(admission), 'FC-TX-001-HOST-ADMISSION': copy.deepcopy(admission),
            'FC-TX-001-N': {'status': 'PASS', 'error': 'revision_conflict', 'sourcePreserved': True,
                           'originalSha256': 'c' * 64, 'desktopSavedSha256': 'd' * 64, 'nativeAttempts': 0,
                           'ownedDesktopStopped': True, 'listenerOwnedByPID': True},
            'FC-TX-001-OUTPUT': {'status': 'PASS', 'error': 'output_execution_conflict', 'competitorNativeSessions': 0,
                                'ownerNativeSessions': 1, 'differentTargetCompletedWhileOwnerHeld': True,
                                'existingUserDirectoryPreserved': True},
            'FC-TX-001-INTERRUPT': {'status': 'PASS', 'error': 'output_execution_reconciling', 'retryNativeSessions': 0,
                                  'recordState': 'running', 'checkpointPreserved': True, 'checkpointReopened': True, 'automaticCleanup': False}}}
        errors = {'planHash': 'plan_identity_conflict', 'nativePlanHash': 'plan_identity_conflict',
                  'inputHashes': 'input_identity_conflict', 'projectRevision': 'revision_conflict',
                  'sourceTreeSha256': 'source_identity_conflict', 'sourceRevision': 'source_identity_conflict',
                  'runtimeIdentity': 'runtime_identity_conflict'}
        report['scenarios']['FC-TX-001-P']['bindingRejections'] = [
            {'field': k, 'status': 'PASS', 'error': v, 'nativeAttempts': 0, 'outputExists': False} for k, v in errors.items()]
        module.validate_report(report)
        edits = [lambda r: r['scenarios']['FC-TX-001-P']['bindingRejections'].pop(),
                 lambda r: r['scenarios']['FC-TX-001-P']['bindingRejections'][0].update(nativeAttempts=1), lambda r: r['scenarios'].pop('FC-TX-001-N'), lambda r: r.update(allInstalledCodeUnchanged=False),
                 lambda r: r['scenarios']['FC-TX-001-P'].update(nativeCases=0),
                 lambda r: r['scenarios']['FC-TX-001-HOST-ADMISSION'].update(evidenceSha256='missing'),
                 lambda r: r['scenarios']['FC-TX-001-N'].update(desktopSavedSha256='c' * 64),
                 lambda r: r['scenarios']['FC-TX-001-N'].update(listenerOwnedByPID=False),
                 lambda r: r['scenarios']['FC-TX-001-OUTPUT'].update(competitorNativeSessions=1),
                 lambda r: r['scenarios']['FC-TX-001-OUTPUT'].update(differentTargetCompletedWhileOwnerHeld=False),
                 lambda r: r['scenarios']['FC-TX-001-INTERRUPT'].update(retryNativeSessions=1),
                 lambda r: r['scenarios']['FC-TX-001-INTERRUPT'].update(checkpointReopened=False),
                 lambda r: r['scenarios']['FC-TX-001-INTERRUPT'].update(automaticCleanup=True)]
        for edit in edits:
            candidate = copy.deepcopy(report); edit(candidate)
            with self.assertRaises(ValueError): module.validate_report(candidate)


if __name__ == '__main__': unittest.main()
