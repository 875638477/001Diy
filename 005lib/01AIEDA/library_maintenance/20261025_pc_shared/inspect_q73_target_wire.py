from pathlib import Path
import sys
G=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025');sys.path.insert(0,str(G));from sexpr import parse_many
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
for name in ['final_alt13','sot34_full2']:
 print(name)
 for no,line in enumerate((R/'w'/name/'explicit_and_boundary_geometry.tsv').read_text().splitlines(),1):
  f=line.split('\t')
  if f[0]!='"line"' or f[1]!='"ETCH/TOP"':continue
  p=parse_many(f[4])[0]
  if any(2300<x<2400 and 1350<y<1460 for x,y in p):print(no,f[4],f[5])
