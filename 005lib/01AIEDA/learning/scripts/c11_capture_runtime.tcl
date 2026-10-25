# Run by the documented Capture command-line Tcl entry point.
# All work and requests remain in this isolated lesson directory.
set ::C11Root {D:/001DIY/005lib/01AIEDA/learning}
set ::C11Runtime [file join $::C11Root logs capture_C_20261019 runtime]
set ::C11Queue [file join $::C11Root staging capture_C_20261019 queue]
file mkdir $::C11Runtime $::C11Queue
proc C11Write {path value} {
    set ch [open "$path.part" w]
    fconfigure $ch -encoding utf-8 -translation lf
    puts $ch $value
    close $ch
    file rename -force "$path.part" $path
}
set boot [dict create pid [pid] executable [info nameofexecutable] tcl [info patchlevel] started [clock format [clock seconds] -format {%Y-%m-%dT%H:%M:%S%z}]]
foreach pkg {DboTclWriteBasic} {
    set code [catch {package require $pkg} result options]
    dict set boot package_$pkg [list code $code result $result]
}
dict set boot native_session_exists [info exists ::DboSession_s_pDboSession]
dict set boot dbo_command_count [llength [info commands Dbo*]]
dict set boot ui_command_count [llength [info commands Menu]]
dict set boot ini [expr {[llength [info commands GetIniPath]] ? [GetIniPath] : {unavailable}}]
C11Write [file join $::C11Runtime ready.tcldict] $boot
proc C11Poll {} {
    foreach path [lsort [glob -nocomplain -directory $::C11Queue *.tcl]] {
        set id [file rootname [file tail $path]]
        set running "$path.running"
        file rename $path $running
        set started [clock milliseconds]
        set code [catch {uplevel #0 [list source $running]} result options]
        set report [dict create id $id code $code result $result started_ms $started finished_ms [clock milliseconds]]
        if {$code} {dict set report errorinfo [dict get $options -errorinfo]}
        C11Write [file join $::C11Runtime "$id.result.tcldict"] $report
        file rename $running "$path.done"
    }
    after 200 C11Poll
}
after 200 C11Poll
