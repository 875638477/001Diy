"""Freeze actual own-net source endpoints; prepare one owned batch repair."""
from pathlib import Path
from decimal import Decimal as D
import sys,json,csv,hashlib,collections
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');W=R/'w/pcb_migration/sot34_migration'
sys.path.insert(0,str(M));from inspect_sot34_neighbors import parse
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'));from sexpr import Atom
source=parse(R/'w/sot34_source_adjacency2/SOT34_pin_adjacency.ilist');target=parse(R/'w/sot34_target_adjacency2/SOT34_pin_adjacency.ilist')
delta=json.loads((M/'sot34_superset_pst_and_pins_v1/SOT34_102_EXPECTED_CHANGES.json').read_text());bydelta={(x['ref'],x['pin']):x for x in delta}
pre=json.loads((M/'global_canonical_publish_v1/PROJECT13_SOT34_DELTA_PREFLIGHT.json').read_text());poses={r['ref']:r for r in pre['rows']}
def groupmap(path):
 with path.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
 g=collections.defaultdict(set);keys={}
 for r in rows:
  # Numbered pins are unique; unnamed mechanical pads retain physical XY.
  k=(r['refdes'],r['pin']) if r['pin'] else (r['refdes'],r['pin'],r['x'],r['y'])
  g[r['group']].add(k);keys[k]=r['group']
 return {k:g[v] for k,v in keys.items()}
sg=groupmap(R/'w/final_alt13/native_copper_pin_groups.tsv');tg=groupmap(R/'w/sot34_full2/native_copper_pin_groups.tsv')
def neteq(a,b):return type(a)==type(b) and a==b
def inv(ref,v):
 a=poses[ref]['exact_fitted_D4_matrix'];return [D(a[0][0])*v[0]+D(a[1][0])*v[1],D(a[0][1])*v[0]+D(a[1][1])*v[1]]
def inner_new(ref,point,new,width):
 x,y=map(abs,inv(ref,[(point[k]-new[k])*D('.0254') for k in range(2)]));r=D('.2')-width*D('.0254')/2;hw=D('.45')-width*D('.0254')/2;hh=D('.6')-width*D('.0254')/2
 return r>0 and x<=hw and y<=hh and max(x-(hw-r),D(0))**2+max(y-(hh-r),D(0))**2<=r*r
def inside_old(ref,point,old):
 x,y=map(abs,inv(ref,[point[k]-old[k] for k in range(2)]));return x*x+max(y-D(3),D(0))**2<=D('19.5')**2
def q(s):return json.dumps(str(s))
def xy(p):return '('+' '.join(str(x) for x in p)+')'
rows=[];decisions=[]
for key,sr in source.items():
 ref,pin=key;tr=target[key];sp=next(x for x in sr if x[0]=='TARGET');tp=next(x for x in tr if x[0]=='TARGET');old=sp[6];new=tp[6];net=sp[3]
 expectednew=[D(bydelta[key]['after']['expected_x']),D(bydelta[key]['after']['expected_y'])]
 assert neteq(net,tp[3]) and all(abs(new[k]-expectednew[k])<D('1e-8') for k in range(2))
 # Native full2 has already checked literal expected coordinates. Its %L
 # diagnostic may print the derived float 1e-10 away from that mil2 value.
 new=expectednew
 paths=[x for x in sr if x[0]=='DIRECT_NEIGHBOR' and x[2] in ('path','cline','line','arc')];shapes=[x for x in sr if x[0]=='DIRECT_NEIGHBOR' and x[2]=='shape']
 targetpaths=[x for x in tr if x[0]=='DIRECT_NEIGHBOR' and x[2] in ('path','cline','line','arc')]
 changed=sg[key]!=tg[key]
 if not paths:
  decisions.append(dict(ref=ref,pin=pin,action='SKIP_NO_SOURCE_PATH',source_shapes=len(shapes),source_group_changed=changed));assert not changed,(key,'source shape-only changed needs explicit native analysis');continue
 # Only pins losing a native path or a physical pin partition need a stub.
 if not changed and len(targetpaths)>=len(paths):
  decisions.append(dict(ref=ref,pin=pin,action='SKIP_NATIVE_PATH_AND_GROUP_PRESERVED'));continue
 assert not isinstance(net,Atom) and net!='','Do not manufacture copper for native NIL/blank NC'
 candidates=[]
 for seg in sr:
  if seg[0] not in ('DIRECT_PATH_SEGMENT','DIRECT_NEIGHBOR') or seg[2] not in ('line','arc'):continue
  if not neteq(seg[3],net) or str(seg[7]) not in ('ETCH/TOP','ETCH/BOTTOM'):continue
  if not isinstance(seg[8],list) or len(seg[8])!=2 or not isinstance(seg[9],D) or seg[9]<=0:continue
  width=min(D(5),seg[9])
  for point in seg[8]:
   if not isinstance(point,list) or len(point)!=2:continue
   if not inside_old(ref,point,old) or not inner_new(ref,point,new,width):continue
   candidates.append((point!=old,sum((point[k]-new[k])**2 for k in range(2)),seg,point,width))
 assert candidates,(key,'No actual same-net source endpoint fitting whole5mil stub')
 _,_,seg,point,width=min(candidates,key=lambda v:(v[0],v[1]))
 rows.append((ref,pin,net,seg[7],seg[2],seg[9],seg[8],point,new,width,old))
 decisions.append(dict(ref=ref,pin=pin,action='RESTORE_SOURCE_PATH_WITH_INTERNAL_STUB',source_direct_paths=len(paths),target_direct_paths=len(targetpaths),source_group_changed=changed,start=[str(x) for x in point],old_pin_center=[str(x) for x in old],target_center=[str(x) for x in new],layer=str(seg[7]),original_width=str(seg[9]),stub_width=str(width)))
assert rows
plan=W/'SOT34_SOURCE_PATH_STUBS.ilist';assert not plan.exists()
plan.write_text('\n'.join('('+' '.join([q(ref),q(pin),q(net),q(layer),q(kind),str(sw),'('+xy(se[0])+' '+xy(se[1])+')',xy(point),xy(new),str(width),xy(old)])+')' for ref,pin,net,layer,kind,sw,se,point,new,width,old in rows)+'\n',encoding='utf-8')
receipt=W/'SOT34_SOURCE_PATH_STUBS.json';assert not receipt.exists();receipt.write_text(json.dumps(dict(status='PREPARED_NOT_RUN',input_board_sha256='5003D5D4DD76314540ABD9B2BB247ED813814621259E9EF820AC9C0E5421E48B',source_board_sha256='49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063',planned_stubs=len(rows),decisions=decisions),indent=2),encoding='utf-8')
s='''load("'''+str(W/'sot34_native_migration.il').replace('\\','/')+'''")
load("'''+str(W.parent/'pc13_native_changed_rings_v10.il').replace('\\','/')+'''")
procedure(pc13SotStubPin(ref num)
 let((c) c=pc13Comp(ref) car(setof(p c->symbol->pins equal(p->number num)))))
procedure(pc13SotStubWalk(o)
 let((attrs)
  when(o && !pc13StubSeen[o]
   pc13StubSeen[o]=t
   when(member(o->objType '("line" "arc")) pc13StubSegments=cons(list(o->objType o->net->name o->layer o->width o->startEnd) pc13StubSegments))
   attrs=o->? when(member('children attrs) foreach(x o->children pc13SotStubWalk(x)))
   when(member('segments attrs) foreach(x o->segments pc13SotStubWalk(x))))))
procedure(pc13SotStubValidate(row)
 let((pin path poly pad outside matching)
  pin=pc13SotStubPin(car(row) cadr(row))
  unless(pin && equal(pin->xy nth(8 row)) && equal(pin->net->name nth(2 row)) && equal(pin->name "PAD_36_47") error("SOT stub target pin guard failed %L\\n" row))
  matching=setof(x pc13StubSegments equal(car(x) nth(4 row)) && equal(nth(1 x) nth(2 row)) && equal(nth(2 x) nth(3 row)) && equal(nth(3 x) nth(5 row)) && (equal(nth(4 x) nth(6 row)) || equal(nth(4 x) reverse(nth(6 row)))))
  unless(matching error("SOT original own-net route segment missing %L\\n" row))
  path=axlPathStart(list(nth(7 row) nth(8 row)) nth(9 row))
  poly=axlPolyFromDB(path ?line2poly t ?endCapType 'ROUND)
  when(axlPolyErrorGet() error("SOT stub stroke native polygon failed\\n"))
  poly=remove(nil poly) unless(poly error("SOT stub has no actual stroke\\n"))
  pad=axlPolyFromDB(pin ?layer nth(3 row) ?padType 'REGULAR ?holes t)
  when(axlPolyErrorGet() error("SOT actual targetpad polygon failed\\n"))
  pad=remove(nil pad) unless(pad error("SOT actual targetpad missing\\n"))
  outside=pc13RingOp(poly pad 'ANDNOT)
  when(outside error("SOT entire stub stroke exceeds actual newpad %L\\n" row)) t))
procedure(pc13SotCreateStubs(rows f)
 let((pin path result before after count)
  count=0
  foreach(row rows
   axlDBRefreshId(nil) pin=pc13SotStubPin(car(row) cadr(row)) before=length(axlDBGetConnect(pin t))
   path=axlPathStart(list(nth(7 row) nth(8 row)) nth(9 row))
   result=axlDBCreatePath(path nth(3 row) nth(2 row)) unless(result error("SOT stub creation failed %L\\n" row))
   axlDBRefreshId(nil) pin=pc13SotStubPin(car(row) cadr(row)) after=length(axlDBGetConnect(pin t))
   unless(after>0 error("SOT repaired pin still has no native neighbors %L\\n" row))
   count=count+1 fprintf(f "%s\\t%s\\t%s\\t%s\\t%L\\t%L\\t%L\\t%d\\t%d\\n" car(row) cadr(row) nth(2 row) nth(3 row) nth(7 row) nth(8 row) nth(9 row) before after) drain(f)) count))
procedure(pc13Sot34RepairStubs(dir)
 let((f row rows textSnapshot poseSnapshot propSnapshot oldDrc count pc13StubSeen pc13StubSegments)
  sstatus(fullPrecision t)
  unless(equal(axlDBGetDesignUnits() '("mils" 2)) error("SOT stub expects original mils2\\n"))
  pc13LoadExpected("'''+str(W/'EXPECTED_PINS_SOT34.ilist').replace('\\','/')+'''")
  foreach(c axlDBGetDesign()->components pc13ExpectedPins(c->name c->symbol))
  textSnapshot=makeTable('pc13SotText nil) poseSnapshot=makeTable('pc13SotPose nil) propSnapshot=makeTable('pc13SotProps nil)
  foreach(c axlDBGetDesign()->components textSnapshot[c->name]=pc13TextSorted(c->symbol) poseSnapshot[c->name]=pc13Pose(c->symbol) propSnapshot[c->name]=pc13Props(c->compdef))
  oldDrc=axlDBControl('drcEnable) pc13StubSeen=makeTable('pc13StubSeen nil) pc13StubSegments=nil
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13SotStubWalk(b)))
  f=infile("'''+str(plan).replace('\\','/')+'''") rows=nil while(row=lineread(f) rows=cons(car(row) rows)) close(f) rows=reverse(rows)
  unless(length(rows)=='''+str(len(rows))+''' error("SOT frozen stub row count failed\\n"))
  foreach(row rows pc13SotStubValidate(row))
  f=outfile(strcat(dir "/SOT34_STUB_APPLIED.tsv")) fprintf(f "refdes\\tpin\\tnet\\tlayer\\told_endpoint\\tnew_pin_center\\twidth\\tbefore_neighbors\\tafter_neighbors\\n")
  count=axlDBCloak('pc13SotCreateStubs(rows f) 'shape) close(f)
  unless(count==length(rows) error("SOT stub batch incomplete\\n"))
  axlDBRefreshId(nil)
  foreach(c axlDBGetDesign()->components
   pc13ExpectedPins(c->name c->symbol)
   unless(equal(textSnapshot[c->name] pc13TextSorted(c->symbol)) && equal(poseSnapshot[c->name] pc13Pose(c->symbol)) && equal(propSnapshot[c->name] pc13Props(c->compdef)) error("SOT text/pose/props changed\\n")))
  unless(equal(oldDrc axlDBControl('drcEnable)) error("SOT source DRC mode changed\\n"))
  unless(axlSaveDesign(?design strcat(dir "/SOT34_ATTACHED.brd") ?noMru t ?noConfirm t) error("SOT repaired candidate save failed\\n"))
  f=outfile(strcat(dir "/SOT34_STUB_COMPLETE.txt")) fprintf(f "SOT34_ALL_SOURCE_PATH_STUBS_COMPLETE\\nSTUBS=%d\\nALL6521_PINS_AND1066_TEXT_POSE_PROPS_EXACT\\nORIGINAL_DRC=%L\\n" count oldDrc) close(f) count))
'''
depth=0;string=False;escape=False
for line in s.splitlines():
 for c in line:
  if string:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':string=False
  elif c==';':break
  elif c=='"':string=True
  elif c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0,line
assert depth==0 and not string
out=W/'sot34_repair_stubs.il';assert not out.exists();out.write_text(s,encoding='utf-8')
print(json.dumps(dict(stubs=len(rows),skipped=len(decisions)-len(rows),q62_3=next(x for x in decisions if x['ref']=='Q62' and x['pin']=='3'),script=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest().upper()),indent=2))
