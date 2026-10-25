from pathlib import Path
import json,copy,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';right=json.loads((R/'RIGHT10_source_joint_v1.json').read_text());m={a['net']:a for a in right['anchors']}
for v in ['2L','4L']:
 pol=json.loads((H/f'plans/ordinary_policy_{v}_v10.json').read_text());spi=json.loads((R/(f'SPI_external_{v}_engineered_v'+('10.json' if v=='2L' else '6.json'))).read_text());spiids={x['id'] for x in spi['operations']}
 pol['pendingOperations']=[x for x in pol['pendingOperations'] if x['id'] not in spiids];pol['pendingDeleteSegments']=[x for x in pol['pendingDeleteSegments'] if x['id'] not in spiids]
 pol['pendingPlacementChanges']+=right['placementChanges'];pol.setdefault('pendingDeleteVias',[]).extend(x for x in right['operations'] if x['type']=='deleteVia');pol['pendingDeleteSegments'] +=[x for x in right['operations'] if x['type']=='deleteSegment'];pol['pendingOperations'] +=[x for x in right['operations'] if x['type'] not in ['deleteVia','deleteSegment']]
 for a in pol['reservedAreas']:
  if a['id']=='HSE_QUIET_SHADOW':a['polygon']=right['oscillatorReference']['applicationGroundVoidPolygon']
 pol['reservedAreas'] += [a for a in right['reservedAreas'] if a['id']=='HSE_QUIET_SHADOW' and not any(z['id']=='HSE_QUIET_SHADOW' for z in pol['reservedAreas'])]
 pol['pendingOperations'].append(dict(type='shape',id='RIGHT_QUIET_VIRTUAL',net='GND',layer='BOTTOM' if v=='2L' else 'L2',polygon=right['oscillatorReference']['islandPolygon'],dynamic=False))
 for a in right['anchors']:pol['componentAnchors'].append(dict(key='ANCHOR_'+a['net'],net=a['net'],xy=a['anchor'],layers=['BOTTOM'],connectedTo='U1.'+str(a['pin']),replacePinAccess=True))
 pol['routeWindows']=[z for z in pol.get('routeWindows',[]) if not(set(z['nets'])&set(m))];pol['routeWindows'].append(dict(nets=list(m),layers=['TOP','BOTTOM'],polygon=[[46.15,15],[79,15],[79,58.4],[46.15,58.4]]))
 pol['manualOnlyNets']=[n for n in pol['manualOnlyNets'] if n not in m];pol['status']='RIGHT10_LONG_EXPLICIT_PAIRS_WITH_FULL_FUTURE_OBSTACLES';pol['sourceCheckpoint']='SPI_external_'+v+'_b012';pol['sourcePlans'].append(dict(path='engineering_power/RIGHT10_source_joint_v1.json',sha256=hashlib.sha256((R/'RIGHT10_source_joint_v1.json').read_bytes()).hexdigest()))
 for l in ['TOP','BOTTOM']:pol['regionOverrides'].append(dict(id='RIGHT10_LOCAL_'+l,layer=l,polygon=right['rules'][0]['polygon'],nets=list(m),kinds=['line','smdpin','via'],gap=.16))
 (R/f'RIGHT10_long_policy_{v}_v1.json').write_text(json.dumps(pol,indent=2),encoding='utf-8')
 b=json.loads((H/f'inventory/checkpoints/SPI_external_{v}_b012/normalized.json').read_text());old=[q for q in b['planes'] if q['net']=='GND' and abs(q['area']-62.31)<.0001 and not q['generated']];assert len(old)==1;b['planes'].remove(old[0]);b['planningOnlyEdit']='Old quiet static shape removed solely from planning copy; newshape/keepout in policy. Actualnativeunchanged.';(R/f'source/RIGHT10_long_{v}_virtual_snapshot.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
base=(H/'scripts/plan_signal_paths.py').read_text();base=base.replace('from routing_geometry import',"sys.path.insert(0,r'D:\\001DIY\\005lib\\01AIEDA\\learning\\examples\\lessonHI_38_50_20261021\\scripts')\nfrom routing_geometry import")
cut=base.index('start=time.time();nets=')
tail='''start=time.time();proofs=[];operations=[];reviews=[];failures=[]
pairs={'SWCLK':[('ANCHOR_SWCLK','J9.4')],'SWO':[('ANCHOR_SWO','J9.6')],'GPIO_PA15':[('ANCHOR_GPIO_PA15','J13.4')],'GPIO_PB4':[('ANCHOR_GPIO_PB4','J13.5')],'GPIO_PB5':[('ANCHOR_GPIO_PB5','J13.6')],'GPIO_PB8':[('ANCHOR_GPIO_PB8','J13.7')],'GPIO_PB9':[('ANCHOR_GPIO_PB9','J13.8')],'I2C_SCL':[('ANCHOR_I2C_SCL','R19.2')],'I2C_SDA':[('ANCHOR_I2C_SDA','R20.2')],'BOOT0':[('ANCHOR_BOOT0','R28.1'),('R28.1','J8.2')]}
for net in selected:
 for join,(source,target) in enumerate(pairs[net]):
  try:segments,vias,expanded=astar(net,source,target,.2)
  except ValueError as e:failures.append(dict(net=net,source=source,target=target,reason=str(e)));print(json.dumps(failures[-1]),flush=True);continue
  for j,xy in enumerate(vias):
   o=dict(type='via',id='RIGHT_LONG_'+net+'_'+str(join)+'_V'+str(j),net=net,xy=xy,padstack='L28_VIA030_C060',purpose='Candidate transition; final return GND and reference proof mandatory');operations.append(o);scene.add_operation(o)
  for j,(layer,pts) in enumerate(segments):
   if len(pts)<2:continue
   o=dict(type='route',id='RIGHT_LONG_'+net+'_'+str(join)+'_R'+str(j),net=net,layer=layer,points=pts,width=.2,purpose='Explicit endpoint/corridor long route after engineered source; actual native/reference review pending');operations.append(o);scene.add_operation(o)
  proofs.append(dict(net=net,source=scene.pins[source].get('connectedTo',source),target=scene.pins[target].get('connectedTo',target)))
  reviews.append(dict(net=net,source=source,target=target,viaCount=len(vias),length_mm=sum(sum(math.dist(a,b) for a,b in zip(pts,pts[1:])) for _,pts in segments),expanded=expanded));print(json.dumps(reviews[-1]),flush=True)
out=pathlib.Path(args.out);out.write_text(json.dumps(dict(status='LONG_PATH_GEOMETRY_CANDIDATE_NEEDS_ENGINEERING_REVIEW',variant=snapshot['variant'],sourceExpectedSHA256=networks.get('sourceSHA256',networks.get('sha256')),operations=operations,proofs=proofs,reviews=reviews,failures=failures,scope='Specified right10 long endpoints only; sourcejoint and all declared future plans are obstacles. I2C remote R19/R20 toJ5 from rootv7 retained as separate knowncandidate, no duplicate automaticstar. Signal transitions need final ground. No Cadence invoked.'),indent=2),encoding='utf-8')
'''
(R/'scripts/plan_RIGHT10_long_v1.py').write_text(base[:cut]+tail,encoding='utf-8');print('ready')