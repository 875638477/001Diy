from pathlib import Path
import sys,json,collections
G=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025');sys.path.insert(0,str(G))
from sexpr import parse_many,Atom
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
def parse(path):
 data={};key=None
 for line in path.read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('BEGIN_PIN '):key=tuple(str(x) for x in parse_many(line[len('BEGIN_PIN '):])[0]);data[key]=[]
  elif key and '\t' in line and not line.startswith('context\t'):
   f=line.split('\t');data[key].append([f[0]]+[parse_many(x)[0] for x in f[1:]])
  elif line.startswith('END_PIN '):key=None
 return data
if __name__=='__main__':
 a=parse(R/'w/sot34_source_adjacency2/SOT34_pin_adjacency.ilist');b=parse(R/'w/sot34_target_adjacency2/SOT34_pin_adjacency.ilist')
 print('source102',len(a),'target102',len(b));print('source_direct',collections.Counter(str(r[2]) for v in a.values() for r in v if r[0]=='DIRECT_NEIGHBOR'));print('target_direct',collections.Counter(str(r[2]) for v in b.values() for r in v if r[0]=='DIRECT_NEIGHBOR'))
 print('Q62.3 SOURCE',a['Q62','3']);print('Q62.3 TARGET',b['Q62','3'])
