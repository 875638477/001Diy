from pathlib import Path
import sys,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many
D=R/'w/all81_sourcecu8'
src=parse_many((D/'SOURCE_ALL4541_VIAS_TYPED.ilist').read_text());dst=parse_many((D/'TARGET_ALL4541_VIAS_TYPED.ilist').read_text())
key=lambda r:(str(r[0]),str(r[1]),str(r[3]))
a={key(r):r for r in src};b={key(r):r for r in dst};assert len(a)==len(b)==4541 and a.keys()==b.keys()
for k in a:
 if a[k]!=b[k]:print('SOURCE',a[k]);print('TARGET',b[k])
