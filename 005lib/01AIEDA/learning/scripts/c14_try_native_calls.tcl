error {Archived failed diagnostic is disabled. Native cache calls did not pass; use c14_controlled_update.tcl and the lesson14 record.}
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_helpers.tcl}
set s [::C12::session];set st [DboState]
set base {D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/run04}
set log {D:/001DIY/005lib/01AIEDA/learning/logs/lesson14_capture_20261019/run04}
set progress [open "$log/native_trial_progress.txt" w]; fconfigure $progress -buffering none
set results {}
foreach {branch name type} {native_part03 QMI8610_C12.Normal 24 native_package03 QMI8610_C12 31 native_replace03 QMI8610_C12 0 native_replace13 QMI8610_C12 1} {
 puts $progress "START $branch"
 set target "$base/${branch}.dsn";file copy "$base/c14_baseline.dsn" $target
 set d [$s GetDesignAndSchematics [::C12::cstring $target] $st]
 puts $progress "DESIGN $d"
 set old {D:\001DIY\005LIB\01AIEDA\LEARNING\EXAMPLES\LESSON14_CAPTURE\RUN04\C14_SOURCE_V1.OLB}
 set new {D:\001DIY\005LIB\01AIEDA\LEARNING\EXAMPLES\LESSON14_CAPTURE\RUN04\C14_RELOCATED_V2.OLB}
 if {[string match native_replace* $branch]} {
  set r [$d ReplaceCache [::C12::cstring $name] [::C12::cstring $old] [::C12::cstring $name] [::C12::cstring $new] $type 1]
 } else {
  set r [$d UpdateCache [::C12::cstring $old] [::C12::cstring $name] $type 1]
 }
 puts $progress "RETURNED $r"
 set failed [$r Failed];puts $progress "FAILED $failed"
 dict set results $branch [dict create failed $failed code [$r Code]]
 puts $progress "CODE READ"
 set pkg [$d GetPackage [::C12::cstring QMI8610_C12] $st]
 ::C14Research::snapshotPackage $pkg "$log/${branch}.tcldict"
 puts $progress "SNAPSHOT"
 $s RemoveDesign $d
}
close $progress
set results
