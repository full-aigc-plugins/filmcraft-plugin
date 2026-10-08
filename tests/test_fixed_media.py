"""固定媒体验收不能接受旧宿主、候选或缺失的原生测量。"""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))


class FixedMediaTests(unittest.TestCase):
    def test_each_native_measurement_is_required_independently(self):
        from verify_fixed_media import validate_fixed_media
        import json
        root=Path(__file__).resolve().parents[1]
        report=json.loads((root/'docs/evidence/filmcraft54-media-candidate-20261009/report.json').read_text())
        report['layer']='native-matrix'
        expected={'ref':'v0.1.0-dev.54','sha':'a'*40}
        host={'schema':'filmcraft-fixed-host-verification/v1','result':'PASS','plugin':expected,'loadingErrors':0}
        validate_fixed_media(host,report,expected)
        for mutation in ('correlation','tail','channel','alpha','font','relink','refusal','missing'):
            broken=copy.deepcopy(report);cases=broken['cases']
            if mutation=='correlation':cases['vfr']['measurements']['audio'][0]['correlation']=.5
            if mutation=='tail':cases['long-audio-tail']['measurements']['aac']['tail'][0]['sampleCount']=543
            if mutation=='channel':cases['long-audio-tail']['measurements']['pcm']['tail'].pop()
            if mutation=='alpha':cases['transparent-sequence']['measurements']['pixels'][0]['maximumChannelError']=4
            if mutation=='font':cases['font-change']['measurements']['fonts'][0].pop('licenseSha256')
            if mutation=='relink':cases['dependency-move']['measurements']['relinkedPixelsUnchanged']=False
            if mutation=='refusal':cases['bad-file']['measurements']['successfulDeliveryExists']=True
            if mutation=='missing':cases.pop('missing-font')
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate_fixed_media(host,broken,expected)

    def test_candidate_old_host_and_incomplete_matrix_are_refused(self):
        from verify_fixed_media import validate_fixed_media
        from media_matrix import CASES
        expected={'ref':'v0.1.0-dev.54','sha':'a'*40}
        host={'schema':'filmcraft-fixed-host-verification/v1','result':'PASS','plugin':expected,'loadingErrors':0}
        report={'result':'PASS','layer':'native-matrix','installationPreserved':True,
                'cases':{name:{'status':'PASS','measurements':{}} for name in CASES}}
        for mutation in ('candidate','old-host','no-measurements','changed-files'):
            h,r=copy.deepcopy(host),copy.deepcopy(report)
            if mutation=='candidate':r['layer']='private-native-candidate'
            if mutation=='old-host':h['plugin']['sha']='b'*40
            if mutation=='changed-files':r['installationPreserved']=False
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate_fixed_media(h,r,expected)
