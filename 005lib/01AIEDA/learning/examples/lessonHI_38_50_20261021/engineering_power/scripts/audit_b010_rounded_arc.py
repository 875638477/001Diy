from pathlib import Path
import json,sys
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'));sys.path.insert(0,str(R/'scripts'))
import cadence_poly as cp
rows=[]
for v in ['2L','4L']:
 b=json.loads((H/f'inventory/checkpoints/postcritical_{v}_b010/normalized.json').read_text())
 for j,z in enumerate(b['planes']):
  q=cp.plane_from_native(dict(z,holes=z['holes'] or []));rows.append(dict(variant=v,index=j,layer=z['layer'],nativeArea=z['area'],convertedArea=q.area,absoluteError_mm2=abs(q.area-z['area'])))
out=dict(status='ROUNDED_ARC_BOUNDED_FLATTEN_AREA_AUDIT',rows=rows,flattenedArcs=cp.ROUNDED_ARC_FLATTENED,maximumSagitta_mm=max((x['sagitta_mm'] for x in cp.ROUNDED_ARC_FLATTENED),default=0),note='Only ambiguous quadrant-tangent minor arcs with sagitta<=1e-5mm flattened; conservative proof shrinks outer/expands holes0.0001mm. Polygon source coordinate rounding and chordal approximation remain quantified; native acceptance preferred.')
(R/'readouts/arc_b010_area_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='flattenedArcs'},indent=2));print('flattened count',len(cp.ROUNDED_ARC_FLATTENED))