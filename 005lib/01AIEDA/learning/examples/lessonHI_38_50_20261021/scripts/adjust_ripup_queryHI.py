from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_exact_ripup_v2.il';s=p.read_text();a=s.index('   if(equal(type "deleteVia")');b=s.index('   unless(length(matches)==1',a);s=s[:a]+'''   if(equal(type "deleteVia") then matches=list(hiUniqueVia(net geom value)) else matches=hiFindExactManualLine(net layer geom value))
'''+s[b:]
s='''procedure(hiFindExactManualLine(net layer points width)
 let((matches seen obj)
  matches=nil seen=nil
  foreach(obj axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
   unless(member(obj seen)
    seen=cons(obj seen)
    when(equal(obj->objType "line") && obj->isEtch && obj->net && equal(obj->net->name net) && equal(obj->layer strcat("ETCH/" layer)) && abs(obj->width-width)<0.00001 && (equal(obj->startEnd points) || equal(reverse(obj->startEnd) points))
     matches=cons(obj matches))))
  matches))
'''+s
p.write_text(s,encoding='ascii')
p=R/'scripts/prepare_exact_ripup_pilotHI.py';s=p.read_text(encoding='utf-8-sig').replace('exact_batch_ripup_pilot_2L_04','exact_batch_ripup_pilot_2L_05');p.write_text(s,encoding='utf8')
