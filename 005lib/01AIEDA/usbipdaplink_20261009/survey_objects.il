let((fp d n b o s)
  fp=outfile("D:/001DIY/023USB/08UsbIPDapLink/02pcb/compact_layout/object_survey.txt")
  d=axlDBGetDesign()
  fprintf(fp "DESIGN_ATTRIBUTES %L\n" d->?)
  foreach(s d->symbols
    fprintf(fp "SYM|%s|%L|%L|%L\n" s->refdes s->xy s->bBox s->children)
  )
  foreach(n d->nets
    foreach(b n->branches
      foreach(o b->children
        fprintf(fp "OBJ|%s|%s|%L|%L|%L\n" n->name o->objType o->bBox o->layer o)
      )
    )
  )
  foreach(o axlDBGetShapes(nil)
    fprintf(fp "SHAPE|%s|%L|%L|%L|%L\n" o->objType o->bBox o->layer o->parent o->?)
  )
  fprintf(fp "COMPLETE\n")
  close(fp)
)
