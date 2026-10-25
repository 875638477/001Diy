
procedure(hiTerminalKey(p)
 sprintf(nil "%s.%s" p->parent->refdes p->number))
procedure(hiNetworkInventory(out)
 let((f tf bf gf sf des allpins net pins pending seed graph terminals index ncomp minjoin totalUnc totalJoins netcount)
  des=axlDBGetDesign()
  axlDBRefreshId(nil)
  f=outfile(strcat(out "/hi_net_connectivity.tsv"))
  tf=outfile(strcat(out "/hi_component_terminals.tsv"))
  bf=outfile(strcat(out "/hi_native_branches.txt"))
  gf=outfile(strcat(out "/hi_graph_objects.tsv"))
  sf=outfile(strcat(out "/hi_network_summary.txt"))
  fprintf(f "net\tterminalCount\tterminalComponents\tminTerminalJoins\tnativeUnconnected\tnativeBranches\tunplaced\tratsnestCount\n")
  fprintf(tf "net\tcomponent\trefdes\tpin\tterminal\txy\tthrough\tpadstack\tgraphObjects\n")
  fprintf(gf "net\tcomponent\tobject\ttype\tlayer\tattributes\n")
  allpins=nil totalUnc=0 totalJoins=0 netcount=0
  foreach(c des->components
   unless(c->symbol error("HI baseline has unplaced component %s\n" c->name))
   foreach(p c->symbol->pins when(p->net allpins=cons(p allpins))))
  foreach(net des->nets
   pins=setof(p allpins equal(p->net net))
   pending=pins index=0
   fprintf(bf "NET %L nativeUnconnected=%L branches=%L unplaced=%L ratsnest=%L attrs=%L\n" net->name net->unconnected net->nBranches net->unplaced length(net->ratsnest) net->??)
   foreach(b net->branches fprintf(bf "BRANCH %L\n" b->??))
   while(pending
    seed=car(pending) graph=gConnectedObjects(seed)
    terminals=setof(p pending member(p graph))
    unless(terminals error("Terminal graph does not contain seed\n"))
    index=index+1
    foreach(p terminals
     fprintf(tf "%L\t%d\t%L\t%L\t%L\t%L\t%L\t%L\t%d\n" net->name index p->parent->refdes p->number hiTerminalKey(p) p->xy p->isThrough p->name length(graph)))
    foreach(obj graph
     fprintf(gf "%L\t%d\t%L\t%L\t%L\t%L\n" net->name index obj obj->objType obj->layer obj->??))
    pending=setof(p pending !member(p terminals)))
   minjoin=max(0 index-1)
   fprintf(f "%L\t%d\t%d\t%d\t%L\t%L\t%L\t%d\n" net->name length(pins) index minjoin net->unconnected net->nBranches net->unplaced length(net->ratsnest))
   totalUnc=totalUnc+net->unconnected totalJoins=totalJoins+minjoin netcount=netcount+1)
  fprintf(sf "NETS=%d\nACTUAL_NETTED_PHYSICAL_TERMINALS=%d\nNATIVE_REMAINING_CONNECTIONS=%d\nGRAPH_MIN_TERMINAL_JOINS=%d\nLONELY_UNNETTED_BRANCHES=%L\n" netcount length(allpins) totalUnc totalJoins axlDBGetLonelyBranches())
  f29DumpDRC(sf "HI_BASELINE")
  fprintf(sf "HI_NETWORK_INVENTORY_COMPLETE\n")
  foreach(o list(f tf bf gf sf) close(o))
  t))
