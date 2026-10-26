; Read-only complete axlFill defstruct: official algroskill/03dbcre8.html axlFill.
; The only defined fields are origin, width, spacing, angle. No pointer omission.
procedure(pub13FillVisit(o f seen)
 let((r c geom)
  when(o && !seen[o]
   seen[o]=t
   when(o->fill
    geom=sprintf(nil "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L"
     o->objType o->layer o->xy o->bBox o->startEnd o->width o->radius o->isClockwise o->vertices o->text o->rotation o->isMirrored o->name o->number o->isMech o->isThrough o->font o->fill o->isHole o->isRect o->shapeIsBoundary o->nSegs o->justify o->textBlock o->isMirrored)
    fprintf(f "(fillObject %L (complete_axlFill_structs" geom)
    if(listp(o->fill) then
     foreach(r o->fill fprintf(f " (origin %L width %L spacing %L angle %L)" r->origin r->width r->spacing r->angle))
    else fprintf(f " (literal_fill %L)" o->fill))
    fprintf(f "))\n"))
   foreach(c o->children pub13FillVisit(c f seen))
   foreach(c o->pins pub13FillVisit(c f seen))
   foreach(c o->segments pub13FillVisit(c f seen))
   foreach(c o->voids pub13FillVisit(c f seen))
   foreach(c o->shapeAuto pub13FillVisit(c f seen)))))
procedure(pub13FillStructReadOnly(dir)
 let((f d n b s o seen vis enabled buttons selected)
  sstatus(fullPrecision t) d=axlDBGetDesign() seen=makeTable('pub13FillSeen nil)
  f=outfile(strcat(dir "/complete_fill_structs.ilist"))
  vis=axlVisibleGet() enabled=axlGetFindFilter(nil) buttons=axlGetFindFilter(t)
  axlVisibleDesign(t) axlClearSelSet() axlSetFindFilter(?enabled '("noall" "alltypes") ?onButtons '("noall" "alltypes"))
  axlAddSelectAll() selected=axlGetSelSet() foreach(o selected pub13FillVisit(o f seen))
  axlClearSelSet() axlVisibleSet(vis) axlSetFindFilter(?enabled enabled ?onButtons buttons)
  foreach(s d->symbols pub13FillVisit(s f seen))
  foreach(n d->nets foreach(b n->branches pub13FillVisit(b f seen)))
  foreach(b axlDBGetLonelyBranches() pub13FillVisit(b f seen))
  foreach(o axlDBGetShapes(nil) pub13FillVisit(o f seen))
  foreach(o d->text pub13FillVisit(o f seen))
  pub13FillVisit(d->designOutline f seen) pub13FillVisit(d->keepinPlace f seen) pub13FillVisit(d->keepinRoute f seen)
  close(f)
  f=outfile(strcat(dir "/FILL_STRUCT_COMPLETE.txt")) fprintf(f "COMPLETE_READONLY_AXLFILL_ORIGIN_WIDTH_SPACING_ANGLE\nSAVE_CALLS=0\n") close(f) t))
