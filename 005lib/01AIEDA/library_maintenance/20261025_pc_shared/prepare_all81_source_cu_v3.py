"""Close actual Cu index over lonely branches; keep4541 guard and exact vias."""
from pathlib import Path
import hashlib,shutil,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');W=R/'w/pcb_migration'
old=W/'all81_source_cu_v2';D=W/'all81_source_cu_v3';assert not D.exists();D.mkdir()
for n in ('SOURCE_FROZEN_REAL_SEGMENTS.ilist','SOURCE_SYMBOL_ETCH_SHAPE_PINS7.ilist'):shutil.copy2(old/n,D/n)
s=(old/'all81_restore_actual_source_cu.il').read_text().replace('/all81_source_cu_v2/','/all81_source_cu_v3/')
lib=(W/'pc13_native_changed_rings_v10.il').read_text();a=lib.index('procedure(pc13BuildCuIndex(side)');b=lib.index('procedure(pc13IndexedCuPolys(',a)
index=lib[a:b]
needle='foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13CuIndexWalk(b)))'
assert needle in index
index=index.replace(needle,needle+'\n  pc13CuStep(strcat(side "_INDEX_BEGIN_LONELY_BRANCHES"))\n  foreach(b axlDBGetLonelyBranches() pc13CuIndexWalk(b))')
insert=s.index('procedure(pc13SourceCuKey(')
extra='''procedure(pc13ViaAllSnapshot(path)
 let((f rows o) rows=nil
  foreach(row pc13CuIndexRows when(equal(nth(4 row) "via")
   o=car(row) rows=cons(sprintf(nil "%L" list(o->xy o->name o->net->name pc13Props(o))) rows)))
  rows=sort(rows 'alphalessp) unless(length(rows)==4541 error("Actual full via snapshot count failed\\n"))
  f=outfile(path) foreach(row rows fprintf(f "%s\\n" row)) close(f) rows))
'''
s=s[:insert]+index+extra+s[insert:]
s=s.replace('close(pf) pc13FrozenSourceCu=reverse(pc13FrozenSourceCu)','''close(pf) pc13FrozenSourceCu=reverse(pc13FrozenSourceCu)
  pc13CuStepPort=outfile(strcat(dir "/STEP_SOURCE.txt")) pc13BuildCuIndex("SOURCE")
  pc13FrozenSourceViaRecords=pc13ViaAllSnapshot(strcat(dir "/SOURCE_ALL4541_VIAS_TYPED.ilist")) close(pc13CuStepPort)''')
s=s.replace('pc13CuStepPort=outfile(strcat(dir "/STEP.txt")) pc13BuildCuIndex("TARGET")','''pc13CuStepPort=outfile(strcat(dir "/STEP.txt")) pc13BuildCuIndex("TARGET")
  unless(equal(pc13FrozenSourceViaRecords pc13ViaAllSnapshot(strcat(dir "/TARGET_ALL4541_VIAS_TYPED.ilist"))) close(pc13CuStepPort) error("Original4541 via XY/pad/net/properties changed; no Cu write allowed\\n"))''')
s=s.replace('axlDBRefreshId(nil) pc13BuildCuIndex("RESTORED") remains=nil','''axlDBRefreshId(nil) pc13BuildCuIndex("RESTORED") remains=nil
  unless(equal(pc13FrozenSourceViaRecords pc13ViaAllSnapshot(strcat(dir "/RESTORED_ALL4541_VIAS_TYPED.ilist"))) error("SourceCu restoration changed via objects\\n"))''')
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
p=D/'all81_restore_actual_source_cu_v3.il';p.write_text(s,encoding='utf-8')
print(p);print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
report={'source_full_geometry':str(R/'w/sot34_full4/explicit_and_boundary_geometry.tsv'),'target_full_geometry':str(R/'w/all81_full4/explicit_and_boundary_geometry.tsv'),'independent_all4541_complete_25field_via_records':'BYTE_EXACT_MULTISET_4541_SOURCE_AND_TARGET; raw geometry includes XY/pad/physical fields; native V3 newly also asserts exact typed net and all properties before/after material restore','fix':'Include axlDBGetLonelyBranches in actualCu index; retain4541 hard guard, then exact independent via XY/pad/net/property snapshots before all writes','script_sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()}
(D/'LONELY_VIA_INDEX_CLOSURE.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
