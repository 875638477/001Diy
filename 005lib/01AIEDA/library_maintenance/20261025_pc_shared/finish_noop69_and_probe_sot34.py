"""Offline handoff checks only; no CAD access."""
from pathlib import Path
import csv,json,collections
from decimal import Decimal
M=Path(__file__).parent
p=M/'review_noop_cache69.py';s=p.read_text()
s=s.replace('public_brd0010_noop_cache_review13','public_brd0010_noop_cache_review13_v2')
s=s.replace("re.fullmatch(r'(dbid|pad|propList):[0-9A-Fa-f]+',str(v))", "re.fullmatch(r'(?:dbid|pad|propList):[0-9A-Fa-f]+|_axlPath@0x[0-9A-Fa-f]+',str(v))")
s=s.replace("prefix=k.split(':')[0]", "prefix=k.split(':')[0] if ':' in k else '_axlPath'")
q=M/'review_noop_cache69_v2.py';assert not q.exists();q.write_text(s,encoding='utf-8')
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
d=json.loads((M/'sot34_superset_pst_and_pins_v1/SOT34_102_EXPECTED_CHANGES.json').read_text())
inverse={}
for x in d:
 a=x['after'];b=x['before'];inverse[x['ref'],x['pin'],Decimal(a['expected_x']),Decimal(a['expected_y'])]=Decimal(b['expected_x']),Decimal(b['expected_y'])
def groups(path,inv):
 with path.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
 g=collections.defaultdict(list);changed=0
 for r in rows:
  x=Decimal(r['x']);y=Decimal(r['y']);k=r['refdes'],r['pin'],x,y
  if inv and k in inverse:x,y=inverse[k];changed+=1
  g[r['group']].append((r['refdes'],r['pin'],str(x.normalize()),str(y.normalize()),r['net']))
 return collections.Counter(tuple(sorted(v)) for v in g.values()),len(rows),changed
a,na,_=groups(R/'w/final_alt13/native_copper_pin_groups.tsv',False);b,nb,nc=groups(R/'w/sot34_full2/native_copper_pin_groups.tsv',True)
print(json.dumps(dict(source_pin_rows=na,target_pin_rows=nb,source_groups=sum(a.values()),target_groups=sum(b.values()),sot_changed_centers_inversed=nc,full_group_counter_equal=a==b,removed_groups=sum((a-b).values()),added_groups=sum((b-a).values())),indent=2))
