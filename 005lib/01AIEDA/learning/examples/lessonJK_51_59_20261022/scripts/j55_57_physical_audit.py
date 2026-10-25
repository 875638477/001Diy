"""Explicit drill, mask and stencil review from embedded native pad shapes, no native mutations."""
from pathlib import Path
import sys,json,csv,re,math,collections,itertools
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';H=R/'learning/examples/lessonHI_38_50_20261021'
sys.path.insert(0,str(H/'tooling/packages'))
from shapely.geometry import box,Point,LineString
# Reuse only the builder's pure helper declarations; does not execute the build body.
text=(J/'scripts/j55_57_build.py').read_text(encoding='utf-8-sig');ns={};exec(text[:text.index("req=['REF DES")],ns);srows=ns['srows'];dump=ns['dump'];csvout=ns['csvout'];load=ns['load'];sx=ns['sx'];sha=ns['sha']
def primitive(fig,b):
 (x0,y0),(x1,y1)=b;w=x1-x0;h=y1-y0
 if fig=='NULL' or w<=0 or h<=0:return None,'NULL'
 if fig in ['RECTANGLE','SQUARE']:return box(x0,y0,x1,y1),'EXACT_AXIS_RECT'
 if fig=='CIRCLE' and abs(w-h)<.0001:return Point((x0+x1)/2,(y0+y1)/2).buffer(w/2,quad_segs=64),'CIRCULAR_POLYGON_APPROX'
 if fig.startswith('OBLONG'):
  if h>=w:g=LineString([((x0+x1)/2,y0+w/2),((x0+x1)/2,y1-w/2)]).buffer(w/2,quad_segs=64)
  else:g=LineString([(x0+h/2,(y0+y1)/2),(x1-h/2,(y0+y1)/2)]).buffer(h/2,quad_segs=64)
  return g,'OBLONG_POLYGON_APPROX'
 return box(x0,y0,x1,y1),'CONSERVATIVE_BBOX_ONLY_ROUND_RADIUS_NOT_EXPORTED'
summary={};allissue=[]
for v in ['2L','4L']:
 C=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';S=load(C/'normalized.json');L=Path(S['readbackDirectory']);pp=srows(L/'physical_pad_layers.tsv');actual=srows(L/'g_actual_pins.tsv');placed=srows(L/'placed_pins.tsv');pd={p['ref']:p for p in S['placements']};records=[];mask=[];paste=[]
 # Actual ref assignment comes from placed pins + physical xy/padstack. Empty numbers may occur twice and are keyed by xy.
 for pin in placed:
  xy=pin['xy'];rows=[q for q in pp if q['kind']=='PIN' and q['xy']==xy and q['padstack']==pin['padstack']]
  r=dict(Variant=v,Reference=pin['refdes'] or 'MECHANICAL_NPTH',Pin=pin['pin'],X_mm=xy[0],Y_mm=xy[1],Padstack=pin['padstack'],Mechanical=bool(pin['mechanical']),Through=bool(pin['through']),Plating=pin['plating'] or '',HoleType=pin['holeType'] or '',Drill_mm=pin['drill'] if pin['through'] else '',SlotX_mm=pin['drillX'] if pin['holeType']=='oval slot' else '',SlotY_mm=pin['drillY'] if pin['holeType']=='oval slot' else '',Profile='USB',Population='DNP' if pin['refdes'] in ['R12','R13'] else 'NOT_A_COMPONENT' if pin['mechanical'] else 'FIT')
  for label,layer in [('CopperTOP','ETCH/TOP'),('MaskTOP','PIN/SOLDERMASK_TOP'),('MaskBOTTOM','PIN/SOLDERMASK_BOTTOM'),('PasteTOP','PIN/PASTEMASK_TOP'),('PasteBOTTOM','PIN/PASTEMASK_BOTTOM')]:
   q=next((q for q in rows if q['layer']==layer),None);r[label+'_Figure']=q['figure'] if q else 'MISSING_READBACK';r[label+'_W_mm']=round(q['bbox'][1][0]-q['bbox'][0][0],6) if q else '';r[label+'_H_mm']=round(q['bbox'][1][1]-q['bbox'][0][1],6) if q else ''
   if q and q['figure']!='NULL':
    bb=[[p[i]+xy[i] for i in range(2)] for p in q['bbox']];g,quality=primitive(q['figure'],bb)
    item=dict(ref=pin['refdes'],pin=pin['pin'],xy=xy,padstack=pin['padstack'],figure=q['figure'],bbox=bb,quality=quality,geometry=g)
    if label=='MaskTOP':mask.append(item)
    if label=='PasteTOP':paste.append(item)
  r['MinimumRectangularMaskExpansionTOP_mm']=round(min((r['MaskTOP_W_mm']-r['CopperTOP_W_mm'])/2,(r['MaskTOP_H_mm']-r['CopperTOP_H_mm'])/2),6) if r['MaskTOP_Figure']!='NULL' and r['CopperTOP_Figure']!='NULL' else ''
  r['NominalCopperAnnulusMin_mm']=round(min((r['CopperTOP_W_mm']-(pin['drillX'] if pin['holeType']=='oval slot' else pin['drill']))/2,(r['CopperTOP_H_mm']-(pin['drillY'] if pin['holeType']=='oval slot' else pin['drill']))/2),6) if pin['through'] and not pin['mechanical'] else ''
  records.append(r)
 assert len(records)==278;csvout(J/f'audits/j55_{v}_278_pad_drill_mask_stencil_b019.csv',records)
 near=[]
 for a,b in itertools.combinations(mask,2):
  dist=a['geometry'].distance(b['geometry'])
  if dist<.250001:near.append(dict(RefA=a['ref'],PinA=a['pin'],RefB=b['ref'],PinB=b['pin'],NominalMaskWeb_mm=round(dist,6),GeometryA=a['quality'],GeometryB=b['quality'],Scope='NOMINAL_PAD_APERTURES_NOT_PROCESS_TOLERANCE'))
 near.sort(key=lambda x:x['NominalMaskWeb_mm']);csvout(J/f'audits/j55_{v}_nominal_mask_web_under025_b019.csv',near)
 pastecheck=[]
 for a in paste:
  x0,y0=a['bbox'][0];x1,y1=a['bbox'][1];pastecheck.append(dict(Reference=a['ref'],Pin=a['pin'],Padstack=a['padstack'],OpeningFigure=a['figure'],X0_mm=x0,Y0_mm=y0,X1_mm=x1,Y1_mm=y1,OpeningWidth_mm=round(x1-x0,6),OpeningHeight_mm=round(y1-y0,6),OpeningAreaApprox_mm2=round(a['geometry'].area,6),ShapeQualification=a['quality'],Population='DNP' if a['ref'] in ['R12','R13'] else 'FIT',StencilThickness_mm='',ProcessStatus='STENCIL_THICKNESS_REDUCTION_COATING_RELEASE_PENDING'))
 assert len(pastecheck)==211;csvout(J/f'assembly/stencil_apertures_{v}_b019_TRAINING.csv',pastecheck)
 # Text bounding boxes are broad-phase intersections only; native glyph ink must be checked in artwork.
 broad=[]
 for p in S['placements']:
  for t in p['texts']:
   if not t['layer'].endswith('/SILKSCREEN_TOP'):continue
   tb=box(*t['bbox'][0],*t['bbox'][1])
   for m in mask:
    if tb.intersection(m['geometry']).area>1e-6:broad.append(dict(TextRef=p['ref'],Layer=t['layer'],Text=t['text'],MaskRef=m['ref'],MaskPin=m['pin'],TextBBox=t['bbox'],MaskBBox=m['bbox'],Result='BBOX_INTERSECTION_REQUIRES_ACTUAL_GLYPH_REVIEW_NOT_CONFIRMED_INK_VIOLATION'))
 dump(J/f'audits/j55_{v}_silk_bbox_candidates_b019.json',dict(scope='Broad-phase only. Bounding box overlap does not prove silk ink on pad. User requires ref origin positions; no unapproved text relocation.',candidates=broad))
 # Low-height zone uses native placement envelope as conservative location test; absent max is unknown, not automatic 1mm.
 low=[]
 for p in S['placements']:
  q=box(*p['bodyExtent'][0],*p['bodyExtent'][1]);overlap=q.intersection(box(10,42,30,52)).area
  if overlap>1e-8:low.append(dict(ref=p['ref'],intersectionAreaMM2=overlap,placeBoundProps=[g['props'] for g in p['geometry'] if g['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP']))
 inv=load(H/f'inventory/inventory_{v}.json');locals={c['ref']:{q['number']:q['localXY'] for q in c['logicalPins']} for c in inv['components']};rotproof=[]
 for p in S['placements']:
  theta=math.radians(p['rotation']);co,si=math.cos(theta),math.sin(theta)
  for pin in p['pins']:
   if not pin['number']:continue
   x,y=locals[p['ref']][pin['number']];expected=[p['xy'][0]+co*x-si*y,p['xy'][1]+si*x+co*y];err=math.dist(expected,pin['xy']);rotproof.append(dict(ref=p['ref'],pin=pin['number'],expected=expected,actual=pin['xy'],errorMM=round(err,8)))
 assert len(rotproof)==272 and max(x['errorMM'] for x in rotproof)<.0002;dump(J/f'audits/j57_{v}_CAD_CCW_rotation_272pins_b019.json',dict(scope='Native package local pin + CCW symbol rotation reproduces actual physical pins; this is not assembly factory zero-angle mapping.',checks=rotproof))
 # Read official actual text block dimensions where available; never infer from visual bbox.
 invp=J/f'exports/native_{v}_TRAINING_NOT_FOR_FAB/inventory_after.tsv';fonts=[];param=None
 if invp.exists():
  for line in invp.read_text(encoding='utf-8').splitlines():
   if line.startswith('TEXTBLOCK\t'):
    _,idx,raw=line.split('\t',2);fonts.append(dict(index=idx,parameters=ns['attrs'](sx(raw.replace(chr(92)+'006',chr(92)*2+'006'))),nativeRaw=raw))
   if line.startswith('PARAM_DESIGN\t'):param=ns['attrs'](sx(line.split('\t',1)[1]))
  dump(J/f'audits/j57_{v}_native_textblocks_and_design_parameters.json',dict(source=str(invp),sha256=sha(invp),textBlocks=fonts,designParameters=param,coordinateContract='CSV uses unchanged world coordinates (0,0); PARAM_DESIGN.xy is drawing extent lower-left, not an instruction to subtract20mm. No machine zero offset is applied.'))
 summary[v]=dict(actualPlacedPhysicalPinRecords=len(records),electricalPins=272,mechanicalNPTH=6,nominalMaskAperturesTOP=len(mask),pasteAperturesTOP=len(paste),DNP_pasteApertures=[{k:a[k] for k in ['ref','pin','padstack','bbox']} for a in paste if a['ref'] in ['R12','R13']],maskMinimumWebMM=near[0]['NominalMaskWeb_mm'] if near else None,maskWebUnder025Count=len(near),mechanicalZoneIntersections=low,silkBBoxOnlyReviewCandidates=len(broad),actualCADCCWPinChecks=272,fontBlocksRead=len(fonts),stencilProcessApproval=False,fixtureOrPolarityApproval=False,scope='Actual embedded regular pad apertures and nominal geometry, not photoplot full-contact preprocessing or manufacturing tolerances. Rounded rectangle radius unavailable: conservative bbox. No material/MPN/placement clearance certification.')
 dump(J/f'audits/j55_{v}_mask_web_stencil_mechanical_summary_b019.json',summary[v])
dump(J/'audits/j55_57_physical_summary_b019.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
