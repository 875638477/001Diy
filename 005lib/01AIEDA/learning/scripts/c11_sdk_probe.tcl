set root {D:/001DIY/005lib/01AIEDA/learning}
set report [open [file join $root logs capture_C_20261019 sdk_probe.txt] w]
fconfigure $report -encoding utf-8 -buffering line
puts $report [list START [info patchlevel] [info nameofexecutable]]
set dll {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll}
set code [catch {load $dll DboTclWriteBasic} result options]
puts $report [list LOAD code $code result $result]
if {$code} {puts $report [dict get $options -errorinfo]}
puts $report [list PACKAGES [package names]]
puts $report [list DBO_COMMAND_COUNT [llength [info commands Dbo*]]]
puts $report [list SESSION_GLOBALS [info globals *DboSession*]]
if {[info exists ::DboSession_s_pDboSession]} {puts $report [list SESSION $::DboSession_s_pDboSession]}
puts $report COMPLETE
close $report
exit
