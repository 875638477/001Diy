from pathlib import Path
import sys,json,argparse
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tooling/packages'));sys.path.insert(0,str(R/'engineering_power/scripts'));from cadence_poly import plane_from_native
p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--out',required=True);p.add_argument('--layers',default='TOP,BOTTOM');a=p.parse_args();C=Path(a.checkpoint);s=json.loads((C/'normalized.json').read_text(encoding='utf8'));ls=a.layers.split(',');out=Path(a.out).resolve();assert out.is_relative_to(R)
def rings(g):
 return [{'outer':list(q.exterior.coords),'holes':[list(h.coords) for h in q.interiors]} for q in ([g] if g.geom_type=='Polygon' else g.geoms)]
x={'label':C.name+' | Native copper; pad BBOX approximation','layers':ls,'planes':[],'pads':[],'bodies':[],'routes':[],'vias':[]}
for q in s['planes']:
 if q['layer'].removeprefix('ETCH/') in ls:x['planes']+=rings(plane_from_native(dict(q,holes=q.get('holes') or [])))
for q in s['placements']:
 x['bodies'].append({'ref':q['ref'],'xy':q['xy'],'bbox':q.get('bodyExtent')})
 for k in q['pins']:
  if k.get('number'):x['pads'].append({'bbox':k['padBBox']})
for q in s['routes']:
 if q['layer'].removeprefix('ETCH/') in ls:x['routes'].append({'points':q['startEnd'],'width':q['width'],'net':q['net'],'layer':q['layer'].removeprefix('ETCH/')})
for q in s['vias']:
 pads=[k for k in q.get('pads',[]) if k['layer'].removeprefix('ETCH/') in ls]
 if pads:x['vias'].append({'xy':q['xy'],'radius':max(abs(z) for k in pads for b in k['bbox'] for z in b),'drill':q['drill']})
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(x),encoding='utf8');print('Vector draw data',len(x['routes']),'segments',len(x['vias']),'vias',len(x['planes']),'polygons')
