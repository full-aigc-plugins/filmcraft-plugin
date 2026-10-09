#!/usr/bin/env python3
"""FC-SK-003 实际宿主意图路由；原生业务与完整宿主发布资格分别验收。"""
from pathlib import Path
import subprocess,json,queue,threading,time,hashlib,os,sys
import argparse, shlex
parser=argparse.ArgumentParser(description='真实宿主只读技能意图评测；使用现有登录态，不安装工具、不复制凭据、不执行创作。')
parser.add_argument('--codex',required=True)
parser.add_argument('--installed-plugin',type=Path,required=True)
parser.add_argument('--source-repository',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
I=args.installed_plugin.resolve();S=args.source_repository.resolve();R=args.output.resolve()
manifest=json.loads((I/'plugin.json').read_text());source=json.loads((I/'skills.lock.json').read_text())['sources'][0]
assert manifest['name']=='filmcraft' and source['package']=='filmcraft-skills'
R.mkdir(mode=0o700)

corpus_bytes=subprocess.check_output(['git','-C',str(S),'show',source['sha']+':docs/routing-corpus.json']);corpus=json.loads(corpus_bytes);(R/'corpus.json').write_bytes(corpus_bytes)
expect={x.name for x in (I/'skills').iterdir()};q=queue.Queue();seq=0;events=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree():return {str(p.relative_to(I)):sha(p) for p in I.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
before=tree();stderr=(R/'host-stderr.private.txt').open('w');process=subprocess.Popen([args.codex,'app-server','--stdio'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr,text=True,bufsize=1)
def reader():
 for line in process.stdout:
  try:q.put(json.loads(line))
  except json.JSONDecodeError:q.put({'hostProtocolError':True})
 q.put(None)
thread=threading.Thread(target=reader,daemon=True);thread.start()
def send(method,params,id=None):
 msg={'method':method,'params':params}
 if id is not None:msg['id']=id
 process.stdin.write(json.dumps(msg,ensure_ascii=False)+'\n');process.stdin.flush()
def get(deadline):
 remaining=deadline-time.monotonic()
 if remaining<=0:raise TimeoutError('host_timeout')
 msg=q.get(timeout=remaining)
 if msg is None:raise RuntimeError('host_stopped')
 # 服务端请求只有只读评测允许范围，任何审批或外部动态工具请求明确拒绝。
 if 'id' in msg and 'method' in msg:
  process.stdin.write(json.dumps({'id':msg['id'],'error':{'code':-32601,'message':'routing_eval_no_approval_or_external_tools'}})+'\n');process.stdin.flush()
 events.append(msg);return msg
def rpc(method,params):
 global seq
 seq+=1;ident=seq;send(method,params,ident);deadline=time.monotonic()+90
 while True:
  msg=get(deadline)
  if msg.get('id')==ident and 'method' not in msg:
   if 'error' in msg:raise RuntimeError('rpc_failed:'+method+':'+str(msg['error'].get('message','unknown')))
   return msg['result']
results=[];report={'schema':'filmcraft-fixed-host-intent-routing/v1','result':'FAIL','pluginRef':'v'+manifest['version'],'sourceRef':source['ref'],'sourceCommit':source['sha'],'corpusSha256':hashlib.sha256(corpus_bytes).hexdigest(),'cases':results,'scope':'actual authenticated Codex app-server ephemeral read-only route selection using unchanged fixed-installed skill roots; independent native businesses tested separately'}
try:
 init=rpc('initialize',{'clientInfo':{'name':'filmcraft-host-routing-eval','version':'0.1.0'},'capabilities':{'experimentalApi':True}});send('initialized',{});report['hostUserAgent']=init.get('userAgent')
 rpc('skills/extraRoots/set',{'extraRoots':[str(I/'skills')]})
 inventory=rpc('skills/list',{'cwds':[str(R)],'forceReload':True});(R/'inventory.private.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
 found=[x for row in inventory.get('data',[]) for x in row.get('skills',[]) if str(x.get('path','')).startswith(str(I/'skills')+'/')]
 assert {x['name'].split(':')[-1] for x in found}==expect,(len(found),len(expect));assert all(x.get('enabled') for x in found)
 report['fixedInstalledSkillsDiscovered']=len(found)
 for case in corpus['cases']:
  start=len(events)
  session=rpc('thread/start',{'cwd':str(R),'sandbox':'read-only','approvalPolicy':'never','ephemeral':True,'experimentalRawEvents':False,'developerInstructions':'这是 FilmCraft 技能路由验收。只选择当前请求的首选 FilmCraft 技能并读取对应 SKILL.md 确认职责；不得执行创作、编写代码、修改文件、下载、联网检索或委派工作。不得调用外部应用。只进行技能选择评测。'})
  tid=session['thread']['id'];model=session.get('model');report.setdefault('model',model)
  rpc('turn/start',{'threadId':tid,'input':[{'type':'text','text':case['request']}],'outputSchema':{'type':'object','properties':{'skill':{'type':'string','enum':sorted(expect)},'reason':{'type':'string'}},'required':['skill','reason'],'additionalProperties':False}})
  deadline=time.monotonic()+240;final=None;status=None
  while True:
   msg=get(deadline);params=msg.get('params',{})
   if params.get('threadId')!=tid:continue
   if msg.get('method')=='item/completed':
    item=params.get('item',{})
    if item.get('type')=='agentMessage':final=item.get('text')
   if msg.get('method')=='turn/completed':status=params.get('turn',{}).get('status');break
  trace=events[start:];f=R/(case['id']+'.private.json');f.write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n')
  selected=json.loads(final) if final else {};chosen=selected.get('skill');row={'id':case['id'],'expectedSkill':case['expectedSkill'],'selectedSkill':chosen,'rejectedSkills':case['rejectSkills'],'turnStatus':status,'traceSha256':sha(f),'status':'PASS' if status=='completed' and chosen==case['expectedSkill'] and chosen not in case['rejectSkills'] else 'FAIL'};results.append(row)
  # 正确标签不足以证明宿主加载；必须有成功读取所选固定 SKILL.md 的轨迹。
  reads=[x['params']['item'] for x in trace if x.get('method')=='item/completed' and x.get('params',{}).get('item',{}).get('type')=='commandExecution']
  target=I/'skills'/str(chosen)/'SKILL.md'
  observed=False
  for item in reads:
   argv=shlex.split(item.get('command',''))
   if len(argv)==3 and argv[1]=='-lc':
    command=shlex.split(argv[2])
    if command==['cat',str(target)] and item.get('exitCode')==0:observed=True
  row['selectedSkillRead']=observed
  if not observed:row['status']='FAIL'
  print(json.dumps({'case':case['id'],'status':row['status'],'selectedSkill':chosen}),flush=True)
  if status != 'completed':raise RuntimeError('host_turn_failed_before_selection')
  (R/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 assert tree()==before,'installed_files_changed'
 report['installedFilesUnchanged']=True;report['result']='PASS' if len(results)==15 and all(x['status']=='PASS' for x in results) else 'FAIL'
except Exception as error:
 report['errorType']=type(error).__name__;report['error']=str(error);print(json.dumps({'result':'FAIL','errorType':type(error).__name__}),flush=True)
finally:
 process.stdin.close();process.terminate()
 try:process.wait(timeout=10)
 except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
 thread.join(timeout=2);process.stdout.close();stderr.close();report['hostProcessStopped']=process.poll() is not None;(R/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':report['result'],'cases':len(results)}),flush=True)
sys.exit(report['result']!='PASS')
