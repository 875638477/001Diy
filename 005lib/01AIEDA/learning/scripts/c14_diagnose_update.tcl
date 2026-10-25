error {Archived failed diagnostic is disabled. Do not rerun cache probes that can yield invalid native objects.}
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_helpers.tcl}
set C14s [::C12::session]; set C14st [DboState]
set C14base {D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/run04}
set C14lib [$C14s GetLib [::C12::cstring "$C14base/c14_relocated_v2.olb"] $C14st]
set C14pkg [$C14lib GetPackage [::C12::cstring QMI8610_C12] $C14st]
::C14Research::snapshotPackage $C14pkg D:/001DIY/005lib/01AIEDA/learning/logs/lesson14_capture_20261019/run04/source_v2_trial02.tcldict
set C14res {}
foreach {C14branch C14kind} {diag_pkg02 31 diag_part02 24 diag_replace02 0 diag_replace12 1} {
 set C14target "$C14base/$C14branch.dsn"
 file copy "$C14base/c14_baseline.dsn" $C14target
 set C14des [$C14s GetDesignAndSchematics [::C12::cstring $C14target] $C14st]
 set C14old {D:\001DIY\005LIB\01AIEDA\LEARNING\EXAMPLES\LESSON14_CAPTURE\RUN04\C14_SOURCE_V1.OLB}
 set C14new {D:\001DIY\005LIB\01AIEDA\LEARNING\EXAMPLES\LESSON14_CAPTURE\RUN04\C14_RELOCATED_V2.OLB}
 if {[string match *replace* $C14branch]} {
  set C14r [$C14des ReplaceCache [::C12::cstring QMI8610_C12] [::C12::cstring $C14old] [::C12::cstring QMI8610_C12] [::C12::cstring $C14new] $C14kind 1]
 } else {
  set C14name QMI8610_C12
  if {$C14kind==24} {set C14name QMI8610_C12.Normal}
  set C14r [$C14des UpdateCache [::C12::cstring $C14old] [::C12::cstring $C14name] $C14kind 1]
 }
 set C14msg [::C12::cstring ""]
 $C14r Message $C14msg
 dict set C14res $C14branch [dict create failed [$C14r Failed] code [$C14r Code] severity [$C14r Severity] message [DboTclHelper_sGetConstCharPtr $C14msg]]
 set C14cp [$C14des GetPackage [::C12::cstring QMI8610_C12] $C14st]
 ::C14Research::snapshotPackage $C14cp "D:/001DIY/005lib/01AIEDA/learning/logs/lesson14_capture_20261019/run04/${C14branch}.tcldict"
 $C14s RemoveDesign $C14des
}
$C14s RemoveLib $C14lib
set C14res
