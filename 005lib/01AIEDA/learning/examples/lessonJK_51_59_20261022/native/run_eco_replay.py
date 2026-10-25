import pathlib,shutil,os,sys,json,hashlib,subprocess,datetime
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');O=R/'eco/DE_REPLAY_ONLY';O.mkdir(exist_ok=False);C=pathlib.Path(r'C:\Program0\Cadence\SPB172\tools\bin');I=R/'eco/source_inputs'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
man=json.loads((R/'eco/replay_input_manifest.json').read_text(encoding='utf8'));files=man['files'];protected={str(p):sha(p) for x in files for p in [pathlib.Path(x['path']),pathlib.Path(x['source'])]};assert all(sha(pathlib.Path(x['path']))==x['sha256']==sha(pathlib.Path(x['source'])) for x in files)
guard=json.loads((R/'native/source_guard.json').read_text());protected.update({x['path']:sha(pathlib.Path(x['path'])) for x in guard['protectedOriginals']})
work=O/'DE_BASELINE_WORKING.brd';shutil.copy2(I/'DE_BASELINE.brd',work);output=O/'DE_ECO_REPLAY.brd';assert not output.exists()
shutil.copy2(R/'source/j55_readback_helpers/2L/00_de_board_read.il',O/'de_board_read.il');shutil.copy2(pathlib.Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS\axlWriteDeviceFile.txt'),O/'axlWriteDeviceFile.txt')
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
runs=[]
def run(tag,args,board=None):
 log=O/'logs'/tag;log.mkdir(parents=True,exist_ok=False);(log/'tmp').mkdir();(log/'pcbenv').mkdir()
 env=os.environ.copy();env.update(TEMP=str(log/'tmp'),TMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'),CDSROOT=str(C.parents[1]));env['PATH']=str(C)+os.pathsep+env.get('PATH','')
 (log/'pcbenv/env').write_text('source $TELENV\nunset autosave\nset autosave_time = 0\nset padpath = '+(I/'library').as_posix()+'\nset psmpath = '+(I/'library').as_posix()+'\n',encoding='ascii')
 check=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process -Filter \"Name='allegro.exe' OR Name='netrev.exe' OR Name='artwork.exe' OR Name='nctape.exe' OR Name='ncroute.exe'\" | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine) | ConvertTo-Json -Compress"],cwd=log,env=env,capture_output=True,text=True,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);assert check.returncode==0
 live=json.loads(check.stdout) if check.stdout.strip() else [];live=[live] if isinstance(live,dict) else live
 for e in live:assert e['CreationDate'] and e['ExecutablePath'].lower()==str(C/'allegro.exe').lower() and str(R).lower() not in e['CommandLine'].lower() and 'lessonhi_38_50_20261021' not in e['CommandLine'].lower() and '-nographic' not in e['CommandLine'].lower(),e
 if board:
  (log/'devices').mkdir()
  for ref in ['C'+str(i) for i in range(1,25)]+['R'+str(i) for i in range(1,33)]+['J'+str(i) for i in range(1,14)]+['U'+str(i) for i in range(1,6)]+['Q1','Q2','D1','F1','L1','Y1']:(log/'devices'/ref).mkdir()
  il='procedure(jkEcoRead()\n let((f)\n deBoardRead("'+log.as_posix()+'")\n f=outfile("'+(log/'component_values_source.tsv').as_posix()+'")\n fprintf(f "refdes\\tinstanceProps\\tdefinitionProps\\tdefinitionAttrs\\n")\n foreach(c axlDBGetDesign()->components\n fprintf(f "%L\\t%L\\t%L\\t%L\\n" c->name axlDBGetProperties(c) axlDBGetProperties(c->compdef) c->compdef->??)\n unless(axlWriteDeviceFile(c->compdef strcat("'+(log/'devices').as_posix()+'/" c->name)) error("Native device definition export failed\\n")))\n fprintf(f "JK_ECO_NATIVE_DEVICE_READ_COMPLETE\\n") close(f) t))\n'
  (log/'read.il').write_text(il,encoding='ascii');(log/'read.scr').write_text('set NOCONFIRM\nskill errset(load("'+(O/'de_board_read.il').as_posix()+'") t)\nskill errset(load("'+(log/'read.il').as_posix()+'") t)\nskill errset(jkEcoRead() t)\nskill axlKillDesign()\nquit\n',encoding='ascii')
  args=[str(C/'allegro.exe'),'-product','Allegro_performance','-safe','-nographic','-readonly','-s',str(log/'read.scr'),'-p',str(log),str(board)]
 record={'tag':tag,'args':args,'startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unownedIndependentGUI':live,'cwd':str(log),'boardBeforeSHA256':sha(board) if board else None}
 with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
  p=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);record['pid']=p.pid;(log/'launch_in_progress.json').write_text(json.dumps(record,indent=2));print(tag,p.pid,flush=True);rc=p.wait(timeout=120)
 record.update(exitCode=rc,finishUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),boardAfterSHA256=sha(board) if board else None,protectedAllUnchanged=all(sha(pathlib.Path(p))==h for p,h in protected.items()))
 (log/'launch.json').write_text(json.dumps(record,indent=2));assert rc==0 and record['protectedAllUnchanged'];assert not board or record['boardBeforeSHA256']==record['boardAfterSHA256'];runs.append(record)
 if board:assert 'JK_ECO_NATIVE_DEVICE_READ_COMPLETE' in (log/'component_values_source.tsv').read_text()
 print(tag,'exit0',flush=True)
run('baseline_readonly',None,work)
run('import_eco',[str(C/'netrev.exe'),'-e','-i',str(I/'eco/netlist'),str(work),str(output)])
assert output.exists() and 'saved to disk' in (O/'logs/import_eco/stdout.txt').read_text(errors='replace').lower()
run('eco_readonly',None,output)
(O/'TRAINING_NOT_FOR_FAB.txt').write_text('ECO_TRAINING_UNPLACED_NOT_HI_NOT_FOR_FAB\nOnly unplaced DE baseline replay. Does not alter routed HI/J55/new-stack/user boards.\n',encoding='ascii')
(O/'native_replay_result.json').write_text(json.dumps({'status':'NATIVE_REPLAY_COMPLETED_FRESH_READBACK_PENDING_INDEPENDENT_DIFF','output':str(output),'outputSHA256':sha(output),'baselineWorkingSHA256':sha(work),'allProtectedOriginalsAndCopiesUnchanged':all(sha(pathlib.Path(p))==h for p,h in protected.items()),'runs':runs},indent=2),encoding='utf8')
print('ECO saved',sha(output),flush=True)
