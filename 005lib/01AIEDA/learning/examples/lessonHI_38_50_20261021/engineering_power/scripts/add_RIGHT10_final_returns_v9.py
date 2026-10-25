from pathlib import Path
import json,copy,math,sys
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'scripts'));from routing_geometry import CopperScene,Point,Polygon,LAYERS
sys.path.insert(0,str(R/'scripts'));from cadence_poly import conservative_plane
v=sys.argv[1] if len(sys.argv)>1 else '2L';p=json.loads((R/f'RIGHT10_FULL_{v}_v8.json').read_text());pol=json.loads((R/f'RIGHT10_full_policy_{v}_v8.json').read_text());b=json.loads((R/f'source/RIGHT10_long_{v}_b014_virtual.json').read_text());nw=json.loads((H/f'inventory/checkpoints/USB_aux_{v}_b014/networks.json').read_text());rules=json.loads((H/f'inventory/checkpoints/USB_aux_{v}_b014/base_net_rules.json').read_text())
for d in pol['pendingDeleteVias']:
 hits=[a for a in b['vias'] if a['net']==d['net'] and a['xy']==d['xy'] and a['padstack']==d['padstack']];assert len(hits)==1;b['vias'].remove(hits[0])
for d in pol['pendingDeleteSegments']:
 hits=[a for a in b['routes'] if a['net']==d['net'] and a['layer']=='ETCH/'+d['layer'] and abs(a['width']-d['width'])<1e-5 and a['startEnd'] in [d['points'],d['points'][::-1]]];assert len(hits)==1;b['routes'].remove(hits[0])
for c in pol['pendingPlacementChanges']:
 a=next(a for a in b['placements'] if a['ref']==c['ref']);assert a['rotation']==c['rotation'];dx=c['xy'][0]-a['xy'][0];dy=c['xy'][1]-a['xy'][1];a['xy']=c['xy'];a['bodyExtent']=[[x+dx,y+dy] for x,y in a['bodyExtent']]
 for pin in a['pins']:pin['xy']=[pin['xy'][0]+dx,pin['xy'][1]+dy];pin['padBBox']=[[x+dx,y+dy] for x,y in pin['padBBox']]
scene=CopperScene(b,nw,rules,pol)
for o in pol['pendingOperations']:scene.add_operation(o)
quiet=[Polygon(a).buffer(.301) for a in pol['noGlobalGroundViaAreas']]
def app(xy):return not any(q.intersects(Point(xy)) for q in quiet)
common=[]
for a in b['vias']:
 if a['net']=='GND' and app(a['xy']):common.append(dict(xy=a['xy'],source='BASE_COMMON_GND'))
for a in scene.pins.values():
 if a['net']=='GND' and a['through'] and app(a['xy']):common.append(dict(xy=a['xy'],source=a['key']))
for o in pol['pendingOperations']:
 if o['type']=='via' and o['net']=='GND' and app(o['xy']):common.append(dict(xy=o['xy'],source=o['id']))
# New candidates only in an existing actual common reference area, .31mm conservative inward margin.
actual=json.loads((H/f'inventory/checkpoints/USB_aux_{v}_b014/normalized.json').read_text());planes=[a for a in actual['planes'] if a['layer'] in (['ETCH/BOTTOM'] if v=='2L' else ['ETCH/L2','ETCH/L3']) and a.get('generated') and a.get('area',0)>4000]
valid=None
for a in planes:
 g=conservative_plane(dict(a,holes=a.get('holes') or [])).buffer(-.31);valid=g if valid is None else valid.intersection(g)
assert valid is not None
masks=[scene.forbidden('GND',l,.6,via=True,gridMargin=.002) for l in LAYERS];allvias=[a['xy'] for a in b['vias']]+[o['xy'] for o in pol['pendingOperations'] if o['type']=='via'];adds=[];reviews=[]
for o in p['operations']:
 if o['type']!='via' or o['net']=='GND':continue
 xy=o['xy'];nearest=min(common,key=lambda a:math.dist(a['xy'],xy));d=math.dist(xy,nearest['xy']);candidates=[]
 if d>1.5:
  for radius in [.9,1.0,1.1,1.2,1.3,1.4,1.48]:
   for angle in range(0,360,10):
    t=math.radians(angle);pt=[round(xy[0]+radius*math.cos(t),3),round(xy[1]+radius*math.sin(t),3)];q=Point(pt)
    if not app(pt) or not valid.covers(q):continue
    if min(math.dist(pt,z) for z in allvias)<.602:continue
    if any(bad.intersects(q) or not area.covers(q) for bad,area in masks):continue
    candidates.append((radius+min(math.dist(pt,z['xy']) for z in common)*.03,pt))
  if candidates:
   _,pt=min(candidates);add=dict(type='via',id='RIGHT_RETURN_'+o['id'],net='GND',xy=pt,padstack='L28_VIA030_C060',purpose='Complete-path screened common APP-GND stitch; actual regenerated-plane/graph proof mandatory, no quiet-island join.');adds.append(add);common.append(dict(xy=pt,source=add['id']));allvias.append(pt);nearest=common[-1];d=math.dist(xy,pt)
 reviews.append(dict(signalVia=o['id'],net=o['net'],xy=xy,returnSource=nearest['source'],groundXY=nearest['xy'],distanceMM=d,withinGeneral1_5Target=d<=1.5,engineeringCondition=('Dense source transition; signal GPIO static/lowrate<=1MHz with lowest adequate slew, SWO disabled initially, I2C100kHz open-drain. No unconditional fast-bus qualification. Direct actualcommonGND path and finite layer-reference change reviewed in native.' if d>1.5 else 'Distance geometry screen only. Actualreference and commonGND connection required.')))
p['batchId']=f'RIGHT10_FULL_{v}_v9';p['status']='FROZEN_COMPLETE_PATH_CANDIDATE_REQUIRES_NATIVE';p['operations']+=adds;p['returnReview']=reviews;p['returnProofs']=[dict(net='GND',sourceXY=o['xy'],sourceId=o['id'],target='U1.23') for o in adds];p['returnLimitations']=['1.5mm is a review target, not fabrication rule; source-bank exceptions quantified individually. No groundvia wall inserted after proving full10 reachable.','2L opposite reference depends on final actualTOP commonGND pour with exactnewquiet/guards void. LongBOTTOM GPIO crossings of TOPpower rows produce local slots; actual ground connectivity/width remains finalreview.','4L actualL2/L3 commonGND intended reference; newvia antipads and HSEstem cutout must be natively re-filled/read back.'];p['frozenPlanInputs']=[dict(path=str(R/f'RIGHT10_FULL_{v}_v8.json'),sha256=__import__('hashlib').sha256((R/f'RIGHT10_FULL_{v}_v8.json').read_bytes()).hexdigest())]
(R/f'RIGHT10_FULL_{v}_v9.json').write_text(json.dumps(p,indent=2),encoding='utf-8');out=dict(status='SCREENED_RETURN_CANDIDATE_NOT_NATIVE',variant=v,newGroundCount=len(adds),signalViaCount=len(reviews),reviews=reviews,sourceExceptions=[a for a in reviews if not a['withinGeneral1_5Target']],operations=adds)
(R/f'readouts/RIGHT10_FULL_{v}_v9_return_plan.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))