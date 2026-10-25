from pathlib import Path
import sys,json,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power';w=load(O/'N40_2L_networks.json');r=load(O/'N40_2L_rules.json');p=load(O/'N40_2L_policy.json');n=load(H/'review/PROVISIONAL_UNSAVED_b016_2L_try09.json');s=CopperScene(n,w,r,p)
for xy in [[35.8,20.5],[35.65,20.5],[35.7,20.45],[35.8,20.4]]:
 pts=[[35.8,21.95],xy];g=LineString(pts).buffer(.3);hits=[]
 for a in s.obstacles:
  if a['net']=='GND':continue
  if a['layer']=='TOP':
   gap=g.distance(a['geometry']);need=s.space('GND',a['net'],'TOP',a['kind'])
   if gap<need-.0001:hits.append(dict(object=a['source'],net=a['net'],kind=a['kind'],gap=gap,need=need,bbox=a['geometry'].bounds))
 for l in LAYERS:
  g=Point(xy).buffer(.3,quad_segs=24)
  for a in s.obstacles:
   if a['net']=='GND' or a['layer']!=l:continue
   gap=g.distance(a['geometry']);need=s.space('GND',a['net'],l,a['kind'],True)
   if gap<need-.0001:hits.append(dict(layer=l,object=a['source'],net=a['net'],kind=a['kind'],gap=gap,need=need,bbox=a['geometry'].bounds))
 print('WEST',xy,hits)
# N40 PA1 blocker including current prior prefix copper
n=load(O/'N40_2L_snapshot.json');s=CopperScene(n,w,r,p)
for op in p['pendingOperations']:
 if op['net']=='GPIO_PA1':
  g=LineString(op['points']).buffer(.1);print('PA1BLOCK',[(a['net'],a['source'],round(g.distance(a['geometry']),6),a['geometry'].bounds) for a in s.obstacles if a['net']!=op['net'] and a['layer']=='BOTTOM' and g.distance(a['geometry'])<.201])
 s.add_operation(op)