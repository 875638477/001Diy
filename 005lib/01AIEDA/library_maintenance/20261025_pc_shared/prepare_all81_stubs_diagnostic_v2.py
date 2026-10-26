"""Collect every branch whose candidate stroke is outside its target pad.
No creates/save calls are executed, even if all candidates fit.
"""
from pathlib import Path
import hashlib
D=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration\all81_stubs_v1')
s=(D/'all81_repair_stubs.il').read_text()
s=s.replace('procedure(pc13AllRepairStubs(dir)','procedure(pc13AllStubsPreflight(dir)')
s=s.replace('count pc13StubSeen pc13StubSegments)','count failed failureFile pc13StubSeen pc13StubSegments)')
s=s.replace('selectedKeys=nil\n  foreach(group groups','selectedKeys=nil failed=nil\n  failureFile=outfile(strcat(dir "/ALL81_ALL_BRANCH_FIT_RESULTS.ilist"))\n  foreach(group groups')
old='''   unless(selected error("ALL81 source path has no whole stroke inside actual targetpad %L\\n" car(group)))
   geometryKey=list(car(selected) cadr(selected) nth(2 selected) nth(3 selected) nth(7 selected) nth(8 selected) nth(9 selected))
   unless(member(geometryKey selectedKeys) selectedKeys=cons(geometryKey selectedKeys) rows=cons(selected rows)))'''
new='''   fprintf(failureFile "%L\\n" list(car(group) if(selected then "FIT" else "NO_CONTAINED_STROKE") selected)) drain(failureFile)
   if(selected then
    geometryKey=list(car(selected) cadr(selected) nth(2 selected) nth(3 selected) nth(7 selected) nth(8 selected) nth(9 selected))
    unless(member(geometryKey selectedKeys) selectedKeys=cons(geometryKey selectedKeys) rows=cons(selected rows))
   else failed=cons(car(group) failed)))
  close(failureFile)
  f=outfile(strcat(dir "/ALL81_ALL_BRANCH_FIT_COMPLETE.txt"))
  fprintf(f "ALL_SOURCE_BRANCHES_CHECKED=%d\\nFIT_UNIQUE_STUBS=%d\\nFAILED_BRANCHES=%d\\nFAILURES=%L\\nNO_CREATE_CALLS=TRUE\\nNO_SAVE_CALLS=TRUE\\n" length(groups) length(rows) length(failed) reverse(failed)) close(f)
  return(length(failed))'''
assert old in s;s=s.replace(old,new)
s=s[:s.index('  return(length(failed))')]+'  length(failed)))\n'
p=D/'all81_stubs_preflight_v3.il';assert not p.exists();p.write_text(s,encoding='utf-8')
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
print(p);print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
