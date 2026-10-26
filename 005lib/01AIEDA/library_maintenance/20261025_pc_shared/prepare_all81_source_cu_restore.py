"""Restore only REAL frozen source route/symbolEtch copper deleted by ECO.
The new library pads remain standard. Restored copper is board-owned routing.
No CAD invocation. Source/target native phases use detached polygons and a
top-level open command, never a reentrant SKILL database open.
"""
from pathlib import Path
import sys,json,hashlib
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration';D=W/'all81_source_cu_v2';V=W/'all81_migration_v7'
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
def atom(x):
 if isinstance(x,list):return '('+' '.join(atom(v) for v in x)+')'
 if isinstance(x,Atom):return str(x)
 if isinstance(x,str):return json.dumps(x)
 return str(x)
def sk(p):return json.dumps(str(p).replace('\\','/'))
assert not D.exists();D.mkdir()
groups=parse_many((W/'all81_stubs_v1/ALL81_STUB_CANDIDATES.ilist').read_text())
segments={}
for key,rows in groups:
 for row in rows:
  end=sorted(row[6]);needle=[row[4],row[2],row[3],row[5],end]
  segments[atom(needle)]=needle
(D/'SOURCE_FROZEN_REAL_SEGMENTS.ilist').write_text('\n'.join(segments)+'\n',encoding='utf-8')
(D/'SOURCE_SYMBOL_ETCH_SHAPE_PINS7.ilist').write_text((V/'SOURCE_SHAPE_LOST_PINS.ilist').read_text(),encoding='utf-8')
s='load('+sk(V/'pc13_native_replace_v7.il')+')\nload('+sk(W/'pc13_native_changed_rings_v10.il')+')\nload('+sk(W/'all81_stubs_v1/all81_repair_stubs.il')+')\n'
s+='''procedure(pc13SourceCuKey(kind net layer width ends)
 let((a b) a=pc13StubGridPoint(car(ends)) b=pc13StubGridPoint(cadr(ends))
  unless(alphalessp(sprintf(nil "%L" a) sprintf(nil "%L" b)) a=pc13StubGridPoint(cadr(ends)) b=pc13StubGridPoint(car(ends)))
  sprintf(nil "%L" list(kind net layer width a b))))
procedure(pc13SourceCuAdd(o key net layer role f)
 let((polys copy e)
  polys=if(member(o->objType '("line" "arc")) then axlPolyFromDB(o ?holes t ?line2poly t ?endCapType 'ROUND) else axlPolyFromDB(o ?holes t)) e=axlPolyErrorGet()
  when(e error("Source real-Cu conversion failed %L\\n" e)) polys=remove(nil polys)
  unless(polys error("Source real-Cu object empty %s\\n" key))
  copy=axlPolyOffset(polys '(0.0 0.0) t) e=axlPolyErrorGet()
  when(e error("Source real-Cu detached clone failed %L\\n" e)) copy=remove(nil copy)
  unless(copy error("Source real-Cu clone empty\\n"))
  when(pc13RingOp(copy polys 'ANDNOT) || pc13RingOp(polys copy 'ANDNOT) error("Source detached clone differs from actual sourceCu\\n"))
  foreach(p copy unless(null(p->holes) error("Source Cu restore requires explicit void handling %s\\n" key)))
  pc13FrozenSourceCu=cons(list(key net layer copy role) pc13FrozenSourceCu)
  pc13RingWrite(f key role copy) t))
procedure(pc13SourceCuVisit(o f)
 let((attrs key kind)
  when(o && !pc13SourceVisitSeen[o]
   pc13SourceVisitSeen[o]=t kind=o->objType
   if(member(kind '("line" "arc")) && member(o->layer '("ETCH/TOP" "ETCH/BOTTOM" "ETCH/L3")) then
    key=pc13SourceCuKey(kind o->net->name o->layer o->width o->startEnd)
    when(pc13SourceNeedles[key]
     pc13SourceMatched[key]=t
     pc13SourceCuAdd(o key o->net->name o->layer "REAL_SOURCE_ROUTE_SEGMENT" f))
   else
    attrs=o->? when(member('children attrs) foreach(child o->children pc13SourceCuVisit(child f)))
    when(member('segments attrs) foreach(child o->segments pc13SourceCuVisit(child f)))))))
procedure(pc13SourceCuPrepare(dir)
 let((f pf row rows keys c p shapes seenShapes key)
  sstatus(fullPrecision t)
  pc13AllPinGate('''+sk(V/'SOURCE_PINS6521.ilist')+''')
  pc13FrozenSourceCu=nil pc13SourceNeedles=makeTable('pc13SourceNeedles nil) pc13SourceMatched=makeTable('pc13SourceMatched nil) pc13SourceVisitSeen=makeTable('pc13SourceVisitSeen nil)
  f=infile('''+sk(D/'SOURCE_FROZEN_REAL_SEGMENTS.ilist')+''') keys=nil
  while(row=lineread(f) row=car(row) key=pc13SourceCuKey(car(row) nth(1 row) nth(2 row) nth(3 row) nth(4 row)) pc13SourceNeedles[key]=t keys=cons(key keys)) close(f)
  unless(length(keys)=='''+str(len(segments))+''' error("Frozen source segment count failed\\n"))
  pf=outfile(strcat(dir "/SOURCE_REAL_CU_POLYGONS.jsonl"))
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13SourceCuVisit(b pf)))
  foreach(b axlDBGetLonelyBranches() pc13SourceCuVisit(b pf))
  foreach(key keys unless(pc13SourceMatched[key] error("Frozen segment not found in actual source %s\\n" key)))
  f=infile('''+sk(D/'SOURCE_SYMBOL_ETCH_SHAPE_PINS7.ilist')+''') rows=nil while(row=lineread(f) rows=cons(car(row) rows)) close(f) seenShapes=makeTable('pc13SourceShapeSeen nil)
  foreach(selection rows
   c=pc13Comp(car(selection)) p=car(setof(q c->symbol->pins equal(q->number cadr(selection)) && equal(q->xy nth(2 selection))))
   unless(p error("Source original symbolEtch pin missing\\n"))
   shapes=setof(q axlDBGetConnect(p t) equal(q->objType "shape") && equal(q->net->name p->net->name) && equal(q->symbolEtch c->symbol))
   unless(shapes error("Source exact symbolEtch shape missing\\n"))
   foreach(shape shapes
    unless(seenShapes[shape]
     seenShapes[shape]=t
     unless(shape->fill && null(shape->voids) && null(shape->dynamicGroup) && member(shape->layer '("ETCH/TOP" "ETCH/BOTTOM")) error("Source symbolEtch unsupported shape mode\\n"))
     key=sprintf(nil "SOURCE_SYMBOL_ETCH_%s.%s" car(selection) cadr(selection))
     pc13SourceCuAdd(shape key shape->net->name shape->layer "EXACT_SOURCE_SYMBOL_ETCH_BRIDGE" pf))))
  close(pf) pc13FrozenSourceCu=reverse(pc13FrozenSourceCu)
  f=outfile(strcat(dir "/SOURCE_CU_PREPARED.txt")) fprintf(f "FROZEN_REAL_ROUTE_SEGMENT_KEYS=%d\\nSOURCE_OBJECTS=%d\\nDETACHED_NATIVE_POLYGONS_CLONED_BIDIRECTIONAL_EXACT\\nNO_SOURCE_MUTATION\\n" length(keys) length(pc13FrozenSourceCu)) close(f) t))
procedure(pc13SourceCuCreate(rows f)
 let((result created actual source count)
  count=0
  foreach(row rows
   source=nth(3 row)
   foreach(poly source
    result=axlDBCreateShape(poly t nth(2 row) nth(1 row) nil)
    unless(result && car(result) error("Exact source Cu shape creation failed %s\\n" car(row)))
    created=car(result) axlDBRefreshId(created)
    unless(equal(created->net->name nth(1 row)) && equal(created->layer nth(2 row)) && null(created->symbolEtch) error("Restored Cu identity/board-owned guard failed\\n"))
    actual=axlPolyFromDB(created ?holes t) when(axlPolyErrorGet() error("Restored Cu conversion failed\\n")) actual=remove(nil actual)
    when(pc13RingOp(actual list(poly) 'ANDNOT) || pc13RingOp(list(poly) actual 'ANDNOT) error("Restored source Cu differs from exact original polygon\\n"))
    count=count+1 fprintf(f "%s\\t%s\\t%s\\t%L\\tSOURCE_CU_EXACT_BOTH_DIRECTIONS\\n" car(row) nth(1 row) nth(2 row) created->bBox) drain(f))) count))
procedure(pc13SourceCuRestore(dir)
 let((f sf row source missing same other cross restore failed targetPose targetText targetProps oldDrc oldFill count key remains)
  unless(pc13FrozenSourceCu error("Source prepare globals missing; top-level open required\\n"))
  sstatus(fullPrecision t) pc13AllPinGate('''+sk(V/'TARGET_PINS6521.ilist')+''')
  targetPose=makeTable('pc13TargetPose nil) targetText=makeTable('pc13TargetText nil) targetProps=makeTable('pc13TargetProps nil)
  foreach(c axlDBGetDesign()->components targetPose[c->name]=pc13Pose(c->symbol) targetText[c->name]=pc13TextSorted(c->symbol) targetProps[c->name]=pc13Props(c->compdef))
  oldDrc=axlDBControl('drcEnable) oldFill=axlDBControl('dynamicFillMode)
  pc13CuStepPort=outfile(strcat(dir "/STEP.txt")) pc13BuildCuIndex("TARGET")
  f=outfile(strcat(dir "/SOURCE_CU_MISSING_AND_CROSS.jsonl")) sf=outfile(strcat(dir "/SOURCE_CU_RESTORE_PREFLIGHT.tsv"))
  fprintf(sf "key\\tnet\\tlayer\\tsource_poly_count\\tmissing_count\\tother_net_intersections\\n") restore=nil failed=nil
  foreach(row pc13FrozenSourceCu
   key=car(row) source=nth(3 row) missing=nil
   foreach(poly source same=pc13NearbySameNetCopper(nth(1 row) nth(2 row) poly->bBox) missing=append(missing pc13RingOp(list(poly) same 'ANDNOT)))
   cross=nil
   foreach(poly missing other=pc13NearbyOtherNetCopper(nth(1 row) nth(2 row) poly->bBox) cross=append(cross pc13RingOp(list(poly) other 'AND)))
   pc13RingWrite(f key "SOURCE_CU_ABSENT_FROM_TARGET_SAME_NET" missing) pc13RingWrite(f key "RESTORATION_OTHER_NET_INTERSECTION" cross)
   fprintf(sf "%s\\t%s\\t%s\\t%d\\t%d\\t%d\\n" key nth(1 row) nth(2 row) length(source) length(missing) length(cross)) drain(sf) drain(f)
   when(cross failed=cons(key failed)) when(missing restore=cons(row restore)))
  close(sf) close(f)
  when(failed close(pc13CuStepPort) error("Original source Cu restoration intersects current other-net Cu %L\\n" failed))
  restore=reverse(restore) f=outfile(strcat(dir "/SOURCE_CU_RESTORED_OBJECTS.tsv"))
  count=axlDBCloak('pc13SourceCuCreate(restore f) 'shape) close(f)
  unless(numberp(count) error("Exact source Cu restoration batch failed\\n"))
  axlDBRefreshId(nil) pc13BuildCuIndex("RESTORED") remains=nil
  foreach(row pc13FrozenSourceCu foreach(poly nth(3 row)
   same=pc13NearbySameNetCopper(nth(1 row) nth(2 row) poly->bBox)
   when(pc13RingOp(list(poly) same 'ANDNOT) remains=cons(car(row) remains))))
  when(remains close(pc13CuStepPort) error("Actual source Cu still missing after restore %L\\n" remains))
  foreach(c axlDBGetDesign()->components
   pc13ExpectedPins(c->name c->symbol)
   unless(equal(targetPose[c->name] pc13Pose(c->symbol)) && equal(targetText[c->name] pc13TextSorted(c->symbol)) && equal(targetProps[c->name] pc13Props(c->compdef)) error("SourceCu restore changed approved pin/pose/text/props\\n")))
  unless(equal(oldDrc axlDBControl('drcEnable)) && equal(oldFill axlDBControl('dynamicFillMode)) error("SourceCu restore changed DRC/fill modes\\n"))
  unless(axlSaveDesign(?design strcat(dir "/ALL81_SOURCE_CU_RESTORED.brd") ?noMru t ?noConfirm t) error("SourceCu restored save failed\\n"))
  f=outfile(strcat(dir "/SOURCE_CU_RESTORE_COMPLETE.txt")) fprintf(f "EXACT_ORIGINAL_CU_RESTORED_AS_BOARD_OWNED_SHAPES=%d\\nALL_FROZEN_SOURCE_ROUTE_AND_SYMBOL_CU_COVERED\\nALL6521_PINS_1066_POSE_TEXT_PROPS_UNCHANGED\\nORIGINAL_DRC=%L\\nORIGINAL_FILL=%L\\n" count oldDrc oldFill) close(f) close(pc13CuStepPort) count))
'''
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
p=D/'all81_restore_actual_source_cu.il';p.write_text(s,encoding='utf-8')
receipt={'status':'PREPARED_NOT_NATIVE_RUN','source_sha256':'06B8DD73EE20A4C01A0BF36E0BF6CD0FDDFE20CE2F89DA430A2C003414BE9405','target_sha256':'A9651E39CBD8DAC0B67566686AF3D2CA38B2AA517C5C1ADCD74E81336D563F51','source_segment_geometry_keys':len(segments),'shape_pin_count':7,'entry_source':'pc13SourceCuPrepare(dir)','entry_target':'pc13SourceCuRestore(dir)','source_objects':'Only real original frozen source route line/arc segments + the7 actual original symbolEtch shapes. Original pin regular pads are not copied.','restoration':'Only source objects with actual same-net target Cu ANDNOT remainder are restored. Full source polygon copied for reliable positive-area attachment. All geometries exact bidirectional, missing new material must have no other-net intersection.','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in D.iterdir()}}
(D/'SOURCE_CU_PREPARATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps(receipt,indent=2))
