
procedure(hiScopedPhysicalNeckChallenge(out name netName)
 let((f net before count hits strictCount result)
  f=outfile(strcat(out "/strict_neck_" netName ".txt")) net=axlDBFindByName('net netName) before=axlCNSGetPhysical(name "TOP" nil)
  unless(abs(axlCNSGetPhysical(name "TOP" 'necklength_max)-2.0)<0.00001 error("Normal local neck budget differs\n"))
  count=axlDRCItem(nil net) fprintf(f "NECK_NORMAL_BEFORE net=%L cset=%L result=%L allTOPFields=%L\n" netName name count before)
  unless(numberp(count) && count==0 error("Normalized route still violates normal rules\n"))
  unwindProtect(progn(
   unless(axlCNSSetPhysical(name "TOP" 'necklength_max 1.7) error("Cannot tighten local physical neck only\n"))
   strictCount=axlDRCItem(nil net) hits=nil f29DumpDRC(f "PAD_INTERNAL_NORMALIZATION_STRICT_NATIVE")
   foreach(d axlDBGetDesign()->drcs
    when(equal(d->name "Maximum Neck Length") && equal(d->source name) && d->actual && abs(atof(d->actual)-1.7414)<0.001 && d->expected && abs(atof(d->expected)-1.7)<0.0001
     hits=cons(d hits) fprintf(f "NATIVE_NORMALIZED_NECK_ACTUAL=%L\n" d->??)))
   unless(numberp(strictCount) && strictCount>0 && hits error("Stricter1.7 did not expose expected1.7414 native neck\n")) t)
   progn(
    axlCNSSetPhysical(name "TOP" 'necklength_max 2.0) result=axlDRCItem(nil net)
    fprintf(f "NECK_NORMAL_RESTORED result=%L allTOPFieldsExactlyRestored=%L actualNeckBudget=%L\n" result equal(before axlCNSGetPhysical(name "TOP" nil)) axlCNSGetPhysical(name "TOP" 'necklength_max))
    unless(numberp(result) && result==0 && equal(before axlCNSGetPhysical(name "TOP" nil)) error("Neck strict challenge restore failed\n"))))
  fprintf(f "NATIVE_NECK_NORMALIZATION_CHALLENGE_COMPLETE EXTERIOR_NARROW_COPPER_NOT_SHORTENED=t\n") close(f) t))
