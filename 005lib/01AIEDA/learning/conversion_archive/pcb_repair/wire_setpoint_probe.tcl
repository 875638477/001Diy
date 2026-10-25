load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set root {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/ad_wire_probe}
set code [catch {
 set s [DboState];set session $::DboSession_s_pDboSession
 set d [::DE::obj [$session GetDesignAndSchematics [::DE::cs "$root/LGA1700.DSN"] $s] $s Open]
 ::DE::obj [$d GetRootOccurrence $s] $s Occurrence
 set top [::DE::obj [$d GetRootSchematic $s] $s Schematic]
 set found 0;set pi [$top NewPagesIter $s]
 for {set p [$pi NextPage $s]} {$p ne "NULL"} {set p [$pi NextPage $s]} {
  if {[::DE::str $p GetName] ne {USB32 GEN1 5G_REAR}} {continue}
  set wi [$p NewWiresIter $s]
  for {set w [$wi NextWire $s]} {$w ne "NULL"} {set w [$wi NextWire $s]} {
   if {[$w GetPointCount $s] != 2} {continue}
   set points [list [::DE::point [$w GetPoint 0 $s]] [::DE::point [$w GetPoint 1 $s]]]
   if {$points eq {{606 824} {606 854}}} {
    ::DE::state [$w SetPoint 1 [::DE::pt 606 844]] SetWirePoint
    ::DE::state [$w MarkModified] WireModified
    incr found
   }
  }
  delete_DboPageWiresIter $wi
 }
 delete_DboSchematicPagesIter $pi
 if {$found!=1} {error "Expected exactly one USB bridge: $found"}
 ::DE::save $d
 ::DE::state [$session RemoveDesign $d] Close
 dict create repaired_wire_count $found
} result options]
::DE::write "$root/probe_result.tcldict" [dict create code $code result $result options $options]
puts [dict create code $code result $result]
if {$code} {puts [dict get $options -errorinfo]}
exit $code
