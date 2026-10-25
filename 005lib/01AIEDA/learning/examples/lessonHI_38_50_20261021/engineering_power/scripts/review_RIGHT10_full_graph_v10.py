from pathlib import Path
import json,sys,math,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'));from shapely.geometry import Point,LineString,box
v=sys.argv[1] if len(sys.argv)>1 else '2L';f=R/f'RIGHT10_FULL_{v}_v10.json';p=json.loads(f.read_text());b=json.loads((H/f'inventory/checkpoints/USB_aux_{v}_b014/normalized.json').read_text());nets={a['net'] for a in p['anchors']};items=[];links=[];pins={};newids=set()
def add(net,layer,geom,label,new=False):
 i=len(items);items.append(dict(net=net,layer=layer,g=geom,label=label,new=new));return i
poses={a['ref']:a for a in p['placementChanges']}
for a in b['placements']:
 dx=poses.get(a['ref'],a)['xy'][0]-a['xy'][0];dy=poses.get(a['ref'],a)['xy'][1]-a['xy'][1]
 for z in a['pins']:
  if z['net'] not in nets:continue
  bb=z['padBBox'];g=box(bb[0][0]+dx,bb[0][1]+dy,bb[1][0]+dx,bb[1][1]+dy);label=a['ref']+'.'+z['number'];layers=['TOP','BOTTOM'] if a['ref'].startswith('J') and a['ref']!='J2' else ['TOP'];ids=[add(z['net'],l,g,label) for l in layers];pins[label]=ids[0]
  if len(ids)>1:links.append(tuple(ids))
dels=[o for o in p['operations'] if o['type']=='deleteSegment'];delvs=[o for o in p['operations'] if o['type']=='deleteVia']
for a in b['routes']:
 if a['net'] not in nets or a['generatedThermal']:continue
 if any(a['net']==o['net'] and a['layer']=='ETCH/'+o['layer'] and abs(a['width']-o['width'])<1e-6 and a['startEnd'] in [o['points'],o['points'][::-1]] for o in dels):continue
 add(a['net'],a['layer'].split('/')[-1],LineString(a['startEnd']).buffer(a['width']/2,quad_segs=16),'BASE_ROUTE')
for a in b['vias']:
 if a['net'] not in nets or any(a['net']==o['net'] and a['xy']==o['xy'] for o in delvs):continue
 ids=[add(a['net'],l,Point(a['xy']).buffer(.3,quad_segs=16),'BASE_VIA') for l in ['TOP','BOTTOM']];links.append(tuple(ids))
for o in p['operations']:
 if o['net'] not in nets:continue
 if o['type']=='route':
  for j,(a,z) in enumerate(zip(o['points'],o['points'][1:])):add(o['net'],o['layer'],LineString([a,z]).buffer((o['widths'][j] if 'widths' in o else o['width'])/2,quad_segs=16),o['id'],True)
 if o['type']=='via':
  ids=[add(o['net'],l,Point(o['xy']).buffer(o.get('padDiameterMM',.6)/2,quad_segs=16),o['id'],True) for l in ['TOP','BOTTOM']];links.append(tuple(ids))
parent=list(range(len(items)))
def find(i):
 while i!=parent[i]:parent[i]=parent[parent[i]];i=parent[i]
 return i
def union(i,j):parent[find(i)]=find(j)
for i,j in links:union(i,j)
for i,a in enumerate(items):
 for j in range(i):
  z=items[j]
  if a['net']==z['net'] and a['layer']==z['layer'] and a['g'].distance(z['g'])<1e-6:union(i,j)
checks=[];fail=[]
for proof in p['proofs']:
 if proof['net'] not in nets:continue
 ok=find(pins[proof['source']])==find(pins[proof['target']]);checks.append(dict(**proof,connected=ok))
 if not ok:fail.append(checks[-1])
orphans=[]
for a in p['anchors']:
 source=find(pins['U1.'+str(a['pin'])]);bad=sorted({z['label'] for j,z in enumerate(items) if z['net']==a['net'] and z['new'] and find(j)!=source})
 if bad:orphans.append(dict(net=a['net'],unreachedOperations=bad))
out=dict(status='PASS_EXPLICIT_ENDPOINT_GEOMETRY_GRAPH' if not fail and not orphans else 'FAIL',variant=v,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),checks=checks,failures=fail,orphanOperations=orphans,scope='Independent geometry DSU from actualmanualcopper/true pad geometry plus fullfuture owncandidate; no globalnet-class symbolicshortcut. No plane/GND return certification. Cadence not invoked.')
(R/f'readouts/RIGHT10_FULL_{v}_v10_explicit_graph.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))