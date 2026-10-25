source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {
 set version v5
 if {[info exists ::C13DesignVersion]} {set version $::C13DesignVersion}
 set d [ok [$session GetDesign [cs "$root/examples/lesson13_capture/c13_scope_$version.dsn"] $s] Open]
 set vi [$d NewViewsIter $s $::IterDefs_SCHEMATICS]
 for {set v [$vi NextView $s]} {$v ne "NULL"} {set v [$vi NextView $s]} {
   set sch [DboViewToDboSchematic $v]
   # This isolated 17.2 SDK eagerly loads the last page only. Re-expand the
   # two-page TOP; do not expand the already complete one-page child folders.
   if {[get $sch GetName] eq "TOP"} {trace "Expand TOP two-page connectivity"; $sch Expand}
 }
 delete_DboLibViewsIter $vi
 set ro [ok [$d GetRootOccurrence $s] Root]
 set rows [list "flat_id\tname\tglobal\tocc_path\tsch_net"]
 set wires [list "flat_id\tname\tocc_path\tpage\twire_id\taliases"]
 set pins [list "flat_id\tname\tocc_path\tpage\treference\tpin_name\tpin_number\ttype\tvisible\traw_global"]
 set ni [$d NewFlatNetsIter $s]
 for {set net [$ni NextFlatNet $s]} {$net ne "NULL"} {set net [$ni NextFlatNet $s]} {
   set name [get $net GetName]; set id [$net GetId $s]; set g [$net GetIsGlobal $s]
   trace "v5 net $id $name"
   set oi [$net NewNetOccurrencesIter]
   for {set occ [$oi NextNetOccurrence $s]} {$occ ne "NULL"} {set occ [$oi NextNetOccurrence $s]} {
     set path [get $occ GetRefPathName]
     lappend rows [join [list $id $name $g $path [get $occ GetNetName]] \t]
     set sn [ok [$occ GetNet $s] SchematicNet]
     set wi [$sn NewWiresIter $s]
     for {set w [$wi NextWire $s]} {$w ne "NULL"} {set w [$wi NextWire $s]} {
       set aliases {}; set ai [$w NewAliasesIter $s]
       for {set a [$ai NextAlias $s]} {$a ne "NULL"} {set a [$ai NextAlias $s]} {lappend aliases [get $a GetName]}
       delete_DboWireAliasesIter $ai
       lappend wires [join [list $id $name $path [get [$w GetOwner] GetName] [$w GetId $s] $aliases] \t]
     }
     delete_DboSchematicNetWiresIter $wi
     set pi [$sn NewPortInstsIter $s]
     for {set p [$pi NextPortInst $s]} {$p ne "NULL"} {set p [$pi NextPortInst $s]} {
       set inst [$p GetOwner]
       set page [$inst GetOwner]
       lappend pins [join [list $id $name $path [get $page GetName] [fullref $inst] [get $p GetPinName] [get $p GetPinNumber] [$p GetPinType $s] [$p GetIsVisible $s] [$p GetIsGlobal $s]] \t]
     }
     delete_DboSchematicNetPortInstsIter $pi
   }
   delete_DboFlatNetNetOccurrencesIter $oi
 }
 delete_DboDesignFlatNetsIter $ni
 write "$root/logs/capture_C_20261019/c13_flat_occurrences_$version.tsv" [join $rows \n]
 write "$root/logs/capture_C_20261019/c13_flat_wires_$version.tsv" [join $wires \n]
 write "$root/logs/capture_C_20261019/c13_flat_pins_$version.tsv" [join $pins \n]
 $session RemoveDesign $d
 set result [list occurrences [expr {[llength $rows]-1}] wires [expr {[llength $wires]-1}] pins [expr {[llength $pins]-1}]]
}
set ::C13::result
