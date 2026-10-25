# Definitions only. Owned standalone Dbo session only; never call on a GUI/user design.
# Creates one unsaved instance in memory, snapshots cache identity, then RemoveDesign.
# No load/open/Save/SavePage/MarkModified call is made here.
namespace eval ::CacheReuseCanary {}
proc ::CacheReuseCanary::cs {s} {return [DboTclHelper_sMakeCString $s]}
proc ::CacheReuseCanary::check {state label} {
 if {$state eq {} || $state eq {NULL}} {error "$label returned NULL state"}
 if {[$state Failed]} {error "$label failed code=[$state Code]"}
}
proc ::CacheReuseCanary::obj {object state label} {
 check $state $label
 if {$object eq {} || $object eq {NULL}} {error "$label returned NULL object"}
 return $object
}
proc ::CacheReuseCanary::str {object method} {
 set b [cs {}];set state [$object $method $b];check $state $method
 set result [DboTclHelper_sGetConstCharPtr $b]
 catch {DboTclHelper_sDeleteCString $b};return $result
}
proc ::CacheReuseCanary::cacheSnapshot {design} {
 set s [DboState];set iter [obj [$design NewCachesIter $s] $s NewCachesIter]
 set rows {};set counts {}
 for {set cached [$iter NextCachedObject $s]} {$cached ne {NULL}} {set cached [$iter NextCachedObject $s]} {
  check $s NextCachedObject
  set libObject [DboBaseObjectToDboLibObject $cached]
  if {$libObject eq {NULL} || $libObject eq {}} {error {Cached object is not a DboLibObject}}
  set name [str $cached GetName];set n [cs $name];set b [cs {}]
  set state [$design GetSourceLibName $n $libObject $b];check $state GetSourceLibName
  set source [DboTclHelper_sGetConstCharPtr $b]
  catch {DboTclHelper_sDeleteCString $n};catch {DboTclHelper_sDeleteCString $b}
  set type [$cached GetObjectType]
  dict incr counts $type
  lappend rows [dict create type $type name $name sourceLibrary $source]
 }
 # Native iterator NULL/end may report code 1022; only this end position allows it.
 if {[$s Failed] && [$s Code] != 1022} {check $s NextCachedObjectEnd}
 delete_DboDesignCachesIter $iter
 return [dict create total [llength $rows] countsByNativeObjectType $counts objects $rows]
}
proc ::CacheReuseCanary::countType {snapshot type} {
 if {[dict exists $snapshot countsByNativeObjectType $type]} {return [dict get $snapshot countsByNativeObjectType $type]}
 return 0
}
proc ::CacheReuseCanary::probeAndDiscard {session design sourceLib packageName reportPath} {
 if {[file exists $reportPath]} {error {Fresh canary report path required}}
 if {$design eq {NULL} || $design eq {} || $sourceLib eq {NULL} || $sourceLib eq {}} {error {NULL input object}}
 set result {};set code [catch {
  set before [cacheSnapshot $design]
  set s [DboState];set name [cs $packageName]
  set pkg [obj [$sourceLib GetPackage $name $s] $s GetPackage]
  catch {DboTclHelper_sDeleteCString $name}
  set dev [obj [$pkg GetDevice 0 $s] $s GetDevice]
  set cell [obj [$dev GetCell $s] $s GetCell]
  set part [obj [$cell FindPart 0 $s] $s FindPart]
  set graphic [str $part GetName]
  set sch [obj [$design GetRootSchematic $s] $s GetRootSchematic]
  set pages [obj [$sch NewPagesIter $s] $s NewPagesIter]
  set page [obj [$pages NextPage $s] $s NextPage]
  delete_DboSchematicPagesIter $pages
  set g [cs $graphic];set n [cs $packageName]
  # Proven lesson pattern: state, graphicName, packageName, source Part, source Device, CPoint.
  # Deliberately off-page in this unsaved disposable memory copy.
  set inst [obj [$page NewPlacedInst $s $g $n $part $dev [DboTclHelper_sMakeCPoint 30000 30000]] $s NewPlacedInst]
  catch {DboTclHelper_sDeleteCString $g};catch {DboTclHelper_sDeleteCString $n}
  set placedSource [str $inst GetSourceLibName]
  set placedPart [str $inst GetSourcePartName]
  set cachedPkg [obj [$inst GetPackage $s] $s PlacedGetPackage]
  set cachedPkgName [str $cachedPkg GetName];set nativePackageType [$cachedPkg GetObjectType]
  set after [cacheSnapshot $design]
  set beforeCount [countType $before $nativePackageType];set afterCount [countType $after $nativePackageType]
  set result [dict create status IN_MEMORY_PLACEMENT_OBSERVED_NOT_SAVED sourceLibrary [str $sourceLib GetName] selectedPackage $packageName sourceGraphic $graphic placedSourceLibrary $placedSource placedSourcePart $placedPart placedCachedPackage $cachedPkgName nativePackageObjectType $nativePackageType packageCountBefore $beforeCount packageCountAfter $afterCount packageCountDelta [expr {$afterCount-$beforeCount}] cacheBefore $before cacheAfter $after]
 } message options]
 # Always discard this owned design without a Save, including failed probes.
 set closeCode [catch {
  set state [$session RemoveDesign $design];check $state RemoveDesign
 } closeMessage]
 if {$code} {dict set result status PROBE_FAILED_DESIGN_DISCARD_ATTEMPTED;dict set result error $message;dict set result errorInfo [dict get $options -errorinfo]}
 dict set result removeDesignFailed $closeCode
 if {$closeCode} {dict set result removeDesignError $closeMessage}
 dict set result saveCalls 0
 file mkdir [file dirname $reportPath]
 set f [open $reportPath w];fconfigure $f -encoding utf-8 -translation lf;puts $f $result;close $f
 if {$code} {return -options $options $message}
 if {$closeCode} {error "RemoveDesign failed: $closeMessage"}
 return $result
}
