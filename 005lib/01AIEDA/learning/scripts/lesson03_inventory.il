; Cadence 17.2 lesson 03: definitions only; all database access is read-only.
procedure(edaL3Bool(value) if(value then t else nil))
procedure(edaL3X(point) if(point then car(point) else nil))
procedure(edaL3Y(point) if(point then cadr(point) else nil))
procedure(edaL3NetName(netRecord)
  cond((axlIsDBIDType(netRecord) netRecord->name)
       (stringp(netRecord) netRecord)
       (t nil))
)
procedure(edaL3BoxWidth(box)
  if(box then car(cadr(box)) - car(car(box)) else nil)
)
procedure(edaL3BoxHeight(box)
  if(box then cadr(cadr(box)) - cadr(car(box)) else nil)
)
procedure(edaL3Export(outDir)
  let((design summary componentFile symbolFile pinFile functionFile padFile
       padstackFile netFile componentRecord symbolRecord pinRecord netRecord
       functionRecord functionPin padRecord padstackRecord definitionRecord
       layerRecord queryLayer queryLayers localBox componentCount placedCount
       pinCount functionCount padCount missingDefinitions ownerMismatches
       symbolMembershipMismatches functionBacklinkMismatches port)
    design = axlDBGetDesign()
    unless(design error("No active design for lesson03\n"))
    summary = outfile(strcat(outDir "/summary.txt"))
    componentFile = outfile(strcat(outDir "/components.tsv"))
    symbolFile = outfile(strcat(outDir "/symbols.tsv"))
    pinFile = outfile(strcat(outDir "/pins.tsv"))
    functionFile = outfile(strcat(outDir "/function_pins.tsv"))
    padFile = outfile(strcat(outDir "/pad_layers.tsv"))
    padstackFile = outfile(strcat(outDir "/padstacks.tsv"))
    netFile = outfile(strcat(outDir "/nets.tsv"))
    unless(summary && componentFile && symbolFile && pinFile && functionFile && padFile && padstackFile && netFile
      error("Cannot open lesson03 output files\n"))
    fprintf(summary "EDA_LESSON03 START\ndesign=%L\nunits=%L\n" axlCurrentDesign() axlDBGetDesignUnits())
    fprintf(componentFile "refdes\tdevice_type\tpackage\tplaced\tdefinition\tx\ty\trotation\tmirrored\tlogical_pin_count\tsymbol_pin_count\n")
    fprintf(symbolFile "symbol_name\trefdes\ttype\tcomponent\tdefinition\tx\ty\trotation\tmirrored\tpin_count\n")
    fprintf(pinFile "refdes\tnumber\tpadstack\tnet\tx\ty\trel_x\trel_y\trotation\trel_rotation\tmirrored\tthrough\tmechanical\tspan\tfunction_names\towner_matches\tin_symbol_pins\n")
    fprintf(functionFile "refdes\tfunction\tfunction_pin_name\tuse\tphysical_number\tin_component_pins\tin_pin_function_list\n")
    fprintf(padFile "refdes\tnumber\tquery_layer\tpad_found\tfigure_name\tlocal_bbox\tlocal_width\tlocal_height\tlocal_offset\treturned_layer\n")
    fprintf(padstackFile "name\ttype\tthrough\tplating\thole_type\tdrill_diameter\tdrill_width\tdrill_height\tdrill_offset\tspan\tis_pad_reference\treferenced_definition\n")
    fprintf(netFile "name\tunconnected_stored\tunplaced_pins\tbranch_count\n")
    queryLayers = nil
    foreach(layerRecord axlXSectionGet(nil 'all)
      when(layerRecord->conductor
        queryLayers = append(queryLayers list(strcat("ETCH/" layerRecord->name))))
    )
    queryLayers = append(queryLayers list("PIN/SOLDERMASK_TOP" "PIN/SOLDERMASK_BOTTOM"))
    componentCount = 0
    placedCount = 0
    pinCount = 0
    functionCount = 0
    padCount = 0
    missingDefinitions = 0
    ownerMismatches = 0
    symbolMembershipMismatches = 0
    functionBacklinkMismatches = 0
    foreach(componentRecord design->components
      componentCount = componentCount + 1
      symbolRecord = componentRecord->symbol
      definitionRecord = if(symbolRecord then symbolRecord->definition else nil)
      when(symbolRecord placedCount = placedCount + 1)
      fprintf(componentFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%d\t%L\n"
        componentRecord->name componentRecord->deviceType componentRecord->package
        edaL3Bool(symbolRecord) if(definitionRecord then definitionRecord->name else nil)
        if(symbolRecord then edaL3X(symbolRecord->xy) else nil)
        if(symbolRecord then edaL3Y(symbolRecord->xy) else nil)
        if(symbolRecord then symbolRecord->rotation else nil)
        if(symbolRecord then symbolRecord->isMirrored else nil)
        length(componentRecord->pins)
        if(symbolRecord then length(symbolRecord->pins) else nil))
      foreach(pinRecord componentRecord->pins
        pinCount = pinCount + 1
        unless(pinRecord->definition missingDefinitions = missingDefinitions + 1)
        unless(equal(pinRecord->component componentRecord) ownerMismatches = ownerMismatches + 1)
        when(symbolRecord && !member(pinRecord symbolRecord->pins)
          symbolMembershipMismatches = symbolMembershipMismatches + 1)
        fprintf(pinFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
          componentRecord->name pinRecord->number pinRecord->name edaL3NetName(pinRecord->net)
          edaL3X(pinRecord->xy) edaL3Y(pinRecord->xy)
          edaL3X(pinRecord->relxy) edaL3Y(pinRecord->relxy)
          pinRecord->rotation pinRecord->relRotation pinRecord->isMirrored
          pinRecord->isThrough pinRecord->isMech pinRecord->startEnd
          pinRecord->functionPins~>name edaL3Bool(equal(pinRecord->component componentRecord))
          if(symbolRecord then edaL3Bool(member(pinRecord symbolRecord->pins)) else nil))
        when(pinRecord->definition
          foreach(queryLayer queryLayers
            padRecord = axlDBGetPad(pinRecord queryLayer "REGULAR")
            localBox = if(padRecord then padRecord->bBox else nil)
            fprintf(padFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
              componentRecord->name pinRecord->number queryLayer edaL3Bool(padRecord)
              if(padRecord then padRecord->figureName else nil) localBox
              edaL3BoxWidth(localBox) edaL3BoxHeight(localBox)
              if(padRecord then padRecord->offset else nil)
              if(padRecord then padRecord->layer else nil))
            padCount = padCount + 1
          )
        )
      )
      foreach(functionRecord componentRecord->functions
        foreach(functionPin functionRecord->pins
          pinRecord = functionPin->pin
          functionCount = functionCount + 1
          unless(pinRecord && member(pinRecord componentRecord->pins) && member(functionPin pinRecord->functionPins)
            functionBacklinkMismatches = functionBacklinkMismatches + 1)
          fprintf(functionFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
            componentRecord->name functionRecord->name functionPin->name functionPin->use
            if(pinRecord then pinRecord->number else nil)
            edaL3Bool(member(pinRecord componentRecord->pins))
            if(pinRecord then edaL3Bool(member(functionPin pinRecord->functionPins)) else nil))
        )
      )
    )
    foreach(symbolRecord design->symbols
      componentRecord = symbolRecord->component
      definitionRecord = symbolRecord->definition
      fprintf(symbolFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%d\n"
        symbolRecord->name symbolRecord->refdes symbolRecord->type
        if(componentRecord then componentRecord->name else nil)
        if(definitionRecord then definitionRecord->name else nil)
        edaL3X(symbolRecord->xy) edaL3Y(symbolRecord->xy)
        symbolRecord->rotation symbolRecord->isMirrored length(symbolRecord->pins))
    )
    foreach(padstackRecord design->padstacks
      definitionRecord = padstackRecord->definition
      fprintf(padstackFile "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n"
        padstackRecord->name padstackRecord->type padstackRecord->isThrough
        padstackRecord->plating padstackRecord->holeType padstackRecord->drillDiameter
        padstackRecord->drillSizeWidth padstackRecord->drillSizeHeight padstackRecord->drillOffset
        padstackRecord->startEnd padstackRecord->isPadRef
        if(definitionRecord then definitionRecord->name else nil))
    )
    foreach(netRecord design->nets
      fprintf(netFile "%L\t%L\t%L\t%L\n" netRecord->name netRecord->unconnected netRecord->unplaced netRecord->nBranches))
    foreach(port list(componentFile symbolFile pinFile functionFile padFile padstackFile netFile) close(port))
    fprintf(summary "components=%d\nplaced_components=%d\nsymbols=%d\npins=%d\nfunction_pins=%d\npad_layer_queries=%d\npadstacks=%d\nnets=%d\n"
      componentCount placedCount length(design->symbols) pinCount functionCount padCount length(design->padstacks) length(design->nets))
    fprintf(summary "missing_pin_definitions=%d\npin_owner_mismatches=%d\nplaced_pin_symbol_membership_mismatches=%d\nfunction_backlink_mismatches=%d\n"
      missingDefinitions ownerMismatches symbolMembershipMismatches functionBacklinkMismatches)
    fprintf(summary "EDA_LESSON03 COMPLETE\n")
    close(summary)
    t
  )
)
