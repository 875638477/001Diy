# A startup-only probe for the documented Capture command-line entry point.
# It does not open or modify a user design.
set report [dict create executable [info nameofexecutable] pid [pid] tcl [info patchlevel] dbo_commands [llength [info commands Dbo*]] menu_commands [llength [info commands Menu]]]
if {[info exists ::DboSession_s_pDboSession]} {dict set report native_session $::DboSession_s_pDboSession}
set out [open {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/gui_probe/boot.tcldict} w]
fconfigure $out -encoding utf-8 -translation lf
puts $out $report
close $out
