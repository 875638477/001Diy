from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_exact_ripup_v2.il';s=p.read_text();a=s.index('   matches=nil seen=nil');b=s.index('   unless(length(matches)==1',a)
s=s[:a]+'''   matches=nil seen=nil
   if(equal(type "deleteVia") then
    matches=list(hiUniqueVia(net geom value))
   else
    foreach(o objects
     unless(member(o seen)
      seen=cons(o seen)
      when(equal(o->objType "line") && o->isEtch && o->net && equal(o->net->name net) && equal(o->layer strcat("ETCH/" layer)) && abs(o->width-value)<0.00001 && (equal(o->startEnd geom) || equal(reverse(o->startEnd) geom))
       matches=cons(o matches)))))
'''+s[b:];p.write_text(s,encoding='ascii')
p=R/'scripts/prepare_exact_ripup_pilotHI.py';s=p.read_text(encoding='utf-8-sig').replace('exact_batch_ripup_pilot_2L_03','exact_batch_ripup_pilot_2L_04');p.write_text(s,encoding='utf8')
