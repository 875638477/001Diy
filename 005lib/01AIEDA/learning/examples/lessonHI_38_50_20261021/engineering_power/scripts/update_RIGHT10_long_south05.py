from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');H=R.parent
old=json.loads((H/'engineering_mcu/plans/GPIO_south_joint_fanout_04.json').read_text());new=json.loads((H/'engineering_mcu/plans/GPIO_south_joint_fanout_05.json').read_text());ids={o['id'] for o in old['operations']+old.get('commonOperations',[])}
for v in ['2L','4L']:
 p=json.loads((R/f'RIGHT10_long_policy_{v}_v2.json').read_text())
 for key in ['pendingOperations','pendingDeleteSegments','pendingDeleteVias']:p[key]=[o for o in p.get(key,[]) if o['id'] not in ids]
 for o in new.get('operations',[])+new.get('commonOperations',[])+new.get('variantOperations',{}).get(v,[]):
  if o['type']=='deleteSegment':p['pendingDeleteSegments'].append(o)
  elif o['type']=='deleteVia':p['pendingDeleteVias'].append(o)
  else:
   if o['type']=='via' and '026' in o['padstack']:o.update(padDiameterMM=.52,drillDiameterMM=.26)
   p['pendingOperations'].append(o)
 p['pendingPlacementChanges'] +=new.get('placementChanges',[])
 for net,x in new.get('partialEndpoints',{}).items():
  for a in p['componentAnchors']:
   if a['key']=='ANCHOR_'+net:a['xy']=x['xy'];a['layers']=[x['layer']]
 (R/f'RIGHT10_long_policy_{v}_v2.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
print('updatedSouth05')