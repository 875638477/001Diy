import pathlib,json,sys,math,copy
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(H/f'engineering_power/N37_{v}_snapshot.json');nw=load(H/f'engineering_power/N37_{v}_networks.json');rs=load(H/f'engineering_power/N37_{v}_rules.json');pol=load(P/f'GPIO_N37_{v}_40_policy.json');y=20.7 if v=='2L' else 20.675
 ops=[dict(type='deleteVia',id='PB15_EAST_RETURN_RIP',net='GND',xy=[38,20]),dict(type='deleteSegment',id='PB15_UP_TAIL_RIP',net='GPIO_PB15',layer='BOTTOM',points=[[38.5,y],[38.5,22.3]],width=.16),dict(type='via',id='PB15_EAST_RETURN_RELOCATED',net='GND',xy=[37.5,19.05],padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26,purpose='Retain a real nearby application-ground stitch while opening the southern GPIO outlet; refresh actual plane connection and all-layer via-only parent permissions.'),dict(type='route',id='PB15_DOWN_NORMAL_EXIT',net='GPIO_PB15',layer='BOTTOM',width=.2,points=[[38.5,y],[38.1,20.3],[38.1,19.7]],purpose='Replace upward dead-end partial with accessible southern normal-width route, preserving MCU TOP source and all power/ADC/HSE copper.')]
 for o in ops:
  if o['type']=='deleteVia':
   z=[z for z in n['vias'] if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-6];assert len(z)==1;n['vias'].remove(z[0])
  elif o['type']=='deleteSegment':
   z=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in [o['points'],list(reversed(o['points']))] and abs(r['width']-o['width'])<1e-6];assert len(z)==1,(v,o,z);n['routes'].remove(z[0])
 s=CopperScene(n,nw,rs,pol)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   z=next(z for z in n['vias'] if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-6);o['geometry']=Point(z['xy']).buffer(.26 if '026_C052' in z['padstack'].upper() else .3,quad_segs=32)
 fresh=[]
 for o in ops:
  if o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):fresh.append(dict(net=o['net'],layer=o['layer'],kind='line',geometry=LineString([a,b]).buffer(.1,quad_segs=32),source=o['id']))
  elif o['type']=='via':
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
  elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=.52,drillDiameterMM=.26,futureCandidate=o['id']))
 for a in pol['componentAnchors']:
  if a['net']=='GPIO_PB15':a['xy']=[38.1,19.7];a['layers']=['BOTTOM']
 q=dict(status='CANDIDATE_ACCESS_EXIT_PENDING_NATIVE' if not issues else 'REJECTED_GEOMETRIC_CANDIDATE',variant=v,batchId=f'PB15_access_exit_{v}_42',operations=ops,partialEndpoints={'GPIO_PB15':dict(xy=[38.1,19.7],layer='BOTTOM',connectedTo='U1.28')},issues=issues,returnDistancesMM={'newGPIOendToGround':math.dist([38.1,19.7],[37.5,19.05]),'PA10sourceToGround':math.dist([40,20.5],[37.5,19.05]),'attachSourceToGround':math.dist([39.3,20.95],[37.5,19.05])},pending=['Actual application-ground graph/plane geometry, not nominal same-net label','Recopy all-layer actual via permission parent at relocated return','Complete PB15 long path/reference and native DRC before acceptance'])
 (P/f'PB15_access_exit_{v}_42.json').write_text(json.dumps(q,indent=2),encoding='utf8')
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_N37_{v}_42_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,len(issues),json.dumps(issues))

