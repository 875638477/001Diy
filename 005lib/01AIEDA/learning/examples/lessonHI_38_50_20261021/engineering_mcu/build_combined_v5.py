import pathlib,json,math
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
u=json.loads((R/"plans/usb_critical_routes_v4.json").read_text(encoding="utf-8"));u["status"]="CANDIDATE_V5_2L_WIDE_TO_SERIES_PAD_GEOMETRY_SCREEN"
u["variantOperations"]["2L"]=[o for o in u["variantOperations"]["2L"] if o["id"] not in ("USB2L_DP_PORT2","USB2L_DM_PORT2")]
for o in u["variantOperations"]["2L"]:
 if o["id"]=="USB2L_DP_WIDE":o["points"]=[[40.905,14.2],[40.905,16.6286],[41.1,16.8236]];o["to"]=["R5","2"]
 if o["id"]=="USB2L_DM_WIDE":o["points"]=[[39.595,14.2],[39.595,16.6286],[39.4,16.8236]];o["to"]=["R6","2"]
u["criticalLimit"]="2L wide1.15/.16 now extends toR5/R6 USB pad2, about2.70437mm coppercenterline; nearest next sharedpad edge.5298mm geometric. U4 port andconnector/MCUstage stillnarrow/nonuniform; manufacturerconfirmationnotobtained, nowholepath90ohm."
u["candidateLengths"]["protectedVariantRoutes"]={v:{o["id"]:sum(math.dist(a,b) for a,b in zip(o["points"],o["points"][1:])) for o in os if o["type"]=="route"} for v,os in u["variantOperations"].items()}
(R/"plans/usb_critical_routes_v5.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
gp=json.loads((R/"plans/gpio_north_escape_v1.json").read_text(encoding="utf-8"))
top={"GPIO_PC13":[[42.25,31.25],[42.25,29.15],[42,28.9]],"GPIO_PC14":[[41.75,31.25],[41.75,29.8],[40.65,29.8],[40.65,28.4]],"GPIO_PC15":[[41.25,31.25],[41.25,30.25],[39.7,30.25],[39.7,28.9]]}
bot={"GPIO_PC13":[[42,28.9],[41.2,28.1],[41.2,26.4],[35.4,26.4]],"GPIO_PC14":[[40.65,28.4],[40.55,28.3],[40.55,25.6],[35,25.6]],"GPIO_PC15":[[39.7,28.9],[39,28.2],[39,24.8],[34.6,24.8]]}
for o in gp["operations"]:
 net=o["net"]
 if net in top:
  if o["type"]=="via":o["xy"]=top[net][-1]
  elif o["layer"]=="TOP":o["points"]=top[net]
  else:o["points"]=bot[net]
 if o["id"]=="GPIO_RETURN_EAST":o["xy"]=[42,27.9]
 if o["id"]=="GPIO_RETURN_WEST":o["xy"]=[39.8,27.3]
gp["status"]="CANDIDATE_V2_AXIAL_BELOW_PIN_PAD_ROW_BEFORE_WEST_ESCAPE"
gp["supersedes"]="v1 GPIO_PC15 turned diagonally at30.85 while adjacentOSC_IN pad extendsdown30.65, leaving only.006mm. v2 keepsaxialtoy30.25 beforewestturn; allviasstaggeredawayfromremainingTOPtracksandV3star."
gp["furtherRouting"]="TheseBOTTOMescapeendsremainunfinished; preservealllayerreferenceandavoidHSEshadow.2LTOPreferencepatchwillhaveSMD/otherescapeapertures, so readactualcoverageandreturnpath; rectanglealoneisnotcontinuousplane."
(R/"plans/gpio_north_escape_v2.json").write_text(json.dumps(gp,ensure_ascii=False,indent=2),encoding="utf-8")
m=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"));power=json.loads((H/"engineering_power/power_star_03b.json").read_text(encoding="utf-8"));esd=json.loads((H/"engineering_power/ESD_ground_routes_04.json").read_text(encoding="utf-8"))
eops=esd.get("operations",[])
for v in ("4L","2L"):
 p=dict(m);p["placementChanges"]=m["placementChanges"]+u["placementChanges"];p["operations"]=m["operations"]+u["commonOperations"]+u["variantOperations"][v]+power["operations"]+gp["operations"]+eops
 (R/f"plans/combined_v5_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/"review_v5_copper.py").read_text(encoding="utf-8")
 s=s.replace('p=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"))',f'p=json.loads((R/"plans/combined_v5_screen_{v}.json").read_text(encoding="utf-8"))')
 s=s.replace('for v in ("4L","2L"):',f'for v in ("{v}",):').replace("mcu_v5_full_copper_screen.json",f"combined_v5_copper_screen_{v}.json")
 (R/f"review_combined_v5_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v5_{v}.py"),"exec"))
print("Combinedv5screen uses actualESDground04 and correctedGPIO2.")
