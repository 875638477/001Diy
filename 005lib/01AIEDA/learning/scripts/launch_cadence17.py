"""Launch official Cadence CLI in an isolated learning directory; log actual process exit code.
Not a desktop-control helper. Does not edit global HOME, libraries or Cadence installation.
"""
import argparse,subprocess,pathlib,os,json,hashlib,datetime,sys
p=argparse.ArgumentParser()
p.add_argument('--mode',choices=['create','readonly'],required=True)
p.add_argument('--board',required=True);p.add_argument('--script',required=True);p.add_argument('--log',required=True)
a=p.parse_args()
root=pathlib.Path(r'D:\001DIY\005lib\01AIEDA').resolve()
board=pathlib.Path(a.board).resolve();script=pathlib.Path(a.script).resolve();log=pathlib.Path(a.log).resolve()
for v in [board,script,log]:
    assert v.is_relative_to(root),'Outside learning root'
assert script.is_file()
assert board.is_file() if a.mode=='readonly' else not board.exists()
log.mkdir(parents=True,exist_ok=True)
assert not (log/'launch.json').exists(),'Use fresh log directory'
def sha(v):return hashlib.sha256(v.read_bytes()).hexdigest().upper()
before=sha(board) if board.exists() else None
exe=pathlib.Path(r'C:\Program0\Cadence\SPB172\tools\bin\allegro.exe')
args=[str(exe),'-product','Allegro_performance','-safe','-nographic']
if a.mode=='readonly':args+=['-readonly']
args+=['-s',str(script),'-p',str(log),str(board)]
env=os.environ.copy();env['ALLEGRO_PCBENV']=str(log/'pcbenv');(log/'pcbenv').mkdir(exist_ok=True)
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
    proc=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
    try: code=proc.wait(timeout=25);done=True
    except subprocess.TimeoutExpired:code=None;done=False
after=sha(board) if board.exists() else None
record={'startUTC':start,'pid':proc.pid,'args':args,'completed':done,'exitCode':code,'scriptSHA256':sha(script),'beforeSHA256':before,'afterSHA256':after,'readonlyHashUnchanged':before==after if a.mode=='readonly' else None}
(log/'launch.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
for file in ['stdout.txt','stderr.txt']:
    print(file+':\n'+(log/file).read_text(encoding='utf-8',errors='replace')[-4500:])
if not done:raise RuntimeError('Owned Cadence process still running; inspect recorded PID and start time.')
assert code==0,'Cadence returned nonzero; inspect logs and saved artifacts before continuing.'
if a.mode=='readonly':assert before==after,'Readonly file hash changed'

