; Read-only native database evidence, including unplaced logical component pins.
procedure(deBoardRead(out)
 let((f cf pf nf comp pin net)
  f=outfile(strcat(out "/native_summary.txt"))
  cf=outfile(strcat(out "/components.tsv"))
  pf=outfile(strcat(out "/component_pins.tsv"))
  nf=outfile(strcat(out "/nets.tsv"))
  unless(f && cf && pf && nf error("Cannot open native readback output\n"))
  fprintf(cf "refdes\tpackage\tdeviceType\tpins\tplaced\n")
  fprintf(pf "refdes\tpin\tnet\tphysical\n")
  fprintf(nf "net\tpins\n")
  foreach(comp axlDBGetDesign()->components
   fprintf(cf "%s\t%s\t%s\t%d\t%L\n" comp->name comp->package comp->deviceType length(comp->pins) if(comp->symbol then t else nil))
   foreach(pin comp->pins
    fprintf(pf "%s\t%s\t%s\t%L\n" comp->name pin->number if(pin->net then pin->net->name else "") if(pin->definition then t else nil))))
  foreach(net axlDBGetDesign()->nets
   fprintf(nf "%s\t%d\n" net->name length(net->pins)))
  fprintf(f "DE_BOARD_READ_COMPLETE\ndesign=%s\ncomponents=%d\nnets=%d\nsymbols=%d\ndrcs=%d\ndrcState=%L\n" axlCurrentDesign() length(axlDBGetDesign()->components) length(axlDBGetDesign()->nets) length(axlDBGetDesign()->symbols) length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState)
  close(cf) close(pf) close(nf) close(f)
  t))
