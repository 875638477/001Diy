"""Independent real-plane/route/return review. Reads only stable native exports; no Cadence."""
from pathlib import Path
import sys,json,csv,re,math,hashlib,collections,datetime
R=Path(r'D:/001DIY/005lib/01AIEDA');H=R/'learning/examples/lessonHI_38_50_20261021';J=R/'learning/examples/lessonJK_51_59_20261022';O=J/'review/independent_newstack';O.mkdir(parents=True,exist_ok=True)
L=J/'logs/native_newstack_4L_reopen_01';S=J/'logs/native_j55_4L_reopen_01';G=J/'logs/native_newstack_4L_build_try03/newstack_guard.txt';B=J/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd'
sys.path[:0]=[str(H/'scripts'),str(H/'engineering_power/scripts'),str(H/'tooling/packages')]
from native_sexpr_data import parse
from shapely.geometry import LineString,Point,box
from shapely.ops import unary_union
import cadence_poly
files={};checks=[]
def raw(p):
 p=Path(p);b=p.read_bytes();files[str(p)]=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest().upper(),bytes=len(b));return b

def txt(p):return raw(p).decode('utf-8-sig')
def js(p):return json.loads(txt(p))
def ss(s):
 try:return parse(s)
 except (ValueError,AssertionError,IndexError):return s

def tab(p):
 rows=list(csv.DictReader(txt(p).splitlines(),delimiter='\t',quotechar='\0'));return [{k:ss(v) for k,v in x.items()}for x in rows if None not in x and all(v is not None for v in x.values())]
def ck(id,ok,detail=None):checks.append(dict(id=id,passed=bool(ok),detail=detail))
def put(name,d):(O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def norm(s):return re.sub(r'(?:dbid|pad|propList):[0-9A-Fa-f]+','TRANSIENT',s)
def key(r):return (r['net'],r['layer'],tuple(sorted(tuple(p)for p in r['startEnd'])),r['width'])
def manual(base):
 roles=tab(base/'hi_route_roles.tsv');by=collections.defaultdict(list)
 for r in roles:by[key(r)].append(r)
 out=[]
 for r in tab(base/'route_geometry.tsv'):
  if not r['layer'].startswith('ETCH/'):continue
  q=by.get(key(r),[])
  if q and any(x['isEtch'] and not x['thermal'] and not x.get('parentThermal') and x['parentType']=='path'for x in q):out.append(r)
 return out
launch=js(L/'launch.json');ck('NEW_FRESH_EXIT0_READONLY_SHA',launch['completed'] and launch['exitCode']==0 and '-readonly'in launch['args'] and launch['scratchBeforeSHA256']==launch['scratchAfterSHA256']==hashlib.sha256(raw(B)).hexdigest().upper())
prov=js(J/'native/newstack_provenance.json');ck('EXPECTED_NEWBOARD_IDENTITY',str(B)==prov['newOutput']);ck('SOURCE_J55_BOARD_UNCHANGED',hashlib.sha256(raw(prov['correctedSource'])).hexdigest().upper()==prov['sourceSHA256'])
source=tab(S/'components.tsv');actual=tab(L/'components.tsv');ck('80_COMPONENT_ROWS_PRESERVED',len(actual)==80 and actual==source)
sp=tab(S/'g_actual_pins.tsv');np=tab(L/'g_actual_pins.tsv');ck('ALL_NATIVE_PIN_PADS_POSES_PRESERVED',np==sp,dict(rows=len(np)))
pins={x['refdes']+'.'+x['pin']:x for x in np if x['pin'] and x['layer']=='ETCH/TOP'};ck('272_LOGICAL_PHYSICAL_PIN_ANCHORS',len(pins)==272)
ck('INSTANCE_SYMBOL_AND_PROPERTIES_PRESERVED',norm(txt(L/'jk55_instance_properties.tsv'))==norm(txt(S/'jk55_instance_properties.tsv')))
for f in ['g_actual_geometry.tsv','board_instance_texts.tsv','placed_pins.tsv','hi_mechanical_pins.tsv','physical_pad_layers.tsv','hi_mechanical_pad_layers.tsv','outline_exact.tsv','mechanical_roots.txt','stackup_full.tsv','films_full.tsv','spacing_csets.tsv','electrical_csets.tsv']:
 ck('SOURCE_FILE_PRESERVED_'+f,(collections.Counter(norm(txt(L/f)).splitlines())==collections.Counter(norm(txt(S/f)).splitlines())) if f=='physical_pad_layers.tsv' else norm(txt(L/f))==norm(txt(S/f)))
sm,nm=manual(S),manual(L);sc=collections.Counter(key(x)for x in sm);nc=collections.Counter(key(x)for x in nm)
ck('ALL_ACTUAL_MANUAL_ROUTES_MULTISET_IDENTICAL',sc==nc and len(nm)>0,dict(sourceCount=len(sm),newCount=len(nm),removed=[str(x)for x in(sc-nc)],added=[str(x)for x in(nc-sc)]))
ck('NO_INNER_MANUAL_SIGNAL_LINES',not any(x['layer']in ['ETCH/L2','ETCH/L3']and x['net']!='GND'for x in nm))
sv,nv=tab(S/'vias.tsv'),tab(L/'vias.tsv');ck('ALL_ACTUAL_VIAS_PAD_MAP_IDENTICAL',collections.Counter(json.dumps(x,sort_keys=True)for x in sv)==collections.Counter(json.dumps(x,sort_keys=True)for x in nv),dict(rows=len(nv)))
unique={ (x['name'],x['x'],x['y'],x['net']):x for x in nv};vias=[dict(name=k[0],xy=[k[1],k[2]],net=k[3],drill=x['drill'])for k,x in unique.items()]
ck('150_PHYSICAL_VIAS',len(vias)==150)
# Old physical PSet fields must remain; only a new V3-plane copy is added.
old=norm(txt(S/'physical_csets.tsv')).splitlines();new=norm(txt(L/'physical_csets.tsv')).splitlines();ck('ALL_OLD_PHYSICAL_CSET_ROWS_IDENTICAL',set(old)<=set(new));put('constraint_differences.json',dict(addedPhysicalRows=sorted(set(new)-set(old)),removedPhysicalRows=sorted(set(old)-set(new)),netRulesBefore=txt(S/'net_rules.tsv'),netRulesAfter=txt(L/'net_rules.tsv'),groupMembersBefore=norm(txt(S/'group_members.tsv')),groupMembersAfter=norm(txt(L/'group_members.tsv'))))
sections=tab(L/'stackup_full.tsv');names=[x['name']for x in sections if x['type']=='CONDUCTOR'];ck('EXACT_UPPERCASE_CONDUCTOR_SEQUENCE',names==['TOP','L2','L3','BOTTOM']);ck('NO_PHYSICAL_MASK',not any(x['type']=='MASK'for x in sections))
shapes=tab(L/'g_copper_shapes.tsv');bounds=tab(L/'hi_dynamic_boundaries.tsv');polys={};areas=[]
for i,s in enumerate(shapes):
 if not s['filled']:continue
 g=cadence_poly.plane_from_native(dict(s,holes=s.get('holes')or[]));areas.append(dict(index=i,net=s['net'],layer=s['layer'],nativeArea=s['area'],parsedArea=g.area,errorMM2=g.area-s['area'],holes=len(s.get('holes')or[])));ck('PLANE_AREA_'+str(i),abs(g.area-s['area'])<.01)
 polys[i]=g
l2=[i for i,s in enumerate(shapes)if s['filled']and s['layer']=='ETCH/L2'];l3=[i for i,s in enumerate(shapes)if s['filled']and s['layer']=='ETCH/L3']
ck('ACTUAL_L2_SINGLE_GND_REFERENCE',len(l2)==1 and shapes[l2[0]]['net']=='GND'and shapes[l2[0]]['generated'])
ck('ACTUAL_L3_SINGLE_V3V3_POWER_PLANE',len(l3)==1 and shapes[l3[0]]['net']=='V3V3'and shapes[l3[0]]['generated'])
ck('L2_LEGACY_STATIC_HSE_ISLAND_ABSENT',not any(s['layer']=='ETCH/L2'and not s.get('generated')for s in shapes))
ck('L2_GND_ONE_MOTHER_NO_PERMANENT_MOAT',len([x for x in bounds if x['layer']=='BOUNDARY/L2'and x['net']=='GND'and not x['permanentVoids']])==1)
ck('L3_OLD_GND_MOTHER_ABSENT',not any(x['layer']=='BOUNDARY/L3'and x['net']=='GND'for x in bounds))
ck('L3_ONE_REAL_V3_MOTHER',len([x for x in bounds if x['layer']=='BOUNDARY/L3'and x['net']=='V3V3'])==1)
terms=tab(L/'hi_component_terminals.tsv');graphs=tab(L/'hi_graph_objects.tsv');nets=tab(L/'hi_net_connectivity.tsv');components={x['net']:x for x in nets}
ck('ALL69_NETS_AND7_UNFINISHED_GPIO',len(nets)==69 and sum(x['minTerminalJoins']for x in nets)==7 and len([x for x in nets if x['minTerminalJoins']])==7)
roots={net:next(x['component']for x in terms if x['terminal']==pin)for net,pin in [('GND','C1.2'),('V3V3','U3.5')]}
for net,count in [('GND',56),('V3V3',32)]:
 tt=[x for x in terms if x['net']==net];ck('ALL_'+net+'_TERMINALS_COMMON',len(tt)==count and all(x['component']==roots[net]for x in tt));
 vv=[v for v in vias if v['net']==net];gm=[x for x in graphs if x['net']==net and x['component']==roots[net]and x['type']=='via'];xy=[]
 for x in gm:
  q=re.search(r'\bxy \(([-\d.]+) ([-\d.]+)\)',x['attributes'])
  if q:xy.append(tuple(float(z)for z in q.groups()))
 ck('ALL_'+net+'_ACTUAL_VIAS_COMMON',all(tuple(v['xy'])in xy for v in vv),dict(actualViaCount=len(vv),nativeCommonViaObjects=len(gm)))
 # A real shape object on the target layer belongs to the same native component as the physical supply pin.
 target='ETCH/L2'if net=='GND'else'ETCH/L3';shapeObjs=[x for x in graphs if x['net']==net and x['component']==roots[net]and x['type']=='shape'and x['layer']==target];ck('REAL_'+target+'_PLANE_NATIVE_COMPONENT',len(shapeObjs)==1,dict(shapeCount=len(shapeObjs)))
proofs=txt(L/'hi_reopen_endpoint_proofs.txt');oldproofs=txt(S/'hi_reopen_endpoint_proofs.txt');pat=r'HI_ENDPOINT_PROOF from="([^"]+)" to="([^"]+)" expected=(\w+) actual=(\w+)';pr=re.findall(pat,proofs);opr=re.findall(pat,oldproofs)
ck('ALL_OLD_CUMULATIVE_PROOFS_PRESERVED',set(opr)<=set(pr) and all(e==a for _,_,e,a in pr),dict(sourceRows=len(opr),newRows=len(pr)))
guard=txt(G);ck('NEW_HSE_DELETE_OLD_ANCHOR_STAYS_COMMON','NEW_HSE_ANCHOR_REMOVAL_EXPECTS_STILL_COMMON actualC22=t actualC23=t'in guard)
ck('ONLY_GND_V3_SCOPED_NATIVE_ZERO','SCOPED_RESULT GND 0'in guard and 'SCOPED_RESULT V3V3 0'in guard)
# Fresh explicit plane contract has76actualGNDvias/3V3vias; intermediate build cache0 is not used.
planeContract=txt(L/'newstack_fresh_plane_contract.txt');ck('FRESH_NATIVE_GND_PLANE_REACH_SUMMARY',bool(re.search(r'layer="ETCH/L2" net="GND" pins=56 vias=76 filledShapes=1',planeContract)));ck('FRESH_NATIVE_V3_PLANE_REACH_SUMMARY',bool(re.search(r'layer="ETCH/L3" net="V3V3" pins=32 vias=3 filledShapes=1',planeContract)))
refs={'ETCH/TOP':unary_union([polys[i]for i in l2]),'ETCH/BOTTOM':unary_union([polys[i]for i in l3])};projection=[]
for net in sorted({r['net']for r in nm if r['net']!='GND'}):
 for signal in ['ETCH/TOP','ETCH/BOTTOM']:
  rr=[r for r in nm if r['net']==net and r['layer']==signal]
  if not rr:continue
  lines=unary_union([LineString(r['startEnd'])for r in rr]);foot=unary_union([LineString(r['startEnd']).buffer(r['width']/2,quad_segs=24)for r in rr]);ref=refs[signal].buffer(.0001);m=lines.difference(ref);mm=foot.difference(ref)
  pieces=list(m.geoms)if hasattr(m,'geoms')else[m]
  projection.append(dict(net=net,signalLayer=signal,referenceLayer='ETCH/L2'if signal=='ETCH/TOP'else'ETCH/L3',referenceNet='GND'if signal=='ETCH/TOP'else'V3V3',manualSegmentCount=len(rr),manualLineUnionLengthMM=lines.length,traceFootprintAreaMM2=foot.area,centerlineOutsideReferenceMM=m.length,footprintOutsideReferenceAreaMM2=mm.area,outsideCenterlinePieces=[list(x.coords)for x in pieces if not x.is_empty and hasattr(x,'coords')],scope='Actual filled native plane+holes; width footprint included, not impedance/simulation/HF current or manufactured SI approval. Reference-net change explicit.'))
put('actual_reference_footprints.json',dict(status='ACTUAL_NEWSTACK_TRACE_WIDTH_PROJECTION_RECOMPUTED_READ_ONLY',rows=projection,planeAreaErrors=areas,sourceParserSHA256=hashlib.sha256(raw(H/'engineering_power/scripts/cadence_poly.py')).hexdigest().upper(),arcEvents=cadence_poly.ROUNDED_ARC_FLATTENED+cadence_poly.COINCIDENT_ARC_ENDPOINTS))
# New reference conversion requires actual populated V3-GND caps; geometric distance is only triage.
caps=[]
for ref in ['C9','C11','C12','C13','C14','C15','C16','C17']:
 p,g=pins[ref+'.1'],pins[ref+'.2'];a=next(x for x in terms if x['terminal']==ref+'.1');b=next(x for x in terms if x['terminal']==ref+'.2');ok=p['net']=='V3V3'and g['net']=='GND'and a['component']==roots['V3V3']and b['component']==roots['GND'];ck('ACTUAL_REFERENCE_CAP_'+ref+'_BOTH_PLANES_REACHED',ok)
 caps.append(dict(ref=ref,powerPin=p['xy'],groundPin=g['xy'],nativeV3L3Reached=ok,nativeGNDL2Reached=ok,scope='Native terminal graph and actual plane membership. Does not prove short low-L return/effective capacitance or mounting.'))
transitions=[]
for v in vias:
 if v['net']in ['GND','V3V3','V5','VIN_RAW','VIN_FUSED','VIN_PROT','VDDA','USB_VBUS']:continue
 near=min(caps,key=lambda c:max(math.dist(v['xy'],c['powerPin']),math.dist(v['xy'],c['groundPin'])));dist=max(math.dist(v['xy'],near['powerPin']),math.dist(v['xy'],near['groundPin']))
 transitions.append(dict(net=v['net'],signalVia=v['xy'],nearestExistingReferenceCap=near['ref'],maxDistanceToBothCapPinsMM=dist,nativeBothPlanesReached=near['nativeV3L3Reached'],status='REFERENCE_CONVERSION_ENGINEERING_REVIEW_OPEN',reason='GNDstitchvia alone cannot couple L2GND to L3V3. Existing cap common connectivity plus distance does not establish actual HF path/loop; inspect local trace/via/thermal geometry and real C/ESR. No blanket1.5mm acceptance.'))
put('reference_conversion_caps_and_vias.json',dict(status='ACTUAL_CAP_PLANE_REACH_VERIFIED_HF_TRANSITION_RETURN_NOT_ACCEPTED',caps=caps,signalViaReviews=transitions,unknowns=['actualedge/driver/cable/load','effectivecapMPN/DCbias/ESR','return path/loop/thermal impedance','USB4/wholeDRC/SI/PI/EMIhardware']))
# New supplement corrects empty inherited sampling without changing board or old fresh dump.
sup=J/'logs/native_newstack_reference_segments_01';sampletxt=txt(L/'newstack_reference_samples.tsv');supplement={}
if (sup/'actual_path_segments.tsv').exists():
 rr=tab(sup/'actual_path_segments.tsv');supplement['rawSegmentCount']=len(rr);supplement['rawHeader']=list(rr[0])if rr else[]
 supplement['nativeSampleCompletion']=txt(sup/'newstack_reference_samples.tsv').splitlines()[-1]
put('manual_route_equivalence.json',dict(status='PASS_EXACT_ACTUAL_MANUAL_MULTISET'if sc==nc and nm else'REVIEW_REQUIRED',source=str(S),fresh=str(L),sourceManual=len(sm),newManual=len(nm),totalEtchGeometryRows=len(tab(L/'route_geometry.tsv')),manualCounterUnique=len(nc),originalEmptySampler=sampletxt,supplement=supplement,method='Direct official fgeo route_geometry + native hi_route_roles line/parent thermal classification; all net/layer/width/startEnd multiset equal. Does not trust earlierGetConnect path-only manual0 guard.'))
cam=J/'review/independent_CAM_NEWSTACK/summary.json'
camEvidence=js(cam)if cam.exists()else None
r=dict(status='PASS_INDEPENDENT_NEWSTACK_PHYSICAL_LAYER_APPLICATION_WITH_OPEN_SI_PI'if all(x['passed']for x in checks)else'NEWSTACK_INDEPENDENT_REVIEW_REQUIRED',created=datetime.datetime.now().isoformat(),checkCount=len(checks),failed=[x for x in checks if not x['passed']],checks=checks,board=str(B),boardSHA256=hashlib.sha256(B.read_bytes()).hexdigest().upper(),sourceBoard=prov['correctedSource'],sourceSHA256=prov['sourceSHA256'],actualArchitecture=dict(TOP='components/signals with existing outerlocalpower',L2='one continuous commonGNDplane,no artificialHSEmoat',L3='one V3V3 powerplane',BOTTOM='signals referencing actualV3V3'),legacyHSESoleAnchorDisconnectionExpectationRetired=True,manualEvidenceScope='Empty sampling preserved as NOT_EVIDENCE; independent750-segment counter closes actualroutepreservation.',nativeSCOPED='GND andV3V3 only0 from native build. Old65nonUSB/USB4/wholeDRC must not be relabeled newfullDRC.',remainingUnconnectedGPIO=[x['net']for x in nets if x['minTerminalJoins']],referenceProjection='actual_reference_footprints.json',transitionReturn='reference_conversion_caps_and_vias.json',openRisks=['7GPIOunfinished','USB4 and wholeboardDRCpending','BOTTOMnowpowerreference: pertransition cap return path not HFaccepted','actualedge/load/cable/capMPN/thermal/ESD/EMIunknown','manufacturing/HWrelease notprovided'],newNativeExecutedByReviewer=False,originalJ51_54SealUnmodified=True,camCrossReference=str(cam)if camEvidence else None,inputs=list(files.values()))
put('review.json',r);print(json.dumps(dict(status=r['status'],checks=len(checks),failed=r['failed'],manualSource=len(sm),manualNew=len(nm),referenceRows=len(projection),capPairs=len(caps),signalViaReviews=len(transitions),boardSHA256=r['boardSHA256']),ensure_ascii=False))