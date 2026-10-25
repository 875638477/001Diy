from pathlib import Path
import json,math,collections
B=Path(r'D:\001DIY\005lib\01AIEDA/learning/examples/lessonG_30_37_20261020')
R=B/'engineering_power'
data=[
('J1',[6,13],0,'Bench DC entry; exact connector/cable/tool envelope pending'),
('F1',[9.2,13],0,'Before reverse diode, visible service fuse'),
('D1',[15,13],90,'SS14 anode left, cathode right to VIN_PROT'),
('C1',[11.2,18.3],0,'Bulk input after D1; positive pin1; 11mm teaching envelope'),
('C2',[25.2,15.4],180,'22uF VIN local reservoir; retain low impedance ground corridor'),
('C3',[26.2,18.6],180,'Closest HF VIN bypass; pin1 toward U2 VIN, pin2 GND via/corridor'),
('U2',[25.5,21],270,'SW left / FB right; high di/dt CIN loop planned separately from output loop'),
('C4',[26.7,23.7],180,'BOOT pin1 to U2.6; pin2 to SW not ground'),
('L1',[20,24],0,'Short lead local pin1 right faces U2 SW; real height max6.1mm'),
('C5',[14.4,23.1],90,'Output cap V5 pin1 lower, GND pin2 upper; sample clean V5 here'),
('C6',[11.7,23.1],90,'Parallel output cap next to C5'),
('R1',[31,19.1],180,'Feedback upper resistor; own quiet sense from C5 positive'),
('R2',[29.9,21.3],180,'Feedback lower resistor; Kelvin GND to U2.1 outside power return'),
('C7',[31,17.3],180,'Feedforward across R1; small FB node away from SW'),
('U3',[30.4,27],0,'LDO DBV5: input left/top output right/top; no exposed pad'),
('C8',[27.8,29],270,'LDO input 0805 pin1 V5 near U3.1; pin2 GND near U3.2'),
('C9',[31.2,30.6],0,'LDO output 0805 above U3; avoids root SPI R24 at y28.2'),
('U4',[40.25,10],180,'USBLC6 flow-through: connector to6/4, protected side1/3; GND2 at y11.3'),
('C10',[42.7,8.6],90,'ESD VBUS rail local100nF; short return via near ground pad'),
('R3',[35,10],90,'CC1 own5.1k to GND; not combined with CC2'),
('R4',[45.5,10],90,'CC2 own5.1k to GND; no TypeC all-pins ESD assertion'),
('R5',[41.4,18.5],270,'USB D+ series position pin1 MCU, pin2 USB; history22R unresolved'),
('R6',[39.4,18.5],270,'USB D- series position pin1 MCU, pin2 USB; moved below C14 envelope'),
('R7',[49,7],0,'USB VBUS sense gate series10k; outside USB pair main corridor'),
('R8',[56.2,9],90,'VBUS MOS gate pull-down; keep off protected pair'),
('Q1',[52,10.8],0,'2N7002 VBUS presence sense, source GND; no USB board power'),
('R9',[56.2,13],90,'VBUS presence drain pullup to3V3'),
('Q2',[48,13.5],0,'D+ attach PMOS source3V3, drain to pullup; default off'),
('R10',[48.5,17.2],0,'Attach gate-source off resistor local toQ2'),
('R11',[46,16.2],180,'1.5k D+ pullup branch; right end source / left end near D+ path'),
('R12',[43.4,18.3],0,'DNP default USB; CAN_TX select pad branch near R5 shared-side node'),
('R13',[37.4,18.3],180,'DNP default USB; CAN_RX select pad branch near R6 shared-side node'),
('U5',[64,16],0,'SO8 pin1 origin: digital left, bus pins6/7 right towardJ3'),
('C11',[61.8,13.3584],90,'CAN100nF: pin1 aligns U5.3 VCC; pin2 near U5.2GND'),
('C12',[59.8,13.3584],90,'CAN1uF next toHF cap, independent local ground return'),
('R14',[60.3,17.9],0,'TXD recessive pullup near U5.1'),
('R15',[71.5,14.75],270,'120R across bus near connector; endpoint-only population'),
('R16',[46.5,20.5],0,'UART TX33R position; source path longer than ideal due USB/decoupling priorities, review route'),
('R17',[50.3,19.4],0,'UART RX0R from external receiver path'),
('R18',[54.5,18.2],90,'UART RX idle pullup'),
]
inv=json.loads((B/'inventory/inventory_4L.json').read_text(encoding='utf-8'))
byref={c['ref']:c for c in inv['components']}
def transform(xy,pos,ang):
 a=math.radians(ang);x,y=xy
 return [round(pos[0]+x*math.cos(a)-y*math.sin(a),4),round(pos[1]+x*math.sin(a)+y*math.cos(a),4)]
out=[];bounds={}
for ref,xy,rot,purpose in data:
 c=byref[ref]
 r={'ref':ref,'xy':xy,'rotation':rot,'purpose':purpose,'package':c['package'],'proposalOnly':True}
 body=c.get('bodyExtent')
 if body:
  points=[transform([x,y],xy,rot) for x in (body[0][0],body[1][0]) for y in (body[0][1],body[1][1])]
  box=[[min(p[i] for p in points) for i in (0,1)],[max(p[i] for p in points) for i in (0,1)]]
  r['transformedBodyBBox']=box;bounds[ref]=box
 r['pins']=[{'number':p['number'],'net':p['net'],'xy':transform(p['localXY'],xy,rot)} for p in c['logicalPins']]
 out.append(r)
(R/'placement_power.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
clashes=[]
for i,a in enumerate(out):
 if a['ref'] not in bounds:continue
 ab=bounds[a['ref']]
 for b in out[i+1:]:
  if b['ref'] not in bounds:continue
  bb=bounds[b['ref']]
  dx=min(ab[1][0],bb[1][0])-max(ab[0][0],bb[0][0]);dy=min(ab[1][1],bb[1][1])-max(ab[0][1],bb[0][1])
  if dx>0 and dy>0:clashes.append({'a':a['ref'],'b':b['ref'],'overlap':[dx,dy]})
(R/'readouts/placement_internal_clashes.json').write_text(json.dumps(clashes,indent=2),encoding='utf-8')
print(json.dumps({'count':len(out),'internalBodyBBoxOverlaps':clashes},ensure_ascii=False))
