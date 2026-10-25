# Definitions only. No DLL load, design open, Save, mutation, or automatic call.
# Caller supplies an already-open owned design; use one native process at a time.
namespace eval ::CaptureCacheReadOnly {}
proc ::CaptureCacheReadOnly::cs {s} {DboTclHelper_sMakeCString $s}
proc ::CaptureCacheReadOnly::str {obj method} {
 set b [cs {}]; set rc [catch {$obj $method $b} st]
 if {$rc} {catch {DboTclHelper_sDeleteCString $b};error $st}
 if {[$st Failed]} {catch {DboTclHelper_sDeleteCString $b};error "Read failed: $method code=[$st Code]"}
 set v [DboTclHelper_sGetConstCharPtr $b];catch {DboTclHelper_sDeleteCString $b};return $v
}
proc ::CaptureCacheReadOnly::tsv {items} {
 set out {};foreach x $items {lappend out [string map [list \\ \\\\ \t {\t} \r {\r} \n {\n}] $x]};join $out \t
}
proc ::CaptureCacheReadOnly::auditEffective {design queryDataPath outputPath} {
 if {$design eq {NULL} || $design eq {}} {error {Design is NULL}}
 if {[file exists $outputPath]} {error "Refusing existing read-only report: $outputPath"}
 set stream [open $queryDataPath r];fconfigure $stream -encoding utf-8;set queries [string trim [read $stream]];close $stream
 dict size $queries
 set s [DboState];set sch [$design GetRootSchematic $s]
 if {[$s Failed] || $sch eq {NULL}} {error {Root schematic unavailable}}
 file mkdir [file dirname $outputPath]
 set f [open $outputPath w];fconfigure $f -encoding utf-8 -translation lf
 puts $f [tsv {page instance_id refdes property read_failed state_code value error}]
 set seen {};set rows 0;set readFailures 0
 set pages [$sch NewPagesIter $s]
 for {set page [$pages NextPage $s]} {$page ne {NULL}} {set page [$pages NextPage $s]} {
  set pn [str $page GetName]
  set insts [$page NewPartInstsIter $s]
  for {set inst [$insts NextPartInst $s]} {$inst ne {NULL}} {set inst [$insts NextPartInst $s]} {
   set ident [$inst GetId $s]
   if {![dict exists $queries $ident]} {continue}
   dict set seen $ident 1
   set placed [DboPartInstToDboPlacedInst $inst]
   if {$placed eq {NULL} || $placed eq {}} {error "Expected placed instance at ID $ident"}
   set ref [str $placed GetReferenceDesignator]
   foreach name [dict get $queries $ident] {
    set n [cs $name];set v [cs {}];set failed 1;set value {};set code {};set err {}
    set rc [catch {$inst GetEffectivePropStringValue $n $v} state]
    if {$rc} {set err $state} else {
     if {$state eq {NULL} || $state eq {}} {set err NULL_STATE} else {
      set failed [$state Failed];set code [$state Code]
      if {!$failed} {set value [DboTclHelper_sGetConstCharPtr $v]} else {set err {READ_FAILED_DO_NOT_TREAT_AS_EMPTY_OR_ABSENT}}
     }
    }
    if {$failed} {incr readFailures}
    puts $f [tsv [list $pn $ident $ref $name $failed $code $value $err]]
    catch {DboTclHelper_sDeleteCString $n};catch {DboTclHelper_sDeleteCString $v}
    incr rows
   }
  }
  delete_DboPagePartInstsIter $insts
 }
 delete_DboSchematicPagesIter $pages
 close $f
 set missing {};foreach ident [dict keys $queries] {if {![dict exists $seen $ident]} {lappend missing $ident}}
 if {[llength $missing]} {error "Read-only report has unresolved query instance IDs: $missing"}
 return [dict create mode READ_ONLY_NO_SAVE query_instances [dict size $queries] visited_instances [dict size $seen] rows $rows read_failures $readFailures note {Undefined effective properties may fail; compare baseline/candidate states and never replace failures with blank values.}]
}
