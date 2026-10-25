source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {
 set version v4
 if {[info exists ::C13DesignVersion]} {set version $::C13DesignVersion}
 set d [ok [$session GetDesignAndSchematics [cs "$root/examples/lesson13_capture/c13_scope_$version.dsn"] $s] Open]
 set out {}
 set vi [$d NewViewsIter $s $::IterDefs_SCHEMATICS]
 for {set v [$vi NextView $s]} {$v ne "NULL"} {set v [$vi NextView $s]} {
   set sch [DboViewToDboSchematic $v]
   set si [$sch NewPagesIter $s]
   for {set page [$si NextPage $s]} {$page ne "NULL"} {set page [$si NextPage $s]} {
     set pn [get $page GetName]
     set rows {}
     set wi [$page NewWiresIter $s]
     for {set w [$wi NextWire $s]} {$w ne "NULL"} {set w [$wi NextWire $s]} {
       set ai [$w NewAliasesIter $s]; set aliases {}
       for {set a [$ai NextAlias $s]} {$a ne "NULL"} {set a [$ai NextAlias $s]} {lappend aliases [get $a GetName]}
       delete_DboWireAliasesIter $ai
       lappend rows [list [$w GetId $s] [get $w GetNetName] $aliases]
     }
     delete_DboPageWiresIter $wi
     dict set out $pn wires $rows
     set pi [$page NewPartInstsIter $s]; set rows {}
     for {set inst [$pi NextPartInst $s]} {$inst ne "NULL"} {set inst [$pi NextPartInst $s]} {
       set pins {}; set piter [$inst NewPinsIter $s]
       for {set pin [$piter NextPin $s]} {$pin ne "NULL"} {set pin [$piter NextPin $s]} {lappend pins [list [get $pin GetPinName] [get $pin GetPinNumber]]}
       delete_DboPartInstPinsIter $piter
       lappend rows [list rawReference [get $inst GetReference] fullReference [fullref $inst] pins $pins]
     }
     delete_DboPagePartInstsIter $pi
     dict set out $pn instances $rows
   }
   delete_DboSchematicPagesIter $si
 }
 delete_DboLibViewsIter $vi
 write "$root/logs/capture_C_20261019/c13_inspection_$version.tcldict" $out
 $session RemoveDesign $d
}
set ::C13::out
