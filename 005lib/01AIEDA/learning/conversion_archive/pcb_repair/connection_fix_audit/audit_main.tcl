load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set auditRoot {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/connection_fix_audit}
proc tsv {values} {
 set cells {}
 foreach value $values {lappend cells [string map [list \t {\t} \r {\r} \n {\n}] $value]}
 return [join $cells \t]
}
set code [catch {
 set session $::DboSession_s_pDboSession
 set state [DboState]
 set design [::DE::obj [$session GetDesignAndSchematics [::DE::cs "$auditRoot/input/LGA1700.DSN"] $state] $state OpenDesign]
 ::DE::obj [$design GetRootOccurrence $state] $state RootOccurrence
 set top [::DE::obj [$design GetRootSchematic $state] $state RootSchematic]
 set pages "page\tinstances\tpins\twires\toffpages"
 set instances "page\treference\tfull_reference\tvalue\tfootprint\tx\ty"
 set pins "page\treference\tfull_reference\tnumber\tname\tnc\tnet\tx\ty"
 set pageCount 0;set instCount 0;set pinCount 0;set wireCount 0;set offCount 0
 set pi [$top NewPagesIter $state]
 for {set page [$pi NextPage $state]} {$page ne "NULL"} {set page [$pi NextPage $state]} {
  set pageName [::DE::str $page GetName];incr pageCount
  set np 0;set ni 0;set nw 0;set no 0
  set ii [$page NewPartInstsIter $state]
  for {set instance [$ii NextPartInst $state]} {$instance ne "NULL"} {set instance [$ii NextPartInst $state]} {
   set placed [DboPartInstToDboPlacedInst $instance]
   if {$placed eq "NULL"} {error "Non-placed part on $pageName"}
   set ref [::DE::str $placed GetReference]
   set fullRef [::DE::str $placed GetReferenceDesignator]
   set value [::DE::str $placed GetPartValue]
   set footprint [::DE::str $placed GetPCBFootprint]
   append instances "\n[tsv [concat [list $pageName $ref $fullRef $value $footprint] [::DE::point [$instance GetLocation $state]]]]"
   incr ni;incr instCount
   set pini [$instance NewPinsIter $state]
   for {set pin [$pini NextPin $state]} {$pin ne "NULL"} {set pin [$pini NextPin $state]} {
    set number [::DE::str $pin GetPinNumber]
    set name [::DE::str $pin GetPinName]
    set nc [$pin GetIsNoConnect $state]
    set net [$pin GetNet $state];set netName {}
    if {$net ne "NULL"} {set netName [::DE::str $net GetNetName]}
    append pins "\n[tsv [concat [list $pageName $ref $fullRef $number $name $nc $netName] [::DE::point [$pin GetOffsetHotSpot $state]]]]"
    incr np;incr pinCount
   }
   delete_DboPartInstPinsIter $pini
  }
  delete_DboPagePartInstsIter $ii
  set wi [$page NewWiresIter $state]
  for {set wire [$wi NextWire $state]} {$wire ne "NULL"} {set wire [$wi NextWire $state]} {incr nw;incr wireCount}
  delete_DboPageWiresIter $wi
  set oi [$page NewOffPageConnectorsIter $state]
  for {set off [$oi NextOffPageConnector $state]} {$off ne "NULL"} {set off [$oi NextOffPageConnector $state]} {incr no;incr offCount}
  delete_DboPageOffPageConnectorsIter $oi
  append pages "\n[tsv [list $pageName $ni $np $nw $no]]"
 }
 delete_DboSchematicPagesIter $pi
 ::DE::write "$auditRoot/pages.tsv" $pages
 ::DE::write "$auditRoot/instances.tsv" $instances
 ::DE::write "$auditRoot/pins.tsv" $pins
 set summary [dict create pages $pageCount instances $instCount pins $pinCount wires $wireCount offpages $offCount root [::DE::str $top GetName]]
 ::DE::state [$session RemoveDesign $design] CloseDesign
 set summary
} result options]
::DE::write "$auditRoot/audit_result.tcldict" [dict create code $code result $result options $options]
puts [dict create code $code result $result]
if {$code} {puts [dict get $options -errorinfo]}
exit $code
