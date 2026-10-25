from pathlib import Path
import json, math, hashlib, sys
B=Path(r'D:\001DIY\005lib\01AIEDA')
G=B/'learning/examples/lessonG_30_37_20261020'
R=G/'engineering_power'
inv=json.loads((G/'inventory/inventory_4L.json').read_text(encoding='utf-8'))
src=json.loads((B/'learning/examples/de_15_26_20261019/integrated_circuit.json').read_text(encoding='utf-8'))
by={c['ref']:c for c in inv['components']}
sp={c['ref']:c for c in src['components']}
proposal=json.loads((R/'placement_power.json').read_text(encoding='utf-8'))
places={p['ref']:p for p in proposal}
places.update({'J2':{'xy':[40,3.675],'rotation':0},'J3':{'xy':[74,12],'rotation':0},'J4':{'xy':[74,25],'rotation':0},'U1':{'xy':[40,27],'rotation':270}})
def tr(xy,po,ang):
 a=math.radians(ang);x,y=xy
 return [round(po[0]+x*math.cos(a)-y*math.sin(a),5),round(po[1]+x*math.sin(a)+y*math.cos(a),5)]
def pin(ref,n):
 c=by[ref];p=next(x for x in c['logicalPins'] if x['number']==str(n));pl=places[ref]
 v=tr(p['localXY'],pl['xy'],pl['rotation'])
 b=p['regularPadBBox'];r=p['localRotation']+pl['rotation']
 pts=[tr([x,y],v,r) for x in [b[0][0],b[1][0]] for y in [b[0][1],b[1][1]]]
 return dict(ref=ref,number=str(n),net=p['net'],xy=v,padBBox=[[min(q[i] for q in pts) for i in [0,1]],[max(q[i] for q in pts) for i in [0,1]]])
checks=[]
def check(id,actual,expected):
 checks.append({'id':id,'pass':actual==expected,'actual':actual,'expected':expected})
for ref in by:
 check('source_pin_map_'+ref,{p['number']:p['net'] for p in by[ref]['logicalPins']},sp[ref]['pins'])
check('components80',len(by),80)
check('logicalPins272',sum(len(c['logicalPins']) for c in by.values()),272)
expected={
 'U2':{'1':'GND','2':'BUCK_SW','3':'VIN_PROT','4':'BUCK_FB','5':None,'6':'BUCK_BOOT'},
 'U3':{'1':'V5','2':'GND','3':'V5','4':None,'5':'V3V3'},
 'U4':{'1':'USB_DP','6':'USB_DP','3':'USB_DM','4':'USB_DM','2':'GND','5':'USB_VBUS'},
 'U5':{'1':'CAN_TXD','2':'GND','3':'V3V3','4':'CAN_RXD','5':None,'6':'CAN_L','7':'CAN_H','8':None},
 'C4':{'1':'BUCK_BOOT','2':'BUCK_SW'},
 'L1':{'1':'BUCK_SW','2':'V5'},
 'D1':{'1':'VIN_PROT','2':'VIN_FUSED'},
 'R5':{'1':'PA12_SHARED','2':'USB_DP'},'R6':{'1':'PA11_SHARED','2':'USB_DM'},
 'R12':{'1':'PA12_SHARED','2':'CAN_TXD'},'R13':{'1':'PA11_SHARED','2':'CAN_RXD'},
}
for ref,pins in expected.items():
 for n,net in pins.items():
  v=next(x['net'] for x in by[ref]['logicalPins'] if x['number']==n)
  check('critical_'+ref+'.'+n,v,net)
  if net is None:check('NC_'+ref+'.'+n,v is None,True)
check('USBdefault_R12_DNP',sp['R12'].get('populate'),'DNP default USB mode')
check('USBdefault_R13_DNP',sp['R13'].get('populate'),'DNP default USB mode')
pairs=[
 ('buck_C3_VIN','U2',3,'C3',1,3.0,'HF bypass forward connection'),
 ('buck_C3_GND','U2',1,'C3',2,3.0,'HF bypass return connection; continuous ground plus close via, not SW shared neck'),
 ('buck_C2_VIN','U2',3,'C2',1,4.5,'main input capacitor'),
 ('boot_to_pin6','U2',6,'C4',1,2.0,'BOOT no GND'),
 ('boot_to_SW','U2',2,'C4',2,4.0,'BOOT return SW, no switch current under IC'),
 ('inductor_shortlead','U2',2,'L1',1,3.0,'short-lead faces switch'),
 ('output_cap_to_L','L1',2,'C5',1,4.0,'filtered output path'),
 ('feedback_pin4_R2','U2',4,'R2',1,2.5,'small quiet FB node'),
 ('ldo_input','U3',1,'C8',1,2.5,'DBV input bypass'),
 ('ldo_input_ground','U3',2,'C8',2,3.0,'LDO quiet common return'),
 ('ldo_output','U3',5,'C9',1,2.5,'DBV output bypass'),
 ('ldo_output_ground','U3',2,'C9',2,4.0,'LDO quiet common return'),
 ('can_HF_VCC','U5',3,'C11',1,2.0,'100nF closest to VCC'),
 ('can_HF_GND','U5',2,'C11',2,2.0,'at least two vias when connection uses ground plane, as TI guidance'),
 ('ESD_VBUS_cap','U4',5,'C10',1,2.0,'rail clamp local capacitor'),
 ('ESD_GND_cap','U4',2,'C10',2,3.0,'direct local ground return'),
 ('USB_R5_to_MCU','U1',33,'R5',1,5.0,'proposed source-side access budget, no vendor fixed-mm assertion'),
 ('USB_R6_to_MCU','U1',32,'R6',1,5.0,'proposed source-side access budget, no vendor fixed-mm assertion'),
 ('UART_TX_driver_R16','U1',30,'R16',1,4.0,'prefer source damping resistor close to driving MCU, current candidate review'),
]
metrics=[]
for id,ra,na,rb,nb,budget,purpose in pairs:
 a,b=pin(ra,na),pin(rb,nb)
 dx=max(0,a['padBBox'][0][0]-b['padBBox'][1][0],b['padBBox'][0][0]-a['padBBox'][1][0])
 dy=max(0,a['padBBox'][0][1]-b['padBBox'][1][1],b['padBBox'][0][1]-a['padBBox'][1][1])
 d=math.hypot(dx,dy)
 metrics.append({'id':id,'a':a,'b':b,'centerDistance_mm':round(math.dist(a['xy'],b['xy']),4),'axisAlignedPadEdgeDistanceLowerBound_mm':round(d,4),'proposalBudget_mm':budget,'budgetProvenance':'engineering placement goal, not manufacturer hard limit','purpose':purpose,'status':'WITHIN_GEOMETRIC_BUDGET_ROUTE_UNPROVEN' if d<=budget else 'REVIEW_PLACEMENT','noTraceLengthClaim':True})
out={'status':'PASS_SOURCE_NATIVE_PIN_MAPPING' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'placementVersion':'initial40 component proposal, not final native placement','metrics':metrics,'metricLimit':'Rectangular pad AABB shortest separation is geometric lower bound only, not actual trace length, loop area/inductance/EMI or impedance result.'}
(R/'readouts/pin_and_geometric_review.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'status':out['status'],'checks':len(checks),'failed':[x for x in checks if not x['pass']],'metricReview':[{'id':m['id'],'distance':m['axisAlignedPadEdgeDistanceLowerBound_mm'],'budget':m['proposalBudget_mm']} for m in metrics if m['status']=='REVIEW_PLACEMENT']},ensure_ascii=False))
