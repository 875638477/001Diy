import pathlib,json,sys,math
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
q=load(P/'NSS_pullup_local_relayout_01.json')
for v in ['4L','2L']:
 n=load(P/f'GPIO_future_{v}_13_snapshot.json');s=CopperScene(n,load(P/f'GPIO_future_{v}_13_networks.json'),load(P/f'GPIO_future_{v}_13_rules.json'),load(P/f'GPIO_future_{v}_13_policy.json'))
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;z=next(z for z in n['vias'] if math.dist(z['xy'],[cc.x,cc.y])<1e-6)
   if z.get('padDiameterMM'):o['geometry']=Point(z['xy']).buffer(z['padDiameterMM']/2,quad_segs=64)
 fresh=[]
 for o in q['operations']+q['variantOperations'][v]:
  if o['type']=='route':
   for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o.get('width',.2)]*(len(o['points'])-1))):fresh.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(w/2,quad_segs=64),kind='line',source=o['id']))
  elif o['type']=='via':
   for l in LAYERS:fresh.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(o['padDiameterMM']/2,quad_segs=64),kind='via',source=o['id']))
 # Also inspect actual moved component terminal copper, not just route centerlines.
 for c in n['placements']:
  if c['ref'] not in ['R21','R23','R25','R32']:continue
  for pp in c['pins']:fresh.append(dict(net=pp['net'],layer='TOP',geometry=box(*pp['padBBox'][0],*pp['padBBox'][1]),kind='smdpin',source=c['ref']+'.'+pp['number']))
 checks=0;issues=[];nearest=[]
 for a in fresh:
  closest=None
  for b in s.obstacles:
   if a['layer']!=b['layer'] or a['net']==b['net']:continue
   checks+=1;d=a['geometry'].distance(b['geometry']);gap=s.space(a['net'],b['net'],a['layer'],b['kind'],a['kind']=='via')
   if closest is None or d<closest['distanceMM']:closest=dict(a=a['source'],aNet=a['net'],b=b['source'],bNet=b['net'],layer=a['layer'],distanceMM=d,requiredGapMM=gap,bBBox=list(b['geometry'].bounds))
   if d<gap-1e-4:issues.append(dict(a=a['source'],aNet=a['net'],b=b['source'],bNet=b['net'],layer=a['layer'],distanceMM=d,requiredGapMM=gap,bBBox=list(b['geometry'].bounds)))
  nearest.append(closest)
 report=dict(status='READ_ONLY_NOMINAL_CLASS_GEOMETRY_REVIEW_NOT_NATIVE_DRC',variant=v,checks=checks,nominalClassViolations=issues,nearestByPiece=nearest,qualification='Uses existing rule table/class gap and exact candidate pad/route/via geometry. Native region resolution, fill and conductive graph still required; no SI/ADC/assembly/manufacturing certification.')
 (P/f'NSS_pullup_relayout_class_review_{v}_01.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 print(v,'checks',checks,'violations',len(issues))
 for x in issues[:15]:print(x)
