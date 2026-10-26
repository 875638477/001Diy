set f [open {D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/capture_all81_plan13/apply_all81_capture_footprints_only.tcl} r]
set s [read $f];close $f
if {![info complete $s]} {error {Tcl incomplete}}
source {D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/capture_all81_plan13/compiled/CAPTURE13_FROZEN_PLAN.tcl}
if {[dict size $footprintPlan] != 56 || [dict size $instanceGuards] != 3118 || [llength $sourceSelectors] != 231} {error {Unexpected counts}}
foreach row $sourceSelectors {if {[dict get $row old_source] ne [dict get $row new_source]} {error {Source mutation}}}
puts {PASS only Tcl syntax/data, noCAD}
