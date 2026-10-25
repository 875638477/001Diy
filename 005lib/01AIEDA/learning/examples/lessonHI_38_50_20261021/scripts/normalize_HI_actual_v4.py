from pathlib import Path
import re,json,csv,argparse,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--log',required=True);P.add_argument('--variant',choices=['4L','2L'],required=True);P.add_argument('--output')
a=P.parse_args();B=Path(a.log);assert B.resolve().is_relative_to(R.resolve())
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=='(':
   q=[]
   while t[i]!=')':q.append(take())
   i+=1;return q
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def rows(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def ssrow(x):return {k:sx(v) for k,v in x.items()}
def absoluteBox(box,xy):
 if box is None:return None
 return [[round(box[i][j]+xy[j],6) for j in range(2)] for i in range(2)]
symbols=[ssrow(x) for x in rows(B/'g_actual_symbols.tsv')]
pins=[ssrow(x) for x in rows(B/'g_actual_pins.tsv')]
geometries=[ssrow(x) for x in rows(B/'g_actual_geometry.tsv')]
texts=[ssrow(x) for x in rows(B/'board_instance_texts.tsv')]
metadata=json.loads((R/f'inventory/inventory_{a.variant}.json').read_text(encoding='utf8'))
metas={x['ref']:x for x in metadata['components']}
placements=[];mechanical=[]
for s in symbols:
 ref=s['refdes'];s['ref']=ref
 if ref is None:mechanical.append(s);continue
 pp=[]
 for p in pins:
  if p['refdes']!=ref or p['layer']!='ETCH/TOP':continue
  pp.append({'number':p['pin'],'xy':p['xy'],'net':p['net'],'padstack':p['padstack'],'rotation':p['padRotation'],'mechanical':p['mechanical'],'figure':p['figure'],'padLocalBBox':p['padbbox'],'padBBox':absoluteBox(p['padbbox'],p['xy'])})
 g=[x for x in geometries if x['refdes']==ref]
 placements.append({'ref':ref,'package':s['package'],'model':metas[ref]['model'],'value':metas[ref]['value'],'xy':s['xy'],'rotation':s['rotation'],'mirrored':s['mirrored'],'bodyExtent':s['bodyExtent'],'bbox':s['bbox'],'pins':pp,'geometry':g,'texts':[x for x in texts if x['refdes']==ref]})
def route_key(net,layer,ends,width):
 return (net,layer,tuple(sorted(tuple(p) for p in ends)) if ends else None,width)
role_index={}
if (B/'hi_route_roles.tsv').is_file():
 for rr in rows(B/'hi_route_roles.tsv'):
  role=ssrow(rr)
  parent_attrs=role.get('parentAttributes') or []
  parent_props=dict(zip(parent_attrs[::2],parent_attrs[1::2]))
  role['lineThermal']=bool(role.get('lineThermal',role.get('thermal')))
  role['parentThermal']=bool(parent_props.get('thermal'))
  role['thermal']=role['lineThermal'] or role['parentThermal']
  k=route_key(role['net'],role['layer'],role['startEnd'],role['width'])
  role_index.setdefault(k,[]).append(role)
routes=[]
for x in rows(B/'route_geometry.tsv'):
 if sx(x['layer']).startswith('ETCH/'):
  routes.append({'kind':sx(x['kind']),'net':sx(x['net']),'layer':sx(x['layer']),'startEnd':sx(x['startEnd']),'width':sx(x['width']),'attributes':x['attributes']})
for route in routes:
 matches=role_index.get(route_key(route['net'],route['layer'],route['startEnd'],route['width']),[])
 route['nativeProvenance']=matches
 route['generatedThermal']=bool(matches) and all(m.get('thermal') for m in matches) if matches else None
 route['fixedManualCline']=any(m.get('isEtch') and not m.get('thermal') and m.get('parentType')=='path' for m in matches) if matches else None
actualEtchLayerSequence=['ETCH/'+sx(x['name']) for x in rows(B/'cross_section.tsv') if sx(x['layerType'])=='CONDUCTOR']
actualEtchLayers=set(actualEtchLayerSequence)
vias=[];seen=set()
for x in rows(B/'vias.tsv'):
 x=ssrow(x)
 if x['layer'].startswith('ETCH/') and x['layer'] not in actualEtchLayers:continue
 key=(x['name'],x['x'],x['y'],x['net'])
 if key not in seen:
  seen.add(key);vias.append({'padstack':x['name'],'xy':[x['x'],x['y']],'net':x['net'],'usage':x['usage'],'drill':x['drill'],'pads':[]})
 next(v for v in vias if v['padstack']==x['name'] and v['xy']==[x['x'],x['y']] and v['net']==x['net'])['pads'].append({'layer':x['layer'],'figure':x['figure'],'bbox':x['bbox']})
copper=[ssrow(x) for x in rows(B/'g_copper_shapes.tsv')]
data={'status':'NATIVE_SNAPSHOT_NORMALIZED','variant':a.variant,'readbackDirectory':str(B),'placements':placements,'mechanical':mechanical,'routes':routes,'vias':vias,'planes':copper,'copperPadBBoxConvention':'padBBox is absolute board bbox = native padLocalBBox translated by native pin.xy; axlDBGetPad already applies pin rotation. Geometry/PlaceBound native bbox and vertices are absolute.','actualEtchLayers':actualEtchLayerSequence,'routeProvenanceSource':str(B/'hi_route_roles.tsv') if role_index else None,'thermalClassification':'Native line thermal OR native parent path thermal. Cadence17.2 generated reliefs return line.thermal=nil but parent.thermal=t; raw parentAttributes retained.','scope':'Only actual physical conductor layers from native cross_section.tsv are included in via pad maps; nonexistent-layer nil probes remain in original raw TSV. Geometric evidence normalized from original native TSV; not a replacement for original native readback, DRC, or electrical route validation.'}
out=Path(a.output) if a.output else R/f'inventory/normalized_actual_{a.variant}.json'
assert out.resolve().is_relative_to(R.resolve())
out.write_text(json.dumps(data,indent=2),encoding='utf8')
print(json.dumps({'output':str(out),'placements':len(placements),'routeSegments':len(routes),'uniqueVias':len(vias),'copperPolygons':len(copper),'sha256':hashlib.sha256(out.read_bytes()).hexdigest().upper()}))
