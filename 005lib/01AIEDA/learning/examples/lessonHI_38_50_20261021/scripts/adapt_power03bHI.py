from pathlib import Path
import json,hashlib,copy
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
src=R/'engineering_power/power_star_03b.json'
d=json.loads(src.read_text())
for v in ['4L','2L']:
 o=copy.deepcopy(d);o['constraintOperations']=[]
 if v=='4L':
  pc='NC_POWER_LV_P';pp='P_POWER_060'
  scs=[('POWER','NC_POWER_LV_S','S_POWER_030')]
  o['constraintOperations'].append({'type':'netClass','name':'HI_VDDA_P','domain':'physical','cset':'P_VDDA_030','nets':['VDDA']})
 else:
  pc='HI2L_POWER_LV_P';pp='HI2L_P_POWER_LV'
  scs=[('POWER','HI2L_POWER_LV_S','HI2L_S_POWER_LV'),('GROUND','HI2L_GROUND_S','HI2L_S_GROUND')]
 for reg in d['rules']:
  assignments=[]
  name=reg['id']+'_P_'+v
  length=reg['physicalOnlyDelta']['necklength_max_mm']
  o['constraintOperations'].append({'type':'csetCopy','domain':'physical','name':name,'copyFrom':pp,'values':{'necklength_max':str(length)+' MM'}})
  assignments.append({'domain':'physical','netClass':pc,'cset':name})
  for label,sc,ss in scs:
   name=reg['id']+'_S_'+label+'_'+v
   o['constraintOperations'].append({'type':'csetCopy','domain':'spacing','name':name,'copyFrom':ss,'values':{k:str(val)+' MM' for k,val in reg['spacingOnlyDelta'].items()}})
   assignments.append({'domain':'spacing','netClass':sc,'cset':name})
  o['constraintOperations'].append({'type':'region','id':reg['id'],'layer':reg['layer'],'polygon':reg['polygon'],'assignments':assignments})
 o['engineeringSource']={'path':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest().upper()}
 o['nativeVariant']=v
 o['adaptationNotes']=['All CSet source templates are copied, not dynamic parents. Region scope follows native classification per domain.','VDDA is separated into its own 4L physical class before region-class assignment so its direct .3/.2 P_VDDA_030 cannot be overridden by copied .6/.25 POWER physical region.','Original budgets preserved for native merged-neck/overlapping-region feedback; do not raise automatically.']
 p=R/f'batches/power_{v}_b003b.json';p.write_text(json.dumps(o,indent=2),encoding='utf8')
 print(p)
