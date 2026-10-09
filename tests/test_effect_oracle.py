"""效果验收oracle不得吞掉源时间、曲线或非目标字段变化。"""
import copy
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('effect_oracle',Path(__file__).resolve().parents[1]/'scripts/verify_installed_effects.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class EffectOracleTests(unittest.TestCase):
    def fixture(self):
        return {'project':{'name':'before','root':{'name':'before'},'next_id':16,
            'items':{'6':{'kind':{'Sequence':{'video_tracks':[{'items':[{'id':11,'effects':[{'effect':'opacity','params':{'opacity':{'value':{'Float':100.0},
                'keyframes':[m.keyframe(1016064000000,{'Float':100.0}),m.keyframe(1270080000000,{'Float':0.0})]}}}]}]}],
                'audio_tracks':[{'volume_db':0.0}], 'markers':[]}}}}}}

    def test_only_known_save_as_names_are_compatible(self):
        a=self.fixture();b=copy.deepcopy(a);b['project']['name']='saved';b['project']['root']['name']='saved';m.assert_project(a,b)

    def test_one_source_tick_difference_is_rejected(self):
        a=self.fixture();b=copy.deepcopy(a)
        b['project']['items']['6']['kind']['Sequence']['video_tracks'][0]['items'][0]['effects'][0]['params']['opacity']['keyframes'][0]['time']+=1
        with self.assertRaises(AssertionError):m.assert_project(a,b)

    def test_wrong_curve_or_influence_is_rejected(self):
        for field,value in [('interp','Hold'),('in_influence',.25),('out_influence',.75),('value',{'Float':99.0})]:
            a=self.fixture();b=copy.deepcopy(a);b['project']['items']['6']['kind']['Sequence']['video_tracks'][0]['items'][0]['effects'][0]['params']['opacity']['keyframes'][0][field]=value
            with self.subTest(field=field),self.assertRaises(AssertionError):m.assert_project(a,b)

    def test_lost_keyframe_is_rejected(self):
        a=self.fixture();b=copy.deepcopy(a);b['project']['items']['6']['kind']['Sequence']['video_tracks'][0]['items'][0]['effects'][0]['params']['opacity']['keyframes'].pop()
        with self.assertRaises(AssertionError):m.assert_project(a,b)

    def test_non_target_audio_or_allocator_change_is_rejected(self):
        a=self.fixture();b=copy.deepcopy(a);b['project']['next_id']+=1
        with self.assertRaises(AssertionError):m.assert_project(a,b)
        b=copy.deepcopy(a);b['project']['items']['6']['kind']['Sequence']['audio_tracks'][0]['volume_db']=-3
        with self.assertRaises(AssertionError):m.assert_project(a,b)

if __name__=='__main__':unittest.main()
