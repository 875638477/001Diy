import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
extra=[]
for name in("STAR_reroute_07b.json","V3_peripheral_distribution_06b.json"):
 d=json.loads((H/"engineering_power"/name).read_text(encoding="utf-8"))
 extra +=[o for o in d["operations"] if o["type"] in("route","via")]
for v in("4L","2L"):
 p=json.loads((R/f"plans/combined_v9_screen_{v}.json").read_text(encoding="utf-8"));p["operations"]+=extra
 for o in p["operations"]:
  if o["id"]=="USB_RETURN_LEFT":o["xy"]=[38.3,5.8]
 (R/f"plans/combined_v10_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v9_{v}.py").read_text(encoding="utf-8").replace("combined_v9","combined_v10")
 (R/f"review_combined_v10_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v10_{v}.py"),"exec"))
(R/"plans/usb_left_return_move_proposal.json").write_text(json.dumps({"status":"GEOMETRY_SCREENED_ONLY_DO_NOT_EXECUTE_USB8_REBUILD_SOLELY_FOR_THIS","change":{"type":"moveVia","net":"GND","padstack":"L28_VIA030_C060","from":[38.15,5.8],"to":[38.3,5.8]},"scope":"Bothvariants applicationGNDreturn only; deleteuniquepreviousviaandrecreate, notaddoverlappingdrill","signalTransitionDistance":{"A6DPvia":[39.75,5.8],"previous":1.6,"proposed":1.45,"rightSignalToReturnStill":.95},"mechanicalNPTH":{"center":[37.11,6.28],"drillDiameter":.65,"proposedViaToNPTHHoleEdge":((38.3-37.11)**2+(5.8-6.28)**2)**.5-.3-.325},"caveat":"TOPpatchactualreturnpath/planeconnectivitystillneeded; distancealoneisnotreturnproof; actualtentandundersideassemblyunchangedopen."},indent=2),encoding="utf-8")
