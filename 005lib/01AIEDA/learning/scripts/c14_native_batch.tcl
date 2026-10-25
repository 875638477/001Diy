load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
if {$::DboSession_s_pDboSession eq "NULL"} {error "Native session is NULL"}
DboSession -this $::DboSession_s_pDboSession
set code [catch {source [lindex $argv 0]} result opts]
set cleanup {}
set cleanupState [DboState]
set session $::DboSession_s_pDboSession
set designs [$session NewDesignsIter $cleanupState]
set object [$designs NextDesign $cleanupState]
set toClose {}
while {$object ne "NULL"} {lappend toClose $object;set object [$designs NextDesign $cleanupState]}
delete_DboSessionDesignsIter $designs
foreach object $toClose {lappend cleanup [list design $object [catch {$session RemoveDesign $object} why] $why]}
set libs [$session NewLibsIter $cleanupState]
set object [$libs NextLib $cleanupState]
set toClose {}
while {$object ne "NULL"} {lappend toClose $object;set object [$libs NextLib $cleanupState]}
delete_DboSessionLibsIter $libs
foreach object $toClose {lappend cleanup [list lib $object [catch {$session RemoveLib $object} why] $why]}
set f [open [lindex $argv 1] w]
fconfigure $f -encoding utf-8 -translation lf
puts $f [dict create code $code result $result options $opts cleanup $cleanup executable [info nameofexecutable] tcl [info patchlevel]]
close $f
puts [dict create code $code result $result]
exit $code
