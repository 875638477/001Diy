; Read-only checks of placed pad polygons for selected representative parts.
procedure(edaL3Geometry(outPath)
  let((design report componentRecord symbolRecord pinRecord layerName padRecord
       polyList polyRecord polyIndex queryCount)
    design = axlDBGetDesign()
    unless(design error("No active design for geometry probe\n"))
    report = outfile(outPath)
    unless(report error("Cannot open geometry report\n"))
    fprintf(report "EDA_LESSON03_GEOMETRY START\nunits=%L\n" axlDBGetDesignUnits())
    queryCount = 0
    foreach(componentRecord design->components
      when(member(componentRecord->name list("C21" "C1" "U17" "Y1"))
        symbolRecord = componentRecord->symbol
        fprintf(report "COMP refdes=%L placed=%L origin=%L rotation=%L mirrored=%L\n"
          componentRecord->name edaL3Bool(symbolRecord)
          if(symbolRecord then symbolRecord->xy else nil)
          if(symbolRecord then symbolRecord->rotation else nil)
          if(symbolRecord then symbolRecord->isMirrored else nil))
        foreach(pinRecord componentRecord->pins
          fprintf(report "PIN refdes=%L number=%L net=%L xy=%L relxy=%L rotation=%L mirrored=%L padstack=%L definition_present=%L\n"
            componentRecord->name pinRecord->number edaL3NetName(pinRecord->net)
            pinRecord->xy pinRecord->relxy pinRecord->rotation pinRecord->isMirrored
            pinRecord->name edaL3Bool(pinRecord->definition))
          when(pinRecord->definition
            foreach(layerName list("TOP" "BOTTOM")
              queryCount = queryCount + 1
              padRecord = axlDBGetPad(pinRecord strcat("ETCH/" layerName) "REGULAR")
              polyList = axlPolyFromDB(pinRecord ?layer strcat("ETCH/" layerName) ?padType 'REGULAR)
              fprintf(report "PAD refdes=%L number=%L layer=%L figure=%L local_bbox=%L local_offset=%L on_layer_respect_suppression=%L on_layer_ignore_suppression=%L polygons=%d\n"
                componentRecord->name pinRecord->number layerName
                if(padRecord then padRecord->figureName else nil)
                if(padRecord then padRecord->bBox else nil)
                if(padRecord then padRecord->offset else nil)
                axlPadOnLayer(pinRecord layerName) axlPadOnLayer(pinRecord layerName t)
                length(polyList))
              polyIndex = 0
              foreach(polyRecord polyList
                polyIndex = polyIndex + 1
                fprintf(report "POLY refdes=%L number=%L layer=%L index=%d bbox=%L area=%L vertices=%L\n"
                  componentRecord->name pinRecord->number layerName polyIndex
                  polyRecord->bBox polyRecord->area polyRecord->vertices)
              )
            )
          )
        )
      )
    )
    fprintf(report "queries=%d\nEDA_LESSON03_GEOMETRY COMPLETE\n" queryCount)
    close(report)
    t
  )
)
