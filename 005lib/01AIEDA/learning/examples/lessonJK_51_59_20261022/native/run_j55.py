import pathlib,os,sys,json,subprocess,hashlib,datetime,argparse,shutil
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');HI=R.parent/'lessonHI_38_50_20261021';C=pathlib.Path(r'C:\Program0\Cadence\SPB172\tools\bin')
P=argparse.ArgumentParser();P.add_argument('--variant',choices=['2L','4L'],required=True);P.add_argument('--mode',choices=['build','reopen'],required=True);P.add_argument('--tag',required=True);a=P.parse_args();assert all(x.isalnum() or x=='_' for x in a.tag)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
config=json.loads((R/'native/source_guard.json').read_text(encoding='utf8'));before={x['path']:sha(pathlib.Path(x['path'])) for x in config['protectedOriginals']};assert all(before[x['path']]==x['sha256'] for x in config['protectedOriginals'])
log=R/'logs'/('native_'+a.tag);log.mkdir(parents=True,exist_ok=False);(log/'tmp').mkdir();(log/'pcbenv').mkdir();(log/'sources').mkdir()
output=R/'native'/a.variant/f'JK_{a.variant}_J55_text_height_review_NOT_RELEASED.brd'
if a.mode=='build':
 assert not output.exists(),output
 board=R/'native'/a.variant/(a.tag+'_WORKING_COPY.brd');assert not board.exists();shutil.copy2(R/'native'/a.variant/f'TRAINING_NOT_FOR_FAB_{a.variant}_b019.brd',board)
else:board=output;assert board.exists()
boardbefore=sha(board)
src=HI/'source/readback_snapshots'/f'reopen_padentry_{a.variant}_b019_stored'/f'16_reopen_padentry_{a.variant}_b019_stored.il'
s=src.read_text(encoding='utf-8-sig').replace((HI/'logs'/f'reopen_padentry_{a.variant}_b019_stored').as_posix(),log.as_posix())
assert s!=src.read_text(encoding='utf-8-sig');(log/'sources/endpoint_proofs.il').write_text(s,encoding='utf8')
loads=sorted((R/'source/j55_readback_helpers'/a.variant).glob('*.il'))+[log/'sources/endpoint_proofs.il',R/'native/native56_probe.il',R/'native/j55_plan_static.il',R/'native/j55_apply_core_v2.il',R/'native/j55_outer.il']
script='set NOCONFIRM\n'+''.join('skill errset(load("'+p.as_posix()+'") t)\n' for p in loads)
if a.mode=='build':script+='skill errset(jk55Run("'+a.variant+'" "'+log.as_posix()+'" "'+output.as_posix()+'") t)\n'
else:script+='skill errset(progn(hiStoredReadback() jk55ReadAll("'+log.as_posix()+'") jk56Probe("'+(log/'probe.tsv').as_posix()+'")) t)\n'
script+='skill axlKillDesign()\nquit\n';(log/'run.scr').write_text(script,encoding='ascii')
env=os.environ.copy();env.update(TEMP=str(log/'tmp'),TMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'),CDSROOT=str(C.parents[1]));env['PATH']=str(C)+os.pathsep+env.get('PATH','')
(log/'pcbenv/env').write_text('source $TELENV\nunset autosave\nset autosave_time = 0\n',encoding='ascii')
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
check=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process -Filter \"Name='allegro.exe' OR Name='artwork.exe' OR Name='nctape.exe' OR Name='ncroute.exe' OR Name='netrev.exe'\" | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine) | ConvertTo-Json -Compress"],cwd=log,env=env,capture_output=True,text=True,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);assert check.returncode==0,check.stderr;live=json.loads(check.stdout) if check.stdout.strip() else []
if isinstance(live,dict):live=[live]
for entry in live:
 assert entry['CreationDate'] and entry['ExecutablePath'].lower()==str(C/'allegro.exe').lower(),entry
 assert str(R).lower() not in entry['CommandLine'].lower() and str(HI).lower() not in entry['CommandLine'].lower() and '-nographic' not in entry['CommandLine'].lower(),entry
 # Root authorizes independent unrelated user GUI coexistence. Never send input/kill/read its board.
args=[str(C/'allegro.exe'),'-product','Allegro_performance','-safe','-nographic','-s',str(log/'run.scr'),'-p',str(log)]+(['-readonly'] if a.mode=='reopen' else [])+[str(board)]
rec={'status':'RUNNING','startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':a.mode,'args':args,'sourceGuard':before,'board':str(board),'boardBeforeSHA':boardbefore,'newOutput':str(output),'unownedUserGUIExcluded':live,'loadedFiles':[{'path':str(p),'sha256':sha(p)} for p in loads]}
with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
 p=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);rec['pid']=p.pid;(log/'launch_in_progress.json').write_text(json.dumps(rec,indent=2),encoding='utf8');print(json.dumps({'pid':p.pid,'log':str(log),'mode':a.mode,'variant':a.variant}),flush=True)
 try:rc=p.wait(timeout=180)
 except subprocess.TimeoutExpired:rc=None
rec.update(status='FINISHED' if rc is not None else 'TIMEOUT_OWNED_PROCESS_INVESTIGATION_REQUIRED',exitCode=rc,finishUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),protectedAfter={x['path']:sha(pathlib.Path(x['path'])) for x in config['protectedOriginals']},boardAfterSHA=sha(board),newOutputSHA=sha(output) if output.exists() else None)
rec['protectedAllUnchanged']=rec['sourceGuard']==rec['protectedAfter'];rec['inputUnchanged']=boardbefore==rec['boardAfterSHA'];(log/'launch.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
print(json.dumps({k:rec[k] for k in ['status','exitCode','protectedAllUnchanged','inputUnchanged','newOutputSHA']}),flush=True)
for n in ['stdout.txt','stderr.txt']:print(n+':'+(log/n).read_text(encoding='utf8',errors='replace')[-4500:])
assert rc==0 and rec['protectedAllUnchanged'] and rec['inputUnchanged']
if a.mode=='build':assert output.exists(),'Core failed and output was correctly not saved: inspect logs'
else:assert (log/'hi_reopen_endpoint_proofs.txt').exists() and 'HI_REOPEN_ALL_ENDPOINTS_COMPLETE' in (log/'hi_reopen_endpoint_proofs.txt').read_text()
