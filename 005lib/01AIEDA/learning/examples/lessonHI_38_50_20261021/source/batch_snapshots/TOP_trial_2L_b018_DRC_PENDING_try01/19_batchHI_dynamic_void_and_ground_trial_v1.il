hiGroundTrialHealthCount=0
procedure(hiShape(f id net layer points dynamic voids)
 let((shape ret geometry)
  geometry=if(equal(points "ROUTE_KEEPIN") then car(axlPolyFromDB(axlDBGetDesign()->keepinRoute)) else hiClosedPath(points))
  shape=axlDBCreateOpenShape(geometry t strcat("ETCH/" layer) net)
  unless(shape error("Cannot create actualshapeoutline\n"))
  unless(dynamic foreach(v voids unless(axlDBCreateVoid(shape hiClosedPath(v)) error("Cannot create staticvoid\n"))))
  ret=axlDBCreateCloseShape(shape t) unless(ret error("Cannot close actualshapeoutline\n")) shape=car(ret)
  when(dynamic shape=axlShapeChangeDynamicType(shape t t) unless(shape error("Cannot convert outline todynamicBOUNDARY\n")))
  hiReg(id "shape" shape)
  when(dynamic
   foreach(v voids hiVoid(f id v))
   shape=caddr(assoc(id hiRegistry))
   unless(equal(axlShapeDynamicUpdate(shape t) 0) error("Dynamicpermanentvoid shapeupdate failed\n")))
  fprintf(f "HI_SHAPE_SUPPORTED_DYNAMIC_VOID_ORDER id=%L dynamic=%L requestedVoidCount=%d actual=%L\n" id dynamic length(voids) shape->??)
  unless(length(shape->voids)==length(voids) error("New globalpermanentvoid count differs\n"))
  foreach(v voids unless(length(setof(h shape->voids hiPolygonMatches(h v)))==1 error("Newglobalpermanentvoid polygon differs\n"))) shape))
procedure(hiRetireReplacedTopReferences(f)
 let((kept)
  kept=nil
  foreach(r hiDeferredReferences
   if(equal(cadr(r) "TOP") then
    fprintf(f "HI_TOP_OLD_MOTHER_INTENTIONALLY_REPLACED_BY_SINGLE_GLOBAL definition=%L\n" r)
   else kept=append(kept list(r))))
  hiDeferredReferences=kept t))
procedure(hiGroundTrialHealth(out expectedPins expectedVias)
 let((f graph pins vias missing shapes orphan ood orphanBranches allpins bg terminals)
  hiGroundTrialHealthCount=hiGroundTrialHealthCount+1
  f=outfile(sprintf(nil "%s/hi_all_ground_common_trial_%d.txt" out hiGroundTrialHealthCount))
  unless(equal(axlShapeDynamicUpdate(nil t) 0) error("Groundtrialforcefill failed\n")) axlDBRefreshId(nil)
  graph=gConnectedObjects(gPin("C1" "2")) pins=0 vias=0 missing=0 shapes=0 orphan=0 ood=0 orphanBranches=0 allpins=nil
  foreach(c axlDBGetDesign()->components
   foreach(p c->symbol->pins
    when(p->net && member(p->net axlDBGetDesign()->nets) allpins=cons(p allpins))
    when(p->net && equal(p->net->name "GND")
     pins=pins+1
     fprintf(f "ALL_GND_PHYSICAL_PIN ref=%L number=%L xy=%L globalC1_2Reached=%L\n" c->name p->number p->xy if(member(p graph) then t else nil))
     unless(member(p graph) missing=missing+1))))
  foreach(v hiAllVias()
   when(v->net && equal(v->net->name "GND")
    vias=vias+1 fprintf(f "ALL_GND_ACTUAL_VIA xy=%L padstack=%L commonC1_2=%L\n" v->xy v->name if(member(v graph) then t else nil))
    unless(member(v graph) missing=missing+1)))
  foreach(s axlDBGetShapes("ETCH")
   when(s->net && equal(s->net->name "GND") && s->fill && !s->shapeIsBoundary
    shapes=shapes+1
    unless(member(s graph) orphan=orphan+1 fprintf(f "ACTUAL_GND_SHAPE_WITHOUT_COMMON=%L polygon=%L\n" s->?? car(axlPolyFromDB(s))->vertices))))
  foreach(b axlDBGetShapes("BOUNDARY")
   when(b->fillOOD ood=ood+1 fprintf(f "OUT_OF_DATE_DYNAMIC_BOUNDARY=%L\n" b->??)))
  foreach(net axlDBGetDesign()->nets
   foreach(branch net->branches
    bg=nil
    foreach(child branch->children foreach(obj gConnectedObjects(child) unless(member(obj bg) bg=cons(obj bg))))
    terminals=setof(p allpins member(p bg))
    unless(terminals orphanBranches=orphanBranches+1 fprintf(f "NO_TERMINAL_BRANCH_TRIAL net=%L branch=%L graph=%L\n" net->name branch->?? bg))))
  fprintf(f "GROUND_TRIAL_SUMMARY pins=%d expectedPins=%d vias=%d expectedVias=%d missing=%d actualGroundShapes=%d shapesWithoutCommon=%d outOfDate=%d allNetTerminalFreeBranches=%d drcEnable=%L designModes=%L\n" pins expectedPins vias expectedVias missing shapes orphan ood orphanBranches axlDBControl('drcEnable) axlCNSDesignModeGet('all)) drain(f)
  unless(pins==expectedPins && vias==expectedVias && missing==0 && orphan==0 && ood==0 && orphanBranches==0 progn(gSnapshot(out hiDiagnosticLibrary) hiNetworkInventory(out) hiExtraRead(out) hiShapeBoundaryRead(out) hiRouteRoles(out) hiBranchAudit(out) error("Groundtrial actualcommon/fill/orphan health failed; preserveactualdiagnostics, noSave\n")))
  fprintf(f "GROUND_TRIAL_ALL_POSITIVE_COMMON_HEALTH_COMPLETE_NOT_FINAL_REFERENCE_CERTIFICATION\n") close(f) t))
