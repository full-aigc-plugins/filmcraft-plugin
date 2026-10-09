"""完整原生工程比较不能遗漏查询未暴露的片段属性。"""
import copy
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('property_oracle',Path(__file__).resolve().parents[1]/'scripts/verify_installed_clip_properties.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class PropertyOracleTests(unittest.TestCase):
    def setUp(self):
        self.expected={'project':{'name':'source','root':{'name':'source'},'next_id':16,
            'items':{'target':{'frame_hold':100,'hold_filters':True,'gain_db':-3,'time_interpolation':'opticalFlow'},
                     'other':{'duration':1000}}}}
    def test_save_as_name_only_is_compatible(self):
        actual=copy.deepcopy(self.expected);actual['project']['name']='copy';actual['project']['root']['name']='copy'
        module.assert_project(actual,self.expected)
    def test_hold_filter_loss_is_refused(self):
        actual=copy.deepcopy(self.expected);actual['project']['items']['target'].pop('hold_filters')
        with self.assertRaises(AssertionError):module.assert_project(actual,self.expected)
    def test_non_target_tick_change_is_refused(self):
        actual=copy.deepcopy(self.expected);actual['project']['items']['other']['duration']+=1
        with self.assertRaises(AssertionError):module.assert_project(actual,self.expected)
    def test_gain_and_interpolation_changes_are_refused(self):
        for key,value in [('gain_db',0),('time_interpolation','frameSampling')]:
            actual=copy.deepcopy(self.expected);actual['project']['items']['target'][key]=value
            with self.assertRaises(AssertionError):module.assert_project(actual,self.expected)
    def test_unexpected_allocator_change_is_refused(self):
        actual=copy.deepcopy(self.expected);actual['project']['next_id']+=1
        with self.assertRaises(AssertionError):module.assert_project(actual,self.expected)

if __name__=='__main__':unittest.main()
