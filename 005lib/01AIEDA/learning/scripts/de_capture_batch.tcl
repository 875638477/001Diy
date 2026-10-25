if {$argc!=2} {error "Usage: de_capture_batch.tcl job.tcl result.tcldict"}
set job [file normalize [lindex $argv 0]];set output [file normalize [lindex $argv 1]]
foreach path [list $job $output] {
 if {![string match {d:/001diy/005lib/01aieda/learning/*} [string tolower [string map {\\ /} $path]]]} {error "Path outside learning"}
}
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
if {$::DboSession_s_pDboSession eq "NULL"} {error "Native session unavailable"}
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set code [catch {source $job} result options]
::DE::cleanup
set report [dict create pid [pid] code $code result $result execution standalone_Capture_17_2_database_SDK]
if {$code} {dict set report errorinfo [dict get $options -errorinfo]}
::DE::write $output $report
puts $report
exit $code
