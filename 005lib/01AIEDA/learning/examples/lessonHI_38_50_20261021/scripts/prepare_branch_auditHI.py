from pathlib import Path
import shutil,json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il'
s=r'''
procedure(hiBranchAudit(out)
 let((f allpins graph terminals seen orphanCount branchCount refs)
  f=outfile(strcat(out "/hi_branch_terminal_audit.txt"))
  allpins=nil orphanCount=0 branchCount=0
  foreach(c axlDBGetDesign()->components
   foreach(p c->symbol->pins when(p->net && member(p->net axlDBGetDesign()->nets) allpins=cons(p allpins))))
  foreach(net axlDBGetDesign()->nets
   foreach(branch net->branches
    graph=nil
    foreach(child branch->children
     foreach(obj gConnectedObjects(child) unless(member(obj graph) graph=cons(obj graph))))
    terminals=setof(p allpins member(p graph))
    refs=mapcar('hiTerminalKey terminals)
    branchCount=branchCount+1
    fprintf(f "BRANCH_AUDIT net=%L branch=%L children=%d reachableObjects=%d physicalTerminals=%d terminalKeys=%L\n" net->name branch length(branch->children) length(graph) length(terminals) refs)
    unless(terminals
     orphanCount=orphanCount+1
     fprintf(f "NO_TERMINAL_BRANCH net=%L branchAttrs=%L\n" net->name branch->??)
     foreach(obj graph fprintf(f "NO_TERMINAL_OBJECT net=%L object=%L attrs=%L\n" net->name obj obj->??)))))
  fprintf(f "HI_BRANCH_TERMINAL_AUDIT_COMPLETE\nbranches=%d\nbranchesWithoutPhysicalTerminals=%d\nscope=Physical branch reachability, not by itself manufacturing or antenna certification.\n" branchCount orphanCount)
  close(f) t))
'''
assert 'procedure(hiBranchAudit' not in p.read_text();p.write_text(p.read_text()+s,encoding='ascii')
p=R/'scripts/prepare_readbackHI_v8.py';s=p.read_text();s=s.replace("captures+='skill errset(hiUSBMaskRead(\"'+out+'\") t)\\n'", "captures+='skill errset(hiUSBMaskRead(\"'+out+'\") t)\\n'\ncaptures+='skill errset(hiBranchAudit(\"'+out+'\") t)\\n'")
(R/'scripts/prepare_readbackHI_v9.py').write_text(s,encoding='ascii')
tag='branch_audit_2L_b010';snap=R/'source/readback_snapshots'/tag;snap.mkdir(parents=True,exist_ok=False)
files=[R/'source/local_copperG_v2.il',R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI_shapes_v3.il']
head='set NOCONFIRM\n';m=[]
for i,src in enumerate(files):
 dst=snap/(str(i).zfill(2)+'_'+src.name);shutil.copyfile(src,dst);head+='skill errset(load('+json.dumps(dst.as_posix())+') t)\n';m.append({'source':str(src),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
head+='skill errset(hiBranchAudit('+json.dumps((R/'logs'/tag).as_posix())+') t)\nquit\nfillin "yes"\n'
(R/f'scripts/{tag}.scr').write_text(head,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(m,indent=2))
print('branch audit pilot prepared, source unchanged')
