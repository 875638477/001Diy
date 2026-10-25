from pathlib import Path
import json,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');H=R.parent;sys.path.insert(0,str(H/'tooling/packages'))
from shapely.geometry import LineString
m=json.loads((H/'engineering_mcu/plans/mcu_critical_routes_v6.json').read_text());areas=[]
for o in m['operations']:
 if o['id'] in ['HSE_GUARD_LEFT_NORTH','HSE_GUARD_RIGHT_NORTH','HSE_GUARD_RIGHT_LOWER']:
  poly=LineString(o['points']).buffer(.6,quad_segs=12);areas.append(dict(id='ACTUAL_'+o['id']+'_SHADOW',polygon=list(poly.exterior.coords)[:-1],layers=['TOP','BOTTOM'],allowedNets=['GND','OSC_IN','OSC_OUT','XTAL_OUT'],purpose='Quiet actual TOPguard .6wide plus.3 engineering spacing; ordinary traces cannot hug opposite-layer edge'))
p=R/'RIGHT10_source_joint_v4.json';d=json.loads(p.read_text());d['quietTopGuardShadows']=areas;d['oscillatorReference']['additionalGlobalTOPApplicationVoidPolygons']=[a['polygon'] for a in areas];d['nativeAcceptance'].append('Final globalTOP applicationGND must void actualquiet TOPguard .6width +.3margin too (north reaches40.4), keep case opening. Never allow new pour to form secondquiet anchor.');p.write_text(json.dumps(d,indent=2),encoding='utf-8')
for v in ['2L','4L']:
 f=R/f'RIGHT10_long_policy_{v}_v4.json';d=json.loads(f.read_text());d['reservedAreas'] += areas;f.write_text(json.dumps(d,indent=2),encoding='utf-8')
print(len(areas))