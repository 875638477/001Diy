procedure(jk55AllNetObjects()
 let((objects)
  objects=nil
  foreach(n axlDBGetDesign()->nets foreach(b n->branches foreach(c b->children foreach(o gConnectedObjects(c) unless(member(o objects) objects=cons(o objects))))))
  foreach(b axlDBGetLonelyBranches() foreach(c b->children foreach(o gConnectedObjects(c) unless(member(o objects) objects=cons(o objects)))))
  foreach(parent objects
   when(member(parent->objType list("path" "cline"))
    foreach(segment parent->segments unless(member(segment objects) objects=cons(segment objects)))))
  objects))
procedure(jkSegmentsRead(out)
 let((f p count thermal total)
  f=outfile(strcat(out "/actual_path_segments.tsv"))
  fprintf(f "net\tlayer\tstartEnd\twidth\tisEtch\tthermal\tparentType\n")
  count=0 thermal=0 total=0
  foreach(o jk55AllNetObjects()
   when(equal(o->objType "line") && o->isEtch
    p=o->parent total=total+1
    if(o->thermal || (p && p->thermal) then thermal=thermal+1 else count=count+1)
    fprintf(f "%L\t%L\t%L\t%L\t%L\t%L\t%L\n" jk55Name(o) o->layer o->startEnd o->width o->isEtch if(o->thermal || (p && p->thermal) then t else nil) if(p then p->objType else nil))))
  fprintf(f "ACTUAL_PATH_SEGMENTS_COMPLETE total=%d manual=%d generatedThermal=%d\n" total count thermal)
  unless(count>0 error("Manual segment traversal must be nonempty\n"))
  close(f)
  jkNewReferenceRead(out) t))
