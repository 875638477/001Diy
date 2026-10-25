from pathlib import Path
import json,os,subprocess,datetime,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_completion_20261018')
L=R/'logs/import_null';L.mkdir()
env=os.environ.copy();env['ALLEGRO_PCBENV']=str(L/'pcbenv');(L/'pcbenv').mkdir()
args=[r'C:\Program0\Cadence\SPB172\tools\bin\padstack_editor.exe','-x',str(R/'library/eda_l07c_npth_200_null.pxml')]
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
with (L/'stdout.txt').open('wb') as o,(L/'stderr.txt').open('wb') as e:
 p=subprocess.Popen(args,cwd=R/'library',env=env,stdout=o,stderr=e,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
 record={'startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':p.pid,'args':args}
 try:record.update(exitCode=p.wait(timeout=15),completed=True,terminated=False)
 except subprocess.TimeoutExpired:
  record.update(completed=False,terminated=True,reason='Warning dialog blocks official -x after PAD saved. Only this owned import process terminated. Checks retained.')
  p.terminate();record['exitCode']=p.wait(timeout=10)
(L/'launch.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
print((R/'library/eda_l07c_npth_200_null.log').read_text(errors='replace'))
