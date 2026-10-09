"""标记查询字段缺失不能掩盖保存工程评论和非目标字段错误。"""
import copy
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('marker_oracle',Path(__file__).resolve().parents[1]/'scripts/verify_installed_markers_settings.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class MarkerOracleTests(unittest.TestCase):
    def setUp(self):
        marker={'id':16,'start':100,'duration':20,'comment':'required'}
        self.expected={'id':6,'markers':[marker],'video':[{'duration':200}]}
        self.actual=copy.deepcopy(self.expected);self.actual['markers'][0].pop('comment')
        self.saved={'project':{'items':{'6':{'kind':{'Sequence':{'markers':[copy.deepcopy(marker)]}}}}}}
    def test_requires_real_serialized_comment(self):
        with self.assertRaisesRegex(AssertionError,'metadata required'): module.assert_sequence(self.actual,self.expected)
    def test_detects_comment_loss_even_when_query_omits_it(self):
        self.saved['project']['items']['6']['kind']['Sequence']['markers'][0]['comment']='lost'
        with self.assertRaisesRegex(AssertionError,'marker fields'): module.assert_sequence(self.actual,self.expected,self.saved)
    def test_detects_non_target_frame_change(self):
        self.actual['video'][0]['duration']+=1
        with self.assertRaisesRegex(AssertionError,'sequence fields'): module.assert_sequence(self.actual,self.expected,self.saved)
    def test_exact_saved_metadata_and_query_pass(self):
        module.assert_sequence(self.actual,self.expected,self.saved)

if __name__=='__main__':unittest.main()
