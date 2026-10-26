"""Freeze all required source-real endpoint candidates; let native full-pad
ANDNOT select a wholly contained 5mil-or-original-narrower attachment stub.
No CAD invocation. Source and target readbacks must be complete before use.
"""
from pathlib import Path
from decimal import Decimal as Q
import argparse,csv,collections,hashlib,json,sys,math
M=Path(__file__).parent
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration';V=W/'all81_migration_v7'
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
def atom(x):
 if isinstance(x,list):return '('+' '.join(atom(v) for v in x)+')'
 if isinstance(x,Atom):return str(x)
 if isinstance(x,str):return json.dumps(x)
 return str(x)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def sk(p):return json.dumps(str(p).replace('\\','/'))
def grid(x):
 n=x.quantize(Q('.01'));assert abs(x-n)<Q('1e-7'),x;return n
def parseadj(p,expected=964):
 out={};key=None
 for line in p.read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('BEGIN_PIN '):
   row=parse_many(line[10:])[0];key=(row[0],row[1],int(row[4]));assert key not in out;out[key]=[]
  elif line.startswith('END_PIN '):key=None
  elif key and '\t' in line and not line.startswith('context\t'):
   fields=line.split('\t');out[key].append([fields[0]]+[parse_many(x)[0] for x in fields[1:]])
 assert len(out)==expected
 assert ('ALL81_ALL964_ADJACENCY_COMPLETE' if expected==964 else 'ALL81_INDIRECT_SOURCE_COMPLETE') in p.read_text()
 return out
def groups(p,expected):
 lookup={};mechanical_by_xy=collections.defaultdict(list)
 for ref,records in expected.items():
  for i,row in enumerate(records):
   key=(ref,row[0],grid(row[1][0]),grid(row[1][1]));assert key not in lookup,key;lookup[key]=(ref,row[0],i)
   if row[3]==Atom('t') and isinstance(row[2],Atom) and row[2]==Atom('nil'):
    mechanical_by_xy[key[1:]].append((ref,row[0],i))
 g=collections.defaultdict(set);keys={}
 with p.open(newline='') as f:
  for r in csv.DictReader(f,delimiter='\t'):
   key=(r['refdes'],r['pin'],grid(Q(r['x'])),grid(Q(r['y'])))
   ident=lookup.get(key)
   if ident is None:
    # Native GetConnect reports component=nil for unnamed mechanical pads.
    # Resolve only a unique numbered+XY native-NIL mechanical ledger record.
    assert r['refdes']=='nil' and r['net']=='nil',r
    matches=mechanical_by_xy[key[1:]];assert len(matches)==1,(r,matches);ident=matches[0]
   g[r['group']].add(ident);assert ident not in keys;keys[ident]=r['group']
 assert len(keys)==6521
 return {k:g[v] for k,v in keys.items()}
def balanced(s):
 depth=0;quoted=False;esc=False
 for line in s.splitlines():
  for c in line:
   if quoted:
    if esc:esc=False
    elif c=='\\':esc=True
    elif c=='"':quoted=False
   elif c==';':break
   elif c=='"':quoted=True
   elif c=='(':depth+=1
   elif c==')':depth-=1;assert depth>=0,line
 assert depth==0 and not quoted
def own_segments(rows,net):
 return [x for x in rows if x[0] in ('DIRECT_PATH_SEGMENT','DIRECT_NEIGHBOR','INDIRECT_PATH_SEGMENT','INDIRECT_SOURCE_PATH') and x[2] in ('line','arc') and type(x[3])==type(net) and x[3]==net and isinstance(x[8],list) and len(x[8])==2]
def line_covered(source,targets):
 a,b=[[int(grid(v)*100) for v in p] for p in source[8]];dx=b[0]-a[0];dy=b[1]-a[1]
 assert dx or dy
 axis=0 if abs(dx)>=abs(dy) else 1;lo=min(a[axis],b[axis]);hi=max(a[axis],b[axis]);ranges=[]
 divisor=math.gcd(dx,dy);dx//=divisor;dy//=divisor
 for t in targets:
  if t[2]!='line' or t[7]!=source[7] or t[9]!=source[9]:continue
  c,d=[[int(grid(v)*100) for v in p] for p in t[8]]
  if (c[0]-a[0])*dy-(c[1]-a[1])*dx or (d[0]-a[0])*dy-(d[1]-a[1])*dx:continue
  l=max(lo,min(c[axis],d[axis]));h=min(hi,max(c[axis],d[axis]))
  if l<=h:ranges.append((l,h))
 reach=lo
 for l,h in sorted(ranges):
  if reach>=hi:return True
  if l>reach:return False
  reach=max(reach,h)
 return reach>=hi
def direct_paths_retained(source,target,net):
 ss=own_segments(source,net);tt=own_segments(target,net)
 if not ss or not tt:return False
 for x in ss:
  if x[2]=='line':
   if not line_covered(x,tt):return False
  elif not any(t[2]=='arc' and t[7]==x[7] and t[9]==x[9] and (t[8]==x[8] or t[8]==list(reversed(x[8]))) for t in tt):return False
 return True
ap=argparse.ArgumentParser()
ap.add_argument('--source-adjacency',type=Path,required=True);ap.add_argument('--target-adjacency',type=Path,required=True)
ap.add_argument('--target-readback',type=Path,required=True);ap.add_argument('--candidate-board',type=Path,required=True)
ap.add_argument('--output-directory',type=Path,required=True)
ap.add_argument('--indirect-source',type=Path)
a=ap.parse_args();D=a.output_directory;assert D.resolve().is_relative_to(R.resolve()) and not D.exists()
assert (a.target_readback/'ALL81_FINAL_FRESH_COMPLETE.txt').exists()
source_report=a.source_adjacency.parent/'launch_report.json'
source_sha='06B8DD73EE20A4C01A0BF36E0BF6CD0FDDFE20CE2F89DA430A2C003414BE9405'
if source_report.exists():
 source_launch=json.loads(source_report.read_text(encoding='utf-8-sig'))
 assert source_launch['source_sha256_before']==source_launch['source_sha256_after']==source_sha and source_launch['input_unchanged']
else:
 # all50_alt3 completed the source read-only phase and all50 immediate guards,
 # then timed out during deferred shape close without saving. Retain that FAIL;
 # reuse its finished source diagnostic bound to the unchanged original copy.
 assert a.source_adjacency.parent.name=='all50_alt3'
 assert sha(a.source_adjacency.parent/'INPUT_COPY.brd')==sha(R/'w/sot34_attached4/SOT34_ATTACHED.brd')==source_sha
 assert 'PHASE=source' in (a.source_adjacency.parent/'ALL81_ADJACENCY_COMPLETE.txt').read_text()
 assert 'pc13All50Adjacency("source"' in (a.source_adjacency.parent/'run.scr').read_text()
 with (a.source_adjacency.parent/'applied.tsv').open(newline='') as f:applied=list(csv.DictReader(f,delimiter='\t'))
 assert len(applied)==50 and all(row['pose_pin_text_preserved']=='TRUE' for row in applied)
 source_launch={'source_sha256_before':source_sha,'source_sha256_after':source_sha,'input_unchanged':True,'bounded_finished_phase_only':True,'whole_run_status':'TIMEOUT_RETAINED_NOT_PASS'}
target_launch=json.loads((a.target_adjacency.parent/'launch_report.json').read_text(encoding='utf-8-sig'))
readback_launch=json.loads((a.target_readback/'launch_report.json').read_text(encoding='utf-8-sig'))
candidate_sha=sha(a.candidate_board)
assert target_launch['source_sha256_before']==target_launch['source_sha256_after']==readback_launch['source_sha256_before']==readback_launch['source_sha256_after']==candidate_sha
assert source_launch['input_unchanged'] and target_launch['input_unchanged'] and readback_launch['input_unchanged']
sp=dict(parse_many((V/'SOURCE_PINS6521.ilist').read_text()));tp=dict(parse_many((V/'TARGET_PINS6521.ilist').read_text()))
sg=groups(R/'w/sot34_full4/native_copper_pin_groups.tsv',sp);tg=groups(a.target_readback/'native_copper_pin_groups.tsv',tp)
source=parseadj(a.source_adjacency);target=parseadj(a.target_adjacency)
if a.indirect_source:
 indirect_launch=json.loads((a.indirect_source.parent/'launch_report.json').read_text(encoding='utf-8-sig'))
 assert indirect_launch['source_sha256_before']==indirect_launch['source_sha256_after']==source_sha and indirect_launch['input_unchanged']
 for key,rows in parseadj(a.indirect_source,7).items():
  assert key in source
  source[key]+=rows
assert source.keys()==target.keys();out=[];decisions=[]
for key,sr in source.items():
 ref,pin,i=key;tr=target[key];old=sp[ref][i];new=tp[ref][i]
 before=next(x for x in sr if x[0]=='TARGET');after=next(x for x in tr if x[0]=='TARGET')
 assert before[3]==after[3]==old[2]==new[2]
 assert all(grid(before[6][k])==old[1][k] and grid(after[6][k])==new[1][k] for k in range(2))
 paths=[x for x in sr if x[0] in ('DIRECT_NEIGHBOR','INDIRECT_SOURCE_PATH') and x[2] in ('path','cline','line','arc')]
 targetpaths=[x for x in tr if x[0]=='DIRECT_NEIGHBOR' and x[2] in ('path','cline','line','arc')]
 changed=sg[key]!=tg[key]
 if not paths:
  source_neighbors=[x for x in sr if x[0]=='DIRECT_NEIGHBOR'];target_neighbors=[x for x in tr if x[0]=='DIRECT_NEIGHBOR']
  decisions.append(dict(ref=ref,pin=pin,index=i,action='SKIP_NO_SOURCE_PATH',partition_changed=changed,source_neighbors=len(source_neighbors),target_neighbors=len(target_neighbors)))
  if changed:
   assert source_neighbors and target_neighbors,(key,'Source no-path/shape-only local connection changed; needs explicit analysis')
  continue
 if (not changed and targetpaths) or direct_paths_retained(sr,tr,old[2]):
  decisions.append(dict(ref=ref,pin=pin,index=i,action='SKIP_PARTITION_OR_FULL_SOURCE_DIRECT_PATH_COVERAGE',partition_changed=changed));continue
 assert not isinstance(old[2],Atom) and old[2]!='',(key,'Never create copper at source NIL/blank NC')
 for source_path in paths:
  # Each source neighbor path is an independent attachment branch. A removed
  # symbolEtch shape may have bridged two differently located real path ends.
  branch=[x for x in own_segments(sr,old[2]) if x[11]==source_path[1] or x[1]==source_path[1]]
  assert branch,(key,source_path,'Source path segments missing')
  if direct_paths_retained(branch,tr,old[2]):
   decisions.append(dict(ref=ref,pin=pin,index=i,source_path=str(source_path[1]),action='SKIP_FULL_SOURCE_PATH_BRANCH_RETAINED'));continue
  choices=[];seen=set()
  for seg in branch:
   if seg[7] not in ('ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM'):continue
   if not isinstance(seg[9],Q) or seg[9]<=0:continue
   se=[[grid(v) for v in p] for p in seg[8]]
   for point in se:
    if point==new[1]:continue
    row=[ref,pin,old[2],seg[7],seg[2],seg[9],se,point,new[1],min(Q(5),seg[9]),old[1],new[5]]
    text=atom(row)
    if text in seen:continue
    seen.add(text);distance=sum((point[k]-new[1][k])**2 for k in range(2))
    choices.append((point!=old[1],distance,row))
  assert choices,(key,source_path,'No actual same-net source branch endpoint')
  choices.sort(key=lambda x:(x[0],x[1]));out.append([list(key)+[str(source_path[1])],[c[2] for c in choices]])
  decisions.append(dict(ref=ref,pin=pin,index=i,source_path=str(source_path[1]),action='NATIVE_SELECT_CONTAINED_SOURCE_BRANCH_ENDPOINT',source_paths=len(paths),target_paths=len(targetpaths),partition_changed=changed,candidates=len(choices)))
assert out
D.mkdir();plan=D/'ALL81_STUB_CANDIDATES.ilist';plan.write_text('\n'.join(atom(x) for x in out)+'\n',encoding='utf-8')
sourceil=(W/'sot34_migration/sot34_repair_stubs_v2.il').read_text()
core=sourceil[sourceil.index('procedure(pc13SotStubPin('):sourceil.index('procedure(pc13Sot34RepairStubs(')]
core=core.replace('equal(pin->name "PAD_36_47")','equal(pin->name nth(11 row))')
core=core.replace('procedure(pc13SotStubValidate(row)','procedure(pc13AllStubFits(row)')
core=core.replace('when(outside error("SOT entire stub stroke exceeds actual newpad %L\\n" row)) t))','null(outside)))')
assert 'null(outside)))' in core
s='load('+sk(V/'pc13_native_replace_v7.il')+')\nload('+sk(W/'pc13_native_changed_rings_v10.il')+')\n'+core
s+='''procedure(pc13AllRepairStubs(dir)
 let((f row groups rows selected geometryKey selectedKeys textSnapshot poseSnapshot propSnapshot oldDrc count pc13StubSeen pc13StubSegments)
  sstatus(fullPrecision t)
  unless(equal(axlDBGetDesignUnits() '("mils" 2)) error("ALL81 stub expects original mils2\\n"))
  pc13AllPinGate('''+sk(V/'TARGET_PINS6521.ilist')+''')
  textSnapshot=makeTable('pc13AllText nil) poseSnapshot=makeTable('pc13AllPose nil) propSnapshot=makeTable('pc13AllProps nil)
  foreach(c axlDBGetDesign()->components textSnapshot[c->name]=pc13TextSorted(c->symbol) poseSnapshot[c->name]=pc13Pose(c->symbol) propSnapshot[c->name]=pc13Props(c->compdef))
  oldDrc=axlDBControl('drcEnable) pc13StubSeen=makeTable('pc13StubSeen nil) pc13StubSegments=nil
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13SotStubWalk(b)))
  f=infile('''+sk(plan)+''') groups=nil while(row=lineread(f) groups=cons(car(row) groups)) close(f) groups=reverse(groups) rows=nil
  unless(length(groups)=='''+str(len(out))+''' error("ALL81 frozen repair group count failed\\n"))
  selectedKeys=nil
  foreach(group groups
   selected=nil
   foreach(candidate cadr(group) when(!selected && pc13AllStubFits(candidate) selected=candidate))
   unless(selected error("ALL81 source path has no whole stroke inside actual targetpad %L\\n" car(group)))
   geometryKey=list(car(selected) cadr(selected) nth(2 selected) nth(3 selected) nth(7 selected) nth(8 selected) nth(9 selected))
   unless(member(geometryKey selectedKeys) selectedKeys=cons(geometryKey selectedKeys) rows=cons(selected rows)))
  rows=reverse(rows)
  f=outfile(strcat(dir "/ALL81_SELECTED_STUBS.ilist")) foreach(row rows fprintf(f "%L\\n" row)) close(f)
  f=outfile(strcat(dir "/ALL81_STUB_APPLIED.tsv")) fprintf(f "refdes\\tpin\\tnet\\tlayer\\told_endpoint\\tnew_pin_center\\twidth\\tbefore_neighbors\\tafter_neighbors\\n")
  count=axlDBCloak('pc13SotCreateStubs(rows f) 'shape) close(f)
  unless(count==length(rows) error("ALL81 stub batch incomplete\\n"))
  axlDBRefreshId(nil)
  foreach(c axlDBGetDesign()->components
   pc13ExpectedPins(c->name c->symbol)
   unless(equal(textSnapshot[c->name] pc13TextSorted(c->symbol)) && equal(poseSnapshot[c->name] pc13Pose(c->symbol)) && equal(propSnapshot[c->name] pc13Props(c->compdef)) error("ALL81 text/pose/props changed\\n")))
  unless(equal(oldDrc axlDBControl('drcEnable)) error("ALL81 source DRC mode changed\\n"))
  unless(axlSaveDesign(?design strcat(dir "/ALL81_ATTACHED.brd") ?noMru t ?noConfirm t) error("ALL81 attachment repair save failed\\n"))
  f=outfile(strcat(dir "/ALL81_STUB_COMPLETE.txt")) fprintf(f "ALL_SOURCE_PATH_STUBS_COMPLETE\\nSTUBS=%d\\nALL6521_PINS_AND1066_TEXT_POSE_PROPS_EXACT\\nORIGINAL_DRC=%L\\n" count oldDrc) close(f) count))
'''
balanced(s);(D/'all81_repair_stubs.il').write_text(s,encoding='utf-8')
inputs=[a.source_adjacency,a.target_adjacency,a.target_readback/'native_copper_pin_groups.tsv',V/'SOURCE_PINS6521.ilist',V/'TARGET_PINS6521.ilist']
if a.indirect_source:inputs.append(a.indirect_source)
receipt={'status':'PREPARED_NOT_NATIVE_RUN','candidate_board':str(a.candidate_board),'candidate_sha256':sha(a.candidate_board),'source_native_evidence':source_launch,'repair_pin_count':len(out),'source_candidate_paths':sum(len(x[1]) for x in out),'decisions':decisions,'inputs':{str(p):sha(p) for p in inputs},'outputs':{p.name:sha(p) for p in D.iterdir()}}
(D/'ALL81_STUB_PREPARATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='decisions'},indent=2))
