procedure(f29CouponConnections(out)
 let((f net pins c p)
  f=outfile(out)
  fprintf(f "kind\tnet_or_ref\tcount_or_pin\tunconnected_or_xy\tunplaced_or_net\n")
  foreach(net axlDBGetDesign()->nets
   pins=axlPinsOfNet(net 'pin)
   fprintf(f "NET\t%s\t%d\t%L\t%L\n" net->name length(pins) net->unconnected net->unplaced))
  foreach(c axlDBGetDesign()->components
   foreach(p c->pins fprintf(f "PIN\t%s\t%s\t%L\t%L\n" c->name p->number p->xy p->net->name)))
  fprintf(f "COUPON_CONNECTIONS_COMPLETE\n") close(f) t))
