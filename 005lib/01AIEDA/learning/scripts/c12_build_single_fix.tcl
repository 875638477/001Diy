set root {D:/001DIY/005lib/01AIEDA/learning}
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source [file join $root scripts c12_helpers.tcl]
set code [catch {
    set a [::C12::CreateQmi8610 [file join $root examples lesson12_capture c12_qmi8610_single.olb] QMI8610_C12_SINGLE HOST_I2C]
    set b [::C12::CreateQmi8610 [file join $root examples lesson12_capture c12_qmi8610_spi4_single.olb] QMI8610_C12_SPI4_SINGLE HOST_SPI4]
    dict create i2c $a spi4 $b
} result options]
set report [dict create pid [pid] executable [info nameofexecutable] code $code result $result]
if {$code} {dict set report errorinfo [dict get $options -errorinfo]}
set out [open [file join $root logs capture_C_20261019 c12_single_create_result.tcldict] w]
fconfigure $out -encoding utf-8 -translation lf
puts $out $report
close $out
puts $report
exit $code
