# Fresh-process persistence check; does not reuse the creation Session.
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
set ::C11DefinitionsOnly 1
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c11_design_exercise.tcl}
set code [catch {
    set root {D:/001DIY/005lib/01AIEDA/learning}
    set sess $::DboSession_s_pDboSession
    set s [DboState]
    set d [::C11Design::obj [$sess GetDesignAndSchematics [::C11Design::cs "$root/examples/lesson11_capture/run02/c11_basics.dsn"] $s] $s GetDesign]
    set result [::C11Design::snapshot $d "$root/logs/capture_C_20261019/c11_design_run02/07_fresh_process.tcldict"]
    if {[dict get $result root] ne "TOP" || [llength [dict get $result pages]]!=2} {error "Unexpected design hierarchy: $result"}
    set page1 [lindex [dict get $result pages] 0]
    set row [lindex [dict get $page1 instances] 0]
    if {[dict get $page1 name] ne "PAGE1" || [dict get $row reference] ne "U101" || [dict get $row location] ne {300 300}} {error "Restored instance differs: $page1"}
    if {[dict get $row footprint] ne "qmi8610_lga16_3d3_p0d5"} {error "Footprint association lost"}
    set inst [::C11Design::firstInstance $d]
    set pins {}; set iter [$inst NewPinsIter $s]
    for {set pin [$iter NextPin $s]} {$pin ne "NULL"} {set pin [$iter NextPin $s]} {
        lappend pins [::C11Design::str $pin GetPinNumber]
    }
    delete_DboPartInstPinsIter $iter
    if {[lsort -integer $pins] ne {1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16}} {error "Physical pin mapping differs: $pins"}
    ::C11Design::ok [$sess RemoveDesign $d] Close
    list PASS fresh_process [pid] pages 2 physical_pins $pins restored_location [dict get $row location]
} result options]
set f [open {D:/001DIY/005lib/01AIEDA/learning/logs/capture_C_20261019/c11_design_run02/fresh_reopen_result.tcldict} w]
fconfigure $f -encoding utf-8 -translation lf
puts $f [dict create code $code result $result]
if {$code} {puts $f [dict get $options -errorinfo]}
close $f
puts $result
exit $code
