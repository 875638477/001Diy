import pathlib,json,sys,math,hashlib,copy,itertools
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
from shapely import affinity
left=load(P/'GPIO_left_joint_fanout_07.json');left.pop('physicalGroundViaApproval',None);(P/'GPIO_left_joint_fanout_07.json').write_text(json.dumps(left,indent=2),encoding='utf8')
nss=load(P/'NSS_pullup_local_relayout_03.json');north=load(P/'GPIO_north_joint_fanout_02.json');south=load(H/'plans/GPIO_south_joint_root_v8.json');pb15=load(P/'GPIO_PB15_bottom_exit_delta_01.json');south=copy.deepcopy(south);south['operations']=[o for o in south['operations'] if o['id'] not in pb15['replacePendingOperationIds']]+pb15['operations'];south['longRouteAnchors'].update(pb15['longRouteAnchors']);south['spacingExceptions']=[x for x in south['spacingExceptions'] if x['id'] not in pb15['removePendingSpacingExceptionIds']]+pb15['spacingExceptions'];south['physicalExceptions']+=pb15['physicalExceptions']
for v in ['4L','2L']:
 base=H/f'inventory/checkpoints/USB_aux_{v}_b014';n=load(base/'normalized.json');nw=load(base/'networks.json');rs=load(base/'base_net_rules.json');pol=load(P/f'GPIO_future_{v}_10_policy.json');right=load(H/f'engineering_power/RIGHT10_FULL_{v}_v10.json')
 allops=[];chgs=[];src=[]
 for path,q in [(H/'plans/GPIO_south_joint_root_v8.json',south),(P/'GPIO_left_joint_fanout_07.json',left),(P/'GPIO_north_joint_fanout_02.json',north),(H/f'engineering_power/RIGHT10_FULL_{v}_v10.json',right),(P/'NSS_pullup_local_relayout_03.json',nss)]:
  src.append(dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest()));chgs+=q.get('placementChanges',[])
  allops += [o for o in q['operations'] if o['id'] not in nss['supersedesOperations']]
  allops += q.get('variantOperations',{}).get(v,[])
 chgs=[z for z in chgs if z['ref']!='R16']+[dict(ref='R16',xy=[45.5,19.9],rotation=0,purpose='Root unique placement override 2026-10-22')]
 for ch in chgs:
  z=next(c for c in n['placements'] if c['ref']==ch['ref']);cx,cy=z['xy'];rot=ch['rotation']-z['rotation'];dx,dy=ch['xy'][0]-cx,ch['xy'][1]-cy
  def tr(p):pp=affinity.translate(affinity.rotate(Point(p),rot,origin=[cx,cy]),dx,dy);return [pp.x,pp.y]
  for pin in z['pins']:
   pin['xy']=tr(pin['xy']);g=affinity.translate(affinity.rotate(box(*pin['padBBox'][0],*pin['padBBox'][1]),rot,origin=[cx,cy]),dx,dy);b=g.bounds;pin['padBBox']=[list(b[:2]),list(b[2:])]
  g=affinity.translate(affinity.rotate(box(*z['bodyExtent'][0],*z['bodyExtent'][1]),rot,origin=[cx,cy]),dx,dy);b=g.bounds;z['bodyExtent']=[list(b[:2]),list(b[2:])];z['xy']=ch['xy'];z['rotation']=ch['rotation']
 deletes=[];pending=[]
 for o in allops:
  if o['type']=='deleteSegment':
   ms=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and abs(r['width']-o['width'])<1e-6 and r['startEnd'] in (o['points'],list(reversed(o['points'])))];assert len(ms)==1,(v,o,len(ms));n['routes'].remove(ms[0]);deletes.append(o['id'])
  elif o['type']=='deleteVia':
   ms=[z for z in n['vias'] if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-6];assert len(ms)==1,(v,o,len(ms));n['vias'].remove(ms[0]);deletes.append(o['id'])
  elif o['type'] in ['route','via','shape']:pending.append(o)
 # Root still-pending remote subsets only; I2C and BOOT0 wholly included in current right10 full.
 rootPlan=H/f'plans/ordinary_remote_{v}_v9.json';src.append(dict(path=str(rootPlan),sha256=hashlib.sha256(rootPlan.read_bytes()).hexdigest()))
 for o in load(rootPlan)['operations']:
  if o['net'] not in ['BOOT_SERVICE','CAN_TXD','BOOT1']:continue
  if o['id'] in left['replacePendingOperationIds']:continue
  pending.append(o)
 pending.append(left['pendingReplacement'])
 servicePath=H/f'plans/root_south_services_{v}_v15.json';service=load(servicePath);pending+=service['operations'];src.append(dict(path=str(servicePath),sha256=hashlib.sha256(servicePath.read_bytes()).hexdigest()));src.append(dict(path=str(P/'GPIO_PB15_bottom_exit_delta_01.json'),sha256=hashlib.sha256((P/'GPIO_PB15_bottom_exit_delta_01.json').read_bytes()).hexdigest()))
 ore=right['oscillatorReference'];moat=ore['applicationGroundVoidPolygon'];island=ore['islandPolygon']
 n['planes']=[z for z in n['planes'] if not(z.get('net')=='GND' and not z.get('generated') and z['layer']=='ETCH/'+('BOTTOM' if v=='2L' else 'L2'))]
 if v=='2L':n['planes'].append(dict(net='GND',layer='ETCH/BOTTOM',filled=True,generated=False,vertices=[[p,0] for p in island],holes=[],futureCandidate='NEW_QUIET_ISLAND'))
 for o in pending:
  if o['type']=='route':
   for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o.get('width',.2)]*(len(o['points'])-1))):
    if a!=b:n['routes'].append(dict(kind='line',net=o['net'],layer='ETCH/'+o['layer'],startEnd=[a,b],width=w,generatedThermal=False,fixedManualCline=True,futureCandidate=o['id']))
  elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=o.get('padDiameterMM',.52 if '026_C052' in o['padstack'].upper() else .6),drillDiameterMM=o.get('drillDiameterMM',.26 if '026_C052' in o['padstack'].upper() else .3),futureCandidate=o['id']))
 pinxy={c['ref']+'.'+p['number']:p['xy'] for c in n['placements'] for p in c['pins'] if p['number']}
 for nn in nw['nets']:
  for cc in nn['components']:
   for t in cc['terminals']:
    if t['key'] in pinxy:t['xy']=pinxy[t['key']]
 # Explicit source anchors updated; signal routes remain future candidate, not native proofs.
 ends={'GPIO_PC13':dict(xy=[35.8,31.1],layer='BOTTOM',connectedTo='U1.2')}
 for qp,field in [(north,'partialEndpoints'),(south,'longRouteAnchors'),(left,'partialEndpoints'),(right,'partialEndpoints')]:
  for net,ep in qp.get(field,{}).items():
   if net.startswith('GPIO_'):ends[net]=ep
 selected=['GPIO_PA1','GPIO_PA2','GPIO_PA3','GPIO_PC13','GPIO_PC14','GPIO_PC15','GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15'];pol['componentAnchors']=[dict(net=net,key=net+'_ENGINEERED_ANCHOR',xy=ends[net]['xy'],layers=[ends[net]['layer']],connectedTo=ends[net]['connectedTo'],replacePinAccess=True) for net in selected]
 pol['reservedAreas']=[a for a in pol['reservedAreas'] if not a['id'].startswith('ADC_REFERENCE') and a['id']!='NO_SPI_BOTTOM_IN_PREFILTER_TOP_REFERENCE_VOID']
 for a in pol['reservedAreas']:
  if a['id']=='HSE_ACTUAL_MOAT_AND_STEM':a['polygon']=moat
 pol['noGlobalGroundViaAreas']=[moat];pol['regionOverrides']=[z for z in pol.get('regionOverrides',[]) if not z.get('id','').startswith('HI_LEFT')]
 for qp in [south,left,north]:
  for ex in qp.get('spacingExceptions',[]):
   pairs=ex.get('netPairs')
   if not pairs and ex.get('netsA'):pairs=[list(z) for z in itertools.product(ex['netsA'],ex['netsB'])]
   if not pairs:pairs=[list(z) for z in itertools.combinations(ex.get('nets',[]),2)]
   for field,gap in ex.get('onlyFields',{}).items():
    kd={'line_line':'line','via_line':'via','smdpin_line':'smdpin','thrupin_line':'thrupin','line_shape':'shape'}.get(field)
    if kd:
     for l in ex.get('layers',[ex.get('layer','TOP')]):pol['regionOverrides'].append(dict(id=ex['id']+'_'+field+'_'+l,layer=l,polygon=ex['polygon'],netPairs=pairs,kinds=[kd],gap=gap))
 pol['routeWindows']=[z for z in pol.get('routeWindows',[]) if not any(nn.startswith('GPIO_') for nn in z['nets'])]+[dict(nets=selected,layers=['TOP','BOTTOM'],polygon=[[12,18],[70,18],[70,57],[12,57]],basis='Reject artificial USB/board-perimeter detours. Full source relayout must permit ordinary GPIO inside practical MCU-to-header region.')];pol['pendingOperations']=[];pol['pendingDeleteSegments']=[];pol['allowInwardPinAccess']=[];pol['sourcePlans']=src;pol['sourceExpectedSHA256']=nw.get('sourceSHA256',nw.get('sha256'))
 n['status']='DERIVED_FUTURE_GEOMETRY_NOT_NATIVE_REOPEN';n['candidateInputs']=src
 # Independent min-copper screen: mandatory floor .1524 (OSH) plus overlaps, exact rules evaluated in native later.
 scene=CopperScene(n,nw,rs,pol)
 for o in scene.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   c=o['geometry'].centroid;z=next(z for z in n['vias'] if math.dist(z['xy'],[c.x,c.y])<1e-6)
   if z.get('padDiameterMM'):o['geometry']=Point(z['xy']).buffer(z['padDiameterMM']/2,quad_segs=32)
 fresh=[]
 for o in pending:
  if o['type']=='via':
   for l in LAYERS:fresh.append(dict(net=o['net'],layer=l,kind='via',geometry=Point(o['xy']).buffer(o.get('padDiameterMM',.6)/2,quad_segs=32),source=o['id']))
  elif o['type']=='route':
   for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o.get('width',.2)]*(len(o['points'])-1))):
    if a!=b:fresh.append(dict(net=o['net'],layer=o['layer'],kind='line',geometry=LineString([a,b]).buffer(w/2,quad_segs=32),source=o['id']))
 issues=[];comparisons=0
 for a in fresh:
  for b in scene.obstacles:
   if a['net']==b['net'] or a['layer']!=b['layer']:continue
   comparisons+=1;d=a['geometry'].distance(b['geometry'])
   if d<.15235:issues.append(dict(new=a['source'],net=a['net'],other=b['source'],otherNet=b['net'],layer=a['layer'],distanceMM=d,overlap=a['geometry'].intersects(b['geometry']),otherBBox=list(b['geometry'].bounds)))
 newRefs={c['ref'] for c in chgs};clashes=[]
 for i,a in enumerate(n['placements']):
  for b in n['placements'][:i]:
   if a['ref'] not in newRefs and b['ref'] not in newRefs:continue
   ga=box(*a['bodyExtent'][0],*a['bodyExtent'][1]);gb=box(*b['bodyExtent'][0],*b['bodyExtent'][1])
   if ga.intersection(gb).area>1e-7:clashes.append(dict(a=a['ref'],b=b['ref'],overlapArea=ga.intersection(gb).area))
 for typ,data in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_future_{v}_16_{typ}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 report=dict(status='CANDIDATE_PRECHECK',baseNative=str(base),baseSnapshotSHA256=hashlib.sha256((base/'normalized.json').read_bytes()).hexdigest(),candidateSourcePlans=src,uniqueDeletes=deletes,comparisons=comparisons,mandatoryMinimumCopperFloorMM=.1524,issues=issues,placeBoundOverlaps=clashes,scope='Candidate source, R25 local relayout and right10 full copper combined. Native rules/graph/source-return/HSE single-anchor proof not yet executed. Generated GND/thermal recreated at native fill, not simulated here.')
 (P/f'GPIO_future_{v}_16_precheck.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 print(v,'comparisons',comparisons,'issues',len(issues),'PlaceBoundclashes',clashes)
 for e in issues[:15]:print(e)

