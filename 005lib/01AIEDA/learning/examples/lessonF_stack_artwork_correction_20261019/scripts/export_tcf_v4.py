import pathlib,subprocess,hashlib,os,json,datetime
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
board=R/'current/F29_CONSTRAINTS_v4.brd'
out=R/'exports/F29_RULES_v4.tcf'
log=R/'exports/techfile_run';log.mkdir(exist_ok=False);(log/'tmp').mkdir()
env=os.environ.copy();env['TMP']=str(log/'tmp');env['TEMP']=str(log/'tmp');env['ALLEGRO_PCBENV']=str(log/'pcbenv');(log/'pcbenv').mkdir()
exe=r'C:\Program0\Cadence\SPB172\tools\bin\techfile.exe'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
before=sha(board)
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
records=[]
for step,args in [('export',[exe,'-w',str(board),str(out)]),('compare',[exe,'-c',str(out),str(board)])]:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (log/f'{step}_stdout.txt').open('wb') as stdout,(log/f'{step}_stderr.txt').open('wb') as stderr:
  p=subprocess.Popen(args,cwd=log,env=env,stdout=stdout,stderr=stderr,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
  code=p.wait(timeout=120)
 rec={'step':step,'startUTC':t,'pid':p.pid,'args':args,'exitCode':code,'boardBefore':before,'boardAfter':sha(board)}
 records.append(rec)
 if (log/'techfile.log').exists(): (log/f'{step}_techfile.log').write_bytes((log/'techfile.log').read_bytes())
 assert code==0,rec
 assert sha(board)==before,rec
rec={'records':records,'output':str(out),'outputExists':out.exists(),'outputSHA256':sha(out) if out.exists() else None,'scope':'Official techfile export of design technology/csets. Not a full net/object DCF export; native readback supplies mappings.'}
(R/'exports/export_result.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
print(json.dumps(rec,indent=2))
