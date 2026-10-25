import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_N47_{v}_50_snapshot.json');nw=load(P/f'GPIO_N47_{v}_50_networks.json');rs=load(P/f'GPIO_N47_{v}_50_rules.json');pol=load(P/f'GPIO_N47_{v}_50_policy.json');y=20.7 if v=='2L' else 20.675;ops=[dict(type='deleteVia',id='PB15_MID_RETURN_RIP',net='GND',xy=[38,20])]
 for id,net,xy in [('PB15_MID_RETURN_NEW','GND',([34.2,20.7] if v=='2L' else [34.2,18.6])),('PB15_LOCAL_BRIDGE_VIA','GPIO_PB15',[37.7,19.5]),('PB15_WEST_BRIDGE_VIA','GPIO_PB15',[34.2,19.6])]:ops.append(dict(type='via',id=id,net=net,xy=xy,padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26))
 ops += [dict(type='route',id='PB15_ESCAPE_NORMAL_BOTTOM',net='GPIO_PB15',layer='BOTTOM',width=.2,points=[[38.5,y],[38.1,20.3],[37.7,19.9],[37.7,19.5]]),dict(type='route',id='PB15_SHORT_WEST_TOP_BRIDGE',net='GPIO_PB15',layer='TOP',width=.2,points=[[37.7,19.5],[34.3,19.5],[34.2,19.6]])]
 if v=='2L':
  old=[[[34.55,22.95],[34.4,22.8]],[[34.4,22.8],[34.4,18.15]]]
  for i,pts in enumerate(old):
   rr=[r for r in n['routes'] if r['net']=='VBUS_PRESENT_N' and r['layer']=='ETCH/BOTTOM' and r['startEnd'] in [pts,list(reversed(pts))] and abs(r['width']-.2)<1e-6];assert len(rr)==1,(v,pts,len(rr));n['routes'].remove(rr[0]);ops.append(dict(type='deleteSegment',id='PB15_2L_VBUS_CLEAR_RIP_'+str(i),net='VBUS_PRESENT_N',layer='BOTTOM',width=.2,points=pts))
  ops.append(dict(type='route',id='PB15_2L_VBUS_FINITE_BYPASS',net='VBUS_PRESENT_N',layer='BOTTOM',width=.2,points=[[34.55,22.95],[34.95,22.55],[34.95,19.45],[34.4,18.9],[34.4,18.15]],purpose='Low-current DC VBUS sense shifts .55mm over finite y19.45..22.55 to permit a normal-clearance TOP/BOTTOM GPIO bridge between the existing TOP3V3 and BOTTOMsense corridors; source and receiver pins unchanged.'))
 z=[z for z in n['vias']if z['net']=='GND'and math.dist(z['xy'],[38,20])<1e-6];assert len(z)==1;n['vias'].remove(z[0]);s=CopperScene(n,nw,rs,pol)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   z=next(z for z in n['vias']if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-6);o['geometry']=Point(z['xy']).buffer(.26 if '026_C052'in z['padstack'].upper()else .3,quad_segs=32)
 for o in pol['pendingOperations']:s.add_operation(o)
 fresh=[]
 for o in ops:
  if o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):fresh.append(dict(net=o['net'],layer=o['layer'],kind='line',geometry=LineString([a,b]).buffer(.1,quad_segs=32),source=o['id']))
  elif o['type']=='via':
   for l in LAYERS:fresh.append(dict(net=o['net'],layer=l,kind='via',geometry=Point(o['xy']).buffer(.26,quad_segs=32),source=o['id']))
 issues=[]
 for i,a in enumerate(fresh):
  for b in s.obstacles+fresh[:i]:
   if a['net']==b['net']or a['layer']!=b['layer']:continue
   d=a['geometry'].distance(b['geometry']);gap=s.space(a['net'],b['net'],a['layer'],b['kind'],a['kind']=='via')
   if d<gap-1e-6:issues.append(dict(a=a['source'],net=a['net'],b=b['source'],otherNet=b['net'],layer=a['layer'],gap=gap,d=d,bbox=b['geometry'].bounds))
 for o in ops:
  if o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=.2,startEnd=[a,b],kind='line',generatedThermal=False,futureCandidate=o['id']))
  elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=.52,drillDiameterMM=.26,futureCandidate=o['id']))
 for a in pol['componentAnchors']:
  if a['net']=='GPIO_PB15':a['xy']=[34.2,19.6];a['layers']=['TOP','BOTTOM']
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_N47_{v}_56_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 q=dict(status='PB15_ENGINEERED_BRIDGE_CANDIDATE_NOT_NATIVE',operations=ops,issues=issues,ruleIntent='All GPIO copper .2mm normal width. MID ground move uses local all-layer actual approved-via-only; no spacing or neck relaxation. Need final actual common-ground proof and per-source finite return review. Old source TOP+original via preserved.',expectedEndpoints={'GPIO_PB15':dict(connectedTo='U1.28',xy=[34.2,19.6],layers=['TOP','BOTTOM'])})
 (P/f'PB15_engineered_access_{v}_56.json').write_text(json.dumps(q,indent=2),encoding='utf8');print(v,len(issues),json.dumps(issues))


