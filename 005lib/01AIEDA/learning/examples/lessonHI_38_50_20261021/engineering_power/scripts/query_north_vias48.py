from pathlib import Path
import sys,json,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power';v='2L';n=load(O/f'N47_{v}_snapshot.json');w=load(O/f'N47_{v}_networks.json');r=load(O/f'N47_{v}_rules.json');p=load(O/f'N47_{v}_policy.json');p['pendingOperations']=[];s=CopperScene(n,w,r,p)
paths=[('GPIO_PC13',[[42,28.9],[41.3,28.9],[33.2,37]]),('GPIO_PC14',[[41.5,29.65],[36,35.15]]),('GPIO_PC15',[[40.3,28.9],[40.3,29],[32.3,37]]),('GPIO_PA1',[[37.5,29.6],[37.5,30.95],[31.45,37]]),('GPIO_PA2',[[36.6,30.4],[36.6,31.25],[30.85,37]]),('GPIO_PA3',[[35.2,31.65],[35.4,31.85],[30.25,37]])]
for net,pts in paths:s.add_operation(dict(type='route',id='TMP48',net=net,layer='BOTTOM',points=pts,width=.2))
for net,ss,y0,y1 in [('GPIO_PC14',71.15,32.5,35.15),('GPIO_PC13',70.2,32,35.2),('GPIO_PC15',69.3,32,35)]:
 bads=[s.forbidden(net,l,.2,True,.002) for l in LAYERS];ok=[]
 for i in range(round(y0*20),round(y1*20)+1):
  y=i/20;x=round(ss-y,5);pt=Point(x,y)
  if all(inside.covers(pt) and not bad.intersects(pt) for bad,inside in bads):ok.append([x,y])
 print(net,ok)
for net,xy in [('GPIO_PC14',[36,35.15]),('GPIO_PC13',[35.4,34.8]),('GPIO_PC15',[36,33.3])]:
 print('WHY',net,xy)
 g=Point(xy).buffer(.3,quad_segs=32)
 for a in s.obstacles:
  if a['net']==net:continue
  gap=g.distance(a['geometry']);need=s.space(net,a['net'],a['layer'],a['kind'],True)
  if gap<need-.0001:print(a['layer'],a['net'],a['kind'],a['source'],gap,need,a['geometry'].bounds)
 for a in p['reservedAreas']:
  if net not in a.get('allowedNets',[]) and Polygon(a['polygon']).buffer(.3).intersects(Point(xy)):print('RESERVE',a['id'],a.get('layers'))