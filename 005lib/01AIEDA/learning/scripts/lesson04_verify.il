; Read-only verification of the saved training .dra in a fresh process.
procedure(edaL4Verify(outDir)
  let((report pinFile padFile geomFile segmentFile textFile design params pinRecord
       padRecord layerName objects obj segmentRecord box isFilled isRect rowCount
       segmentCount textCount segments port)
    report = outfile(strcat(outDir "/verify.txt"))
    pinFile = outfile(strcat(outDir "/pins.tsv"))
    padFile = outfile(strcat(outDir "/pads.tsv"))
    geomFile = outfile(strcat(outDir "/geometry.tsv"))
    segmentFile = outfile(strcat(outDir "/segments.tsv"))
    textFile = outfile(strcat(outDir "/texts.tsv"))
    unless(report && pinFile && padFile && geomFile && segmentFile && textFile
      error("Cannot open verification outputs\n"))
    design = axlDBGetDesign()
    params = axlGetParam("paramDesign")
    fprintf(report "EDA_LESSON04_VERIFY START\ndesign=%L\ntype=%L\nunits=%L\ndrawing_extents=%L\npins=%d\nstored_drcs=%d drc_state=%L\n"
      axlCurrentDesign() axlDesignType(t) axlDBGetDesignUnits() params->bBox
      length(design->pins) length(design->drcs) design->drcState)
    fprintf(pinFile "number\tpadstack\tx\ty\trotation\tmirrored\tthrough\thole_type\tdrill_diameter\n")
    fprintf(padFile "number\tlayer\tfigure\twidth\theight\tlocal_bbox\tlocal_offset\n")
    foreach(pinRecord design->pins
      fprintf(pinFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
        pinRecord->number pinRecord->name car(pinRecord->xy) cadr(pinRecord->xy)
        pinRecord->rotation pinRecord->isMirrored pinRecord->isThrough
        pinRecord->definition->holeType pinRecord->definition->drillDiameter)
      foreach(layerName list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/SOLDERMASK_BOTTOM" "PIN/PASTEMASK_TOP" "PIN/PASTEMASK_BOTTOM")
        padRecord = axlDBGetPad(pinRecord layerName "REGULAR")
        box = if(padRecord then padRecord->bBox else nil)
        fprintf(padFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
          pinRecord->number layerName if(padRecord then padRecord->figureName else nil)
          if(box then car(cadr(box))-car(car(box)) else nil)
          if(box then cadr(cadr(box))-cadr(car(box)) else nil) box
          if(padRecord then padRecord->offset else nil))
      )
    )
    fprintf(geomFile "type\tlayer\tmin_x\tmin_y\tmax_x\tmax_y\tfilled\tis_rectangle\n")
    fprintf(segmentFile "layer\ttype\tstart_x\tstart_y\tend_x\tend_y\twidth\n")
    fprintf(textFile "layer\ttext\tx\ty\trotation\n")
    objects = axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
    unless(objects error("FULL_GEOMETRY returned no objects\n"))
    rowCount = 0
    segmentCount = 0
    textCount = 0
    foreach(obj objects
      when(member(obj->layer list("PACKAGE GEOMETRY/SILKSCREEN_TOP" "PACKAGE GEOMETRY/ASSEMBLY_TOP" "PACKAGE GEOMETRY/PLACE_BOUND_TOP" "REF DES/SILKSCREEN_TOP"))
        box = obj->bBox
        isFilled = nil
        isRect = nil
        when(equal(obj->objType "shape") isFilled = obj->fill isRect = obj->isRect)
        fprintf(geomFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
          obj->objType obj->layer car(car(box)) cadr(car(box)) car(cadr(box)) cadr(cadr(box)) isFilled isRect)
        rowCount = rowCount + 1
        segments = nil
        when(equal(obj->objType "path") segments = obj->segments)
        when(member(obj->objType list("line" "arc")) segments = list(obj))
        when(segments
          foreach(segmentRecord segments
            fprintf(segmentFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
              obj->layer segmentRecord->objType car(car(segmentRecord->startEnd)) cadr(car(segmentRecord->startEnd))
              car(cadr(segmentRecord->startEnd)) cadr(cadr(segmentRecord->startEnd)) segmentRecord->width)
            segmentCount = segmentCount + 1
          )
        )
        when(equal(obj->objType "text")
          fprintf(textFile "%L\t%L\t%L\t%L\t%L\n" obj->layer obj->text car(obj->xy) cadr(obj->xy) obj->rotation)
          textCount = textCount + 1
        )
      )
    )
    fprintf(report "full_geometry_objects=%d\ntarget_geometry_rows=%d\noutline_segments=%d\nrefdes_text_rows=%d\n"
      length(objects) rowCount segmentCount textCount)
    foreach(port list(pinFile padFile geomFile segmentFile textFile) close(port))
    fprintf(report "EDA_LESSON04_VERIFY COMPLETE\n")
    close(report)
    t
  )
)
