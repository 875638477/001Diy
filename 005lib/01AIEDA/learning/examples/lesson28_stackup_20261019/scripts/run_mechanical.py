from pathlib import Path
import subprocess,sys,json
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
for tag,board in [('mechbase01',B/'source'/'F27_MECHANICAL.brd'),('mech2_01',B/'native'/'F28_2L.brd'),('mech4_01',B/'native'/'F28_4L.brd')]:
 out=B/'logs'/tag;s=B/'scripts'/(tag+'.scr')
 assert not s.exists()
 s.write_text('set NOCONFIRM\nskill errset(load("'+(B/'scripts'/'mechanical28.il').as_posix()+'") t)\nskill errset(l28Mechanical("'+out.as_posix()+'") t)\nquit\nfillin "yes"\n',encoding='ascii')
 p=subprocess.run([sys.executable,str(B/'scripts'/'launch28.py'),'--mode','readonly','--board',str(board),'--script',str(s),'--log',str(out)],cwd=B,capture_output=True)
 assert p.returncode==0,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace')
 assert '*Error*' not in (out/'stdout.txt').read_text(errors='replace')
 assert 'L28_MECHANICAL_DIRECT COMPLETE' in (out/'mechanical_roots.txt').read_text()
 print(tag,json.loads((out/'launch.json').read_text())['exitCode'])
