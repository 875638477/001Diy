; Staging on an owned independent candidate copy only. Definitions do not execute.
procedure(pub13RestoreSourceClasses(dir)
 let((rows row d c count returned f saved)
  rows=list(list("CAP_C0402_100NF/0402/25V/10%_" "IC" "DISCRETE" 53) list("CAP_C0402_10NF/0402/16V/10%_" "IC" "DISCRETE" 3) list("CAP_C0402_10PF/0402/50V/5%_" "IC" "DISCRETE" 3) list("CAP_C0402_1NF/0402/50V/10%_" "IC" "DISCRETE" 6) list("CAP_C0402_1UF/0402/6.3V/10%_" "IC" "DISCRETE" 20) list("CAP_C0402_2.2UF/0402/6.3V/10%_" "IC" "DISCRETE" 1) list("CAP_C0402_4.7UF/0402/10V/10%_" "IC" "DISCRETE" 20) list("CAP_C0402_NC_10PF/0402/50V/5%_" "IC" "DISCRETE" 1) list("CAP_C0402_NC_1NF/0402/50V/10%_" "IC" "DISCRETE" 3) list("CAP_C0603_10UF/0603/16V/20%_" "IC" "DISCRETE" 8) list("CAP_C0603_1UF/0603/25V/10%_" "IC" "DISCRETE" 5) list("CAP_C0603_2.2UF/0603/25V/10%_" "IC" "DISCRETE" 2) list("CAP_C0603_4.7UF/0603/25V/10%_" "IC" "DISCRETE" 2) list("R_0_R0402_NC_0R/0402/1%_" "IC" "DISCRETE" 2) list("R_R0402_0R/0402/1%_" "IC" "DISCRETE" 49) list("R_R0402_100K/0402/1%_" "IC" "DISCRETE" 10) list("R_R0402_10K/0402/1%_" "IC" "DISCRETE" 32) list("R_R0402_1.3K/0402/1%_" "IC" "DISCRETE" 2) list("R_R0402_1K/0402/1%_" "IC" "DISCRETE" 8) list("R_R0402_20K/0402/1%_" "IC" "DISCRETE" 3) list("R_R0402_22K/0402/1%_" "IC" "DISCRETE" 1) list("R_R0402_22R/0402/1%_00000000004" "IC" "DISCRETE" 1) list("R_R0402_33R/0402/1%_" "IC" "DISCRETE" 49) list("R_R0402_40.2K/0402/1%_" "IC" "DISCRETE" 1) list("R_R0402_4.99K/0402/1%_" "IC" "DISCRETE" 12) list("R_R0402_5.1K/0402/1%_" "IC" "DISCRETE" 7) list("R_R0402_NC_1.3K/0402/1%_" "IC" "DISCRETE" 1) list("R_R0402_NC_1K/0402/1%_" "IC" "DISCRETE" 1) list("R_R1206_15R/1206/1%_" "IC" "DISCRETE" 2))
  f=outfile(strcat(dir "/EXACT_CLASS_RESTORE.txt"))
  fprintf(f "BOARD=008 PLAN_SHA256=C4BE6D8A3F6561E8A8700B7FA52368E8C7775AE050846B4575D92546B078DFE9\n")
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
