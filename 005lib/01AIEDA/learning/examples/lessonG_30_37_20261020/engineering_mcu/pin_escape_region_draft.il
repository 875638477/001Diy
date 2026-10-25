; UNEXECUTED RESEARCH DRAFT - do not treat this file as native proof.
; Caller must inspect actual CONSTRAINT REGION subclass/layer applicability,
; review three small bbox polygons, and use an isolated experimental board.
; API references copied beside this file in api_sources.
; PIN_ESCAPE is NOT a spacing override.
procedure(g31LocalEscapeRegionDraft(regionName regionLayer boxes)
 let((region shape cset table)
  unless(axlLayerGet(regionLayer)
   error("Caller-supplied actual constraint-region layer does not exist\n"))
  cset="G31_PIN_ESCAPE_020"
  unless(axlCNSCreate('spacing cset "S_POWER_030")
   error("Draft requires fresh independent CSet; inspect existing names\n"))
  unless(axlCNSSetSpacing(cset "TOP" 'smdpin_line "0.20 MM")
   error("Cannot set local smdpin_line spacing\n"))
  unless(axlCNSSetSpacing(cset "TOP" 'line_line "0.20 MM")
   error("Cannot set local line_line spacing\n"))
  region=axlRegionCreate(regionName)
  unless(region error("Region create failed or name already exists/license unsupported\n"))
  foreach(box boxes
   shape=car(axlDBCreateRectangle(box nil regionLayer))
   unless(shape error("Constraint-region rectangle creation failed\n"))
   unless(axlRegionAdd(region shape) error("Region membership failed\n")))
  table=axlCnsClassTableCreate("NC_POWER_LV_S" nil region 'spacing cset)
  unless(table error("Region-class binding failed\n"))
  unless(axlCnsClassTableSeek("NC_POWER_LV_S" nil region)
   error("Readback missing region-class entry\n"))
  axlCNSMapUpdate()
  axlDRCUpdate(t)
  ; REQUIRED: actual boundary/subclass/member/CSet dump and current DRC,
  ; identical spacing challenge inside/outside; rollback; save/reopen;
  ; original class/default values unchanged. No manufacturing claim.
  table))
