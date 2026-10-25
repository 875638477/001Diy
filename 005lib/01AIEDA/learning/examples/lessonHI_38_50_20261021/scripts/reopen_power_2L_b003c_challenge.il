
procedure(hiStarNeckChallenge()
 let((f names count)
  f=outfile("D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/logs/reopen_power_2L_b003c/hi_star_neck_challenge.txt")
  names=list("HI_U1_INNER_LEFT_P_2L" "HI_U1_INNER_SOUTH_P_2L")
  foreach(name names
   unless(equal(axlCNSGetPhysical(name "TOP" 'necklength_max) 1.4) error("Unexpected normal star neck rule\n"))
   unless(axlCNSSetPhysical(name nil 'necklength_max "1.3 MM") error("Cannot restore controlled strict star neck\n")))
  axlDRCUpdate(t) axlDBRefreshId(nil) f29DumpDRC(f "STAR_LOCAL_STRICT_1P3")
  count=length(axlDBGetDesign()->drcs)
  unless(count==2 error("Expected exactly two old outward-neck violations under overlapping new regions\n"))
  foreach(name names
   unless(axlCNSSetPhysical(name nil 'necklength_max "1.4 MM") error("Cannot restore approved star neck\n")))
  axlDRCUpdate(t) axlDBRefreshId(nil) f29DumpDRC(f "STAR_LOCAL_RESTORED_1P4")
  unless(length(axlDBGetDesign()->drcs)==0 error("Star neck restore did not clear DRC\n"))
  foreach(name names
   fprintf(f "RESTORED_CSET=%L width=%L neck=%L limit=%L\n" name axlCNSGetPhysical(name "TOP" 'width_min) axlCNSGetPhysical(name "TOP" 'neckwidth_min) axlCNSGetPhysical(name "TOP" 'necklength_max)))
  fprintf(f "HI_STAR_NECK_CHALLENGE_COMPLETE_NO_SAVE\n") close(f) t))
