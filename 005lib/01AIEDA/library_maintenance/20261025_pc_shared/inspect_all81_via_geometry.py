from pathlib import Path
import collections,json,hashlib
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
paths=[R/'w/sot34_full4/explicit_and_boundary_geometry.tsv',R/'w/all81_full4/explicit_and_boundary_geometry.tsv']
rows=[]
for p in paths:
 c=collections.Counter(line for line in p.read_text().splitlines() if line.startswith('"via"\t'));rows.append(c)
 print(p.parent.name,'count',c.total(),'unique',len(c))
print('removed',list((rows[0]-rows[1]).items())[:10]);print('added',list((rows[1]-rows[0]).items())[:10])
print('exact',rows[0]==rows[1])
