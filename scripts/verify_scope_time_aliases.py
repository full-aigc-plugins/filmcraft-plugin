#!/usr/bin/env python3
"""固定安装示波器时间别名；单实例连续查询和重开，不使用播放头自证别名。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

TICKS=254016000000
FRAME=TICKS//24


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assert_scope(view,frame):
    """夹具204帧为均匀橙色，276帧为空隙黑色；逐RGB直方桶独立核验。"""
    assert view['frame']==frame and view['time']==frame*FRAME,'scope time alias ignored'
    assert view['samples']==[32,32] and view['colorSpace']=='Rec. 709','scope image contract mismatch'
    h=view['histogram'];assert h['samples']==1024 and h['below']==h['above']==[0]*4
    expected=(230,85,39) if frame==204 else (0,0,0)
    assert frame in (204,276)
    for channel,index in zip('rgb',expected):
        bins=[0]*256;bins[index]=1024
        assert h[channel]==bins and h['peakBin'][channel]==index,'scope full histogram mismatch'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['installed-plugin','runtime-home','timeline-audit','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();root=a.output.resolve();root.mkdir(mode=0o700);audit=a.timeline_audit.resolve();runtime=a.runtime_home.resolve();skill=a.installed_plugin.resolve()/'skills/filmcraft-use'
    task=load(skill/'scripts/task_session.py','scope_task');commands=load(skill/'scripts/commands.py','scope_commands');results=[]
    def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    def op(name,params=None,alias=None):
        r={'command':name,'params':params or {}}
        if alias:r['as']=alias
        return r
    for mode in ['headless','bridge']:
        work=root/mode;source=audit/mode/'fixture/baseline.fcproj';source_hash=sha(source);base=json.loads(source.read_text());queries=[];receipts=[]
        for frame,seconds,tc in [(204,8.5,'00:00:08:12'),(276,11.5,'00:00:11:12')]:
            for kind,value in [('time',frame*FRAME),('frame',frame),('seconds',seconds),('timecode',tc)]:
                queries.append(op('scopes.read',{'scopes':['histogram'],'scale':1,'bins':True,kind:value},kind+'_'+str(frame)))
        policy=commands.load('execution_permissions').from_cli([str(root),str(audit)],[str(root),str(runtime)])
        with task.TaskSession(work,runtime,policy,mode,protected_paths=[audit]) as session:
            def execute(name,operations,inputs=None):
                plan={'schema':'craft-command-plan/v1','operations':operations};write(work/(name+'-plan.private.json'),plan)
                result=session.execute(plan,name,inputs);write(work/(name+'-receipt.private.json'),result);assert result['result']=='PASS',result.get('error');receipts.append(result);return result
            create=execute('create',[op('file.open',{'path':{'$ref':'source.path'}}),op('playhead.set',{'seconds':0})]+queries+[op('file.saveAs',{'path':{'$output':'saved.fcproj'}})],{'source':source})
            saved=work/'create/saved.fcproj';saved_hash=sha(saved)
            reopened=execute('reopen',[op('file.closeAllProjects',{'force':True}),op('file.open',{'path':{'$ref':'source.path'}}),op('playhead.set',{'seconds':0})]+queries+[op('file.saveAs',{'path':{'$output':'reopened.fcproj'}})],{'source':saved})
            for result in [create,reopened]:
                views=[s['result'] for s in result['steps'] if s['command']=='scopes.read'];assert len(views)==8
                for index,frame in enumerate([204,276]):
                    batch=views[index*4:index*4+4]
                    for view in batch:assert_scope(view,frame)
                    assert all(v==batch[0] for v in batch),'time alias views differ'
            for f in [saved,work/'reopen/reopened.fcproj']:
                actual=json.loads(f.read_text());expected=copy.deepcopy(base)
                for v in [actual,expected]:v['project']['name']='Owned scopes';v['project']['root']['name']='Owned scopes'
                assert actual==expected,'scope query changed project'
            assert sha(source)==source_hash and sha(saved)==saved_hash
            execute('close_project',[op('file.closeAllProjects',{'force':True})])
        proof=json.loads((work/'task-session.json').read_text());assert proof['sessionsStarted']==1 and proof['singleProcessIdentity'] and proof['closed'] and proof['ownedProcessesStopped']
        views=[{'phase':phase,'views':[s['result'] for s in result['steps'] if s['command']=='scopes.read']} for phase,result in zip(['create','reopen'],[create,reopened])]
        write(work/'scope-views.json',views);results.append({'mode':mode,'result':'PASS','views':16,'fullHistogramBuckets':16*3*256,'fullProjectComparisons':2,'sourceSha256':source_hash,'runtimeSha256':create['runtimeSha256'],'sessionSha256':sha(work/'task-session.json'),'scopeViewsSha256':sha(work/'scope-views.json'),'receiptsSha256':[sha(work/(name+'-receipt.private.json')) for name in ['create','reopen','close_project']]})
        print(mode,'PASS16 scopes / original PID / complete project',flush=True)
    report={'schema':'filmcraft-fixed-scopes-time-alias/v1','result':'PASS','results':results,'verifierSha256':sha(__file__),'commandsSha256':sha(skill/'scripts/commands.py'),'scope':'Three shorthand aliases and explicit ticks at two actual non-playhead frames, original/reopened project, full RGB histogram buckets. No all-scopes/types/HDR/GUI/full command or V1 qualification.'};write(root/'report.json',report)


if __name__=='__main__':main()
