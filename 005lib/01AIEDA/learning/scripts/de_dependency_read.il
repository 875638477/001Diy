procedure(deDependencyRead(out)
 let((f s p layer pad box summary)
  f=outfile(strcat(out "/pins.tsv"))
  unless(f error("Output unavailable\n"))
  fprintf(f "package\tpin\tpadstack\tx\ty\tmechanical\tlayer\tfigure\tw\th\tdrill\tholeType\tplating\n")
  foreach(s axlDBGetDesign()->symbols
   foreach(p s->pins
    foreach(layer list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
     pad=axlDBGetPad(p layer "REGULAR")
     box=if(pad then pad->bBox else nil)
     fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
      s->name p->number p->name car(p->relxy) cadr(p->relxy) p->isMech layer if(pad then pad->figureName else nil)
      if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
      p->definition->drillDiameter p->definition->holeType p->definition->plating))))
  close(f)
  summary=outfile(strcat(out "/summary.txt"))
  fprintf(summary "DE_DEPENDENCY_READ_COMPLETE\npackages=%d\nunits=%L\ndrcs=%d\ndrcState=%L\npsmpath=%L\npadpath=%L\n" length(axlDBGetDesign()->symbols) axlDBGetDesignUnits() length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState axlGetVariableList("psmpath") axlGetVariableList("padpath"))
  close(summary)
  t))
