"""Lesson29 official Cadence launcher; all writable process dirs remain in 01AIEDA."""
import argparse,pathlib,subprocess,os,json,datetime,hashlib
P=argparse.ArgumentParser()
P.add_argument('--board',required=True);P.add_argument('--script',required=True);P.add_argument('--log',required=True);P.add_argument('--readonly',action='store_true')
a=P.parse_args();ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA').resolve()
board=pathlib.Path(a.board).resolve();script=pathlib.Path(a.script).resolve();log=pathlib.Path(a.log).resolve()
assert all(p.is_relative_to(ROOT) for p in [board,script,log])
assert board.is_file() and script.is_file()
log.mkdir(parents=True,exist_ok=False)
for n in ['tmp','pcbenv']:(log/n).mkdir()
env=os.environ.copy()
env.update(TEMP=str(log/'tmp'),TMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
before=sha(board)
exe=r'C:\Program0\Cadence\SPB172\tools\bin\allegro.exe'
args=[exe,'-product','Allegro_performance','-safe','-nographic']
if a.readonly:args.append('-readonly')
args+=['-s',str(script),'-p',str(log),str(board)]
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
 proc=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
 try: code=proc.wait(timeout=55);done=True
 except subprocess.TimeoutExpired:code=None;done=False
record={'startUTC':start,'pid':proc.pid,'args':args,'completed':done,'exitCode':code,'beforeSHA256':before,'afterSHA256':sha(board),'readonly':a.readonly,'scriptSHA256':sha(script),'processEnvironmentOverrides':{k:env[k] for k in ['TEMP','TMP','ALLEGRO_PCBENV']}}
(log/'launch.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print(json.dumps(record,indent=2))
for n in ['stdout.txt','stderr.txt']:
 print(n+':\n'+(log/n).read_text(encoding='utf8',errors='replace')[-7000:])
assert done,'Owned process may still run; match recorded PID/start and inspect before stopping.'
assert code==0
if a.readonly: assert record['beforeSHA256']==record['afterSHA256']
