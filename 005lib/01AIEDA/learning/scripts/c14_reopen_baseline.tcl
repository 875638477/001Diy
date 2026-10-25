source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_helpers.tcl}
set C14st [DboState]
set C14s $::DboSession_s_pDboSession
DboSession -this $C14s
set C14ds [$C14s GetDesignAndSchematics [::C14Research::cstring D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/run03/c14_baseline.dsn] $C14st]
if {$C14ds eq "NULL"} {error GetDesignAndSchematicsFailed}
set C14sch [$C14ds GetRootSchematic $C14st]
set C14pi [$C14sch NewPagesIter $C14st]
set C14page [$C14pi NextPage $C14st]
set C14res {}
while {$C14page ne "NULL"} {
 lappend C14res [::C14Research::readString $C14page GetName]
 set C14ii [$C14page NewPartInstsIter $C14st]
 set C14inst [$C14ii NextPartInst $C14st]
 while {$C14inst ne "NULL"} {
  set C14placed [DboPartInstToDboPlacedInst $C14inst]
  set C14ref [::C14Research::readString $C14placed GetReferenceDesignator]
  ::C14Research::snapshotPlacedInstance $C14placed D:/001DIY/005lib/01AIEDA/learning/logs/lesson14_capture_20261019/run03/baseline_reopened_${C14ref}.tcldict
  lappend C14res $C14ref
  set C14inst [$C14ii NextPartInst $C14st]
 }
 delete_DboPagePartInstsIter $C14ii
 set C14page [$C14pi NextPage $C14st]
}
delete_DboSchematicPagesIter $C14pi
$C14s RemoveDesign $C14ds
set C14res
