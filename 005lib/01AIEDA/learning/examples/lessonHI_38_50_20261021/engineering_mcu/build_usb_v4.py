import pathlib,json,math,hashlib,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
u=json.loads((R/"plans/usb_critical_routes_v3.json").read_text(encoding="utf-8"))
u["status"]="CANDIDATE_V4_MINIMUM_MIRROR_WITH_TRUE_U4_PCB_FLOW_2L_GAP016"
u["commonOperations"] += [
 {"type":"route","id":"USB_U4_DP_FLOW","net":"USB_DP","layer":"TOP","points":[[41.2,10.1],[41.2,12.7]],"width":.2,"from":["U4","6"],"to":["U4","1"],"purpose":"ActualshortPCB copperflowthroughmatchingpads, noPIN_SHORT softwarewaiver. Packageinternalparallelconductorunknown; symmetric portwidth."},
 {"type":"route","id":"USB_U4_DM_FLOW","net":"USB_DM","layer":"TOP","points":[[39.3,10.1],[39.3,12.7]],"width":.2,"from":["U4","4"],"to":["U4","3"],"purpose":"ActualmatchingPCBflow, currentDRC/neck/ESDreturngeometrycheck."}]
for o in u["variantOperations"]["2L"]:
 pts=o["points"]
 if o["id"]=="USB2L_DP_PORT1":o["points"]=[[41.2,12.7],[41.2,13.905],[40.905,14.2]]
 if o["id"]=="USB2L_DM_PORT1":o["points"]=[[39.3,12.7],[39.3,13.905],[39.595,14.2]]
 if o["id"]=="USB2L_DP_WIDE":o["points"]=[[40.905,14.2],[40.905,15.6]]
 if o["id"]=="USB2L_DM_WIDE":o["points"]=[[39.595,14.2],[39.595,15.6]]
 if o["id"]=="USB2L_DP_PORT2":o["points"]=[[40.905,15.6],[41.1,15.795],[41.1,16.8236]]
 if o["id"]=="USB2L_DM_PORT2":o["points"]=[[39.595,15.6],[39.4,15.795],[39.4,16.8236]]
 if o["id"]=="USB_PULLUP_BRANCH":o["points"]=[[40.905,14.6],[41.3,14.6]]
u["twoLayerFabricationMinimum"]="OSH2L公开mincoppertrace/space.1524mm. Selectedactualgap.16mm, never.15; factorycapabilitydoesnotcertifyselectedfullboard. Fourlayerseparate.15 remains."
def le(p):return sum(math.dist(a,b) for a,b in zip(p,p[1:]))
lens={o["id"]:le(o["points"]) for o in u["commonOperations"] if o["type"]=="route"}
dpa=lens["USB_DP_ENTRY"]+lens["USB_DP_A6_TO_MIRROR"]+lens["USB_DP_B6_TO_MIRROR"]+lens["USB_DP_MIRROR_BOTTOM"]
b7leaf=1.245
dma=lens["USB_DM_ENTRY"]+lens["USB_DM_A7_MERGE"]-2*b7leaf
sharedDiff=lens["USB_SHARED_DP"]-lens["USB_SHARED_DM"]
u["candidateLengths"]={"units":"Planarcenterline geometry only; nativeactual pending; seriescomponentinternalpath excluded","method":"Splitnetatcommonmerge node. ForA7 do NOT traverse unused B7 leafandback; subtract2*1.245 from branch+canonicalentry sum.","orientationB":{"J2.B6_to_U4.6":lens["USB_DP_ENTRY"],"J2.B7_to_U4.4":lens["USB_DM_ENTRY"],"DPminusDM":lens["USB_DP_ENTRY"]-lens["USB_DM_ENTRY"]},"orientationA":{"J2.A6_to_U4.6_planar":dpa,"J2.A7_to_U4.4_planar":dma,"DPminusDM_planar":dpa-dma,"DPextraFullThroughViaCount":2},"sharedMCUSide":{"R5.1_to_U1.33":lens["USB_SHARED_DP"],"R6.1_to_U1.32":lens["USB_SHARED_DM"],"DPminusDM":sharedDiff},"protectedVariantRoutes":{v:{o["id"]:le(o["points"]) for o in os if o["type"]=="route"} for v,os in u["variantOperations"].items()},"eachCommonRoute":lens,"mainWholePlanarSkewExcludingEqualSeriesParts":{"orientationB":lens["USB_DP_ENTRY"]-lens["USB_DM_ENTRY"]+sharedDiff,"orientationA":dpa-dma+sharedDiff},"correction":"v3 terminalsum mistakenly double-counted unused B7 spur when computingA7shortestpath; corrected explicitmerge-node formulation. NoPCB execution depended onwrongcandidate length."}
u["delayScaleEstimate"]["orientationA_planarSkew_ps_range"]=[(dpa-dma)*math.sqrt(er)/.299792458 for er in (2.8,3.5)]
u["delayScaleEstimate"]["orientationA_entryTotalSkew_ps_range"]={v:[x+y for x in u["delayScaleEstimate"]["orientationA_planarSkew_ps_range"]] for v,y in u["delayScaleEstimate"]["extraBarrelDelay_ps"].items()}
u["delayScaleEstimate"]["orientationA_wholeDataPathSkew_ps_range"]={v:[(dpa-dma+sharedDiff)*math.sqrt(er)/.299792458+y for er in (2.8,3.5)] for v,y in u["delayScaleEstimate"]["extraBarrelDelay_ps"].items()}
u["geometryPrecheckContext"]="CombinewithMCUv5,powerstar03b (notoldcrossing03) andnewU4GND vias40.0,11.4/40.5,11.6. Earlier40.9,11.5 via would shorttrueDPflowcolumnx41.2."
(R/"plans/usb_critical_routes_v4.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
e=json.loads((R/"plans/usb_impedance_estimate.json").read_text(encoding="utf-8"));d=e["variants"]["2L"];d["selectedBulkGeometry"]["gap"]=.16
w,s,h,t,er=1.15,.16,1.524,.0356,4.5
z0=87/math.sqrt(er+1.41)*math.log(5.98*h/(.8*w+t))
d["cases"].append({"width":w,"gap":s,"Z0_ohm":z0,"Zdiff_ohm":2*z0*(1-.48*math.exp(-.96*s/h)),"selected":"True; .16>=public.1524 copperminimum"})
e["fabricationCorrection"]="Two-layer .15mm example retained only as rejectedcalculationbelowpublic.1524 minimum; selectedactualgap.16. Fourlayer.15 hasdifferentprocesscapability."
(R/"plans/usb_impedance_estimate.json").write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"entryLengths":{k:v for k,v in u["candidateLengths"].items() if k.startswith("orientation")},"wholeSkew":u["candidateLengths"]["mainWholePlanarSkewExcludingEqualSeriesParts"],"delays":u["delayScaleEstimate"],"2LselectedZ":d["cases"][-1]},ensure_ascii=True))
