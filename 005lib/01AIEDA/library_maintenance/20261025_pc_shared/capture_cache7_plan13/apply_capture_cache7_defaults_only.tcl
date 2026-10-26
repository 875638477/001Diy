# Cache7defaultsOnly. Exact full-instance/cache guards; no source library setters. Root owns isolated native process.
# Plan is generated from fixed full XML and exact existing/new OLB proofs.
source {D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/tools/native_helpers/layout_native_common.tcl}
if {[llength $argv] != 4} {error {Usage: inputDSN freshTargetDSN frozenPlanTcl freshReportDirectory}}
lassign $argv input target planFile reportDir
if {[file exists $target] || [file exists $reportDir]} {error {Fresh target and report directory required}}
source $planFile
foreach v {sourceSelectors instanceGuards footprintPlan expectedCacheCounts expectedInstanceCounts} {if {![info exists $v]} {error "Missing frozen plan variable $v"}}
# The three CN1/CN2/CN3 source instances have no User_Value in instance or package.
# A missing property is not an empty value: preserve both native missing-pointer state and effective read status.
proc pc13UserValueAbsence {inst} {
 set st [DboState];set raw [$inst GetUserProp [::LAY::cs User_Value] $st]
 if {$raw ne {NULL} && $raw ne {}} {error {Unexpected newly materialized User_Value property}}
 set rawStatus [list [$st Failed] [$st Code]]
 set value [::LAY::cs {}];set es [$inst GetEffectivePropStringValue [::LAY::cs User_Value] $value]
 return [list $rawStatus [$es Failed] [$es Code] [DboTclHelper_sGetConstCharPtr $value]]
}
set categoryTypes [dict create PACKAGE $::DboBaseObject_PACKAGE PART_CELL $::DboBaseObject_PART_CELL LIBRARY_PART $::DboBaseObject_LIBRARY_PART GlobalSymbol $::DboBaseObject_GLOBAL_SYMBOL OffPageSymbol $::DboBaseObject_OFF_PAGE_SYMBOL PortSymbol $::DboBaseObject_PORT_SYMBOL]
set expectedSelectors {}
foreach row $sourceSelectors {
 set category [dict get $row category]
 set key [list [dict get $categoryTypes $category] [dict get $row name] [dict get $row old_source]]
 if {[dict exists $expectedSelectors $key]} {error {Ambiguous native selector}}
 if {![file isfile [dict get $row new_source]]} {error "Unpublished target library: [dict get $row new_source]"}
 dict set expectedSelectors $key $row
}
file mkdir [file dirname $target]
file copy $input $target
file mkdir $reportDir
lassign [::LAY::openDesign $target] d top
set s [DboState]
# Completely bind the exact Cache membership, before any mutations.
set iter [$d NewCachesIter $s];::LAY::obj $iter $s CacheIter
set cacheBound {};set actualCounts {}
for {set obj [$iter NextCachedObject $s]} {$obj ne {NULL}} {set obj [$iter NextCachedObject $s]} {
 ::LAY::state $s CacheObject
 set libobj [DboBaseObjectToDboLibObject $obj]
 if {$libobj eq {NULL}} {error {Cached object is not a library object}}
 set name [::LAY::str $obj GetName]
 set n [::LAY::cs $name];set old [::LAY::cs {}]
 ::LAY::state [$d GetSourceLibName $n $libobj $old] GetSourceLibName
 set oldText [DboTclHelper_sGetConstCharPtr $old]
 set type [$obj GetObjectType]
 set key [list $type $name $oldText]
 if {![dict exists $expectedSelectors $key]} {error "Unplanned cache object: $key"}
 if {[dict exists $cacheBound $key]} {error "Duplicate cache object: $key"}
 set plan [dict get $expectedSelectors $key]
 dict incr actualCounts [dict get $plan category]
 dict set cacheBound $key [list $libobj $n $old $plan]
}
if {[$s Failed] && [$s Code] != 1022} {::LAY::state $s CacheIterEnd}
delete_DboDesignCachesIter $iter
if {[dict size $cacheBound] != [dict size $expectedSelectors]} {error {Native cache selection incomplete}}
dict for {kind count} $expectedCacheCounts {if {![dict exists $actualCounts $kind] || [dict get $actualCounts $kind] != $count} {error "Cache multiplicity guard $kind"}}
if {[dict size $actualCounts] != [dict size $expectedCacheCounts]} {error {Unplanned cache category}}
# Bind every actual instance and its business/pose before any mutations.
set instanceBound {};set pages {};set counts {}
set pi [$top NewPagesIter $s]
for {set page [$pi NextPage $s]} {$page ne {NULL}} {set page [$pi NextPage $s]} {
 set pn [::LAY::str $page GetName];lappend pages $page
 foreach spec {{PartInst NewPartInstsIter NextPartInst delete_DboPagePartInstsIter} {Global NewGlobalsIter NextGlobal delete_DboPageGlobalsIter} {OffPageConnector NewOffPageConnectorsIter NextOffPageConnector delete_DboPageOffPageConnectorsIter} {Port NewPortsIter NextPort delete_DboPagePortsIter}} {
  lassign $spec kind newIterator nextObject deleteIterator
  if {![dict exists $expectedInstanceCounts $kind] || [dict get $expectedInstanceCounts $kind] == 0} {continue}
  set ii [$page $newIterator $s];::LAY::obj $ii $s "$kind iter"
  for {set inst [$ii $nextObject $s]} {$inst ne {NULL}} {set inst [$ii $nextObject $s]} {
   ::LAY::state $s "$kind next"
   set id [$inst GetId $s];set key [list $kind $id]
   if {![dict exists $instanceGuards $key] || [dict exists $instanceBound $key]} {error "Unplanned/duplicate instance $key"}
   set g [dict get $instanceGuards $key]
   if {$pn ne [dict get $g page]} {error "Instance page guard $key"}
   set object $inst
   if {$kind eq {PartInst}} {set object [DboPartInstToDboPlacedInst $inst]}
   if {[::LAY::str $object GetSourceLibName] ne [dict get $g old_source]} {error "Source guard $key"}
   if {[::LAY::point [$inst GetLocation $s]] ne [dict get $g location] || [$inst GetRotation $s] ne [dict get $g rotation] || [$inst GetMirror $s] ne [dict get $g mirror]} {error "Instance pose guard $key"}
   if {$kind eq {PartInst}} {
    if {[dict exists $g user_value_explicit_absent]} {dict set g uv_absence_native_state [pc13UserValueAbsence $inst]}
    if {[dict exists $g user_value] && [::LAY::str $inst GetEffectivePropStringValue [::LAY::cs User_Value]] ne [dict get $g user_value]} {error "User_Value before guard $key"}
    if {[::LAY::str $object GetReference] ne [dict get $g ref] || [::LAY::str $object GetPartValue] ne [dict get $g value] || [::LAY::str $object GetPCBFootprint] ne [dict get $g footprint]} {error "Part business guard $key"}
   } else {
    if {[::LAY::str $inst GetName] ne [dict get $g net_name]} {error "Network name guard $key"}
   }
   dict set instanceBound $key [list $inst $object $g]
   dict incr counts $kind
  }
  if {[$s Failed] && [$s Code] != 1022} {::LAY::state $s "$kind iter end"}
  $deleteIterator $ii
 }
}
delete_DboSchematicPagesIter $pi
if {[dict size $instanceBound] != [dict size $instanceGuards]} {error {Instance guard selection incomplete}}
dict for {kind count} $expectedInstanceCounts {
 set actual 0;if {[dict exists $counts $kind]} {set actual [dict get $counts $kind]}
 if {$actual != $count} {error "Instance count guard $kind"}
}
dict for {id row} $footprintPlan {
 set key [list PartInst $id]
 if {![dict exists $instanceBound $key]} {error "Missing footprint target $id"}
 set guard [lindex [dict get $instanceBound $key] 2]
 if {[dict get $row before] ne [dict get $guard footprint]} {error "Footprint plan guard $id"}
}
# This variant is footprint-only. The preceding full cache/source guards are read-only.
dict for {key binding} $cacheBound {
 lassign $binding libobj name old row
 if {[dict get $row old_source] ne [dict get $row new_source]} {error {Source edits forbidden in Cache7 plan}}
}
# Bind exactcached DboPackage via the proven placed-instance GetPackage API.
# PublicOLB sameDboPackage GetPCBFootprint/SetPCBFootprint are already nativelyproven.
if {![info exists cacheDefaultPlan] || [dict size $cacheDefaultPlan] != 7 || [dict size $footprintPlan] != 0} {error {Cache7 exactplan required}}
set defaultBound {}
dict for {ikey ibinding} $instanceBound {
 if {[lindex $ikey 0] ne {PartInst}} {continue}
 lassign $ibinding inst placed guard
 set s [DboState];set pkg [::LAY::obj [$inst GetPackage $s] $s GetCachedPackageViaInstance]
 set pn [::LAY::str $pkg GetName]
 if {![dict exists $cacheDefaultPlan $pn]} {continue}
 set r [dict get $cacheDefaultPlan $pn]
 if {[$pkg GetObjectType] ne $::DboBaseObject_PACKAGE} {error "CachePackage type differs: $pn"}
 if {[::LAY::str $pkg GetPCBFootprint] ne [dict get $r before]} {error "Cachedefault exactbefore differs: $pn"}
 if {![dict exists $defaultBound $pn]} {dict set defaultBound $pn [list $pkg $r]}
}
if {[dict size $defaultBound] != 7} {error {CachePackage exactseven selection incomplete}}
set f [::LAY::channel $reportDir CACHE_DEFAULT_FP_IMMEDIATE_READBACK.tsv {package before after}]
dict for {pn binding} $defaultBound {
 lassign $binding pkg r
 ::LAY::state [$pkg SetPCBFootprint [::LAY::cs [dict get $r after]]] "CachePCBFootprint $pn"
 if {[::LAY::str $pkg GetPCBFootprint] ne [dict get $r after]} {error "Cachedefault immediate readback differs: $pn"}
 puts $f [::LAY::row [list $pn [dict get $r before] [dict get $r after]]]
}
close $f
set f [::LAY::channel $reportDir FOOTPRINT_IMMEDIATE_READBACK.tsv {id ref page before after}]
dict for {id row} $footprintPlan {
 lassign [dict get $instanceBound [list PartInst $id]] inst placed guard
 ::LAY::state [$inst SetUserPropStringValue [::LAY::cs {PCB Footprint}] [::LAY::cs [dict get $row after]]] "PCB Footprint $id"
 if {[::LAY::str $placed GetPCBFootprint] ne [dict get $row after]} {error "Footprint immediate mismatch $id"}
 puts $f [::LAY::row [list $id [dict get $guard ref] [dict get $guard page] [dict get $row before] [dict get $row after]]]
}
close $f
# Verify source links propagated to every referenced instance; preserve all values and poses.
set f [::LAY::channel $reportDir INSTANCE_SOURCE_IMMEDIATE_READBACK.tsv {kind id page before after}]
dict for {key binding} $instanceBound {
 lassign $binding inst object guard;lassign $key kind id
 if {[::LAY::str $object GetSourceLibName] ne [dict get $guard new_source]} {error "Instance source setter did not propagate: $key"}
 if {[::LAY::point [$inst GetLocation $s]] ne [dict get $guard location] || [$inst GetRotation $s] ne [dict get $guard rotation] || [$inst GetMirror $s] ne [dict get $guard mirror]} {error "Unexpected pose mutation $key"}
 if {$kind eq {PartInst}} {
  set fp [dict get $guard footprint]
  if {[dict exists $footprintPlan $id]} {set fp [dict get $footprintPlan $id after]}
  if {[dict exists $guard user_value_explicit_absent] && [pc13UserValueAbsence $inst] ne [dict get $guard uv_absence_native_state]} {error "User_Value absence/native state changed $key"}
  if {[dict exists $guard user_value] && [::LAY::str $inst GetEffectivePropStringValue [::LAY::cs User_Value]] ne [dict get $guard user_value]} {error "Unexpected User_Value mutation $key"}
  if {[::LAY::str $object GetPartValue] ne [dict get $guard value] || [::LAY::str $object GetReference] ne [dict get $guard ref] || [::LAY::str $object GetPCBFootprint] ne $fp} {error "Unexpected business value mutation $key"}
 } elseif {[::LAY::str $inst GetName] ne [dict get $guard net_name]} {error "Unexpected net name mutation $key"}
 puts $f [::LAY::row [list $kind $id [dict get $guard page] [dict get $guard old_source] [dict get $guard new_source]]]
}
close $f
::LAY::save $d $top $pages
::LAY::state [$::DboSession_s_pDboSession RemoveDesign $d] CloseSavedTarget
::LAY::write [file join $reportDir COMPLETE.tcldict] [dict create status SAVED_PENDING_INDEPENDENT_REOPEN cache_count [dict size $cacheBound] instance_count [dict size $instanceBound] footprint_changes [dict size $footprintPlan] cache_default_footprint_changes [dict size $cacheDefaultPlan] pages [llength $pages]]
puts "CAPTURE13_NATIVE_SAVED cache=[dict size $cacheBound] instances=[dict size $instanceBound] footprint_changes=[dict size $footprintPlan]"