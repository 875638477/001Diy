import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['4L','2L']:
 src=H/f'engineering_power/RIGHT10_FULL_{v}_v11.json';q=load(src);n=load(P/f'GPIO_future_{v}_17_snapshot.json');ore=q['oscillatorReference'];island=Polygon(ore['islandPolygon']);void=Polygon(ore['applicationGroundVoidPolygon']);anchor=[46.35,29.4]
 viaAudit=[]
 for z in n['vias']:
  r=z.get('padDiameterMM',.6)/2;g=Point(z['xy']).buffer(r,quad_segs=64);intr=g.intersection(island)
  if not intr.is_empty:viaAudit.append(dict(net=z['net'],xy=z['xy'],padstack=z['padstack'],intersectionAreaMM2=intr.area,isUniqueAnchor=math.dist(z['xy'],anchor)<1e-6,isQuietCap=z.get('futureCandidate','') in ['HSE_LOCAL_C22','HSE_LOCAL_C23'] or z['net']=='GND' and (z['xy'][1]>32 and island.covers(Point(z['xy']))),allRegularCuWithinApplicationVoid=void.covers(g),source=z.get('futureCandidate','nativeInherited')))
 powerProjection=[];ordinaryIntr=[]
 for z in n['routes']:
  if z.get('generatedThermal') or z['layer'] not in ['ETCH/TOP','ETCH/BOTTOM']:continue
  g=LineString(z['startEnd']).buffer(z['width']/2,quad_segs=32);intr=g.intersection(island)
  if not intr.is_empty and intr.area>1e-9:
   if z['net']=='V3V3':powerProjection.append(dict(net=z['net'],layer=z['layer'],xy=z['startEnd'],width=z['width'],islandProjectionAreaMM2=intr.area,source=z.get('futureCandidate','nativeInherited')))
   elif z['net'] not in ['GND','OSC_IN','OSC_OUT','XTAL_OUT']:ordinaryIntr.append(dict(net=z['net'],layer=z['layer'],xy=z['startEnd'],area=intr.area,source=z.get('futureCandidate','nativeInherited')))
 # Independent hypothetical electrical graph: actual TOP copper + all through-GND vias + one local island node.
 # Application plane is a separate external node, connected only to via centers outside specified appvoid.
 gs=[]
 for c in n['placements']:
  for pp in c['pins']:
   if pp['net']=='GND':gs.append(dict(id=c['ref']+'.'+pp['number'],kind='pad',geom=box(*pp['padBBox'][0],*pp['padBBox'][1])))
 for z in n['routes']:
  if z['net']=='GND' and z['layer']=='ETCH/TOP' and not z.get('generatedThermal'):gs.append(dict(id=z.get('futureCandidate','nativeTOPGND'),kind='topline',geom=LineString(z['startEnd']).buffer(z['width']/2,quad_segs=32)))
 for z in n['vias']:
  if z['net']=='GND':gs.append(dict(id='via'+str(z['xy']),kind='via',xy=z['xy'],geom=Point(z['xy']).buffer(z.get('padDiameterMM',.6)/2,quad_segs=32)))
 def analyze(removeAnchor):
  zz=[a for a in gs if not(removeAnchor and a['kind']=='via' and math.dist(a['xy'],anchor)<1e-6)];parent=list(range(len(zz)+2));local=len(zz);app=local+1
  def find(i):
   while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
   return i
  def join(a,b):parent[find(a)]=find(b)
  for i,a in enumerate(zz):
   for j,b in enumerate(zz[:i]):
    if a['geom'].distance(b['geom'])<1e-6:join(i,j)
   if a['kind']=='via':
    if a['geom'].intersection(island).area>1e-9:join(i,local)
    if not void.intersects(a['geom']):join(i,app)
  # VSS47 and both GND metal-case pads use actual transformed pad boxes.
  entries={key:next(i for i,a in enumerate(zz) if a['id']==key) for key in ['U1.47','Y1.2','Y1.4','C22.2','C23.2']}
  return dict(localReachesApplication=find(local)==find(app),terminalLocal={key:find(i)==find(local) for key,i in entries.items()},terminalApplication={key:find(i)==find(app) for key,i in entries.items()},qualification='Geometry candidate graph with app-connected via qualification, not native filled plane/physical connect proof.')
 positive=analyze(False);negative=analyze(True)
 report=dict(status='INDEPENDENT_HYPOTHETICAL_REFERENCE_TOPOLOGY_REVIEW_NOT_NATIVE',variant=v,source=str(src),sourceSHA256=hashlib.sha256(src.read_bytes()).hexdigest(),islandValid=island.is_valid,voidValid=void.is_valid,islandArea=island.area,voidArea=void.area,islandCoveredByVoid=void.covers(island),localThroughViaRegularCopperAudit=viaAudit,powerStemProjection=powerProjection,nonOscillatorDigitalOrAnalogIslandProjection=ordinaryIntr,positiveHypotheticalGraph=positive,anchorRemovedHypotheticalGraph=negative,scope='Uses exact candidate pad/trace/via geometry. L2/BOTTOM actual appfill void, every through-via all-layer pad/antipad and actual native negative/restore challenge remain mandatory. Does not assert computed current path or AN2867 full hardware implementation.')
 (P/f'RIGHT11_independent_reference_{v}_01.json').write_text(json.dumps(report,indent=2),encoding='utf8')
 print(v,'viaAudits',viaAudit,'ordinaryShadow',ordinaryIntr,'positive',positive,'negative',negative)
