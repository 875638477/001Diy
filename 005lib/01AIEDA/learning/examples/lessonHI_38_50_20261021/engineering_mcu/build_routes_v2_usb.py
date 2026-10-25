import pathlib,json,math,datetime,hashlib
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
p=json.loads((R/"plans/mcu_critical_routes_v1.json").read_text(encoding="utf-8"))
p["status"]="CANDIDATE_V2_NATIVE_DRC_AND_ISOLATION_PENDING";p["supersedes"]="v1 HSE anchor conflicts with new internal V3V3 star; original kept for audit, do not execute old anchor."
for o in p["operations"]:
 if o["id"]=="HSE_SINGLE_ANCHOR":o["xy"]=[45.45,30.1]
 if o["id"]=="HSE_UNIQUE_TOP_ANCHOR":
  o["points"]=[[45.05,29.25],[45.45,29.65],[45.45,30.1]];o.pop("width",None);o["widths"]=[.25,.6];o["purpose"]="Only new anchor from EXISTING VSS47/C15 branch at45.05,29.25. Retained first .8 + new .565685 neck=1.365685; wide final .45. Fits prior1.4; isolated via is clear of existing GND route. Delete these 2 segments for local-island negative test."
 if o["id"]=="VSSA8_APP":o["xy"]=[38.7,29.5]
 if o["id"]=="VSSA8_INWARD":o["points"]=[[39.25,31.25],[39.25,30.05],[38.7,29.5]]
 if o["id"]=="VBAT_PIN_CAP":o["points"]=[[42.75,31.25],[43.55,31.25],[46.2016,31.25],[46.2016,32.4]];o["widths"]=[.25,.6,.6]
p["oscillatorReference"]["islandPolygon"]=[[45.1,29.75],[45.8,29.75],[45.8,31.25],[45.1,31.95],[45.3,31.95],[45.3,33.2],[47.5,33.2],[47.5,39.4],[37.2,39.4],[37.2,36.8],[40.0,36.8],[40.0,32.8],[40.6,32.8],[40.6,31.95],[44.4,31.95],[45.1,31.25]]
p["oscillatorReference"]["applicationGroundVoidPolygon"]=[[44.75,29.4],[46.15,29.4],[46.15,31.4],[45.65,31.9],[45.65,32.85],[47.85,32.85],[47.85,39.75],[36.85,39.75],[36.85,36.45],[39.65,36.45],[39.65,32.45],[40.25,32.45],[40.25,31.6],[44.25,31.6],[44.75,31.1]]
p["oscillatorReference"]["neckProjectionException"]="Main HSE shadow excludes C17 app decoupling via/right-bottom notch. The narrow GND connection neck near source VSS47 can have a short nearby/projecting VBAT feed in dense source escape; it is not an unrelated digital route corridor or a claim of zero field coupling."
for x in p["reservedAreas"]:
 if x["id"]=="HSE_QUIET_SHADOW":
  x["polygon"]=p["oscillatorReference"]["applicationGroundVoidPolygon"]
  x["sourceEscapeException"]="Only short VBAT/VDD source-area feed near narrow grounding neck as separately checked; no PC13/14/15 or arbitrary fast signal crossing."
for x in p["regions"]:
 if x["id"]=="HI_OSC_RETURN_ESCAPE":x["polygon"]=[[44.8,29.1],[45.85,29.1],[45.85,30.5],[44.8,30.5]]
p["gpioNorthEscape"]["candidateTOPFanouts"]=[
 {"ref":"U1","pin":"2","net":"GPIO_PC13","points":[[42.25,31.25],[42.25,29.85],[42,29.6]],"width":.2,"via":[42,29.6]},
 {"ref":"U1","pin":"3","net":"GPIO_PC14","points":[[41.75,31.25],[41.75,30.3],[40.9,29.45],[40.9,29.3]],"width":.2,"via":[40.9,29.3]},
 {"ref":"U1","pin":"4","net":"GPIO_PC15","points":[[41.25,31.25],[41.25,30.85],[39.9,29.5],[39.9,28.6]],"width":.2,"via":[39.9,28.6]}]
p["gpioNorthEscape"]["candidateBOTTOMFirstEscape"]=[
 {"net":"GPIO_PC13","points":[[42,29.6],[42,30.2],[41.1,31.1],[36.4,31.1]]},
 {"net":"GPIO_PC14","points":[[40.9,29.3],[40.9,30.3],[36,30.3]]},
 {"net":"GPIO_PC15","points":[[39.9,28.6],[39.8,28.7],[35.6,28.7]]}]
p["gpioNorthEscape"]["acceptance"]="These are candidate staggered fanouts only; native actual GND vias/plane/return/crossings further west must be read back. BOTTOM TOP-reference copper essential2L;4L L3 actual plane and nearby return transition vias required. Do not claim whole net complete from these partial escape points."
(R/"plans/mcu_critical_routes_v2.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
def z(w,s,h,t,er):
 z0=87/math.sqrt(er+1.41)*math.log(5.98*h/(.8*w+t))
 return {"Z0_ohm":z0,"Zdiff_ohm":2*z0*(1-.48*math.exp(-.96*s/h))}
est={"status":"ANALYTIC_PRELAYOUT_ESTIMATE_NOT_90OHM_CERTIFICATION","source":"TI SLVA531A p15 eq1/2","formula":"Z0=87/sqrt(Er+1.41)*ln(5.98H/(0.8W+T));Zdiff=2Z0*(1-0.48exp(-0.96S/H))","units":"All dimensions same mm; log natural","notModeled":["mask/conductive roughness/trapezoid/etch/tolerance/nearbycoplanarGND/vias/pads/bends/reference open gaps","Dk dispersion:2L4.5 source10MHz;4L4.4 frequency notpublished","actual differential coupling outside straightparallel regions; connector and ESD discontinuities"],"variants":{}}
for v,h,t,er,w in [("2L",1.524,.0356,4.5,1.15),("4L",.2104,.035,4.4,.26)]:
 vals=[]
 for ww,ss in [(.2,.15),(w,.15),(w,.2)]:
  vals.append({"width":ww,"gap":ss,**z(ww,ss,h,t,er)})
 est["variants"][v]={"H":h,"T":t,"Er":er,"reference":"BOTTOM" if v=="2L" else"L2","selectedBulkGeometry":{"width":w,"gap":.15},"cases":vals}
(R/"plans/usb_impedance_estimate.json").write_text(json.dumps(est,ensure_ascii=False,indent=2),encoding="utf-8")
usb={"status":"CANDIDATE_V1_ALL_NATIVE_COPPER_MASK_REFERENCE_AND_MATCHING_PENDING","units":"mm","placementChanges":[{"ref":"U4","xy":[40.25,11.4],"rotation":180,"purpose":"Create1.62mm raw y gap J2 tips→U4 input copper; preserve short ESD entry"},{"ref":"R5","xy":[41.1,18.5],"rotation":270,"purpose":"Symmetric toR6 aroundx40.25 and clearC14"},{"ref":"R12","xy":[42.8,18.3],"rotation":0,"purpose":"Reduce DNP CAN shared stub"},{"ref":"R13","xy":[38,18.3],"rotation":180,"purpose":"Reduce DNP CAN shared stub"},{"ref":"R11","xy":[42.7,14.5],"rotation":270,"purpose":"USB DP pullup branch nearU4 output: pad2=(42.7,12.8236), short1.5mm off-main branch; Q2 slowfeed may longer"}],"commonOperations":[],"variantOperations":{},"rulesNeeded":[{"id":"HI_J2_MIRROR_BOTTOM","scope":"USB_DP only, BOTTOM short connector mirror bridge, rectangle x39.35..41.15 y5.3..6.7","change":"Allow BOTTOM in explicit Region-Class Physical CSet; preservevia whitelist/spacing/width; verify via-count2","reason":"Existing P_USB_PROVISIONAL forbids BOTTOM; cannot silently violate"},{"id":"HI_USB_MCU_ESCAPE","scope":"TOP rectangle x39.8..41.6 y21.2..23.4, USB class vs ordinary digital class only","change":"Region-Class-Class copyS_USB_OTHER_050: smdpin_line/line_line .20 only; originaloutside.50 kept; other fields unchanged","reason":"AdjacentUART31/SWD34 pad .3 at.5pitch gives.25 edge gap for.2line, so global.5 cannot apply tofirstescape"},{"id":"HI_USB_PORT_BREAKOUT","scope":"Named J2/U4/R5R6/U1 short port regions only","change":"Normalwidth.20 atports, separate bulk2L1.15 or4L.26. Length budget derived native; no fullrun neck falsely<=1mm.","reason":"Wide2L strips cannot fit fine-pitch pads and local ports; nonuniformimpedance explicit."}],"referenceAndReturn":{"2L":"For BOTTOM mirror branch, add real TOP application-GND reference patch underconnector minusallTOPsignalclearances, tie toBOTTOMvia pair; sample coverage to expose unavoidable local cutout at TOP DM bridge and viaantipads. This is a real local discontinuity, not a fullyuniformmicrostrip. MainTOPpair sees BOTTOM actualGND without longslots.","4L":"MainTOP seesL2; BOTTOMmirror sees actualL3 GND (must create ifabsent) withreturnviasnearbothends connectingL2/L3/TOP. Viaantipads still localdiscontinuities to measure.","returnVias":[[38.15,5.8],[41.7,5.8]],"topReferencePatch":[[37.7,4.3],[42.2,4.3],[42.2,6.6],[37.7,6.6]],"clearances":"Actualpad/line/mask checks includingNPTH pegs, connectorbody and shell; neverfloodTOPreference over same-layerUSB signals"},"maskAndAssembly":"Signal andground underconnector vias must be tented/no opening in actualMASKfilm. Nullmask pad definition alone insufficient ifArtworkdrawMissingPadAperturescreatesholes. If fallback actualtentvariant needed createprivateHIpadstack andaddapprovedvia list, no publiclib edits. Connectorunderside metalclearance/maskprocess remainmanufacturing open.","dnpStubs":"R12/R13 retained separate pads and nets evenDNP. Route shared side from R5.1/R6.1 node as short explicit offmain branches; do not carry USB main through CAN branch, do not deleteorignorepads. Measure maxstub native; DNP=openscomponent, not absentPCB copper.","matching":"Evaluate both TypeC orientation terminal paths (B6/B7 andA6/A7), USB PCB andPA sharedsegments separately, add package/seriescomp discontinuity asunknown. No snakejust to equal totalnetcopper includingbranches; matching cannotreplace reference/impedance.","manufacturingRelease":False}
def route(id,net,pts,w,fr=None,to=None,layer="TOP",purpose=""):
 d={"type":"route","id":id,"net":net,"layer":layer,"points":pts,"width":w,"purpose":purpose}
 if fr:d["from"]=fr
 if to:d["to"]=to
 return d
def vv(id,net,xy,purpose):return {"type":"via","id":id,"net":net,"xy":xy,"padstack":"L28_VIA030_C060_OR_VERIFIED_TENTED_PRIVATE_VARIANT","purpose":purpose,"mustBeTented":True}
common=usb["commonOperations"]
common.extend([vv("USB_DP_MIRROR_A","USB_DP",[39.75,5.8],"Underhousing tented"),vv("USB_DP_MIRROR_B","USB_DP",[40.75,5.8],"Underhousing tented"),
 route("USB_DP_A6_TO_MIRROR","USB_DP",[[39.75,7.355],[39.75,5.8]],.2,["J2","A6"]),
 route("USB_DP_B6_TO_MIRROR","USB_DP",[[40.75,7.355],[40.75,5.8]],.2,["J2","B6"]),
 route("USB_DP_MIRROR_BOTTOM","USB_DP",[[39.75,5.8],[39.75,6.1],[39.95,6.3],[40.55,6.3],[40.75,6.1],[40.75,5.8]],.2,layer="BOTTOM",purpose="Short1.765685mm branch compensates intrinsic TypeC mirror orientation budget without extra via; compare simpler straight1mm option"),
 route("USB_DM_A7_MERGE","USB_DM",[[40.25,7.355],[40.25,6.6],[40.15,6.5],[40.15,5.1],[39.15,5.1],[39.15,6.5],[39.25,6.6],[39.25,7.355]],.2,["J2","A7"],["J2","B7"],purpose="Short mirrored topU branch5.5928mm underhousing, noextra vias;balancesTypeCorientationwithin1mmcandidate. Compare directnorthmerge2.245mm option ifmatchingbudgetexplicitlyrelaxed."),
 route("USB_DP_ENTRY","USB_DP",[[40.75,7.355],[40.75,8.6],[41.2,9.05],[41.2,10.1]],.2,["J2","B6"],["U4","6"],purpose="Directflowthroughprotection input"),
 route("USB_DM_ENTRY","USB_DM",[[39.25,7.355],[39.25,8.6],[39.3,8.65],[39.3,10.1]],.2,["J2","B7"],["U4","4"],purpose="Directflowthroughprotection input"),
 route("USB_PULLUP_BRANCH","USB_DP",[[41.2,12.7],[42.5764,12.7],[42.7,12.8236]],.2,["U4","1"],["R11","2"],purpose="Required FS pullup keptshort; not CANtestbranch"),
 route("USB_SHARED_DP","PA12_SHARED",[[41.1,18.3984],[41.1,19.85],[40.95,20.0],[40.95,21.6],[41.25,21.9],[41.25,22.75]],.2,["R5","1"],["U1","33"],purpose="PassleftofC14groundloop, .2finepitchport; preservelocalclasspairexception"),
 route("USB_SHARED_DM","PA11_SHARED",[[39.4,18.3984],[39.4,18.95],[40.45,20.0],[40.45,21.6],[40.75,21.9],[40.75,22.75]],.2,["R6","1"],["U1","32"],purpose="NoCANtrunk; routewithDPgeometrycheck, skewnotassumed"),
 route("USB_DNP_STUB_DP","PA12_SHARED",[[41.1,18.3984],[42.8032,18.3984],[42.9016,18.3]],.2,["R5","1"],["R12","1"],purpose="ExplicitDNPoffmainstub~1.8424mm"),
 route("USB_DNP_STUB_DM","PA11_SHARED",[[39.4,18.3984],[37.9968,18.3984],[37.8984,18.3]],.2,["R6","1"],["R13","1"],purpose="ExplicitDNPoffmainstub~1.5424mm"),
 vv("USB_RETURN_LEFT","GND",[38.15,5.8],"ActualTOP/BOTTOM/L2/L3 applicationreturn; outside signalvia antipads"),vv("USB_RETURN_RIGHT","GND",[41.7,5.8],"ActualTOP/BOTTOM/L2/L3 applicationreturn; outside signalvia antipads")])
usb["variantOperations"]["4L"]=[
 route("USB4L_PROTECTED_DP","USB_DP",[[41.2,12.7],[41.2,13.3],[40.455,14.045],[40.455,15.7],[41.1,16.345],[41.1,16.8236]],.26,["U4","1"],["R5","2"],purpose="TIformula~90ohm straightbulk.26/.15, portsuncoupled andnearbycoppernotmodeled"),
 route("USB4L_PROTECTED_DM","USB_DM",[[39.3,12.7],[39.3,13.3],[40.045,14.045],[40.045,15.7],[39.4,16.345],[39.4,16.8236]],.26,["U4","3"],["R6","2"],purpose="SymmetrictonativeDPcandidate")
]
usb["variantOperations"]["2L"]=[
 route("USB2L_DP_PORT1","USB_DP",[[41.2,12.7],[41.2,13.9],[40.9,14.2]],.2,["U4","1"],purpose="Shortnarrowportexplicitlynonuniform"),
 route("USB2L_DM_PORT1","USB_DM",[[39.3,12.7],[39.3,13.9],[39.6,14.2]],.2,["U4","3"],purpose="Symmetricnarrowport"),
 route("USB2L_DP_WIDE","USB_DP",[[40.9,14.2],[40.9,15.6]],1.15,purpose="Onlyfreeparallelbulksegment,w1.15gap.15,h1.524; notwholepath90"),
 route("USB2L_DM_WIDE","USB_DM",[[39.6,14.2],[39.6,15.6]],1.15,purpose="Same geometry; native neighboring copper and transitionspending"),
 route("USB2L_DP_PORT2","USB_DP",[[40.9,15.6],[41.1,15.8],[41.1,16.8236]],.2,to=["R5","2"],purpose="Symmetricwidthtransition/tapercandidate"),
 route("USB2L_DM_PORT2","USB_DM",[[39.6,15.6],[39.4,15.8],[39.4,16.8236]],.2,to=["R6","2"],purpose="Finepadbreakoutnot1.15mm"),
]
def length(a):return sum(math.dist(x,y) for x,y in zip(a,a[1:]))
usb["candidateLengths"]={o["id"]:length(o["points"]) for o in common if o["type"]=="route"}
usb["candidateLengths"]["orientationB_entrySkew"]=usb["candidateLengths"]["USB_DP_ENTRY"]-usb["candidateLengths"]["USB_DM_ENTRY"]
usb["candidateLengths"]["orientationA_entrySkew"]=usb["candidateLengths"]["USB_DP_ENTRY"]+2*1.555+usb["candidateLengths"]["USB_DP_MIRROR_BOTTOM"]-usb["candidateLengths"]["USB_DM_ENTRY"]-usb["candidateLengths"]["USB_DM_A7_MERGE"]
usb["criticalLimit"]="2Lwidebulk only1.4mm long: most connector/ESD/resistor/MCUbreakouts remain narrow andnonuniform; cannot claimwhole2L90ohm. ActualMask/Dk/tolerances/returnvoids andmanufacturerconfirmation remainopen. Retainroutegeometryaslearningcomparison; fourlayerpreferredphysicalreference."
(R/"plans/usb_critical_routes_v1.json").write_text(json.dumps(usb,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"mcuV2":str(R/"plans/mcu_critical_routes_v2.json"),"usbPlan":str(R/"plans/usb_critical_routes_v1.json"),"impedance":est["variants"],"orientationSkew":{k:v for k,v in usb["candidateLengths"].items() if k.startswith("orientation")}},ensure_ascii=True))
