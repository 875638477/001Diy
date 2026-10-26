; Root finite decision27: restore original21 real board paths, not cropped shapes.
; Whole source thermal path Cu may overlap the old land; no old land is cloned.
load("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_external_thermal_restore_bundle13_v2/public0010_external_thermal_restore_v2.il")
procedure(pc25OriginalThermalPrepare(dir)
 let((f row key objects o parent rp converted ps)
  pc25ExternalSourcePrepare(dir) pc25OriginalPaths=nil
  f=outfile(strcat(dir "/SOURCE21_ACTUAL_PATH_RPATH_PROOF.ilist"))
  foreach(item pc25Frozen
   key=car(item)
   when(member(key '(1 2 4 5 7 8 9 10 11 13 14 15 16 17 18 19 20 21 23 24 25))
    row=nth(1 item) ps=nth(2 item)
    objects=pub0010ActualLines[pub0010RouteGeomKey(car(row) nth(2 row) nth(3 row) nth(4 row))]
    unless(length(objects)==1 error("Original thermal exact source line not unique\n")) o=car(objects) parent=o->parent
    unless(equal(parent->objType "path") && parent->nSegs==1 && equal(parent->thermal t) && null(parent->symbolEtch) && null(pc13Props(parent)) && null(pc13Props(o)) error("Original21 source native parent/path/owner/props differs\n"))
    rp=axlDB2Path(parent) unless(rp error("Original thermal official axlDB2Path failed\n"))
    converted=axlPolyFromDB(rp ?line2poly t ?endCapType 'ROUND ?holes t)
    when(axlPolyErrorGet() error("Original thermal detached r_path Cu conversion failed\n")) converted=remove(nil converted)
    when(pc13RingOp(converted ps 'ANDNOT) || pc13RingOp(ps converted 'ANDNOT) error("Original thermal detached path did not preserve source width/caps/exact Cu\n"))
    pc25OriginalPaths=cons(list(key row rp ps) pc25OriginalPaths)
    fprintf(f "%L\n" list(key row parent->?? o->?? "DETACHED_RPATH_VS_SOURCE_NATIVE_ANDNOT_BOTH_EMPTY")) drain(f)))
  close(f) pc25OriginalPaths=reverse(pc25OriginalPaths) unless(length(pc25OriginalPaths)==21 error("Original21 source r_path count differs\n"))
  f=outfile(strcat(dir "/SOURCE21_ORIGINAL_THERMAL_PATHS_PREPARED.txt")) fprintf(f "ORIGINAL21_BOARD_THERMAL_PATHS_NATIVE_RPATH_AND_FULL_CU_EXACT\nNO_OLD_LAND_CLONE_NO_SOURCE_SAVE\n") close(f) t))
procedure(pc25CollectBottomPowerCu()
 let((result ps)
  pub0010BuildCuIndex() result=nil
  foreach(index pc13CuIndexRows
   when(member(nth(1 index) '("1V" "1V8" "3V3")) && (member(nth(4 index) '("pin" "via")) || equal(nth(2 index) "ETCH/BOTTOM"))
    ps=pc13IndexedCuPolys(index "ETCH/BOTTOM")
    when(ps result=cons(list(nth(1 index) nth(3 index) ps) result))))
  foreach(net '("1V" "1V8" "3V3") unless(exists(r result equal(car(r) net)) error("Original thermal actual power-Cu index missing net %s\n" net)))
  reverse(result)))
procedure(pc25PowerNear(rows net box)
 let((ps) ps=nil foreach(r rows when(equal(car(r) net) && pc13BoxesMeet(nth(1 r) box) ps=append(ps nth(2 r)))) ps))
procedure(pc25OriginalSourceNear(net box)
 let((ps) ps=nil foreach(r pc25OriginalPaths when(equal(nth(1 nth(1 r)) net) foreach(p nth(3 r) when(pc13BoxesMeet(p->bBox box) ps=cons(p ps))))) ps))
procedure(pc25CreateOriginalPaths(rows f)
 let((result objects actual source count key)
  count=0
  foreach(item rows
   key=car(item) source=nth(1 item)
   fprintf(pc25CreateStepPort "BEFORE_ORIGINAL_PATH %L SOURCE=%L\n" key source) drain(pc25CreateStepPort)
   result=axlDBCreatePath(nth(2 item) nth(2 source) nth(1 source))
   fprintf(pc25CreateStepPort "AFTER_ORIGINAL_PATH %L RESULT=%L\n" key result) drain(pc25CreateStepPort)
   unless(result && car(result) error("Original source thermal native path creation failed\n")) objects=car(result)
   unless(listp(objects) objects=list(objects)) actual=nil
   foreach(o objects
    axlDBRefreshId(o)
    unless(equal(o->net->name nth(1 source)) && equal(o->layer nth(2 source)) && null(o->symbolEtch) && null(pc13Props(o)) error("Original source recreated path net/layer/board-owner/properties differs\n"))
    actual=append(actual axlPolyFromDB(o ?holes t ?endCapType 'ROUND))
    when(axlPolyErrorGet() error("Original source recreated path actual copper conversion error\n"))
    fprintf(f "%L\n" list(key source o o->?? "NEW_NATIVE_THERMAL_FLAG" o->thermal "BOARD_OWNED_PATH_NOT_PUBLIC_LAND")) drain(f))
   actual=remove(nil actual) unless(actual error("Original source recreated paths empty actual Cu\n"))
   pc25WritePolys(key "CREATED_OR_MERGED_ORIGINAL_PATH_ACTUAL_CU" actual)
   count=count+1) count))
procedure(pc25CreateOriginalPathsChecked()
 let((r) r=errset(pc25CreateOriginalPaths(pc25OriginalPaths pc25OriginalCreatePort) t)
  unless(r error("Original source thermal native creation failed; see CREATE_STEP and actual stdout\n")) car(r)))
procedure(pc25OriginalThermalRestore(dir)
 let((oldDrc oldFill beforeCache beforeCu afterCu f keys failures cross row key ps same foreign count extra missing net index beforeNear sourceNear afterNear)
  unless(length(pc25OriginalPaths)==21 error("Original thermal frozen21 source paths absent\n"))
  sstatus(fullPrecision t) pub403ReadUnits() oldDrc=axlDBControl('drcEnable) oldFill=axlDBControl('dynamicFillMode)
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  beforeCache=pc25CacheSnapshot(strcat(dir "/BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist"))
  unless(equal(pc25OriginalVias pub0010ViasSnapshot(strcat(dir "/BEFORE_ALL1739_TYPED_VIAS.ilist"))) error("Original thermal before all1739 source vias differ\n"))
  beforeCu=pc25CollectBottomPowerCu() pc25PolyPort=outfile(strcat(dir "/ORIGINAL21_THERMAL_CU_NATIVE_POLYGONS.jsonl"))
  f=outfile(strcat(dir "/SOURCE21_FULL_PATH_FOREIGN_CU_PREFLIGHT.ilist")) failures=nil keys=nil
  foreach(item pc25OriginalPaths
   key=car(item) row=nth(1 item) ps=nth(3 item) cross=nil keys=cons(key keys)
   foreach(p ps cross=append(cross pc13RingOp(list(p) pc13NearbyOtherNetCopper(nth(1 row) nth(2 row) p->bBox) 'AND)))
   pc25WritePolys(key "FULL_ORIGINAL_SOURCE_THERMAL_PATH" ps)
   pc25WritePolys(key "BEFORE_SOURCE21_OTHER_NET_INTERSECTION" cross)
   fprintf(f "%L\n" list(key row "SOURCE_FULL_PATH" pc25Summary(ps) "FOREIGN_ACTUAL_CU" pc25Summary(cross))) drain(f)
   when(cross failures=cons(key failures))) close(f)
  unless(equal(reverse(keys) '(1 2 4 5 7 8 9 10 11 13 14 15 16 17 18 19 20 21 23 24 25)) error("Original thermal exact finite21 key set differs\n"))
  when(failures error("Original full thermal path actual foreign Cu intersects keys %L;NO_CREATE_NO_SAVE\n" failures))
  pc25OriginalCreatePort=outfile(strcat(dir "/RECREATED_SOURCE21_NATIVE_PATHS.ilist")) pc25CreateStepPort=outfile(strcat(dir "/CREATE_STEP.txt"))
  count=axlDBCloak('pc25CreateOriginalPathsChecked() 'shape) close(pc25OriginalCreatePort) close(pc25CreateStepPort)
  unless(count==21 error("Original source21 thermal creation incomplete;NO_SAVE\n"))
  axlDBRefreshId(nil) afterCu=pc25CollectBottomPowerCu()
  f=outfile(strcat(dir "/FULL_THREE_NET_BOTTOM_CU_UNION_EQUIVALENCE.ilist")) failures=nil index=0
  ; Exact global3-net relation AFTER = BEFORE UNION SOURCE21, per native polygon.
  ; Bboxes are query indexes only; every acceptance uses native ANDNOT.
  foreach(r afterCu
   net=car(r)
   foreach(p nth(2 r)
    index=index+1 beforeNear=pc25PowerNear(beforeCu net p->bBox) sourceNear=pc25OriginalSourceNear(net p->bBox)
    extra=pc13RingOp(list(p) append(beforeNear sourceNear) 'ANDNOT)
    fprintf(f "%L\n" list("AFTER_MINUS_BEFORE_AND_SOURCE21" index net pc25Summary(extra))) drain(f)
    when(extra failures=cons(list("NEW_CU_OUTSIDE_ORIGINAL_OR_PREEXISTING" index net) failures)) ))
  foreach(r beforeCu
   net=car(r)
   foreach(p nth(2 r)
    index=index+1 afterNear=pc25PowerNear(afterCu net p->bBox) missing=pc13RingOp(list(p) afterNear 'ANDNOT)
    fprintf(f "%L\n" list("PREEXISTING_CU_MINUS_AFTER" index net pc25Summary(missing))) drain(f)
    when(missing failures=cons(list("PREEXISTING_CU_LOST" index net) failures))))
  foreach(item pc25OriginalPaths
   key=car(item) row=nth(1 item) ps=nth(3 item) missing=nil cross=nil
   foreach(p ps
    missing=append(missing pc13RingOp(list(p) pc25PowerNear(afterCu nth(1 row) p->bBox) 'ANDNOT))
    cross=append(cross pc13RingOp(list(p) pc13NearbyOtherNetCopper(nth(1 row) nth(2 row) p->bBox) 'AND)))
   pc25WritePolys(key "AFTER_ORIGINAL_SOURCE21_PATH_CU_STILL_MISSING" missing)
   pc25WritePolys(key "AFTER_SOURCE21_OTHER_NET_INTERSECTION" cross)
   fprintf(f "%L\n" list("SOURCE21_PATH_MINUS_AFTER" key pc25Summary(missing) "FOREIGN_ACTUAL_CU" pc25Summary(cross))) drain(f)
   when(missing || cross failures=cons(list("SOURCE_PATH_COVERAGE_OR_FOREIGN" key) failures)))
  ; All original25 paths are covered outside old pads; four inside-only land
  ; changes remain canonical. No old pad shape is recreated anywhere.
  foreach(item pc25Frozen
   key=car(item) row=nth(1 item) missing=nil
   foreach(p nth(2 item) missing=append(missing pc13RingOp(list(p) pc25PowerNear(afterCu nth(1 row) p->bBox) 'ANDNOT)))
   extra=pc13RingOp(missing nth(6 item) 'ANDNOT)
   fprintf(f "%L\n" list("ALL25_MISSING_OUTSIDE_OLD_ACTUAL_PAD_AFTER" key pc25Summary(extra))) drain(f)
   pc25WritePolys(key "AFTER_ALL25_MISSING_OUTSIDE_OLD_ACTUAL_PAD" extra)
   when(extra failures=cons(list("ORIGINAL_OUTSIDE_PAD_CU_LOSS" key) failures)))
  close(f) close(pc25PolyPort) when(failures error("Original thermal exact whole three-net union/source/foreign postproof failed %L;NO_SAVE\n" failures))
  unless(equal(beforeCache pc25CacheSnapshot(strcat(dir "/AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist"))) error("Original thermal modified cached PSM/PAD/figure/textblock/property graphs\n"))
  unless(equal(pc25OriginalVias pub0010ViasSnapshot(strcat(dir "/AFTER_ALL1739_TYPED_VIAS.ilist"))) error("Original thermal all1739 typed source via records changed\n"))
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  unless(equal(oldDrc axlDBControl('drcEnable)) && equal(oldFill axlDBControl('dynamicFillMode)) error("Original thermal DRC/fill mode changed\n"))
  unless(axlSaveDesign(?design strcat(dir "/PUB0010_ORIGINAL_THERMAL_RESTORED.brd") ?noMru t ?noConfirm t) error("Original thermal private candidate save failed\n"))
  f=outfile(strcat(dir "/SOURCE21_ORIGINAL_THERMAL_RESTORE_COMPLETE.txt"))
  fprintf(f "FINITE_ORIGINAL21_REAL_BOARD_THERMAL_PATHS_RECREATED\nROOT_DECISION27_ALLOWS_ORIGINAL_PATH_CU_INSIDE_OLD_PAD_NOT_WHOLE_OLD_LAND\nFULL_BOTTOM_1V_1V8_3V3_AFTER_CU_EQUALS_BEFORE_UNION_SOURCE21_EXACT\nNO_PREEXISTING_CU_LOSS_NO_CU_OUTSIDE_SOURCE21_PLUS_PREEXISTING\nALL25_SOURCE_THERMAL_CU_OUTSIDE_OLD_REGULAR_PAD_COVERED\nSOURCE21_FOREIGN_ACTUAL_CU_INTERSECTION_ZERO_BEFORE_AND_AFTER\nALL_CACHED_PSM_PAD_FIGURE_TEXTBLOCK_PROPERTY_GRAPHS_EXACT\nALL2698_593_572_AND_ORIGINAL1739_TYPED_VIAS_EXACT\nRECREATED_BOARD_PATH_NATIVE_THERMAL_FLAGS_RECORDED_NOT_CLAIMED_DYNAMIC\nFRESH_FULL915_AND_CFX_REQUIRED_BEFORE_FINAL_APPROVAL\n") close(f) count))
