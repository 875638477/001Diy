set f [open {D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/capture_cache7_plan13/v2/apply_capture_cache7_defaults_only_v2.tcl} r]
set s [read $f];close $f
if {![info complete $s]} {error {IncompleteTcl}}
source {D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/capture_cache7_plan13/compiled/CAPTURE13_FROZEN_PLAN.tcl}
if {[dict size $cacheDefaultPlan]!=7 || [dict size $footprintPlan]!=0} {error {Wrongcounts}}
puts {PASS Tclsyntax/data only;noCAD}
