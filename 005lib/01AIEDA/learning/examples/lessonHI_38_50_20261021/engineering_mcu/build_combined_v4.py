import pathlib,json,math,hashlib,shutil
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
u=json.loads((R/"plans/usb_critical_routes_v4.json").read_text(encoding="utf-8"))
m=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"))
power=json.loads((H/"engineering_power/power_star_03b.json").read_text(encoding="utf-8"))
gops=[]
for z in m["gpioNorthEscape"]["candidateTOPFanouts"]:
 gops += [{"type":"route","id":"GPIO_"+z["net"]+"_TOP","net":z["net"],"layer":"TOP","points":z["points"],"width":.2,"from":["U1",z["pin"]],"purpose":"Shortinsideescape; noHSEshadowcross"},{"type":"via","id":"GPIO_"+z["net"]+"_VIA","net":z["net"],"xy":z["via"],"padstack":"L28_VIA030_C060","purpose":"OffpadunderLQFP; masktent/return/referencecheck"}]
for z in m["gpioNorthEscape"]["candidateBOTTOMFirstEscape"]:
 gops.append({"type":"route","id":"GPIO_"+z["net"]+"_BOTTOM_START","net":z["net"],"layer":"BOTTOM","points":z["points"],"width":.2,"purpose":"OnlypartialwestescapeunderMCU, completeordinaryGPIOoutsideHSEmoat;2LactualTOPreferencecoverageandgaplengthmustbechecked"})
for id,xy in [("GPIO_RETURN_EAST",[42,28.6]),("GPIO_RETURN_WEST",[40,27.5])]:
 gops.append({"type":"via","id":id,"net":"GND","xy":xy,"padstack":"L28_VIA030_C060","purpose":"NearbyapplicationGNDreturn tiesactualTOPreference to2LBOTTOM or4LL2/L3. Physicalplaneconnectivityrequired."})
gp={"status":"CANDIDATE_PARTIAL_ESCAPE_NATIVE_PENDING","operations":gops,"localRule":"Preserve ordinarydigital.2; finepitchvsoscillator/power parent.3 needsnorthregionexception only","reference":"FourlayerBOTTOM needsrealL3reference;2LBOTTOM needsactualTOPapplicationGNDpatch minusallpad/clines, measure gaps causedbyotherMCUescape slots, donotclaimcontinuousreferencefromabstractrectangle.","topReferenceCandidatePolygon":[[35.8,27],[42.4,27],[42.4,31.9],[35.8,31.9]],"furtherRouting":"Westescape endpointsareunfinished, not completeGPIOconnections. Continuewest/northoutsideADCcurrentcorridor andHSEmoat withactualreturnreview."}
(R/"plans/gpio_north_escape_v1.json").write_text(json.dumps(gp,ensure_ascii=False,indent=2),encoding="utf-8")
esd=[
 {"type":"via","id":"U4_GND_A","net":"GND","xy":[40,11.4],"padstack":"L28_VIA030_C060","purpose":"f28proposedbodyinsideparallelreturn,newU4pose"},
 {"type":"via","id":"U4_GND_B","net":"GND","xy":[40.5,11.6],"padstack":"L28_VIA030_C060","purpose":"f28proposedbodyinsideparallelreturn; >.203holeclear"},
 {"type":"route","id":"U4_GND_TRUNK","net":"GND","layer":"TOP","points":[[40.25,12.7],[40.25,11.6],[40.5,11.6]],"width":.6,"purpose":"ShortESDreturn"},
 {"type":"route","id":"U4_GND_A_LINK","net":"GND","layer":"TOP","points":[[40.25,11.6],[40.05,11.4],[40,11.4]],"width":.6,"purpose":"ShortparallelESDreturn"}
]
for v in ("4L","2L"):
 p=dict(m);p["placementChanges"]=m["placementChanges"]+u["placementChanges"];p["operations"]=m["operations"]+u["commonOperations"]+u["variantOperations"][v]+power["operations"]+gops+esd
 (R/f"plans/combined_v4_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/"review_v5_copper.py").read_text(encoding="utf-8")
 s=s.replace('p=json.loads((R/"plans/mcu_critical_routes_v5.json").read_text(encoding="utf-8"))',f'p=json.loads((R/"plans/combined_v4_screen_{v}.json").read_text(encoding="utf-8"))')
 s=s.replace('for v in ("4L","2L"):',f'for v in ("{v}",):').replace("mcu_v5_full_copper_screen.json",f"combined_v4_copper_screen_{v}.json")
 (R/f"review_combined_v4_{v}.py").write_text(s,encoding="utf-8")
 exec(compile(s,str(R/f"review_combined_v4_{v}.py"),"exec"))
(R/"review/inputs").mkdir(exist_ok=True)
records=[]
for v in ("4L","2L"):
 source=H/f"inventory/normalized_actual_{v}.json";sha=hashlib.sha256(source.read_bytes()).hexdigest()
 dest=R/f"review/inputs/normalized_{v}_{sha[:12]}.json";shutil.copyfile(source,dest);records.append({"source":str(source),"archive":str(dest),"sha256":sha})
(R/"review/inputs/manifest.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
print("combinedv4includesMCUv5USBv4power03bGPIOESD; input snapshots archived.")
