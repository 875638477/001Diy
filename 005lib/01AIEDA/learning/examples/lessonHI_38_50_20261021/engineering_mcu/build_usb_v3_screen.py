import pathlib,json,math
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
u=json.loads((R/"plans/usb_critical_routes_v2.json").read_text(encoding="utf-8"))
for c in u["placementChanges"]:
 if c["ref"]=="R11":c["xy"]=[42.9764,14.6];c["rotation"]=180;c["purpose"]="DPpad2=(41.3,14.6), sourcepad1=(42.8748,14.6). Directly adjacent maintrunk: .845mm4L or.4mm2L; cannot put.94mm pad onto.41mm-centered4Lpair without short toDM."
u["commonOperations"]=[o for o in u["commonOperations"] if o["id"]!="USB_PULLUP_BRANCH"]
def route(id,pts):return {"type":"route","id":id,"net":"USB_DP","layer":"TOP","points":pts,"width":.2,"from":["USB_DP_TRUNK_NODE","14.6"],"to":["R11","2"],"purpose":"RequiredFS pullup shorttee; sourceotherendtoQ2 may be longer"}
u["variantOperations"]["4L"].append(route("USB_PULLUP_BRANCH",[[40.455,14.6],[41.3,14.6]]))
u["variantOperations"]["2L"].append(route("USB_PULLUP_BRANCH",[[40.9,14.6],[41.3,14.6]]))
def le(pts):return sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))
lens={o["id"]:le(o["points"]) for o in u["commonOperations"] if o["type"]=="route"}
b=next(o for o in u["commonOperations"] if o["id"]=="USB_DP_MIRROR_BOTTOM")
dpa=lens["USB_DP_ENTRY"]+lens["USB_DP_A6_TO_MIRROR"]+lens["USB_DP_B6_TO_MIRROR"]+le(b["points"])
dma=lens["USB_DM_ENTRY"]+lens["USB_DM_A7_MERGE"]
u["candidateLengths"]={"units":"mm, centerline plan only, not actual native nor component propagation","orientationB":{"J2.B6_to_U4.6":lens["USB_DP_ENTRY"],"J2.B7_to_U4.4":lens["USB_DM_ENTRY"],"DPminusDM":lens["USB_DP_ENTRY"]-lens["USB_DM_ENTRY"]},"orientationA":{"J2.A6_to_U4.6_planar":dpa,"J2.A7_to_U4.4_planar":dma,"DPminusDM_planar":dpa-dma,"DPextraFullThroughViaCount":2},"sharedMCUSide":{"R5.1_to_U1.33":lens["USB_SHARED_DP"],"R6.1_to_U1.32":lens["USB_SHARED_DM"],"DPminusDM":lens["USB_SHARED_DP"]-lens["USB_SHARED_DM"]},"eachCommonRoute":lens,"protectedVariantRoutes":{v:{o["id"]:le(o["points"]) for o in os if o["type"]=="route"} for v,os in u["variantOperations"].items()}}
u["delayScaleEstimate"]={"status":"Simpletimeofflightestimateonly_not_softwareSI_simulation_norhardwaremeasurement","assumptions":{"planarEffectiveDkRange":[2.8,3.5],"planar_ps_per_mm_range":[math.sqrt(2.8)/.299792458,math.sqrt(3.5)/.299792458],"throughViaRelativeDk":4.5,"via_ps_per_mm":math.sqrt(4.5)/.299792458},"orientationA_planarSkew_ps_range":[(dpa-dma)*math.sqrt(er)/.299792458 for er in (2.8,3.5)],"extraBarrelDelay_ps":{"2L":2*1.5952*math.sqrt(4.5)/.299792458,"4L":2*1.5862*math.sqrt(4.5)/.299792458},"context":"DS5319PDF73Table46 tr/tf4..20ns atCL50pF bydesign, nottestedproduction. USBFS12Mbit/s period83.333ns. These numbers establish scale only, not specificationpermission for mismatch or boardcertification."}
u["matchingDecision"]+=" Include actualnativevia/barrel contribution. A4mm scalarbudget may be insufficient ifCadence counts both full through barrels; derive finalUSB_CONNECTOR copy phase fromactual+margin (about7mm physicalpathcandidate ifbarrelsincluded), preserve maxvia anduncoupledlimits unless explicitseparatereason. No guessingnativepass."
u["status"]="CANDIDATE_V3_GEOMETRY_SCREEN_PENDING"
(R/"plans/usb_critical_routes_v3.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
m=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"))
power=json.loads((R.parent/"engineering_power/power_star_03.json").read_text(encoding="utf-8"))
for v in ("4L","2L"):
 p=dict(m);p["placementChanges"]=m["placementChanges"]+u["placementChanges"];p["operations"]=m["operations"]+u["commonOperations"]+u["variantOperations"][v]+power["operations"]
 (R/f"plans/combined_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/"review_v5_copper.py").read_text(encoding="utf-8")
 s=s.replace('p=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"))',f'p=json.loads((R/"plans/combined_screen_{v}.json").read_text(encoding="utf-8"))')
 s=s.replace('for v in ("4L","2L"):',f'for v in ("{v}",):')
 s=s.replace("mcu_v5_full_copper_screen.json",f"combined_copper_screen_{v}.json")
 (R/f"review_combined_{v}.py").write_text(s,encoding="utf-8")
 exec(compile(s,str(R/f"review_combined_{v}.py"),"exec"))
print(json.dumps({"USBLengths":u["candidateLengths"],"delay":u["delayScaleEstimate"]},ensure_ascii=True))
