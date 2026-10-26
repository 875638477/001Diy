set m {D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/capture_sot34_plan_v1}
set f [open [file join $m apply_capture13_footprints_only.tcl] r]
set script [read $f];close $f
if {![info complete $script]} {error {Native script Tcl syntax incomplete}}
source [file join $m compiled_v2 CAPTURE13_FROZEN_PLAN.tcl]
if {[dict size $footprintPlan] != 34 || [dict size $instanceGuards] != 3118 || [llength $sourceSelectors] != 231} {error {Unexpected guard/change count}}
foreach row $sourceSelectors {if {[dict get $row old_source] ne [dict get $row new_source]} {error {Source selector mutation forbidden}}}
dict for {k row} $instanceGuards {if {[dict get $row old_source] ne [dict get $row new_source]} {error {Source instance mutation forbidden}}}
puts {PASS Tcl syntactic completion, exact34FP/3118guard/231cache, source edits0; no CAD or native setter invoked}
