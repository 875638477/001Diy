from pathlib import Path
import json,sys,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power';sys.path.insert(0,str(R/'tooling/packages'));sys.path.insert(0,str(P/'scripts'))
from shapely.geometry import LineString,Point,box
from cadence_poly import plane_from_native
f=R/'review/PROVISIONAL_FAILED_BOOT_2L_GEOMETRY.json';s=json.loads(f.read_text(encoding='utf-8'));g=LineString([[52.8984,27.18],[47.27,27.18]]).buffer(.1);near=[];planes=[]
for a in s['routes']:
 if a['layer'] not in ['TOP','ETCH/TOP']:continue
 q=LineString(a['startEnd']).buffer(a['width']/2);d=g.distance(q)
 if d<.45:near.append(dict(kind='line',net=a['net'],startEnd=a['startEnd'],width=a['width'],gap=d,intersectionArea=g.intersection(q).area,generatedThermal=a.get('generatedThermal')))
for c in s['placements']:
 for a in c['pins']:
  if not a.get('padBBox'):continue
  q=box(*a['padBBox'][0],*a['padBBox'][1]);d=g.distance(q)
  if d<.45:near.append(dict(kind='pad',ref=c['ref'],pin=a['number'],net=a['net'],xy=a['xy'],padBBox=a['padBBox'],gap=d,intersectionArea=g.intersection(q).area))
for a in s['vias']:
 q=Point(a['xy']).buffer(.26 if 'HI_VIA026' in a['padstack']else.3);d=g.distance(q)
 if d<.45:near.append(dict(kind='via',net=a['net'],xy=a['xy'],padstack=a['padstack'],gap=d,intersectionArea=g.intersection(q).area))
for a in s['planes']:
 if a['layer'] not in ['TOP','ETCH/TOP']or not a.get('filled'):continue
 q=plane_from_native(dict(a,holes=a.get('holes')or[]));d=g.distance(q)
 if d<.45:planes.append(dict(net=a['net'],layer=a['layer'],generated=a.get('generated'),filled=a.get('filled'),nativeArea=a.get('area'),gap=d,intersectionArea=g.intersection(q).area,bounds=q.bounds))
out=dict(status='DIAGNOSTIC_NATIVE_UNSAVED_FAILED_NOT_ACCEPTANCE',actualSource=str(f),tested=dict(net='BOOT0',layer='TOP',points=[[52.8984,27.18],[47.27,27.18]],width=.2),nearbyCopper=near,nearbyFilledPlanes=planes,scope='Allactual frozen failurestage geometry; not futureprediction. Does not establish nativeAPI rootcause.')
(P/'readouts/actual_BOOT_failure07_geometry.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))