"""Prepare a read-only native all-branch stroke-containment preflight. No CAD."""
from pathlib import Path
import hashlib,json,sys
M=Path(__file__).parent
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration';P=M/'public0010_path_stubs_plan13_v1';D=M/'public0010_stub_preflight_bundle13_v1';B=M/'public0010_native403_bundle13_v6_restore'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
sk=lambda p:json.dumps(str(p).replace('\\','/'))
def balanced(s):
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
 assert depth==0 and not quoted,(depth,quoted)
def main():
 assert not D.exists();report=json.loads((P/'PUB0010_STUB_PREPARATION.json').read_text());assert not report['unresolved_issues']
 ring=(W/'pc13_native_changed_rings_v10.il').read_text()
 pure=ring[ring.index('procedure(pc13RingOp('):ring.index('procedure(pc13ShapeTable(')]
 pure+=ring[ring.index('procedure(pc13BoxesMeet('):ring.index('procedure(pc13BuildCuIndex(')]
 pure+=ring[ring.index('procedure(pc13IndexedCuPolys('):ring.index(' ; Read-only fallback:')]
 proven=(W/'all81_stubs_post_cu_v3/all81_repair_stubs_v3.il').read_text()
 core=proven[proven.index('procedure(pc13SotStubPin('):proven.index('procedure(pc13BuildCuIndex(')]
 core=core.replace('mils2','millimeters4').replace('x*100.0','x*10000.0').replace('y*100.0','y*10000.0').replace('ix/100.0','ix/10000.0').replace('iy/100.0','iy/10000.0')
 s='pub403Bundle='+sk(B)+'\nload('+sk(B/'public0010_native403_v1.il')+')\n'+pure+core
 s+='''
; No expected via hardcount is borrowed from the main motherboard case.
; All symbols (including21 nonlogical symbols) and lonely branches are indexed.
procedure(pub0010BuildCuIndex()
 let((f)
  pc13CuIndexSeen=makeTable('pc13CuIndexSeen nil) pc13CuIndexRows=nil pc13CuIndexCounts=makeTable('pc13CuIndexCounts 0)
  pc13CuPolyCache=makeTable('pc13CuPolyCache nil) pc13CuPolyCached=makeTable('pc13CuPolyCached nil)
  foreach(s axlDBGetDesign()->symbols foreach(p s->pins pc13CuIndexWalk(p)))
  foreach(s axlDBGetShapes(nil) when(member(s->layer '("ETCH/TOP" "ETCH/L2" "ETCH/L3" "ETCH/BOTTOM")) pc13CuIndexWalk(s)))
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13CuIndexWalk(b)))
  foreach(b axlDBGetLonelyBranches() pc13CuIndexWalk(b))
  pc13CuIndexRows=reverse(pc13CuIndexRows)
  unless(pc13CuIndexCounts["pin"]==2698 && pc13CuIndexCounts["path"]>0 error("PUB0010 actual-Cu index incomplete\\n"))
  t))
procedure(pub0010SourceKey(kind net layer width se) sprintf(nil "%L" list(kind net layer width se)))
procedure(pub0010FrozenStrokeCovered(row)
 let((key path polys same covered)
  covered=nil
  when(equal(nth(4 row) "line")
   key=pub0010SourceKey(nth(4 row) nth(2 row) nth(3 row) nth(5 row) nth(6 row))
   unless(pub0010FrozenKeys[key] error("PUB0010 whole-stroke check outside exact frozen source2068 ledger\\n"))
   if(pub0010StrokeCached[key] then covered=pub0010StrokeCovered[key]
   else
    path=axlPathStart(nth(6 row) nth(5 row)) polys=axlPolyFromDB(path ?line2poly t ?endCapType 'ROUND ?holes t)
    when(axlPolyErrorGet() error("PUB0010 original source stroke conversion error\\n")) polys=remove(nil polys)
    unless(polys error("PUB0010 frozen original source stroke is empty\\n")) covered=t
    foreach(poly polys
     same=pc13NearbySameNetCopper(nth(2 row) nth(3 row) poly->bBox)
     when(pc13RingOp(list(poly) same 'ANDNOT) covered=nil))
    pub0010StrokeCached[key]=t pub0010StrokeCovered[key]=covered))
  covered))
; Return an explicit reason for each tested candidate. Errors are separately
; caught by the collector, which continues through every source branch.
procedure(pub0010StubCandidateStatus(row)
 prog((pin matching path polys pad outside)
  pin=pc13SotStubPin(car(row) cadr(row))
  unless(pin && equal(pin->xy nth(8 row)) && equal(pin->net->name nth(2 row)) && equal(pin->name nth(11 row)) return("TARGET_PIN_GUARD_FAILED"))
  matching=setof(x pc13StubSegments equal(car(x) nth(4 row)) && equal(nth(1 x) nth(2 row)) && equal(nth(2 x) nth(3 row)) && equal(nth(3 x) nth(5 row)) && (equal(nth(4 x) nth(6 row)) || equal(nth(4 x) reverse(nth(6 row)))))
  unless(matching || (equal(nth(4 row) "line") && pc13SotLineUnionCovers(row)) || pub0010FrozenStrokeCovered(row) return("ORIGINAL_SOURCE_STROKE_NOT_IN_CURRENT_SAME_NET_CU"))
  path=axlPathStart(list(nth(7 row) nth(8 row)) nth(9 row))
  polys=axlPolyFromDB(path ?line2poly t ?endCapType 'ROUND ?holes t)
  when(axlPolyErrorGet() return("STUB_STROKE_POLYGON_ERROR")) polys=remove(nil polys)
  unless(polys return("EMPTY_STUB_STROKE"))
  pad=axlPolyFromDB(pin ?layer nth(3 row) ?padType 'REGULAR ?holes t)
  when(axlPolyErrorGet() return("TARGET_REGULAR_PAD_POLYGON_ERROR")) pad=remove(nil pad)
  unless(pad return("EMPTY_TARGET_REGULAR_PAD"))
  outside=pc13RingOp(polys pad 'ANDNOT)
  return(if(outside then "STROKE_OUTSIDE_TARGET_REGULAR_PAD" else "FIT_WHOLE_STROKE_INSIDE_TARGET_REGULAR_PAD"))))
procedure(pub0010StubPreflight(dir)
 let((groups f statusPort selectedPort failedPort row frozenCount pc13StubSeen pc13StubSegments oldDrc group selected result status geometryKey selectedKeys rows failed tested fits)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  pub403SnapshotAll(strcat(dir "/PREFLIGHT_BEFORE_FULL593_TEXT_PROPS.ilist")) oldDrc=axlDBControl('drcEnable)
  pc13StubSeen=makeTable('pc13StubSeen nil) pc13StubSegments=nil
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13SotStubWalk(b)))
  foreach(b axlDBGetLonelyBranches() pc13SotStubWalk(b))
  pub0010BuildCuIndex() pub0010FrozenKeys=makeTable('pub0010FrozenKeys nil)
  pub0010StrokeCached=makeTable('pub0010StrokeCached nil) pub0010StrokeCovered=makeTable('pub0010StrokeCovered nil)
  frozenCount=0 f=infile(@FROZEN@)
  while(row=lineread(f) row=car(row) frozenCount=frozenCount+1 pub0010FrozenKeys[pub0010SourceKey(car(row) nth(1 row) nth(2 row) nth(3 row) nth(4 row))]=t) close(f)
  unless(frozenCount==@FROZEN_COUNT@ error("PUB0010 source actual segment ledger incomplete\\n"))
  groups=pub403Rows(@PLAN@) unless(length(groups)==@GROUPS@ error("PUB0010 exact source branch group count differs\\n"))
  statusPort=outfile(strcat(dir "/ALL_BRANCH_CANDIDATE_NATIVE_STATUS.ilist"))
  selectedPort=outfile(strcat(dir "/SELECTED_WHOLE_PAD_INTERNAL_STUBS.ilist"))
  failedPort=outfile(strcat(dir "/FAILED_SOURCE_BRANCH_GROUPS.ilist"))
  failed=0 tested=0 fits=0 selectedKeys=nil rows=nil
  foreach(group groups
   selected=nil
   foreach(candidate cadr(group)
    unless(selected
     result=errset(pub0010StubCandidateStatus(candidate) t) tested=tested+1
     status=if(result then car(result) else "NATIVE_ERROR_SEE_EXACT_STDOUT")
     fprintf(statusPort "%L\\n" list(car(group) status candidate)) drain(statusPort)
     when(equal(status "FIT_WHOLE_STROKE_INSIDE_TARGET_REGULAR_PAD") selected=candidate)))
   if(selected then
    fits=fits+1 geometryKey=list(car(selected) cadr(selected) nth(2 selected) nth(3 selected) nth(7 selected) nth(8 selected) nth(9 selected))
    unless(member(geometryKey selectedKeys) selectedKeys=cons(geometryKey selectedKeys) rows=cons(selected rows) fprintf(selectedPort "%L\\n" selected) drain(selectedPort))
   else failed=failed+1 fprintf(failedPort "%L\\n" group) drain(failedPort))
   printf("PUB0010_STUB_PREFLIGHT_BRANCH %d FIT=%d FAILED=%d\\n" fits+failed fits failed))
  close(statusPort) close(selectedPort) close(failedPort)
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  unless(equal(oldDrc axlDBControl('drcEnable)) error("PUB0010 read-only preflight changed DRC mode\\n"))
  pub403SnapshotAll(strcat(dir "/PREFLIGHT_AFTER_FULL593_TEXT_PROPS.ilist"))
  f=outfile(strcat(dir "/ALL_SOURCE_BRANCH_PREFLIGHT_COMPLETE.txt"))
  fprintf(f "PUB0010_ALL_SOURCE_BRANCHES_PREFLIGHT_COMPLETE_NO_CREATE_NO_SAVE\\nGROUPS=%d\\nFIT_GROUPS=%d\\nFAILED_GROUPS=%d\\nTESTED_CANDIDATES=%d\\nUNIQUE_SELECTED_STUBS=%d\\nFULL2698_593SYMBOLS_572COMPONENTS_AND_SOURCE_TEXT_PROPS_EXACT\\nNATIVE_FULL915_CONNECTION_PARTITION_PROOF_STILL_REQUIRED\\n" length(groups) fits failed tested length(rows)) close(f) failed))
'''
 s=s.replace('@FROZEN@',sk(P/'SOURCE_FROZEN_REAL_SEGMENTS.ilist')).replace('@PLAN@',sk(P/'PUB0010_STUB_CANDIDATES.ilist')).replace('@FROZEN_COUNT@',str(report['frozen_actual_source_segments'])).replace('@GROUPS@',str(report['branch_groups']))
 balanced(s);D.mkdir();helper=D/'public0010_stub_preflight_v1.il';helper.write_text(s,'utf-8')
 files=[helper,P/'PUB0010_STUB_CANDIDATES.ilist',P/'SOURCE_FROZEN_REAL_SEGMENTS.ilist',P/'PUB0010_STUB_PREPARATION.json']
 old=json.loads((B/'BUNDLE_MANIFEST.json').read_text('utf-8-sig'));files += [Path(x['path']) for x in old['bundle_files']+old['external_proofs']]
 man=dict(schema='PUBLIC0010_ALL_SOURCE_BRANCH_READONLY_STUB_PREFLIGHT_V1',units=['millimeters',4],candidate_board=report['candidate_board'],candidate_board_sha256=report['candidate_sha256'],branch_groups=report['branch_groups'],candidate_rows=report['candidate_rows'],helper=str(helper),entry='pub0010StubPreflight',marker='ALL_SOURCE_BRANCH_PREFLIGHT_COMPLETE.txt',files=[dict(path=str(p),sha256=sha(p)) for p in dict.fromkeys(files)],does_not_create_paths_or_save=True)
 (D/'MANIFEST.json').write_text(json.dumps(man,indent=2),'utf-8');print(json.dumps(dict(helper_sha256=sha(helper),manifest_sha256=sha(D/'MANIFEST.json'),groups=report['branch_groups'],candidates=report['candidate_rows']),indent=2))
if __name__=='__main__':main()
