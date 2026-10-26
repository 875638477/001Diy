from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from inspect_sot34_neighbors import parse
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
for name in ('all50_alt3','all81_full4'):
 data=parse(R/'w'/name/'ALL81_pin_adjacency.ilist')
 print(name)
 for k,rows in data.items():
  if k[0]=='U5' and k[1]=='9':
   print(k)
   for row in rows:print(row)
