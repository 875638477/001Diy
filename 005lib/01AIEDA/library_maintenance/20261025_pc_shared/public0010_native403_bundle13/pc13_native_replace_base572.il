; Source/target native full package signatures are bound outside this IL.
; This ledger gate permits only frozen per-number world coordinates/target pad name,
; with exact net/mechanical/through/exploded status and no additional pins.
procedure(pc13LoadExpected(path)
 let((f row)
  pc13Expected=makeTable('pc13Expected nil) f=infile(path)
  unless(f error("V13 expected pins missing\n"))
  while(row=lineread(f) row=car(row) unless(length(row)==2 error("V13 expected pin format invalid\n")) pc13Expected[car(row)]=cadr(row))
  close(f) t))
procedure(pc13ExpectedPins(ref s)
 let((expected row p used)
  expected=pc13Expected[ref] used=nil
  unless(expected && length(expected)==length(s->pins) error("V13 expected pin count %s\n" ref))
  foreach(row expected
   p=car(setof(x s->pins !member(x used) && equal(x->number car(row)) && equal(x->xy cadr(row))))
   unless(p error("V13 expected pin missing %s %s\n" ref car(row)))
   used=cons(p used)
   unless(equal(p->xy cadr(row)) && equal(p->net->name nth(2 row)) && equal(p->isMech nth(3 row)) && equal(p->isThrough nth(4 row)) && equal(p->name nth(5 row)) && null(p->isExploded) error("V13 pin ledger fields changed %s %s\n" ref car(row))))
  t))
; V13 source-bound package-name migration. Prepared, not yet natively tested.
; The caller must verify input/library SHA and own the isolated CAD process.
; Never invoke on a user session or source12. No output overwrite checks exist in SKILL:
; enforce fresh output paths in the owning PowerShell/Python runner.
procedure(pc13Comp(ref) car(setof(x axlDBGetDesign()->components equal(x->name ref))))
procedure(pc13Props(o) sort(axlDBGetProperties(o '("user" "allegro")) lambda((a b) alphalessp(sprintf(nil "%L" a) sprintf(nil "%L" b)))))
procedure(pc13TextSnapshot(s)
 let((out ch)
  out=nil
  foreach(ch s->children
   when(equal(ch->objType "text")
    out=cons(list(ch->text ch->xy ch->rotation ch->isMirrored ch->justify ch->layer ch->textBlock pc13Props(ch)) out)))
  reverse(out)))
procedure(pc13TextSorted(s) sort(foreach(mapcar r pc13TextSnapshot(s) sprintf(nil "%L" r)) 'alphalessp))
procedure(pc13PinSnapshot(s)
 sort(foreach(mapcar p s->pins sprintf(nil "%L" list(p->number p->xy p->isMech p->isThrough p->net->name p->isExploded))) 'alphalessp))
procedure(pc13Pose(s) list(s->xy s->rotation s->isMirrored))
procedure(pc13TextRestore(s records)
 let((texts used rec ch orient result extra oldprops)
  texts=setof(x s->children equal(x->objType "text")) used=nil
  foreach(rec records
   ch=car(setof(x texts !member(x used) && equal(x->layer nth(5 rec))))
   orient=make_axlTextOrientation(?textBlock nth(6 rec) ?rotation nth(2 rec) ?mirrored nth(3 rec) ?justify nth(4 rec))
   if(ch then
    used=cons(ch used)
    unless(axlDBChangeText(ch car(rec) orient) error("V13 text change failed\n"))
    axlDBRefreshId(ch)
    unless(axlTransformObject(ch ?move list(xCoord(cadr(rec))-xCoord(ch->xy) yCoord(cadr(rec))-yCoord(ch->xy))) error("V13 text move failed\n"))
   else
    result=axlDBCreateText(car(rec) cadr(rec) orient nth(5 rec) s)
    unless(result error("V13 text create failed\n"))
    ch=car(result)
    when(listp(ch) ch=car(ch))
   )
   ; Property mismatches are fatal: do not silently discard or invent invisible properties.
   ; Rendering fields above are restored. The full visible property list must already match.
   unless(equal(pc13Props(ch) nth(7 rec)) error("V13 text property mismatch after restore\n"))
  )
  foreach(extra texts unless(member(extra used) unless(axlDeleteObject(extra) error("V13 extra replacement text removal failed\n"))))
  axlDBRefreshId(s)
  foreach(ch s->children axlDBRefreshId(ch))
  t))
procedure(pc13ReadRows(planTSV)
 let((f line fields rows ref from target delta)
  f=infile(planTSV) unless(f error("V13 ref map missing\n"))
  gets(line f)
  unless(equal(parseString(line "\t\r\n") '("refdes" "from_package" "target_package" "delta")) error("V13 ref map header invalid\n"))
  rows=nil
  while(gets(line f)
   fields=parseString(line "\t\r\n")
   unless(length(fields)==4 error("V13 ref map row malformed\n"))
   ref=car(fields) from=cadr(fields) target=caddr(fields) delta=atof(cadddr(fields))
   unless(zerop(delta) error("V13 has no approved rotation changes\n"))
   when(member(ref foreach(mapcar r rows car(r))) error("V13 duplicate ref\n"))
   unless(equal(from target) rows=cons(list(ref from target delta) rows))
  ) close(f) reverse(rows)))
procedure(pc13WriteMetadata(outDir label)
 let((f pf tf c s p ch)
  f=outfile(strcat(outDir "/components_" label ".tsv"))
  pf=outfile(strcat(outDir "/pins_" label ".tsv"))
  tf=outfile(strcat(outDir "/texts_full_" label ".ilist"))
  foreach(c axlDBGetDesign()->components
   s=c->symbol
   fprintf(f "%L\t%L\t%L\t%L\t%L\t%L\n" c->name c->package s->name s->definition->name pc13Pose(s) pc13Props(c->compdef))
   foreach(p s->pins fprintf(pf "%L\t%L\n" c->name p->??))
   foreach(ch s->children when(equal(ch->objType "text") fprintf(tf "%L\n" list(c->name ch->?? pc13Props(ch) axlGetParam(strcat("paramTextBlock:" ch->textBlock))->??))))
  ) close(f) close(pf) close(tf) t))

; Each shape cloak closes before checkpoint/save. No transaction crosses its boundary.
; Do not retain DBIDs across cloak. Every row resolves its component freshly by ref.
procedure(pc13ReplaceOne(row f)
 let((ref from target c s pose pins texts props oldalt)
  ref=car(row) from=cadr(row) target=caddr(row) c=pc13Comp(ref) s=c->symbol
  pose=pc13Pose(s) texts=pc13TextSnapshot(s) props=pc13Props(c->compdef)
  oldalt=assoc('ALT_SYMBOLS props)
  unless(axlDBAddProp(list(c->compdef) list("ALT_SYMBOLS" strcat("(" target ")"))) error("V13 ALT_SYMBOLS failed %s\n" ref))
  unless(axlAltSymbolReplace(c target) error("V13 replace failed %s\n" ref))
  axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol
  pc13TextRestore(s texts)
  if(oldalt then axlDBAddProp(list(c->compdef) list("ALT_SYMBOLS" cadr(oldalt))) else axlDBDeleteProp(c->compdef "ALT_SYMBOLS"))
  axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol
  unless(equal(pose pc13Pose(s)) error("V13 pose changed %s\n" ref))
  pc13ExpectedPins(ref s)
  unless(equal(sort(foreach(mapcar r texts sprintf(nil "%L" r)) 'alphalessp) pc13TextSorted(s)) error("V13 text changed %s\n" ref))
  unless(equal(props pc13Props(c->compdef)) error("V13 component props/ALT changed %s\n" ref))
  fprintf(f "%s\t%s\t%s\tTRUE\n" ref from target) drain(f)
  t))
procedure(pc13ReplaceRows(rows f)
 let((count row)
  count=0
  foreach(row rows pc13ReplaceOne(row f) count=count+1)
  count))
procedure(pc13Replace(planTSV outDir outputBoard publicPsmPath publicPadPath maxCount expectedPinsFile)
 let((rows pending selected row c s ref from target f snapshot count skipped chunk result oldDrc checkpoint)
  unless(length(axlDBGetDesign()->components)==572 error("V13 expected572 placed components\n"))
  oldDrc=axlDBControl('drcEnable)
  unless(axlSetVariable("psmpath" publicPsmPath) error("V13 PSMPATH failed\n"))
  unless(axlSetVariable("padpath" publicPadPath) error("V13 PADPATH failed\n"))
  pc13LoadExpected(expectedPinsFile) rows=pc13ReadRows(planTSV) pending=nil skipped=0
  ; Safe checkpoint resumption: only original or already-ledger-approved target names.
  foreach(row rows
   ref=car(row) from=cadr(row) target=caddr(row) c=pc13Comp(ref)
   unless(c && c->symbol error("V13 source component missing %s\n" ref))
   unless(member(upperCase(c->package) list(upperCase(from) upperCase(target))) error("V13 source package guard failed %s\n" ref))
   if(equal(upperCase(c->symbol->name) upperCase(target)) then
    pc13ExpectedPins(ref c->symbol) skipped=skipped+1
   else
    unless(equal(upperCase(c->symbol->name) upperCase(from)) error("V13 source symbol guard failed %s\n" ref))
    pending=cons(row pending)))
  pending=reverse(pending) selected=nil count=0
  foreach(row pending
   when(maxCount<=0 || count<maxCount selected=cons(row selected) count=count+1))
  selected=reverse(selected) count=0
  pc13WriteMetadata(outDir "before")
  snapshot=outfile(strcat(outDir "/original_all_text_snapshot.ilist"))
  foreach(c axlDBGetDesign()->components fprintf(snapshot "%L\n" list(c->name pc13TextSnapshot(c->symbol)))) close(snapshot)
  f=outfile(strcat(outDir "/applied.tsv"))
  fprintf(f "refdes\tfrom_package\ttarget_package\tpose_pin_text_preserved\n")
  while(selected
   chunk=nil
   while(selected && length(chunk)<100 chunk=cons(car(selected) chunk) selected=cdr(selected))
   chunk=reverse(chunk)
   printf("PC13_CLOAK_BEGIN completed=%d batch=%d skipped=%d\n" count length(chunk) skipped)
   result=axlDBCloak('pc13ReplaceRows(chunk f) 'shape)
   unless(result && result==length(chunk) error("V13 shape cloak incomplete %L\n" result))
   unless(equal(oldDrc axlDBControl('drcEnable)) error("V13 source drcEnable state changed\n"))
   count=count+result
   printf("PC13_CLOAK_END completed=%d source_drcEnable=%L\n" count oldDrc)
   when(mod(count 100)==0
    checkpoint=sprintf(nil "%s/CHECKPOINT_%04d.brd" outDir count+skipped)
    unless(axlSaveDesign(?design checkpoint ?noMru t ?noConfirm t) error("V13 checkpoint save failed\n"))
    printf("PC13_CHECKPOINT %s\n" checkpoint))
  )
  close(f) pc13WriteMetadata(outDir "after")
  unless(equal(oldDrc axlDBControl('drcEnable)) error("V13 final drcEnable state changed\n"))
  unless(axlSaveDesign(?design outputBoard ?noMru t ?noConfirm t) error("V13 final save failed\n"))
  printf("PC13_REPLACE_COMPLETE changed=%d already_target=%d original_drc=%L final_drc=%L\n" count skipped oldDrc axlDBControl('drcEnable))
  count))

procedure(pc13RestoreAfterNetrev(snapshotPath outDir outputBoard)
 let((f row ref c expected count)
  f=infile(snapshotPath) unless(f error("V13 snapshot missing\n")) count=0
  while(row=lineread(f)
   row=car(row) ref=car(row) expected=cadr(row) c=pc13Comp(ref)
   unless(c && c->symbol error("V13 postnetrev ref missing %s\n" ref))
   pc13TextRestore(c->symbol expected)
   unless(equal(sort(foreach(mapcar r expected sprintf(nil "%L" r)) 'alphalessp) pc13TextSorted(c->symbol)) error("V13 postnetrev text mismatch %s\n" ref))
   count=count+1)
  close(f) unless(count==572 error("V13 text snapshot coverage mismatch\n"))
  pc13WriteMetadata(outDir "restored")
  unless(axlSaveDesign(?design outputBoard ?noMru t ?noConfirm t) error("V13 restore save failed\n")) count))
procedure(pc13Readback(snapshotPath approvedRefTSV outDir expectedPinsFile)
 let((f row ref c expected count rows rr)
  pc13LoadExpected(expectedPinsFile)
  f=infile(snapshotPath) count=0
  while(row=lineread(f)
   row=car(row) ref=car(row) expected=cadr(row) c=pc13Comp(ref)
   unless(c && c->symbol error("V13 readback ref missing\n"))
   unless(equal(sort(foreach(mapcar r expected sprintf(nil "%L" r)) 'alphalessp) pc13TextSorted(c->symbol)) error("V13 readback text mismatch %s\n" ref)) count=count+1)
  close(f) unless(count==572 error("V13 readback coverage mismatch\n"))
  rows=pc13ReadRows(approvedRefTSV)
  foreach(rr rows c=pc13Comp(car(rr)) unless(equal(upperCase(c->package) upperCase(caddr(rr))) && equal(upperCase(c->symbol->name) upperCase(caddr(rr))) && equal(upperCase(c->symbol->definition->name) upperCase(caddr(rr))) error("V13 readback package/symbol mismatch %s\n" car(rr))))
  foreach(c axlDBGetDesign()->components pc13ExpectedPins(c->name c->symbol))
  pc13WriteMetadata(outDir "reopened") count))