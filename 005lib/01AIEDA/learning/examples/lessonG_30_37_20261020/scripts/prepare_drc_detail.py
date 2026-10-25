from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
p=R/'scripts/placementG.il';s=p.read_text()
s=s.replace('  fprintf(df "G_SNAPSHOT_COMPLETE\\n")','''  foreach(drc axlDBGetDesign()->drcs
   foreach(v drc->violations
    fprintf(df "VIOLATION_OBJECT\\tref=%L\\t%L\\n" if(equal(v->objType "pin") then v->parent->refdes else nil) v->??)))
  fprintf(df "G_SNAPSHOT_COMPLETE\\n")''')
p.write_text(s,encoding='ascii')
print('DRC_OBJECT_DETAIL_READY')
