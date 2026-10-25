from pathlib import Path
import json,sys,math,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'));sys.path.insert(0,str(R/'scripts'))
from shapely.geometry import Point,LineString,box
from shapely.ops import unary_union
from cadence_poly import conservative_plane
b=json.loads((H/'inventory/checkpoints/postcritical_2L_b010/normalized.json').read_text());p=json.loads((R/'SPI_external_2L_engineered_v9.json').read_text())
# exact ripup, no mutation to native or frozen source
for o in p['operations']:
 if o['type']=='deleteSegment':
  hits=[r for r in b['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in [o['points'],o['points'][::-1]] and abs(r['width']-o['width'])<1e-6];assert len(hits)==1; b['routes'].remove(hits[0])
G=unary_union([conservative_plane(dict(z,holes=z['holes'] or [])) for z in b['planes'] if z['layer']=='ETCH/BOTTOM' and z['net']=='GND'])
G=unary_union([G]+[LineString(z['startEnd']).buffer(z['width']/2) for z in b['routes'] if z['net']=='GND' and z['layer']=='ETCH/BOTTOM' and z['kind']=='line'])
ng=[o for o in p['operations'] if o.get('net')!='GND'];cuts=[]
for o in ng:
 if o['type']=='route' and o['layer']=='BOTTOM':cuts.append(LineString(o['points']).buffer(o['width']/2+.3))
 if o['type']=='via':cuts.append(Point(o['xy']).buffer(.6))
# conservative predicted cutout, not native generated copper; global line-line .3 chosen as stricter than SPI .2
pred=G.difference(unary_union(cuts));guards=[]
for o in p['operations']:
 if o['net']=='GND' and o['type']=='route':guards.append(LineString(o['points']).buffer(o['width']/2))
newGV=[o for o in p['operations'] if o['net']=='GND' and o['type']=='via'];pred=unary_union([pred]+guards+[Point(o['xy']).buffer(.3) for o in newGV])
parts=list(pred.geoms) if hasattr(pred,'geoms') else [pred]; anchor=Point(28.6,29).buffer(.3)
common=[q for q in parts if q.intersection(anchor).area>.001];assert len(common)==1;common=common[0]
viaG=[dict(id='OLD_'+str(i),xy=v['xy']) for i,v in enumerate(b['vias']) if v['net']=='GND']+[dict(id=o['id'],xy=o['xy']) for o in newGV]
trans=[]
for o in p['operations']:
 if o['type']!='via' or o['net']=='GND':continue
 v=min(viaG,key=lambda v:math.dist(v['xy'],o['xy']));trans.append(dict(id=o['id'],net=o['net'],xy=o['xy'],nearestGND=v['id'],groundXY=v['xy'],distance_mm=math.dist(v['xy'],o['xy'])))
foreignTop=[]
for z in b['routes']:
 if z['net'] and z['net']!='GND' and z['layer']=='ETCH/TOP' and z['kind']=='line':foreignTop.append(LineString(z['startEnd']).buffer(z['width']/2+.3))
for c in b['placements']:
 for z in c['pins']:
  if z['net'] not in [None,'GND'] and z['figure']!='NULL':foreignTop.append(box(*z['padBBox'][0],*z['padBBox'][1]).buffer(.3))
for o in p['operations']:
 if o['type']=='route' and o.get('layer')=='TOP' and o['net'] not in ['GND','SPI_SCK','SPI_MISO','SPI_MOSI','SPI_NSS']:foreignTop.append(LineString(o['points']).buffer(o['width']/2+.3))
foreignTop=unary_union(foreignTop)
bridges=[]
for o in p['operations']:
 if o['type']=='route' and o['layer']=='BOTTOM' and o['net']!='GND':
  l=LineString(o['points']);u=l.intersection(foreignTop);bridges.append(dict(id=o['id'],net=o['net'],length_mm=l.length,potentialTOPGroundUnavailableLength_mm=u.length,unavailableBBox=list(u.bounds) if not u.is_empty else None,note='Projected foreign TOP copper plus .3mm halo upper-bound; TOP global GND has not been poured. These are deliberate coplanar-return bridges, not certified opposite-plane routes.'))
groundCore=common.buffer(-.299)
for q in bridges:
 o=next(v for v in p['operations'] if v['id']==q['id']);l=LineString(o['points']);samples=[]
 for j in range(1,int(l.length/.1)):
  t=j*.1
  if t<.7 or t>l.length-.7:continue
  a=l.interpolate(t);samples.append((a.distance(groundCore),list(a.coords)[0]))
 q['maxDistanceToWidth0598GroundCore_mm']=max([x[0] for x in samples],default=0)
 q['worstGroundCoreSample']=max(samples,default=(0,None))[1]
 q['groundCoreProofScope']='Predicted BOTTOM common GND eroded by0.299mm. Distance is to center set of >=0.598mm ground corridor; candidate-generated native shape still unverified.'
conn=[]
for o,g in zip([o for o in p['operations'] if o['net']=='GND' and o['type']=='route'],guards):conn.append(dict(id=o['id'],explicitWidth_mm=.6,fullGuardInPredictedCommonGND=common.buffer(1e-7).covers(g)))
for v in newGV:conn.append(dict(id=v['id'],viaAnnulusInPredictedCommonGND=common.intersection(Point(v['xy']).buffer(.3)).area>.1))
out={'status':'CANDIDATE_RETURN_ENGINEERING_REVIEW_NEEDS_NATIVE_REFILL','sourceSHA256':'76ED85DA3999A7DAFBDF9EB99EEC425B480A5EAEB49843BF970F8664707DE0AF','candidateSHA256':hashlib.sha256((R/'SPI_external_2L_engineered_v9.json').read_bytes()).hexdigest(),'signalTransitions':trans,'allSignalsHaveGNDWithin1_5mm':all(v['distance_mm']<=1.5+1e-9 for v in trans),'bottomBridges':bridges,'predictedCopperConnections':conn,'guardConnectionsAllInCommon':all(all(z for k,z in v.items() if k in ['fullGuardInPredictedCommonGND','viaAnnulusInPredictedCommonGND']) for v in conn),'guardReturnIntent':['SCK: existing C9 GND via (28.6,29) feeds .6mm guard y29.25 beside local 8.95mm BOTTOM bridge. Opposite TOP has unavoidable LDO VIN/EN/VOUT gap.','MISO and NSS: .6mm guard y31.55 connected by two offpad through vias; row31.55 is between signal30.8 and32.3 with .35mm nominal edge spacing. NSS still lies below TOP low-current V3 prefilter shifted to32.55, explicitly not opposite GND.','MOSI: BOTTOM x26.6..31.15 at y28.3 then x14.8..26.4 at28.5 avoids SW land projection. Closest ground vias and global BOTTOM plane provide coplanar return; TOP V5 projection locally remains.','Predicted common-ground proof conservatively subtracts .3mm halos for all new signal BOTTOM copper and .6mm radius signal-via antipads from frozen actual BOTTOM ground. It is a planning proof, not native regeneration acceptance.'],'manufacturingLimits':['New vias are off actual SMD copper and no drill intersects SMD pad. BodyExtent/PlaceBound is not a verified MPN body; C9 nearby via requires physical component/tenting review.','L28 through-via mask aperture/tent and annular ring are existing library process conditions; no in-pad approval implied.','J6 has one GND at pin6 and external cable length/edge/return is outside board DRC.'],'requiredNativeAcceptance':['0 DRC and fresh readback source hash unchanged','new GND via annular copper and both .6mm guard corridors in same actual common ground after all other digital routes and actual plane refill','No unexpected isolated copper or slit at SPI/GPIO crossings; record local minimum GND neck instead of relying on plane area','All source resistor -> SPI output -> correct J6 pin connectivity proven; no branch bypassing series resistor','Report actual parallel/coplanar return state and leave waveform/EMI/manufacturing conditions open']}
(R/'readouts/SPI_external_2L_v9_return_plan.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({'viaDistances':trans,'guardConnections':conn,'allCommon':out['guardConnectionsAllInCommon'],'bridgeProjection':bridges},indent=2))