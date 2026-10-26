; Definitions only. Root executes on an owned independent006 candidate copy.
; No save. Purpose is to test documented axlComponentChangeClass availability
; in this Allegro product, not to approve or publish any module.
procedure(pub13ClassCanary(dir)
 let((d f c dt result before after count)
  d=axlDBGetDesign() unless(d error("No active module006 candidate\n"))
  dt="CAP_C0402_1NF_" count=0
  f=outfile(strcat(dir "/CLASS_CANARY.txt"))
  foreach(c d->components when(c->deviceType==dt
   count=count+1 fprintf(f "BEFORE_REF=%L COMPONENT_CLASS=%L COMPDEF=%L\n" c->name c->class c->compdef->??)))
  unless(count>0 close(f) error("Exact006 canary device absent\n"))
  result=errset(axlComponentChangeClass(dt "DISCRETE") t)
  fprintf(f "CALL_RESULT=%L\n" result)
  d=axlDBGetDesign()
  foreach(c d->components when(c->deviceType==dt
   fprintf(f "AFTER_REF=%L COMPONENT_CLASS=%L COMPDEF=%L\n" c->name c->class c->compdef->??)))
  fprintf(f "SAVE_CALLS=0\nSOURCE_PROTECTION_BY_OWNED_WRAPPER_REQUIRED\n") close(f)
  unless(result error("Documented class setter unavailable/failed in this product\n"))
  f=outfile(strcat(dir "/CLASS_CANARY_COMPLETE.txt")) fprintf(f "COMPLETE_NATIVE_API_CANARY_ONLY\n") close(f) t))
