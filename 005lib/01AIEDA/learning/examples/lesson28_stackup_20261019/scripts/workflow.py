from pathlib import Path
import json,hashlib,subprocess,sys,shutil,os,datetime
B=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019')
R=B.parents[2]
SOURCE=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson27_mechanical_20261019/F27_MECHANICAL.brd')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def launch(mode,board,scr,tag):
 log=B/'logs'/tag
 assert not log.exists()
 args=[sys.executable,str(B/'scripts'/'launch28.py'),'--mode',mode,'--board',str(board),'--script',str(scr),'--log',str(log)]
 p=subprocess.run(args,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 print(p.stdout.decode('utf-8',errors='replace'));print(p.stderr.decode('utf-8',errors='replace'))
 assert p.returncode==0
 text=(log/'stdout.txt').read_text(errors='replace')
 assert '*Error*' not in text
 return log
def script(tag,body):
 p=B/'scripts'/(tag+'.scr')
 assert not p.exists()
 p.write_text('set NOCONFIRM\nskill errset(load("'+str(B/'scripts'/'lesson28.il').replace('\\','/')+'") t)\n'+body+'\nquit\nfillin "yes"\n',encoding='ascii')
 return p
mode=sys.argv[1];tag=sys.argv[2]
if mode=='import':
 log=B/'logs'/tag;log.mkdir()
 env=os.environ.copy()
 for k,d in [('ALLEGRO_PCBENV','pcbenv'),('TMP','temp'),('TEMP','temp')]:
  (log/d).mkdir(exist_ok=True);env[k]=str(log/d)
 exe=r'C:/Program0/Cadence/SPB172/tools/bin/padstack_editor.exe'
 args=[exe,'-x',str(B/'native'/'l28_via030_c060.pxml')]
 si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
 with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
  p=subprocess.Popen(args,cwd=B/'native',env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
  try:code=p.wait(timeout=20);done=True
  except subprocess.TimeoutExpired:code=None;done=False
 rec={'args':args,'pid':p.pid,'startUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':done,'exitCode':code}
 (log/'launch.json').write_text(json.dumps(rec,indent=2),encoding='utf-8')
 print(json.dumps(rec));assert done and code==0
elif mode=='baseline':
 dst=B/'source'/'F27_MECHANICAL.brd'
 assert not dst.exists();shutil.copy2(SOURCE,dst)
 (B/'source'/'input_manifest.json').write_text(json.dumps({'source':str(SOURCE),'copy':str(dst),'SHA256':sha(dst)},indent=2),encoding='utf-8')
 out=B/'logs'/tag
 s=script(tag,'skill errset(l28Read("'+str(out).replace('\\','/')+'") t)')
 launch('readonly',dst,s,tag)
 assert 'L28_READ COMPLETE' in (out/'readback.txt').read_text()
elif mode.startswith('build'):
 n=int(mode[-1]);board=B/'native'/('F28_%dL.brd'%n)
 assert not board.exists();shutil.copy2(B/'source'/'F27_MECHANICAL.brd',board)
 out=B/'logs'/tag
 s=script(tag,'skill errset(l28Build(%d "%s" "%s" "%s") t)'%(n,str(board).replace('\\','/'),str(out).replace('\\','/'),str(B/'native').replace('\\','/')))
 launch('edit',board,s,tag)
 assert 'L28_BUILD COMPLETE' in (out/'build.txt').read_text()
elif mode.startswith('filmfix'):
 n=int(mode[-1]);board=B/'native'/('F28_%dL.brd'%n);out=B/'logs'/tag
 s=script(tag,'skill errset(l28FilmFix(%d "%s" "%s" "%s") t)'%(n,board.as_posix(),out.as_posix(),(B/'native').as_posix()))
 launch('edit',board,s,tag)
 assert 'L28_FILM_FIX COMPLETE' in (out/'fix.txt').read_text()
elif mode.startswith('reopen'):
 n=int(mode[-1]);board=B/'native'/('F28_%dL.brd'%n)
 out=B/'logs'/tag
 s=script(tag,'skill errset(l28Read("'+str(out).replace('\\','/')+'") t)')
 launch('readonly',board,s,tag)
 assert 'L28_READ COMPLETE' in (out/'readback.txt').read_text()
else:raise ValueError(mode)
