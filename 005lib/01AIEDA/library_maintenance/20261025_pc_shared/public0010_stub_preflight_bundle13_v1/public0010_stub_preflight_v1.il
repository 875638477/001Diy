pub403Bundle="D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_native403_bundle13_v6_restore"
load("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_native403_bundle13_v6_restore/public0010_native403_v1.il")
procedure(pc13RingOp(a b op)
 let((r e)
  cond((null(a) if(equal(op 'OR) then b else nil))
       (null(b) if(equal(op 'AND) then nil else a))
       (t r=axlPolyOperation(a b op) e=axlPolyErrorGet()
        when(e error("Native polygon operation failed %L\n" e))
        unless(r error("Native polygon returned NIL instead of empty placeholder\n"))
        remove(nil r)))))
procedure(pc13BoxesMeet(a b)
 a && b && caar(a)<=caadr(b) && caadr(a)>=caar(b) && cadar(a)<=cadadr(b) && cadadr(a)>=cadar(b))
procedure(pc13CuStep(message)
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
procedure(pc13SotStubPin(ref num)
 let((c) c=pc13Comp(ref) car(setof(p c->symbol->pins equal(p->number num)))))
procedure(pc13SotStubWalk(o)
 let((attrs)
  when(o && !pc13StubSeen[o]
   pc13StubSeen[o]=t
   when(member(o->objType '("line" "arc")) pc13StubSegments=cons(list(o->objType o->net->name o->layer o->width o->startEnd) pc13StubSegments))
   attrs=o->? when(member('children attrs) foreach(x o->children pc13SotStubWalk(x)))
   when(member('segments attrs) foreach(x o->segments pc13SotStubWalk(x))))))
 ; Coordinate normalization is to the DECLARED millimeters4 database grid.
; No cross-line distance/bbox tolerance is allowed in interval coverage.
procedure(pc13StubGridPoint(p)
 let((x y ix iy)
  x=xCoord(p) y=yCoord(p) ix=round(x*10000.0) iy=round(y*10000.0)
  unless(abs(x-ix/10000.0)<0.0000001 && abs(y-iy/10000.0)<0.0000001
   error("Manual source/target route endpoint is off declared millimeters4 grid %L\n" p))
  list(ix iy)))
procedure(pc13StubGcd(a b)
 let((r) a=abs(a) b=abs(b)
  while(b!=0 r=mod(a b) a=b b=r) a))
procedure(pc13SotLineUnionCovers(row)
 let((ab a b dx dy divisor axis lo hi ranges c d cx cy dx2 dy2 first low high reach ok)
  ab=nth(6 row) a=pc13StubGridPoint(car(ab)) b=pc13StubGridPoint(cadr(ab))
  dx=car(b)-car(a) dy=cadr(b)-cadr(a)
  unless(dx!=0 || dy!=0 error("Degenerate frozen source line\n"))
  axis=if(abs(dx)>=abs(dy) then 0 else 1)
  divisor=pc13StubGcd(dx dy) dx=dx/divisor dy=dy/divisor
  lo=min(nth(axis a) nth(axis b)) hi=max(nth(axis a) nth(axis b)) ranges=nil
  foreach(seg pc13StubSegments
   when(equal(car(seg) "line") && equal(nth(1 seg) nth(2 row)) && equal(nth(2 seg) nth(3 row)) && equal(nth(3 seg) nth(5 row))
    c=pc13StubGridPoint(car(nth(4 seg))) d=pc13StubGridPoint(cadr(nth(4 seg)))
    cx=car(c)-car(a) cy=cadr(c)-cadr(a) dx2=car(d)-car(a) dy2=cadr(d)-cadr(a)
    when(cx*dy-cy*dx==0 && dx2*dy-dy2*dx==0
     low=max(lo min(nth(axis c) nth(axis d))) high=min(hi max(nth(axis c) nth(axis d)))
     when(low<=high ranges=cons(list(low high) ranges)))))
  ranges=sort(ranges lambda((u v) car(u)<car(v))) reach=lo ok=t
  foreach(r ranges
   when(reach<hi
    if(car(r)>reach then ok=nil else reach=max(reach cadr(r)))))
  ok && reach>=hi))

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
  unless(pc13CuIndexCounts["pin"]==2698 && pc13CuIndexCounts["path"]>0 error("PUB0010 actual-Cu index incomplete\n"))
  t))
procedure(pub0010SourceKey(kind net layer width se) sprintf(nil "%L" list(kind net layer width se)))
procedure(pub0010FrozenStrokeCovered(row)
 let((key path polys same covered)
  covered=nil
  when(equal(nth(4 row) "line")
   key=pub0010SourceKey(nth(4 row) nth(2 row) nth(3 row) nth(5 row) nth(6 row))
   unless(pub0010FrozenKeys[key] error("PUB0010 whole-stroke check outside exact frozen source2068 ledger\n"))
   if(pub0010StrokeCached[key] then covered=pub0010StrokeCovered[key]
   else
    path=axlPathStart(nth(6 row) nth(5 row)) polys=axlPolyFromDB(path ?line2poly t ?endCapType 'ROUND ?holes t)
    when(axlPolyErrorGet() error("PUB0010 original source stroke conversion error\n")) polys=remove(nil polys)
    unless(polys error("PUB0010 frozen original source stroke is empty\n")) covered=t
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
  frozenCount=0 f=infile("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_path_stubs_plan13_v1/SOURCE_FROZEN_REAL_SEGMENTS.ilist")
  while(row=lineread(f) row=car(row) frozenCount=frozenCount+1 pub0010FrozenKeys[pub0010SourceKey(car(row) nth(1 row) nth(2 row) nth(3 row) nth(4 row))]=t) close(f)
  unless(frozenCount==2068 error("PUB0010 source actual segment ledger incomplete\n"))
  groups=pub403Rows("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_path_stubs_plan13_v1/PUB0010_STUB_CANDIDATES.ilist") unless(length(groups)==877 error("PUB0010 exact source branch group count differs\n"))
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
     fprintf(statusPort "%L\n" list(car(group) status candidate)) drain(statusPort)
     when(equal(status "FIT_WHOLE_STROKE_INSIDE_TARGET_REGULAR_PAD") selected=candidate)))
   if(selected then
    fits=fits+1 geometryKey=list(car(selected) cadr(selected) nth(2 selected) nth(3 selected) nth(7 selected) nth(8 selected) nth(9 selected))
    unless(member(geometryKey selectedKeys) selectedKeys=cons(geometryKey selectedKeys) rows=cons(selected rows) fprintf(selectedPort "%L\n" selected) drain(selectedPort))
   else failed=failed+1 fprintf(failedPort "%L\n" group) drain(failedPort))
   printf("PUB0010_STUB_PREFLIGHT_BRANCH %d FIT=%d FAILED=%d\n" fits+failed fits failed))
  close(statusPort) close(selectedPort) close(failedPort)
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  unless(equal(oldDrc axlDBControl('drcEnable)) error("PUB0010 read-only preflight changed DRC mode\n"))
  pub403SnapshotAll(strcat(dir "/PREFLIGHT_AFTER_FULL593_TEXT_PROPS.ilist"))
  f=outfile(strcat(dir "/ALL_SOURCE_BRANCH_PREFLIGHT_COMPLETE.txt"))
  fprintf(f "PUB0010_ALL_SOURCE_BRANCHES_PREFLIGHT_COMPLETE_NO_CREATE_NO_SAVE\nGROUPS=%d\nFIT_GROUPS=%d\nFAILED_GROUPS=%d\nTESTED_CANDIDATES=%d\nUNIQUE_SELECTED_STUBS=%d\nFULL2698_593SYMBOLS_572COMPONENTS_AND_SOURCE_TEXT_PROPS_EXACT\nNATIVE_FULL915_CONNECTION_PARTITION_PROOF_STILL_REQUIRED\n" length(groups) fits failed tested length(rows)) close(f) failed))
