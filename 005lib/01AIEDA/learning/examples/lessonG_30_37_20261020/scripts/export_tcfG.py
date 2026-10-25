import pathlib,subprocess,hashlib,os,json,datetime
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
E=R/'exports';E.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
allrecords={}
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
for key in ['4L','2L']:
 board=R/f'current/G_{key}_LAYOUT_v1.brd';out=E/f'G_{key}_RULES_v1.tcf'
 log=E/f'techfile_{key}';log.mkdir(exist_ok=False)
 for n in ['tmp','pcbenv']:(log/n).mkdir()
 env=os.environ.copy();env.update(TMP=str(log/'tmp'),TEMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'))
 exe=r'C:\Program0\Cadence\SPB172\tools\bin\techfile.exe'
 before=sha(board);records=[]
 for step,args in [('export',[exe,'-w',str(board),str(out)]),('compare',[exe,'-c',str(out),str(board)])]:
  with (log/f'{step}_stdout.txt').open('wb') as stdout,(log/f'{step}_stderr.txt').open('wb') as stderr:
   start=datetime.datetime.now(datetime.timezone.utc).isoformat()
   p=subprocess.Popen(args,cwd=log,env=env,stdout=stdout,stderr=stderr,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);code=p.wait(timeout=120)
  rec={'step':step,'startUTC':start,'pid':p.pid,'args':args,'exitCode':code,'boardBefore':before,'boardAfter':sha(board)}
  records.append(rec)
  if (log/'techfile.log').exists():(log/f'{step}_techfile.log').write_bytes((log/'techfile.log').read_bytes())
  assert code==0 and sha(board)==before,rec
 allrecords[key]={'records':records,'output':str(out),'outputSHA256':sha(out)}
(E/'export_result.json').write_text(json.dumps({'status':'PASS_OFFICIAL_TECHFILE_EXPORT_COMPARE','boards':allrecords,'scope':'Technology/CSet export and compare; native readback supplies net/class/region mappings. Not a full DCF export.'},indent=2),encoding='utf8')
print(json.dumps(allrecords,indent=2))
