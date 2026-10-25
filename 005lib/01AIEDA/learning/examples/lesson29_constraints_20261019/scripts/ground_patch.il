
procedure(f29PatchGround(board out)
 let((f net c)
  f=outfile(out)
  f29Phys("P_GND_PLANE" "0.60 MM" "0.25 MM" "1 MM")
  foreach(c axlCnsList('physical)
   foreach(l list("L2" "L3")
    if(equal(c "P_GND_PLANE") then
     f29Must(axlCNSSetPhysical(c l 'allow_etch t) "GND layer copper/connection")
    else
     f29Must(axlCNSSetPhysical(c l 'allow_etch nil) "no signal or power cline in GND layers"))))
  net=axlDBFindByName('net "GND")
  axlDBAddProp(list(net) list(list("PHYSICAL_CONSTRAINT_SET" "P_GND_PLANE")))
  fprintf(f "GND_EXCEPTION=%L\n" axlDBGetProperties(net))
  unless(equal(cadr(assoc('PHYSICAL_CONSTRAINT_SET axlDBGetProperties(net))) "P_GND_PLANE") error("GND override failed\n"))
  fprintf(f "UPDATE=%L\n" axlDRCUpdate(t)) f29DumpDRC(f "FINAL_PATCHED")
  f29Must(axlSaveDesign(?design board ?noMru t ?noConfirm t) "final3save")
  fprintf(f "GROUND_PATCH_COMPLETE\n") close(f) t))
