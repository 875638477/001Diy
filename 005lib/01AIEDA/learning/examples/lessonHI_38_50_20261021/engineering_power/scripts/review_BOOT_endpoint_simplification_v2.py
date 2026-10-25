from pathlib import Path
import json,sys,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'tooling/packages'))
from shapely.geometry import LineString,Point,box
points=[[46.8,27.65],[47.27,27.18],[52.8984,27.18],[52.8984,28]]
geom=LineString(points).buffer(.1,cap_style=1,join_style=1);rows=[]
for variant in ['2L','4L']:
 s=json.loads((R/f'engineering_mcu/plans/GPIO_future_{variant}_21_snapshot.json').read_text(encoding='utf-8'));near=[]
 for line in s['routes']:
  if line['net']=='BOOT0' or line['layer'] not in ['TOP','ETCH/TOP']:continue
  if line.get('generatedThermal'):continue
  o=LineString(line['startEnd']).buffer(line['width']/2,cap_style=1)
  d=geom.distance(o)
  if d<.5:near.append(dict(kind='line',net=line['net'],startEnd=line['startEnd'],gap=d,overlap=geom.intersection(o).area))
 for c in s['placements']:
  for p in c['pins']:
   if p['net'] in ['BOOT0',None] or not p.get('padBBox'):continue
   a,b=p['padBBox'];o=box(*a,*b);d=geom.distance(o)
   if d<.5:near.append(dict(kind='pad',ref=c['ref'],pin=p['number'],net=p['net'],gap=d,overlap=geom.intersection(o).area))
 for via in s['vias']:
  if via['net']=='BOOT0':continue
  o=Point(via['xy']).buffer(.26 if 'HI_VIA026' in via['padstack'] else .3);d=geom.distance(o)
  if d<.5:near.append(dict(kind='via',net=via['net'],xy=via['xy'],gap=d,overlap=geom.intersection(o).area))
 assert not any(n['overlap']>1e-8 for n in near)
 rows.append(dict(variant=variant,nearbyOtherCopper=sorted(near,key=lambda z:z['gap']),status='NO_OTHER_NET_OVERLAP_ENDPOINT_SIMPLIFICATION_ONLY_NATIVE_PILOT_REQUIRED'))
out=dict(status='SCOPED_ENDPOINT_SIMPLIFICATION_GEOMETRY_NOT_API_CAUSE_PROOF',originalFailure='RIGHT_BOOT_DIRECT_TOP axlDBCreatePath=nil/SPMHSY49 Error9 after R28 correctactual180pose',newPoints=points,net='BOOT0',layer='TOP',width=.2,reason='Eliminate in-pad turn and restore actual.3mm GNDpadclearance: original y27.3 gives.1935; y27.18 gives.3135. No global/local rule relax. R28.1center52.8984,28 correct. Does not prove nativeAPI rootcause.',reviews=rows)
(R/'engineering_power/readouts/BOOT_endpoint_simplification_02.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))