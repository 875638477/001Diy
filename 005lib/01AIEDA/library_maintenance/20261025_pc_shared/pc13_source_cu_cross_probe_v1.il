; READ ONLY: source06B8 -> top-level OPEN targetA965. No create, no save.
load("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_source_cu_v5/all81_restore_actual_source_cu_v5.il")
procedure(pc13CrossDescription(o)
 let((a result)
  a=o->? result=list('OBJECT o 'FIELDS o->??)
  when(member('parent a) && o->parent result=append(result list('PARENT o->parent->??)))
  when(member('component a) && o->component result=append(result list('COMPONENT o->component->??)))
  when(member('symbolEtch a) && o->symbolEtch result=append(result list('SYMBOL_ETCH o->symbolEtch->??)))
  when(member('shapeBoundary a) && o->shapeBoundary result=append(result list('SHAPE_BOUNDARY o->shapeBoundary->??)))
  result))
procedure(pc13CrossSelectedRows()
 let((rows)
  rows=setof(row pc13FrozenSourceCu
   member(car(row) '("(\"line\" \"VDD10_1\" \"ETCH/TOP\" 8.0 (67860 52180) (67860 55860))" "(\"line\" \"USB_FRONT__USB3_RXP4__AD17\" \"ETCH/TOP\" 4.5 (317440 -199780) (317440 -203220))")))
  unless(length(rows)==2 error("Cross diagnostic frozen2 source keys missing\n")) rows))
procedure(pc13CrossSourcePrepare(dir)
 let((f pf row source layer key other ps hit saved count)
  pc13SourceCuPrepare(dir)
  pc13CuStepPort=outfile(strcat(dir "/CROSS_STEP_SOURCE.txt"))
  pc13FrozenCrossRows=nil
  f=outfile(strcat(dir "/SOURCE_OTHER_NET_OBJECTS.ilist"))
  pf=outfile(strcat(dir "/SOURCE_OTHER_NET_INTERSECTIONS.jsonl")) count=0
  foreach(row pc13CrossSelectedRows()
   source=nth(3 row) layer=nth(2 row) key=car(row) saved=nil
   foreach(index pc13CuIndexRows
    when(!equal(nth(1 index) nth(1 row)) && (member(nth(4 index) '("pin" "via")) || equal(nth(2 index) layer))
     when(car(setof(poly source pc13BoxesMeet(poly->bBox nth(3 index))))
      ps=pc13IndexedCuPolys(index layer)
      when(ps
       saved=cons(list(nth(1 index) ps) saved)
       hit=pc13RingOp(source ps 'AND)
       when(hit count=count+1 fprintf(f "%L\n" list(key nth(1 index) nth(4 index) pc13CrossDescription(car(index)))) drain(f)
        pc13RingWrite(pf key sprintf(nil "SOURCE_ALREADY_INTERSECTS_NET_%L_KIND_%s" nth(1 index) nth(4 index)) hit) drain(pf))))))
   pc13FrozenCrossRows=cons(list(row saved) pc13FrozenCrossRows))
  close(f) close(pf)
  f=outfile(strcat(dir "/CROSS_SOURCE_PREPARED.txt")) fprintf(f "SOURCE_KEYS=2\nSOURCE_OTHER_NET_INTERSECTING_OBJECTS=%d\nREAD_ONLY_NO_MUTATION\n" count) close(f)
  pc13CuStep("SOURCE_CROSS_PREPARED_COMPLETE") close(pc13CuStepPort) t))
procedure(pc13CrossTargetProbe(dir)
 let((f pf sf row old source layer key missing same ps hit oldNet newCross count keyHits)
  unless(length(pc13FrozenCrossRows)==2 error("Source cross globals missing; top-level open required\n"))
  sstatus(fullPrecision t)
  pc13AllPinGate("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/TARGET_PINS6521.ilist")
  pc13CuStepPort=outfile(strcat(dir "/CROSS_STEP_TARGET.txt")) pc13BuildCuIndex("TARGET_CROSS")
  f=outfile(strcat(dir "/TARGET_OTHER_NET_OBJECTS.ilist"))
  pf=outfile(strcat(dir "/TARGET_OTHER_NET_INTERSECTIONS.jsonl"))
  sf=outfile(strcat(dir "/CROSS_SUMMARY.tsv")) fprintf(sf "key\tother_net\tkind\thit_polys\tnew_vs_source_same_other_net_polys\n") count=0
  foreach(pair pc13FrozenCrossRows
   row=car(pair) old=cadr(pair) source=nth(3 row) layer=nth(2 row) key=car(row) missing=nil keyHits=0
   foreach(poly source same=pc13NearbySameNetCopper(nth(1 row) layer poly->bBox) missing=append(missing pc13RingOp(list(poly) same 'ANDNOT)))
   pc13RingWrite(pf key "MISSING_SOURCE_CU" missing)
   foreach(index pc13CuIndexRows
    when(!equal(nth(1 index) nth(1 row)) && (member(nth(4 index) '("pin" "via")) || equal(nth(2 index) layer))
     when(car(setof(poly missing pc13BoxesMeet(poly->bBox nth(3 index))))
      ps=pc13IndexedCuPolys(index layer) hit=pc13RingOp(missing ps 'AND)
      when(hit
       keyHits=keyHits+1 count=count+1 oldNet=nil
       foreach(saved old when(equal(car(saved) nth(1 index)) oldNet=append(oldNet cadr(saved))))
       newCross=pc13RingOp(hit oldNet 'ANDNOT)
       fprintf(f "%L\n" list(key nth(1 index) nth(4 index) pc13CrossDescription(car(index)))) drain(f)
       pc13RingWrite(pf key sprintf(nil "TARGET_OTHER_NET_%L_KIND_%s" nth(1 index) nth(4 index)) hit)
       pc13RingWrite(pf key sprintf(nil "NEW_CROSS_VS_SOURCE_OTHER_NET_%L" nth(1 index)) newCross) drain(pf)
       fprintf(sf "%s\t%L\t%s\t%d\t%d\n" key nth(1 index) nth(4 index) length(hit) length(newCross)) drain(sf)))))
   pc13CuStep(sprintf(nil "TARGET_KEY_COMPLETE %s objects=%d" key keyHits)))
  close(f) close(pf) close(sf)
  f=outfile(strcat(dir "/CROSS_DIAGNOSTIC_COMPLETE.txt")) fprintf(f "SOURCE_KEYS=2\nTARGET_INTERSECTING_OTHER_NET_OBJECTS=%d\nSOURCE_BASELINE_SAME_OTHER_NET_UNION_COMPARED\nREAD_ONLY_NO_CREATE_NO_SAVE\n" count) close(f)
  pc13CuStep("TARGET_CROSS_DIAGNOSTIC_COMPLETE") close(pc13CuStepPort) count))
