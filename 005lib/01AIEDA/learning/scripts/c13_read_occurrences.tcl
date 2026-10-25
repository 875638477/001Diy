source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {
set d [ok [$session GetDesignAndSchematics [cs "$root/examples/lesson13_capture/c13_scope_v4.dsn"] $s] Open]
set ro [ok [$d GetRootOccurrence $s] Root]
set ni [$d NewFlatNetsIter $s]
set rows [list "flat_id\tname\tglobal\tocc_path\tsch_net"]
for {set net [$ni NextFlatNet $s]} {$net ne "NULL"} {set net [$ni NextFlatNet $s]} {
 set name [get $net GetName]; set id [$net GetId $s]; set g [$net GetIsGlobal $s]
 trace "occ net $id $name"
 set oi [$net NewNetOccurrencesIter]
 trace "occ iter $oi"
 for {set occ [$oi NextNetOccurrence $s]} {$occ ne "NULL"} {set occ [$oi NextNetOccurrence $s]} {
   trace "occ $occ"
   lappend rows [join [list $id $name $g [get $occ GetRefPathName] [get $occ GetNetName]] \t]
 }
 delete_DboFlatNetNetOccurrencesIter $oi
}
delete_DboDesignFlatNetsIter $ni
write "$root/logs/capture_C_20261019/c13_flat_occurrences_v4.tsv" [join $rows \n]
$session RemoveDesign $d
set result [list rows [expr {[llength $rows]-1}]]
}
set ::C13::result
