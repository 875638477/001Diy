
procedure(l28More(out)
 let((f pf sf s p ps layer v)
 f=outfile(strcat(out "/placed_pins.tsv"))
 pf=outfile(strcat(out "/placed_pads.tsv"))
 sf=outfile(strcat(out "/padstacks.tsv"))
 fprintf(f "symbol\trefdes\ttype\tanchor\tpin\txy\tpadstack\tmechanical\tthrough\tholeType\tplating\tdrill\tdrillX\tdrillY\n")
 fprintf(pf "symbol\trefdes\tpin\txy\tpadstack\tlayer\tfigure\tbbox\n")
 fprintf(sf "name\tusage\tthrough\tstartEnd\tholeType\tplating\tdrill\tdrillX\tdrillY\n")
 foreach(ps axlDBGetDesign()->padstacks
  fprintf(sf "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" ps->name ps->usage ps->isThrough ps->startEnd ps->holeType ps->plating ps->drillDiameter ps->drillSizeWidth ps->drillSizeHeight))
 foreach(s axlDBGetDesign()->symbols
  foreach(p s->pins
   ps=p->definition
   fprintf(f "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" s->name s->refdes s->type s->xy p->number p->xy p->name p->isMech p->isThrough ps->holeType ps->plating ps->drillDiameter ps->drillSizeWidth ps->drillSizeHeight)
   foreach(layer list("ETCH/TOP" "ETCH/L2" "ETCH/L3" "ETCH/BOTTOM")
    when(axlIsLayer(layer)
     v=axlDBGetPad(p layer "REGULAR")
     fprintf(pf "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" s->name s->refdes p->number p->xy p->name layer if(v then v->figureName else nil) if(v then v->bBox else nil))))))
 foreach(p list(f pf sf) close(p)) t))
