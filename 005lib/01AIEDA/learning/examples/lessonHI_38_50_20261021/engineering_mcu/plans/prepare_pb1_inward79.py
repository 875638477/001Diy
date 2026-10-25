import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(P/f'GPIO_J12south_{v}_68_snapshot.json');nw=load(P/f'GPIO_J12south_{v}_68_networks.json');rs=load(P/f'GPIO_J12south_{v}_68_rules.json');p=load(P/f'GPIO_J12south_{v}_68_policy.json');ops=[]
 def dv(net,xy):
  zz=[z for z in n['vias'] if z['net']==net and math.dist(z['xy'],xy)<1e-6];assert len(zz)==1;n['vias'].remove(zz[0]);ops.append(dict(type='deleteVia',id=f'RIP79_{net}_{xy[0]}_{xy[1]}',net=net,xy=xy,padstack=zz[0]['padstack']))
 def via(net,xy,small=False):
  op=dict(type='via',id=f'ADD79_{net}_{xy[0]}_{xy[1]}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT' if small else 'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3);ops.append(op);n['vias'].append(dict(op,pads=[]))
 def route(net,layer,pts,w):
  op=dict(type='route',id=f'ADD79_{net}_{layer}_{len(ops)}',net=net,layer=layer,points=pts,width=w);ops.append(op)
 def ds(net,layer,pts,w):
  zz=[z for z in n['routes'] if z['net']==net and z['layer']=='ETCH/'+layer and abs(z['width']-w)<1e-6 and z['startEnd'] in [pts,pts[::-1]]];assert len(zz)==1;n['routes'].remove(zz[0]);ops.append(dict(type='deleteSegment',id=f'RIP79_{net}_{layer}_{len(ops)}',net=net,layer=layer,points=pts,width=w))
 for z in list(n['routes']):
  if z['net']=='GPIO_PB1' and not z.get('generatedThermal'):ds(z['net'],z['layer'].removeprefix('ETCH/'),z['startEnd'],z['width'])
 dv('GPIO_PB1',[38.3,27.35]);dv('V3V3',[37,24]);ds('V3V3','BOTTOM',[[37,25.7],[37,24]],.6)
 dv('GND',[35.8,21.95]);via('GND',[36.2,22.4],True)
 if v=='2L':dv('GND',[37.4,27.4]);via('GND',[36.92,27.8])
 via('V3V3',[37.2,24.35]);via('GPIO_PB1',[41.9,26.79],True)
 route('V3V3','BOTTOM',[[37,25.7],[37,24.55],[37.2,24.35]],.6);route('V3V3','TOP',[[37,24],[37.2,24.2],[37.2,24.35]],.6)
 route('GPIO_PB1','TOP',[[35.75,26.75],[37,26.75]],.16);route('GPIO_PB1','TOP',[[37,26.75],[37.35,27.1],[38.3,27.1],[38.81,26.59],[41,26.59],[41.2,26.79],[41.9,26.79]],.2)
 via('GPIO_PB1',[35.6,21.75],True);via('GPIO_PB1',[34.2,21.75],True);route('GPIO_PB1','BOTTOM',[[41.9,26.79],[41.9,23.6],[36.7,23.6],[36.7,21.75],[35.6,21.75]],.2);route('GPIO_PB1','TOP',[[35.6,21.75],[34.2,21.75]],.2)
 s=CopperScene(n,nw,rs,p)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias'] if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(.26 if '026_C052' in vv['padstack'].upper() else .3,quad_segs=16)
 checks=[]
 for op in ops:
  if op['type']=='route':
   clear=s.path_clear(op['net'],op['layer'],op['points'],op['width']);checks.append(dict(id=op['id'],clear=clear))
   if not clear:
    ln=LineString(op['points']);hits=[]
    for oo in s.obstacles:
     if oo['net']==op['net'] or oo['layer']!=op['layer']:continue
     d=ln.distance(oo['geometry'])-op['width']/2;gap=s.space(op['net'],oo['net'],op['layer'],oo['kind'])
     if d<gap:hits.append(dict(net=oo['net'],kind=oo['kind'],source=oo['source'],bbox=oo['geometry'].bounds,gap=d,required=gap))
    for a in p['reservedAreas']:
     if op['layer'] in a.get('layers',LAYERS) and op['net']not in a.get('allowedNets',[]) and ln.distance(Polygon(a['polygon']))<op['width']/2+.001:hits.append(a)
    checks[-1]['hits']=hits
   s.add_operation(op)
  elif op['type']=='via':
   # Via already added to temporary n above; test exact all-layer same-net-independent geometric mask.
   bad=[]
   for lay in LAYERS:
    for oo in s.obstacles:
     if oo['net']==op['net'] or oo['layer']!=lay:continue
     d=Point(op['xy']).distance(oo['geometry'])-op['padDiameterMM']/2;gap=s.space(op['net'],oo['net'],lay,oo['kind'],True)
     if d<gap:bad.append(dict(layer=lay,net=oo['net'],kind=oo['kind'],source=oo['source'],bbox=oo['geometry'].bounds,gap=d,required=gap))
   checks.append(dict(id=op['id'],clear=not bad,hits=bad))
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PB1':a['xy']=[34.2,21.75];a['layers']=['BOTTOM']
 p['pendingOperations']=p.get('pendingOperations',[])+[o for o in ops if o['type']=='route']
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p),('delta',ops),('check',checks)]: (P/f'GPIO_PB1_inward_{v}_79_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,json.dumps(checks))

