; Read only: all cached package definitions, including any unused entries.
procedure(pc13DefinitionInventoryOnly(dir)
 let((f d count instances unused)
  count=0 instances=0 unused=0
  f=outfile(strcat(dir "/ALL_PACKAGE_DEFINITIONS.tsv"))
  fprintf(f "name\tobjType\tusedCount\n")
  foreach(d axlDBGetDesign()->symdefs
   fprintf(f "%L\t%L\t%L\n" d->name d->objType length(d->instances))
   count=count+1 instances=instances+length(d->instances)
   when(null(d->instances) unused=unused+1))
  close(f)
  f=outfile(strcat(dir "/DEFINITION_INVENTORY_COMPLETE.txt"))
  fprintf(f "ALL_SAVED_PACKAGE_DEFINITIONS_READ_ONLY\nCOUNT=%d\nINSTANCES=%d\nUNUSED=%d\n" count instances unused)
  close(f)
  unless(count==59 && instances==1066 && unused==0 error("Final59 complete-definition cohort differs\n"))
  t))
