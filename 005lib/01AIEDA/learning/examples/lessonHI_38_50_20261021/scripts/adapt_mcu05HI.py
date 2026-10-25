from pathlib import Path
import json,copy,hashlib,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
src=R/'engineering_mcu/plans/mcu_critical_routes_v5.json';d=json.loads(src.read_text())
for v in ['4L','2L']:
 o=copy.deepcopy(d);o['constraintOperations']=[]
 reg=d['regions'][0];assign=[]
 if v=='4L':
  physical=[('VDDA','HI_VDDA_P','P_VDDA_030'),('GROUND','G31_GND_P','P_GND_PLANE')]
  spacing=[('ANALOG','NC_ANALOG_SENSITIVE_S','S_ANALOG_030'),('OSCILLATOR','NC_OSCILLATOR_S','S_ANALOG_030'),('POWER','NC_POWER_LV_S','S_POWER_030')]
 else:
  physical=[('VDDA','HI2L_VDDA_P','HI2L_P_VDDA'),('GROUND','HI2L_GROUND_P','HI2L_P_GROUND')]
  spacing=[('ADC','HI2L_ADC_S','HI2L_S_ADC'),('OSCILLATOR','HI2L_OSCILLATOR_S','HI2L_S_OSCILLATOR'),('POWER','HI2L_POWER_LV_S','HI2L_S_POWER_LV'),('VDDA','HI2L_VDDA_S','HI2L_S_VDDA'),('GROUND','HI2L_GROUND_S','HI2L_S_GROUND')]
 for label,cl,cs in physical:
  name='HI_MCU_NORTH_P_'+label+'_'+v
  o['constraintOperations'].append({'type':'csetCopy','domain':'physical','name':name,'copyFrom':cs,'values':{'necklength_max':'1.4 MM'}})
  assign.append({'domain':'physical','netClass':cl,'cset':name})
 for label,cl,cs in spacing:
  name='HI_MCU_NORTH_S_'+label+'_'+v
  o['constraintOperations'].append({'type':'csetCopy','domain':'spacing','name':name,'copyFrom':cs,'values':{'smdpin_line':'0.2 MM','line_line':'0.2 MM'}})
  assign.append({'domain':'spacing','netClass':cl,'cset':name})
 o['constraintOperations'].append({'type':'region','id':reg['id'],'layer':'TOP','polygon':reg['polygon'],'assignments':assign})
 ops=[];osc=d['oscillatorReference'];localLayer=osc['localLayer'][v]
 for layer in (['L2','L3'] if v=='4L' else ['BOTTOM']):
  sid='HI_APP_GND_'+layer
  ops.append({'type':'bindShape','id':sid,'net':'GND','layer':layer})
  ops.append({'type':'void','id':sid+'_HSE_MOAT','net':'GND','shapeId':sid,'polygon':osc['applicationGroundVoidPolygon']})
 ops.append({'type':'shape','id':'HI_HSE_QUIET','net':'GND','layer':localLayer,'polygon':osc['islandPolygon'],'dynamic':False})
 vias=[x for x in d['operations'] if x['type']=='via']
 for orig in d['operations']:
  p=copy.deepcopy(orig)
  for key in ['from','to']:
   if isinstance(p.get(key),list):p[key]=p[key][0]+'.'+str(p[key][1])
  if p['type']=='route' and p.get('from') and not p.get('to'):
   candidates=[x for x in vias if x['net']==p['net'] and math.dist(x['xy'],p['points'][-1])<.00001]
   if len(candidates)==1:p['to']=candidates[0]['id']
  ops.append(p)
 o['operations']=ops
 o['aliases']=[{'id':'HI_GUARD_LEFT_END','net':'GND','layer':'TOP','xy':[42.2,39.8]},{'id':'HI_GUARD_RIGHT_END','net':'GND','layer':'TOP','xy':[44.2,39.8]},{'id':'HI_GUARD_RIGHT_LOWER_END','net':'GND','layer':'TOP','xy':[47.8,33.5]}]
 o['proofs']=[{'from':'C22.2','to':'HI_HSE_QUIET','connected':True},{'from':'C23.2','to':'HI_HSE_QUIET','connected':True},{'from':'HI_GUARD_LEFT_END','to':'C23.2','connected':True},{'from':'HI_GUARD_RIGHT_END','to':'C22.2','connected':True},{'from':'HI_GUARD_RIGHT_LOWER_END','to':'C22.2','connected':True},{'from':'C22.2','to':'U1.47','connected':True}]
 o['postChecks']=[{'type':'hseIsolation','anchorXY':[45.45,28.85],'localLayer':localLayer,'guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}]
 o['engineeringSource']={'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest().upper()}
 o['nativeVariant']=v
 o['adaptationNotes']=['Physical north-region applies only VDDA and GND (own base template, neck1.4); V3V3 .8mm new outward VBAT neck uses existing NE1.5, avoiding accidental restriction of existing1.453553mm inward VBAT route.','Application dynamic GND boundary has permanent all-layer HSE moat void; local quiet static plane is physically separate, same GND label is not evidence of isolation.','TOP guard extents need additional void around any future TOP global pour; negative-test repeated after final all-layer copper and stitches.','CSet values are independent copies, not dynamic inherited parents.']
 p=R/f'batches/mcu_{v}_b005.json';p.write_text(json.dumps(o,indent=2),encoding='utf8');print(p)
