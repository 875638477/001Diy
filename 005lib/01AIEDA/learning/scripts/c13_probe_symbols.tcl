source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {
set cap [openLib "$root/examples/lesson13_capture/capsym_source.olb"]
set result {}
foreach {kind name method} {global VCC GetGlobalSymbol offpage OFFPAGELEFT-L GetOffPageSymbol port PORTLEFT-L GetPortSymbol} {
set sym [ok [$cap $method [cs $name] $s] $name]
set row {}
set p [$sym GetPin $s]
ok $p Pin
set hot [$p GetHotSpot $s]
dict set row hot [list [DboTclHelper_sGetCPointX $hot] [DboTclHelper_sGetCPointY $hot]]
dict set result $kind $row
}
}
set ::C13::result
