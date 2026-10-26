load {C:/Program0/Cadence/SPB172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
if {[llength $argv] != 2} {error {Usage inputOLB freshOutputDirectory}}
lassign $argv input output
if {[file exists $output]} {error {Fresh output required}}
file mkdir $output
set s [XMATIC_OLB2XML $input [file join $output native_library.xml] {C:/Program0/Cadence/SPB172/tools/capture/tclscripts/capDB/olb.xsd} [file join $output export.log] 0]
if {[$s Failed]} {error {Native library export failed}}
puts {OLB_NATIVE_REOPEN_EXPORTED}