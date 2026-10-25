# Definitions only. Caller owns an isolated standalone Dbo design/session.
# Mirrors installed Cadence capUtils/capReplacePathInCache.tcl's two setters.
# No open, DLL load, Save, placement or automatic operation.
namespace eval ::CaptureSourceRelink {}
proc ::CaptureSourceRelink::cs {v} {return [DboTclHelper_sMakeCString $v]}
proc ::CaptureSourceRelink::check {s context} {
 if {$s eq {} || $s eq {NULL} || [$s Failed]} {error "Native state failed: $context"}
}
proc ::CaptureSourceRelink::apply {design oldSource newSource expectedCounts} {
 if {$oldSource eq $newSource || $oldSource eq {} || $newSource eq {}} {error {Explicit distinct source identities required}}
 if {$design eq {NULL} || $design eq {}} {error {Missing owned design}}
 set s [DboState];set iter [$design NewCachesIter $s];check $s NewCachesIter
 set rows {};set counts {}
 for {set obj [$iter NextCachedObject $s]} {$obj ne {NULL}} {set obj [$iter NextCachedObject $s]} {
  check $s NextCachedObject
  set libobj [DboBaseObjectToDboLibObject $obj]
  if {$libobj eq {NULL}} {error {Cache object is not a library object}}
  set name [cs {}];check [$obj GetName $name] GetCacheName
  set source [cs {}];check [$design GetSourceLibName $name $libobj $source] GetSourceLibName
  if {[DboTclHelper_sGetConstCharPtr $source] eq $oldSource} {
   set type [$obj GetObjectType];dict incr counts $type
   lappend rows [list $libobj $name $source]
  }
 }
 if {[$s Failed] && [$s Code] != 1022} {check $s CacheIteratorEnd}
 delete_DboDesignCachesIter $iter
 if {[dict size $counts] != [dict size $expectedCounts]} {error {Unexpected cache type count}}
 dict for {type count} $expectedCounts {
  if {![dict exists $counts $type] || [dict get $counts $type] != $count} {error "Unexpected cache object multiplicity: $type"}
 }
 if {![llength $rows]} {error {No exact source identities selected}}
 # Validate all selectors/multiplicities before the first mutation.
 set target [cs $newSource]
 foreach row $rows {
  lassign $row libobj name source
  $design ReplaceSourceLibName $name $libobj $source $target
  $libobj SetSourceLibName $target
  set current [cs {}];check [$design GetSourceLibName $name $libobj $current] ReadChangedSource
  if {[DboTclHelper_sGetConstCharPtr $current] ne $newSource} {error {Source identity immediate readback mismatch}}
 }
 return [dict create status APPLIED_NOT_SAVED cache_objects [llength $rows] counts $counts old_source $oldSource new_source $newSource]
}
