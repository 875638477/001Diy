from pathlib import Path
import sys,json,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power';v='2L';n=load(O/f'N47_{v}_snapshot.json');w=load(O/f'N47_{v}_networks.json');r=load(O/f'N47_{v}_rules.json');p=load(O/f'N47_{v}_policy.json');p['pendingOperations']=[];s=CopperScene(n,w,r,p)
paths=[('GPIO_PC13',[[42,28.9],[41.3,28.9],[33.2,37]]),('GPIO_PC15',[[40.3,28.9],[40.3,29],[32.3,37]]),('GPIO_PA1',[[37.5,29.6],[37.5,30.95],[31.45,37]]),('GPIO_PA2',[[36.6,30.4],[36.6,31.25],[30.85,37]]),('GPIO_PA3',[[35.2,31.65],[35.4,31.85],[30.25,37]])]
for net,pts in paths:
 print(net,s.path_clear(net,'BOTTOM',pts,.2));
 for a in p['reservedAreas']:
  if 'BOTTOM' in a.get('layers',LAYERS) and net not in a.get('allowedNets',[]) and LineString(pts).buffer(.1).intersects(Polygon(a['polygon'])):print('RESERVE',a['id'])
 for a in s.obstacles:
  if a['layer']=='BOTTOM' and a['net']!=net and a['geometry'].distance(LineString(pts).buffer(.1))<s.space(net,a['net'],'BOTTOM',a['kind'])-.0001:print('HIT',a['net'],a['source'],a['geometry'].bounds,LineString(pts).buffer(.1).distance(a['geometry']))
 s.add_operation(dict(type='route',id='TEST48',net=net,layer='BOTTOM',points=pts,width=.2))