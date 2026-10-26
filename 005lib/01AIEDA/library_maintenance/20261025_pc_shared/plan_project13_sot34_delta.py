"""Read-only SOT34 exact local transforms and conservative old-etch-endpoint shape coverage."""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal,localcontext
import csv,json,hashlib,importlib.util,sys
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');P=R/'w/final_alt13';OUT=M/'global_canonical_publish_v1';B=R.parent/'cadence_geometry_merge_20261025';sys.path.insert(0,str(B));from sexpr import parse_many,attrs,Atom
D=Decimal;F=D('.0254');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def uq(x):return x[1:-1] if x.startswith('"') and x.endswith('"') else x
def tab(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return [{k:uq(v) for k,v in r.items()} for r in csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE)]
def readnodes(p):
 rows=parse_many(p.read_text(encoding='utf-8-sig'));return {str(r[1]):attrs(r[2]) for r in rows if r[0]=='object'}
def inside_old(v):
 x,y=map(abs,v);return x*x+max(y-D(3),D(0))**2<=D('19.5')**2
# Target true rounded rectangle, NOTbbox-only. Units below are millimeters.
def inside_target(v):
 x,y=map(abs,v);hw,hh,r=D('.45'),D('.6'),D('.2')
 return x<=hw and y<=hh and max(x-(hw-r),D(0))**2+max(y-(hh-r),D(0))**2<=r*r
source=P/'def_0012.sexp';sn=readnodes(source);selected=next(a for a in sn.values() if a.get('objType')=='symdef');sp={str(sn[str(i)]['number']):sn[str(i)]['relxy'] for i in selected['pins']}
traw=M/'global_suffix_native_v3/e00939/output/0000.sexp';tn=readnodes(traw);ts=next(a for a in tn.values() if a.get('objType')=='symdef');tp={str(tn[str(i)]['number']):tn[str(i)]['relxy'] for i in ts['pins']}
assert set(sp)==set(tp)=={'1','2','3'}
sy=[r for r in tab(P/'symbols.tsv') if r['symbol_name'].lower()=='sot23_123'];pins=tab(P/'all_symbol_pins.tsv');byref=defaultdict(dict)
for p in pins:
 if p['symbol_name'].lower()=='sot23_123':byref[p['refdes']][p['number']]=p
mats=[((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),((-1,0),(0,1)),((1,0),(0,-1)),((0,1),(1,0)),((0,-1),(-1,0))]
def mult(a,p):return [D(a[0][0])*p[0]+D(a[0][1])*p[1],D(a[1][0])*p[0]+D(a[1][1])*p[1]]
endpoints=defaultdict(list);n=0
for no,l in enumerate((P/'explicit_and_boundary_geometry.tsv').read_text(encoding='utf-8-sig').splitlines(),1):
 f=l.split('\t')
 if f[0] not in ('"line"','"arc"') or not uq(f[1]).startswith('ETCH/'):continue
 pair=parse_many(f[4])[0]
 if not isinstance(pair,list) or len(pair)!=2:continue
 for end,point in enumerate(pair):
  if not isinstance(point,list) or len(point)!=2 or not all(isinstance(v,D) for v in point):continue
  endpoints[(int(point[0]//100),int(point[1]//100))].append({'point':point,'row':no,'endpoint':end,'kind':uq(f[0]),'layer':uq(f[1]),'width':str(parse_many(f[5])[0])});n+=1
result=[];outside=[];allcenter=0
for s in sy:
 ref=s['refdes'];origin=[D(s['x']),D(s['y'])];actual=byref[ref];fits=[]
 for a in mats:
  err=max(abs(D(actual[num][axis])-origin[k]-mult(a,sp[num])[k]) for num in sp for k,axis in enumerate(('x','y')))
  if err<=D('.000001'):fits.append((a,err))
 assert len(fits)==1,(ref,fits)
 a,err=fits[0];inv=((a[0][0],a[1][0]),(a[0][1],a[1][1]));pr=[]
 for number,oldp in sorted(sp.items()):
  newp=tp[number];worldoffset=mult(a,[v/F for v in newp]);newworld=[origin[k]+worldoffset[k] for k in range(2)];oldworld=[D(actual[number]['x']),D(actual[number]['y'])];oldcenterlocalmm=[oldp[k]*F-newp[k] for k in range(2)];centercovered=inside_target(oldcenterlocalmm);allcenter+=centercovered
  ox,oy=oldworld;near=[]
  for ix in range(int(ox//100)-1,int(ox//100)+2):
   for iy in range(int(oy//100)-1,int(oy//100)+2):
    for ep in endpoints.get((ix,iy),[]):
     local=mult(inv,[ep['point'][k]-origin[k] for k in range(2)]);oldrelative=[local[k]-oldp[k] for k in range(2)]
     if not inside_old(oldrelative):continue
     newrelative=[local[k]*F-newp[k] for k in range(2)];covered=inside_target(newrelative);r={**ep,'point':[str(v) for v in ep['point']],'old_pad_local_mils':[str(v) for v in oldrelative],'new_pad_local_mm':[str(v) for v in newrelative],'inside_new_rounded_rectangle':covered};near.append(r)
     if not covered:outside.append({'ref':ref,'pin':number,'net':actual[number]['net'],'candidate':r})
  pr.append({'number':number,'net':actual[number]['net'],'source_local_mils':[str(v) for v in oldp],'source_local_mm':[str(v*F) for v in oldp],'target_local_mm':[str(v) for v in newp],'delta_local_mm':[str(newp[k]-oldp[k]*F) for k in range(2)],'source_world_mils':[str(v) for v in oldworld],'target_ideal_world_mils':[str(v) for v in newworld],'delta_world_mils':[str(newworld[k]-oldworld[k]) for k in range(2)],'old_pin_center_inside_new_pad':centercovered,'old_pad_geometric_etch_endpoint_candidates':near})
 result.append({'ref':ref,'origin_mils':[str(v) for v in origin],'rotation':s['rotation'],'mirrored':s['mirrored'],'exact_fitted_D4_matrix':a,'source_pose_fit_max_error_mils':str(err),'recommended_rotation_change_degrees':'0','recommended_origin_change_mils':['0','0'],'pins':pr})
report={'status':'READONLY_SOURCE34_POSE_AND_REAL_PAD_SHAPE_ENDPOINT_PREFLIGHT_NOT_NATIVE_CONNECTION_APPROVAL','source_board':str(R/'w/via_alt13/PC13_FINAL.brd'),'source_board_sha256':sha(R/'w/via_alt13/PC13_FINAL.brd'),'source_cached_definition':str(source),'source_cached_definition_sha256':sha(source),'target_generic_native':str(traw),'target_generic_native_sha256':sha(traw),'source_geometry':str(P/'explicit_and_boundary_geometry.tsv'),'source_geometry_sha256':sha(P/'explicit_and_boundary_geometry.tsv'),'component_count':len(sy),'pin_count':sum(len(r['pins']) for r in result),'old_centers_inside_new_pad':allcenter,'manual_etch_line_arc_endpoints_scanned':n,'old_pad_candidate_endpoints_outside_new_pad':outside,'rows':result,'limits':['Every oldpin center fits true new rounded rectangle, but old pad is not fully covered by new pad.','Endpoint candidates are actual frozen geometry lines/arcs inside oldpill shape; snapshot omits net/DBID/parent, so candidates may include unrelated-net or shape-boundary endpoints. They are not proof of actual electrical attachment.','Target ideal coordinates use complete generic pad metrics; mils2 board loading quantizes native values. Root must capture actual newpad world shapes/pins after AltSymbolReplace.','Use unchanged componentpose and pin labels1/2/3, then native GetConnect source/target partition proof. Add only approved own-net stubs when required; do not infer connection from overlap.','This frozen49AF snapshot precedes copper-only followups; root final candidate must be bound and independently validated.','NativePST plus exactly34 CapturePCBFootprint overrides and exactly34 actualPCB symbol replacements need full second13 verification before releasing.']}
(OUT/'PROJECT13_SOT34_DELTA_PREFLIGHT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('rows','old_pad_candidate_endpoints_outside_new_pad','limits')},ensure_ascii=False));print('outsidecandidate_count',len(outside));print(json.dumps(outside[:8],ensure_ascii=False,indent=2))
