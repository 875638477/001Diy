import pathlib,os,subprocess,json,hashlib,datetime,sys,shutil
B=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson27_mechanical_20261019')
R=pathlib.Path(r'D:/001DIY/005lib/01AIEDA')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
for d in ['source','library','scripts','logs','runtime','readback']: (B/d).mkdir(parents=True,exist_ok=True)
inputs=[
(R/'learning/examples/de_15_26_20261019/native_flow_final/DE_BASELINE.brd',B/'source/DE_BASELINE.brd'),
(R/'learning/examples/lesson07_completion_20261018/library/eda_l07c_npth_200_null.pad',B/'library/eda_l07c_npth_200_null.pad')]
manifest=[]
for a,b in inputs:
 if not b.exists():shutil.copy2(a,b)
 assert sha(a)==sha(b)
 manifest.append({'source':str(a),'copy':str(b),'SHA256':sha(a)})
(B/'source/input_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
# preserve full original library as read-only external dependency: output stays local
def run(kind,board,scr,tag):
 log=B/'logs'/tag;log.mkdir(parents=True,exist_ok=True)
 assert not (log/'launch.json').exists()
 for p in [board,scr,log]: assert p.resolve().is_relative_to(R.resolve())
 env=os.environ.copy()
 for k,v in [('ALLEGRO_PCBENV',log/'pcbenv'),('TEMP',log/'temp'),('TMP',log/'temp')]:
  pathlib.Path(v).mkdir(exist_ok=True);env[k]=str(v)
 exe=r'C:/Program0/Cadence/SPB172/tools/bin/allegro.exe'
 args=[exe,'-product','Allegro_performance','-safe','-nographic']
 if kind=='package':args+=['-symbol','package']
 if kind=='readonly':args+=['-readonly']
 args+=['-s',str(scr),'-p',str(log),str(board)]
 before=sha(board) if board.exists() else None
 si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
  p=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
  try:code=p.wait(timeout=45);done=True
  except subprocess.TimeoutExpired:code=None;done=False
 rec={'args':args,'startUTC':t,'pid':p.pid,'completed':done,'exitCode':code,'inputBeforeSHA256':before,'inputAfterSHA256':sha(board) if board.exists() else None,'scriptSHA256':sha(scr)}
 (log/'launch.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
 print(json.dumps(rec,indent=2))
 print((log/'stdout.txt').read_text(errors='replace')[-7000:])
 print((log/'stderr.txt').read_text(errors='replace')[-3000:])
 assert done and code==0
 if before:assert sha(board)==before,'Input was changed'
if len(sys.argv)>1:
 mode=sys.argv[1]
 if mode=='package':run('package',B/'library/l27_npth_d200_mech.dra',B/'scripts/package.scr','package03')
 elif mode=='create':run('edit',B/'source/DE_BASELINE.brd',B/'scripts/create.scr',sys.argv[2])
 elif mode=='read':run('readonly',B/'F27_MECHANICAL.brd',B/'scripts/read.scr',sys.argv[2])
