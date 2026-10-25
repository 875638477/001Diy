# One private native database process. No UI or shared session is used.
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
set script [lindex $argv 0]
set output [lindex $argv 1]
puts "C13 owned native batch PID [pid]"
flush stdout
set code [catch {source $script} result options]
set data [dict create script $script code $code result $result pid [pid] nativeVersion 17.2.2016045 tcl [info patchlevel]]
if {$code} {dict set data errorinfo [dict get $options -errorinfo]}
set f [open $output w]; fconfigure $f -encoding utf-8; puts $f $data; close $f
puts $data
exit $code
