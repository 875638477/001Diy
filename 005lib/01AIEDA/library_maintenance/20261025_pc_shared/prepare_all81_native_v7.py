"""Prepare remaining50 approved public-package swaps; no CAD invocation."""
from pathlib import Path
from decimal import Decimal
import csv,hashlib,json,sys
M=Path(__file__).parent
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration';D=W/'all81_migration_v7'
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def sk(p):return json.dumps(str(p).replace('\\','/'))
def atom(x):
 if isinstance(x,list):return '('+' '.join(atom(v) for v in x)+')'
 if isinstance(x,Atom):return str(x)
 if isinstance(x,str):return json.dumps(x)
 return str(x)
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
def save(name,s):
 p=D/name;assert not p.exists();p.write_text(s,encoding='utf-8');return p
source=R/'w/sot34_attached4/SOT34_ATTACHED.brd'
assert sha(source)=='06B8DD73EE20A4C01A0BF36E0BF6CD0FDDFE20CE2F89DA430A2C003414BE9405'
plan=M/'project81_final_canonical_plan13/ALL81_PHYSICAL_REF_MIGRATION.tsv'
assert sha(plan)=='AC07E9D41A7A1976896B42953F2D8A090D070B45888320D3D6FB4E4DA92487FC'
with plan.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==84
remaining=[r for r in rows if r['from_package']!='SOT23_123'];assert len(remaining)==50
byref={r['refdes']:r for r in rows}
assert all(Decimal(r['delta']) in (0,90,-90) for r in rows)
assert not D.exists();D.mkdir()
header='refdes\tfrom_package\ttarget_package\tdelta\n'
save('REMAINING50.tsv',header+'\n'.join('\t'.join(r[k] for k in ('refdes','from_package','target_package','delta')) for r in remaining)+'\n')
old=W/'sot34_migration/EXPECTED_PINS_SOT34.ilist';new=M/'project81_expected_pins13/ALL81_EXPECTED_PINS6521.ilist'
assert sha(new)=='CEC52E81720BB61058E8A404D4EA5477086F59CCE94ED291509CC11B9527E008'
save('SOURCE_PINS6521.ilist',old.read_text());save('TARGET_PINS6521.ilist',new.read_text())
oldpins=dict(parse_many(old.read_text()));newpins=dict(parse_many(new.read_text()))
assert len(oldpins)==len(newpins)==1066 and sum(map(len,oldpins.values()))==sum(map(len,newpins.values()))==6521
with (R/'w/sot34_full4/symbols.tsv').open(newline='') as f:symbols=list(csv.DictReader(f,delimiter='\t'))
assert len(symbols)==1066
sourceposes=[];targetposes=[];approvals=[]
for s in symbols:
 ref=s['refdes'];xy=[Decimal(s['x']),Decimal(s['y'])];rot=Decimal(s['rotation']);mirror=Atom(s['mirrored']);delta=Decimal(byref[ref]['delta']) if ref in byref else Decimal(0)
 sourceposes.append([ref,[xy,rot,mirror]])
 targetposes.append([ref,[xy,(rot+delta)%360 if rot+delta>=0 else (rot+delta)%360+360,mirror]])
 target=byref[ref]['target_package'] if ref in byref else s['symbol_name']
 approvals.append('\t'.join((ref,s['symbol_name'],target,'0')))
save('SOURCE_POSES1066.ilist','\n'.join(atom(x) for x in sourceposes)+'\n')
save('TARGET_POSES1066.ilist','\n'.join(atom(x) for x in targetposes)+'\n')
save('ALL1066_APPROVED.tsv',header+'\n'.join(approvals)+'\n')
# Every physical pad of the remaining50 is selected by number AND world position.
# This retains repeated/blank installation-pad numbers without merging records.
pairs=[]
for r in remaining:
 ref=r['refdes'];a=oldpins[ref];b=newpins[ref];assert len(a)==len(b)
 assert [v[0] for v in a]==[v[0] for v in b]
 for i,(x,y) in enumerate(zip(a,b)):
  assert x[2:5]==y[2:5]
  pairs.append([ref,x[0],x[1],y[1],i])
assert len(pairs)==964
save('REMAINING50_PHYSICAL_PINS964.ilist','\n'.join(atom(x) for x in pairs)+'\n')
base=(W/'pc13_native_replace_v6.il').read_text()
base=base.replace('unless(zerop(delta) error("V13 has no approved rotation changes\\n"))','unless(member(delta \'(0.0 90.0 -90.0)) error("V13 unapproved rotation magnitude\\n"))')
base=base.replace('let((ref from target c s pose pins texts props oldalt)','let((ref from target c s pose pins texts props oldalt delta expectedPose)')
base=base.replace('pose=pc13Pose(s) texts=pc13TextSnapshot(s) props=pc13Props(c->compdef)','pose=pc13Pose(s) texts=pc13TextSnapshot(s) props=pc13Props(c->compdef)\n  delta=nth(3 row) expectedPose=pc13TargetPoses[ref]\n  unless(equal(pose pc13SourcePoses[ref]) error("ALL81 source pose mismatch %s\\n" ref))')
base=base.replace('axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol\n  pc13TextRestore(s texts)','axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol\n  unless(equal(pose pc13Pose(s)) error("ALL81 Alt unexpectedly moved source pose %s\\n" ref))\n  unless(zerop(delta)\n   unless(axlTransformObject(s ?angle delta ?origin car(pose)) error("ALL81 approved rotation failed %s\\n" ref))\n   axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol)\n  unless(equal(expectedPose pc13Pose(s)) error("ALL81 exact approved target pose mismatch %s\\n" ref))\n  pc13TextRestore(s texts)')
base=base.replace('unless(equal(pose pc13Pose(s)) error("V13 pose changed %s\\n" ref))','unless(equal(expectedPose pc13Pose(s)) error("ALL81 target pose changed %s\\n" ref))')
assert 'no approved rotation changes' not in base and 'ALL81 exact approved' in base
s=base+'\n'+'''procedure(pc13AllLoadPoses(path)
 let((f row table) table=makeTable('pc13PoseTable nil) f=infile(path)
  unless(f error("ALL81 pose manifest missing\\n"))
  while(row=lineread(f) row=car(row) table[car(row)]=cadr(row)) close(f) table))
procedure(pc13AllPoseGate(table)
 let((count) count=0
  foreach(c axlDBGetDesign()->components
   unless(equal(table[c->name] pc13Pose(c->symbol)) error("ALL81 full pose guard failed %s\\n" c->name)) count=count+1)
  unless(count==1066 error("ALL81 pose coverage failed\\n")) t))
procedure(pc13AllPinGate(path)
 let((count) count=0 pc13LoadExpected(path)
  foreach(c axlDBGetDesign()->components pc13ExpectedPins(c->name c->symbol) count=count+length(c->symbol->pins))
  unless(count==6521 error("ALL81 physical pin coverage failed\\n")) t))
'''
s+='load('+sk(R.parent/'12electrical_fixed_20261025/tools/rules_eco/composite_readonly.il')+')\n'
s+='load('+sk(W/'pc13_export_owned_geometry.il')+')\nload('+sk(W/'pc13_export_board_definitions.il')+')\n'
s+='''procedure(pc13All50Apply(dir)
 let((result)
  sstatus(fullPrecision t)
  unless(equal(axlDBGetDesignUnits() '("mils" 2)) error("ALL81 expects original mils2\\n"))
  pc13SourcePoses=pc13AllLoadPoses('''+sk(D/'SOURCE_POSES1066.ilist')+''')
  pc13TargetPoses=pc13AllLoadPoses('''+sk(D/'TARGET_POSES1066.ilist')+''')
  pc13AllPoseGate(pc13SourcePoses)
  pc13AllPinGate('''+sk(D/'SOURCE_PINS6521.ilist')+''')
  result=pc13Replace('''+sk(D/'REMAINING50.tsv')+''' dir strcat(dir "/ALL81_ALT50.brd") "D:/001DIY/005lib/01Psm_lib" "D:/001DIY/005lib/01Pad_lib" 0 '''+sk(D/'TARGET_PINS6521.ilist')+''')
  unless(result==50 error("ALL81 expected exactly50 replacements\\n"))
  pc13AllPoseGate(pc13TargetPoses) pc13AllPinGate('''+sk(D/'TARGET_PINS6521.ilist')+''')
  result))
procedure(pc13AllRestore(snapshot dir)
 pc13RestoreAfterNetrev(snapshot dir strcat(dir "/ALL81_RESTORED.brd")))
procedure(pc13AllFresh(snapshot dir)
 let((f)
  sstatus(fullPrecision t)
  pc13TargetPoses=pc13AllLoadPoses('''+sk(D/'TARGET_POSES1066.ilist')+''') pc13AllPoseGate(pc13TargetPoses)
  pc13Readback(snapshot '''+sk(D/'ALL1066_APPROVED.tsv')+''' dir '''+sk(D/'TARGET_PINS6521.ilist')+''')
  eco12CompositeRead(dir) pc13ExportOwnedGeometry(strcat(dir "/owned_geometry.tsv")) pc13ExportBoardDefinitions(dir)
  f=outfile(strcat(dir "/ALL81_FINAL_FRESH_COMPLETE.txt"))
  fprintf(f "ALL6521_TYPED_PHYSICAL_PINS_AND1066_TEXT_POSE_COMPLETE\\nALL1066_PACKAGE_SYMBOL_DEFINITION_COMPLETE\\n") close(f) t))
'''
balanced(s);save('pc13_native_replace_v7.il',s)
diag=(W/'sot34_migration/sot34_adjacency_probe.il').read_text();diag=diag[:diag.index('procedure(pc13Sot34Adjacency(')]
diag+='''procedure(pc13All50Adjacency(phase dir)
 let((f pf plan line selections p connected n ends endobj index c xy)
  sstatus(fullPrecision t)
  unless(member(phase '("source" "target")) error("ALL81 adjacency phase invalid\\n"))
  plan=infile('''+sk(D/'REMAINING50_PHYSICAL_PINS964.ilist')+''') selections=nil
  while(line=lineread(plan) selections=cons(car(line) selections)) close(plan) selections=reverse(selections)
  unless(length(selections)==964 error("ALL81 expects964 physical selections\\n"))
  f=outfile(strcat(dir "/ALL81_pin_adjacency.ilist")) pf=outfile(strcat(dir "/ALL81_pin_adjacency_summary.tsv"))
  fprintf(f "context\\tdbid\\tkind\\tnet\\trefdes\\tpin\\txy\\tlayer\\tstartEnd\\twidth\\tbBox\\tparent\\tparent_net\\tnSegs\\n")
  fprintf(pf "refdes\\tpin\\txy\\tnet\\tdirect_connected_count\\tdirect_kinds\\n")
  foreach(selection selections
   c=pc13DiagRef(car(selection)) xy=if(equal(phase "source") then nth(2 selection) else nth(3 selection))
   p=car(setof(q c->symbol->pins equal(q->number cadr(selection)) && equal(q->xy xy)))
   unless(p error("ALL81 physical pin selection missing %L\\n" selection))
   fprintf(f "BEGIN_PIN %L\\n" selection) pc13DiagRow(f "TARGET" p)
   connected=axlDBGetConnect(p t) fprintf(f "DIRECT_CONNECT %L\\n" connected)
   fprintf(pf "%s\\t%s\\t%L\\t%L\\t%d\\t%L\\n" car(selection) cadr(selection) p->xy p->net->name length(connected) foreach(mapcar q connected q->objType))
   foreach(n connected
    pc13DiagRow(f "DIRECT_NEIGHBOR" n)
    when(member(n->objType '("path" "cline" "line" "arc"))
     foreach(seg n->segments pc13DiagRow(f "DIRECT_PATH_SEGMENT" seg))
     ends=axlDBGetConnect(n t) fprintf(f "DIRECT_PATH_ENDPOINT_CONNECTIONS %L\\n" ends)
     when(listp(car(ends)) index=0 foreach(side ends index=index+1 foreach(endobj side pc13DiagRow(f sprintf(nil "PATH_END_%d" index) endobj)))))
    when(equal(n->objType "shape") fprintf(f "DIRECT_SHAPE_PROPERTIES %L\\n" n->??)))
   fprintf(f "END_PIN %L\\n" selection) drain(f) drain(pf))
  fprintf(f "ALL81_ALL964_ADJACENCY_COMPLETE\\n") close(f) close(pf)
  f=outfile(strcat(dir "/ALL81_ADJACENCY_COMPLETE.txt")) fprintf(f "PHASE=%s\\nALL964_NATIVE_PHYSICAL_PIN_NEIGHBORS_COMPLETE\\n" phase) close(f) t))
'''
balanced(diag);save('all81_adjacency_probe.il',diag)
receipt={'status':'PREPARED_NOT_NATIVE_RUN','source_board':str(source),'source_sha256':sha(source),'remaining_refs':50,'all81_refs':84,'remaining_physical_pins':964,'full_physical_pins':6521,'components':1066,'approved_rotations':[{k:r[k] for k in ('refdes','delta')} for r in remaining if Decimal(r['delta'])], 'files':{p.name:sha(p) for p in D.iterdir() if p.is_file()},'native_api_reference':'SPB172/doc/algroskill/06intedt.html#821370 axlTransformObject ?angle ?origin; all transforms exact source/target pose guarded; source text restored after approved rotation'}
save('ALL81_NATIVE_V7_PREPARATION.json',json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
