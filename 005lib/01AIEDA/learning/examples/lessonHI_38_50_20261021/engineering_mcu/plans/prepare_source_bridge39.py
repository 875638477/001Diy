import pathlib,json,sys,math,copy
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
ops=[]
def rt(id,net,l,pts,w=.2):ops.append(dict(type='route',id=id,net=net,layer=l,points=pts,width=w,purpose='Short TOP normal-width bridge across existing BOTTOM PC15 source bar, preserving MCU power and analog geometry.'))
def via(id,net,xy):ops.append(dict(type='via',id=id,net=net,xy=xy,padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26,purpose='Offpad private-via transition in explicit all-conductor approved-via-only permission region; normal spacing retained.'))
rt('PB1_ACCESS_TOP','GPIO_PB1','TOP',[[38.3,27.35],[37.9,27.75],[37.9,28.25],[36.82,29.32]])
via('PB1_ACCESS_VIA','GPIO_PB1',[36.82,29.32])
rt('PB10_ACCESS_BOTTOM','GPIO_PB10','BOTTOM',[[38,26.3],[38.4,26.3],[39,26.9]])
via('PB10_ACCESS_IN_VIA','GPIO_PB10',[39,26.9])
rt('PB10_ACCESS_TOP','GPIO_PB10','TOP',[[39,26.9],[39,27.5],[38.7,27.8],[38.7,28.4],[37.99,29.11],[37.99,30.15]])
via('PB10_ACCESS_OUT_VIA','GPIO_PB10',[37.99,30.15])
via('PB1_ACCESS_RETURN_VIA','GND',[36.95,28])
q=dict(status='EXPLICIT_SOURCE_BRIDGE_CANDIDATE_PENDING_FULL_LONG_ROUTE_AND_NATIVE',batchId='GPIO_source_access_bridges39',operations=ops,partialEndpoints={'GPIO_PB1':dict(xy=[36.82,29.32],layer='BOTTOM',connectedTo='U1.19'),'GPIO_PB10':dict(xy=[37.99,30.15],layer='BOTTOM',connectedTo='U1.21')},ruleIntent='All new routes normal .2mm; do not extend original .16mm source neck budget. Small-via permission local all actual conductor layers only; no spacing relaxation, no power/ADC/HSE changes.',proofs=[dict(from_='U1.19',toXY=[36.82,29.32]),dict(from_='U1.21',toXY=[37.99,30.15])])
(P/'GPIO_source_access_bridges39.json').write_text(json.dumps(q,indent=2),encoding='utf8')
for v in ['2L','4L']:
 n=load(P/f'GPIO_future_{v}_36_snapshot.json');nw=load(P/f'GPIO_future_{v}_36_networks.json');rs=load(P/f'GPIO_future_{v}_36_rules.json');pol=load(P/f'GPIO_future_{v}_37_policy.json');s=CopperScene(n,nw,rs,pol)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   z=next(z for z in n['vias'] if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-6);o['geometry']=Point(z['xy']).buffer(.26 if '026_C052' in z['padstack'].upper() else .3,quad_segs=32)
 fresh=[]
 for o in ops:
  if o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):fresh.append(dict(net=o['net'],layer=o['layer'],kind='line',geometry=LineString([a,b]).buffer(.1,quad_segs=32),source=o['id']))
  else:
   for l in LAYERS:fresh.append(dict(net=o['net'],layer=l,kind='via',geometry=Point(o['xy']).buffer(.26,quad_segs=32),source=o['id']))
 issues=[]
 for i,a in enumerate(fresh):
  for b in s.obstacles+fresh[:i]:
   if a['net']==b['net'] or a['layer']!=b['layer']:continue
   gap=s.space(a['net'],b['net'],a['layer'],b['kind'],a['kind']=='via');d=a['geometry'].distance(b['geometry'])
   if d<gap-1e-6:issues.append(dict(a=a['source'],net=a['net'],b=b['source'],otherNet=b['net'],layer=a['layer'],d=d,gap=gap,bbox=b['geometry'].bounds))
 for o in ops:
  if o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=.2,startEnd=[a,b],kind='line',generatedThermal=False,futureCandidate=o['id']))
  else:n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=.52,drillDiameterMM=.26,futureCandidate=o['id']))
 for a in pol['componentAnchors']:
  if a['net'] in q['partialEndpoints']:a['xy']=q['partialEndpoints'][a['net']]['xy'];a['layers']=['TOP','BOTTOM']
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_future_{v}_39_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 (P/f'GPIO_source_access_bridges39_{v}_review.json').write_text(json.dumps(dict(issues=issues,scope='Exact new copper vs source pads/vias/clines and each other, generated shapes/thermal/reference and native class-pair region review still pending.'),indent=2),encoding='utf8');print(v,len(issues));print(json.dumps(issues,indent=1))
