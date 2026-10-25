from pathlib import Path
import json,sys,math
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'))
from shapely.geometry import Point,LineString,box,Polygon
from shapely.ops import nearest_points
variant=sys.argv[1] if len(sys.argv)>1 else '2L';p=json.loads((R/f'RIGHT10_FULL_{variant}_v10.json').read_text());b=json.loads((H/f'inventory/checkpoints/USB_aux_{variant}_b014/normalized.json').read_text());items=[];proof=[]
for o in p['operations']:
 if o['type']=='deleteSegment':
  hits=[r for r in b['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in [o['points'],o['points'][::-1]] and abs(r['width']-o['width'])<1e-6 and not r['generatedThermal']];assert len(hits)==1,(o['id'],len(hits));b['routes'].remove(hits[0]);proof.append(dict(id=o['id'],unique=True))
 if o['type']=='deleteVia':
  hits=[v for v in b['vias'] if v['net']==o['net'] and v['padstack']==o['padstack'] and v['xy']==o['xy']];assert len(hits)==1,(o['id'],len(hits));b['vias'].remove(hits[0]);proof.append(dict(id=o['id'],unique=True))
poses={x['ref']:x for x in p['placementChanges']}
for c in b['placements']:
 if c['ref'] not in poses:continue
 z=poses[c['ref']];dx=z['xy'][0]-c['xy'][0];dy=z['xy'][1]-c['xy'][1];assert z['rotation']==c['rotation'];c['xy']=z['xy'];c['bodyExtent']=[[q[0]+dx,q[1]+dy] for q in c['bodyExtent']]
 for pad in c['pins']:pad['xy']=[pad['xy'][0]+dx,pad['xy'][1]+dy];pad['padBBox']=[[q[0]+dx,q[1]+dy] for q in pad['padBBox']]
def add(i,n,l,g,new=False,kind='line'):items.append(dict(id=i,net=n,layer=l,g=g,new=new,kind=kind))
for j,r in enumerate(b['routes']):
 if r['kind']=='line' and r['net'] and not r['generatedThermal']:add('BASE_R'+str(j),r['net'],r['layer'].split('/')[-1],LineString(r['startEnd']).buffer(r['width']/2,quad_segs=32))
for j,v in enumerate(b['vias']):
 for l in ['TOP','BOTTOM']:add('BASE_V'+str(j),v['net'],l,Point(v['xy']).buffer(v['drill']/2+.15,quad_segs=32),kind='via')
for c in b['placements']:
 for pad in c['pins']:
  if pad['figure']=='NULL':continue
  for l in (['TOP','BOTTOM'] if c['ref'].startswith('J') and c['ref']!='J2' else ['TOP']):add(c['ref']+'.'+pad['number'],pad['net'],l,box(*pad['padBBox'][0],*pad['padBBox'][1]),c['ref'] in poses,'pad')
for o in p['operations']:
 if o['type']=='route':
  for j,(a,z) in enumerate(zip(o['points'],o['points'][1:])):
   w=o['widths'][j] if 'widths' in o else o['width'];add(o['id']+':'+str(j),o['net'],o['layer'],LineString([a,z]).buffer(w/2,quad_segs=32),True)
 if o['type']=='via':
  rad=.26 if o['padstack']=='HI_VIA026_C052_TENT' else .3
  for l in ['TOP','BOTTOM']:add(o['id'],o['net'],l,Point(o['xy']).buffer(rad,quad_segs=32),True,'via')
right=Polygon(p['rules'][0]['polygon']);oldright=box(43.5,28.8,47,30.9);signal=set(p['rules'][0]['signalNets'])
def req(a,z):
 ns={a['net'],z['net']};pa,pz=nearest_points(a['g'],z['g']);local=right.covers(pa) and right.covers(pz)
 if ns&{'BUCK_SW','BUCK_BOOT'}:return .5
 if local and ns<=signal:return .16
 if ns&{'GND','V3V3','V5','VDDA'}:
  if oldright.covers(pa) and oldright.covers(pz):return .2
  if local and ns&{'GND'} and ns&signal:return .2
  return .16 if a['kind']=='pad' or z['kind']=='pad' else .2 if a['kind']=='via' and z['kind']=='via' else .3
 if ns&{'ADC_IN','ADC0','BUCK_FB'}:return .3
 return .16 if 'pad' in {a['kind'],z['kind']} else .2
issues=[];tests=0
for i,a in enumerate(items):
 for z in items[i+1:]:
  if not(a['new'] or z['new']) or a['net']==z['net'] or a['layer']!=z['layer']:continue
  tests+=1;d=a['g'].distance(z['g']);mn=req(a,z)
  if d<mn-1e-5:issues.append(dict(a=a['id'],b=z['id'],netA=a['net'],netB=z['net'],layer=a['layer'],gap=round(d,6),overlap=round(a['g'].intersection(z['g']).area,6),required=mn))
# no drill inside any actual SMD pad, independent of copper same-net
for o in p['operations']:
 if o['type']!='via':continue
 drill=.13 if o['padstack']=='HI_VIA026_C052_TENT' else .15
 for c in b['placements']:
  if c['ref'].startswith('J'):continue
  for z in c['pins']:
   if z['figure']=='NULL':continue
   d=Point(o['xy']).distance(box(*z['padBBox'][0],*z['padBBox'][1]))
   if d<drill-1e-6:issues.append(dict(kind='DRILL_IN_SMD_PAD',via=o['id'],pad=c['ref']+'.'+z['number'],distance=d))
newshadow=Polygon(p['oscillatorReferenceRework']['applicationGroundVoidPolygon']);viol=[]
for o in p['operations']:
 if o['type']=='route' and o['net'] not in ['GND','V3V3']:
  for a,z in zip(o['points'],o['points'][1:]):
   if LineString([a,z]).buffer((o.get('width') or min(o['widths']))/2).intersects(newshadow):viol.append(o['id'])
 if o['type']=='via' and o['net'] not in ['GND']:
  if Point(o['xy']).buffer(.26 if 'C052' in o['padstack'] else .3).intersects(newshadow):viol.append(o['id'])
placement=[]
for c in b['placements']:
 if c['ref'] not in poses:continue
 for z in b['placements']:
  if z['ref']==c['ref'] or not z.get('bodyExtent'):continue
  a=box(*c['bodyExtent'][0],*c['bodyExtent'][1]);g=box(*z['bodyExtent'][0],*z['bodyExtent'][1]);area=a.intersection(g).area
  if area>1e-7:placement.append(dict(a=c['ref'],b=z['ref'],area=area))
out={'status':'PRECHECK_PASS_NOT_NATIVE' if not(issues or viol or placement) else 'REVISE_FULL_GROUP','variant':variant,'tests':tests,'issueCount':len(issues),'issues':issues,'shadowViolations':viol,'placementOverlaps':placement,'uniqueDeleteProofs':proof,'scope':'Actual USBauxb014 manual copper/vias and true pad AABB. Dynamic thermal clines excluded because placement/void changes regenerate. Exact deleted objects removed only in-memory. Proposed new quiet island/void not yet native. Existing G31 right.2 spacing retained; right10 private.16 signal exception only explicitregion; no privateGNDvia present.'}
(R/f'readouts/RIGHT10_FULL_v10_{variant}_precheck.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))