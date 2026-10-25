from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/edit_pilotHI_v2.il').read_text()
s=s.replace('routes ret a b c gnd shape path void graph)','routes ret a b c gnd shape path void graph seg rippedPoints rippedWidth beforeCount afterCount)')
needle='  unless(equal(axlDBFindByName(\'net "V3V3")->unconnected initialUnc) error("Reroute changed V3V3 required joins\\n"))'
extra='''
  path=car(setof(x axlDBGetConnect(gPin("U1" "24") t) equal(x->objType "path")))
  seg=car(path->segments) rippedPoints=seg->startEnd rippedWidth=seg->width
  beforeCount=length(setof(x axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil) equal(x->objType "line") && equal(x->layer "ETCH/TOP") && x->net && equal(x->net->name "V3V3")))
  fprintf(f "SINGLE_SEGMENT_BEFORE=%L points=%L width=%L count=%d\\n" seg->?? rippedPoints rippedWidth beforeCount)
  unless(axlDeleteObject(seg) error("Cannot delete single cline segment\\n"))
  axlDBRefreshId(nil)
  afterCount=length(setof(x axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil) equal(x->objType "line") && equal(x->layer "ETCH/TOP") && x->net && equal(x->net->name "V3V3")))
  fprintf(f "SINGLE_SEGMENT_AFTER count=%d targetConnected=%L\\n" afterCount if(member(gPin("C13" "1") gConnectedObjects(gPin("U1" "24"))) then t else nil))
  unless(afterCount==beforeCount-1 && !member(gPin("C13" "1") gConnectedObjects(gPin("U1" "24"))) error("Single-segment delete was not scoped or did not disconnect\\n"))
  gRouteNative("V3V3" rippedPoints list(rippedWidth) "ETCH/TOP" f "HI_RECREATE_SINGLE_SEGMENT")
  axlDBRefreshId(nil)
  gConnectivityProof(f "U1" "24" "C13" "1" nil)
'''
assert needle in s;s=s.replace(needle,needle+extra)
(R/'scripts/edit_pilotHI_v3.il').write_text(s,encoding='ascii')
s=(R/'scripts/edit_pilot_4L_02.scr').read_text().replace('edit_pilotHI_v2.il','edit_pilotHI_v3.il').replace('edit_pilot_4L_02','edit_pilot_4L_03')
(R/'scripts/edit_pilot_4L_03.scr').write_text(s,encoding='ascii')
