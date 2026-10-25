import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(H/f'review/b020_engineering/PB10_NW_{v}_v46_snapshot.json');B=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');p=load(P/f'GPIO_PB1_inward_{v}_80_policy.json')
 def apply(op):
  if op['type']=='via':n['vias'].append(dict(op,pads=[]))
  elif op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],generatedThermal=False,futureCandidate=op['id']))
  elif op['type']=='deleteVia':
   z=[x for x in n['vias']if x['net']==op['net']and math.dist(x['xy'],op['xy'])<1e-6];assert len(z)==1;n['vias'].remove(z[0])
  elif op['type']=='deleteSegment':
   z=[x for x in n['routes']if x['net']==op['net']and x['layer']=='ETCH/'+op['layer']and abs(x['width']-op['width'])<1e-6 and x['startEnd']in[op['points'],op['points'][::-1]]];assert len(z)==1;n['routes'].remove(z[0])
  else:raise Exception(op)
 for op in load(P/f'GPIO6_{v}_manualPortal81.json')['operations']:apply(op)
 for op in load(P/f'PB15_attach_{v}_87_delta.json'):
  if op['net']in['USB_ATTACH_N','GPIO_PB15']:apply(op)
 q=next(z for z in n['placements']if z['ref']=='J12');assert q['xy']==[40,55];q['xy']=[18,9]
 for pin in q['pins']:pin['xy']=[pin['xy'][0]-22,pin['xy'][1]-46];pin['padBBox']=[[pt[0]-22,pt[1]-46]for pt in pin['padBBox']]
 for net in nw['nets']:
  for c in net['components']:
   for t in c['terminals']:
    if t['key'].startswith('J12.'):t['xy']=[t['xy'][0]-22,t['xy'][1]-46]
 for z in p['routeWindows']:
  if 'GPIO_PB10'in z['nets']:z['nets'].remove('GPIO_PB10')
 p['routeWindows'].append(dict(nets=['GPIO_PB10'],polygon=[[7,6.3],[70,6.3],[70,57],[7,57]]))
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PB10':a['xy']=[28,36.1];a['layers']=['TOP']
 ops=[]
 def via(net,xy,small=True):ops.append(dict(type='via',id=f'PB10_91_{net}_V{len(ops)}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT'if small else'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3))
 def rt(net,l,pts,w):ops.append(dict(type='route',id=f'PB10_91_R{len(ops)}',net=net,layer=l,points=pts,width=w))
 rt('GPIO_PB10','TOP',[[28,36.1],[24,36.1]],.2);via('GPIO_PB10',[24,36.1]);via('GND',[25,35.1],False)
 rt('GPIO_PB10','BOTTOM',[[24,36.1],[8.5,36.1],[8.5,6.8],[16.73,6.8]],.2);via('GPIO_PB10',[16.73,6.8]);via('GND',[17.73,6.8],False);rt('GPIO_PB10','TOP',[[16.73,6.8],[16.73,9]],.2)
 for op in ops:apply(op)
 s=CopperScene(n,nw,rs,p)
 for o in s.obstacles:
  if o['kind']=='via'and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias']if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(vv.get('padDiameterMM',.52 if '026_C052'in vv['padstack'].upper()else .6)/2,quad_segs=16)
 checks=[]
 for op in ops:
  gg=Point(op['xy'])if op['type']=='via'else LineString(op['points']);rr=op['padDiameterMM']/2 if op['type']=='via'else op['width']/2;hits=[]
  for lay in LAYERS if op['type']=='via'else[op['layer']]:
   for o in s.obstacles:
    if o['net']==op['net']or o['layer']!=lay:continue
    d=gg.distance(o['geometry'])-rr;g=s.space(op['net'],o['net'],lay,o['kind'],op['type']=='via')
    if d<g:hits.append(dict(layer=lay,net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=d,required=g))
   for z in p['reservedAreas']:
    if lay in z.get('layers',LAYERS)and op['net']not in z.get('allowedNets',[])and gg.distance(Polygon(z['polygon']))<rr+.001:hits.append(dict(reservation=z['id']))
  checks.append(dict(id=op['id'],clear=not hits,hits=hits))
 data=dict(status='MANUAL_COMPLETE_PB10_SOUTH_CANDIDATE_NOT_NATIVE',variant=v,operations=ops,checks=checks,sourcePrerequisites='f29 b019+80adapted+North4 repack46 then81 four-long and87 Attach+PB15 source; J12 candidate south; supply pending32.19mm',signalAddedLengthMM=sum(LineString(o['points']).length for o in ops if o['type']=='route'and o['net']=='GPIO_PB10'),qualification='Complete route from explicit TOP portal28,36.1 toJ12.4; source46 and return/reference review independent, no manufacturing/DRC claim')
 for t,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p),('candidate',data)]: (P/f'PB10_south_{v}_91_{t}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,json.dumps(data))
