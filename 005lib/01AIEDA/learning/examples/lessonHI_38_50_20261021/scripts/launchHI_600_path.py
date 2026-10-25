"""Lesson29 official Cadence launcher; all writable process dirs remain in 01AIEDA."""
import argparse,pathlib,subprocess,os,json,datetime,hashlib,shutil
P=argparse.ArgumentParser()
P.add_argument('--new',action='store_true');P.add_argument('--symbol-package',action='store_true');P.add_argument('--board',required=True);P.add_argument('--script',required=True);P.add_argument('--log',required=True);P.add_argument('--readonly',action='store_true')
a=P.parse_args();ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA').resolve()
board=pathlib.Path(a.board).resolve();script=pathlib.Path(a.script).resolve();log=pathlib.Path(a.log).resolve()
assert all(p.is_relative_to(ROOT) for p in [board,script,log])
assert script.is_file(); assert not board.exists() if a.new else board.is_file()
log.mkdir(parents=True,exist_ok=False)
for n in ['tmp','pcbenv']:(log/n).mkdir()
env=os.environ.copy()
env.update(TEMP=str(log/'tmp'),TMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'))
cadence_bin=r'C:\Program0\Cadence\SPB172\tools\bin'
original_path=env.get('PATH','')
bem2d_before=shutil.which('bem2d',path=original_path)
env['PATH']=cadence_bin+os.pathsep+original_path
bem2d_after=shutil.which('bem2d',path=env['PATH'])
(log/'child_environment_resolution.json').write_text(json.dumps({'scope':'Child process environment only; no system/user PATH changed','bem2dBefore':bem2d_before,'bem2dAfter':bem2d_after,'prepended':cadence_bin,'originalPATH':original_path,'childPATH':env['PATH']},indent=2),encoding='utf8')
assert bem2d_after and pathlib.Path(bem2d_after).resolve().is_relative_to(pathlib.Path(cadence_bin).resolve())

sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
before=sha(board) if board.exists() else None
exe=r'C:\Program0\Cadence\SPB172\tools\bin\allegro.exe'
args=[exe,'-product','Allegro_performance','-safe','-nographic']
if a.readonly:args.append('-readonly')
if a.symbol_package:args+=['-symbol','package']
args+=['-s',str(script),'-p',str(log),str(board)]
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
 proc=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
 (log/'launch_in_progress.json').write_text(json.dumps({'startUTC':start,'pid':proc.pid,'args':args,'sourceSHA256':before,'timeoutSeconds':600},indent=2),encoding='utf8')
 print(json.dumps({'startUTC':start,'pid':proc.pid,'timeoutSeconds':600}),flush=True)
 try: code=proc.wait(timeout=600);done=True
 except subprocess.TimeoutExpired:code=None;done=False
record={'startUTC':start,'pid':proc.pid,'args':args,'completed':done,'finishUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeoutSeconds':600,'bem2dBefore':bem2d_before,'bem2dAfter':bem2d_after,'exitCode':code,'beforeSHA256':before,'afterSHA256':sha(board) if board.exists() else None,'readonly':a.readonly,'scriptSHA256':sha(script),'processEnvironmentOverrides':{k:env[k] for k in ['TEMP','TMP','ALLEGRO_PCBENV']}}
(log/'launch.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print(json.dumps(record,indent=2))
for n in ['stdout.txt','stderr.txt']:
 print(n+':\n'+(log/n).read_text(encoding='utf8',errors='replace')[-1500:])
assert done,'Owned process may still run; match recorded PID/start and inspect before stopping.'
assert code==0
if a.readonly: assert record['beforeSHA256']==record['afterSHA256']
