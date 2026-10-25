; SUGGESTED SOURCE ONLY. Not loaded or executed in Allegro.
; Cadence 17.2 native SKILL APIs, no external UI bridge.
; Loading defines procedures only. Call ONLY in a NEW BOARD PRACTICE COPY.
; l6TxnPractice commits a final +2,+1 move in memory; it never saves.
; l6GridPractice explicitly restores the one grid it changes.
; Sources under C:/Program0/Cadence/SPB172/doc/algroskill/:
; 06intedt.html#821370 (transform)
; 17dbtran.html#1076430/#1076368/#1076373/#1076401/#1076340
; 04parmgt.html#1120502/#1120503 (grid)
; 07dbaccs.html#700407 (dbid refresh)

procedure(l6OneSymbolResult(result)
 unless(result error("Lesson06 native transform returned nil\n"))
 if(axlIsDBIDType(result) then result else car(result))
)

procedure(l6FindSymbolAt(point)
 let((found count s)
  axlDBRefreshId(nil)
  count=0
  foreach(s axlDBGetDesign()->symbols
   s=axlDBRefreshId(s)
   when(axlGeoPointsEqual(s->xy point)
    found=s
    count=count+1
   )
  )
  unless(count==1 error("Lesson06 expected one symbol at %L, found %d\n" point count))
  found
 )
)

procedure(l6PrintSnapshot(label sym)
 let((p)
  sym=axlDBRefreshId(sym)
  printf("L6 %s SYMBOL xy=%L rotation=%L mirror=%L pins=%d children=%d\n"
   label sym->xy sym->rotation sym->isMirrored length(sym->pins) length(sym->children))
  foreach(p sym->pins
   p=axlDBRefreshId(p)
   printf("L6 %s PIN number=%L xy=%L rotation=%L relxy=%L relRotation=%L mirror=%L\n"
    label p->number p->xy p->rotation p->relxy p->relRotation p->isMirrored)
  )
  t
 )
)

procedure(l6TxnPractice(sym)
 let((mark status start moved angle mirror r)
  unless(equal(axlDesignType(t) "BOARD") error("Lesson06 requires a practice BOARD\n"))
  sym=axlDBRefreshId(sym)
  start=sym->xy
  angle=sym->rotation
  mirror=sym->isMirrored
  moved=list(car(start)+2.0 cadr(start)+1.0)
  l6PrintSnapshot("BASELINE" sym)
  mark=axlDBTransactionStart()
  unless(mark error("Lesson06 TransactionStart failed\n"))
  status=errset(progn(
   r=axlTransformObject(sym ?move 2.0:1.0 ?allOrNone t)
   sym=axlDBRefreshId(l6OneSymbolResult(r))
   unless(axlGeoPointsEqual(sym->xy moved) error("Lesson06 move mismatch\n"))
   l6PrintSnapshot("MOVED_A" sym)
   unless(axlDBTransactionMark(mark) error("Lesson06 TransactionMark failed\n"))
   r=axlTransformObject(sym ?angle 90.0 ?origin sym->xy ?allOrNone t)
   sym=axlDBRefreshId(l6OneSymbolResult(r))
   l6PrintSnapshot("ROTATED_B" sym)
   unless(axlDBTransactionOops(mark) error("Lesson06 TransactionOops failed\n"))
   sym=l6FindSymbolAt(moved)
   unless(equal(sym->rotation angle) && equal(sym->isMirrored mirror)
    error("Lesson06 Oops did not restore symbol A attributes\n"))
   l6PrintSnapshot("OOPS_TO_A" sym)
   unless(axlDBTransactionRollback(mark) error("Lesson06 TransactionRollback failed\n"))
   mark=nil
   sym=l6FindSymbolAt(start)
   unless(equal(sym->rotation angle) && equal(sym->isMirrored mirror)
    error("Lesson06 Rollback did not restore baseline symbol attributes\n"))
   l6PrintSnapshot("ROLLBACK_TO_BASELINE" sym)
   t
  ) t)
  when(mark axlDBTransactionRollback(mark) mark=nil)
  unless(status error("Lesson06 rollback practice failed; inspect output\n"))
  ; Independent second transaction: retain just a move.
  mark=axlDBTransactionStart()
  unless(mark error("Lesson06 second TransactionStart failed\n"))
  status=errset(progn(
   r=axlTransformObject(sym ?move 2.0:1.0 ?allOrNone t)
   sym=axlDBRefreshId(l6OneSymbolResult(r))
   unless(axlGeoPointsEqual(sym->xy moved) error("Lesson06 committed move mismatch\n"))
   unless(axlDBTransactionCommit(mark) error("Lesson06 TransactionCommit failed\n"))
   mark=nil
   sym=l6FindSymbolAt(moved)
   l6PrintSnapshot("COMMITTED_MOVE" sym)
   t
  ) t)
  when(mark axlDBTransactionRollback(mark) mark=nil)
  unless(status error("Lesson06 commit practice failed; inspect output\n"))
  ; No save here. If saved later, reacquire all dbids after save.
  sym
 )
)

procedure(l6GridPractice(gridName)
 let((g saved status restored)
  g=axlDBGridGet(gridName)
  unless(g error("Lesson06 unknown grid %L\n" gridName))
  saved=list(g->xOrigin g->yOrigin g->xGrids g->yGrids)
  printf("L6 GRID before name=%L settings=%L\n" gridName g)
  status=errset(progn(
   g->xOrigin=0.0
   g->yOrigin=0.0
   g->xGrids=0.05
   g->yGrids=0.05
   unless(axlDBGridSet(g) error("Lesson06 GridSet failed\n"))
   printf("L6 GRID changed name=%L settings=%L\n" gridName axlDBGridGet(gridName))
   t
  ) t)
  ; GridSet is NOT undo-able. Restore explicitly even on a caught error.
  g=axlDBGridGet(gridName)
  g->xOrigin=nth(0 saved)
  g->yOrigin=nth(1 saved)
  g->xGrids=nth(2 saved)
  g->yGrids=nth(3 saved)
  restored=axlDBGridSet(g)
  g=axlDBGridGet(gridName)
  printf("L6 GRID restored name=%L result=%L settings=%L\n" gridName restored g)
  unless(equal(list(g->xOrigin g->yOrigin g->xGrids g->yGrids) saved)
   error("Lesson06 grid settings did not restore\n"))
  unless(status error("Lesson06 grid practice failed before restore\n"))
  t
 )
)

; Suggested native selection steps, after root confirms filter getter semantics:
; oldVis=axlVisibleGet()
; oldEnabled=axlGetFindFilter(nil) ; SDK convention, verify in this version first
; oldButtons=axlGetFindFilter(t)
; axlVisibleDesign(nil)
; axlVisibleLayer("PACKAGE GEOMETRY/PLACE_BOUND_TOP" t)
; axlSetFindFilter(?enabled list("noall" "shapes")
;                  ?onButtons list("noall" "shapes"))
; axlSingleSelectBox(list(-20:-10 20:10)) ; both corners prevent a user prompt
; printf("L6 SELECTION %L\n" axlGetSelSet())
; axlClearSelSet()
; axlSetFindFilter(?enabled cons("noall" oldEnabled)
;                  ?onButtons cons("noall" oldButtons))
; axlVisibleSet(oldVis)
; Source: 05selfnd.html#580450/#580646/#580660,
; 04parmgt.html#1068075/#1068227/#1068430/#1068662,
; official share/pcb/examples/skill/select/ashfindall.il.
; WARNING: GetFindFilter prose reverses t/nil compared with its examples and SDK.
; Set known distinct lists, read both getters, confirm, THEN implement restoration.

; Precision/origin work is a separate NEW EMPTY mm/3 practice, not the old demo:
; - axlDBChangeDesignUnits("millimeters" 3), verify axlDBGetDesignUnits().
; - Compare positive/negative 0.0004/0.0005/0.0006 inputs near zero and near 10mm.
; - Compare exact-grid geometry with a 0.101mm-wide line's half-grid boundaries.
; - Read actual DB coordinates, polygon bbox and vertices; save/reopen after commit.
; - axlDBChangeDesignOrigin(list(2.0 -3.0)) is an OFFSET, not an absolute target.
; - Verify all objects move equally, dimensions/relative positions unchanged;
;   inverse offset list(-2.0 3.0), and save/reopen in a new run if required.
; - paramDesign->xy is the lower-left drawing corner, not a package origin.
; - Do not infer the old mil/0 half-mil discrepancy's cause from a passing mm/3 run.
