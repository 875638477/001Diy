from pathlib import Path
import sys,json,copy,math,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
from native_sexpr_data import parse
import csv
USB={'PA11_SHARED','PA12_SHARED'}
def geom_parts(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return[g]
 return[p for a in getattr(g,'geoms',[])for p in geom_parts(a)]
def cu(op):
 if op['type']=='via':return Point(op['xy']).buffer(.26,quad_segs=64)
 pts=op['points'];return LineString(pts).buffer(op['width']/2,quad_segs=64)
def mutated(v):
 cp=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');plan=load(O/f'USB_RETURN_SOURCE_COMPARE_{v}_03.json');after=copy.deepcopy(n)
 for op in plan['operations']:
  if op['type']=='deleteVia':
   xs=[a for a in after['vias']if a['net']==op['net']and a['xy']==op['xy']];assert len(xs)==1;old=xs[0];after['vias'].remove(old)
  elif op['type']=='deleteSegment':
   xs=[a for a in after['routes']if a['net']==op['net']and a['layer']=='ETCH/'+op['layer']and abs(a['width']-op['width'])<1e-7 and(a['startEnd']==op['points']or a['startEnd']==op['points'][::-1])];assert len(xs)==1;after['routes'].remove(xs[0])
  elif op['type']=='via':
   a=copy.deepcopy(old);a['xy']=op['xy'];after['vias'].append(a)
  elif op['type']=='route':
   for a,b in zip(op['points'],op['points'][1:]):after['routes'].append(dict(net=op['net'],layer='ETCH/'+op['layer'],startEnd=[a,b],width=op['width'],kind='line',fixedManualCline=True,generatedThermal=False))
 p=load(O/f'N49_{v}_policy.json');p['pendingOperations']=[];scenes=[CopperScene(a,w,r,p)for a in [n,after]]
 for proof in plan['connectivityProofs']:assert scenes[0].pins[proof['from']]['net']==scenes[0].pins[proof['to']]['net']
 log=Path(n['readbackDirectory']);allowed={}
 for a in csv.DictReader((log/'hi_dynamic_boundaries.tsv').open(),delimiter='\t'):
  if not a.get('vertices'):continue
  l=a['layer'].strip('"').removeprefix('BOUNDARY/');g=polygon_from_vertices(parse(a['vertices']));holes=parse(a['permanentVoids'])or[]
  if holes:g=g.difference(unary_union([polygon_from_vertices(h)for h in holes]))
  allowed[l]=g
 results=[];roi=box(38.7,18.8,42.5,22.3);native={}
 for l in ['TOP','BOTTOM']if v=='2L'else['TOP','L2','L3']:
  plane=unary_union([plane_from_native(dict(a,holes=a.get('holes')or[]))for a in n['planes']if a['layer']=='ETCH/'+l and a.get('generated')]);native[l]=plane
  old=[];new=[]
  for op in plan['operations']:
   if op['type']in ['deleteVia','via']:
    (old if op['type']=='deleteVia'else new).append(Point(op['xy']).buffer(.26+.3002,quad_segs=64))
   elif l in ['TOP','BOTTOM']and op.get('layer')==l and op['type']in['deleteSegment','route']:(old if op['type']=='deleteSegment'else new).append(LineString(op['points']).buffer(op['width']/2+.3002,quad_segs=64))
  old=unary_union(old);new=unary_union(new)
  blocks=[]
  if l in ['TOP','BOTTOM']:
   for a in scenes[1].obstacles:
    if a['layer']!=l or a['net']=='GND' or a['kind']in['keepout','hole']:continue
    blocks.append(a['geometry'].buffer(.3002))
  else:
   for a in after['vias']:
    if a['net']=='GND':continue
    pad=next(q for q in a['pads']if q['layer']=='ETCH/'+l);rad=(pad['bbox'][1][0]-pad['bbox'][0][0])/2;blocks.append(Point(a['xy']).buffer(rad+.3002,quad_segs=64))
   # In this local source ROI there are no foreign through-pin pads; assert.
   for c in after['placements']:
    for a in c['pins']:
     if a['net']=='GND':continue
     if a['figure']=='CIRCLE'and roi.intersects(box(*a['padBBox'][0],*a['padBBox'][1])):raise AssertionError(('UnexpectedthroughpinROI',c['ref'],a['number']))
  blocks=unary_union(blocks)
  freed=old.difference(blocks).intersection(allowed[l])
  predicted=plane.difference(new).union(freed)
  # New freed polygons must touch an actually connected plane piece in 2D;
  # that is still weaker than an actualpostfillnativecommonproof.
  retained=[]
  for g in geom_parts(predicted):
   if g.intersection(plane).area>1e-5:retained.append(g)
  predicted=unary_union(retained)
  local=dict(layer=l,nativeAreaROI=plane.intersection(roi).area,predictedAreaROI=predicted.intersection(roi).area,newlyAvailableROI=predicted.difference(plane).intersection(roi).area,newlyBlockedROI=plane.difference(predicted).intersection(roi).area,scope='BOOLEANPOTENTIALONLY .3002mmGNDclearance assumed; notCadencesmoothing/thermals/DRC/netgraph')
  for net in USB:
   metrics={}
   for label,g in [('actualBefore',plane),('booleanPotentialAfter',predicted)]:
    length=missing=footArea=footMissing=0
    for a in n['routes']:
     if a['net']!=net or a['layer']!='ETCH/TOP':continue
     q=LineString(a['startEnd']);foot=q.buffer(a['width']/2,cap_style=2);length+=q.length;missing+=q.difference(g.buffer(.0001)).length;footArea+=foot.area;footMissing+=foot.difference(g.buffer(.0001)).area
    metrics[label]=dict(centerlineLengthMM=length,missingCenterlineMM=missing,footprintAreaMM2=footArea,missingFootprintMM2=footMissing)
   if (l=='BOTTOM'and v=='2L')or(l=='L2'and v=='4L'):results.append(dict(net=net,reference=l,**metrics))
  local['booleanAvailableGeometryWKT']=predicted.intersection(roi).wkt
  (O/f'readouts/USB_RETURN_SOURCE_COMPARE_{v}_03_{l}_potential.json').write_text(json.dumps(local,indent=2)+'\n')
 # Newviaallconductorclearances, no TOP/BOTTOM-only radius oversight.
 newxy=[39.8,20.52];nearest=[]
 for a in after['vias']:
  if a['xy']==newxy:continue
  rad=(a['pads'][0]['bbox'][1][0]-a['pads'][0]['bbox'][0][0])/2;nearest.append(dict(net=a['net'],xy=a['xy'],copperGapMM=math.dist(newxy,a['xy'])-.26-rad))
 nearest.sort(key=lambda a:a['copperGapMM'])
 commonGroundNearest=[a for a in nearest if a['net']=='GND'][:3]
 out=dict(status='READ_ONLY_COMPARISON_REFERENCE_POTENTIAL_NOT_ACTUAL_FILL_OR_ACCEPTANCE',variant=v,sourceSHA=w['sha256'],plan=str(O/f'USB_RETURN_SOURCE_COMPARE_{v}_03.json'),planSHA=hashlib.sha256((O/f'USB_RETURN_SOURCE_COMPARE_{v}_03.json').read_bytes()).hexdigest(),netMetrics=results,nearestOtherViaCopperGaps=nearest[:8],nearestGroundVias=commonGroundNearest,limits=['ActualBefore is native b019; booleanPotentialAfter is only localfree-space upper-bound .3002GND expansion, noCadencesmoothing/minaperture/thermal/directCNS/joinorHFmodel','SourceUART_RX/TXphysicalpinsmustremain; removedoldviaaliasmustbeexplicitlyretired,newallconductorapprovedpointneedsadaptation','Allmanufacturingdrill/padspacingsunchanged; no0.5globalUSBspacingloweringclaimed, existinglimiteddenseescapeexceptionsneednativeeffectiveCNS','TOPCOP/neck/groundreachmaychangeafterfill: native actuals mandatory beforeacceptance','NoCADchangeapplied, criticalUSB/C14/HSEunchanged; otherSouthfuturecandidatesnotyetmerged'])
 (O/f'readouts/USB_RETURN_SOURCE_COMPARE_{v}_03_reference_potential.json').write_text(json.dumps(out,indent=2)+'\n');print(v,json.dumps(results),commonGroundNearest)
for v in ['2L','4L']:mutated(v)
