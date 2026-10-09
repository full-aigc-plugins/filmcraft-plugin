"""示波器别名oracle必须识别播放头回退、单桶错误和不完整画面。"""
import copy
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('scope_alias_oracle',Path(__file__).resolve().parents[1]/'scripts/verify_scope_time_aliases.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ScopeAliasOracleTests(unittest.TestCase):
    def fixture(self):
        h={'samples':1024,'below':[0]*4,'above':[0]*4,'peakBin':{}}
        for c,i in zip('rgb',[230,85,39]):h[c]=[0]*256;h[c][i]=1024;h['peakBin'][c]=i
        return {'frame':204,'time':204*m.FRAME,'samples':[32,32],'colorSpace':'Rec. 709','histogram':h}
    def test_valid_histogram_passes(self):m.assert_scope(self.fixture(),204)
    def test_playhead_fallback_is_rejected(self):
        v=self.fixture();v.update(frame=0,time=0)
        with self.assertRaises(AssertionError):m.assert_scope(v,204)
    def test_single_bucket_cannot_hide_behind_correct_peak(self):
        v=self.fixture();v['histogram']['r'][229]=1
        with self.assertRaises(AssertionError):m.assert_scope(v,204)
    def test_wrong_sample_shape_or_source_tick_is_rejected(self):
        for field,value in [('samples',[32,26]),('time',204*m.FRAME+1)]:
            v=copy.deepcopy(self.fixture());v[field]=value
            with self.subTest(field=field),self.assertRaises(AssertionError):m.assert_scope(v,204)
if __name__=='__main__':unittest.main()
