#!/usr/bin/env python3
"""工程素材箱QA：为持续公开JSONL会话生成计划并独立核验完整工程。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def op(command, params=None, alias=None):
    result={'command':command,'params':params or {}}
    if alias:result['as']=alias
    return result


def expected_bin(base, bin_id):
    value=copy.deepcopy(base)
    assert value['project']['next_id']==bin_id
    value['project']['root']['children'].append({'Bin':{'id':bin_id,'name':'Owned bin','children':[]}})
    value['project']['next_id']+=1
    return value


def suite(base, bin_id, media_id, second_media):
    """各预期从输入独立构造，不能从被测保存结果复制目标字段。"""
    cases=[];next_id=base['project']['next_id']
    renamed=copy.deepcopy(base);renamed['project']['root']['children'][-1]['Bin']['name']='Renamed bin'
    cases.append(('project.renameBin',{'bin':bin_id,'name':'Renamed bin'},[],base,renamed))
    moved=copy.deepcopy(base);children=moved['project']['root']['children'];children.remove({'Item':media_id});children[-1]['Bin']['children'].append({'Item':media_id})
    cases.append(('project.moveToBin',{'items':[media_id],'bin':bin_id},[],base,moved))
    marked=copy.deepcopy(base);media=marked['project']['items'][str(media_id)]['kind']['Media'];media['mark_in']=254016000000;media['mark_out']=762048000000
    cases.append(('project.setMarks',{'item':media_id,'in':254016000000,'out':762048000000},[],base,marked))
    grouped=copy.deepcopy(base);children=grouped['project']['root']['children']
    for item in [media_id,second_media]:children.remove({'Item':item})
    children.append({'Bin':{'id':next_id,'name':'Selected media','children':[{'Item':media_id},{'Item':second_media}]}});grouped['project']['next_id']+=1
    cases.append(('file.newBinFromSelection',{'items':[media_id,second_media],'name':'Selected media'},[op('project.select',{'items':[media_id,second_media]})],base,grouped))
    # 独立新增未被序列引用的相同生成素材，删除时不借级联行为推断原序列。
    unused=copy.deepcopy(base);item=copy.deepcopy(unused['project']['items'][str(media_id)]);item['id']=next_id;item['created']=next_id
    unused['project']['items'][str(next_id)]=item;unused['project']['root']['children'].append({'Item':next_id});unused['project']['next_id']+=1
    removed=copy.deepcopy(base);removed['project']['next_id']+=1
    cases.append(('project.delete',{'items':[next_id]},[op('file.newColorMatte',{'color':'#e65527','seconds':20}),op('project.select',{'items':[next_id]})],unused,removed))
    operations=[];expected={}
    def capture(value):
        name='check_'+str(len(expected))+'.fcproj';operations.append(op('file.saveAs',{'path':{'$output':name}}));expected[name]=copy.deepcopy(value)
    for identifier,params,setup,before,after in cases:
        operations.extend(setup);capture(before);operations.append(op(identifier,params));capture(after)
        operations.append(op('edit.undo'));capture(before);operations.append(op('edit.redo'));capture(after)
        operations.append(op('edit.undo'));capture(before)
        # project.select不是持久编辑，不应多撤销一次。
        for row in reversed(setup):
            if row['command']!='project.select':operations.append(op('edit.undo'))
        capture(base)
    return operations,expected


def search_project(base, search_id):
    value=copy.deepcopy(base);assert value['project']['next_id']==search_id
    value['project']['search_bins']=[{'id':search_id,'name':'Color search','query':{'rows':[{'column':'Name','op':'contains','text':'Color'}],'match_all':True,'case_sensitive':False}}]
    value['project']['next_id']+=1
    return value


def search_suite(base, search_id):
    edited=copy.deepcopy(base);row=edited['project']['search_bins'][0];row['name']='Tone search';row['query'].update(match_all=False,case_sensitive=True);row['query']['rows'][0]['text']='Tone'
    deleted=copy.deepcopy(base);del deleted['project']['search_bins']
    operations=[];expected={};queries={}
    def capture(value,items=None):
        name='search_'+str(len(expected))+'.fcproj';operations.append(op('file.saveAs',{'path':{'$output':name}}));expected[name]=copy.deepcopy(value)
        if items is not None:
            alias='query_'+str(len(queries));operations.append(op('project.searchBinItems',{'bin':search_id},alias));queries[alias]={'bin':search_id,'items':items,**copy.deepcopy(value['project']['search_bins'][0])};queries[alias].pop('id')
    operations.append(op('project.editSearchBin',{'bin':search_id,'name':'Tone search','column':'Name','operator':'contains','text':'Tone','matchAll':False,'caseSensitive':True}));capture(edited,[12])
    operations.append(op('edit.undo'));capture(base,[7]);operations.append(op('edit.redo'));capture(edited,[12]);operations.append(op('edit.undo'));capture(base,[7])
    operations.append(op('project.deleteSearchBin',{'bin':search_id}));capture(deleted)
    operations.append(op('edit.undo'));capture(base,[7]);operations.append(op('edit.redo'));capture(deleted);operations.append(op('edit.undo'));capture(base,[7])
    return operations,expected,queries


def assert_project(actual,expected):
    def normalize(value):
        value=copy.deepcopy(value);value['project']['name']='Owned bins';value['project']['root']['name']='Owned bins';return value
    assert normalize(actual)==normalize(expected),'full project/bin mismatch'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--audit',type=Path,required=True);p.add_argument('--fixture',type=Path,required=True);p.add_argument('--mode',choices=['headless','bridge'],required=True);p.add_argument('--action',choices=['prepare','verify'],required=True)
    a=p.parse_args();root=a.audit.resolve();source=a.fixture.resolve();base=json.loads(source.read_text());bin_id=base['project']['next_id'];grouped=expected_bin(base,bin_id)
    # 此夹具仅选择两个确定为Synthetic的素材，其他对象保持全字段独立比较。
    ids=[int(k) for k,v in base['project']['items'].items() if 'Media' in v['kind']];assert len(ids)==2
    operations,expected=suite(grouped,bin_id,*ids)
    assert ids==[7,12], 'unsupported_procedural_fixture'
    searched=search_project(grouped,grouped['project']['next_id'])
    search_ops,search_expected,queries=search_suite(searched,grouped['project']['next_id'])
    if a.action=='prepare':
        initial={'name':'create','inputs':{'source':str(source)},'plan':{'schema':'craft-command-plan/v1','operations':[op('file.open',{'path':{'$ref':'source.path'}}),op('file.newBin',{'name':'Owned bin'},'bin'),op('project.inspect'),op('file.saveAs',{'path':{'$output':'bin.fcproj'}})]}}
        search_create={'name':'search_create','plan':{'schema':'craft-command-plan/v1','operations':[op('file.newSearchBin',{'name':'Color search','column':'Name','operator':'contains','text':'Color'},'search'),op('project.searchBinItems',{'bin':{'$ref':'search.bin'}},'search_items'),op('file.saveAs',{'path':{'$output':'search.fcproj'}})]}}
        for label,request in [('create',initial),('search_create',search_create)]:
            (root/(a.mode+'-'+label+'-request.private.json')).write_text(json.dumps(request)+'\n')
        request={'name':'bin_cases','plan':{'schema':'craft-command-plan/v1','operations':operations}}
        (root/(a.mode+'-cases-request.private.json')).write_text(json.dumps(request)+'\n')
        (root/(a.mode+'-search-request.private.json')).write_text(json.dumps({'name':'search_cases','plan':{'schema':'craft-command-plan/v1','operations':search_ops+[op('file.saveAs',{'path':{'$output':'persistent.fcproj'}})]}})+'\n')
        reopen_ops,reopen_expected=suite(searched,bin_id,*ids)
        reopen_request={'name':'reopen_revision','inputs':{'source':str(root/a.mode/'search_cases/persistent.fcproj')},'plan':{'schema':'craft-command-plan/v1','operations':[op('file.closeAllProjects',{'force':True}),op('file.open',{'path':{'$ref':'source.path'}})]+reopen_ops+search_ops+[op('project.renameBin',{'bin':bin_id,'name':'Reopened revised'}),op('project.moveToBin',{'items':[ids[0]],'bin':bin_id}),op('project.setMarks',{'item':ids[0],'in':254016000000,'out':508032000000}),op('file.saveAs',{'path':{'$output':'revised.fcproj'}}),op('edit.undo'),op('edit.undo'),op('edit.undo'),op('file.saveAs',{'path':{'$output':'restored.fcproj'}}),op('command.list')]}}
        (root/(a.mode+'-reopen-request.private.json')).write_text(json.dumps(reopen_request)+'\n')
        print('prepared',len(expected),'initial project checkpoints plus search/reopen phases')
    else:
        work=root/a.mode
        assert_project(json.loads((work/'create/bin.fcproj').read_text()),grouped)
        for filename,value in expected.items():assert_project(json.loads((work/'bin_cases'/filename).read_text()),value)
        assert_project(json.loads((work/'search_create/search.fcproj').read_text()),searched)
        search_stage='explicit_search_cases' if (work/'explicit_search_cases').is_dir() else 'search_cases'
        reopen_search_stage='explicit_reopen_search' if (work/'explicit_reopen_search').is_dir() else 'reopen_revision'
        for filename,value in search_expected.items():assert_project(json.loads((work/search_stage/filename).read_text()),value)
        assert_project(json.loads((work/search_stage/'persistent.fcproj').read_text()),searched)
        _,reopen_expected=suite(searched,bin_id,*ids)
        for filename,value in reopen_expected.items():assert_project(json.loads((work/'reopen_revision'/filename).read_text()),value)
        for filename,value in search_expected.items():assert_project(json.loads((work/reopen_search_stage/filename).read_text()),value)
        revised=copy.deepcopy(searched);revised['project']['root']['children'][-1]['Bin']['name']='Reopened revised';revised['project']['root']['children'].remove({'Item':ids[0]});revised['project']['root']['children'][-1]['Bin']['children'].append({'Item':ids[0]});revised['project']['items'][str(ids[0])]['kind']['Media'].update(mark_in=254016000000,mark_out=508032000000)
        assert_project(json.loads((work/'reopen_revision/revised.fcproj').read_text()),revised)
        assert_project(json.loads((work/'reopen_revision/restored.fcproj').read_text()),searched)
        receipts=[json.loads(line) for line in (root/(a.mode+'-stream.private.jsonl')).read_text().splitlines()]
        successful=[r for r in receipts if r.get('result')=='PASS']
        assert successful[0]['inputs']['source']['sha256']==sha(source)
        assert successful[0]['steps'][1]['result']=={'bin':bin_id}
        initial_search=next(r for r in successful if any(s.get('command')=='file.newSearchBin' for s in r.get('steps',[])))
        expected_initial={'bin':grouped['project']['next_id'],'items':[ids[0]],'name':'Color search','query':searched['project']['search_bins'][0]['query']}
        for step in initial_search['steps'][:2]:assert step['result']==expected_initial
        receipts_by_sha={r['planSha256']:r for r in successful}
        query_count=0
        for kind in (['explicit_search','explicit_reopen'] if (work/'explicit_search_cases').is_dir() else ['search','reopen']):
            request=json.loads((root/(a.mode+'-'+kind+'-request.private.json')).read_text());plan=request['plan']
            plan_sha=hashlib.sha256(json.dumps(plan,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()
            receipt=receipts_by_sha[plan_sha];assert len(receipt['steps'])==len(plan['operations'])
            for operation,step in zip(plan['operations'],receipt['steps']):
                assert operation['command']==step['command'] and step['state']=='succeeded'
                if operation.get('as') in queries:
                    assert step['result']==queries[operation['as']];query_count+=1
        assert query_count==12
        print('PASS',1+len(expected)+1+len(search_expected)+1+len(reopen_expected)+len(search_expected)+2,'complete projects /14 exact search results / reopened revision')


if __name__=='__main__':main()
