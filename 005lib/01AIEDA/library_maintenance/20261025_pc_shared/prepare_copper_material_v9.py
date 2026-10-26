"""Reject numerically shrinking expands and conservatively guard instead."""
from pathlib import Path
import hashlib,ast
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'pc13_native_changed_rings_v8.il').read_text(encoding='utf-8')
s=s.replace('let((expanded e method residual bb)', 'let((expanded e method residual bb df)')
old='''  residual=pc13RingOp(list(p) expanded 'ANDNOT)
  when(residual error("Cross-net guard lost source added copper\\n"))'''
new=r'''  residual=pc13RingOp(list(p) expanded 'ANDNOT)
  when(residual && equal(method "NATIVE_EXPAND_0D01MIL")
   ; A nonempty numerical expand is not necessarily a containing guard.
   ; Keep the failed containment evidence and use the same STRICT bbox
   ; alternative, whose own original-containment test must still pass.
   pc13CuStep(sprintf(nil "NATIVE_EXPAND_NONCONTAINMENT_FALLBACK %s pieces=%d" key length(residual)))
   df=outfile(strcat(pc13Cu8OutDir "/margin_rejected_expansions.jsonl") "a")
   pc13RingWrite(df key "REJECTED_NATIVE_EXPAND" expanded)
   pc13RingWrite(df key "REJECTED_EXPAND_LOST_INPUT_RESIDUE" residual) close(df)
   method="CONSERVATIVE_BBOX_NATIVE_EXPAND_NONCONTAINMENT_MIN_NATIVE_MARGIN_0D02MIL"
   expanded=pc13CuConservativeBox(p)
   residual=pc13RingOp(list(p) expanded 'ANDNOT))
  when(residual error("Final conservative cross-net guard lost source added copper\n"))'''
assert old in s
s=s.replace(old,new).replace('ENTER_V8_SOURCE','ENTER_V9_SOURCE').replace('ENTER_V8_TARGET','ENTER_V9_TARGET').replace('GUARD_VERSION=8','GUARD_VERSION=9')
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
out=W/'pc13_native_changed_rings_v9.il';assert not out.exists();out.write_text(s,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
r=(W/'review_native_material_ledger13_v7.py').read_text(encoding='utf-8')
r=r.replace("counts.get('GUARD_VERSION')==8", "counts.get('GUARD_VERSION')==9").replace('guard version8','guard version9').replace('guard_validation=dict(version=8,','guard_validation=dict(version=9,').replace('ENTER_V8_SOURCE','ENTER_V9_SOURCE').replace('ENTER_V8_TARGET','ENTER_V9_TARGET')
r=r.replace("'CONSERVATIVE_BBOX_ZERO_AREA_ACCESSOR_MIN_NATIVE_MARGIN_0D02MIL'}", "'CONSERVATIVE_BBOX_ZERO_AREA_ACCESSOR_MIN_NATIVE_MARGIN_0D02MIL','CONSERVATIVE_BBOX_NATIVE_EXPAND_NONCONTAINMENT_MIN_NATIVE_MARGIN_0D02MIL'}")
needle=" a.out.write_text(json.dumps(safe(report),indent=2),encoding='utf-8')"
assert needle in r
r=r.replace(needle," if (n/'margin_rejected_expansions.jsonl').exists():report['rejected_native_expansion_evidence']=dict(path=str(n/'margin_rejected_expansions.jsonl'),sha256=sha(n/'margin_rejected_expansions.jsonl'))\n"+needle)
ast.parse(r)
out=W/'review_native_material_ledger13_v8.py';assert not out.exists();out.write_text(r,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
