"""Keep v7 transform/shape/DRC semantics; add 10-ref completed checkpoints.
Mixed original/approved-target pin and pose guards permit safe checkpoint resume.
Only generates a new helper, never invokes Cadence.
"""
from pathlib import Path
import hashlib
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
D=R/'w/pcb_migration/all81_migration_v7'
s=(D/'pc13_native_replace_v7.il').read_text()
assert s.count('while(selected && length(chunk)<100')==1
s=s.replace('while(selected && length(chunk)<100','while(selected && length(chunk)<10')
s=s.replace('when(mod(count 100)==0','when(t\n    pc13AllMixedGate()')
old='''  pc13AllPoseGate(pc13SourcePoses)
  pc13AllPinGate("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/SOURCE_PINS6521.ilist")'''
assert old in s
s=s.replace(old,'''  pc13AllInitMixedGate()
  pc13AllMixedGate()''')
s=s.replace('unless(result==50 error("ALL81 expected exactly50 replacements\\n"))','unless(result>=0 && result<=50 error("ALL81 invalid replacement count\\n"))\n  foreach(row pc13AllFrozenRows unless(equal(upperCase(pc13Comp(car(row))->symbol->name) upperCase(caddr(row))) error("ALL81 resumed run missing final target\\n")))')
addition='''
; Completed checkpoint resumption accepts only exact frozen original OR target.
; All other components, mechanical/NC pads and source text are still guarded.
procedure(pc13AllInitMixedGate()
 pc13LoadExpected("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/SOURCE_PINS6521.ilist") pc13AllSourcePins=pc13Expected
 pc13LoadExpected("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/TARGET_PINS6521.ilist") pc13AllTargetPins=pc13Expected
 pc13AllFrozenRows=pc13ReadRows("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/REMAINING50.tsv")
 pc13AllRowsByRef=makeTable('pc13AllRowsByRef nil)
 foreach(row pc13AllFrozenRows pc13AllRowsByRef[car(row)]=row)
 t)
procedure(pc13AllMixedGate()
 let((row isTarget expectedPose pinCount)
  pinCount=0
  foreach(c axlDBGetDesign()->components
   row=pc13AllRowsByRef[c->name] isTarget=nil
   when(row
    unless(c->symbol && member(upperCase(c->package) list(upperCase(cadr(row)) upperCase(caddr(row)))) error("ALL81 mixed package guard failed %s\\n" c->name))
    isTarget=equal(upperCase(c->symbol->name) upperCase(caddr(row)))
    unless(isTarget || equal(upperCase(c->symbol->name) upperCase(cadr(row))) error("ALL81 mixed symbol guard failed %s\\n" c->name)))
   pc13Expected=if(isTarget then pc13AllTargetPins else pc13AllSourcePins)
   expectedPose=if(isTarget then pc13TargetPoses[c->name] else pc13SourcePoses[c->name])
   unless(equal(expectedPose pc13Pose(c->symbol)) error("ALL81 mixed exact pose guard failed %s\\n" c->name))
   pc13ExpectedPins(c->name c->symbol) pinCount=pinCount+length(c->symbol->pins))
  pc13Expected=pc13AllTargetPins
  unless(pinCount==6521 error("ALL81 mixed6521 coverage failed\\n")) t))
'''
s+=addition
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
p=D/'pc13_native_replace_batch10_v8.il';assert not p.exists();p.write_text(s,encoding='utf-8')
print(str(p));print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
