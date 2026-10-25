set root {D:/001DIY/005lib/01AIEDA/learning}
set logRoot [file join $root logs capture_C_20261019]
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source [file join $root scripts c12_helpers.tcl]
set code [catch {
    set results {}
    foreach {file package mode reportdir} {
        c12_qmi8610_single.olb QMI8610_C12_SINGLE HOST_I2C c12_single_fresh_i2c
        c12_qmi8610_spi4_single.olb QMI8610_C12_SPI4_SINGLE HOST_SPI4 c12_single_fresh_spi4
    } {
        set path [file join $root examples lesson12_capture $file]
        set readback [::C12::ReadQmi8610 $path $package [file join $logRoot $reportdir] $mode]
        set session [::C12::session]
        set status [DboState]
        set lib [$session GetLib [::C12::cstring $path] $status]
        ::C12::nonnull $lib $status GetLib
        set pkg [$lib GetPackage [::C12::cstring $package] $status]
        ::C12::nonnull $pkg $status GetPackage
        set dev [$pkg GetDevice 0 $status]
        ::C12::nonnull $dev $status GetDevice
        set suffix [::C12::string_value $dev GetDesignator]
        if {$suffix ne ""} {error "Single-unit suffix is not empty: $suffix"}
        set info [dict create library $path package $package devicePosition [$dev GetPosition $status] deviceDesignator $suffix readback $readback]
        ::C12::check [$session RemoveLib $lib] RemoveLib
        dict set results $mode $info
    }
    set results
} result options]
set report [dict create pid [pid] executable [info nameofexecutable] tcl [info patchlevel] package [package require DboTclWriteBasic] code $code result $result]
if {$code} {dict set report errorinfo [dict get $options -errorinfo]}
set out [open [file join $logRoot c12_single_freshprocess_result.tcldict] w]
fconfigure $out -encoding utf-8 -translation lf
puts $out $report
close $out
puts $report
exit $code
