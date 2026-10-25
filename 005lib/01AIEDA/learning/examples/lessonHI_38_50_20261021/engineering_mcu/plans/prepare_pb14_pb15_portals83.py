import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_PB1_inward_{v}_80_snapshot.json');nw=load(P/f'GPIO_PB1_inward_{v}_80_networks.json');rs=load(P/f'GPIO_PB1_inward_{v}_80_rules.json');p=load(P/f'GPIO_PB1_inward_{v}_80_policy.json');ops=[]
 def dv(net,xy):
  zz=[z for z in n['vias']if z['net']==net and math.dist(z['xy'],xy)<1e-6];assert len(zz)==1;n['vias'].remove(zz[0]);ops.append(dict(type='deleteVia',id=f'RIP83_{net}_{xy}',net=net,xy=xy))
 def ds(z):
  n['routes'].remove(z);ops.append(dict(type='deleteSegment',id=f'RIP83_{z["net"]}_{len(ops)}',net=z['net'],layer=z['layer'].removeprefix('ETCH/'),points=z['startEnd'],width=z['width']))
 def via(net,xy,small=True):
  op=dict(type='via',id=f'ADD83_{net}_{xy}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT'if small else'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3);ops.append(op);n['vias'].append(dict(op,pads=[]))
 def route(net,layer,pts,w):ops.append(dict(type='route',id=f'ADD83_{net}_{layer}_{len(ops)}',net=net,layer=layer,points=pts,width=w))
 dv('GPIO_PB14',[38,21.25]);dv('GPIO_PB15',[38.5,20.7 if v=='2L' else 20.675]);dv('GND',[38,20]);dv('GND',[38.8,19.7]);via('GND',[38,18]);via('GND',[38.9,19.55]);via('GPIO_PB14',[34.3,19.25]);via('GPIO_PB15',[38.7,20.45]);via('GPIO_PB15',[37,18.75]);via('GPIO_PB15',[34.3,17.4])
 for z in list(n['routes']):
  if z['net']=='GPIO_PB15' and not z.get('generatedThermal'):ds(z)
 route('GPIO_PB15','TOP',[[38.75,22.75],[38.75,21.8],[38.7,21.75],[38.7,20.45]],.16)
 route('GPIO_PB14','TOP',[[38,21.25],[38.1,21.15],[38.1,19.5],[35.7,19.5],[34.3,19.25]],.2)
 route('GPIO_PB15','BOTTOM',[[38.7,20.45],[37.0,18.75]],.2)
 route('GPIO_PB15','TOP',[[37,18.75],[35.65,18.75],[34.3,17.4]],.2)
 if v=='2L':
  zz=[z for z in n['routes'] if z['net']=='VBUS_PRESENT_N' and z.get('futureCandidate')=='PB15_2L_VBUS_FINITE_BYPASS'];assert zz
  for z in zz:ds(z)
  route('VBUS_PRESENT_N','BOTTOM',[[34.75,23.15],[34.95,22.95],[34.95,18.8],[34.4,18.25],[34.4,18.15]],.2)
 s=CopperScene(n,nw,rs,p)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias']if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(vv.get('padDiameterMM',.52 if '026_C052' in vv['padstack'].upper() else .6)/2,quad_segs=16)
 checks=[]
 for op in ops:
  if op['type']=='route':
   ok=s.path_clear(op['net'],op['layer'],op['points'],op['width']);hits=[]
   if not ok:
    ln=LineString(op['points'])
    for o in s.obstacles:
     if o['net']==op['net']or o['layer']!=op['layer']:continue
     d=ln.distance(o['geometry'])-op['width']/2;g=s.space(op['net'],o['net'],op['layer'],o['kind'])
     if d<g:hits.append(dict(net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=d,required=g))
    for a in p['reservedAreas']:
     if op['layer']in a.get('layers',LAYERS)and op['net']not in a.get('allowedNets',[])and ln.distance(Polygon(a['polygon']))<op['width']/2+.001:hits.append(a)
   checks.append(dict(id=op['id'],clear=ok,hits=hits));s.add_operation(op)
  elif op['type']=='via':
   hits=[]
   for l in LAYERS:
    for o in s.obstacles:
     if o['layer']!=l or o['net']==op['net']:continue
     d=Point(op['xy']).distance(o['geometry'])-op['padDiameterMM']/2;g=s.space(op['net'],o['net'],l,o['kind'],True)
     if d<g:hits.append(dict(layer=l,net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=d,required=g))
   checks.append(dict(id=op['id'],clear=not hits,hits=hits))
 for op in ops:
  if op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],generatedThermal=False,futureCandidate=op['id']))
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PB14':a['xy']=[34.3,19.25];a['layers']=['TOP','BOTTOM']
  if a['net']=='GPIO_PB15':a['xy']=[34.3,17.4];a['layers']=['TOP','BOTTOM']
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p),('delta',ops),('check',checks)]: (P/f'GPIO_PB14_PB15_{v}_83_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,json.dumps(checks))

