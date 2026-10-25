source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_helpers.tcl}
namespace eval ::C14Run {
 variable root {D:/001DIY/005lib/01AIEDA/learning}
 variable base {D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/run04}
 variable log {D:/001DIY/005lib/01AIEDA/learning/logs/lesson14_capture_20261019/run04}
}
proc ::C14Run::check {s context} {::C12::check $s $context}
proc ::C14Run::c {s} {return [::C12::cstring $s]}
proc ::C14Run::obj {o s context} {return [::C12::nonnull $o $s $context]}
proc ::C14Run::properties {o pairs} {
 foreach {k v} $pairs {
  set s [$o SetUserPropStringValue [c $k] [c $v]]
  if {[$s Failed]} {::C12::user_prop $o $k $v}
 }
}
proc ::C14Run::build {} {
 variable root; variable base; variable log
 file mkdir $base; file mkdir $log
 set source [file join $root examples/lesson12_capture/c12_qmi8610.olb]
 set libpath [file join $base c14_source_v1.olb]
 set dsnpath [file join $base c14_baseline.dsn]
 if {[file exists $libpath] || [file exists $dsnpath]} {error "Baseline exists; refuse overwrite"}
 file copy $source $libpath
 set session [::C12::session]; set state [DboState]
 set lib [obj [$session GetLib [c $libpath] $state] $state GetLib]
 set package [obj [$lib GetPackage [c QMI8610_C12] $state] $state GetPackage]
 set device [$package GetDevice 0 $state]; set cell [$device GetCell $state]; set part [$cell FindPart 0 $state]
 check [$device SetDesignator [c ""]] SetDesignator
 check [$part SetPartValue [c QMI8610_V1]] PartValue
 properties $part {MPN QMI8610_MPN_V1 LIB_REV C14_V1 C14_INST_OVERRIDE LIB_DEFAULT_V1 C14_LIB_ONLY LIB_ONLY_V1}
 check [$lib SavePackageAll $package] SavePackageAll
 check [$session SaveLib $lib] SaveLib
 set design [obj [$session CreateDesign $state [c $dsnpath] [c TOP]] $state CreateDesign]
 set sch [obj [$design GetRootSchematic $state] $state GetRootSchematic]
 set page [obj [$sch NewPage $state [c PAGE1]] $state NewPage]
 set d $device; set p $part
 set number 0
 foreach location {{500 500} {1000 500}} {
  incr number
  set ref U140$number
  set inst [obj [$page NewPlacedInst $state [c QMI8610_C12.Normal] [c QMI8610_C12] $p $d [DboTclHelper_sMakeCPoint {*}$location]] $state NewPlacedInst]
  check [$inst SetReference [c $ref]] SetReference
  if {$number==2} {
   check [$inst SetPartValue [c INSTANCE_VALUE_OVERRIDE]] SetInstanceValue
   properties $inst {MPN INSTANCE_MPN_OVERRIDE C14_INST_OVERRIDE INSTANCE_CUSTOM_OVERRIDE}
   check [$inst SetPCBFootprint [c C14_PROP_SENTINEL_NOT_FOR_PCB]] SetPCBFootprint
  }
  lassign $location x y
  set wire [obj [$page NewWireScalar $state [DboTclHelper_sMakeCPoint [expr {$x+240}] [expr {$y+120}]] [DboTclHelper_sMakeCPoint [expr {$x+340}] [expr {$y+120}]]] $state NewWireScalar]
  set font [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16]
  obj [$wire NewAlias $state [c "C14_SCL_$number"] [DboTclHelper_sMakeCPoint [expr {$x+270}] [expr {$y+120}]] $font 0 0] $state NewAlias
  ::C14Research::snapshotPlacedInstance $inst [file join $log "baseline_immediate_${ref}.tcldict"]
 }
 ::C14Research::snapshotCache $design [file join $log baseline_cache.tcldict]
 check [$sch SavePage $page] SavePage
 check [$session SaveDesign $design] SaveDesign
 check [$session RemoveDesign $design] RemoveDesign
 check [$session RemoveLib $lib] RemoveLib
 return [dict create design $dsnpath library $libpath]
}
::C14Run::build
