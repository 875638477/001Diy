load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set root {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/ad_baseline_sch}
set code [catch {
 set f [open "$root/source_identifiers_native.tsv" r]
 fconfigure $f -encoding utf-8
 set rows [split [string trimright [read $f] "\r\n"] \n];close $f
 set sources [dict create]
 foreach row [lrange $rows 1 end] {
  lassign [split [string trimright $row \r] \t] page type name x y sourceLine
  if {$type ni {17 18} || $name eq {} || ![string is integer -strict $x] || ![string is integer -strict $y]} {error "Invalid source record: $row"}
  dict lappend sources "$page|$type" [list $name $x $y $sourceLine]
 }
 source "$root/zero_stubs.tcl"
 set stubCount 0
 set s [DboState];set session $::DboSession_s_pDboSession
 set design [::DE::obj [$session GetDesignAndSchematics [::DE::cs "$root/LGA1700.DSN"] $s] $s OpenDesign]
 ::DE::obj [$design GetRootOccurrence $s] $s RootOccurrence
 set top [::DE::obj [$design GetRootSchematic $s] $s RootSchematic]
 set cap [::DE::obj [$session GetLib [::DE::cs {C:/Program0/Cadence/spb172/tools/capture/library/capsym.olb}] $s] $s Capsym]
 set offSymbol [::DE::obj [$cap GetOffPageSymbol [::DE::cs OFFPAGELEFT-L] $s] $s OffPageSymbol]
 set powerCount 0;set movedPowerCount 0;set offCount 0
 set changes "page\ttype\tname\told_hot_x\told_hot_y\tnew_hot_x\tnew_hot_y\tsource_line"
 set pi [$top NewPagesIter $s]
 for {set page [$pi NextPage $s]} {$page ne "NULL"} {set page [$pi NextPage $s]} {
  set pn [::DE::str $page GetName]
  set oi [$page NewOffPageConnectorsIter $s]
  set existing [$oi NextOffPageConnector $s]
  delete_DboPageOffPageConnectorsIter $oi
  if {$existing ne "NULL"} {error "Refuse repeated application: existing offpage on $pn"}
  set globals {};set gi [$page NewGlobalsIter $s]
  for {set g [$gi NextGlobal $s]} {$g ne "NULL"} {set g [$gi NextGlobal $s]} {lappend globals $g}
  delete_DboPageGlobalsIter $gi
  set expected {}
  if {[dict exists $sources "$pn|17"]} {set expected [dict get $sources "$pn|17"]}
  if {[llength $expected] != [llength $globals]} {error "Global count mismatch $pn"}
  foreach g $globals raw $expected {
   lassign $raw name tx ty sourceLine
   if {[::DE::str $g GetName] ne $name} {error "Global source order mismatch $pn $sourceLine"}
   lassign [::DE::point [$g GetLocation $s]] lx ly
   lassign [::DE::point [$g GetOffsetHotSpot $s]] hx hy
   if {abs($tx-$hx)>10 || abs($ty-$hy)>10} {error "Unexpected global displacement $pn $sourceLine"}
   if {$tx!=$hx || $ty!=$hy} {
    ::DE::state [$g SetLocation [::DE::pt [expr {$lx+$tx-$hx}] [expr {$ly+$ty-$hy}]]] AlignGlobal
    ::DE::state [$g MarkModified] MarkGlobal
    incr movedPowerCount
   }
   if {[::DE::point [$g GetOffsetHotSpot $s]] ne [list $tx $ty]} {error "Global hotspot alignment failed $pn $sourceLine"}
   append changes "\n[join [list $pn power $name $hx $hy $tx $ty $sourceLine] \t]"
   incr powerCount
  }
  if {[dict exists $zeroStubs $pn]} {
   foreach point [dict get $zeroStubs $pn] {
    lassign $point sx sy
    set stub [::DE::obj [$page NewWireScalar $s [::DE::pt $sx $sy] [::DE::pt [expr {$sx+1}] $sy]] $s ZeroLengthWireReplacement]
    ::DE::prop $stub AD_ZERO_LENGTH_WIRE_RESTORED 1
    ::DE::state [$stub MarkModified] MarkStub
    incr stubCount
   }
  }
  if {[dict exists $sources "$pn|18"]} {
   foreach raw [dict get $sources "$pn|18"] {
    lassign $raw name tx ty sourceLine
    set port [::DE::obj [$page NewOffPageConnector $s [::DE::cs $name] $offSymbol [::DE::pt 0 0]] $s NewOffPage]
    lassign [::DE::point [$port GetHotSpot $s]] hx hy
    ::DE::state [$port SetLocation [::DE::pt [expr {$tx-$hx}] [expr {$ty-$hy}]]] AlignOffPage
    ::DE::prop $port AD_SOURCE_RECORD "18:$sourceLine"
    ::DE::state [$port MarkModified] MarkOffPage
    if {[::DE::point [$port GetOffsetHotSpot $s]] ne [list $tx $ty]} {error "Offpage hotspot alignment failed $pn $sourceLine"}
    append changes "\n[join [list $pn port $name {} {} $tx $ty $sourceLine] \t]"
    incr offCount
   }
  }
  ::DE::state [$page MarkModified] MarkPage
 }
 delete_DboSchematicPagesIter $pi
 if {$powerCount!=839 || $movedPowerCount!=496 || $offCount!=1147 || $stubCount!=16} {error "Unexpected counts $powerCount/$movedPowerCount/$offCount/$stubCount"}
 ::DE::save $design
 ::DE::write "$root/changes.tsv" $changes
 ::DE::state [$session RemoveDesign $design] CloseDesign
 ::DE::state [$session RemoveLib $cap] CloseCapsym
 dict create checked_power_symbols $powerCount aligned_power_symbols $movedPowerCount restored_flat_ports $offCount zero_length_wire_replacements $stubCount
} result options]
::DE::write "$root/fix_result.tcldict" [dict create code $code result $result options $options]
puts [dict create code $code result $result]
if {$code} {puts [dict get $options -errorinfo]}
exit $code
