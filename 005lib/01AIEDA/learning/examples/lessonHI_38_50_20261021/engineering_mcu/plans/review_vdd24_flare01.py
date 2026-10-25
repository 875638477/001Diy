import json,pathlib,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_future_{v}_36_snapshot.json');s=CopperScene(n,load(P/f'GPIO_future_{v}_36_networks.json'),load(P/f'GPIO_future_{v}_36_rules.json'),load(P/f'GPIO_future_{v}_36_policy.json'));line=LineString([[35.1,23.6],[35.1,23.2]]).buffer(.3,quad_segs=32);issues=[];mins=[]
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   z=next(z for z in n['vias'] if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-6);o['geometry']=Point(z['xy']).buffer(.26 if '026_C052' in z['padstack'].upper() else .3,quad_segs=32)
  if o['layer']!='TOP' or o['net']=='V3V3':continue
  gap=s.space('V3V3',o['net'],'TOP',o['kind']);d=line.distance(o['geometry']);mins.append(dict(other=o['net'],source=o['source'],kind=o['kind'],gap=gap,d=d,bbox=o['geometry'].bounds))
  if d<gap-1e-6:issues.append(mins[-1])
 q=dict(status='GEOMETRIC_CANDIDATE_NATIVE_NECK_CHECK_PENDING',variant=v,operations=[dict(type='deleteSegment',id='VDD24_EXPAND_RIP',net='V3V3',layer='TOP',points=[[35.1,23.6],[35.1,23.2]],width=.25),dict(type='route',id='VDD24_SHORTER_NORMAL_FLARE',net='V3V3',layer='TOP',points=[[35.1,23.6],[35.1,23.2]],width=.6,purpose='Restore normal power width after .919239mm fine-pitch escape, avoiding new neck rule relaxation.')],retainedNeckLengthMM=math.dist([35.75,24.25],[35.1,23.6]),issues=issues,closest=sorted(mins,key=lambda z:z['d'])[:8])
 (P/f'VDD24_neck_geometric_fix_{v}_01.json').write_text(json.dumps(q,indent=2),encoding='utf8');print(v,len(issues),json.dumps(q['closest'][:3]))
