import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;sys.path.insert(0,str(H/'scripts'))
from routing_geometry import *
f=H/'inventory/checkpoints/postcritical_2L_b010';n=load(f/'normalized.json');p=load(H/'engineering_power/SPI_external_2L_engineered_v9.json');deleted=[]
for o in p['operations']:
 if o['type']!='deleteSegment':continue
 m=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and abs(r['width']-o['width'])<1e-7 and r['startEnd'] in (o['points'],list(reversed(o['points'])))];assert len(m)==1,(o,len(m));deleted.append(o['id']);n['routes'].remove(m[0])
s=CopperScene(n,load(f/'networks.json'),load(f/'base_net_rules.json'),{})
new=[];issues=[];drill=[];checks=0
for o in p['operations']:
 if o['type']=='deleteSegment':continue
 if o['type']=='via':
  for l in LAYERS:new.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(.3,quad_segs=64),kind='via',source=o['id']))
  d=Point(o['xy']).buffer(.15,quad_segs=64)
  for k,pin in s.pins.items():
   if pin['through']:continue
   if d.intersects(pin['geom']):drill.append(dict(via=o['id'],pad=k,net=pin['net']))
 elif o['type']=='route':
  for a,b in zip(o['points'],o['points'][1:]):new.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(o['width']/2,quad_segs=64),kind='line',source=o['id']))
for i,a in enumerate(new):
 for b in s.obstacles+new[:i]:
  if a['layer']!=b['layer'] or a['net']==b['net']:continue
  checks+=1;d=a['geometry'].distance(b['geometry'])
  if d<.19995:issues.append(dict(a=a['source'],b=b['source'],nets=[a['net'],b['net']],layer=a['layer'],distance=d,overlap=a['geometry'].intersects(b['geometry'])))
quiet=Polygon(load(R/'plans/mcu_critical_routes_v6.json')['oscillatorReference']['applicationGroundVoidPolygon'])
nearQuiet=min((a['geometry'].distance(quiet),a['source']) for a in new)
allgnd=[z['xy'] for z in n['vias'] if z['net']=='GND']+[o['xy'] for o in p['operations'] if o['type']=='via' and o['net']=='GND'];rv=[]
for o in p['operations']:
 if o['type']=='via' and o['net']!='GND':
  d,xy=min((math.dist(o['xy'],xy),xy) for xy in allgnd);rv.append(dict(signalVia=o['id'],xy=o['xy'],nearestCommonGroundVia=xy,distanceMM=d,targetAtMost1Point5=d<=1.5))
existingGuardAnchor=any(z['net']=='GND' and math.dist(z['xy'],[28.6,29])<1e-8 for z in n['vias'])
report=dict(status='INDEPENDENT_CANDIDATE_GEOMETRY_SCREEN_NOT_NATIVE_APPROVAL',sourceCheckpoint=str(f),sourceSnapshotSHA256=hashlib.sha256((f/'normalized.json').read_bytes()).hexdigest(),sourcePlan=str(H/'engineering_power/SPI_external_2L_engineered_v9.json'),sourcePlanSHA256=hashlib.sha256((H/'engineering_power/SPI_external_2L_engineered_v9.json').read_bytes()).hexdigest(),deletedUniqueSegments=deleted,otherNetComparisons=checks,belowPoint20Issues=issues,drillInSMDPadIntersections=drill,minimumCandidateCopperToHSEMoat=nearQuiet,guardClockMOSIExplicitlyJoinsRetainedCommonGNDvia28Point6_29=existingGuardAnchor,signalReturnViaDistances=rv,referenceObservations=['NSS BOTTOM y32.3 is below shifted TOP V3V3 copper row y32.55; it is not a continuous opposite GND microstrip. Grounded BOTTOM guard y31.55 and GND via29,33.2 /20.8,33.75 provide proposed same-layer/transition return options, to be checked in actual post-fill native geometry.','The two guards are conductors tied to explicit common-GND vias; same-net names alone are insufficient. First guard starts on inherited via28.6,29 and second directly connects two new GND vias.','TOP power-row shift is +0.20mm; ADC_INPUT TOP y34 remains separate, no direct HSE/main moat intersection.','All eight signal-transition nearest proposed/inherited common-GND via center distances <=1.5mm. This is a geometric policy target, not evidence of HF return path or EMI pass.','Native DRC, TCF, branch-terminal orphan audit, HSE unique-anchor negative test, actual generated GND polygon and reference/return inspection remain required.','Concurrent ordinary GPIO candidates are not frozen; root must merge all candidate copper before native execution.'])
(R/'plans/SPI9_independent_review_01.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps({k:report[k] for k in ('otherNetComparisons','belowPoint20Issues','drillInSMDPadIntersections','minimumCandidateCopperToHSEMoat','guardClockMOSIExplicitlyJoinsRetainedCommonGNDvia28Point6_29','signalReturnViaDistances')},indent=2))
