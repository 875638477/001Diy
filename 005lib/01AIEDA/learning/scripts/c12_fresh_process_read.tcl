# Read-only native reopen in a new Tclsh process. No GUI or existing session used.
set root {D:/001DIY/005lib/01AIEDA/learning}
set logRoot [file join $root logs capture_C_20261019]
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source [file join $root scripts c12_helpers.tcl]
set code [catch {
    set i2c [::C12::ReadQmi8610 [file join $root examples lesson12_capture c12_qmi8610.olb] QMI8610_C12 [file join $logRoot c12_freshprocess_i2c] HOST_I2C]
    set spi [::C12::ReadQmi8610 [file join $root examples lesson12_capture c12_qmi8610_spi4.olb] QMI8610_C12_SPI4 [file join $logRoot c12_freshprocess_spi4] HOST_SPI4]
    dict create i2c $i2c spi4 $spi
} result options]
set report [dict create pid [pid] executable [info nameofexecutable] tcl [info patchlevel] package [package require DboTclWriteBasic] code $code result $result]
if {$code} {dict set report errorinfo [dict get $options -errorinfo]}
set out [open [file join $logRoot c12_freshprocess_result.tcldict] w]
fconfigure $out -encoding utf-8 -translation lf
puts $out $report
close $out
puts $report
exit $code
