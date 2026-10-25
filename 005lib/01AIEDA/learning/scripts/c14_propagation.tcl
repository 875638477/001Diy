source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_helpers.tcl}
namespace eval ::C14Prop {
 variable base {D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/run04}
 variable log {D:/001DIY/005lib/01AIEDA/learning/logs/lesson14_capture_20261019/run04}
}
proc ::C14Prop::c {s} {return [::C12::cstring $s]}
proc ::C14Prop::check {s ctx} {return [::C12::check $s $ctx]}
proc ::C14Prop::nn {o s ctx} {return [::C12::nonnull $o $s $ctx]}
proc ::C14Prop::props {o pairs} {
 foreach {k v} $pairs {
  set s [$o SetUserPropStringValue [c $k] [c $v]]
  if {[$s Failed]} {::C12::user_prop $o $k $v}
 }
}
proc ::C14Prop::snapshot {design dir} {
 set state [DboState]; file mkdir $dir
 ::C14Research::snapshotCache $design [file join $dir cache.tcldict]
 set pi [[$design GetRootSchematic $state] NewPagesIter $state]
 set page [$pi NextPage $state]; set refs {}
 while {$page ne "NULL"} {
  set ii [$page NewPartInstsIter $state]; set inst [$ii NextPartInst $state]
  while {$inst ne "NULL"} {
   set placed [DboPartInstToDboPlacedInst $inst]
   set ref [::C14Research::readString $placed GetReferenceDesignator]
   ::C14Research::snapshotPlacedInstance $placed [file join $dir "${ref}.tcldict"]
   set package [$placed GetPackage $state]
   if {![file exists [file join $dir package.tcldict]]} {::C14Research::snapshotPackage $package [file join $dir package.tcldict]}
   lappend refs $ref
   set inst [$ii NextPartInst $state]
  }
  delete_DboPagePartInstsIter $ii
  set page [$pi NextPage $state]
 }
 delete_DboSchematicPagesIter $pi
 return $refs
}
proc ::C14Prop::save {design} {
 set st [DboState]; set sch [$design GetRootSchematic $st]
 set pi [$sch NewPagesIter $st]; set page [$pi NextPage $st]
 while {$page ne "NULL"} {check [$sch SavePage $page] SavePage; set page [$pi NextPage $st]}
 delete_DboSchematicPagesIter $pi
 set s [::C12::session]; check [$s SaveDesign $design] SaveDesign
}
proc ::C14Prop::v2 {source} {
 set s [::C12::session]; set st [DboState]
 set lib [nn [$s GetLib [c $source] $st] $st GetLib]
 set pkg [nn [$lib GetPackage [c QMI8610_C12] $st] $st GetPackage]
 set d [$pkg GetDevice 0 $st]; set cell [$d GetCell $st]; set p [$cell FindPart 0 $st]
 check [$p SetPartValue [c QMI8610_V2]] SetPartValue
 props $p {MPN QMI8610_MPN_V2 LIB_REV C14_V2 C14_INST_OVERRIDE LIB_DEFAULT_V2 C14_LIB_ONLY LIB_ONLY_V2}
 nn [$p NewLine $st [DboTclHelper_sMakeCPoint 0 0] [DboTclHelper_sMakeCPoint 220 180] 0 0] $st NewLine
 set pins [$p NewLPinsIter $st]; set pin [$pins NextPin $st]
 while {$pin ne "NULL"} {
  if {[$pin GetPinPosition $st]==3} {check [$pin SetIsNumberVisible 0] SetIsNumberVisible}
  set pin [$pins NextPin $st]
 }
 delete_DboLibPartPinsIter $pins
 check [$lib SavePackageAll $pkg] SavePackageAll
 check [$s SaveLib $lib] SaveLib
 check [$s RemoveLib $lib] RemoveLib
}
proc ::C14Prop::run {} {
 variable base; variable log
 set source [file join $base c14_source_v1.olb]
 set baseline [file join $base c14_baseline.dsn]
 set v2path [file join $base c14_relocated_v2.olb]
 foreach branch {update replace0 replace1} {
  set target [file join $base "c14_${branch}.dsn"]
  if {[file exists $target]} {error "Branch exists: $target"}
  file copy $baseline $target
 }
 file copy $source [file join $base c14_source_v1_archive.olb]
 v2 $source
 file copy $source $v2path
 set s [::C12::session]; set st [DboState]; set result {}
 foreach branch {update replace0 replace1} {
  set target [file join $base "c14_${branch}.dsn"]
  set design [nn [$s GetDesignAndSchematics [c $target] $st] $st OpenBranch]
  set refs [snapshot $design [file join $log $branch before]]
  if {$branch eq "update"} {
   set res [::C14Research::updateCache $design $source QMI8610_C12 $::DboBaseObject_PACKAGE]
  } else {
   set flag [string index $branch end]
   set res [::C14Research::replaceCache $design QMI8610_C12 $source QMI8610_C12 $v2path $flag 1]
  }
  set failed [$res Failed]
  ::C14Research::writeTclReport [file join $log $branch native_call.tcldict] [dict create branch $branch failed $failed refsBefore $refs]
  if {$failed} {error "Native cache call failed: $branch"}
  snapshot $design [file join $log $branch immediate]
  save $design
  check [$s RemoveDesign $design] RemoveDesign
  set design [nn [$s GetDesignAndSchematics [c $target] $st] $st ReopenBranch]
  set finalrefs [snapshot $design [file join $log $branch reopened]]
  check [$s RemoveDesign $design] RemoveDesign
  dict set result $branch [dict create path $target refs $finalrefs]
 }
 return $result
}
if {![info exists ::C14DefinitionsOnly] || !$::C14DefinitionsOnly} {error {Archived cache-API diagnostic is disabled; source with C14DefinitionsOnly=1 for safe helper definitions.}}
