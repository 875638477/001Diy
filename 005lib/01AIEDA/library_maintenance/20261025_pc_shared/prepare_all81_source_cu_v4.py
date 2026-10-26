"""Restore the two exact source via nets with source-via-Cu-contained anchors.
API axlChangeNet is advisory; original via copper anchors supply the physical
same-net shape required by the official17.2 API. No new physical copper area.
"""
from pathlib import Path
import hashlib,shutil
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');W=R/'w/pcb_migration';old=W/'all81_source_cu_v3';D=W/'all81_source_cu_v5'
assert not D.exists();D.mkdir()
for n in ('SOURCE_FROZEN_REAL_SEGMENTS.ilist','SOURCE_SYMBOL_ETCH_SHAPE_PINS7.ilist'):shutil.copy2(old/n,D/n)
s=(old/'all81_restore_actual_source_cu_v3.il').read_text().replace('/all81_source_cu_v3/','/all81_source_cu_v5/')
extra='''; Exactly two source via nets were changed to nativeNIL by the ECO.
; Full4541 XY/pad/properties are independently exact. No other delta is allowed.
procedure(pc13FrozenViaObjects()
 let((rows found o) rows='(((1496.59 -220.0) "VIA_18D10" "PWR_BTN#" nil) ((1521.59 1385.0) "VIA_18D10" "PWR_BTN#" nil)) found=nil
  foreach(item rows
   o=car(setof(row pc13CuIndexRows equal(nth(4 row) "via") && equal(car(row)->xy car(item)) && equal(car(row)->name cadr(item))))
   unless(o && equal(pc13Props(car(o)) nth(3 item)) error("Frozen source-via physical/props identity missing\\n"))
   found=cons(list(car(o) item) found)) reverse(found)))
procedure(pc13PrepareViaSourceAnchors(dir)
 let((f o item ps box x y0 x1 y1 path rect anchor copy)
  pc13FrozenViaAnchors=nil f=outfile(strcat(dir "/SOURCE_VIA_ANCHORS.jsonl"))
  foreach(pair pc13FrozenViaObjects()
   o=car(pair) item=cadr(pair)
   unless(equal(o->net->name nth(2 item)) error("Frozen original via source net missing\\n"))
   ps=axlPolyFromDB(o ?layer "ETCH/TOP" ?padType 'REGULAR ?holes t) when(axlPolyErrorGet() error("Source via actual Cu conversion failed\\n")) ps=remove(nil ps)
   unless(ps error("Source via top copper missing\\n"))
   box=o->bBox x=xCoord(o->xy) y0=cadar(box) x1=caadr(box) y1=cadadr(box)
   ; This box SELECTS a half-annulus from actual source Cu. It never admits Cu.
   path=axlPathStart(list(x:y0 x1:y0 x1:y1 x:y1 x:y0) 0.0)
   rect=axlPolyFromDB(path) when(axlPolyErrorGet() error("Source via clip conversion failed\\n")) rect=remove(nil rect)
   anchor=pc13RingOp(ps rect 'AND)
   unless(anchor error("Source via half-annulus empty\\n"))
   foreach(poly anchor unless(poly->area>0 && null(poly->holes) error("Source via anchor not a positive simply connected sourceCu sector\\n")))
   when(pc13RingOp(anchor ps 'ANDNOT) error("Source via anchor extends actual source Cu\\n"))
   copy=axlPolyOffset(anchor '(0.0 0.0) t) when(axlPolyErrorGet() error("Source via anchor clone failed\\n")) copy=remove(nil copy)
   unless(copy && null(pc13RingOp(copy anchor 'ANDNOT)) && null(pc13RingOp(anchor copy 'ANDNOT)) error("Source via anchor detached clone differs\\n"))
   originalViaCu=ps ps=axlPolyOffset(ps '(0.0 0.0) t) when(axlPolyErrorGet() error("Full source via Cu clone failed\\n")) ps=remove(nil ps)
   unless(ps && null(pc13RingOp(ps originalViaCu 'ANDNOT)) && null(pc13RingOp(originalViaCu ps 'ANDNOT)) error("Full source via Cu clone differs\\n"))
   pc13FrozenViaAnchors=cons(list(item ps copy) pc13FrozenViaAnchors)
   pc13RingWrite(f sprintf(nil "%L" car(item)) "ACTUAL_SOURCE_VIA_TOP_CU_SUBSET" copy))
  close(f) pc13FrozenViaAnchors=reverse(pc13FrozenViaAnchors) t))
procedure(pc13RestoreExactViaNets(dir)
 let((f o item original anchors actual result created rows allowed row repaired)
  unless(length(pc13FrozenViaAnchors)==2 error("Source exact-via anchors unavailable\\n"))
  rows=pc13ViaAllSnapshot(strcat(dir "/TARGET_ALL4541_VIAS_BEFORE_REPAIR.ilist"))
  allowed=nil
  foreach(record pc13FrozenSourceViaRecords
   row=car(linereadstring(record))
   when(member(car(row) '((1496.59 -220.0) (1521.59 1385.0)))
    allowed=cons(sprintf(nil "%L" list(car(row) cadr(row) nil nth(3 row))) allowed)))
  ; All target records must equal source, except these exact2 may be source-net or NIL.
  foreach(record rows unless(member(record pc13FrozenSourceViaRecords) || member(record allowed) error("Unexpected via delta beyond frozen two source-net corrections %s\\n" record)))
  f=outfile(strcat(dir "/VIA_SOURCE_NET_REPAIR.tsv")) repaired=0
  foreach(pair pc13FrozenViaObjects()
   o=car(pair) item=cadr(pair)
   unless(equal(o->net->name nth(2 item))
    unless(null(o->net->name) error("Frozen via acquired unexpected third net\\n"))
    original=car(setof(a pc13FrozenViaAnchors equal(car(a) item))) anchors=nth(2 original)
    actual=axlPolyFromDB(o ?layer "ETCH/TOP" ?padType 'REGULAR ?holes t) when(axlPolyErrorGet() error("Target via actualCu conversion failed\\n")) actual=remove(nil actual)
    when(pc13RingOp(actual nth(1 original) 'ANDNOT) || pc13RingOp(nth(1 original) actual 'ANDNOT) error("Target via physical Cu differs from exact original\\n"))
    when(pc13RingOp(anchors actual 'ANDNOT) error("Original via anchor would add new physical Cu\\n"))
    foreach(poly anchors
     result=axlDBCreateShape(poly t "ETCH/TOP" nth(2 item) nil) unless(result error("Source via anchor creation failed\\n"))
     created=car(result) axlDBRefreshId(created)
     actual=axlPolyFromDB(created ?holes t) when(axlPolyErrorGet() error("Created via anchor conversion failed\\n")) actual=remove(nil actual)
     when(pc13RingOp(actual list(poly) 'ANDNOT) || pc13RingOp(list(poly) actual 'ANDNOT) error("Via anchor differs from exact sourceCu subset\\n")))
    axlDBRefreshId(o)
    unless(equal(o->net->name nth(2 item)) unless(axlChangeNet(o nth(2 item)) error("Official axlChangeNet original via assignment failed\\n")))
    axlDBRefreshId(o) unless(equal(o->net->name nth(2 item)) error("Original via net did not remain source net after exact sourceCu anchor\\n"))
    repaired=repaired+1 fprintf(f "%L\\t%s\\tSOURCE_PWR_BTN#_RESTORED\\tANCHOR_PHYSICAL_ADDED_CU_ZERO\\n" o->xy o->name) drain(f)))
  close(f) axlDBRefreshId(nil) pc13BuildCuIndex("AFTER_SOURCE_VIA_NET_REPAIR")
  unless(equal(pc13FrozenSourceViaRecords pc13ViaAllSnapshot(strcat(dir "/TARGET_ALL4541_VIAS_TYPED.ilist"))) error("Full4541 source via identity/net/properties not restored\\n")) repaired))
'''
# linereadstring is not a supported API; use readstring for a single native list.
extra=extra.replace('car(linereadstring(record))','car(parseString(record "\\n"))') if False else extra
# SKILL lineread accepts a string source via linereadstring? Avoid parsing entirely:
start=extra.index('  allowed=nil\n  foreach(record pc13FrozenSourceViaRecords')
end=extra.index('  ; All target records',start)
extra=extra[:start]+'''  allowed='("((1496.59 -220.0) \\"VIA_18D10\\" nil nil)" "((1521.59 1385.0) \\"VIA_18D10\\" nil nil)")
'''+extra[end:]
s=s.replace('procedure(pc13SourceCuKey(',extra+'procedure(pc13SourceCuKey(',1)
s=s.replace('pc13FrozenSourceViaRecords=pc13ViaAllSnapshot(strcat(dir "/SOURCE_ALL4541_VIAS_TYPED.ilist")) close(pc13CuStepPort)','pc13FrozenSourceViaRecords=pc13ViaAllSnapshot(strcat(dir "/SOURCE_ALL4541_VIAS_TYPED.ilist"))\n  pc13PrepareViaSourceAnchors(dir) close(pc13CuStepPort)')
oldcheck='unless(equal(pc13FrozenSourceViaRecords pc13ViaAllSnapshot(strcat(dir "/TARGET_ALL4541_VIAS_TYPED.ilist"))) close(pc13CuStepPort) error("Original4541 via XY/pad/net/properties changed; no Cu write allowed\\n"))'
assert oldcheck in s;s=s.replace(oldcheck,'pc13RestoreExactViaNets(dir)')
depth=0;quoted=False;esc=False
for line in s.splitlines():
 for c in line:
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c==';':break
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0,line
assert depth==0 and not quoted
p=D/'all81_restore_actual_source_cu_v5.il';p.write_text(s,encoding='utf-8')
print(p);print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
