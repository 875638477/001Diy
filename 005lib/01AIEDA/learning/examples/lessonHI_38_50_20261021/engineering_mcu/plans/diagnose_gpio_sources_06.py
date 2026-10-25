import sys,pathlib,json,math
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for variant in ('4L','2L'):
 n=load(P/f'GPIO_future_{variant}_06_snapshot.json');pol=load(P/f'GPIO_future_{variant}_06_policy.json');s=CopperScene(n,load(P/f'GPIO_future_{variant}_06_networks.json'),load(P/f'GPIO_future_{variant}_06_rules.json'),pol)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;v=next(v for v in n['vias'] if math.dist(v['xy'],[cc.x,cc.y])<1e-5)
   if v.get('padDiameterMM'):o['geometry']=Point(v['xy']).buffer(v['padDiameterMM']/2)
 report=[]
 for a in pol['componentAnchors']:
  if a['net'] not in ['GPIO_PA1','GPIO_PA2','GPIO_PA3','GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB15']:continue
  net=a['net'];pt=Point(a['xy']);rows=[]
  for layer in ('TOP','BOTTOM'):
   bad,inside=s.forbidden(net,layer,.2,False,.03736)
   near=sorted([dict(net=o['net'],kind=o['kind'],source=o['source'],distance=round(pt.distance(o['geometry'])-.1,4),required=s.space(net,o['net'],layer,o['kind']),bbox=list(o['geometry'].bounds)) for o in s.obstacles if o['net']!=net and o['layer']==layer],key=lambda x:x['distance'])[:8]
   areas=[x['id'] for x in pol['reservedAreas'] if layer in x.get('layers',LAYERS) and net not in x.get('allowedNets',[]) and Polygon(x['polygon']).buffer(.13736).covers(pt)]
   rows.append(dict(layer=layer,blocked=bad.covers(pt),near=near,reservations=areas))
  report.append(dict(anchor=a,detail=rows))
 (P/f'GPIO_source_diagnostics_{variant}_06.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 print(variant)
 for r in report:
  print(r['anchor']['net'],r['anchor']['xy'],[(x['layer'],x['blocked'],[(q['net'],q['distance'],q['required']) for q in x['near'][:2]],x['reservations']) for x in r['detail']])
