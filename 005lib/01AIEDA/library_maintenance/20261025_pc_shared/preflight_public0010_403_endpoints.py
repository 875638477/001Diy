"""Read-only actual source wire-end stroke coverage for403 exact per-ref target choices.
Uses actual cached rectangles and independently cold-loaded target capsule/roundrect,
including relative pad rotation and actualcomponentD4pose. Never claims GetConnect.
"""
from pathlib import Path
from collections import defaultdict,Counter
from decimal import Decimal
import csv,hashlib,importlib.util,json,math
M=Path(__file__).resolve().parent;O=M/'public0010_403_endpoint_preflight13';O.mkdir(exist_ok=True);P=M/'w/public_brd0010_source_full13_v2';C=M/'w/public_brd0010_source_allcache13'
S=importlib.util.spec_from_file_location('native',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(S);S.loader.exec_module(N)
jr=N.jread;sha=N.sha
planpath=M/'public_four_module_fp_plans13_v2/0010_EXACT_FOOTPRINT_PLAN.json';plan=jr(planpath);assert len(plan['changes'])==403 and sha(plan['source_board'])==plan['source_board_sha256']
tab=lambda p:list(csv.DictReader(p.open(encoding='utf-8-sig'),delimiter='\t'))
symbols={r['refdes']:r for r in tab(P/'symbols.tsv') if r['refdes']!='nil'};actual=defaultdict(dict);selectedrefs={r['ref'] for r in plan['changes']}
for r in tab(P/'all_symbol_pins.tsv'):
 if r['refdes'] in selectedrefs:
  if r['number'] in actual[r['refdes']]:raise ValueError('Expected ordinary source unique pin numbers')
  actual[r['refdes']][r['number']]=r
needed={r['old_package'].lower() for r in plan['changes']};source={}
for r in tab(C/'manifest.tsv'):
 if r['name'].lower() in needed:source[r['name'].lower()]=N.inspect(Path(r['file']))
targets={e['stem'].lower():e for p in (M/'global_canonical_targets_review13').glob('e*_SCHEMA_GEOMETRY.json') for e in jr(p)}
binding=jr(M/'global_canonical_targets_review13/FULL_PAD_XML_BINDING.json');pads={Path(r['path']).stem.lower():r for r in binding['records']}
mats=[((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),((-1,0),(0,1)),((1,0),(0,-1)),((0,1),(1,0)),((0,-1),(-1,0))]
def mul(a,p):return(a[0][0]*p[0]+a[0][1]*p[1],a[1][0]*p[0]+a[1][1]*p[1])
def rot(p,angle):
 angle%=360
 if angle==0:return p
 if angle==90:return(-p[1],p[0])
 if angle==180:return(-p[0],-p[1])
 if angle==270:return(p[1],-p[0])
 raise ValueError('Non-D4 pin rotation')
def shape(p,target=False):
 ls=[r for r in p['pad_layers'] if r['layer']=='ETCH/TOP' and r['type']=='REGULAR' and r['figure_name'] not in ('NULL','nil')];assert len(ls)==1
 l=ls[0];assert l['offset_mm']==['0','0'];bb=[[float(v) for v in q] for q in l['bbox_mm']];hw=(bb[1][0]-bb[0][0])/2;hh=(bb[1][1]-bb[0][1])/2;cx=(bb[1][0]+bb[0][0])/2;cy=(bb[1][1]+bb[0][1])/2
 r=0.0
 if l['figure_name']=='ROUNDED_RECTANGLE':
  assert target,'Oldsource actual rectangles expected'
  xml=pads[p['pad_name'].lower()];x=[r for r in xml['geometry_mm']['copper'] if r['layer']=='BEGIN_LAYER'];assert len(x)==1 and x[0]['figure']=='ROUNDED_RECTANGLE';r=float(x[0]['corner_mm'])
 assert l['figure_name'] in {'RECTANGLE','OBLONG_X','OBLONG_Y','ROUNDED_RECTANGLE','CIRCLE'}
 return {'figure':l['figure_name'],'halfwidth':hw,'halfheight':hh,'center_x':cx,'center_y':cy,'radius':r,'pin_rotation':int(Decimal(p['local_rotation']['number']))%360,'pin_xy':list(map(float,p['local_xy_mm']))}
def distance(pt,s):
 pt=rot((pt[0]-s['pin_xy'][0],pt[1]-s['pin_xy'][1]),-s['pin_rotation']);x=abs(pt[0]-s['center_x']);y=abs(pt[1]-s['center_y']);hw,hh=s['halfwidth'],s['halfheight'];f=s['figure']
 if f in ('OBLONG_X','OBLONG_Y','CIRCLE'):
  r=min(hw,hh);return math.hypot(max(x-(hw-r),0),max(y-(hh-r),0))-r
 r=s['radius'];dx=x-(hw-r);dy=y-(hh-r);return math.hypot(max(dx,0),max(dy,0))+min(max(dx,dy),0)-r
endpoints=defaultdict(list);count=0;maxwidth=0
geometry=P/'explicit_and_boundary_geometry.tsv'
for no,line in enumerate(geometry.read_text('utf-8-sig').splitlines(),1):
 f=line.split('\t')
 if f[0] not in ('"line"','"arc"') or f[1] not in ('"ETCH/TOP"','"ETCH/BOTTOM"'):continue
 width=N.parse_many(f[5])[0]
 if not isinstance(width,Decimal) or width<=0:continue
 pair=N.parse_many(f[4])[0]
 if not isinstance(pair,list) or len(pair)!=2:continue
 maxwidth=max(maxwidth,float(width))
 for endpoint,pt in enumerate(pair):
  if not isinstance(pt,list) or len(pt)!=2 or not all(isinstance(v,Decimal) for v in pt):continue
  x,y=map(float,pt);r={'point':(x,y),'row':no,'endpoint':endpoint,'kind':f[0].strip('"'),'layer':f[1].strip('"'),'width_mm':float(width)};endpoints[(math.floor(x/2),math.floor(y/2))].append(r);count+=1
rows=[];outside=[];unsupported=[];allpinchanges=[]
for change in plan['changes']:
 ref=change['ref'];sy=symbols[ref];e=source[change['old_package'].lower()];target=targets[change['new_package'].lower()];assert e['units']=='millimeters' and e['pin_numbers']==target['pin_numbers']==['1','2']
 origin=(Decimal(sy['x']),Decimal(sy['y']));sp={p['number']:p for p in e['pins']};tp={p['number']:p for p in target['pins']};fits=[]
 for mat in mats:
  err=[]
  for n,p in sp.items():
   q=mul(mat,tuple(map(Decimal,p['local_xy_mm'])));a=actual[ref][n];err += [abs(q[i]+origin[i]-Decimal(a['x' if i==0 else 'y'])) for i in range(2)]
  if max(err)<Decimal('0.00000001'):fits.append(mat)
 assert fits,(ref,'old actual pose mismatch');mat=fits[0];inv=((mat[0][0],mat[1][0]),(mat[0][1],mat[1][1]));originf=tuple(map(float,origin));pr=[]
 # Same-numbered2pad parents are collinear; actual native rotation resolves the mirror ambiguity for off-axis route ends.
 angle=int(Decimal(sy['rotation']))%360;mirrored=sy['mirrored']=='t';rotmat={0:mats[0],90:mats[1],180:mats[2],270:mats[3]}[angle];preferred=((-rotmat[0][0],rotmat[0][1]),(-rotmat[1][0],rotmat[1][1])) if mirrored else rotmat
 if preferred in fits:mat=preferred;inv=((mat[0][0],mat[1][0]),(mat[0][1],mat[1][1]))
 for n,p in sp.items():
  oldshape=shape(p);newshape=shape(tp[n],True);a=actual[ref][n];oldworld=tuple(map(float,[a['x'],a['y']]));newloc=tp[n]['local_xy_mm'];newworld=mul(mat,tuple(map(float,newloc)));newworld=[newworld[i]+originf[i] for i in range(2)];near=[]
  oldcenterlocal=tuple(map(float,p['local_xy_mm']));centercoverage=distance(oldcenterlocal,newshape)<=1e-9
  # Neighborhood bound includes the actual widest source trace stroke, not bboxonly inclusion.
  reach=max(oldshape['halfwidth'],oldshape['halfheight'])+maxwidth/2+0.1;cells=math.ceil(reach/2)+1;bx,by=(math.floor(v/2) for v in oldworld)
  for ix in range(bx-cells,bx+cells+1):
   for iy in range(by-cells,by+cells+1):
    for ep in endpoints.get((ix,iy),[]):
     if ep['layer']!=('ETCH/BOTTOM' if mirrored else 'ETCH/TOP'):continue
     local=mul(inv,(ep['point'][0]-originf[0],ep['point'][1]-originf[1]));stroke=ep['width_mm']/2;od=distance(local,oldshape)
     if od>stroke+1e-9:continue
     nd=distance(local,newshape);covered=nd<=stroke+1e-9;item=dict(ep,source_true_pad_stroke_distance_mm=od,target_true_pad_stroke_distance_mm=nd,stroke_radius_mm=stroke,covered_by_new_pad_including_trace_halfwidth=covered);near.append(item)
     if not covered:outside.append({'ref':ref,'pin':n,'actual_pin_net':a['net'],'old_package':change['old_package'],'new_package':change['new_package'],'old_center_world_mm':oldworld,'new_center_world_mm':newworld,'candidate':item})
  pr.append({'pin':n,'net':a['net'],'old_world_mm':oldworld,'target_expected_ideal_world_mm':newworld,'world_delta_mm':[newworld[i]-oldworld[i] for i in range(2)],'old_center_inside_new_true_pad':centercoverage,'endpoint_candidates_including_stroke':near,'old_shape':oldshape,'target_shape':newshape})
  allpinchanges.append({'ref':ref,'pin':n,'net':a['net'],'old_pad':p['pad_name'],'target_pad':tp[n]['pad_name'],'old_world_mm':oldworld,'target_world_mm':newworld,'target_native':target['native_path'],'target_native_sha256':target['native_sha256']})
 rows.append({'ref':ref,'old_package':change['old_package'],'target_package':change['new_package'],'rotation_delta':0,'source_actual_rotation':sy['rotation'],'source_actual_mirror':sy['mirrored'],'source_fitted_D4':mat,'pins':pr})
assert len(rows)==403 and len(allpinchanges)==806
report={'status':'READONLY_403_ACTUAL_SOURCE_ENDPOINT_STROKE_PREFLIGHT_NOT_NATIVE_ATTACH_PROOF','source_board':plan['source_board'],'source_board_sha256':plan['source_board_sha256'],'exact_per_ref_FP_plan':str(planpath),'exact_per_ref_FP_plan_sha256':sha(planpath),'source_actual_geometry':str(geometry),'source_actual_geometry_sha256':sha(geometry),'source_actual_cache_manifest':str(C/'manifest.tsv'),'source_actual_cache_manifest_sha256':sha(C/'manifest.tsv'),'units':'mm','source_accuracy':4,'physical_refs':403,'physical_pads':806,'typed_pin_net_names_preserved':True,'true_positive_width_manual_line_arc_endpoints':count,'max_trace_width_mm':maxwidth,'candidate_endpoints_outside_new_true_pad_even_including_halfwidth':len(outside),'pins_with_outside_candidates':len({(r['ref'],r['pin']) for r in outside}),'refs_with_outside_candidates':len({r['ref'] for r in outside}),'refs_requiring_actual_attachment_probe_or_stub_planning':sorted({r['ref'] for r in outside}),'outside_candidates':outside,'rows':rows,'limitations':['Endpointtable lacksnet/DBID/parent, so candidates may be unrelated-othernet geometriccontacts. Do not addstubs blindly from this list.','Truecurrent rectangular pads and independentlycold-read targetcapsule/roundedrectangle are tested with actualrelativepadrotation, actualcomponentD4+mirror, and each actualtrace linewidth/2.','A trace can cross a pad without endpointinside. Suchbranches/shapes/vias and completeactualattachment require nativeGetConnect; center/outlineoverlap is not approval.','Current0010all806pads are electricallyactive, not a palette. Candidatepad changes require complete2698pad/915partition/nativepinattachments/text/CFX/copper preservation gates.','R205 borrowedC0603 resolvesr0603_pc; BEAD borrowedR0805 resolvesfb0805_pc via actualdevicePART_NAME plan, notsourcefilenamefamily.']}
N.dump(O/'0010_403_ENDPOINT_STROKE_PREFLIGHT.json',report);N.dump(O/'0010_403_806_EXPECTED_PIN_IDEAL_DELTAS.json',allpinchanges);print(json.dumps({k:v for k,v in report.items() if k not in ('rows','outside_candidates','limitations','refs_requiring_actual_attachment_probe_or_stub_planning')},indent=2))
