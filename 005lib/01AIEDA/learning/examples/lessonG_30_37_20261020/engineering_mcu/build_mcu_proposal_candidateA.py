import os,json,pathlib,math,hashlib,itertools
ROOT=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu")
os.environ["TMP"]=os.environ["TEMP"]=str(ROOT/"runtime")
G=ROOT.parent
inventory=G/"inventory/inventory_4L.json"
d=json.loads(inventory.read_text(encoding="utf-8-sig"))
components={c["ref"]:c for c in d["components"]}
P=[
("U1",[40,27],270,"MCU USB32/33 toward bottom edge; clock/ADC toward upper quiet area"),
("C13",[33.4,23.5984],90,"100nF for U1.24/23; outside left side"),
("C14",[44.0016,20.3],180,"100nF for U1.36/35; shifted right to preserve USB x40.75..41.25 corridor"),
("C15",[46.5,30.4016],270,"100nF for U1.48/47; outside right side"),
("C16",[49.5,30.3],270,"10uF VDD3 bulk; effective capacitance >=4.7uF remains procurement gate"),
("C17",[44.2,33.0],0,"VBAT1 100nF; connected V3V3, no backup battery"),
("C18",[37.2,32.8984],90,"VDDA9 10nF closest high-frequency bypass; VSSA8 return zone"),
("C19",[34.8,36.8984],90,"VDDA9 additional 100nF, native schematic value retained"),
("C20",[32.2,37.0],90,"VDDA9 2.2uF local reservoir; effective >=1uF gate"),
("C21",[39.4,32.8984],90,"NRST7 100nF close to MCU; service header remains farther away"),
("C22",[47.2984,38.7],0,"OSC_IN load16pF; adjacent to Y1.1, actual routed parasitics pending"),
("C23",[38.7016,36.3],180,"XTAL_OUT load16pF; adjacent to Y1.3, compactness to optimize"),
("C24",[35.0,32.8984],90,"ADC0 PA0.10 100nF, on MCU side of R32"),
("R26",[29.5,36.8984],90,"0R V3V3->VDDA measurement link; not qualified ferrite"),
("R27",[38.0,41.3],0,"10k NRST pullup; C21 remains at pin7"),
("R28",[48.6,26.1],180,"BOOT0 10k pulldown; avoid USB direct route"),
("R29",[31.0,27.5],0,"BOOT1/PB2.20 10k pulldown"),
("R30",[56.7,31.0],90,"1k service feed to J8; header coordinate optional for root integration"),
("R31",[41.6,32.8984],90,"0R OSC_OUT tuning position; pin1 faces MCU.6"),
("R32",[31.0,33.0],0,"ADC series1k; pin2 connects C24.1/MCU.10, pin1 connects J10"),
("Y1",[43.0,37.5],180,"ABM3B8MHz; pin3 left-bottom, pin1 right-top; explicit no full AN2867 ground implementation claim"),
("J7",[33.0,43.0],270,"RESET service shunt; body avoids x<=30 low-height zone, accessible top"),
("J8",[54.0,32.0],0,"BOOT0 service jumper; optional coordinate subject global headers"),
("J10",[25.0,34.0],270,"ADC input1 points toward R32, input2 GND beside source; outside low-height zone")
]
def rotate(point,a):
    rad=math.radians(a)
    return [round(point[0]*math.cos(rad)-point[1]*math.sin(rad),6),round(point[0]*math.sin(rad)+point[1]*math.cos(rad),6)]
def xy(point,p,a):
    q=rotate(point,a)
    return [round(q[0]+p[0],6),round(q[1]+p[1],6)]
def bbox(box,p,a,offset=(0,0)):
    corners=[xy([x+offset[0],y+offset[1]],p,a) for x in [box[0][0],box[1][0]] for y in [box[0][1],box[1][1]]]
    return [[min(q[0] for q in corners),min(q[1] for q in corners)],[max(q[0] for q in corners),max(q[1] for q in corners)]]
placements=[]
for ref,p,a,purpose in P:
    c=components[ref]
    item=dict(ref=ref,xy=p,rotation=a,purpose=purpose,package=c["package"],bodyBound=bbox(c["bodyExtent"],p,a),source="native inventory 4L package-local readback, not final placed board",pins=[])
    for pin in c["logicalPins"]:
        q=dict(number=pin["number"],net=pin["net"],xy=xy(pin["localXY"],p,a),regularCopperBBox=bbox(pin["regularPadBBox"],p,a,pin["localXY"]))
        item["pins"].append(q)
    placements.append(item)
byref={p["ref"]:p for p in placements}
def pin(ref,n): return next(p["xy"] for p in byref[ref]["pins"] if p["number"]==str(n))
pairs=[("C13",24,23,[32.45,25.2748],[34.5,25.0]),("C14",36,35,[42.3252,19.3],[42.25,21.5]),("C15",48,47,[47.5,28.7252],[45.5,29.0])]
loops=[]
for cap,power,gnd,cv,gv in pairs:
    loops.append(dict(cap=cap,powerPin="U1."+str(power),groundPin="U1."+str(gnd),powerPinXY=pin("U1",power),groundPinXY=pin("U1",gnd),capPowerPad=cap+".1",capPowerXY=pin(cap,1),capGroundPad=cap+".2",capGroundXY=pin(cap,2),capGroundViaProposed=cv,mcuGroundViaProposed=gv,viaDefinition="L28VIA030C060, drill0.3 copper0.6; check DRC before retain",loopOrder=["cap.1","MCU.VDD","internal load(not PCB geometry)","MCU.VSS","MCU GND via","actual GND copper","cap GND via","cap.2"],verificationRequired=["native final pin and pad readback","cap power to matching supply pin connected","both GND vias connected to actual same GND copper","no plane void/thermal neck blocking return","netlist and dynamic DRC current","short neck rule/USB corridor preserved"],status="PROPOSED_UNROUTED_CENTERLINES_NOT_CONNECTIVITY_PROOF"))
overlaps=[]
for a,b in itertools.combinations(placements,2):
    aa,bb=a["bodyBound"],b["bodyBound"]
    dx=min(aa[1][0],bb[1][0])-max(aa[0][0],bb[0][0])
    dy=min(aa[1][1],bb[1][1])-max(aa[0][1],bb[0][1])
    if dx>1e-6 and dy>1e-6:overlaps.append(dict(a=a["ref"],b=b["ref"],dx=dx,dy=dy))
out=dict(schema="G_mcu_placement_proposal_v1",status="ENGINEERING_PROPOSAL_NEEDS_NATIVE_PLACEMENT_ROUTE_AND_DRC",inventorySHA256=hashlib.sha256(inventory.read_bytes()).hexdigest(),rotationConvention="CCW cartesian mathematical transform; final native placement readback must match",boardAssumptions=dict(size=[80,60],usbJ2=[40,3.675],lowProfileZone=[10,42,30,52],lowProfileCondition="z>=2mm forbidden, not all placement forbidden"),placements=placements,loops=loops,adcPath=dict(order=["J10.1 ADC_IN","R32.1","R32.2 ADC0","C24.1","U1.10"],returnPath=["C24.2","local quiet GND copper","U1.8 VSSA"],status="plan only; no claim actual routed"),clockPaths=[["U1.5","C22.1","Y1.1"],["U1.6","R31.1","R31.2","C23.1","Y1.3"]],groundingScope=dict(sharedNet="GND",AN2867LocalUnderneathGround="not implemented by this proposal; preserve a local quiet return and guard reservation, exact copper/connection reviewed in routing",crystalCasePads="Y1.2 and Y1.4 GND per Abracon; do not make their return carry sensitive load-cap currents"),bodyBoxPrecheck=dict(scope="only these proposed components, all other global parts absent",overlaps=overlaps,passNoOverlap=len(overlaps)==0),rejectedCandidates=[dict(ref="C14",xy=[43.0016,20.3],rotation=180,reason="GND pad and via impinge USB straight corridor; shifted +1mm X before native")])
(ROOT/"placement_mcu.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
(ROOT/"placement_precheck.json").write_text(json.dumps(dict(placements=len(P),overlaps=overlaps),indent=2),encoding="utf-8")
print(json.dumps(dict(placements=len(P),overlaps=overlaps,loops=loops),ensure_ascii=True,indent=2))
