import pathlib,sys,math,json
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');n['vias']=[z for z in n['vias'] if not(z['net']=='GND' and math.dist(z['xy'],[37.4,27.4])<1e-5)];s=CopperScene(n,load(P/f'GPIO_actualB016_{v}_59_networks.json'),load(P/f'GPIO_actualB016_{v}_59_rules.json'),p)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias'] if math.dist(z['xy'],[cc.x,cc.y])<1e-5);o['geometry']=Point(vv['xy']).buffer(.26 if '026_C052' in vv['padstack'].upper() else .3,quad_segs=16)
 for net,pts in [('GPIO_PB1',[[38.3,27.35],[37.9,27.35],[34.4,30.85],[34.4,31.95]]),('GPIO_PB10',[[38,26.3],[34,30.3],[34,31.6]])]:
  print(v,net,'clear',s.path_clear(net,'BOTTOM',pts,.2));line=LineString(pts)
  for o in s.obstacles:
   if o['layer']!='BOTTOM' or o['net']==net:continue
   d=line.distance(o['geometry'])-.1;g=s.space(net,o['net'],'BOTTOM',o['kind'])
   if d<g-.0001:print('hit',o['net'],o['kind'],o['source'],o['geometry'].bounds,round(d,4),g)

