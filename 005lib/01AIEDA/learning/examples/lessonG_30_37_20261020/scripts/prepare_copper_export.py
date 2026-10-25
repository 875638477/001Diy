from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
p=R/'scripts/placementG.il'
s=p.read_text()
s=s.replace('  f29DumpDRC(df "G_SNAPSHOT")','  gCopperRead(out)\n  f29DumpDRC(df "G_SNAPSHOT")')
s+=r'''
procedure(gCopperRead(out)
 let((f poly shape)
  f=outfile(strcat(out "/g_copper_shapes.tsv"))
  fprintf(f "layer\tnet\tfilled\tboundary\tgenerated\tfillOOD\tbbox\tarea\tvertices\tholes\n")
  foreach(shape axlDBGetShapes("ETCH")
   foreach(poly axlPolyFromDB(shape)
    fprintf(f "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" shape->layer if(shape->net then shape->net->name else nil) shape->fill shape->shapeIsBoundary if(shape->shapeBoundary then t else nil) shape->fillOOD shape->bBox poly->area poly->vertices mapcar(lambda((h) h->vertices) poly->holes))))
  close(f) t))
'''
p.write_text(s,encoding='ascii')
print('COPPER_POLYGON_EXPORT_READY')
