from pathlib import Path
import json,sys,math,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'));sys.path.insert(0,str(R/'scripts'))
from shapely.geometry import LineString,Point,box
from shapely.ops import unary_union
from cadence_poly import conservative_plane
b=json.loads((H/'inventory/checkpoints/postcritical_4L_b010/normalized.json').read_text());p=json.loads((H/'plans/SPI_external_4L_candidate_v5.json').read_text())
P={l:unary_union([conservative_plane(dict(x,holes=x['holes'] or [])) for x in b['planes'] if x['net']=='GND' and x['layer']=='ETCH/'+l]) for l in ['L2','L3']}
results=[]
for o in p['operations']:
 if o['type']!='route':continue
 line=LineString(o['points']);ref='L2' if o['layer']=='TOP' else 'L3';test=line.buffer(.1)
 own_terminals=unary_union([box(*z['padBBox'][0],*z['padBBox'][1]).buffer(.301) for c in b['placements'] if c['ref']=='J6' for z in c['pins'] if z['net']==o['net']]); d=test.difference(P[ref]);core=d.difference(own_terminals);results.append(dict(id=o['id'],net=o['net'],layer=o['layer'],reference=ref,length_mm=line.length,footprintArea_mm2=test.area,uncoveredArea_mm2=d.area,uncoveredOutsideOwnHeaderAntipad_mm2=core.area,uncoveredBBox=list(d.bounds) if not d.is_empty else None))
source='inventory/checkpoints/postcritical_4L_b010/normalized.json'
out={'status':'FROZEN_REFERENCE_PROJECTION_PRECHECK_NOT_NATIVE_FINAL','source':source,'sourceJSON_SHA256':hashlib.sha256((H/source).read_bytes()).hexdigest(),'candidate':'plans/SPI_external_4L_candidate_v5.json','checks':results,'passes_all_new_path_footprints':all(x['uncoveredOutsideOwnHeaderAntipad_mm2']<1e-8 for x in results),'limits':['Actual pre-route native L2/L3 GND copper projection, converted with official signed arc semantics and conservative tolerance. New signal-via antipads are not present yet, final fill must be rechecked.','Own signal THT landing necessarily has a ground antipad, excluded only with its own actual pad AABB +0.301mm. This is not a remote reference hole. Header has only one GND at pin6; external cable return/edge limits remain explicit.', 'Return via within 1.5mm at each signal transition still required. No 90ohm or SPI timing/simulation certification.','MOSI BOTTOM y26.25 passes under TOP SW/inductor region: intervening actual L3 is present, but switching noise/EMI tradeoff remains; exact edge/return checks mandatory.']}
(R/'readouts/SPI_external_4L_v5_actual_L3_projection.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))