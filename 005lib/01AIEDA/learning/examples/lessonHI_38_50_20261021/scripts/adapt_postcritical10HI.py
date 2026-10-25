from pathlib import Path
import json,sys,copy,hashlib,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
sys.dont_write_bytecode=True
sys.path.insert(0,str(R/'tooling/packages'))
from shapely.geometry import Polygon
paths=[R/'engineering_power/STAR_reroute_07c.json',R/'engineering_power/V3_peripheral_distribution_06b.json',R/'engineering_mcu/plans/gpio_north_escape_v6.json',R/'engineering_power/interface_CAN_routes_04.json',R/'engineering_power/CAN_local_supply_05.json',R/'plans/SPI_source_explicit_v5.json']
plans=[json.loads(p.read_text(encoding='utf8')) for p in paths]
mcu=json.loads((R/'engineering_mcu/plans/mcu_critical_routes_v6.json').read_text(encoding='utf8'))
moat=Polygon(mcu['oscillatorReference']['applicationGroundVoidPolygon'])
ids=[op['id'] for d in plans for op in d['operations']]
assert len(ids)==len(set(ids))
components={x['ref'] for x in json.loads((R/'inventory/normalized_actual_4L.json').read_text(encoding='utf8'))['placements']}
for v in ['4L','2L']:
 ops=copy.deepcopy([op for d in plans for op in d['operations']])
 known={op['id'] for op in ops};aliases={}
 vias=[op for op in ops if op['type']=='via']
 for op in ops:
  if op['type']!='route':continue
  for field,xy in [('from',op['points'][0]),('to',op['points'][-1])]:
   val=op.get(field)
   if isinstance(val,list):
    assert len(val) in (1,2), 'Endpoint list must be a single named alias or [ref,pin]'
    val=val[0] if len(val)==1 else val[0]+'.'+str(val[1]);op[field]=val
   if val and '.' not in val and val not in known:
    kind='via' if val.startswith('V_') or val.startswith('G31_') else 'point'
    aliases.setdefault(val,{'id':val,'net':op['net'],'layer':op['layer'],'xy':xy,'type':kind})
   if not val:
    matches=[w for w in vias if w['net']==op['net'] and math.dist(w['xy'],xy)<1e-5]
    if len(matches)==1:op[field]=matches[0]['id']
 reg=plans[0]['rules'][0];cset='HI_STAR_RETURN_GND_P_'+v
 constraints=[{'type':'csetCopy','domain':'physical','name':cset,'copyFrom':'P_GND_PLANE' if v=='4L' else 'HI2L_P_GROUND','values':{'necklength_max':'1.4 MM'}},{'type':'region','id':reg['id'],'layer':'TOP','polygon':reg['polygon'],'assignments':[{'domain':'physical','netClass':'G31_GND_P' if v=='4L' else 'HI2L_GROUND_P','cset':cset}]}]
 clips=[]
 if v=='2L':
  for i,patch in enumerate(plans[2]['twoLayerReferencePatches'],1):
   original=Polygon(patch['polygon']);clipped=original.difference(moat)
   polys=list(clipped.geoms) if hasattr(clipped,'geoms') else [clipped]
   for j,p in enumerate(polys,1):
    assert p.geom_type=='Polygon' and p.is_valid and not p.is_empty
    op={'type':'shape','id':f'HI_GPIO_TOP_REF_{i}_{j}','net':'GND','layer':'TOP','polygon':[list(x) for x in p.exterior.coords[:-1]],'voids':[[list(x) for x in ring.coords[:-1]] for ring in p.interiors],'dynamic':True}
    ops.append(op)
   clips.append({'sourcePolygon':patch['polygon'],'sourceArea':original.area,'clippedArea':clipped.area,'removedMoatOverlapArea':original.intersection(moat).area})
 proofs=copy.deepcopy(plans[-1]['proofs'])
 for p in plans[1].get('expectedNewV3Endpoints',[]):proofs.append({'from':'C9.1','to':p,'connected':True})
 for a,b in [('U1.23','V_HI_STAR_GND_EAST'),('U1.23','U1.47'),('C9.1','U1.24'),('C9.1','U1.36'),('C9.1','U1.48'),('C9.1','U1.1')]:
  proofs.append({'from':a,'to':b,'connected':True})
 o={'status':'EXPLICIT_POST_USB_CRITICAL_CANDIDATE_REQUIRE_NATIVE_DRC','nativeVariant':v,'units':'mm','constraintOperations':constraints,'operations':ops,'aliases':list(aliases.values()),'proofs':proofs,'postChecks':[{'type':'hseIsolation','anchorXY':[45.45,28.85],'localLayer':'L2' if v=='4L' else 'BOTTOM','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}],'engineeringSources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()} for p in paths],'twoLayerReferencePatchClipping':clips,'notes':['Exactly remove two old BOTTOM STAR segments, preserve all other old supply copper, then build reviewed diagonal and TOP peripheral tap.','STAR07c geometric flare advances to36.952,25.222; plannedGNDneck1.397508801 <= oldG31 1.4. Newregion1.4 only; existingG31/global unmodified. Old07b native1.4654/1.4 DRC candidate retained.','GPIO6 reference patches geometrically exclude application-HSE moat on TOP; actual auto-voids/coverage/connected components require review.','SPI source5 leaves header-side ordinary routes unfinished; reference and HSE negative test are explicit, not a whole-board acceptance.']}
 p=R/f'batches/postcritical_{v}_b010.json';p.write_text(json.dumps(o,indent=2),encoding='utf8');print(v,len(ops),'ops',len(proofs),'proofs',len(aliases),'aliases','clip',clips)
