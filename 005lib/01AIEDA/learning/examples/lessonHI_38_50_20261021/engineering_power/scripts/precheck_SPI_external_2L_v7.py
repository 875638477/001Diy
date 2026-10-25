from pathlib import Path
import json,sys,math
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'))
from shapely.geometry import Point,LineString,box
b=json.loads((H/'inventory/checkpoints/postcritical_2L_b010/normalized.json').read_text());p=json.loads((R/'SPI_external_2L_engineered_v7.json').read_text())
for o in p['operations']:
 if o['type']=='deleteSegment':
  hits=[r for r in b['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in [o['points'],o['points'][::-1]] and abs(r['width']-o['width'])<1e-6]
  assert len(hits)==1,(o['id'],len(hits))
  b['routes'].remove(hits[0])
items=[]
def add(i,n,l,g,new=False,kind='line'):items.append(dict(id=i,net=n,layer=l,g=g,new=new,kind=kind))
for j,r in enumerate(b['routes']):
 if r['kind']=='line' and r['net']:add('BASE_R'+str(j),r['net'],r['layer'].split('/')[-1],LineString(r['startEnd']).buffer(r['width']/2,quad_segs=16))
for j,v in enumerate(b['vias']):
 for l in ['TOP','BOTTOM']:add('BASE_V'+str(j),v['net'],l,Point(v['xy']).buffer(.3,quad_segs=32),kind='via')
for c in b['placements']:
 for pad in c['pins']:
  if pad['figure']=='NULL':continue
  bb=pad['padBBox'];ls=['TOP','BOTTOM'] if c['ref'].startswith('J') and c['ref']!='J2' else ['TOP']
  for l in ls:add(c['ref']+'.'+pad['number'],pad['net'],l,box(*bb[0],*bb[1]),kind='pad')
for o in p['operations']:
 if o['type']=='route':
  for j,(a,z) in enumerate(zip(o['points'],o['points'][1:])):add(o['id']+':'+str(j),o['net'],o['layer'],LineString([a,z]).buffer(o['width']/2,quad_segs=32),True)
 if o['type']=='via':
  for l in ['TOP','BOTTOM']:add(o['id'],o['net'],l,Point(o['xy']).buffer(.3,quad_segs=32),True,'via')
def req(a,b):
 ns={a['net'],b['net']}
 if ns&{'BUCK_SW','BUCK_BOOT'}:return .5
 if ns&{'GND','V3V3','V5','VDDA'}:
  return .16 if a['kind']=='pad' or b['kind']=='pad' else .2 if a['kind']=='via' and b['kind']=='via' else .3
 if ns&{'ADC_IN','ADC0','BUCK_FB'}:return .3
 return .16 if 'pad' in {a['kind'],b['kind']} else .2
issues=[];tests=0
for i,a in enumerate(items):
 for z in items[i+1:]:
  if not(a['new'] or z['new']) or a['net']==z['net'] or a['layer']!=z['layer']:continue
  tests+=1;d=a['g'].distance(z['g']);mn=req(a,z)
  if d<mn-1e-5:issues.append(dict(a=a['id'],b=z['id'],netA=a['net'],netB=z['net'],layer=a['layer'],gap=round(d,6),overlap=round(a['g'].intersection(z['g']).area,6),required=mn))
out={'status':'PRECHECK_PASS_NOT_NATIVE' if not issues else 'REVISE_CANDIDATE','tests':tests,'issueCount':len(issues),'issues':issues,'note':'Actual b010 routes/vias plus conservative pad AABB. Spacing uses engineering conservative line .2/power .3; pair pad minima .16. Native full rules/plane refill still required.'}
(R/'readouts/SPI_external_2L_v7_precheck.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))