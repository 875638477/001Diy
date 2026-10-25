import pathlib,json,sys,math,hashlib,copy,itertools
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
from shapely import affinity
own=[P/'GPIO_north_joint_fanout_02.json',P/'GPIO_south_joint_fanout_05.json',P/'GPIO_left_joint_fanout_04.json',H/'engineering_power/RIGHT10_source_joint_v3.json']
for v in ('4L','2L'):
 f=H/f'inventory/checkpoints/SPI_external_{v}_b012';n=load(f/'normalized.json');nw=load(f/'networks.json');rs=load(f/'base_net_rules.json');pol=load(P/f'gpio_policy_{v}_03.json');src=[];pending=[];left=load(own[2]);ownPlans=[load(q) for q in own]
 for q in own:src.append(dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
 for q in ownPlans:
  for ch in q.get('placementChanges',[]):
   z=next(t for t in n['placements'] if t['ref']==ch['ref']);cx,cy=z['xy'];rot=ch['rotation']-z['rotation'];dx,dy=ch['xy'][0]-cx,ch['xy'][1]-cy
   def trans(pt):
    pp=affinity.translate(affinity.rotate(Point(pt),rot,origin=[cx,cy]),dx,dy);return [pp.x,pp.y]
   for pp in z['pins']:
    pp['xy']=trans(pp['xy']);gg=affinity.translate(affinity.rotate(box(*pp['padBBox'][0],*pp['padBBox'][1]),rot,origin=[cx,cy]),dx,dy);bb=gg.bounds;pp['padBBox']=[list(bb[:2]),list(bb[2:])]
   if z.get('bodyExtent'):
    gg=affinity.translate(affinity.rotate(box(*z['bodyExtent'][0],*z['bodyExtent'][1]),rot,origin=[cx,cy]),dx,dy);bb=gg.bounds;z['bodyExtent']=[list(bb[:2]),list(bb[2:])]
   z['xy']=ch['xy'];z['rotation']=ch['rotation']
  for o in q['operations']:
   if o['type']=='deleteSegment':
    ms=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in (o['points'],list(reversed(o['points']))) and abs(r['width']-o['width'])<1e-6];assert len(ms)==1,(o,ms);n['routes'].remove(ms[0])
   elif o['type']=='deleteVia':
    ms=[r for r in n['vias'] if r['net']==o['net'] and math.dist(r['xy'],o['xy'])<1e-6];assert len(ms)==1,(o,ms);n['vias'].remove(ms[0])
   elif o['type'] in ('route','via','shape'):pending.append(o)
 names=[f'ordinary_remote_{v}_v7.json',f'aux_remote_{v}_v9.json',f'CC_entry_{v}_v4.json',f'VBUS_entry_{v}_v3.json',f'USB_aux_returns_{v}_03.json']
 for name in names:
  q=H/'plans'/name;src.append(dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
  for o in load(q)['operations']:
   if o['id'] not in left['replacePendingOperationIds'] and o.get('net')!='BOOT0':pending.append(o)
 pending.append(left['pendingReplacement'])
 # Candidate reference boundaries must follow the right10 joint rework rather than old exact outlines.
 right=ownPlans[-1];ore=right['oscillatorReference'];moat=ore['applicationGroundVoidPolygon'];island=ore['islandPolygon']
 n['planes']=[a for a in n['planes'] if not(a.get('net')=='GND' and not a.get('generated') and a['layer']=='ETCH/'+('BOTTOM' if v=='2L' else 'L2'))]
 if v=='2L':pending.append(dict(type='shape',id='FUTURE_QUIET_ISLAND',net='GND',layer='BOTTOM',polygon=island,dynamic=False))
 for o in pending:
  if o['type']=='route':
   for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o.get('width',.2)]*(len(o['points'])-1))):
    if a!=b:n['routes'].append(dict(kind='line',net=o['net'],layer='ETCH/'+o['layer'],startEnd=[a,b],width=w,generatedThermal=False,fixedManualCline=True,futureCandidate=o['id']))
  elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=o.get('padDiameterMM',.52 if '026_C052' in o['padstack'].upper() else .6),drillDiameterMM=o.get('drillDiameterMM',.26 if '026_C052' in o['padstack'].upper() else .3),futureCandidate=o['id']))
 # Network terminal coordinates use proposed poses; do not label these as native readback.
 pinxy={c['ref']+'.'+p['number']:p['xy'] for c in n['placements'] for p in c['pins'] if p['number']}
 for nn in nw['nets']:
  for cc in nn['components']:
   for t in cc['terminals']:
    if t['key'] in pinxy:t['xy']=pinxy[t['key']]
 pol['componentAnchors']=[]
 ends={'GPIO_PC13':dict(xy=[35.8,31.1],layer='BOTTOM',connectedTo='U1.2')}
 for q,field in [(ownPlans[0],'partialEndpoints'),(ownPlans[1],'longRouteAnchors'),(ownPlans[2],'partialEndpoints'),(right,'partialEndpoints')]:
  for net,ep in q.get(field,{}).items():
   if net.startswith('GPIO_'):ends[net]=ep
 selected=['GPIO_PA1','GPIO_PA2','GPIO_PA3','GPIO_PC13','GPIO_PC14','GPIO_PC15','GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']
 for net in selected:
  ep=ends[net];pol['componentAnchors'].append(dict(net=net,key=net+'_ENGINEERED_ANCHOR',xy=ep['xy'],layers=[ep['layer']],connectedTo=ep['connectedTo'],replacePinAccess=True))
 pol['allowInwardPinAccess']=[];pol['pendingOperations']=[];pol['pendingDeleteSegments']=[];pol['sourcePlans']=src
 areas=[]
 for a in pol['reservedAreas']:
  if a['id']=='HSE_ACTUAL_MOAT_AND_STEM':a=copy.deepcopy(a);a['polygon']=moat
  if a['id'].startswith('ADC_REFERENCE'):
   if v=='4L':continue
   # Original0.65 buffer was a prototype reservation, not user/manufacturing keepout.
   name=a['id'].removeprefix('ADC_REFERENCE_');route=next(x for x in load(P/'mcu_critical_routes_v6.json')['operations'] if x['id']==name)
   a=copy.deepcopy(a);a['polygon']=[list(x) for x in LineString(route['points']).buffer(.25,quad_segs=12).exterior.coords[:-1]];a['basis']='2L preserve finite .25mm bottom reference corridor about actual TOP ADC centerline. Original arbitrary .65 prototype buffer is not hardkeepout. Generated return geometry/any via-antipad interaction must be independently checked.'
  areas.append(a)
 for o in load(P/'mcu_critical_routes_v6.json')['operations']:
  if o['id'] in ('HSE_GUARD_LEFT_NORTH','HSE_GUARD_RIGHT_NORTH','HSE_GUARD_RIGHT_LOWER'):
   g=LineString(o['points']).buffer(.6,quad_segs=12);areas.append(dict(id='HSE_GUARD_SHADOW_'+o['id'],layers=['TOP','BOTTOM'],allowedNets=['GND','OSC_IN','OSC_OUT','XTAL_OUT'],polygon=[list(p) for p in g.exterior.coords[:-1]],basis='Actual .6mm TOP oscillator guard copper plus .3mm engineering margin, reject ordinary signal under guard on either layer.'))
 pol['reservedAreas']=areas;pol['noGlobalGroundViaAreas']=[moat,pol['noGlobalGroundViaAreas'][-1]];pol['futureReferenceQualification']='4L TOP ADC references L2, BOTTOM GPIO uses L3; bottom centerline crossing does not itself cut L2 but every through-via pad/antipad must be checked. 2L uses finite actual reference corridor+same-layer ground return review, not opposite coverage only.'
 # Map only explicitly declared spacing fields to candidate trace-versus-obstacle regions.
 for qp in ownPlans:
  for ex in qp.get('spacingExceptions',[]):
   pairs=ex.get('netPairs')
   if not pairs and ex.get('netsA'):pairs=[list(z) for z in itertools.product(ex['netsA'],ex['netsB'])]
   if not pairs:pairs=[list(z) for z in itertools.combinations(ex.get('nets',[]),2)]
   kinds={'line_line':'line','via_line':'via','smdpin_line':'smdpin','thrupin_line':'thrupin','line_shape':'shape'}
   for field,gap in ex.get('onlyFields',{}).items():
    if field not in kinds:continue
    for layer in ex.get('layers',[ex.get('layer','TOP')]):
     pol.setdefault('regionOverrides',[]).append(dict(id=ex['id']+'_'+field+'_'+layer,layer=layer,polygon=ex['polygon'],netPairs=pairs,kinds=[kinds[field]],gap=gap,basis='Exact declared source finite spacing field only; outside native parent retained.'))
 n['status']='DERIVED_PLANNING_SCENE_NOT_NATIVE_READBACK';n['candidateInputs']=src;nw['status']='DERIVED_PLANNING_TERMINAL_POSES_NOT_NATIVE_REOPEN';pol['sourceExpectedSHA256']=nw.get('sourceSHA256',nw.get('sha256'))
 for nm,data in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]:
  (P/f'GPIO_future_{v}_07_{nm}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 (P/f'GPIO_future_{v}_07_metadata.json').write_text(json.dumps(dict(status='DERIVED_CANDIDATE_SCENE',nativeBaseline=str(f),nativeSnapshotSHA256=hashlib.sha256((f/'normalized.json').read_bytes()).hexdigest(),plans=src,selectedNets=selected,anchors=pol['componentAnchors'],scope='All planned copper explicit future obstacles. No search or file change is a native PCB modification or validation.'),indent=2),encoding='utf8')
 print(v,'future',len(n['routes']),'routes',len(n['vias']),'vias','13anchors')
s=(P/'plan_gpio_paths_local.py').read_text(encoding='utf8')
s=s.replace("scene=CopperScene(snapshot,networks,load(args.rules),policy)","scene=CopperScene(snapshot,networks,load(args.rules),policy)\n# Native pads remain original. Only explicitly derived future via copper uses its declared diameter.\nfor o in scene.obstacles:\n if o['kind']=='via' and o['source']=='native_via':\n  cc=o['geometry'].centroid\n  vv=next((v for v in snapshot['vias'] if math.dist(v['xy'],[cc.x,cc.y])<1e-5),None)\n  if vv and vv.get('padDiameterMM'):o['geometry']=Point(vv['xy']).buffer(vv['padDiameterMM']/2,quad_segs=16)")
(P/'plan_gpio_future_local_07.py').write_text(s,encoding='utf8')
