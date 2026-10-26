; Staging on an owned independent candidate copy only. Definitions do not execute.
procedure(pub13RestoreSourceClasses(dir)
 let((rows row d c count returned f saved)
  rows=list(list("CAP_C0402_1NF_" "IC" "DISCRETE" 3) list("CAP_C0402_NC_12PF_" "IC" "DISCRETE" 1) list("CAP_C0402_NC_1.8PF_" "IC" "DISCRETE" 1) list("R_R0402_10K_" "IC" "DISCRETE" 18) list("R_R0402_1K_" "IC" "DISCRETE" 17) list("R_R0402_33R_" "IC" "DISCRETE" 7) list("R_R0402_NC_4.7K_" "IC" "DISCRETE" 5))
  f=outfile(strcat(dir "/EXACT_CLASS_RESTORE.txt"))
  fprintf(f "BOARD=006 PLAN_SHA256=1479D7321EE1F5546996E6BA1350DDDA4B0C52E5D30503AE3E3FEFB214A6320F\n")
  foreach(row rows
   d=axlDBGetDesign() count=0
   foreach(c d->components when(c->deviceType==car(row)
    count=count+1 unless(equal(c->class cadr(row)) close(f) error("Candidate CLASS precondition failed\n"))))
   unless(count==cadddr(row) close(f) error("Exact primitive/ref cohort count failed\n"))
   returned=axlComponentChangeClass(car(row) caddr(row))
   fprintf(f "DEVICE=%L BEFORE_RETURNED=%L AFTER_PLANNED=%L REFS=%d\n" car(row) returned caddr(row) count) drain(f)
   unless(equal(returned cadr(row)) close(f) error("Official class setter failed or wrong original class\n"))
   d=axlDBGetDesign() count=0
   foreach(c d->components when(c->deviceType==car(row)
    count=count+1 unless(equal(c->class caddr(row)) close(f) error("Immediate class readback failed\n"))))
   unless(count==cadddr(row) close(f) error("Post-class exact refs changed\n")))
  saved=axlDBSave(strcat(dir "/CLASS_RESTORED.brd")) fprintf(f "SAVE=%L\n" saved) close(f)
  unless(saved error("Staging class-restored save failed\n"))
  f=outfile(strcat(dir "/CLASS_RESTORE_COMPLETE.txt")) fprintf(f "COMPLETE_EXACT_SOURCE_CLASS_RESTORE_NATIVE_STAGING_ONLY\n") close(f) t))
