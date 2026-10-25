; DEFINITIONS ONLY. READ-ONLY OWNER AUDIT. No DB changes, selection, DRC, save or shell.
; Official SPB17.2 algroskill/02dbdesc.html: Symbol children/component/refdes;
; Text parent/xy/bBox/text/textBlock/justify/rotation/isMirrored.
; axlDBGetExtents(o nil): algroskill/14dsnctl.html#730938 (TEXT supported).
procedure(rcTextAudit(outDir)
 let((d f g h done s o c cp sp tp value p row rows count valuesCount symbolCount badParent parent owned seen block blockKey blockProps extents geom i n)
  d=axlDBGetDesign()
  unless(d error("No open design"))
  rows=nil count=0 valuesCount=0 symbolCount=0 badParent=0
  seen=makeTable('rcTextSeen nil)
  g=outfile(strcat(outDir "/symbol_component_values.tsv"))
  fprintf(g "ref\tsymbol_dbid\tcomponent_dbid\tcomponent_name\tcomponent_value\tsymbol_name\tsymbol_xy\tsymbol_rotation\tsymbol_mirrored\tsymbol_properties\tcomponent_properties\n")
  foreach(s d->symbols
   symbolCount=symbolCount+1 c=s->component
   sp=axlDBGetProperties(s '("user" "allegro"))
   cp=if(c then axlDBGetProperties(c '("user" "allegro")) else nil)
   value=nil p=assoc('COMP_VALUE cp)
   when(p value=cadr(p))
   fprintf(g "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" s->refdes s c if(c then c->name else nil) value s->name s->xy s->rotation s->isMirrored sp cp)
   foreach(o s->children
    when(equal(o->objType "text")
     seen[o]=t count=count+1 parent=o->parent owned=equal(parent s)
     unless(owned badParent=badParent+1)
     when(member(o->layer '("COMPONENT VALUE/SILKSCREEN_TOP" "COMPONENT VALUE/SILKSCREEN_BOTTOM" "COMPONENT VALUE/ASSEMBLY_TOP" "COMPONENT VALUE/ASSEMBLY_BOTTOM")) valuesCount=valuesCount+1)
     block=o->textBlock blockProps=nil
     when(block blockKey=sprintf(nil "paramTextBlock:%s" block) blockProps=axlGetParam(blockKey))
     tp=axlDBGetProperties(o '("user" "allegro"))
     extents=axlDBGetExtents(o nil)
     geom=sprintf(nil "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L"
      o->objType o->layer o->xy o->bBox o->startEnd o->width o->radius o->isClockwise o->vertices o->text o->rotation o->isMirrored o->name o->number o->isMech o->isThrough o->font o->fill o->isHole o->isRect o->shapeIsBoundary o->nSegs o->justify o->textBlock o->isMirrored)
     row=sprintf(nil "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L"
      s->refdes s c o parent owned o->layer o->xy o->text o->bBox o->font o->textBlock o->justify o->rotation o->isMirrored o->mirrorType value s->name s->xy s->rotation s->isMirrored if(blockProps then blockProps->?? else nil) tp o->?? extents list(o parent if(parent then parent->parent else nil)) geom)
     rows=cons(row rows)
    )
   )
  )
  close(g)
  f=outfile(strcat(outDir "/symbol_owned_texts.tsv"))
  fprintf(f "ref\tsymbol_dbid\tcomponent_dbid\ttext_dbid\tparent_dbid\tparent_matches_symbol\tlayer\txy\ttext\tbbox\tfont\ttextBlock\tjustify\trotation\tmirrored\tmirrorType\tcomponent_value\tsymbol_name\tsymbol_xy\tsymbol_rotation\tsymbol_mirrored\ttextblock_attributes\ttext_properties\tall_text_attributes\twhole_object_extents\tparent_chain\traw_geometry_25column_record\n")
  foreach(row sort(rows 'alphalessp) fprintf(f "%s\n" row)) close(f)
  h=outfile(strcat(outDir "/all_textblocks.tsv"))
  fprintf(h "index\tname\twidth\theight\tcharSpace\tlineSpace\tphotoWidth\tall_attributes\n")
  n=axlDBGetTextBlockCount()
  for(i 1 n
   blockProps=axlGetParam(sprintf(nil "paramTextBlock:%d" i))
   fprintf(h "%d\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" i blockProps->name blockProps->width blockProps->height blockProps->charSpace blockProps->lineSpace blockProps->photoWidth blockProps->??)
  ) close(h)
  h=outfile(strcat(outDir "/unowned_design_texts.tsv"))
  fprintf(h "text_dbid\tparent_dbid\tparent_type\tlayer\txy\ttext\tbbox\tfont\ttextBlock\tjustify\trotation\tmirrored\tproperties\n")
  foreach(o d->text
   unless(seen[o]
    parent=o->parent
    fprintf(h "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" o parent if(parent then parent->objType else nil) o->layer o->xy o->text o->bBox o->font o->textBlock o->justify o->rotation o->isMirrored axlDBGetProperties(o '("user" "allegro")))
   )
  ) close(h)
  unless(badParent==0 error("Text child parent mismatch: %d" badParent))
  done=outfile(strcat(outDir "/COMPLETE.txt"))
  fprintf(done "COMPLETE\nsymbols=%d\nsymbol_owned_texts=%d\ncomponent_value_standard_layer_texts=%d\nbad_parent=%d\ntextblocks=%d\nSAVE_CALLS=0\nMUTATION_CALLS=0\n" symbolCount count valuesCount badParent n)
  close(done)
  t
 ))
