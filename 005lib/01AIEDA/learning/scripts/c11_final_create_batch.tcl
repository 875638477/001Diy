load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
set code [catch {source {D:/001DIY/005lib/01AIEDA/learning/scripts/c11_design_exercise.tcl}} result options]
file mkdir {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c11_final}
set f [open {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c11_final/create_result.tcldict} w]
fconfigure $f -encoding utf-8 -translation lf
puts $f [dict create code $code result $result]
if {$code} {puts $f [dict get $options -errorinfo]}
close $f
puts $result
exit $code
