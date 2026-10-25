from pathlib import Path
import subprocess,sys,json
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
for tag,board in [('morebase01',B/'source'/'F27_MECHANICAL.brd'),('more2_01',B/'native'/'F28_2L.brd'),('more4_01',B/'native'/'F28_4L.brd')]:
 out=B/'logs'/tag;s=B/'scripts'/(tag+'.scr')
 assert not s.exists()
 s.write_text('set NOCONFIRM\nskill errset(load("'+(B/'scripts'/'more28.il').as_posix()+'") t)\nskill errset(l28More("'+out.as_posix()+'") t)\nquit\nfillin "yes"\n',encoding='ascii')
 p=subprocess.run([sys.executable,str(B/'scripts'/'launch28.py'),'--mode','readonly','--board',str(board),'--script',str(s),'--log',str(out)],cwd=B,capture_output=True)
 assert p.returncode==0,p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace')
 assert '*Error*' not in (out/'stdout.txt').read_text(errors='replace')
 assert len((out/'placed_pins.tsv').read_text().splitlines())==23
 print(tag,json.loads((out/'launch.json').read_text())['exitCode'])
