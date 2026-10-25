set ::C14DefinitionsOnly 1
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_propagation.tcl}
proc ::C14Prop::replaceInstances {} {
 variable base; variable log
 set s [::C12::session]; set st [DboState]; set result {}
 set source "$base/c14_relocated_v2.olb"
 set lib [nn [$s GetLib [c $source] $st] $st GetNewLib]
 set pkg [nn [$lib GetPackage [c QMI8610_C12] $st] $st GetNewPackage]
 set dev [$pkg GetDevice 0 $st]; set cell [$dev GetCell $st]; set part [$cell FindPart 0 $st]
 foreach flag {0 1} {
  set branch "native_replace${flag}"
  set target "$base/${branch}.dsn"
  file copy "$base/c14_baseline.dsn" $target
  set design [nn [$s GetDesignAndSchematics [c $target] $st] $st Open]
  snapshot $design "$log/$branch/before"
  set sch [$design GetRootSchematic $st]; set pi [$sch NewPagesIter $st]; set page [$pi NextPage $st]
  while {$page ne "NULL"} {
   set ii [$page NewPartInstsIter $st]; set inst [$ii NextPartInst $st]; set instances {}
   while {$inst ne "NULL"} {lappend instances [DboPartInstToDboPlacedInst $inst];set inst [$ii NextPartInst $st]}
   delete_DboPagePartInstsIter $ii
   foreach inst $instances {
    set new [nn [$page ReplaceInst $inst [c QMI8610_C12] $part $dev $st $flag 1 1] $st ReplaceInst]
   }
   set page [$pi NextPage $st]
  }
  delete_DboSchematicPagesIter $pi
  snapshot $design "$log/$branch/immediate"
  save $design
  check [$s RemoveDesign $design] RemoveDesign
  set design [nn [$s GetDesignAndSchematics [c $target] $st] $st Reopen]
  dict set result $branch [snapshot $design "$log/$branch/reopened"]
  check [$s RemoveDesign $design] RemoveDesign
 }
 check [$s RemoveLib $lib] RemoveLib
 return $result
}
::C14Prop::replaceInstances
