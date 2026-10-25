; Read back in a fresh Allegro process, never saves the drawing.
procedure(qmiVerify(outDir)
  let((report pinFile padFile segFile textFile d p pad layer box objs obj segs seg bound props)
    report = outfile(strcat(outDir "/verify.txt"))
    pinFile = outfile(strcat(outDir "/pins.tsv"))
    padFile = outfile(strcat(outDir "/pads.tsv"))
    segFile = outfile(strcat(outDir "/segments.tsv"))
    textFile = outfile(strcat(outDir "/texts.tsv"))
    unless(report && pinFile && padFile && segFile && textFile error("Cannot open readback outputs\n"))
    d = axlDBGetDesign()
    fprintf(report "QMI8610_VERIFY START\ndesign=%L type=%L units=%L\npins=%d drcs=%d drcState=%L\n"
      axlCurrentDesign() axlDesignType(t) axlDBGetDesignUnits() length(d->pins) length(d->drcs) d->drcState)
    fprintf(pinFile "number\tpadstack\tx\ty\trotation\tmirrored\tthrough\thole_type\tdrill_diameter\ttop\tbottom\n")
    fprintf(padFile "number\tlayer\tfigure\twidth\theight\tbbox\toffset\n")
    foreach(p d->pins
      fprintf(pinFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
        p->number p->name car(p->xy) cadr(p->xy) p->rotation p->isMirrored p->isThrough
        p->definition->holeType p->definition->drillDiameter axlPadOnLayer(p "TOP") axlPadOnLayer(p "BOTTOM"))
      foreach(layer list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/SOLDERMASK_BOTTOM" "PIN/PASTEMASK_TOP" "PIN/PASTEMASK_BOTTOM")
        pad = axlDBGetPad(p layer "REGULAR")
        box = if(pad then pad->bBox else nil)
        fprintf(padFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\n" p->number layer
          if(pad then pad->figureName else nil)
          if(box then car(cadr(box))-car(car(box)) else nil)
          if(box then cadr(cadr(box))-cadr(car(box)) else nil)
          box if(pad then pad->offset else nil))
      )
    )
    objs = axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
    unless(objs error("No FULL_GEOMETRY objects\n"))
    fprintf(segFile "layer\ttype\tx1\ty1\tx2\ty2\twidth\n")
    fprintf(textFile "layer\ttext\tx\ty\trotation\ttextblock\n")
    foreach(obj objs
      when(member(obj->layer list("PACKAGE GEOMETRY/SILKSCREEN_TOP" "PACKAGE GEOMETRY/ASSEMBLY_TOP"))
        segs = nil
        when(equal(obj->objType "path") segs = obj->segments)
        when(member(obj->objType list("line" "arc")) segs = list(obj))
        foreach(seg segs
          fprintf(segFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\n" obj->layer seg->objType
            car(car(seg->startEnd)) cadr(car(seg->startEnd)) car(cadr(seg->startEnd)) cadr(cadr(seg->startEnd)) seg->width))
      )
      when(equal(obj->objType "text") && member(obj->layer list("REF DES/SILKSCREEN_TOP" "REF DES/ASSEMBLY_TOP" "COMPONENT VALUE/ASSEMBLY_TOP"))
        fprintf(textFile "%L\t%L\t%L\t%L\t%L\t%L\n" obj->layer obj->text car(obj->xy) cadr(obj->xy) obj->rotation obj->textBlock))
    )
    foreach(bound axlDBGetShapes("PACKAGE GEOMETRY/PLACE_BOUND_TOP")
      props = axlDBGetProperties(bound nil)
      fprintf(report "place_bound_bbox=%L filled=%L properties=%L\n" bound->bBox bound->fill props))
    fprintf(report "textblocks=%L\n" axlGetParam("paramTextBlock"))
    foreach(p list(report pinFile padFile segFile textFile) close(p))
    report = outfile(strcat(outDir "/complete.txt"))
    fprintf(report "QMI8610_VERIFY COMPLETE\n")
    close(report)
    t
  )
)
