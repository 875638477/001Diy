from pathlib import Path
import re,json,hashlib,html
from html.parser import HTMLParser
r=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
class P(HTMLParser):
 def __init__(self):super().__init__();self.o=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
  if t in ('p','div','tr','li','table','h1','h2','h3'):self.o.append('\n')
 def handle_data(self,s):
  if not self.skip:self.o.append(s)
for f in (r/'source').glob('*.html'):
 p=P();p.feed(f.read_text(encoding='utf-8',errors='replace'));txt=re.sub(r'\n\s*\n','\n',''.join(p.o));f.with_suffix('.txt').write_text(txt,encoding='utf-8')
src=Path(r'D:\001DIY\005lib\01AIEDA\learning\scripts\launch_cadence17.py').read_text(encoding='utf-8')
src=src.replace("env=os.environ.copy();env['ALLEGRO_PCBENV']=str(log/'pcbenv');(log/'pcbenv').mkdir(exist_ok=True)", "env=os.environ.copy()\nfor k,d in [('ALLEGRO_PCBENV','pcbenv'),('TMP','runtime_tmp'),('TEMP','runtime_tmp')]:\n    (log/d).mkdir(exist_ok=True);env[k]=str(log/d)")
(r/'scripts'/'launch28.py').write_text(src,encoding='utf-8')
import sys
sys.path.insert(0,r'D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2')
import pymupdf
doc=pymupdf.open(r/'source'/'macrofab_pcb_specifications.pdf')
text='\n'.join(p.get_text() for p in doc)
(r/'source'/'macrofab_pcb_specifications.txt').write_text(text,encoding='utf-8')
print('PDF pages',len(doc));print(text[:15000])
