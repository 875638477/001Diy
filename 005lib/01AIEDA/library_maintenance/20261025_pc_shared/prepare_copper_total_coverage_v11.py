"""Freeze V10 native added-piece identities and prepare source-total Cu audit."""
from pathlib import Path
from decimal import Decimal
import csv,json,hashlib
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
N=W.parent/'copper_material_checked13_v10open'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def qt(s):return json.dumps(s,ensure_ascii=True)
def box(b):return '('+' '.join('('+' '.join(str(v) for v in p)+')' for p in b)+')'
rows=[json.loads(l,parse_float=Decimal) for l in (N/'actual_material_differences.jsonl').read_text().splitlines()]
added=[x for x in rows if x['side']=='ACTUAL_SHAPE_COPPER_ADDED']
methods=list(csv.DictReader((N/'margin_validation_methods.tsv').open(),delimiter='\t'))
checks=list(csv.DictReader((N/'cross_net_checks.tsv').open(),delimiter='\t'))
assert len(added)==len(methods)==len(checks)==150
plans=[];normal_probes=0
for i,(r,m,c) in enumerate(zip(added,methods,checks),1):
 assert r['key']==m['key']==c['key']
 layer,net,_=r['key'].split('|')
 probe=m['method']=='NATIVE_EXPAND_0D01MIL' and int(c['margin_intersections'])>0
 normal_probes+=probe
 poly=r['poly']
 plans.append('('+ ' '.join([str(i),qt(r['key']),qt(layer),qt(net),box(poly['bbox']),qt(m['input_bbox']),qt(format(poly['area'],'.10f')),str(len(poly['outer'])),str(len(poly['holes'])),'t' if probe else 'nil']) +')')
assert normal_probes==6
plan=W/'FROZEN150_SOURCE_TOTAL_CU_PLAN_V11.ilist';assert not plan.exists()
plan.write_text('\n'.join(plans)+'\n',encoding='utf-8')
receipt=W/'FROZEN150_SOURCE_TOTAL_CU_PLAN_V11.json';assert not receipt.exists()
receipt.write_text(json.dumps(dict(pieces=150,normal_margin_windows=6,plan=str(plan),plan_sha256=sha(plan),inputs={str(p):sha(p) for p in [N/'actual_material_differences.jsonl',N/'margin_validation_methods.tsv',N/'cross_net_checks.tsv',N/'MATERIAL_DIFF_COMPLETE.txt',N/'launch_report.json']}),indent=2),encoding='utf-8')

s=(W/'pc13_native_changed_rings_v10.il').read_text(encoding='utf-8')
s+=r'''
; V11: frozen bbox is ONLY an object-index query. Full native source copper
; is cloned and used as the ANDNOT operand; no bbox authorizes a Cu delta.
procedure(pc13Cu11Rectangle(bb extra)
 let((x0 y0 x1 y1 path ps e)
  x0=caar(bb)-extra y0=cadar(bb)-extra x1=caadr(bb)+extra y1=cadadr(bb)+extra
  path=axlPathStart(list(x0:y0 x1:y0 x1:y1 x0:y1 x0:y0) 0.0)
  unless(path error("V11 query rectangle path failed\n"))
  ps=axlPolyFromDB(path) e=axlPolyErrorGet()
  when(e error("V11 query rectangle polygon error %L\n" e))
  ps=remove(nil ps) unless(length(ps)==1 error("V11 query rectangle missing\n")) ps))
procedure(pc13Cu11ProbeSource(row geometryf objectf summaryf)
 let((i key layer net bb clipBox same clip guard residual sourceDirect sourceMargin objectNo obj kind ref pin other direct margin)
  i=car(row) key=nth(1 row) layer=nth(2 row) net=nth(3 row) bb=nth(4 row)
  clipBox=pc13Cu11Rectangle(bb 0.1)
  same=pc13NearbySameNetCopper(net layer car(clipBox)->bBox)
  clip=pc13RingOp(same clipBox 'AND)
  guard=nil residual=nil
  when(clip
   guard=axlPolyExpand(clip 0.01 'ACU_BLUNT)
   when(axlPolyErrorGet() error("V11 source normal-margin error\n"))
   unless(guard error("V11 source normal-margin bareNIL\n"))
   guard=remove(nil guard)
   residual=pc13RingOp(clip guard 'ANDNOT))
  ; Keep a failed containment as source-probe diagnostic. Never substitute a
  ; wide bbox for the SOURCE margin or claim a clearance proof from it.
  pc13RingWrite(geometryf sprintf(nil "SOURCE6|%d" i) "SOURCE_CLIPPED_SAME_NET_ACTUAL_CU" clip)
  pc13RingWrite(geometryf sprintf(nil "SOURCE6|%d" i) "SOURCE_NORMAL_0D01MIL_GUARD" guard)
  pc13RingWrite(geometryf sprintf(nil "SOURCE6|%d" i) "SOURCE_GUARD_LOST_INPUT_RESIDUE" residual)
  sourceDirect=0 sourceMargin=0 objectNo=0
  pc13Cu11SourceMarginContacts[i]=nil pc13Cu11SourceGuardLost[i]=length(residual)
  foreach(ir pc13CuIndexRows
   kind=nth(4 ir)
   when(!equal(nth(1 ir) net) && (member(kind '("pin" "via")) || equal(nth(2 ir) layer)) && pc13BoxesMeet(nth(3 ir) car(clipBox)->bBox)
    obj=car(ir) other=pc13IndexedCuPolys(ir layer)
    when(other
     objectNo=objectNo+1 ref=if(equal(kind "pin") then pc13Cu11PinOwners[obj] else "") pin=if(equal(kind "pin") then obj->number else "")
     direct=pc13RingOp(clip other 'AND) margin=pc13RingOp(guard other 'AND)
     sourceDirect=sourceDirect+length(direct) sourceMargin=sourceMargin+length(margin)
     when(margin pc13Cu11SourceMarginContacts[i]=append(pc13Cu11SourceMarginContacts[i] axlPolyOffset(margin '(0.0 0.0) t)))
     fprintf(objectf "%d\t%s\t%d\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\t%d\t%d\n" i key objectNo nth(1 ir) kind obj ref pin obj->name obj->xy nth(3 ir) length(direct) length(margin))
     pc13RingWrite(geometryf sprintf(nil "SOURCE6|%d|OBJECT%d" i objectNo) "OTHER_NET_ACTUAL_CU" other)
     pc13RingWrite(geometryf sprintf(nil "SOURCE6|%d|OBJECT%d" i objectNo) "SOURCE_ACTUAL_INTERSECTS_OTHER_NET" direct)
     pc13RingWrite(geometryf sprintf(nil "SOURCE6|%d|OBJECT%d" i objectNo) "SOURCE_MARGIN_INTERSECTS_OTHER_NET" margin))))
  fprintf(summaryf "%d\t%s\t%d\t%d\t%d\t%d\n" i key objectNo sourceDirect sourceMargin length(residual))
  drain(geometryf) drain(objectf) drain(summaryf)
  pc13CuStep(sprintf(nil "SOURCE6_PROBE_COMPLETE piece=%d otherobjects=%d direct=%d margin=%d guardLost=%d" i objectNo sourceDirect sourceMargin length(residual)))
  t))
procedure(pc13MaterialSourcePrepareV11(planPath fragmentPlan outDir)
 let((f row rows geometryf objectf summaryf pc13CuIndexSeen pc13CuIndexRows pc13CuIndexCounts pc13CuPolyCache pc13CuPolyCached)
  pc13MaterialSourcePrepare(planPath outDir)
  pc13CuStepPort=outfile(strcat(outDir "/STEP.txt") "a") pc13CuStep("ENTER_V11_SOURCE_TOTAL_CU")
  f=infile(fragmentPlan) unless(f error("Frozen150 plan missing\n")) rows=nil
  while(row=lineread(f) rows=cons(car(row) rows)) close(f) rows=reverse(rows)
  unless(length(rows)==150 error("Expected150 frozen added pieces\n"))
  pc13Cu11Rows=rows pc13Cu11SourceTotal=makeTable('pc13Cu11SourceTotal nil)
  pc13Cu11SourceMarginContacts=makeTable('pc13Cu11SourceMarginContacts nil) pc13Cu11SourceGuardLost=makeTable('pc13Cu11SourceGuardLost nil)
  pc13Cu11PinOwners=makeTable('pc13Cu11PinOwners "")
  foreach(c axlDBGetDesign()->components foreach(p c->symbol->pins pc13Cu11PinOwners[p]=c->name))
  pc13BuildCuIndex("SOURCE150")
  geometryf=outfile(strcat(outDir "/source6_actual_and_margin_geometry.jsonl"))
  objectf=outfile(strcat(outDir "/source6_object_identity.tsv"))
  summaryf=outfile(strcat(outDir "/source6_summary.tsv"))
  fprintf(objectf "piece\tkey\tobject_index\tnet\tkind\tdbid\trefdes\tpin\tname\txy\tbbox\tdirect_intersections\tmargin_intersections\n")
  fprintf(summaryf "piece\tkey\tother_objects\tdirect_intersections\tmargin_intersections\tsource_guard_lost_input\n")
  foreach(row rows
   ; Whole actual polygon lists are independently detached by the indexed
   ; polygon cache, which pc13IndexedCuPolys builds with copy=t.
   pc13Cu11SourceTotal[car(row)]=pc13NearbySameNetCopper(nth(3 row) nth(2 row) nth(4 row))
   when(nth(9 row) pc13Cu11ProbeSource(row geometryf objectf summaryf))
   when(mod(car(row) 25)==0 pc13CuStep(sprintf(nil "SOURCE150_PRELOADED %d" car(row)))))
  close(geometryf) close(objectf) close(summaryf)
  pc13Cu11Ready=t pc13CuStep("SOURCE_V11_150_PRELOAD_COMPLETE_TOP_LEVEL_OPEN_TARGET")
  close(pc13CuStepPort) pc13CuStepPort=nil t))
procedure(pc13MaterialTargetFinishV11(outDir)
 let((f rows before after a b aMat bMat removed added key i fp outside inputf outsidef summaryf materialf materialsummaryf totalOutside probegeometryf probesummaryf guard others contacts newcontacts guardlost totalNewContacts pc13CuIndexSeen pc13CuIndexRows pc13CuIndexCounts pc13CuPolyCache pc13CuPolyCached)
  unless(pc13Cu11Ready && pc13Cu8Ready && equal(pc13Cu8OutDir outDir) error("V11 source preload context missing\n"))
  pc13CuStepPort=outfile(strcat(outDir "/STEP.txt") "a") pc13CuStep("ENTER_V11_TARGET_AFTER_TOP_LEVEL_OPEN")
  sstatus(fullPrecision t) rows=pc13Cu8Rows before=pc13Cu8Before
  after=pc13RingCollect(rows "TARGET") pc13PC184Pad() pc13BuildCuIndex("TARGET150")
  inputf=outfile(strcat(outDir "/all150_added_native.jsonl")) outsidef=outfile(strcat(outDir "/added_outside_source_total_cu.jsonl"))
  summaryf=outfile(strcat(outDir "/added_source_total_coverage.tsv"))
  materialf=outfile(strcat(outDir "/v11_actual_material_differences.jsonl")) materialsummaryf=outfile(strcat(outDir "/v11_actual_material_summary.tsv"))
  probegeometryf=outfile(strcat(outDir "/six_margin_contact_regression.jsonl")) probesummaryf=outfile(strcat(outDir "/six_margin_contact_regression.tsv"))
  fprintf(probesummaryf "piece\tkey\tsource_guard_lost_input\ttarget_guard_lost_input\tsource_contact_polys\ttarget_contact_polys\tnew_margin_contact_polys\n")
  fprintf(summaryf "piece\tkey\tinput_area_native\tinput_bbox\tsource_candidate_polys\toutside_polys\toutside_area_native\n")
  fprintf(materialsummaryf "key\tremoved_polys\tadded_polys\tremoved_area\tadded_area\n")
  i=0 totalOutside=0 totalNewContacts=0
  foreach(row rows
   key=car(row) a=before[key] b=after[key]
   pc13CuStep(strcat("V11_KEY_BEGIN " key))
   aMat=pc13RingOp(car(a) cadr(a) 'ANDNOT) bMat=pc13RingOp(car(b) cadr(b) 'ANDNOT)
   removed=pc13RingOp(aMat bMat 'ANDNOT) added=pc13RingOp(bMat aMat 'ANDNOT)
   pc13RingWrite(materialf key "ACTUAL_SHAPE_COPPER_REMOVED" removed) pc13RingWrite(materialf key "ACTUAL_SHAPE_COPPER_ADDED" added)
   foreach(p added
    i=i+1 fp=nth(i-1 pc13Cu11Rows)
    unless(fp && car(fp)==i && equal(nth(1 fp) key) && equal(nth(5 fp) sprintf(nil "%L" p->bBox)) && equal(nth(6 fp) sprintf(nil "%.10f" p->area)) && nth(7 fp)==length(p->vertices) && nth(8 fp)==length(p->holes)
     pc13CuStep(sprintf(nil "FROZEN150_IDENTITY_FAIL piece=%d key=%s bbox=%L area10=%.10f" i key p->bBox p->area))
     error("Target actual added fragment differs from frozenV10 identity\n"))
    outside=pc13RingOp(list(p) pc13Cu11SourceTotal[i] 'ANDNOT)
    totalOutside=totalOutside+length(outside)
    pc13RingWrite(inputf sprintf(nil "PIECE%d|%s" i key) "ACTUAL_ADDED_INPUT" list(p))
    pc13RingWrite(outsidef sprintf(nil "PIECE%d|%s" i key) "ADDED_OUTSIDE_SOURCE_SAME_NET_TOTAL_CU" outside)
    fprintf(summaryf "%d\t%s\t%L\t%L\t%d\t%d\t%L\n" i key p->area p->bBox length(pc13Cu11SourceTotal[i]) length(outside) apply('plus cons(0.0 cons(0.0 foreach(mapcar z outside z->area))))) drain(summaryf) drain(inputf) drain(outsidef)
    when(nth(9 fp)
     guard=axlPolyExpand(list(p) 0.01 'ACU_BLUNT)
     when(axlPolyErrorGet() error("V11 target normal-margin probe error\n"))
     unless(guard error("V11 target normal-margin probe bareNIL\n"))
     guard=remove(nil guard) guardlost=pc13RingOp(list(p) guard 'ANDNOT)
     others=nil foreach(g guard others=append(others pc13NearbyOtherNetCopper(nth(3 fp) nth(2 fp) g->bBox)))
     contacts=pc13RingOp(guard others 'AND)
     newcontacts=pc13RingOp(contacts pc13Cu11SourceMarginContacts[i] 'ANDNOT)
     totalNewContacts=totalNewContacts+length(newcontacts)
     pc13RingWrite(probegeometryf sprintf(nil "SOURCE6|%d" i) "TARGET_0D01_MARGIN_CONTACTS" contacts)
     pc13RingWrite(probegeometryf sprintf(nil "SOURCE6|%d" i) "NEW_CONTACTS_RELATIVE_TO_SOURCE_NATIVE_0D01_MARGIN" newcontacts)
     fprintf(probesummaryf "%d\t%s\t%d\t%d\t%d\t%d\t%d\n" i key pc13Cu11SourceGuardLost[i] length(guardlost) length(pc13Cu11SourceMarginContacts[i]) length(contacts) length(newcontacts)) drain(probesummaryf) drain(probegeometryf)))
   fprintf(materialsummaryf "%s\t%d\t%d\t%L\t%L\n" key length(removed) length(added) apply('plus cons(0.0 cons(0.0 foreach(mapcar p removed p->area)))) apply('plus cons(0.0 cons(0.0 foreach(mapcar p added p->area))))) drain(materialf) drain(materialsummaryf)
   pc13CuStep(strcat("V11_KEY_COMPLETE " key)))
  unless(i==150 error("Target actual added fragment total differs from frozen150\n"))
  close(inputf) close(outsidef) close(summaryf) close(materialf) close(materialsummaryf) close(probegeometryf) close(probesummaryf)
  f=outfile(strcat(outDir "/SOURCE_TOTAL_CU_COVERAGE_COMPLETE.txt"))
  fprintf(f "NATIVE_SOURCE_TOTAL_CU_COVERAGE_V11_COMPLETE\nADDED_INPUT_PIECES=%d\nOUTSIDE_SOURCE_SAME_NET_POLYS=%d\nPC184_SOURCE_OLD_HOLE_TOTAL_CU_OUTSIDE=%d\nSIX_NORMAL_MARGIN_NEW_CONTACT_POLYS=%d\n" i totalOutside length(pc13Cu8SourceLocalRemainder) totalNewContacts) close(f)
  pc13CuStep("V11_ALL_COMPLETE") close(pc13CuStepPort) pc13CuStepPort=nil pc13Cu11Ready=nil pc13Cu8Ready=nil t))
pc13Cu11Ready=nil
'''
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
out=W/'pc13_native_source_total_coverage_v11.il';assert not out.exists();out.write_text(s,encoding='utf-8')
print(plan);print(sha(plan));print(out);print(sha(out));print(receipt);print(sha(receipt))
