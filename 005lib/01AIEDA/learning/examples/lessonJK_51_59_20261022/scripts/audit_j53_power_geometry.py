from pathlib import Path
import json,sys,math,hashlib
R=Path(r'D:/001DIY/005lib/01AIEDA');H=R/'learning/examples/lessonHI_38_50_20261021';J=R/'learning/examples/lessonJK_51_59_20261022';A=J/'audits'
sys.path[:0]=[str(H/'tooling/packages'),str(H/'engineering_power/scripts')]
from shapely.geometry import LineString,box,Point
from shapely.ops import unary_union,nearest_points
import cadence_poly
out=[]
for v in ['2L','4L']:
 cp=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';n=json.loads((cp/'normalized.json').read_text());by={c['ref']:c for c in n['placements']};pins={c['ref']+'.'+str(p['number']):p for c in n['placements'] for p in c['pins'] if p.get('number')};manual=[r for r in n['routes'] if not r.get('generatedThermal')]
 def copper(net,layer='ETCH/TOP'):
  return unary_union([LineString(r['startEnd']).buffer(r['width']/2,quad_segs=24) for r in manual if r['net']==net and r['layer']==layer]+[box(*p['padBBox'][0],*p['padBBox'][1]) for p in pins.values() if p['net']==net])
 def nm(net):
  rows=[r for r in manual if r['net']==net];dist={}
  for r in rows:dist[str(r['width'])]=dist.get(str(r['width']),0)+math.dist(*r['startEnd'])
  return dict(net=net,manualLengthByWidthMM=dist,allManualSegments=[dict(layer=r['layer'],points=r['startEnd'],widthMM=r['width']) for r in rows],scope='Actual full-net geometry includes every branch. Width below global normal can be legal only under its original coordinate-specific constraints; this report does not evaluate effective CNS or infer currents.')
 sw,fb=copper('BUCK_SW'),copper('BUCK_FB');a,b=nearest_points(sw,fb)
 gs=[]
 for x in n['planes']:
  if x['net']=='GND' and x['layer']=='ETCH/TOP' and x.get('generated') and x.get('filled'):gs.append(cadence_poly.plane_from_native(dict(x,holes=x.get('holes')or[])))
 top=unary_union(gs+[LineString(r['startEnd']).buffer(r['width']/2,quad_segs=24) for r in manual if r['net']=='GND' and r['layer']=='ETCH/TOP']+[box(*p['padBBox'][0],*p['padBBox'][1]) for p in pins.values() if p['net']=='GND'])
 gtargets=[('C3.2','U2.1'),('C8.2','U3.2'),('C9.2','U3.2'),('C13.2','U1.23'),('C14.2','U1.35'),('C15.2','U1.47')]
 same=[]
 parts=list(top.geoms) if hasattr(top,'geoms') else [top]
 for f,t in gtargets:
  pp,qq=Point(pins[f]['xy']),Point(pins[t]['xy']);same.append(dict(fromPin=f,toPin=t,fromXY=pins[f]['xy'],toXY=pins[t]['xy'],directDistanceMM=pp.distance(qq),sameActualTOPCopperComponent=any(p.buffer(.0002).covers(pp)and p.buffer(.0002).covers(qq) for p in parts),scope='TOP polygon/real trace/pad copper connectivity only, solid via pad included by pad list only if physical pin; does not establish shortest/low-L return or native effective thermal width. CommonGND across layers has independent native proof.'))
 groundvias=[x for x in n['vias'] if x['net']=='GND'];closest=[]
 for key in ['C3.2','U2.1','R2.2','C8.2','C9.2','U4.2','U5.2']:
  p=pins[key];near=sorted(groundvias,key=lambda g:math.dist(g['xy'],p['xy']))[:3];closest.append(dict(pin=key,xy=p['xy'],nearestActualGroundVias=[dict(xy=g['xy'],padstack=g['padstack'],distanceMM=math.dist(p['xy'],g['xy'])) for g in near]))
 out.append(dict(variant=v,SWFBminActualTOPCopperDistanceMM=sw.distance(fb),nearestSWXY=[a.x,a.y],nearestFBXY=[b.x,b.y],SWCopperFootprintAreaMM2=sw.area,geometricGroundPairs=same,groundPinVias=closest,powerNetWidthAndActualSegments=[nm(net) for net in ['VIN_RAW','VIN_FUSED','VIN_PROT','BUCK_SW','BUCK_BOOT','BUCK_FB','V5','V3V3','VDDA','USB_VBUS']],notANativeDRCResult=True,notCurrentOrThermalOrImpedanceSolution=True))
p=A/'j53_power_geometry_and_return_detail.json';p.write_text(json.dumps(dict(status='READ_ONLY_ACTUAL_POWER_COPPER_WIDTH_RETURN_REVIEW',boards=out),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps([dict(variant=x['variant'],SWFBgap=x['SWFBminActualTOPCopperDistanceMM'],topGroundPairs=x['geometricGroundPairs'])for x in out],ensure_ascii=False))