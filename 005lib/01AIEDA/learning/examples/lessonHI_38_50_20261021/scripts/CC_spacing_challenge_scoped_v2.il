procedure(hiCCSpacingChallenge(out)
 let((f name result hit hasCC net)
  f=outfile(strcat(out "/hi_cc_spacing_challenge.txt")) name="HI_USB_CC1_J2_S_2L" hit=nil net=axlDBFindByName('net "USB_CC1")
  unless(net error("CC1 challenge target net absent\n"))
  foreach(key list('smdpin_line 'line_line) unless(abs(axlCNSGetSpacing(name "TOP" key)-0.2)<0.00001 error("Unexpected baseline scopedCC spacing\n")))
  unwindProtect(progn(
   foreach(key list('smdpin_line 'line_line) unless(axlCNSSetSpacing(name nil key "0.4 MM") error("Cannot tighten scoped CC rule\n")))
   axlDBControl('drcEnable t)
   fprintf(f "CC_STRICT_REQUEST scope=USB_CC1_ONLY_API_axlDRCItem_nil time=%L cset=%L twoFieldsNormal=.2 strict=.4 online=%L\n" getCurrentTime() name axlDBControl('drcEnable)) drain(f)
   result=axlDRCItem(nil net) fprintf(f "CC_STRICT_RETURN time=%L result=%L\n" getCurrentTime() result) f29DumpDRC(f "CC1_STRICT_040")
   unless(numberp(result) error("Strict scopedCC DRC did not return numeric result\n"))
   foreach(d axlDBGetDesign()->drcs
    hasCC=nil
    foreach(obj d->violations when(obj->net && equal(obj->net->name "USB_CC1") hasCC=t))
    when(hasCC && abs(atof(d->expected)-0.4)<0.00011 && abs(atof(d->actual)-0.3)<0.00011 hit=t fprintf(f "CC1_REAL_030_NATIVE_DRC=%L\n" d->??)))
   unless(hit error("Tightened CC1 rule did not catch planned real0.3mm gap\n"))
   t) progn(
    foreach(key list('smdpin_line 'line_line) unless(axlCNSSetSpacing(name nil key "0.2 MM") error("Cannot restore scopedCC rule\n")))
    result=axlDRCItem(nil net) fprintf(f "CC_RESTORED_RETURN time=%L result=%L storedDRCs=%d\n" getCurrentTime() result length(axlDBGetDesign()->drcs)) f29DumpDRC(f "CC1_RESTORED_020")
    unless(numberp(result) && result==0 error("Restored scoped CC rule did not recover zero DRC on USB_CC1\n"))))
  fprintf(f "CC1_SPACING_CHALLENGE_COMPLETE_REAL030_CAUGHT_THEN_RESTORED020_SCOPED_NET_ONLY_FULL_BOARD_CHECK_FOLLOWS\n") close(f) t))
