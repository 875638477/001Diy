from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
base=R/'scripts'
p=base/'correction.il'
p.write_text(p.read_text()+r'''
procedure(fcorOutline(out)
 let((f d obj poly)
  f=outfile(strcat(out "/outline_exact.tsv"))
  d=axlDBGetDesign()
  fprintf(f "role\tlayer\tbbox\tfilled\tvertices\n")
  foreach(layer list("BOARD GEOMETRY/DESIGN_OUTLINE" "BOARD GEOMETRY/OUTLINE")
   foreach(obj axlDBGetShapes(layer)
    poly=car(axlPolyFromDB(obj))
    fprintf(f "%L\t%L\t%L\t%L\t%L\n" if(equal(obj d->designOutline) then "AUTHORITATIVE_ROOT" else "NON_ROOT_COPY") obj->layer obj->bBox obj->fill poly->vertices)))
  fprintf(f "FCOR_OUTLINE_COMPLETE\n")
  close(f) t))
''',encoding='ascii')
for key in ['F28_2L','F28_4L','F29']:
 s=(base/f'reopen_{key}.scr').read_text()
 a=s.index('skill errset(fcorRead(');b=s.index('\nquit',a)
 s=s[:a]+f'skill errset(fcorOutline("{R.as_posix()}/logs/outline_{key}") t)'+s[b:]
 (base/f'outline_{key}.scr').write_text(s,encoding='ascii')
old=(R.parent/'lesson29_constraints_20261019/scripts/export_tcf.py').read_text()
old=old.replace("lesson29_constraints_20261019'","lessonF_stack_artwork_correction_20261019'")
old=old.replace("native/F29_CONSTRAINTS_v3.brd","current/F29_CONSTRAINTS_v4.brd").replace('F29_RULES.tcf','F29_RULES_v4.tcf')
(base/'export_tcf_v4.py').write_text(old,encoding='ascii')
print('SUPPLEMENTAL_AND_TCF_READY')
