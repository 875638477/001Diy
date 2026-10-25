; Cadence 17.2 read-only database lesson. Does not edit or save a design.
procedure(edaLesson02Probe(reportPath)
  let((report design stackup layers conductorCount)
    report = outfile(reportPath)
    unless(report error("Cannot open lesson report: %s\n" reportPath))
    fprintf(report "EDA_LESSON02 START\n")
    design = axlDBGetDesign()
    if(design then
      fprintf(report "design=%L\n" axlCurrentDesign())
      fprintf(report "units=%L\n" axlDBGetDesignUnits())
      fprintf(report "components=%d\n" length(design->components))
      fprintf(report "nets=%d\n" length(design->nets))
      fprintf(report "symbols=%d\n" length(design->symbols))
      fprintf(report "design_bbox=%L\n" design->bBox)
      fprintf(report "stored_drcs=%d drc_state=%L\n"
        length(design->drcs) design->drcState)
      fprintf(report "stackups=%L\n" axlXSectionGet(nil 'stackups))
      conductorCount = 0
      layers = axlXSectionGet(nil 'all)
      foreach(layer layers
        fprintf(report "layer position=%L name=%L type=%L conductor=%L thickness=%L material=%L\n"
          layer->position layer->name layer->layerType
          layer->conductor layer->thickness layer->material)
        when(layer->conductor conductorCount = conductorCount + 1)
      )
      fprintf(report "conductor_layers=%d\n" conductorCount)
      fprintf(report "EDA_LESSON02 COMPLETE\n")
    else
      fprintf(report "EDA_LESSON02 FAILED no design loaded\n")
    )
    close(report)
  )
)
edaLesson02Probe("D:/001DIY/005lib/01AIEDA/learning/logs/lesson02_readonly_20261017/probe.txt")
