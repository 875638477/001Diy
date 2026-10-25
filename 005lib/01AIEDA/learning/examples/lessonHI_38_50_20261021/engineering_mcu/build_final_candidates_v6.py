import pathlib,json,math,copy
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
m=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"))
m["status"]="CANDIDATE_V6_NATIVE_TWO_SPACING_CORRECTIONS"
for p in m["placementChanges"]:
 if p["ref"]=="R23":p["xy"][1]=33.02;p["purpose"]+="; +.02mm y avoids native POWER .3 clearance against retained STAR_C9_FEED"
for o in m["operations"]:
 if o["id"]=="ADC_PIN_CAP":
  o["points"]=[[38.25,31.25],[38.25,32.3],[35.5,32.3],[34.8,33]]
m["nativeV5Corrections"]={"4L_and_2L_failures":[{"object":"R23.2 versus STAR_C9_FEED","actualGap":.2959,"required":.3,"solution":"R23 y33.02, preserve global rule"},{"object":"ADC_PIN_CAP versus U1.12 at37.25,32.2 outside north-local region","actualGap":.25,"required":.3,"solution":"Horizontal y32.3 then45degree intoC24; preserve region/global scopes"}],"nativeOtherTests":"Both layers V5 32target endpoints and oscillator uniquevia-removal challenge passed; not claimed final until V6 rebuilt/reopened"}
# Avoid old descriptive GPIO candidates being accidentally executed.
m["gpioCandidateNotice"]="All embedded descriptive candidate GPIO suggestions are superseded; only gpio_north_escape_v3.json is executable."
(R/"plans/mcu_critical_routes_v6.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
u=json.loads((R/"plans/usb_critical_routes_v5.json").read_text(encoding="utf-8"))
u["status"]="CANDIDATE_V6_2L_SHARED_CORNER_GAP_GE016"
old=next(o for o in u["commonOperations"] if o["id"]=="USB_SHARED_DM")
u["commonOperations"]=[o for o in u["commonOperations"] if o["id"]!="USB_SHARED_DM"]
u["variantOperations"]["4L"].append(old)
dm=copy.deepcopy(old);dm["points"]=[[39.4,18.3984],[39.4,18.97],[40.43,20],[40.43,21.6],[40.75,21.92],[40.75,22.75]]
dm["purpose"]+="; 2L .52mm trunk centers give .167696mm minimum45degree corner gap, not previous.153553 below selected.16 rule"
u["variantOperations"]["2L"].append(dm)
le=lambda p:sum(math.dist(a,b) for a,b in zip(p,p[1:]))
dp=next(o for o in u["commonOperations"] if o["id"]=="USB_SHARED_DP")
u["candidateLengths"]["sharedMCUSideByVariant"]={v:{"DP":le(dp["points"]),"DM":le(next(o for o in os if o["id"]=="USB_SHARED_DM")["points"]),"DPminusDM":le(dp["points"])-le(next(o for o in os if o["id"]=="USB_SHARED_DM")["points"])} for v,os in u["variantOperations"].items()}
u["candidateLengths"]["sharedMCUSide"]["scope"]="Historical4L/common throughv5; 2L current values insharedMCUSideByVariant"
u["candidateLengths"]["mainWholePlanarSkewByVariant"]={v:{o:u["candidateLengths"][o]["DPminusDM" if o=="orientationB" else"DPminusDM_planar"]+x["DPminusDM"] for o in ("orientationA","orientationB")} for v,x in u["candidateLengths"]["sharedMCUSideByVariant"].items()}
u["delayScaleEstimate"]["orientationA_wholeDataPathSkew_ps_range"]={v:[u["candidateLengths"]["mainWholePlanarSkewByVariant"][v]["orientationA"]*math.sqrt(er)/.299792458+y for er in(2.8,3.5)] for v,y in u["delayScaleEstimate"]["extraBarrelDelay_ps"].items()}
u["fabricationCornerCorrection"]="V5 .153553mm shared45corner below selected2L .16spacing (though barely above public.1524); v6 DMshift.02 left/end.02up preserves >=.16 without global relaxation. Fourlayer unchanged."
(R/"plans/usb_critical_routes_v6.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
power=json.loads((H/"engineering_power/power_star_03b.json").read_text(encoding="utf-8"))
esd=json.loads((H/"engineering_power/ESD_ground_routes_04b.json").read_text(encoding="utf-8"))
gp=json.loads((R/"plans/gpio_north_escape_v3.json").read_text(encoding="utf-8"))
for v in("4L","2L"):
 p=dict(m);p["placementChanges"]=m["placementChanges"]+u["placementChanges"];p["operations"]=m["operations"]+u["commonOperations"]+u["variantOperations"][v]+power["operations"]+gp["operations"]+esd["operations"]
 (R/f"plans/combined_v7_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v6_{v}.py").read_text(encoding="utf-8").replace("combined_v6","combined_v7")
 (R/f"review_combined_v7_{v}.py").write_text(s,encoding="utf-8")
 exec(compile(s,str(R/f"review_combined_v7_{v}.py"),"exec"))
print(json.dumps({"sharedMCU":u["candidateLengths"]["sharedMCUSideByVariant"],"fullskew":u["candidateLengths"]["mainWholePlanarSkewByVariant"]},ensure_ascii=True))
