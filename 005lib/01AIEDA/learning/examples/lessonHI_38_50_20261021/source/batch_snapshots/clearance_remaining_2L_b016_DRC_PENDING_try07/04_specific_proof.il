procedure(f29SpecificProof(out)
 let((f c v seen des)
  f=outfile(strcat(out "/specific_proof.tsv"))
  des=axlDBGetDesign()
  fprintf(f "CLASS_CLASS_HEADER\tclass1\tclass2\tspacing\tphysical1\tspacing1\telectrical1\tphysical2\tspacing2\telectrical2\n")
  foreach(c axlCnsClassTableFind('classClass)
   fprintf(f "CLASS_CLASS\t%s\t%s\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" c->netclass1->name c->netclass2->name c->spacing
    c->netclass1->physical c->netclass1->spacing c->netclass1->electrical
    c->netclass2->physical c->netclass2->spacing c->netclass2->electrical))
  seen=nil
  foreach(v axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
   when(equal(v->objType "via") && !member(v seen)
    seen=cons(v seen)
    fprintf(f "UNIQUE_VIA\t%L\t%L\t%L\t%L\t%L\n" v v->name v->xy v->net->name v->definition->usage)))
  fprintf(f "UNIQUE_VIA_COUNT\t%d\n" length(seen))
  fprintf(f "SPECIFIC_PROOF_COMPLETE\n")
  close(f) t))
