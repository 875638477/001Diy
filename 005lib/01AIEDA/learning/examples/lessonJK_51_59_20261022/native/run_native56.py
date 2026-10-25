import pathlib,os,sys,json,subprocess,hashlib,datetime,argparse
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022")
C=pathlib.Path(r"C:\Program0\Cadence\SPB172\tools\bin")
P=argparse.ArgumentParser();P.add_argument('--variant',choices=['2L','4L'],required=True);P.add_argument('--action',choices=['params','list','artwork','nctape','ncroute'],required=True);P.add_argument('--tag',required=True);P.add_argument('--board');a=P.parse_args()
assert all(x.isalnum() or x=='_' for x in a.tag)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
config=json.loads((R/'native/source_guard.json').read_text(encoding='utf8'));before={x['path']:sha(pathlib.Path(x['path'])) for x in config['protectedOriginals']};assert all(before[x['path']]==x['sha256'] for x in config['protectedOriginals'])
board=pathlib.Path(a.board) if a.board else R/'native'/a.variant/f'TRAINING_NOT_FOR_FAB_{a.variant}_b019.brd';assert board.resolve().is_relative_to((R/'native').resolve());assert board.is_file()
out=R/'exports'/f'native_{a.variant}_TRAINING_NOT_FOR_FAB';assert out.is_dir();log=R/'logs'/('native_'+a.tag);log.mkdir(parents=True,exist_ok=False);(log/'tmp').mkdir();(log/'pcbenv').mkdir()
env=os.environ.copy();env.update(TEMP=str(log/'tmp'),TMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'));env['PATH']=str(C)+os.pathsep+env.get('PATH','')
(log/'pcbenv/env').write_text('unset autosave\nset autosave_time = 0\nset ads_sdart = .\nset ncdpath = '+out.as_posix()+'\nset artpath = '+out.as_posix()+'\nset artwork_allwarnings\n',encoding='ascii')
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
check=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process -Filter \"Name='allegro.exe' OR Name='artwork.exe' OR Name='nctape.exe' OR Name='ncroute.exe'\" | Select-Object ProcessId,CreationDate,ExecutablePath) | ConvertTo-Json -Compress"],cwd=log,env=env,capture_output=True,text=True,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);assert check.returncode==0,check.stderr;assert not check.stdout.strip(),check.stdout
if a.action=='params':args=[str(C/'allegro.exe'),'-product','Allegro_performance','-safe','-nographic','-s',str(R/'native'/f'native56_params_{a.variant}_try01.scr'),'-p',str(log),str(board)]
elif a.action=='list':args=[str(C/'artwork.exe'),'-l',str(board)]
else:args=[str(C/(a.action+'.exe')),str(board)]
record={'status':'RUNNING_TASK_LOCAL_TRAINING_OUTPUT_ONLY','startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'args':args,'cwd':str(out),'log':str(log),'protectedBefore':before,'scratchInput':str(board),'scratchBeforeSHA256':sha(board),'mode':'No original env/hotkey replay; no original board opened; no DB geometry or DRC-rule changes','processEnvironmentOverrides':{k:env[k] for k in ('TEMP','TMP','ALLEGRO_PCBENV')}}
with (log/'stdout.txt').open('wb') as stdout,(log/'stderr.txt').open('wb') as stderr:
 p=subprocess.Popen(args,cwd=out,env=env,stdout=stdout,stderr=stderr,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);record['pid']=p.pid;(log/'launch_in_progress.json').write_text(json.dumps(record,indent=2),encoding='utf8');print(json.dumps({'pid':p.pid,'action':a.action,'variant':a.variant,'log':str(log)}),flush=True)
 try:rc=p.wait(timeout=180);done=True
 except subprocess.TimeoutExpired:rc=None;done=False
record.update(finishUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),completed=done,exitCode=rc,scratchAfterSHA256=sha(board),protectedAfter={x['path']:sha(pathlib.Path(x['path'])) for x in config['protectedOriginals']});record['protectedAllUnchanged']=before==record['protectedAfter'];(log/'launch.json').write_text(json.dumps(record,indent=2),encoding='utf8');assert record['protectedAllUnchanged'];assert done,'Only owned process may need timeout investigation; do not launch another native tool.'
print(json.dumps({'completed':done,'exitCode':rc,'scratchInputUnchanged':record['scratchBeforeSHA256']==record['scratchAfterSHA256'],'protectedAllUnchanged':record['protectedAllUnchanged']}),flush=True)
for n in ('stdout.txt','stderr.txt'):print(n+':'+(log/n).read_text(encoding='utf8',errors='replace')[-2800:])
assert rc==0
