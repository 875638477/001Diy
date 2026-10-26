"""Prepare read-only102-pin native adjacency probes; never launches CAD."""
from pathlib import Path
import json,hashlib
M=Path(__file__).parent;W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration');D=W/'sot34_migration'
changes=json.loads((M/'sot34_superset_pst_and_pins_v1/SOT34_102_EXPECTED_CHANGES.json').read_text());assert len(changes)==102
pairs=[(r['ref'],r['pin']) for r in changes];assert len(set(pairs))==102
plan=D/'SOT34_PIN_PAIRS102.ilist';assert not plan.exists();plan.write_text('\n'.join('('+json.dumps(r)+' '+json.dumps(p)+')' for r,p in pairs)+'\n',encoding='utf-8')
base=(W/'pc13_connectivity_diagnostics.il').read_text();start=base.index('procedure(pc13ConnectivityDiagnostics(')
s=base[:start]+r'''procedure(pc13Sot34Adjacency(dir)
 let((f pf plan line selections p connected n ends endobj index)
  sstatus(fullPrecision t)
  plan=infile("'''+str(plan).replace('\\','/')+r'''") selections=nil
  while(line=lineread(plan) selections=cons(car(line) selections)) close(plan) selections=reverse(selections)
  unless(length(selections)==102 error("Expected102 SOT pins\n"))
  f=outfile(strcat(dir "/SOT34_pin_adjacency.ilist")) pf=outfile(strcat(dir "/SOT34_pin_adjacency_summary.tsv"))
  fprintf(f "context\tdbid\tkind\tnet\trefdes\tpin\txy\tlayer\tstartEnd\twidth\tbBox\tparent\tparent_net\tnSegs\n")
  fprintf(pf "refdes\tpin\txy\tnet\tdirect_connected_count\tdirect_kinds\n")
  foreach(selection selections
   p=pc13DiagPin(car(selection) cadr(selection)) unless(p error("SOT source/target pin missing\n"))
   fprintf(f "BEGIN_PIN %L\n" selection) pc13DiagRow(f "TARGET" p)
   connected=axlDBGetConnect(p t) fprintf(f "DIRECT_CONNECT %L\n" connected)
   fprintf(pf "%s\t%s\t%L\t%L\t%d\t%L\n" car(selection) cadr(selection) p->xy p->net->name length(connected) foreach(mapcar q connected q->objType))
   foreach(n connected
    pc13DiagRow(f "DIRECT_NEIGHBOR" n)
    when(member(n->objType '("path" "cline" "line" "arc"))
     foreach(seg n->segments pc13DiagRow(f "DIRECT_PATH_SEGMENT" seg))
     ends=axlDBGetConnect(n t) fprintf(f "DIRECT_PATH_ENDPOINT_CONNECTIONS %L\n" ends)
     when(listp(car(ends)) index=0 foreach(side ends index=index+1 foreach(endobj side pc13DiagRow(f sprintf(nil "PATH_END_%d" index) endobj)))))
    when(equal(n->objType "shape") fprintf(f "DIRECT_SHAPE_PROPERTIES %L\n" n->??)))
   fprintf(f "END_PIN %L\n" selection) drain(f) drain(pf))
  fprintf(f "SOT34_ALL102_ADJACENCY_COMPLETE\n") close(f) close(pf)
  f=outfile(strcat(dir "/SOT34_ADJACENCY_COMPLETE.txt")) fprintf(f "SOURCE_OR_TARGET102_NATIVE_PIN_NEIGHBORS_COMPLETE\n") close(f) t))
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
out=D/'sot34_adjacency_probe.il';assert not out.exists();out.write_text(s,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
