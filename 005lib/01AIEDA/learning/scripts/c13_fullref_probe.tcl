source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {
set version v7
if {[info exists ::C13DesignVersion]} {set version $::C13DesignVersion}
set d [ok [$session GetDesignAndSchematics [cs "$root/examples/lesson13_capture/c13_scope_$version.dsn"] $s] Open]
set out {}
set table [list "page\traw_reference\tfull_reference\tdevice"]
set vi [$d NewViewsIter $s $::IterDefs_SCHEMATICS]
for {set v [$vi NextView $s]} {$v ne "NULL"} {set v [$vi NextView $s]} {
set sch [DboViewToDboSchematic $v]; set pi [$sch NewPagesIter $s]
for {set page [$pi NextPage $s]} {$page ne "NULL"} {set page [$pi NextPage $s]} {
set ii [$page NewPartInstsIter $s]
for {set inst [$ii NextPartInst $s]} {$inst ne "NULL"} {set inst [$ii NextPartInst $s]} {
set row [list page [get $page GetName] raw [get $inst GetReference] baseFull [get $inst GetReferenceDesignator]]
set placed [DboPartInstToDboPlacedInst $inst]
if {$placed ne "NULL"} {
 lappend row placedFull [get $placed GetReferenceDesignator]
 set dev [ok [$placed GetDevice $s] Device]
 lappend table [join [list [get $page GetName] [get $inst GetReference] [get $placed GetReferenceDesignator] [get $dev GetDesignator]] \t]
}
lappend out $row
}
delete_DboPagePartInstsIter $ii
}
delete_DboSchematicPagesIter $pi
}
delete_DboLibViewsIter $vi
write "$root/logs/capture_C_20261019/c13_fullrefs_$version.tsv" [join $table \n]
$session RemoveDesign $d
}
set ::C13::out
