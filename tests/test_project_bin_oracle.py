"""工程素材箱oracle不能遗漏内容、分配器、源入出点及非目标序列。"""
import copy
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('bin_oracle',Path(__file__).resolve().parents[1]/'scripts/verify_project_bins.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ProjectBinOracleTests(unittest.TestCase):
    def fixture(self):
        return {'project':{'name':'source','root':{'id':0,'name':'source','children':[{'Item':7},{'Item':12}]},'next_id':16,'items':{'7':{'id':7,'created':7,'kind':{'Media':{'mark_in':None,'mark_out':None}}},'12':{'id':12,'created':12,'kind':{'Media':{'mark_in':None,'mark_out':None}}}},'sequence':{'tracks':[{'clips':[1,2]}]}}}

    def test_allocated_bin_and_nested_items_have_exact_identity(self):
        base=m.expected_bin(self.fixture(),16);ops,expected=m.suite(base,16,7,12)
        grouped=next(v for v in expected.values() if v['project']['next_id']==18 and any('Bin' in c and c['Bin']['name']=='Selected media' for c in v['project']['root']['children']))
        self.assertEqual(grouped['project']['root']['children'][-1],{'Bin':{'id':17,'name':'Selected media','children':[{'Item':7},{'Item':12}]}})
        self.assertEqual(len(expected),30)
        self.assertIn('project.delete',{o['command'] for o in ops})

    def test_wrong_bin_name_or_missing_item_refused(self):
        expected=m.expected_bin(self.fixture(),16)
        actual=copy.deepcopy(expected);actual['project']['root']['children'][-1]['Bin']['name']='wrong'
        with self.assertRaises(AssertionError):m.assert_project(actual,expected)
        actual=copy.deepcopy(expected);actual['project']['root']['children'].pop(0)
        with self.assertRaises(AssertionError):m.assert_project(actual,expected)

    def test_wrong_allocator_refused(self):
        expected=m.expected_bin(self.fixture(),16);actual=copy.deepcopy(expected);actual['project']['next_id']+=1
        with self.assertRaises(AssertionError):m.assert_project(actual,expected)
        with self.assertRaises(AssertionError):m.expected_bin(self.fixture(),17)

    def test_source_tick_and_non_target_sequence_change_refused(self):
        expected=m.expected_bin(self.fixture(),16)
        actual=copy.deepcopy(expected);actual['project']['items']['7']['kind']['Media']['mark_in']=1
        with self.assertRaises(AssertionError):m.assert_project(actual,expected)
        actual=copy.deepcopy(expected);actual['project']['sequence']['tracks'][0]['clips'].reverse()
        with self.assertRaises(AssertionError):m.assert_project(actual,expected)

    def test_only_save_as_names_normalized(self):
        expected=m.expected_bin(self.fixture(),16);actual=copy.deepcopy(expected)
        actual['project']['name']='saved';actual['project']['root']['name']='saved';m.assert_project(actual,expected)
        actual['project']['root']['id']=1
        with self.assertRaises(AssertionError):m.assert_project(actual,expected)

if __name__=='__main__':unittest.main()
