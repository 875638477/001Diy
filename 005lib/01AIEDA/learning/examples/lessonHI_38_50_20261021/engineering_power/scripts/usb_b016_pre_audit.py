from pathlib import Path
import sys,json,math,csv,re
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
from shapely.ops import nearest_points
O=H/'engineering_power';root=load(H/'review/reference_projection_screen_b016.json');audit={}
for v in ['2L','4L']:
 cp=H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');p=load(O/f'N49_{v}_policy.json');p['pendingOperations']=[];s=CopperScene(n,w,r,p)
 commonIds=set();commonXY=set();commonBB={}
 for row in csv.DictReader((Path(n['readbackDirectory'])/'hi_graph_objects.tsv').open(encoding='utf8'),delimiter='\t'):
  if row['net'].strip(chr(34))!='GND' or row['component']!='1':continue
  commonIds.add(row['object']);mt=re.search(r'\bxy \(([-+\d.]+) ([-+\d.]+)\)',row['attributes'])
  if mt:commonXY.add(tuple(float(z) for z in mt.groups()))
  if row['type'].strip(chr(34))=='shape':
   mt=re.search(r'\bbBox \(\(([-+\d.]+) ([-+\d.]+)\) \(([-+\d.]+) ([-+\d.]+)\)\)',row['attributes'])
   if mt:commonBB.setdefault(row['layer'].strip(chr(34)),[]).append(tuple(float(z) for z in mt.groups()))
 cop={l:[] for l in ['TOP','BOTTOM','L2','L3']};membership=[]
 for a in n['planes']:
  if a['net']!='GND' or not a.get('generated'):continue
  g=plane_from_native(dict(a,holes=a.get('holes') or []));l=a['layer'].removeprefix('ETCH/')
  if any(max(abs(x-y) for x,y in zip(g.bounds,bb))<.001 for bb in commonBB.get(a['layer'],[])):cop[l].append(g);membership.append(dict(kind='generatedshape',layer=l,area=g.area,bbox=g.bounds,nativeCommon=1))
 for a in n['routes']:
  if a['net']!='GND' or a.get('generatedThermal'):continue
  mt=re.search(r'\bparent (dbid:[^ )]+)',a.get('attributes',''));parent=mt.group(1) if mt else None
  if parent not in commonIds:continue
  l=a['layer'].removeprefix('ETCH/');cop[l].append(LineString(a['startEnd']).buffer(a['width']/2,quad_segs=12));membership.append(dict(kind='manualgroundcline',layer=l,points=a['startEnd'],width=a['width'],nativeParent=parent))
 for a in s.obstacles:
  if a['net']!='GND' or a['kind'] not in ['via','smdpin','thrupin']:continue
  xy=tuple(round(x,5) for x in ([a['geometry'].centroid.x,a['geometry'].centroid.y] if a['kind']=='via' else s.pins.get(a['source'],{}).get('xy',[999,999])))
  if any(math.dist(xy,b)<.001 for b in commonXY):cop[a['layer']].append(a['geometry'])
 cop={l:unary_union(g) for l,g in cop.items()};selected={'PA11_SHARED','PA12_SHARED','USB_DP','USB_DM'};details=[]
 for a in root[v]['outsideCenterlinePieces']:
  if a['net'] not in selected:continue
  line=LineString(a['points']);samples=[line.interpolate(t,normalized=True) for t in [0,.25,.5,.75,1]];same=cop[a['signalLayer']];near=[]
  for b in s.obstacles:
   if b['layer']!=a['candidateReferenceLayer'] or b['net']=='GND':continue
   d=line.distance(b['geometry'])
   if d<.7:near.append(dict(net=b['net'],kind=b['kind'],source=b['source'],bbox=b['geometry'].bounds,projectedMinDistanceMM=d))
  profile=[]
  for pt in samples:
   d=pt.distance(same) if not same.is_empty else None;nearpt=nearest_points(pt,same)[1] if not same.is_empty else None
   profile.append(dict(xy=[pt.x,pt.y],nearestSameLayerNativeCommonGNDMM=d,commonPoint=[nearpt.x,nearpt.y] if nearpt else None))
  details.append(dict(**a,sameLayerCommonProfile=profile,nearbyOppositeNonGroundCopper=near))
 summary=[a for a in root[v]['netLayerMetrics'] if a['net'] in selected];routes=[dict(net=a['net'],layer=a['layer'],points=a['startEnd'],width=a['width']) for a in n['routes'] if a['net'] in selected and not a.get('generatedThermal')]
 audit[v]=dict(status='PREAUDIT_ACTUAL_COMMON_GEOMETRY_UNRESOLVED_REFERENCE_NO_SI_ACCEPTANCE',boardSHA=w['sha256'],reflectedRootMetrics=summary,missingPieces=details,manualRoutes=routes,groundMembershipEvidence=membership,limits=['Coplanar GND included only nativecomponent1 paths/pads/vias/generatedplanes; quiet static excluded even if sameGND','SMD/through land bbox is conservative polygon approximation, not fieldmodel','Opposite nearby foreign copper correlation does not alone prove historical causalvoidcreation','CurrentTOPnotfinal; must rerunactualsameLayercommonwidthcore after realfinalTOPfill','Actualcommonconnectivity still does notprove HFcurrentreturn path or90ohm impedance'])
 print(v,[(a['net'],a['signalLayer'],a['projectedCenterlineOutsidePlaneMm'])for a in summary]);print('SHARED',[(a['net'],a['points'],[(round(z['xy'][1],3),round(z['nearestSameLayerNativeCommonGNDMM'],3))for z in a['sameLayerCommonProfile']])for a in details if a['net'].startswith('PA')])
(O/'readouts/USB_b016_actual_common_pre_audit.json').write_text(json.dumps(audit,indent=2))