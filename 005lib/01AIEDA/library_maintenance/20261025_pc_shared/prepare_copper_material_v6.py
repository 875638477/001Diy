"""Handle native zero-area accessor fragments without dropping geometry."""
from pathlib import Path
import hashlib
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'pc13_native_changed_rings_v5.il').read_text(encoding='utf-8')
start=s.index('procedure(pc13CuGuard(')
end=s.index('\nprocedure(pc13AddedCuCrossNet(',start)
s=s[:start]+r'''procedure(pc13CuGuard(p key mf ms)
 let((expanded e method residual bb)
  unless(p && numberp(p->area) && p->area>=0.0 && length(p->vertices)>=3
   error("Added copper requires nonnegative native area and valid vertices\n"))
  bb=p->bBox
  unless(bb && caar(bb)<caadr(bb) && cadar(bb)<cadadr(bb)
   error("Added copper must retain positive native bbox width AND height\n"))
  pc13RingWrite(mf key "ADDED_COPPER_INPUT" list(p)) drain(mf)
  e=axlPolyErrorGet() when(e error("Unconsumed native polygon error before margin %L\n" e))
  if(p->area==0.0 then
   ; The kernel can return a nonnil sub-micro polygon whose area accessor
   ; rounds to zero. Never drop it or infer empty material from that scalar.
   printf("PC13_ZERO_AREA_ACCESSOR_GUARD %s bbox=%L vertices=%d\n" key bb length(p->vertices))
   method="CONSERVATIVE_BBOX_ZERO_AREA_ACCESSOR_MIN_NATIVE_MARGIN_0D02MIL"
   expanded=pc13CuConservativeBox(p)
  else
   expanded=axlPolyExpand(list(p) 0.01 'ACU_BLUNT)
   e=axlPolyErrorGet() when(e error("Cross-net margin expansion error %L\n" e))
   unless(expanded error("Cross-net margin returned bareNIL (not empty placeholder)\n"))
   expanded=remove(nil expanded) method="NATIVE_EXPAND_0D01MIL"
   unless(expanded
    printf("PC13_MARGIN_EMPTY_FALLBACK %s area=%L bbox=%L vertices=%d\n" key p->area bb length(p->vertices))
    method="CONSERVATIVE_BBOX_0D03MIL_MIN_NATIVE_MARGIN_0D02MIL"
    expanded=pc13CuConservativeBox(p)))
  unless(expanded error("Cross-net margin/fallback unexpectedly empty\n"))
  residual=pc13RingOp(list(p) expanded 'ANDNOT)
  when(residual error("Cross-net guard lost source added copper\n"))
  pc13RingWrite(mf key method expanded)
  fprintf(ms "%s\t%s\t%L\t%L\t%d\n" key method p->area bb length(expanded)) drain(ms) drain(mf)
  expanded))
''' + s[end:]
s=s.replace('pc13NativeChangedMaterialCheckedV5(', 'pc13NativeChangedMaterialCheckedV6(').replace('GUARD_VERSION=5','GUARD_VERSION=6')
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
out=W/'pc13_native_changed_rings_v6.il';assert not out.exists()
out.write_text(s,encoding='utf-8')
print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())

r=(W/'review_native_material_ledger13_v4.py').read_text(encoding='utf-8')
r=r.replace("counts.get('GUARD_VERSION')==5", "counts.get('GUARD_VERSION')==6")
r=r.replace('guard version5','guard version6')
r=r.replace("'CONSERVATIVE_BBOX_0D03MIL_MIN_NATIVE_MARGIN_0D02MIL'}", "'CONSERVATIVE_BBOX_0D03MIL_MIN_NATIVE_MARGIN_0D02MIL','CONSERVATIVE_BBOX_ZERO_AREA_ACCESSOR_MIN_NATIVE_MARGIN_0D02MIL'}")
r=r.replace("Decimal(x['input_native_area'])>0", "Decimal(x['input_native_area'])>=0")
r=r.replace('POSITIVE_ADDED_COPPER_INPUT','ADDED_COPPER_INPUT')
r=r.replace("guard_validation=dict(version=5,", "guard_validation=dict(version=6,zero_native_area_accessor_fragments=sum(Decimal(x['input_native_area'])==0 for x in methods),")
needle=" inputs=collections.Counter(x['key'] for x in guard_polys if x['side']=='ADDED_COPPER_INPUT')"
assert needle in r
r=r.replace(needle," assert all((Decimal(x['input_native_area'])==0)==('ZERO_AREA_ACCESSOR' in x['method']) for x in methods),'Zero-area-accessor fragments must use explicit conservative guard'\n"+needle)
import ast
ast.parse(r)
out=W/'review_native_material_ledger13_v5.py';assert not out.exists()
out.write_text(r,encoding='utf-8')
print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
