# Generic Capture native reader helpers. Sourcing defines functions only.
namespace eval ::CAPDB {variable helperDirectory [file dirname [file normalize [info script]]]}
proc ::CAPDB::init {cadenceRoot} {
 set dll [file join [file normalize $cadenceRoot] tools bin orDb_Dll_Tcl64.dll]
 if {![file isfile $dll]} {error {Cadence root has no tools/bin/orDb_Dll_Tcl64.dll}}
 if {![llength [info commands DboState]]} {
  set ::env(CDSROOT) [file normalize $cadenceRoot]
  set ::env(PATH) "[file nativename [file dirname $dll]];$::env(PATH)"
  load $dll DboTclWriteBasic
 }
 if {![info exists ::DboSession_s_pDboSession]} {set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]}
 DboSession -this $::DboSession_s_pDboSession
}
proc ::CAPDB::outputPath {path allowLearningExercise} {
 variable helperDirectory
 set out [file normalize $path]
 set learning [file dirname $helperDirectory]
 if {[string equal -nocase [file tail $learning] learning] && [string equal -nocase [file tail $helperDirectory] scripts]} {
  set pre "[string tolower [file normalize $learning]]/"
  set candidate "[string tolower $out]/"
  if {[string first $pre $candidate]==0 && !$allowLearningExercise} {error {Real-project outputs must be outside learning; explicit course-exercise exception required}}
 }
 if {[file exists $out]} {error {Output must be fresh}}
 return $out
}
proc ::CAPDB::cs {v} {DboTclHelper_sMakeCString $v}
proc ::CAPDB::point {v} {list [DboTclHelper_sGetCPointX $v] [DboTclHelper_sGetCPointY $v]}
proc ::CAPDB::state {s context} {if {[$s Failed]} {error "DboState failed: $context code=[$s Code]"};return $s}
proc ::CAPDB::obj {o s context} {state $s $context;if {$o eq {NULL} || $o eq {}} {error "Missing object: $context"};return $o}
proc ::CAPDB::str {o method args} {set c [cs {}];state [$o $method {*}$args $c] $method;DboTclHelper_sGetConstCharPtr $c}
proc ::CAPDB::write {path value} {set f [open $path w];fconfigure $f -encoding utf-8 -translation lf;puts $f $value;close $f}
proc ::CAPDB::row {values} {set r {}; foreach v $values {lappend r [string map [list \\ \\\\ \t {\t} \r {\r} \n {\n}] $v]}; join $r \t}
proc ::CAPDB::channel {out name columns} {set f [open [file join $out $name] w];fconfigure $f -encoding utf-8 -translation lf;puts $f [row $columns];return $f}
proc ::CAPDB::openDesign {input} {
 set s [DboState];set d [obj [$::DboSession_s_pDboSession GetDesignAndSchematics [cs $input] $s] $s OpenDesign]
 obj [$d GetRootOccurrence $s] $s RootOccurrence
 return [list $d [obj [$d GetRootSchematic $s] $s RootSchematic]]
}
