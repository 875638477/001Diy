exec(open(__file__.replace('inspect_target61.py','prepare_gpio_target61.py'),encoding='utf-8-sig').read().split('for v in')[0])
from shapely.geometry import LineString,Polygon
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');nw=load(P/f'GPIO_actualB016_{v}_59_networks.json');r=load(P/f'GPIO_actualB016_{v}_59_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');s=CopperScene(n,nw,r,p)
 for ck in load(P/f'GPIO_TARGET61_{v}_check.json'):
  net=ck['net'];line=LineString(ck['points']);hits=[]
  for o in s.obstacles:
   if o['layer']!='BOTTOM' or o['net']==net:continue
   d=line.distance(o['geometry'])-.1;g=s.space(net,o['net'],'BOTTOM',o['kind'])
   if d<g:hits.append(dict(net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=round(d,4),expected=g))
  for a in p.get('reservedAreas',[]):
   if 'BOTTOM' in a.get('layers',['TOP','BOTTOM']) and net not in a.get('allowedNets',[]) and line.distance(Polygon(a['polygon']))<.101:hits.append(a)
  print(v,net,hits)
 print('windows',p.get('routeWindows'))
