; Restore ONLY real source thermal Cu which is missing outside the OLD land.
; Deliberately do not reintroduce the old land inside the approved canonical pad.
load("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_source25_owner_probe_bundle13_v2/public0010_source25_owner_probe_v2.il")
procedure(pc25ExternalSourcePrepare(dir)
 let((f objects row key o p count)
  pub0010Source25Prepare(dir) f=outfile(strcat(dir "/SOURCE25_THERMAL_OWNERSHIP_GUARD.ilist")) count=0
  foreach(item pc25Frozen
   key=car(item) row=nth(1 item)
   objects=pub0010ActualLines[pub0010RouteGeomKey(car(row) nth(2 row) nth(3 row) nth(4 row))]
   unless(length(objects)==1 error("External thermal source line must be unique\n"))
   o=car(objects) p=o->parent
   unless(equal(o->net->name nth(1 row)) && equal(p->objType "path") && equal(p->thermal t) && null(p->symbolEtch) && null(pc25Owned[o]) && null(pc13Props(o)) && null(pc13Props(p)) error("External source25 thermal/net/owner/properties differs\n"))
   fprintf(f "%L\n" list(key row o->?? p->??)) count=count+1)
  close(f) unless(count==25 error("External thermal source count differs\n"))
  f=outfile(strcat(dir "/SOURCE25_EXTERNAL_RESTORE_PREPARED.txt")) fprintf(f "SOURCE25_THERMAL_T_SYMBOL_ETCH_NIL_FULL_PROPERTIES_AND_DETACHED_OLD_PADS_FROZEN\nNO_SOURCE_MUTATION_OR_SAVE\n") close(f) t))
; Proven full-cache exporter uses sprintf DBID keys including user-type pad:.
; Preserve all native attributes, complete figures, global textblocks and props.
load("D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025/dra_audit/export.il")
procedure(pc25CacheSnapshot(path)
 let((f rows count seen line)
  seen=makeTable('pc25CacheExportSeen nil) count=0 f=outfile(path)
  foreach(d axlDBGetDesign()->symdefs draAuditVisit(d f seen) count=count+1)
  unless(count>0 error("External thermal complete cached definitions missing\n"))
  close(f) f=infile(path) rows=nil
  while(gets(line f) rows=cons(line rows)) close(f) sort(rows 'alphalessp)))
procedure(pc25CreateExternal(rows f)
 let((result created actual count key source requested)
  count=0
  foreach(item rows
   key=car(item) source=nth(1 item)
   fprintf(pc25CreateStepPort "KEY_BEGIN %L SOURCE=%L POLYS=%L\n" key source pc25Summary(nth(2 item))) drain(pc25CreateStepPort)
   foreach(poly nth(2 item)
    requested=list(poly) fprintf(pc25CreateStepPort "BEFORE_CREATE %L\n" key) drain(pc25CreateStepPort)
    result=axlDBCreateShape(poly t nth(2 source) nth(1 source) nil)
    fprintf(pc25CreateStepPort "AFTER_CREATE %L RESULT=%L\n" key result) drain(pc25CreateStepPort)
    unless(result && car(result) error("External thermal bounded source shape creation failed\n"))
    created=car(result) axlDBRefreshId(created)
    unless(equal(created->objType "shape") && equal(created->net->name nth(1 source)) && equal(created->layer nth(2 source)) && null(created->shapeIsBoundary) && null(created->shapeBoundary) && null(pc13Props(created)) error("External source thermal board-owned static shape attributes differ\n"))
    actual=axlPolyFromDB(created ?holes t)
    when(axlPolyErrorGet() error("External source thermal created actual Cu conversion error\n")) actual=remove(nil actual)
    when(pc13RingOp(actual requested 'ANDNOT) || pc13RingOp(requested actual 'ANDNOT) error("External source thermal created Cu not exact in BOTH directions\n"))
    pc25WritePolys(key "CREATED_EXTERNAL_SOURCE_THERMAL_ACTUAL_CU" actual)
    fprintf(f "%L\n" list(key source created created->?? "ANDNOT_BOTH_DIRECTIONS_EMPTY")) drain(f) count=count+1)) count))
procedure(pc25RestoreExternalThermal(dir)
 let((f pf pre status row key ps same missing outsideOld foreign cross failures rows keys oldDrc oldFill beforeCache count remaining)
  unless(length(pc25Frozen)==25 error("External thermal source detached globals missing\n"))
  sstatus(fullPrecision t) pub403ReadUnits() oldDrc=axlDBControl('drcEnable) oldFill=axlDBControl('dynamicFillMode)
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  beforeCache=pc25CacheSnapshot(strcat(dir "/BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist"))
  unless(equal(pc25OriginalVias pub0010ViasSnapshot(strcat(dir "/BEFORE_ALL1739_TYPED_VIAS.ilist"))) error("External thermal before all1739 source vias differ\n"))
  pub0010BuildCuIndex() pc25PolyPort=outfile(strcat(dir "/EXTERNAL_THERMAL_CU_NATIVE_POLYGONS.jsonl"))
  f=outfile(strcat(dir "/ALL25_EXTERNAL_THERMAL_PREFLIGHT.ilist")) failures=nil rows=nil keys=nil
  foreach(item pc25Frozen
   key=car(item) row=nth(1 item) ps=nth(2 item) same=nil
   foreach(poly ps same=append(same pc13NearbySameNetCopper(nth(1 row) nth(2 row) poly->bBox)))
   missing=pc13RingOp(ps same 'ANDNOT) outsideOld=pc13RingOp(missing nth(6 item) 'ANDNOT)
   pc25WritePolys(key "SOURCE_MISSING_OUTSIDE_OLD_ACTUAL_REGULAR_PAD" outsideOld)
   cross=nil
   foreach(poly outsideOld
    foreign=pc13NearbyOtherNetCopper(nth(1 row) nth(2 row) poly->bBox)
    cross=append(cross pc13RingOp(list(poly) foreign 'AND)))
   pc25WritePolys(key "PREFLIGHT_OTHER_NET_ACTUAL_CU_INTERSECTION" cross)
   when(cross failures=cons(key failures))
   when(outsideOld
    when(pc13RingOp(outsideOld ps 'ANDNOT) || pc13RingOp(outsideOld nth(6 item) 'AND) error("External thermal source-only/excludes-old-pad hard bound failed\n"))
    keys=cons(key keys) rows=cons(list(key row outsideOld) rows))
   fprintf(f "%L\n" list(key row "ALL_MISSING_SOURCE_CU" pc25Summary(missing) "ONLY_EXTERNAL_SOURCE_CU_TO_RESTORE" pc25Summary(outsideOld) "FOREIGN_CU_INTERSECTION" pc25Summary(cross))) drain(f))
  close(f) keys=reverse(keys) rows=reverse(rows)
  unless(equal(keys '(1 2 4 5 7 8 9 10 11 13 14 15 16 17 18 19 20 21 23 24 25)) error("External thermal exact approved21 key set differs\n"))
  when(failures error("External thermal all25 preflight complete, foreign actual Cu intersections on keys %L; NO_CREATE_NO_SAVE\n" failures))
  f=outfile(strcat(dir "/CREATED_EXTERNAL_THERMAL_SHAPES.ilist"))
  pc25CreateStepPort=outfile(strcat(dir "/CREATE_STEP.txt"))
  fprintf(pc25CreateStepPort "PRE_CREATE_EXACT_ROWS=%d KEYS=%L\n" length(rows) keys) drain(pc25CreateStepPort)
  ; Official axlDBCloak documentation recommends direct calls for debugging.
  ; errset(t) preserves the real first native error; no partial save follows it.
  count=errset(pc25CreateExternal(rows f) t) close(f) close(pc25CreateStepPort)
  unless(count error("External thermal direct create failed; see actual stdout and CREATE_STEP;NO_SAVE\n")) count=car(count)
  unless(count==21 error("External thermal created exact21 source fragments incomplete\n"))
  axlDBRefreshId(nil) pub0010BuildCuIndex() f=outfile(strcat(dir "/ALL25_POST_SOURCE_EXTERNAL_CU_COVERAGE.ilist")) failures=nil
  foreach(item pc25Frozen
   key=car(item) row=nth(1 item) ps=nth(2 item) same=nil
   foreach(poly ps same=append(same pc13NearbySameNetCopper(nth(1 row) nth(2 row) poly->bBox)))
   remaining=pc13RingOp(pc13RingOp(ps same 'ANDNOT) nth(6 item) 'ANDNOT)
   pc25WritePolys(key "AFTER_SOURCE_CU_MISSING_OUTSIDE_OLD_ACTUAL_PAD" remaining)
   when(remaining failures=cons(key failures))
   fprintf(f "%L\n" list(key row "MISSING_OUTSIDE_OLD_ACTUAL_PAD_AFTER" pc25Summary(remaining))) drain(f)) close(f)
  foreach(item rows
   key=car(item) row=nth(1 item) cross=nil
   foreach(poly nth(2 item) cross=append(cross pc13RingOp(list(poly) pc13NearbyOtherNetCopper(nth(1 row) nth(2 row) poly->bBox) 'AND)))
   pc25WritePolys(key "AFTER_CREATED_FRAGMENT_OTHER_NET_ACTUAL_CU_INTERSECTION" cross)
   when(cross failures=cons(key failures)))
  close(pc25PolyPort) when(failures error("External source-only Cu postcoverage/crossnet failed keys %L;NO_SAVE\n" failures))
  unless(equal(beforeCache pc25CacheSnapshot(strcat(dir "/AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist"))) error("External thermal modified a cached package/pad/figure/text definition\n"))
  unless(equal(pc25OriginalVias pub0010ViasSnapshot(strcat(dir "/AFTER_ALL1739_TYPED_VIAS.ilist"))) error("External thermal all1739 source via typed records changed\n"))
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  unless(equal(oldDrc axlDBControl('drcEnable)) && equal(oldFill axlDBControl('dynamicFillMode)) error("External thermal DRC/fill state changed\n"))
  unless(axlSaveDesign(?design strcat(dir "/PUB0010_EXTERNAL_THERMAL_RESTORED.brd") ?noMru t ?noConfirm t) error("External thermal private candidate save failed\n"))
  f=outfile(strcat(dir "/SOURCE25_EXTERNAL_THERMAL_RESTORE_COMPLETE.txt"))
  fprintf(f "SOURCE25_APPROVED21_EXTERNAL_OLD_THERMAL_CU_RESTORED_EXACT\nOLD_LAND_INTERNAL_DIFFERENCES_NOT_REINTRODUCED\nALL25_SOURCE_CU_OUTSIDE_OLD_ACTUAL_REGULAR_PAD_COVERED\nCREATED21_SOURCE_POLYS_NATIVE_ANDNOT_BOTH_DIRECTIONS_EMPTY\nACTUAL_FOREIGN_NET_INTERSECTIONS_ZERO_BEFORE_AND_AFTER\nALL_CACHED_PACKAGE_PAD_FIGURE_GRAPHS_UNCHANGED\nALL1739_SOURCE_TYPED_VIAS_EXACT\nALL2698_593_572_TEXT_PROPERTIES_AND_NAMES_EXACT\nFRESH_SOURCE915_PARTITIONS_CFX_AND_EXTERNAL_CU_FINAL_REVIEW_REQUIRED\n") close(f) count))
