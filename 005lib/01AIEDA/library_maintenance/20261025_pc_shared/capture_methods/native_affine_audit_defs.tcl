# Definitions only: no DLL load, file/design open, Save, mutation or automatic call.
# Caller supplies an already-open owned design in its single native process.
namespace eval ::CaptureNativeAffine {}
proc ::CaptureNativeAffine::state {s label} {
 if {$s eq {} || $s eq {NULL}} {error "Missing state: $label"}
 if {[$s Failed]} {error "Read failed: $label code=[$s Code]"}
}
proc ::CaptureNativeAffine::point {p} {
 if {$p eq {} || $p eq {NULL}} {error {Missing native point}}
 return [list [DboTclHelper_sGetCPointX $p] [DboTclHelper_sGetCPointY $p]]
}
proc ::CaptureNativeAffine::str {obj method} {
 set c [DboTclHelper_sMakeCString {}]
 set rc [catch {set s [$obj $method $c];state $s $method;set value [DboTclHelper_sGetConstCharPtr $c]} message options]
 catch {DboTclHelper_sDeleteCString $c}
 if {$rc} {return -options $options $message}
 return $value
}
proc ::CaptureNativeAffine::tsv {items} {
 set out {};foreach item $items {lappend out [string map [list \\ \\\\ \t {\t} \r {\r} \n {\n}] $item]};join $out \t
}
proc ::CaptureNativeAffine::auditPartFrames {design outputPath} {
 if {$design eq {} || $design eq {NULL}} {error {Expected already-open owned design}}
 if {[file exists $outputPath]} {error "Refusing existing report: $outputPath"}
 set s [DboState];set schematic [$design GetRootSchematic $s];state $s GetRootSchematic
 if {$schematic eq {} || $schematic eq {NULL}} {error {Root schematic unavailable}}
 file mkdir [file dirname $outputPath]
 set stream [open $outputPath w];fconfigure $stream -encoding utf-8 -translation lf
 set pages {};set insts {};set count 0;set pageCount 0;set eofStates {}
 set rc [catch {
  puts $stream [tsv {page id ref rotation mirror ox oy frame_origin_x frame_origin_y a_xx a_xy a_yx a_yy offset_x offset_y}]
  set pages [$schematic NewPagesIter $s];state $s NewPagesIter
  for {set page [$pages NextPage $s]} {$page ne {NULL}} {set page [$pages NextPage $s]} {
   state $s NextPage;incr pageCount;set name [str $page GetName]
   set insts [$page NewPartInstsIter $s];state $s NewPartInstsIter
   for {set obj [$insts NextPartInst $s]} {$obj ne {NULL}} {set obj [$insts NextPartInst $s]} {
    state $s NextPartInst;set inst [DboPartInstToDboPlacedInst $obj]
    if {$inst eq {} || $inst eq {NULL}} {error {Expected placed instance}}
    set ident [$inst GetId $s];state $s GetId
    set reference [str $inst GetReferenceDesignator]
    set rotation [$inst GetRotation $s];state $s GetRotation
    set mirror [$inst GetMirror $s];state $s GetMirror
    lassign [point [$inst GetLocation $s]] ox oy;state $s GetLocation
    # The three actual native basis samples include any bounding-frame offset.
    lassign [point [$inst GetOffsetGraphicPoint [DboTclHelper_sMakeCPoint 0 0]]] zx zy
    lassign [point [$inst GetOffsetGraphicPoint [DboTclHelper_sMakeCPoint 1 0]]] xx xy
    lassign [point [$inst GetOffsetGraphicPoint [DboTclHelper_sMakeCPoint 0 1]]] yx yy
    set a [expr {$xx-$zx}];set b [expr {$yx-$zx}];set c [expr {$xy-$zy}];set d [expr {$yy-$zy}]
    if {abs($a*$d-$b*$c)!=1 || $a*$a+$c*$c!=1 || $b*$b+$d*$d!=1 || $a*$b+$c*$d!=0} {error "Unsupported native affine orientation: $ident"}
    puts $stream [tsv [list $name $ident $reference $rotation $mirror $ox $oy $zx $zy $a $b $c $d [expr {$zx-$ox}] [expr {$zy-$oy}]]]
    incr count
   }
   # EOF states are recorded separately; do not pass NULL to an object getter.
   lappend eofStates [list PartInst $name [$s Failed] [$s Code]]
   delete_DboPagePartInstsIter $insts;set insts {}
  }
  lappend eofStates [list Page {} [$s Failed] [$s Code]]
 } message options]
 if {$insts ne {}} {catch {delete_DboPagePartInstsIter $insts}}
 if {$pages ne {}} {catch {delete_DboSchematicPagesIter $pages}}
 close $stream
 if {$rc} {return -options $options $message}
 return [dict create status COMPLETE_READONLY_BASIS_AUDIT pages $pageCount instances $count eof_states $eofStates output $outputPath no_save 1]
}
