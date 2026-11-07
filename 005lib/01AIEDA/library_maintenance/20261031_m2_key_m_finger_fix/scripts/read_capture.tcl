source {D:/001DIY/005lib/01AIEDA/learning/scripts/capture_dbo_readonly_common.tcl}
load {C:/Program0/Cadence/SPB172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
namespace import ::CAPDB::*
proc cs {v} {::CAPDB::cs $v}
proc sv {obj method args} {::CAPDB::str $obj $method {*}$args}
set base [file normalize [file join [file dirname [info script]] ..]]
set out [file join $base logs read_capture]
if {[llength $argv]>1} {set out [lindex $argv 1]}
file mkdir $out
set st [DboState]
set session $::DboSession_s_pDboSession
set libpath [file join $base source 019Connector.olb]
if {[llength $argv]>0} {set libpath [lindex $argv 0]}
set lib [::CAPDB::obj [$session GetLib [cs $libpath] $st] $st OpenLib]
foreach name {{M_2 KEY M} {M_2-05NGFF-KEY-M}} {
 set package [::CAPDB::obj [$lib GetPackage [cs $name] $st] $st GetPackage]
 set dev [::CAPDB::obj [$package GetDevice 0 $st] $st GetDevice]
 set cell [::CAPDB::obj [$dev GetCell $st] $st GetCell]
 set part [::CAPDB::obj [$cell FindPart 0 $st] $st FindPart]
 set fn [string map [list { } _] $name]
 set f [::CAPDB::channel $out ${fn}_pins.tsv {number position name type visible global noConnect startX startY hotX hotY}]
 set it [$part NewLPinsIter $st];set pin [$it NextPin $st]
 while {$pin ne {NULL}} {
  set pos [$pin GetPinPosition $st]
  puts $f [::CAPDB::row [concat [list [sv $dev GetPinNumber $pos] $pos [sv $pin GetPinName] [$pin GetPinType $st] [$pin GetIsVisible $st] [$pin GetIsGlobal $st] [$pin GetIsNoConnect $st]] [::CAPDB::point [$pin GetStartPoint $st]] [::CAPDB::point [$pin GetHotSpot $st]]]]
  set pin [$it NextPin $st]
 }
 close $f;delete_DboLibPartPinsIter $it
 set f [::CAPDB::channel $out ${fn}_props.tsv {property value}]
 puts $f "footprint\t[sv $package GetPCBFootprint]"
 puts $f "value\t[sv $part GetPartValue]"
 close $f
}
::CAPDB::state [$session RemoveLib $lib] RemoveLib
puts CAPTURE_READ_COMPLETE
exit 0
