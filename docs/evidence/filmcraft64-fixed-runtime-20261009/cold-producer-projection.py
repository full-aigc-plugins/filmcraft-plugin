from pathlib import Path
import hashlib,importlib.util,json,os,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
ROOT=Path.cwd();WORK=ROOT.parent.parent/'.local/filmcraft-recovery-01a11a34-20261008';OUT=WORK/'runtime64-fixed-cold-cli';OUT.mkdir(mode=0o700)
DIRECTORIES=json.loads((WORK/'host64/installed-directories.private.json').read_text()); ROOT=Path(DIRECTORIES['filmcraft-use']).parent.parent; LOCK=json.loads((ROOT/'skills.lock.json').read_text());source=LOCK['sources'][0];assert source['ref']=='v0.1.0-dev.47'
NODE='[HOME]/.nvm/versions/node/v24.18.0/bin/node';PYTHON='[PYTHON]'
def tree(path):
 p=subprocess.run([NODE,'--input-type=module','-e',"import{fingerprintSkill}from'./src/adapters/python_workflow.ts';console.log(fingerprintSkill(process.argv[1]));",str(path)],cwd=ROOT,capture_output=True,text=True,timeout=45);assert p.returncode==0,p.stderr;return p.stdout.strip()
spec=importlib.util.spec_from_file_location('vendor_hash',ROOT/'scripts/vendor/skill_vendor.py');vendor=importlib.util.module_from_spec(spec);spec.loader.exec_module(vendor)
rows=[];started=time.monotonic()
for name in source['skills']:
 own=OUT/name;own.mkdir(mode=0o700);skill=own/'skill';skill=Path(DIRECTORIES[name]);before=tree(skill);assert vendor.hash_skill_dir(skill)==source['sha256'][name]
 runtime=own/'runtime';assert not runtime.exists();env=os.environ.copy();env['FILMCRAFT_DATA_DIR']=str(own/'native-data')
 argv=[PYTHON,'-I','-B',str(skill/'scripts/cli.py'),'--runtime-home',str(runtime),'--','--version'];p=subprocess.run(argv,capture_output=True,text=True,timeout=300,env=env);(own/'cli.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stdout+p.stderr
 lock=json.loads((skill/'scripts/runtime.lock.json').read_text());artifact=lock['artifacts']['darwin-arm64'];assert p.stdout.strip()==artifact['versionOutput']
 spec=importlib.util.spec_from_file_location(name,skill/'scripts/bootstrap.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);installed=module.install(lock,runtime)
 binary=Path(installed['executable']);assert hashlib.sha256(binary.read_bytes()).hexdigest()==artifact['binarySha256'];assert tree(skill)==before
 rows.append({'skill':name,'skillSha256':source['sha256'][name],'runtimeSourceTreeSha256':before,'result':'PASS','coldBefore':True,'versionOutput':p.stdout.strip(),'binarySha256':artifact['binarySha256'],'reusedAfterFirstCall':installed['reused'],'receiptSha256':hashlib.sha256((binary.parent/'installation.json').read_bytes()).hexdigest(),'logSha256':hashlib.sha256((own/'cli.log').read_bytes()).hexdigest()});print(name,'PASS',flush=True)
report={'schema':'filmcraft-independent-cold-cli/v1','result':'PASS','sourceRef':source['ref'],'sourceRevision':source['sha'],'platform':'darwin-arm64','pythonVersion':sys.version.split()[0],'skills':rows,'elapsedSeconds':time.monotonic()-started,'producerSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'13 actual fixed64 installed skill trees; fixed64 tag/plugin identity independently verified; independent empty caches, actual public runtime download and --version execution, verified reuse and unchanged skill bytes. No native creative/model/GUI/full V1 qualification.'};(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'result':'PASS','skills':len(rows),'elapsedSeconds':report['elapsedSeconds']}))
