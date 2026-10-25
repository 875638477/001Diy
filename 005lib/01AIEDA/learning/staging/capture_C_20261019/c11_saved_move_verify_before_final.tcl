load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
set ::C11DefinitionsOnly 1
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c11_design_exercise.tcl}
set code [catch {
 set root {D:/001DIY/005lib/01AIEDA/learning}
 set path "$root/examples/lesson11_capture/run02/c11_saved_move_marked.dsn"
 if {[file exists $path]} {error "Refuse to overwrite saved-move exercise"}
 file copy "$root/examples/lesson11_capture/run02/c11_basics_baseline.dsn" $path
 set sess $::DboSession_s_pDboSession; set s [DboState]
 set d [::C11Design::obj [$sess GetDesignAndSchematics [::C11Design::cs $path] $s] $s OpenCopy]
 set inst [::C11Design::firstInstance $d]
 ::C11Design::ok [$inst SetLocation [DboTclHelper_sMakeCPoint 500 450]] Move
 ::C11Design::ok [$inst MarkModified] MarkInstanceModified
 set top [$d GetRootSchematic $s]
 set page [::C11Design::obj [$top GetPage [::C11Design::cs PAGE1] $s] $s Page]
 ::C11Design::ok [$page MarkModified] MarkPageModified
 ::C11Design::ok [$top SavePage $page] SavePage
 ::C11Design::ok [$sess SaveDesign $d] SaveDesign
 ::C11Design::ok [$sess RemoveDesign $d] Close
 set d [::C11Design::obj [$sess GetDesignAndSchematics [::C11Design::cs $path] $s] $s ReopenCopy]
 set report [::C11Design::snapshot $d "$root/logs/capture_C_20261019/c11_design_run02/08_saved_move_reopened.tcldict"]
 set row [lindex [dict get [lindex [dict get $report pages] 0] instances] 0]
 if {[dict get $row location] ne {500 450}} {error "Saved move was not persistent"}
 ::C11Design::ok [$sess RemoveDesign $d] CloseFinal
 list PASS saved_and_reopened_location [dict get $row location] reference [dict get $row reference]
} result options]
set f [open {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c11_design_run02/saved_move_result.tcldict} w]
puts $f [dict create code $code result $result]
if {$code} {puts $f [dict get $options -errorinfo]}
close $f
puts $result
exit $code
