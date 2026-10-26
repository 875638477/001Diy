"""Fix diagnostic sums for empty polygon lists; no boolean/guard changes."""
from pathlib import Path
import hashlib,ast
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'pc13_native_changed_rings_v9.il').read_text(encoding='utf-8')
old="apply('plus cons(0.0 foreach(mapcar p {v} p->area)))"
for v in ('removed','added','oldLocalRemainder'):
 a=old.format(v=v)
 assert a in s,(v,'sum pattern missing')
 s=s.replace(a,"apply('plus cons(0.0 cons(0.0 foreach(mapcar p "+v+" p->area))))")
s=s.replace('ENTER_V9_SOURCE','ENTER_V10_SOURCE').replace('ENTER_V9_TARGET','ENTER_V10_TARGET').replace('GUARD_VERSION=9','GUARD_VERSION=10')
depth=0;string=False;escape=False
for line in s.splitlines():
 for c in line:
  if string:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':string=False
  elif c==';':break
  elif c=='"':string=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1;assert depth>=0,line
assert depth==0 and not string,(depth,string)
out=W/'pc13_native_changed_rings_v10.il';assert not out.exists();out.write_text(s,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
r=(W/'review_native_material_ledger13_v8.py').read_text(encoding='utf-8')
r=r.replace("counts.get('GUARD_VERSION')==9", "counts.get('GUARD_VERSION')==10").replace('guard version9','guard version10').replace('guard_validation=dict(version=9,','guard_validation=dict(version=10,').replace('ENTER_V9_SOURCE','ENTER_V10_SOURCE').replace('ENTER_V9_TARGET','ENTER_V10_TARGET')
ast.parse(r)
out=W/'review_native_material_ledger13_v9.py';assert not out.exists();out.write_text(r,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
