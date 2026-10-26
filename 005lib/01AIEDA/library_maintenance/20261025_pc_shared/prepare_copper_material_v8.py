"""Split read-only source/target lifetimes around an ordinary top-level edit."""
from pathlib import Path
import hashlib,ast
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'pc13_native_changed_rings_v7.il').read_text(encoding='utf-8')
start=s.index('procedure(pc13NativeChangedMaterialCheckedV7(')
s=s[:start]+r''' ; Top-level runner must execute these in order:
; skill pc13MaterialSourcePrepare(planPath outDir)
; edit "<owned target-copy .brd>"
; skill pc13MaterialTargetFinish(outDir)
; No axlOpenDesignForBatch inside a SKILL callback. No design setters/save.
procedure(pc13MaterialSourcePrepare(planPath outDir)
 let((f row rows before oldPad oldHole oldLocal oldLocalRemainder pc13CuIndexSeen pc13CuIndexRows pc13CuIndexCounts pc13CuPolyCache pc13CuPolyCached)
  when(pc13CuStepPort close(pc13CuStepPort))
  pc13CuStepPort=outfile(strcat(outDir "/STEP.txt"))
  pc13CuStep("ENTER_V8_SOURCE")
  pc13Cu8Ready=nil pc13Cu8OutDir=nil pc13Cu8Rows=nil pc13Cu8Before=nil pc13Cu8OldHole=nil pc13Cu8SourceLocalRemainder=nil
  sstatus(fullPrecision t)
  f=infile(planPath) unless(f error("Source plan missing\n"))
  rows=nil while(row=lineread(f) rows=cons(car(row) rows)) close(f) rows=reverse(rows)
  unless(length(rows)==11 error("Expected11 source plans\n"))
  pc13CuStep("SOURCE_COLLECT_BEGIN")
  before=pc13RingCollect(rows "SOURCE") oldPad=pc13PC184Pad()
  pc13CuStep("SOURCE_COLLECT_COMPLETE")
  pc13BuildCuIndex("SOURCE")
  oldHole=cadr(before["ETCH/TOP|V12MOS|OWNER511"])
  unless(length(oldHole)==1 error("ExpectedPC184 source hole4\n"))
  pc13CuStep("SOURCE_LOCAL_TOTAL_CU_BEGIN")
  oldLocal=pc13NearbySameNetCopper("V12MOS" "ETCH/TOP" car(oldHole)->bBox)
  oldLocalRemainder=pc13RingOp(oldHole oldLocal 'ANDNOT)
  pc13CuStep("SOURCE_LOCAL_TOTAL_CU_COMPLETE")
  ; pc13RingCollect uses axlPolyOffset(... t) for every saved outline/hole.
  ; Source-total remnants are explicitly detached once more before edit.
  pc13Cu8OutDir=outDir pc13Cu8Rows=rows pc13Cu8Before=before
  pc13Cu8OldHole=axlPolyOffset(oldHole '(0.0 0.0) t)
  unless(pc13Cu8OldHole error("Detached source hole lost\n"))
  pc13Cu8SourceLocalRemainder=if(oldLocalRemainder then remove(nil axlPolyOffset(oldLocalRemainder '(0.0 0.0) t)) else nil)
  when(axlPolyErrorGet() error("Detached source polygon error\n"))
  unless(length(pc13Cu8SourceLocalRemainder)==length(oldLocalRemainder) error("Detached source remainder count changed\n"))
  pc13Cu8Ready=t
  pc13CuStep("SOURCE_PREPARE_COMPLETE_EDIT_TARGET_AT_TOP_LEVEL")
  close(pc13CuStepPort) pc13CuStepPort=nil
  t))
procedure(pc13MaterialTargetFinish(outDir)
 let((f row rows before after oldHole oldLocalRemainder newLocalRemainder a b aMat bMat removed added key cf sf crossf crosss crosshits marginf margins newPad pc13CuIndexSeen pc13CuIndexRows pc13CuIndexCounts pc13CuPolyCache pc13CuPolyCached)
  unless(pc13Cu8Ready && equal(pc13Cu8OutDir outDir) error("V8 source context missing/wrong output directory\n"))
  when(pc13CuStepPort close(pc13CuStepPort))
  pc13CuStepPort=outfile(strcat(outDir "/STEP.txt") "a")
  pc13CuStep("ENTER_V8_TARGET_AFTER_TOP_LEVEL_EDIT")
  sstatus(fullPrecision t)
  rows=pc13Cu8Rows before=pc13Cu8Before oldHole=pc13Cu8OldHole oldLocalRemainder=pc13Cu8SourceLocalRemainder
  unless(length(rows)==11 && before && length(oldHole)==1 error("V8 detached context invalid\n"))
  pc13CuStep("TARGET_COLLECT_BEGIN")
  after=pc13RingCollect(rows "TARGET") newPad=pc13PC184Pad()
  pc13CuStep("TARGET_COLLECT_COMPLETE")
  pc13BuildCuIndex("TARGET")
  pc13CuStep("TARGET_LOCAL_TOTAL_CU_BEGIN")
  newLocalRemainder=pc13RingOp(oldHole pc13NearbySameNetCopper("V12MOS" "ETCH/TOP" car(oldHole)->bBox) 'ANDNOT)
  pc13CuStep("TARGET_LOCAL_TOTAL_CU_COMPLETE")
  cf=outfile(strcat(outDir "/actual_material_differences.jsonl")) sf=outfile(strcat(outDir "/actual_material_summary.tsv"))
  crossf=outfile(strcat(outDir "/cross_net_intersections.jsonl")) crosss=outfile(strcat(outDir "/cross_net_checks.tsv")) crosshits=0
  marginf=outfile(strcat(outDir "/margin_validation_polygons.jsonl")) margins=outfile(strcat(outDir "/margin_validation_methods.tsv"))
  fprintf(margins "key\tmethod\tinput_native_area\tinput_bbox\tguard_polys\n")
  fprintf(crosss "key\tdirect_intersections\tmargin_intersections\n")
  fprintf(sf "key\tremoved_polys\tadded_polys\tremoved_area\tadded_area\n")
  foreach(row rows
   key=car(row) a=before[key] b=after[key]
   pc13CuStep(strcat("KEY_BEGIN " key))
   ; Identical valid common holes cancel; changed holes stay in the material.
   aMat=pc13RingOp(car(a) cadr(a) 'ANDNOT) bMat=pc13RingOp(car(b) cadr(b) 'ANDNOT)
   removed=pc13RingOp(aMat bMat 'ANDNOT) added=pc13RingOp(bMat aMat 'ANDNOT)
   pc13CuStep(strcat("KEY_MATERIAL_COMPLETE_BEGIN_CROSS_NET " key))
   crosshits=crosshits+pc13AddedCuCrossNet(added nth(4 row) nth(3 row) key crossf crosss marginf margins)
   pc13RingWrite(cf key "ACTUAL_SHAPE_COPPER_REMOVED" removed) pc13RingWrite(cf key "ACTUAL_SHAPE_COPPER_ADDED" added)
   fprintf(sf "%s\t%d\t%d\t%.10f\t%.10f\n" key length(removed) length(added) apply('plus cons(0.0 foreach(mapcar p removed p->area))) apply('plus cons(0.0 foreach(mapcar p added p->area)))) drain(sf) drain(cf)
   printf("PC13_MATERIAL_DIFF %s removed=%d added=%d\n" key length(removed) length(added))
   pc13CuStep(strcat("KEY_COMPLETE " key)))
  pc13RingWrite(cf "PC184.2|V12MOS" "OLD_HOLE_OUTSIDE_SOURCE_SAME_NET_TOTAL_CU" oldLocalRemainder)
  pc13RingWrite(cf "PC184.2|V12MOS" "OLD_HOLE_OUTSIDE_TARGET_SAME_NET_TOTAL_CU" newLocalRemainder)
  fprintf(sf "PC184_SOURCE_TOTAL_CU_GAP\t%d\t0\t%.10f\t0\n" length(oldLocalRemainder) apply('plus cons(0.0 foreach(mapcar p oldLocalRemainder p->area))))
  close(cf) close(sf) close(crossf) close(crosss) close(marginf) close(margins)
  f=outfile(strcat(outDir "/MATERIAL_DIFF_COMPLETE.txt"))
  fprintf(f "NATIVE_ACTUAL_CHANGED11_COMPLETE\nSOURCE_SAME_NET_CU_OUTSIDE=%d\nTARGET_SAME_NET_CU_OUTSIDE=%d\nCROSS_NET_INTERSECTIONS_INCLUDING_0D01MIL_MARGIN=%d\nGUARD_VERSION=8\n" length(oldLocalRemainder) length(newLocalRemainder) crosshits)
  close(f) pc13CuStep("ALL_COMPLETE") close(pc13CuStepPort) pc13CuStepPort=nil pc13Cu8Ready=nil
  t))
; Initialize only the names required before SourcePrepare's first access.
pc13CuStepPort=nil
pc13Cu8Ready=nil
'''
# No callback body in V8 may contain any open command. The legacy rings
# entry retained from earlier versions is removed to prevent wrong entry use.
a=s.index('procedure(pc13NativeChangedRings(')
b=s.index('; Exact bbox is a query optimization only.',a)
s=s[:a]+s[b:]
assert 'axlOpenDesignForBatch(' not in s
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
out=W/'pc13_native_changed_rings_v8.il';assert not out.exists()
out.write_text(s,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
r=(W/'review_native_material_ledger13_v6.py').read_text(encoding='utf-8')
r=r.replace("counts.get('GUARD_VERSION')==7", "counts.get('GUARD_VERSION')==8").replace('guard version7','guard version8').replace('guard_validation=dict(version=7,','guard_validation=dict(version=8,')
r=r.replace("steps[0]=='ENTER_V7'", "steps[0]=='ENTER_V8_SOURCE' and 'SOURCE_PREPARE_COMPLETE_EDIT_TARGET_AT_TOP_LEVEL' in steps and 'ENTER_V8_TARGET_AFTER_TOP_LEVEL_EDIT' in steps")
ast.parse(r)
out=W/'review_native_material_ledger13_v7.py';assert not out.exists()
out.write_text(r,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
