import pathlib,json,sys,math,copy
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
from shapely import affinity
for v in ['2L','4L']:
 n=load(P/f'GPIO_future_{v}_28_snapshot.json');pol=load(P/f'GPIO_future_{v}_28_policy.json');nw=load(P/f'GPIO_future_{v}_21_networks.json');rs=load(P/f'GPIO_future_{v}_21_rules.json');removed=[];added=[]
 def rem(test):
  global n
  ms=[r for r in n['routes'] if test(r)];removed.extend(ms);n['routes']=[r for r in n['routes'] if r not in ms];return ms
 def route(net,pts,w,id):
  added.append(dict(type='route',id=id,net=net,layer='TOP',points=pts,width=w))
  for a,b in zip(pts,pts[1:]):n['routes'].append(dict(net=net,layer='ETCH/TOP',width=w,startEnd=[a,b],generatedThermal=False,fixedManualCline=True,kind='line',futureCandidate=id))
 def via(net,xy,tiny,id):
  d=.52 if tiny else .6;pad='HI_VIA026_C052_TENT' if tiny else 'L28_VIA030_C060';added.append(dict(type='via',id=id,net=net,xy=xy,padstack=pad,padDiameterMM=d,drillDiameterMM=.26 if tiny else .3));n['vias'].append(dict(net=net,xy=xy,padstack=pad,padDiameterMM=d,drillDiameterMM=.26 if tiny else .3,futureCandidate=id))
 assert len(rem(lambda r:r['net']=='GPIO_PC13' and r['layer']=='ETCH/BOTTOM'))==2
 for net in ['GPIO_PA1','GPIO_PA2']:rem(lambda r:r['net']==net);n['vias']=[z for z in n['vias'] if z['net']!=net]
 route('GPIO_PA1',[[37.75,31.25],[37.75,32.35],[37,32.35]],.16,'NEW_PA1_OUTWARD');via('GPIO_PA1',[37,32.35],True,'NEW_PA1_VIA')
 route('GPIO_PA2',[[37.25,31.25],[37.25,31.95],[36.15,31.95]],.16,'NEW_PA2_OUTWARD');via('GPIO_PA2',[36.15,31.95],True,'NEW_PA2_VIA')
 c=next(c for c in n['placements'] if c['ref']=='C18');delta=[-.4,.9]
 for p in c['pins']:
  p['xy']=[a+b for a,b in zip(p['xy'],delta)];p['padBBox']=[[a+b for a,b in zip(pt,delta)] for pt in p['padBBox']]
 c['xy']=[a+b for a,b in zip(c['xy'],delta)];c['bodyExtent']=[[a+b for a,b in zip(pt,delta)] for pt in c['bodyExtent']]
 rem(lambda r:r['net']=='VDDA' and r['layer']=='ETCH/TOP' and (any(math.dist(p,[37,33.2])<1e-5 for p in r['startEnd']) or (r['startEnd'][0][0]>=35.89 and r['startEnd'][1][0]>=35.89)))
 route('VDDA',[[38.75,31.25],[38.75,32.1],[39,32.35]],.25,'VDDA_NEW_NECK')
 route('VDDA',[[39,32.35],[39,33.5],[38.4,34.1],[36.6,34.1]],.6,'VDDA_NEW_CAP')
 route('VDDA',[[36.6,34.1],[35.9,34.8],[35.9,35.9],[34.8,37]],.6,'VDDA_NEW_BULK')
 rem(lambda r:r['net']=='GND' and r['layer']=='ETCH/TOP' and any(math.dist(p,[37,34.7748])<1e-5 for p in r['startEnd']));n['vias']=[z for z in n['vias'] if not(z['net']=='GND' and math.dist(z['xy'],[37.9,34.7748])<1e-5)]
 route('GND',[[36.6,35.6748],[37.5,35.6748]],.6,'C18_NEW_GND');via('GND',[37.5,35.6748],False,'C18_NEW_GND_VIA')
 rem(lambda r:r['net']=='ADC0' and r['layer']=='ETCH/TOP' and not r.get('futureCandidate'))
 route('ADC0',[[38.25,31.25],[38.25,32.3],[38.2,32.35],[38.2,33.05],[34.8,33]],.2,'ADC_MAIN_NEW_NORTH')
 pins={p['number']:p for c in n['placements'] if c['ref']=='U1' for p in c['pins']}
 for a in pol['componentAnchors']:
  if a['net'] in ['GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15','GPIO_PB1','GPIO_PB10','GPIO_PB11']:a['xy']=pins[a['connectedTo'].split('.')[1]]['xy'];a['layers']=['TOP']
  if a['net']=='GPIO_PC13':a['xy']=[42,28.9];a['layers']=['TOP','BOTTOM']
  if a['net']=='GPIO_PA1':a['xy']=[37,32.35];a['layers']=['BOTTOM']
  if a['net']=='GPIO_PA2':a['xy']=[36.15,31.95];a['layers']=['BOTTOM']
 pol['regionOverrides'].append(dict(id='NORTH_NEW_PAD_ESCAPE',layer='TOP',polygon=[[36.8,30.6],[38.9,30.6],[38.9,32.5],[36.8,32.5]],netPairs=[[a,b] for a in ['GPIO_PA1','GPIO_PA2','ADC0','VDDA'] for b in ['GPIO_PA1','GPIO_PA2','ADC0','VDDA'] if a!=b],kinds=['smdpin','line'],gap=.2))
 pol['studyStatus']='SOURCE_TOPOLOGY_COMPARISON_NOT_NATIVE; PC13 bar rerouted by candidate long planner, PA1/2 outside MCU, C18+ADC route shifted to clear north pins. Inward PB old outward stubs remain temporarily and must remove in final delta.'
 for typ,q in [('snapshot',n),('policy',pol)]: (P/f'GPIO_future_{v}_30_{typ}.json').write_text(json.dumps(q,indent=2),encoding='utf8')
 scene=CopperScene(n,nw,rs,pol)
 for o in scene.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   z=next(z for z in n['vias'] if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-5);o['geometry']=Point(z['xy']).buffer(z.get('padDiameterMM',.6)/2,quad_segs=24)
 fresh=[]
 for o in added:
  if o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):fresh.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(o['width']/2,quad_segs=24),kind='line',source=o['id']))
  else:
   for l in LAYERS:fresh.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(o['padDiameterMM']/2,quad_segs=24),kind='via',source=o['id']))
 issues=[]
 for a in fresh:
  for b in scene.obstacles:
   if a['net']==b['net'] or a['layer']!=b['layer']:continue
   d=a['geometry'].distance(b['geometry']);gap=scene.space(a['net'],b['net'],a['layer'],b['kind'],a['kind']=='via')
   # actual declared finite source spacing applied only where a and b intersect its polygon
   if a['kind']=='line':
    for poly,ex in scene.regions:
     if ex.get('layer')==a['layer'] and b['kind'] in ex.get('kinds',[]) and any(set(p)=={a['net'],b['net']} for p in ex.get('netPairs',[])) and poly.covers(a['geometry'].intersection(b['geometry'].buffer(gap))):gap=min(gap,ex['gap'])
   if d<gap-1e-5:issues.append(dict(new=a['source'],net=a['net'],other=b['source'],otherNet=b['net'],layer=a['layer'],distance=d,required=gap,bbox=list(b['geometry'].bounds)))
 for c in n['placements']:
  if c['ref']=='C18':continue
  if box(*c['bodyExtent'][0],*c['bodyExtent'][1]).intersection(box(*next(z for z in n['placements'] if z['ref']=='C18')['bodyExtent'][0],*next(z for z in n['placements'] if z['ref']=='C18')['bodyExtent'][1])).area>1e-6:issues.append(dict(placeBound='C18 vs '+c['ref']))
 (P/f'GPIO_source_topology30_{v}_precheck.json').write_text(json.dumps(dict(status='STUDY_ONLY',added=added,removed=removed,issues=issues),indent=2),encoding='utf8');print(v,'issues',len(issues));print(json.dumps(issues[:12],indent=1))
