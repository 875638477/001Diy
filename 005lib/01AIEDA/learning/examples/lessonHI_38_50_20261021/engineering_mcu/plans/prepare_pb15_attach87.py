import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_PB1_inward_{v}_80_snapshot.json');nw=load(P/f'GPIO_PB1_inward_{v}_80_networks.json');rs=load(P/f'GPIO_PB1_inward_{v}_80_rules.json');p=load(P/f'GPIO_PB1_inward_{v}_80_policy.json');ops=[]
 for op in load(P/f'GPIO6_{v}_manualPortal81.json')['operations']:
  if op['type']=='via':n['vias'].append(dict(op,pads=[]))
  elif op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],generatedThermal=False,futureCandidate=op['id']))
 def ds(z):n['routes'].remove(z);ops.append(dict(type='deleteSegment',id=f'RIP87_{len(ops)}',net=z['net'],layer=z['layer'].removeprefix('ETCH/'),points=z['startEnd'],width=z['width']))
 def route(net,layer,pts,w):ops.append(dict(type='route',id=f'ADD87_{net}_{layer}_{len(ops)}',net=net,layer=layer,points=pts,width=w))
 z=next(z for z in n['vias']if z['net']=='USB_ATTACH_N'and z['xy']==[39,21.2]);n['vias'].remove(z);ops.append(dict(type='deleteVia',id='RIP87_ATTACH_VIA',net='USB_ATTACH_N',xy=[39,21.2]))
 for z in list(n['routes']):
  if z['net']=='USB_ATTACH_N'and not z.get('generatedThermal')and ((z['layer']=='ETCH/TOP'and max(pt[0]for pt in z['startEnd'])<40)or(z['layer']=='ETCH/BOTTOM'and min(pt[0]for pt in z['startEnd'])<39.71 and max(pt[0]for pt in z['startEnd'])<40)):ds(z)
 ops.append(dict(type='via',id='ADD87_ATTACH_VIA',net='USB_ATTACH_N',xy=[39.14,21.2],padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26))
 route('USB_ATTACH_N','TOP',[[39.25,22.75],[39.25,22.1],[39.14,21.99],[39.14,21.2]],.16)
 route('USB_ATTACH_N','BOTTOM',[[39.14,21.2],[39.14,20.44],[39.7,19.88],[39.7,18.6]],.2)
 zz=[]
 for z in list(n['routes']):
  if z['net']=='GPIO_PB1'and z['layer']=='ETCH/BOTTOM'and z['startEnd']in[[[41.9,26.79],[41.9,23.55]],[[41.9,23.55],[36.7,23.55]]]:zz.append(z);ds(z)
 assert len(zz)==2
 route('GPIO_PB1','BOTTOM',[[41.9,26.79],[40.8,25.69],[40.8,23.55],[36.7,23.55]],.2)
 route('GPIO_PB15','BOTTOM',[[38.5,20.7 if v=='2L'else 20.675],[38.57,20.77],[38.57,21.8],[38.7,21.93],[38.7,22.95],[41.25,22.95],[41.6,23.3],[47.1,23.3]],.2)
 for op in ops:
  if op['type']=='via':n['vias'].append(dict(op,pads=[]))
 # All new features simultaneously present before pair checks; no ordering blind spot.
 for op in ops:
  if op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],generatedThermal=False,futureCandidate=op['id']))
 if v=='4L':
  for z in p['reservedAreas']:
   if z['id'].startswith('USB_SHARED_REFERENCE_'):z['layers']=[]
 s=CopperScene(n,nw,rs,p)
 for o in s.obstacles:
  if o['kind']=='via'and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias']if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(vv.get('padDiameterMM',.52 if '026_C052'in vv['padstack'].upper()else .6)/2,quad_segs=16)
 checks=[]
 for op in ops:
  if op['type']not in ['route','via']:continue
  gg=Point(op['xy'])if op['type']=='via'else LineString(op['points']);rr=.26 if op['type']=='via'else op['width']/2;hits=[]
  for lay in LAYERS if op['type']=='via'else[op['layer']]:
   for o in s.obstacles:
    if o['net']==op['net']or o['layer']!=lay:continue
    d=gg.distance(o['geometry'])-rr;g=s.space(op['net'],o['net'],lay,o['kind'],op['type']=='via')
    if d<g:hits.append(dict(layer=lay,net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=d,required=g))
   for z in p['reservedAreas']:
    if lay in z.get('layers',LAYERS)and op['net']not in z.get('allowedNets',[])and gg.distance(Polygon(z['polygon']))<rr+.001:hits.append(dict(reservation=z['id']))
  ok=not hits if op['type']=='via'else s.path_clear(op['net'],op['layer'],op['points'],op['width'])
  checks.append(dict(id=op['id'],clear=ok,hits=hits))
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PB15':a['xy']=[47.1,23.3];a['layers']=['BOTTOM']
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p),('delta',ops),('check',checks)]: (P/f'PB15_attach_{v}_87_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,json.dumps(checks))
