"""Add durable phases and one-pass actual-copper indexes. Never launches CAD."""
from pathlib import Path
import hashlib,ast
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'pc13_native_changed_rings_v6.il').read_text(encoding='utf-8')
start=s.index('procedure(pc13CuVisit(')
end=s.index(' ; Read-only fallback:',start)
s=s[:start]+r'''procedure(pc13CuStep(message)
 unless(pc13CuStepPort error("PersistentSTEP port unavailable\n"))
 fprintf(pc13CuStepPort "%s\n" message) drain(pc13CuStepPort))
procedure(pc13CuIndexWalk(o)
 let((kind attrs)
  when(o && !pc13CuIndexSeen[o]
   pc13CuIndexSeen[o]=t kind=o->objType
   if(member(kind '("pin" "via" "path" "cline" "shape")) then
    ; Whole paths already include their line/arc segments. Branches contain
    ; vias separately; do not repeatedly descend every route segment.
    unless(o->isHole
     when(member(kind '("pin" "via")) || member(o->layer '("ETCH/TOP" "ETCH/L2" "ETCH/L3" "ETCH/BOTTOM"))
      unless(o->bBox error("Actual copper object missing bbox %L %L\n" kind o))
      pc13CuIndexRows=cons(list(o o->net->name o->layer o->bBox kind) pc13CuIndexRows)
      pc13CuIndexCounts[kind]=1+pc13CuIndexCounts[kind]))
   else
    ; Official ashshowelement.il uses dbid->? to enumerate valid attributes.
    ; Only traverse supported container properties, once per board.
    attrs=o->?
    when(member('children attrs) foreach(child o->children pc13CuIndexWalk(child)))
    when(member('segments attrs) foreach(child o->segments pc13CuIndexWalk(child)))))))
procedure(pc13BuildCuIndex(side)
 let((f)
  pc13CuIndexSeen=makeTable('pc13CuIndexSeen nil)
  pc13CuIndexRows=nil pc13CuIndexCounts=makeTable('pc13CuIndexCounts 0)
  pc13CuPolyCache=makeTable('pc13CuPolyCache nil) pc13CuPolyCached=makeTable('pc13CuPolyCached nil)
  pc13CuStep(strcat(side "_INDEX_BEGIN_PINS"))
  foreach(c axlDBGetDesign()->components foreach(p c->symbol->pins pc13CuIndexWalk(p)))
  pc13CuStep(strcat(side "_INDEX_BEGIN_SHAPES"))
  foreach(s axlDBGetShapes(nil) when(member(s->layer '("ETCH/TOP" "ETCH/L2" "ETCH/L3" "ETCH/BOTTOM")) pc13CuIndexWalk(s)))
  pc13CuStep(strcat(side "_INDEX_BEGIN_BRANCHES"))
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13CuIndexWalk(b)))
  pc13CuIndexRows=reverse(pc13CuIndexRows)
  pc13CuStep(sprintf(nil "%s_INDEX_COMPLETE objects=%d pins=%d vias=%d paths=%d clines=%d shapes=%d" side length(pc13CuIndexRows) pc13CuIndexCounts["pin"] pc13CuIndexCounts["via"] pc13CuIndexCounts["path"] pc13CuIndexCounts["cline"] pc13CuIndexCounts["shape"]))
  unless(pc13CuIndexCounts["pin"]==6521 && pc13CuIndexCounts["via"]==4541 && pc13CuIndexCounts["path"]>0 error("Actual-copper index completeness guard failed\n"))
  t))
procedure(pc13IndexedCuPolys(row layer)
 let((o kind key ps e)
  o=car(row) kind=nth(4 row) key=strcat(sprintf(nil "%L" o) "|" layer)
  unless(pc13CuPolyCached[key]
   ps=if(member(kind '("pin" "via")) then axlPolyFromDB(o ?layer layer ?padType 'REGULAR ?holes t) else axlPolyFromDB(o ?holes t ?endCapType 'ROUND))
   e=axlPolyErrorGet() when(e error("Indexed actual-copper conversion error %L %L\n" o e))
   ps=remove(nil ps)
   when(ps
    ps=axlPolyOffset(ps '(0.0 0.0) t)
    e=axlPolyErrorGet() when(e error("Indexed actual-copper clone error %L %L\n" o e))
    unless(ps error("Actual-copper clone returned bareNIL\n"))
    ps=remove(nil ps))
   pc13CuPolyCache[key]=ps pc13CuPolyCached[key]=t)
  pc13CuPolyCache[key]))
procedure(pc13NearbyIndexedCopper(netName layer box other)
 let((polys kind)
  polys=nil
  foreach(row pc13CuIndexRows
   kind=nth(4 row)
   when(if(other then !equal(nth(1 row) netName) else equal(nth(1 row) netName)) && (member(kind '("pin" "via")) || equal(nth(2 row) layer)) && pc13BoxesMeet(nth(3 row) box)
    polys=append(polys pc13IndexedCuPolys(row layer))))
  polys))
procedure(pc13NearbySameNetCopper(netName layer box) pc13NearbyIndexedCopper(netName layer box nil))
procedure(pc13NearbyOtherNetCopper(netName layer box) pc13NearbyIndexedCopper(netName layer box t))
''' + s[end:]
s=s.replace('pc13NativeChangedMaterialCheckedV6(', 'pc13NativeChangedMaterialCheckedV7(').replace('GUARD_VERSION=6','GUARD_VERSION=7')
s=s.replace('crosshits marginf margins)', 'crosshits marginf margins pc13CuStepPort pc13CuIndexSeen pc13CuIndexRows pc13CuIndexCounts pc13CuPolyCache pc13CuPolyCached)')
s=s.replace('  sstatus(fullPrecision t)\n  f=infile(planPath) rows=nil', '  pc13CuStepPort=outfile(strcat(outDir "/STEP.txt")) pc13CuStep("ENTER_V7")\n  sstatus(fullPrecision t)\n  f=infile(planPath) rows=nil')
s=s.replace('  before=pc13RingCollect(rows "SOURCE") oldPad=pc13PC184Pad()\n  oldHole=', '  pc13CuStep("SOURCE_COLLECT_BEGIN")\n  before=pc13RingCollect(rows "SOURCE") oldPad=pc13PC184Pad()\n  pc13CuStep("SOURCE_COLLECT_COMPLETE")\n  pc13BuildCuIndex("SOURCE")\n  oldHole=')
s=s.replace('  oldLocal=pc13NearbySameNetCopper(', '  pc13CuStep("SOURCE_LOCAL_TOTAL_CU_BEGIN")\n  oldLocal=pc13NearbySameNetCopper(')
s=s.replace('  oldLocalRemainder=pc13RingOp(oldHole oldLocal \'ANDNOT)\n  unless(axlOpenDesignForBatch(candidateCopy "wf") error("Cannot open candidate copy\\n"))\n  after=', '  oldLocalRemainder=pc13RingOp(oldHole oldLocal \'ANDNOT)\n  pc13CuStep("SOURCE_LOCAL_TOTAL_CU_COMPLETE")\n  pc13CuStep("OPEN_CANDIDATE_BEGIN")\n  unless(axlOpenDesignForBatch(candidateCopy "wf") error("Cannot open candidate copy\\n"))\n  pc13CuStep("OPEN_CANDIDATE_COMPLETE")\n  pc13CuStep("TARGET_COLLECT_BEGIN")\n  after=')
s=s.replace('  after=pc13RingCollect(rows "TARGET") newPad=pc13PC184Pad()\n  newLocalRemainder=', '  after=pc13RingCollect(rows "TARGET") newPad=pc13PC184Pad()\n  pc13CuStep("TARGET_COLLECT_COMPLETE")\n  pc13BuildCuIndex("TARGET")\n  pc13CuStep("TARGET_LOCAL_TOTAL_CU_BEGIN")\n  newLocalRemainder=')
s=s.replace('  cf=outfile(strcat(outDir "/actual_material_differences.jsonl"))', '  pc13CuStep("TARGET_LOCAL_TOTAL_CU_COMPLETE")\n  cf=outfile(strcat(outDir "/actual_material_differences.jsonl"))')
s=s.replace('   key=car(row) a=before[key] b=after[key]\n   ; The same native', '   key=car(row) a=before[key] b=after[key]\n   pc13CuStep(strcat("KEY_BEGIN " key))\n   ; The same native')
s=s.replace('   crosshits=crosshits+pc13AddedCuCrossNet(', '   pc13CuStep(strcat("KEY_MATERIAL_COMPLETE_BEGIN_CROSS_NET " key))\n   crosshits=crosshits+pc13AddedCuCrossNet(')
s=s.replace('   printf("PC13_MATERIAL_DIFF %s removed=%d added=%d\\n" key length(removed) length(added)))', '   printf("PC13_MATERIAL_DIFF %s removed=%d added=%d\\n" key length(removed) length(added))\n   pc13CuStep(strcat("KEY_COMPLETE " key)))')
s=s.replace(' close(f) t))', ' close(f) t))')
needle='length(oldLocalRemainder) length(newLocalRemainder) crosshits) close(f) t))'
assert needle in s
s=s.replace(needle,'length(oldLocalRemainder) length(newLocalRemainder) crosshits) close(f) pc13CuStep("ALL_COMPLETE") close(pc13CuStepPort) t))')
assert 'SOURCE_LOCAL_TOTAL_CU_COMPLETE' in s and 'OPEN_CANDIDATE_COMPLETE' in s and 'KEY_COMPLETE ' in s
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
out=W/'pc13_native_changed_rings_v7.il';assert not out.exists()
out.write_text(s,encoding='utf-8')
print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
r=(W/'review_native_material_ledger13_v5.py').read_text(encoding='utf-8')
r=r.replace("counts.get('GUARD_VERSION')==6", "counts.get('GUARD_VERSION')==7").replace('guard version6','guard version7').replace('guard_validation=dict(version=6,','guard_validation=dict(version=7,')
needle=" assert counts.get('GUARD_VERSION')==7,'Require final conservative native guard version7'"
assert needle in r
r=r.replace(needle,needle+"\n steps=(n/'STEP.txt').read_text().splitlines();assert steps[0]=='ENTER_V7' and steps[-1]=='ALL_COMPLETE';assert sum(x.startswith('KEY_COMPLETE ') for x in steps)==11;assert 'SOURCE_INDEX_COMPLETE objects=' in '\\n'.join(steps) and 'TARGET_INDEX_COMPLETE objects=' in '\\n'.join(steps)")
r=r.replace("n/'launch_report.json']", "n/'launch_report.json',n/'STEP.txt']")
ast.parse(r)
out=W/'review_native_material_ledger13_v6.py';assert not out.exists()
out.write_text(r,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
