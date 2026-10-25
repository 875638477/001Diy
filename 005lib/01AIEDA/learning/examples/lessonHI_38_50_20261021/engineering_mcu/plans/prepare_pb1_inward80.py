import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 B=H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING';n=load(B/'normalized.json');nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');ops=[]
 def apply(o):
  if o['type']=='deleteVia':
   zz=[z for z in n['vias'] if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-6];assert len(zz)==1;n['vias'].remove(zz[0])
  elif o['type']=='deleteSegment':
   zz=[z for z in n['routes'] if z['net']==o['net'] and z['layer']=='ETCH/'+o['layer'] and abs(z['width']-o['width'])<1e-6 and z['startEnd']in[o['points'],o['points'][::-1]]];assert len(zz)==1;n['routes'].remove(zz[0])
  elif o['type']=='via':n['vias'].append(dict(o,pads=[]))
  elif o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=o['width'],startEnd=[a,b],futureCandidate=o['id'],generatedThermal=False))
  else:raise Exception(o)
 for o in load(H/f'engineering_power/GPIO_NORTH6_{v}_51.json')['operations']:apply(o)
 for a in p['componentAnchors']:
  if a['net'].startswith('GPIO_PB'):
   vv=[z for z in n['vias'] if z['net']==a['net']];assert len(vv)==1;a['xy']=vv[0]['xy'];a['layers']=['TOP','BOTTOM']
 # Current candidate J12 south only, native placement is unchanged until approved integration.
 pp=next(z for z in n['placements'] if z['ref']=='J12');assert pp['xy']==[40,55];pp['xy']=[18,9]
 for pin in pp['pins']:pin['xy']=[pin['xy'][0]-22,pin['xy'][1]-46];pin['padBBox']=[[pt[0]-22,pt[1]-46]for pt in pin['padBBox']]
 for nk in nw['nets']:
  for c in nk['components']:
   for t in c['terminals']:
    if t['key'].startswith('J12.'):t['xy']=[t['xy'][0]-22,t['xy'][1]-46]
 def add(o):ops.append(o)
 def dv(net,xy):add(dict(type='deleteVia',id=f'RIP80_{net}_{xy}',net=net,xy=xy))
 def ds(net,layer,pts,w):add(dict(type='deleteSegment',id=f'RIP80_{net}_{len(ops)}',net=net,layer=layer,points=pts,width=w))
 def via(net,xy,small=False):add(dict(type='via',id=f'ADD80_{net}_{xy}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT' if small else 'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3))
 def route(net,layer,pts,w):add(dict(type='route',id=f'ADD80_{net}_{layer}_{len(ops)}',net=net,layer=layer,points=pts,width=w))
 for z in list(n['routes']):
  if z['net']=='GPIO_PB1' and not z.get('generatedThermal'):ds(z['net'],z['layer'].removeprefix('ETCH/'),z['startEnd'],z['width'])
 dv('GPIO_PB1',[38.3,27.35]);dv('V3V3',[37,24]);ds('V3V3','BOTTOM',[[37,25.7],[37,24]],.6)
 dv('GND',[35.8,21.95]);via('GND',[35.65,22.1],True)
 if v=='2L':
  dv('GND',[37.4,27.4]);via('GND',[36.92,27.8])
  for o in load(P/'PB15_engineered_access_2L_59.json')['operations']:
   if o['net']=='VBUS_PRESENT_N':add(o)
 via('V3V3',[37.2,24.3]);via('GPIO_PB1',[41.9,26.79],True);via('GPIO_PB1',[36.25,21.35],True);via('GPIO_PB1',[34.2,20.0],True)
 route('V3V3','BOTTOM',[[37,25.7],[37,24.5],[37.2,24.3]],.6);route('V3V3','TOP',[[37,24],[37.2,24.2],[37.2,24.3]],.6)
 route('GPIO_PB1','TOP',[[35.75,26.75],[37,26.75]],.16);route('GPIO_PB1','TOP',[[37,26.75],[37.35,27.1],[38.3,27.1],[38.81,26.59],[41,26.59],[41.2,26.79],[41.9,26.79]],.2)
 route('GPIO_PB1','BOTTOM',[[41.9,26.79],[41.9,23.55],[36.7,23.55],[36.7,21.8],[36.25,21.35]],.2);route('GPIO_PB1','TOP',[[36.25,21.35],[35.55,21.35],[34.2,20]],.2)
 # Apply deletions and via changes before checking added routes as a complete construction transaction.
 for o in ops:
  if o['type'] in ['deleteVia','deleteSegment','via']:apply(o)
 s=CopperScene(n,nw,rs,p)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias'] if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(vv.get('padDiameterMM',.52 if '026_C052' in vv['padstack'].upper() else .6)/2,quad_segs=16)
 checks=[]
 for op in ops:
  if op['type']=='route':
   clear=s.path_clear(op['net'],op['layer'],op['points'],op['width']);hits=[]
   if not clear:
    ln=LineString(op['points'])
    for oo in s.obstacles:
     if oo['net']==op['net'] or oo['layer']!=op['layer']:continue
     d=ln.distance(oo['geometry'])-op['width']/2;gap=s.space(op['net'],oo['net'],op['layer'],oo['kind'])
     if d<gap:hits.append(dict(net=oo['net'],kind=oo['kind'],source=oo['source'],bbox=oo['geometry'].bounds,gap=d,required=gap))
    for a in p['reservedAreas']:
     if op['layer'] in a.get('layers',LAYERS) and op['net']not in a.get('allowedNets',[]) and ln.distance(Polygon(a['polygon']))<op['width']/2+.001:hits.append(a)
   checks.append(dict(id=op['id'],clear=clear,hits=hits));s.add_operation(op)
  elif op['type']=='via':
   bad=[]
   for lay in LAYERS:
    for oo in s.obstacles:
     if oo['net']==op['net'] or oo['layer']!=lay:continue
     d=Point(op['xy']).distance(oo['geometry'])-op['padDiameterMM']/2;gap=s.space(op['net'],oo['net'],lay,oo['kind'],True)
     if d<gap:bad.append(dict(layer=lay,net=oo['net'],kind=oo['kind'],source=oo['source'],bbox=oo['geometry'].bounds,gap=d,required=gap))
   checks.append(dict(id=op['id'],clear=not bad,hits=bad))
 for o in ops:
  if o['type']=='route':apply(o)
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PB1':a['xy']=[34.2,20];a['layers']=['TOP','BOTTOM']
 p['pendingOperations']=[dict(type='route',id='J12_SOUTH_V3_SUPPLY80',net='V3V3',layer='TOP',points=[[33.3,1],[9.11,1],[9.11,9]],width=.6)]
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p),('delta',ops),('check',checks)]: (P/f'GPIO_PB1_inward_{v}_80_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,json.dumps(checks))
