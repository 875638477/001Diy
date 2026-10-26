"""Prepare minimal read-only source symbolEtch->real-path diagnostics."""
from pathlib import Path
import sys,json,hashlib
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
V=R/'w/pcb_migration/all81_migration_v7'
sys.path.insert(0,str(M));from inspect_sot34_neighbors import parse
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'));from sexpr import parse_many
source=parse(R/'w/all50_alt3/ALL81_pin_adjacency.ilist');target=parse(R/'w/all81_full4/ALL81_pin_adjacency.ilist')
selections=parse_many((V/'REMAINING50_PHYSICAL_PINS964.ilist').read_text());bykey={(r[0],r[1],str(r[2]),str(r[3]),str(r[4])):r for r in selections}
chosen=[]
for key,sr in source.items():
 paths=[r for r in sr if r[0]=='DIRECT_NEIGHBOR' and r[2] in ('path','cline','line','arc')]
 shapes=[r for r in sr if r[0]=='DIRECT_NEIGHBOR' and r[2]=='shape']
 targetpaths=[r for r in target[key] if r[0]=='DIRECT_NEIGHBOR' and r[2] in ('path','cline','line','arc')]
 targetshapes=[r for r in target[key] if r[0]=='DIRECT_NEIGHBOR' and r[2]=='shape']
 if shapes and not paths and not targetpaths and not targetshapes:chosen.append(bykey[key])
assert chosen
def atom(x):
 if isinstance(x,list):return '('+' '.join(atom(v) for v in x)+')'
 if isinstance(x,str):return json.dumps(x)
 return str(x)
p=V/'SOURCE_SHAPE_LOST_PINS.ilist';assert not p.exists();p.write_text('\n'.join(atom(x) for x in chosen)+'\n',encoding='utf-8')
s='load("'+str(V/'pc13_native_replace_v7.il').replace('\\','/')+'")\n'
diag=(V/'all81_adjacency_probe.il').read_text();s+=diag[:diag.index('procedure(pc13All50Adjacency(')]
s+='''procedure(pc13AllIndirectShapeSource(dir)
 let((f pf rows row c p neighbors shapes indirect count)
  sstatus(fullPrecision t)
  pc13AllPinGate("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/SOURCE_PINS6521.ilist")
  f=infile("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_migration_v7/SOURCE_SHAPE_LOST_PINS.ilist") rows=nil
  while(row=lineread(f) rows=cons(car(row) rows)) close(f) rows=reverse(rows)
  unless(length(rows)=='''+str(len(chosen))+''' error("ALL81 shape-only source selection count failed\\n"))
  f=outfile(strcat(dir "/ALL81_INDIRECT_SOURCE_PATHS.ilist")) count=0
  fprintf(f "context\\tdbid\\tkind\\tnet\\trefdes\\tpin\\txy\\tlayer\\tstartEnd\\twidth\\tbBox\\tparent\\tparent_net\\tnSegs\\n")
  foreach(selection rows
   c=pc13Comp(car(selection)) p=car(setof(q c->symbol->pins equal(q->number cadr(selection)) && equal(q->xy nth(2 selection))))
   unless(p error("ALL81 indirect source pin missing\\n"))
   fprintf(f "BEGIN_PIN %L\\n" selection) pc13DiagRow(f "TARGET" p)
   neighbors=axlDBGetConnect(p t) shapes=setof(q neighbors equal(q->objType "shape") && equal(q->net->name p->net->name))
   unless(shapes error("ALL81 expected source own-net shape missing\\n"))
   foreach(shape shapes
    pc13DiagRow(f "SOURCE_LINK_SHAPE" shape)
    fprintf(f "SOURCE_LINK_SHAPE_PROPERTIES %L\\n" shape->??)
    indirect=shape->connect
    foreach(n indirect
     when(member(n->objType '("path" "cline" "line" "arc")) && equal(n->net->name p->net->name)
      pc13DiagRow(f "INDIRECT_SOURCE_PATH" n)
      foreach(seg n->segments pc13DiagRow(f "INDIRECT_PATH_SEGMENT" seg))
      fprintf(f "INDIRECT_PATH_PROPERTIES %L\\n" n->??))))
   fprintf(f "END_PIN %L\\n" selection) drain(f) count=count+1)
  fprintf(f "ALL81_INDIRECT_SOURCE_COMPLETE\\n") close(f)
  f=outfile(strcat(dir "/ALL81_INDIRECT_SOURCE_COMPLETE.txt")) fprintf(f "SOURCE_ONLY_SHAPE_TO_REAL_OWN_NET_PATHS_COMPLETE\\nPINS=%d\\n" count) close(f) count))
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
p=V/'all81_indirect_shape_source.il';assert not p.exists();p.write_text(s,encoding='utf-8')
print('pins',len(chosen),[(r[0],r[1]) for r in chosen]);print(p);print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
