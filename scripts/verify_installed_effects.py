#!/usr/bin/env python3
"""固定安装效果／关键帧命令：公开任务实例复用、完整工程及可独立解码画面。"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(path, name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def assert_project(actual, expected):
    """只归一化已知saveAs名称，保留所有对象、时间、关键帧和非目标字段。"""
    def normalize(v):
        v=copy.deepcopy(v);v['project']['name']='Owned effects';v['project']['root']['name']='Owned effects';return v
    assert normalize(actual)==normalize(expected),'complete effect project mismatch'


def keyframe(time, value, interpolation='Linear'):
    return {'time':time,'value':copy.deepcopy(value),'interp':interpolation,'in_influence':1/3,'out_influence':1/3}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for n in ['installed-plugin','runtime-home','timeline-audit','output']:parser.add_argument('--'+n,type=Path,required=True)
    parser.add_argument('--plugin-sha',required=True);parser.add_argument('--source-sha',required=True)
    args=parser.parse_args();root=args.output.resolve();root.mkdir(mode=0o700)
    runtime=args.runtime_home.resolve(strict=True);audit=args.timeline_audit.resolve(strict=True)
    scripts=args.installed_plugin.resolve(strict=True)/'skills/filmcraft-use/scripts'
    commands=load(scripts/'commands.py','fx_commands');task=load(scripts/'task_session.py','fx_task')
    helper=load(Path(__file__).with_name('verify_installed_timeline_edits.py'),'fx_helper')
    matrix=load(Path(__file__).with_name('command_evidence.py'),'fx_matrix');op=helper.op;sha=helper.digest;write=helper.write
    results=[]
    for mode in ['headless','bridge']:
        work=root/mode;source=audit/mode/'fixture/baseline.fcproj';source_hash=sha(source);base=json.loads(source.read_text())
        state=json.loads((audit/mode/'fixture-receipt.private.json').read_text())['steps'][-2]['result']
        seq_id=str(state['id']);target=state['video'][1]['items'][0]['clip']
        def clip(value):return next(i for t in value['project']['items'][seq_id]['kind']['Sequence']['video_tracks'] for i in t['items'] if i['id']==target)
        def effect(value, name='motion'):return next(e for e in clip(value)['effects'] if e['effect']==name)
        def param(value, name='position', fx='motion'):return effect(value,fx)['params'][name]
        start=clip(base)['start'];media=clip(base)['source_in'];T=helper.TICKS
        common={'clip':target,'effect':'motion','param':'position'}
        position=copy.deepcopy(param(base)['value'])
        def animated(time=media, interpolation='Linear'):
            v=copy.deepcopy(base);param(v)['keyframes']=[keyframe(time,position,interpolation)];return v
        gaussian={'effect':'gaussian_blur','enabled':True,'params':{'blurriness':{'value':{'Float':0.0}},'dimensions':{'value':{'Choice':0}},'repeat_edge':{'value':{'Bool':False}}}}
        applied=copy.deepcopy(base);clip(applied)['effects'].insert(0,gaussian)
        moved=copy.deepcopy(base);param(moved)['value']={'Vec2':{'x':8.0,'y':16.0}}
        disabled=copy.deepcopy(base);effect(disabled)['enabled']=False
        add=op('effects.addKeyframe',{**common,'time':start})
        changed_key=animated();param(changed_key)['keyframes'][0].update(value={'Vec2':{'x':8.0,'y':16.0}},in_influence=.25,out_influence=.75)
        cases=[
            ('effects.apply',{'clips':[target],'effect':'gaussian_blur'},[],base,applied),
            ('effects.remove',{'clip':target,'index':0},[op('effects.apply',{'clips':[target],'effect':'gaussian_blur'})],applied,base),
            ('effects.setParam',{**common,'value':[8,16]},[],base,moved),
            ('effects.toggleAnimation',common,[],base,animated()),
            ('effects.toggleEnabled',{'clip':target,'index':0},[],base,disabled),
            ('effects.reset',{'clip':target,'index':0},[op('effects.setParam',{**common,'value':[8,16]})],moved,base),
            ('effects.addKeyframe',{**common,'time':start+T},[],base,animated(media+T)),
            ('effects.deleteKeyframe',{**common,'mediaTime':media},[add],animated(),base),
            ('effects.moveKeyframe',{**common,'mediaTime':media,'to':media+T},[add],animated(),animated(media+T)),
            ('effects.setKeyframe',{**common,'mediaTime':media,'value':[8,16],'inInfluence':.25,'outInfluence':.75},[add],animated(),changed_key),
        ]
        for native,stored in [('linear','Linear'),('bezier','Bezier'),('autoBezier','AutoBezier'),('continuousBezier','ContinuousBezier'),('hold','Hold'),('easeIn','EaseIn'),('easeOut','EaseOut')]:
            cases.append(('effects.setInterpolation',{**common,'mediaTime':media,'interpolation':native},[add],animated(),animated(interpolation=stored)))
        identifiers=sorted({c[0] for c in cases}|{'effects.list','file.exportFrame'});comparisons=[];receipts={};images={}
        policy=commands.load('execution_permissions').from_cli([str(root),str(audit)],[str(root),str(runtime)])
        with task.TaskSession(work,runtime,policy,mode,protected_paths=[audit]) as session:
            def execute(name,operations,inputs=None):
                operations=[row for part in operations for row in (part if isinstance(part,list) else [part])]
                plan={'schema':'craft-command-plan/v1','operations':operations};write(work/(name+'-plan.private.json'),plan)
                result=session.execute(plan,name,inputs);write(work/(name+'-receipt.private.json'),result)
                assert result['result']=='PASS',result.get('error');receipts[name]=sha(work/(name+'-receipt.private.json'));return result
            def suite():
                operations=[op('playhead.set',{'time':start})];expected={}
                def save(value):
                    name='check_'+str(len(expected))+'.fcproj';operations.append(op('file.saveAs',{'path':{'$output':name}}));expected[name]=copy.deepcopy(value)
                for identifier,params,setup,before,after in cases:
                    operations.extend(setup);operations.append(op(identifier,params));save(after)
                    operations.append(op('edit.undo'));save(before);operations.append(op('edit.redo'));save(after)
                    operations.append(op('edit.undo'));save(before)
                    operations.extend(op('edit.undo') for _ in setup);save(base)
                return operations,expected
            def check(name,expected):
                for file,value in expected.items():
                    try:assert_project(json.loads((work/name/file).read_text()),value)
                    except AssertionError as e:raise AssertionError((mode,name,file,str(e))) from e
                comparisons.append({'phase':name,'completeProjects':len(expected)})
            def render(label,seconds):
                return [op('playhead.set',{'seconds':seconds}),{'command':'file.exportFrame','params':{'path':{'$output':label+'.png'},'format':'png','import':False},'as':label}]
            def collect(name,result):
                for operation,step in zip(json.loads((work/(name+'-plan.private.json')).read_text())['operations'],result['steps']):
                    if operation.get('command')=='file.exportFrame':
                        path=work/name/operation['params']['path']['$output'];images[operation['as']]={'path':str(path.relative_to(work)),'sha256':sha(path)}
            operations,expected=suite()
            opacity={'clip':target,'effect':'opacity','param':'opacity'}
            visual=[render('baseline',8.5),op('effects.setParam',{**common,'value':[8,16]}),render('shifted',8.5),op('edit.undo'),
                op('playhead.set',{'time':start}),op('effects.toggleAnimation',opacity),
                op('effects.setParam',{**opacity,'value':0,'time':start+T}),render('linear_start',8),render('linear_half',8.5),render('linear_end',9),
                op('effects.setInterpolation',{**opacity,'mediaTime':media,'interpolation':'hold'}),render('hold_half',8.5),op('edit.undo'),
                op('file.saveAs',{'path':{'$output':'animated.fcproj'}})]
            first=execute('create',[op('file.open',{'path':{'$ref':'source.path'}}),op('effects.list',{'kind':'Video','detail':True})]+operations+visual,{'source':source})
            check('create',expected);collect('create',first)
            persistent=copy.deepcopy(base);param(persistent,'opacity','opacity')['keyframes']=[keyframe(media,{'Float':100.0}),keyframe(media+T,{'Float':0.0})]
            assert_project(json.loads((work/'create/animated.fcproj').read_text()),persistent)
            saved=work/'create/animated.fcproj';saved_hash=sha(saved)
            execute('reopen',[op('file.closeAllProjects',{'force':True}),op('file.open',{'path':{'$ref':'source.path'}}),
                op('file.saveAs',{'path':{'$output':'reopened.fcproj'}})],{'source':saved})
            assert_project(json.loads((work/'reopen/reopened.fcproj').read_text()),persistent)
            revise=[render('reopened_half',8.5),op('effects.setKeyframe',{**opacity,'mediaTime':media+T,'value':100}),render('revised_half',8.5),
                op('file.saveAs',{'path':{'$output':'revised.fcproj'}}),op('edit.undo'),
                op('playhead.set',{'time':start}),op('effects.toggleAnimation',opacity)]
            operations,expected=suite()
            result=execute('revision',revise+operations+[op('effects.list',{'kind':'Video','detail':True}),render('restored',8.5),op('file.saveAs',{'path':{'$output':'restored.fcproj'}})])
            collect('revision',result);check('revision',expected)
            revised=copy.deepcopy(persistent);param(revised,'opacity','opacity')['keyframes'][1]['value']={'Float':100.0}
            assert_project(json.loads((work/'revision/revised.fcproj').read_text()),revised)
            assert_project(json.loads((work/'revision/restored.fcproj').read_text()),base)
            assert sha(source)==source_hash and sha(saved)==saved_hash
            negatives=[]
            for index,identifier in enumerate(identifiers):
                bad={'schema':'craft-command-plan/v1','operations':[op(identifier,{'UNDEFINED_EFFECT_FIELD':True})]}
                destination=work/('invalid_'+str(index))
                try:commands.execute(bad,destination,runtime_home=runtime,permissions=policy)
                except ValueError as e:assert str(e)=='invalid_native_parameters'
                else:raise AssertionError('undefined effect field accepted')
                assert not destination.exists();negatives.append(identifier)
            rows=execute('discovery',[op('command.list')])['steps'][0]['result']
            execute('close_project',[op('file.closeAllProjects',{'force':True})])
            denied=session.execute({'schema':'craft-command-plan/v1','operations':[op('effects.apply',{'clips':[target],'effect':'gaussian_blur'})]},'empty_refusal')
            assert denied['result']=='FAIL' and denied['steps'][-1]['state']=='blocked' and denied['error'].startswith('precondition_failed:')
            write(work/'empty-refusal.private.json',denied)
            try:session.execute({'schema':'craft-command-plan/v1','operations':[op('state.inspect',{})]},'after_stop')
            except RuntimeError as e:assert str(e)=='task_session_stopped'
            else:raise AssertionError('continued after refusal')
            assert not (work/'after_stop').exists()
        proof=json.loads((work/'task-session.json').read_text());assert proof['sessionsStarted']==1 and proof['singleProcessIdentity'] and proof['closed'] and proof['ownedProcessesStopped'] and proof['stopped']
        binding={'pluginSha':args.plugin_sha,'sourceSha':args.source_sha,'runtimeSha256':first['runtimeSha256'],'runtimeVersion':'0.2.0-craft.5','platform':'darwin-arm64','mode':mode}
        scopes={'parameterValidation':'Actual valid parameters; all13 undefined-field refusals before output.',
            'positiveExecution':'Eleven editing commands, all7 interpolation enums, detail query and full-resolution native frame export; exact whole-project/undo/redo comparisons. Images await independent decoding.',
            'negativeRejection':'Each command rejects undefined fields. Only effects.apply has actual empty-native blocked evidence; public task then stops without restart.',
            'reopen':'Opacity keyframes saved/closed/reopened, all17 editing cases rerun after reopen; query repeated.',
            'nonTargetPreservation':'85 complete project checkpoints per phase plus persistent/reopened/revised/restored artifacts; source and saved input hashes unchanged.'}
        observations=[{'command':identifier,'dimension':dim,'status':'PASS','evidence':'observations.json','scope':scope} for identifier in identifiers for dim,scope in scopes.items()]
        write(work/'matrix.json',matrix.build(rows,binding,{'binding':binding,'observations':observations}))
        write(work/'observations.json',{'binding':binding,'commands':identifiers,'comparisons':comparisons,'sourceSha256':source_hash,'savedInputSha256':saved_hash,
            'receiptsSha256':receipts,'renderImages':images,'unknownFieldRefusals':negatives,'emptyNativeRefusal':{'command':'effects.apply','receiptSha256':sha(work/'empty-refusal.private.json')},
            'keyframeScope':'mediaTime/to are exact source media ticks; time/playhead converted from timeline. Seven interpolation modes stored; only linear/hold output independently tested.',
            'fullV1':'NOT_PROVEN'})
        results.append({'mode':mode,'result':'PASS','commands':len(identifiers),'completeProjectComparisons':sum(r['completeProjects'] for r in comparisons)+4,'pngOutputs':len(images),
            'matrixSha256':sha(work/'matrix.json'),'observationsSha256':sha(work/'observations.json'),'sessionSha256':sha(work/'task-session.json')})
        print(mode,'PASS13 effect/export commands /17 cases / continuous task',flush=True)
    write(root/'report.json',{'schema':'filmcraft-fixed-effect-commands/v1','result':'PASS','results':results,'driverSha256':sha(Path(__file__)),
        'taskSessionSha256':sha(scripts/'task_session.py'),'fullCommandAcceptance':'NOT_PROVEN','remainingTask':'8.3','renderAcceptance':'independent decoder required'})


if __name__=='__main__':main()
