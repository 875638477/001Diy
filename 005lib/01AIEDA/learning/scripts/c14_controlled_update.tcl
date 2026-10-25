set ::C14DefinitionsOnly 1
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_propagation.tcl}
proc ::C14Prop::controlled {} {
 set root {D:/001DIY/005lib/01AIEDA/learning}
 set base "$root/examples/lesson14_capture/final"
 set log "$root/logs/lesson14_capture_20261019/final"
 file mkdir "$base/library";file mkdir $log
 set original "$root/examples/lesson14_capture/run04"
 set source "$base/library/c14_qmi8610_v2.olb"
 if {[file exists $source]} {error "Final source exists"}
 file copy "$original/c14_relocated_v2.olb" $source
 set s [::C12::session];set st [DboState]
 set lib [nn [$s GetLib [c $source] $st] $st SourceV2]
 set pkg [nn [$lib GetPackage [c QMI8610_C12] $st] $st PackageV2]
 set dev [$pkg GetDevice 0 $st];set cell [$dev GetCell $st];set part [$cell FindPart 0 $st]
 set results {}
 foreach mode {update_preserve relocated_preserve replace_properties} {
  set target "$base/c14_${mode}.dsn"
  file copy "$original/c14_baseline.dsn" $target
  set design [nn [$s GetDesignAndSchematics [c $target] $st] $st Open]
  snapshot $design "$log/$mode/before"
  set sch [$design GetRootSchematic $st];set pi [$sch NewPagesIter $st];set page [$pi NextPage $st]
  set changes {}
  while {$page ne "NULL"} {
   set ii [$page NewPartInstsIter $st];set inst [$ii NextPartInst $st];set items {}
   while {$inst ne "NULL"} {lappend items [DboPartInstToDboPlacedInst $inst];set inst [$ii NextPartInst $st]}
   delete_DboPagePartInstsIter $ii
   foreach inst $items {
    set reference [::C14Research::readString $inst GetReference]
    set oldValue [::C14Research::readString $inst GetPartValue]
    set oldMpn [::C14Research::property $inst MPN]
    set oldCustom [::C14Research::property $inst C14_INST_OVERRIDE]
    set oldFootprint [::C14Research::readString $inst GetPCBFootprint]
    set new [nn [$page ReplaceInst $inst [c QMI8610_C12] $part $dev $st 0 1 1] $st ReplaceInst]
    set rawReference [::C14Research::readString $new GetReference]
    check [$new SetReference [c $reference]] RestoreReference
    # The exercise has explicit instance overrides only on U1402.
    # Keep the override list explicit rather than guessing from inherited values.
    if {$mode ne "replace_properties" && $reference eq "U1402"} {
     check [$new SetPartValue [c $oldValue]] RestoreValueOverride
     props $new [list MPN $oldMpn C14_INST_OVERRIDE $oldCustom]
     check [$new SetPCBFootprint [c $oldFootprint]] RestoreFootprintOverride
    }
    $new MarkModified
    lappend changes [dict create refdes $reference rawNativeReference $rawReference explicitOverrideRestored [expr {$mode ne "replace_properties" && $reference eq "U1402"}]]
   }
   $page MarkModified
   set page [$pi NextPage $st]
  }
  delete_DboSchematicPagesIter $pi
  ::C14Research::writeTclReport "$log/$mode/method.tcldict" [dict create method {native ReplaceInst plus explicit reference/override policy} changes $changes]
  snapshot $design "$log/$mode/immediate"
  save $design;check [$s RemoveDesign $design] Close
  set design [nn [$s GetDesignAndSchematics [c $target] $st] $st Reopen]
  dict set results $mode [snapshot $design "$log/$mode/reopened"]
  check [$s RemoveDesign $design] CloseReopened
 }
 check [$s RemoveLib $lib] CloseSource
 return $results
}
::C14Prop::controlled
