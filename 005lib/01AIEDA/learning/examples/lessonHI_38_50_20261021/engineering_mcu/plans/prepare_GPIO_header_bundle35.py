import pathlib,json,sys,math,hashlib,copy
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
fix=load(P/'GPIO_LEFT_NORTH_spacing_fix_09.json')
for v in ['2L','4L']:
 B=H/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING';n=load(B/'normalized.json');nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');pol=load(P/f'GPIO_future_{v}_32_policy.json');assert nw.get('nativeLog',nw.get('readback'))==n['readbackDirectory']
 for op in fix['operations']:
  if op['type']=='deleteSegment':
   ms=[r for r in n['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and r['startEnd'] in [op['points'],list(reversed(op['points']))]];assert len(ms)==1,(v,op,len(ms));n['routes'].remove(ms[0])
  elif op['type']=='deleteVia':
   ms=[z for z in n['vias'] if z['net']==op['net'] and math.dist(z['xy'],op['xy'])<1e-6];assert len(ms)==1;n['vias'].remove(ms[0])
  elif op['type']=='via':n['vias'].append(dict(net=op['net'],xy=op['xy'],padstack=op['padstack'],padDiameterMM=op['padDiameterMM'],drillDiameterMM=op['drillDiameterMM']))
  elif op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],kind='line',generatedThermal=False,fixedManualCline=True,futureCandidate=op['id']))
 for a in pol['componentAnchors']:
  if a['net'] in fix['partialEndpoints']:a['xy']=fix['partialEndpoints'][a['net']]['xy']
 # Classify and remove confirmed original R25 dead V3 stub. No other geometry ripup.
 for pts in [[[31.11,55],[31.11,47]],[[31.11,47],[38.1016,47]]]:
  ms=[r for r in n['routes'] if r['net']=='V3V3' and r['layer']=='ETCH/TOP' and r['startEnd'] in [pts,list(reversed(pts))]];assert len(ms)==1;n['routes'].remove(ms[0])
 c=next(c for c in n['placements'] if c['ref']=='J12');assert c['xy']==[40,55] and c['rotation']==90;delta=[-22,-46];c['xy']=[18,9]
 for key in ['bodyExtent','bbox']:c[key]=[[a+b for a,b in zip(pt,delta)] for pt in c[key]]
 for p in c['pins']:p['xy']=[a+b for a,b in zip(p['xy'],delta)];p['padBBox']=[[a+b for a,b in zip(pt,delta)] for pt in p['padBBox']]
 for nn in nw['nets']:
  for cc in nn['components']:
   for t in cc['terminals']:
    if t['key'].startswith('J12.'):t['xy']=[a+b for a,b in zip(t['xy'],delta)]
 for q in pol['routeWindows']:
  if any(z.startswith('GPIO_') for z in q['nets']):q['polygon']=[[7,7],[70,7],[70,57],[7,57]]
 ops=[]
 def route(id,net,layer,pts,w=.2):ops.append(dict(type='route',id=id,net=net,layer=layer,points=pts,width=w,purpose='Engineered ordinary GPIO bundle with explicit transition/GND return; native and actual reference review pending.'))
 def via(id,net,xy):ops.append(dict(type='via',id=id,net=net,xy=xy,padstack='L28_VIA030_C060',padDiameterMM=.6,drillDiameterMM=.3,purpose='Explicit signal transition or shared-reference return via.'))
 route('J12_NEW_V3_PROVISIONAL','V3V3','TOP',[[33.3,1],[9.11,1],[9.11,9]],.6)
 route('N35_PC15_BOTTOM','GPIO_PC15','BOTTOM',[[35.4,28.75],[28.15,36],[20,41]]);via('N35_PC15_VIA','GPIO_PC15',[20,41]);route('N35_PC15_TOP','GPIO_PC15','TOP',[[20,41],[19.27,41.73],[19.27,55]])
 route('N35_PA1_BOTTOM','GPIO_PA1','BOTTOM',[[37.5,29.6],[35.5,29.6],[29.1,36],[23,41]]);via('N35_PA1_VIA','GPIO_PA1',[23,41]);route('N35_PA1_TOP','GPIO_PA1','TOP',[[23,41],[21.81,42.19],[21.81,55]])
 route('N35_PA2_BOTTOM','GPIO_PA2','BOTTOM',[[36.6,30.4],[35.8,30.4],[30.2,36],[26,40],[26,41]]);via('N35_PA2_VIA','GPIO_PA2',[26,41]);route('N35_PA2_TOP','GPIO_PA2','TOP',[[26,41],[24.35,42.65],[24.35,55]])
 route('N35_PA3_BOTTOM','GPIO_PA3','BOTTOM',[[35.2,31.65],[30.85,36],[29,41]]);via('N35_PA3_VIA','GPIO_PA3',[29,41]);route('N35_PA3_TOP','GPIO_PA3','TOP',[[29,41],[26.89,41],[26.89,55]])
 route('N35_PC13_BOTTOM','GPIO_PC13','BOTTOM',[[35.8,31.1],[35.8,31.55],[35.85,31.6],[35.85,33.2],[14.2,54.85],[14.2,55],[14.19,55]])
 route('N35_PC14_BOTTOM','GPIO_PC14','BOTTOM',[[49.2,25.2],[49.2,26.5],[50.5,27.8],[50.5,43]]);via('N35_PC14_VIA','GPIO_PC14',[50.5,43]);route('N35_PC14_TOP','GPIO_PC14','TOP',[[50.5,43],[50.5,56.7],[16.73,56.7],[16.73,55]])
 for id,xy in [('PC15',[20,39.8]),('PA1',[23,39.8]),('PA2',[25,40.7]),('PA3',[30,41]),('PC14_N',[51.5,43]),('PC14_S',[50.4,25.2])]:via('N35_GND_'+id,'GND',xy)
 scene=CopperScene(n,nw,rs,pol)
 for o in scene.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   vv=next(z for z in n['vias'] if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(.26 if '026_C052' in vv['padstack'].upper() else .3,quad_segs=32)
 fresh=[]
 for op in ops:
  if op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):fresh.append(dict(net=op['net'],layer=op['layer'],kind='line',geometry=LineString([a,b]).buffer(op['width']/2,quad_segs=32),source=op['id']))
  else:
   for l in LAYERS:fresh.append(dict(net=op['net'],layer=l,kind='via',geometry=Point(op['xy']).buffer(.3,quad_segs=32),source=op['id']))
 issues=[]
 for i,a in enumerate(fresh):
  for b in scene.obstacles+fresh[:i]:
   if a['net']==b['net'] or a['layer']!=b['layer']:continue
   d=a['geometry'].distance(b['geometry']);gap=scene.space(a['net'],b['net'],a['layer'],b['kind'],a['kind']=='via')
   if d<gap-1e-5:issues.append(dict(a=a['source'],net=a['net'],b=b['source'],otherNet=b['net'],layer=a['layer'],distance=d,required=gap,bbox=b['geometry'].bounds))
 for op in ops:
  if op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):n['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],width=op['width'],startEnd=[a,b],kind='line',generatedThermal=False,fixedManualCline=True,futureCandidate=op['id']))
  else:n['vias'].append(dict(net=op['net'],xy=op['xy'],padstack=op['padstack'],padDiameterMM=.6,drillDiameterMM=.3,futureCandidate=op['id']))
 pol['engineeredNorthOperations']=ops;pol['headerPlacementChange']=dict(ref='J12',xy=[18,9],rotation=90,purpose='Alternative routing/return tradeoff candidate, not native authorization.');pol['candidateMustRebase']='Actual b015 pending native has source spacing failures; root allfix changes still require incorporation before final.'
 for typ,q in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_future_{v}_35_{typ}.json').write_text(json.dumps(q,indent=2),encoding='utf8')
 report=dict(status='ENGINEERED_NORTH_BUNDLE_REQUIRES_CORRECTION' if issues else 'ENGINEERED_NORTH_BUNDLE_GEOMETRY_PENDING_REFERENCE_NATIVE',base=str(B),issues=issues,operations=ops);(P/f'GPIO_north_bundle35_{v}_review.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(v,'issues',len(issues));print(json.dumps(issues[:25],indent=1))
