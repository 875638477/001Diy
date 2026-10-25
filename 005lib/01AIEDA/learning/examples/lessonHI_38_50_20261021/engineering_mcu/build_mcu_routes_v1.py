import pathlib,json,hashlib,shutil,datetime,math,sys,os
B=pathlib.Path(r"D:\001DIY\005lib\01AIEDA");G=B/"learning/examples/lessonG_30_37_20261020";R=B/"learning/examples/lessonHI_38_50_20261021/engineering_mcu"
for x in ("source","runtime","plans","review"):(R/x).mkdir(parents=True,exist_ok=True)
os.environ["TMP"]=os.environ["TEMP"]=str(R/"runtime")
inputs=[B/"EDA.md",B/"\u8bfe\u7a0b\u7d22\u5f15.md",B/"learning/notes/record_location_rules.md",B/"learning/notes/lessonG_mcu_20261020.md",B/"learning/notes/lessonG_30_37_20261020.md",G/"inventory/normalized_actual_2L.json",G/"inventory/normalized_actual_4L.json",G/"engineering_mcu/local_copper_independent_final_review.json",G/"current/G_4L_LAYOUT_v1.brd",G/"current/G_2L_LAYOUT_v1.brd"]
manifest={"created":datetime.datetime.now().astimezone().isoformat(),"inputs":[{"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size} for p in inputs],"copiedSources":[],"failedReadOnlyPreparation":"Initial PowerShell stdin Python read of Chinese course-index literal became ???? under pipe encoding and raised OSError. No CAD operation. Replaced with UTF-8 script file/unicode escapes; original G and user project untouched."}
for name in ("AN2867_current.pdf","AN2867_current.txt","AN2586_current.pdf","AN2586_current.txt","DS5319_inherited.pdf","DS5319_inherited.txt","AN2834_current.pdf","AN2834_current.txt","ABM3B_inherited.pdf","ABM3B_inherited.txt"):
 p=G/"engineering_mcu/source"/name;q=R/"source"/name;shutil.copyfile(p,q)
 manifest["copiedSources"].append({"origin":str(p),"copy":str(q),"sha256":hashlib.sha256(q.read_bytes()).hexdigest()})
sys.path.insert(0,str(B/"learning/tools/pymupdf_1_28_2"));import fitz
for name,pages,url in (("TI_SLVA531A.pdf",[15],"https://www.ti.com/lit/an/slva531a/slva531a.pdf"),("USBLC6_DS4260.pdf",[1,5,6],"https://www.st.com/resource/en/datasheet/usblc6-2.pdf")):
 p=R/"source"/name
 with fitz.open(p) as d:
  (R/"source"/(p.stem+".txt")).write_text("\n".join(f"=== PDF_INDEX_1BASED {i+1} ===\n"+pg.get_text() for i,pg in enumerate(d)),encoding="utf-8")
  for i in pages:
   if i<=len(d): d[i-1].get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(R/"source"/f"{p.stem}_p{i:02}.png")
  manifest["copiedSources"].append({"url":url,"copy":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"pages":len(d),"rendered":pages})
(R/"input_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
ops=[]
def rt(id,net,pts,w,fr=None,to=None,purpose="",layer="TOP",**kw):
 q={"type":"route","id":id,"net":net,"layer":layer,"points":pts,"purpose":purpose}
 q["widths" if isinstance(w,list) else "width"]=w
 if fr:q["from"]=fr
 if to:q["to"]=to
 q.update(kw);ops.append(q)
def via(id,net,xy,purpose):ops.append({"type":"via","id":id,"net":net,"xy":xy,"padstack":"L28_VIA030_C060","purpose":purpose,"tentRequirement":"No mask aperture on TOP/BOTTOM unless explicitly outside body and qualified; verify Artwork drawMissingPadApertures and actual aperture data."})
rt("HSE_IN","OSC_IN",[[40.75,31.25],[40.75,32.3],[43,32.3],[44.4,33.7]],.2,["U1","5"],["Y1","1"],"Short high-impedance input, source entry port then quiet island; north GPIO must not cross")
rt("HSE_IN_LOAD","OSC_IN",[[44.4,33.7],[44.7,34.0],[46.2,34.0]],.2,["Y1","1"],["C22","1"],"No test branch; load capacitor at resonator side")
rt("HSE_OUT","OSC_OUT",[[40.25,31.25],[40.25,32.15],[40.2,32.2],[40.2,33.2]],.2,["U1","6"],["R31","1"],"Retain series component; no unrequested calculated drive resistor")
rt("HSE_XTAL_OUT","XTAL_OUT",[[40.2,34.7748],[40.2,37.7],[42,37.7]],.2,["R31","2"],["Y1","3"],"Inside oscillator shadow only")
rt("HSE_OUT_LOAD","XTAL_OUT",[[40.2,37.7],[39.8,37.7]],.2,["R31","2"],["C23","1"],"Branch at output arm not long test stub")
via("HSE_LOCAL_C22","GND",[47.1,35.5748],"ONLY local quiet island; global GND void on all copper layers traversed")
via("HSE_LOCAL_C23","GND",[37.7,37.7],"ONLY local quiet island; global GND void on all copper layers traversed")
via("HSE_SINGLE_ANCHOR","GND",[43.0,29.25],"ONLY local island neck; TOP sole connection to digital VSS47; global planes excluded here too")
rt("HSE_C22_RETURN","GND",[[46.2,35.5748],[47.1,35.5748]],.6,["C22","2"],None,"Quiet cap ground into local island only")
rt("HSE_C23_RETURN","GND",[[38.2252,37.7],[37.7,37.7]],.6,["C23","2"],None,"Quiet cap ground into local island only")
rt("HSE_UNIQUE_TOP_ANCHOR","GND",[[44.25,29.25],[43.0,29.25]],.25,["U1","47"],None,"Sole removable 1.25mm TOP anchor; local 1.4 neck + .20 spacing; do not add any other quiet/global bridge",isolationChallengeTarget=True)
rt("HSE_GUARD_LEFT_NORTH","GND",[[37.7,37.7],[37,37.7],[37,39.8],[42.2,39.8]],.6,["C23","2"],None,"Quiet TOP guard; intentionally open case-ground escape port x42.2..44.2")
rt("HSE_GUARD_RIGHT_NORTH","GND",[[47.1,35.5748],[47.8,35.5748],[47.8,39.8],[44.2,39.8]],.6,["C22","2"],None,"Quiet TOP guard with separate case-return opening")
rt("HSE_GUARD_RIGHT_LOWER","GND",[[47.8,35.5748],[47.8,33.5]],.6,None,None,"Quiet guard stops below C17 application ground, does not contact it")
via("HSE_CASE_APP","GND",[43.2,40.8],"Application GND OUTSIDE local moat; must remain reached after unique TOP anchor deletion")
rt("HSE_CASE4_APP","GND",[[42,33.7],[42,34.8],[43.2,36.0],[43.2,40.8]],.6,["Y1","4"],None,"Metal case application return, separate from quiet guard and local vias")
rt("HSE_CASE2_APP","GND",[[44.4,37.7],[43.2,38.9],[43.2,40.8]],.6,["Y1","2"],None,"Case branch through north guard opening; no guard intersection")
rt("VDDA_PIN_CAP","VDDA",[[38.75,31.25],[38.75,32.55],[38.1,33.2],[37,33.2]],[.25,.6,.6],["U1","9"],["C18","1"],"1.30mm whole pin-centered neck, then .60; explicit north spacing exception .20 only")
rt("VDDA_CAP_BULK","VDDA",[[37,33.2],[36.5,33.2],[35.9,33.8],[35.9,35.9],[34.8,37]],.6,["C18","1"],["C19","1"],"Pass real gap between shifted C24 and C18; .3935 each-side copper margin")
rt("VDDA_BULKS","VDDA",[[34.8,37],[32.2,37]],.6,["C19","1"],["C20","1"],"Local low-frequency reservoir")
rt("VDDA_FILTER","VDDA",[[32.2,37],[31.4,37],[30.9,37.5],[30.9,38.1748],[30.5,38.5748],[29.5,38.5748]],.6,["C20","1"],["R26","2"],"Avoid R26 V3V3 pad1 and C20 GND pad2")
via("VSSA8_APP","GND",[39.7,29.6],"Application reference under MCU, not oscillator island")
rt("VSSA8_INWARD","GND",[[39.25,31.25],[39.25,30.05],[39.7,29.6]],[.25,.6],["U1","8"],None,"Pin-centered inward escape: 1.2 neck then wide; local north .20 spacing")
for id,xy,fr,pts in [
 ("C18_APP_GND",[37.9,34.7748],["C18","2"],[[37,34.7748],[37.9,34.7748]]),
 ("C19_APP_GND",[34.8,39.7],["C19","2"],[[34.8,38.5748],[34.8,39.7]]),
 ("C20_APP_GND",[32.2,40.1],["C20","2"],[[32.2,39.032],[32.2,40.1]]),
 ("C24_APP_GND",[34.8,35.8],["C24","2"],[[34.8,34.5748],[34.8,35.8]]),
 ("C21_APP_GND",[39,35.4],["C21","2"],[[39.3764,36.25],[39,35.8736],[39,35.4]])]:
 via(id,"GND",xy,"Application plane outside all oscillator voids; offpad/tented as needed")
 rt(id+"_TRACE","GND",pts,.6,fr,None,"Short independent application return, never local oscillator island")
rt("ADC_PIN_CAP","ADC0",[[38.25,31.25],[38.25,32.2],[35.6,32.2],[34.8,33]],.2,["U1","10"],["C24","1"],"No reference slot; local north exception only for fine-pitch power neighbor")
rt("ADC_CAP_SERIES","ADC0",[[34.8,33],[32.8,35],[32.6764,35]],.2,["C24","1"],["R32","2"],"Keep RC on MCU side; avoids C24.GND2")
rt("ADC_INPUT","ADC_IN",[[31.1016,35],[30.8,35],[29.8,34],[26.27,34]],.2,["R32","1"],["J10","1"],"Quiet paired-return input, no SW/buck corridor")
rt("NRST_PIN_CAP","NRST",[[39.75,31.25],[39.75,32.05],[38.2,33.6],[38.2,35.8516],[37.8016,36.25]],.2,["U1","7"],["C21","1"],"After C21 move avoids VDDA cap pad and quiet island/moat; reset capacitor ~5.8mm route engineering tradeoff")
via("NRST_SERVICE","NRST",[38.2,35.4],"Branch service net only after local C21; BOTTOM route outside HSE shadow, layer permission explicit")
rt("NRST_SERVICE_TAP","NRST",[[37.8016,36.25],[38.2,35.8516],[38.2,35.4]],.2,["C21","1"],None,"Branch to R27/J7/J9 routed later outside reserved oscillator area")
rt("VBAT_PIN_CAP","V3V3",[[42.75,31.25],[43.55,31.25],[45.05,31.25],[46.2,32.4],[46.2016,32.4]],[.25,.6,.6,.6],["U1","1"],["C17","1"],"VBAT tied V3V3 needs own100nF; inward/side escape does not cross OSC_IN")
via("VBAT_C17_APP","GND",[48.9,32.4],"Application GND outside oscillator moat, not quiet guard")
rt("VBAT_C17_RETURN","GND",[[47.7764,32.4],[48.9,32.4]],.6,["C17","2"],None,"Keep application decoupling return outside quiet island")
island=[[42.65,28.9],[43.35,28.9],[43.35,31.95],[47.5,31.95],[47.5,39.4],[37.2,39.4],[37.2,36.8],[40.0,36.8],[40.0,32.8],[40.6,32.8],[40.6,31.95],[42.65,31.95]]
void=[[42.30,28.55],[43.70,28.55],[43.70,31.60],[47.85,31.60],[47.85,39.75],[36.85,39.75],[36.85,36.45],[39.65,36.45],[39.65,32.45],[40.25,32.45],[40.25,31.60],[42.30,31.60]]
plan={"status":"CANDIDATE_V1_NATIVE_GEOMETRY_DRC_AND_ISOLATION_CHALLENGE_PENDING","date":"2026-10-21","scope":"HI38-50 MCU/HSE/ADC/NRST first batch; native sole executor f29; not all-board routing or manufacturing approval","sourceG":str(G),"units":"mm","placementChanges":[{"ref":"C21","xy":[37.7,36.25],"rotation":0,"purpose":"Free blocked VDDA/ADC short TOP corridor; PlaceBound gaps to R31/C18 about.104 and C23 .129, not physical body/assembly certification"},{"ref":"C24","xy":[34.8,32.8984],"rotation":90,"purpose":"Shift left .2 so .60 VDDA branch atx35.9 has actual .3935mm to each GND/ADC pad edge"}],"operations":ops,"oscillatorReference":{"net":"GND","islandPolygon":island,"applicationGroundVoidPolygon":void,"localLayer":{"2L":"BOTTOM","4L":"L2"},"allOtherCopperLayers":"No application-GND metal under local HSE vias or inside moat; explicit void on any global L3/BOTTOM/TOP pour. Allow only quiet TOP routes/guard and separate case traces without connecting intersection.","singleBridgeOperation":"HSE_UNIQUE_TOP_ANCHOR","allThroughViaPadChecks":["HSE_LOCAL_C22","HSE_LOCAL_C23","HSE_SINGLE_ANCHOR"],"negativeChallenge":"Transaction delete only HSE_UNIQUE_TOP_ANCHOR: C22.2/C23.2/quiet shape/guard still mutually connected; must no longer reach global GND/VSS47/case; Y1.2/.4 still reach application GND and not quiet shape. Restore transaction; redo current DRC/update and save/reopen proof.","guardPort":"North x42.2..44.2 intentionally open for case return; source ports south for oscillator nets; do not bridge with same-net fills"},"regions":[{"id":"HI_MCU_NORTH_ESCAPE","layer":"TOP","polygon":[[37.7,29.25],[43.9,29.25],[43.9,32.9],[37.7,32.9]],"purpose":"Only short fine-pitch north MCU entries; narrow to actual per-net route after native feedback","bindings":[{"netClasses":["NC_ANALOG_SENSITIVE_S","NC_OSCILLATOR_S","NC_POWER_LV_S"],"spacingCopyFrom":"their own source CSet","change":{"smdpin_line":.20,"line_line":.20},"preserve":"All other rules and global.30 unchanged; class-pair exceptions separately readback where applicable"},{"netClasses":["VDDA","GND","V3V3"],"physicalChange":{"necklength_max":1.4},"preserve":"Other P_POWER/P_GND fields; exact net/class scope, no global width waiver"}]},{"id":"HI_OSC_RETURN_ESCAPE","layer":"TOP","polygon":[[42.7,28.8],[44.9,28.8],[44.9,29.65],[42.7,29.65]],"allowedNets":["GND"],"physicalCopyFrom":"P_GND_PLANE or 2L GND equivalent","change":{"necklength_max":1.4},"spacingChanges":{"line_line":.2,"smdpin_line":.2},"purpose":"Pin47 inward quiet island anchor1.25mm, not a global relaxation"}],"reservedAreas":[{"id":"HSE_QUIET_SHADOW","polygon":void,"allowedNets":["OSC_IN","OSC_OUT","XTAL_OUT","GND"],"forbidden":"PC13/14/15, SPI/I2C/USB/clock/test branches and unrelated power/returns on all layers; case GND only defined separate TOP path; quiet/app GND not interchangeable"},{"id":"ADC_TOP_CORRIDOR","polygon":[[26,31.8],[39,31.8],[39,39.8],[26,39.8]],"allowedNets":["ADC_IN","ADC0","VDDA","GND","NRST"],"purpose":"Not blanket route keepout, prioritize measured paths and return over arbitrary ordinary digital cut"}],"gpioNorthEscape":{"pins":[["U1","2"],["U1","3"],["U1","4"]],"strategy":"Inward TOP axial toward MCU body to offpad throughvia, then BOTTOM under MCU and south/west of HSE moat, return TOP outside shadow. Explicit BOTTOM permission on those nets; GND return near transitions; 2L add measured TOP reference copper and avoid slicing appground. Native must allocate nonoverlapping via sites (not all same y at .5 pitch) after current obstacles; do not just send north across OSC_IN."},"acceptance":["Native all lines/pads/vias/nets readback and independent exact geometry","Current dynamic fill/DRC and explicit applicable CSet fields, no blanket waiver","Physical shape polygons and moat with all throughvia layer pads verified","Only unique intentional oscillator-to-application GND anchor; reversible isolation challenge","HSE startup/CL/drive/effective capacitor tolerance and real assembly remain open"]}
(R/"plans/mcu_critical_routes_v1.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"operations":len(ops),"routes":sum(o["type"]=="route" for o in ops),"vias":sum(o["type"]=="via" for o in ops),"plan":str(R/"plans/mcu_critical_routes_v1.json"),"sources":len(manifest["copiedSources"])},ensure_ascii=True))
