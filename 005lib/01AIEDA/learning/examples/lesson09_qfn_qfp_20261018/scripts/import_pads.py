import pathlib,subprocess,os,json,datetime,hashlib
BASE=pathlib.Path(__file__).resolve().parent.parent
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
for pxml in sorted((BASE/'library').glob('*.pxml')):
 out=BASE/'logs'/('pad_'+pxml.stem);out.mkdir(exist_ok=True)
 assert not(out/'launch.json').exists()
 env=os.environ.copy();env['ALLEGRO_PCBENV']=str(out/'pcbenv');(out/'pcbenv').mkdir(exist_ok=True)
 args=[r'C:\Program0\Cadence\SPB172\tools\bin\padstack_editor.exe','-x',str(pxml)]
 with (out/'stdout.txt').open('wb') as so,(out/'stderr.txt').open('wb') as se:
  proc=subprocess.Popen(args,cwd=BASE/'library',env=env,stdout=so,stderr=se,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
  try: code=proc.wait(timeout=15)
  except subprocess.TimeoutExpired: code=None
 rec={'pid':proc.pid,'args':args,'exitCode':code,'inputSHA256':hashlib.sha256(pxml.read_bytes()).hexdigest().upper(),'completed':code is not None}
 (out/'launch.json').write_text(json.dumps(rec,indent=2),encoding='utf-8')
 print(json.dumps(rec))
 if code is None: raise RuntimeError('Owned process remains; inspect PID before next run')
 assert code==0
 assert pxml.with_suffix('.pad').is_file()
 print(pxml.with_suffix('.log').read_text(errors='replace'))
