"""Add explicit ALL1066 package-name assertions to the v7 fresh reader.
V6 pc13ReadRows intentionally drops from==target rows; fresh coverage must not.
No mutation API or Alt behavior changes in this helper.
"""
from pathlib import Path
import hashlib,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
D=R/'w/pcb_migration/all81_migration_v7'
def sk(p):return json.dumps(str(p).replace('\\','/'))
s='load('+sk(D/'pc13_native_replace_v7.il')+')\n'
s+='''procedure(pc13AllPackageGate()
 let((f line fields count c target)
  f=infile('''+sk(D/'ALL1066_APPROVED.tsv')+''') unless(f error("ALL81 name manifest missing\\n")) gets(line f) count=0
  while(gets(line f)
   fields=parseString(line "\\t\\r\\n") unless(length(fields)==4 error("ALL81 full-name row invalid\\n"))
   c=pc13Comp(car(fields)) target=upperCase(caddr(fields))
   unless(c && c->symbol && equal(upperCase(c->package) target) && equal(upperCase(c->symbol->name) target) && equal(upperCase(c->symbol->definition->name) target)
    error("ALL81 complete package/symbol/definition mismatch %L\\n" fields)) count=count+1)
  close(f) unless(count==1066 error("ALL81 full-name coverage mismatch\\n")) t))
procedure(pc13AllFresh(snapshot dir)
 let((f)
  sstatus(fullPrecision t)
  pc13AllPackageGate()
  pc13TargetPoses=pc13AllLoadPoses('''+sk(D/'TARGET_POSES1066.ilist')+''') pc13AllPoseGate(pc13TargetPoses)
  pc13Readback(snapshot '''+sk(D/'ALL1066_APPROVED.tsv')+''' dir '''+sk(D/'TARGET_PINS6521.ilist')+''')
  eco12CompositeRead(dir) pc13ExportOwnedGeometry(strcat(dir "/owned_geometry.tsv")) pc13ExportBoardDefinitions(dir)
  f=outfile(strcat(dir "/ALL81_FINAL_FRESH_COMPLETE.txt"))
  fprintf(f "ALL6521_TYPED_PHYSICAL_PINS_AND1066_TEXT_POSE_COMPLETE\\nALL1066_PACKAGE_SYMBOL_DEFINITION_COMPLETE_EXPLICIT_UNFILTERED\\n") close(f) t))
'''
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
p=D/'all81_fresh_v8.il';assert not p.exists();p.write_text(s,encoding='utf-8')
print(str(p));print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
