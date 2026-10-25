load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set root {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/connection_fix_audit}
proc tsv {values} {
 set cells {}
 foreach value $values {lappend cells [string map [list \t {\t} \r {\r} \n {\n}] $value]}
 return [join $cells \t]
}
proc effectiveprops {object prefix} {
 set state [DboState]
 set out {}
 set pi [$object NewEffectivePropsIter $state]
 set n [::DE::cs {}]; set v [::DE::cs {}]
 set typ [DboTclHelper_sMakeDboValueType];set editable [DboTclHelper_sMakeInt]
 for {set s [$pi NextEffectiveProp $n $v $typ $editable]} {![$s Failed]} {set s [$pi NextEffectiveProp $n $v $typ $editable]} {
  append out "\n[tsv [list $prefix [DboTclHelper_sGetConstCharPtr $n] [DboTclHelper_sGetConstCharPtr $v]]]"
 }
 delete_DboEffectivePropsIter $pi
 return $out
}
set code [catch {
 set state [DboState];set session $::DboSession_s_pDboSession
 set design [::DE::obj [$session GetDesignAndSchematics [::DE::cs "$root/input/LGA1700.DSN"] $state] $state OpenDesign]
 ::DE::obj [$design GetRootOccurrence $state] $state RootOccurrence
 set top [::DE::obj [$design GetRootSchematic $state] $state RootSchematic]
 set objects "page\tkind\tname\tsource_symbol\tnet\tx\ty\thot_x\thot_y\trotation\tmirror"
 set aliases "page\tname\tx\ty\trotation\twire_points"
 set wires "page\tpoints\tobject_type\tline_style\tline_width\tnet"
 set counts "page\tglobals\tports\toffpages"
 set props "object\tname\tvalue"
 append props [effectiveprops $design design]
 append props [effectiveprops $top schematic]
 set totals [dict create global 0 port 0 offpage 0]
 set pi [$top NewPagesIter $state]
 for {set page [$pi NextPage $state]} {$page ne "NULL"} {set page [$pi NextPage $state]} {
  set pn [::DE::str $page GetName]
  set pagecounts [dict create global 0 port 0 offpage 0]
  set wi [$page NewWiresIter $state]
  for {set w [$wi NextWire $state]} {$w ne "NULL"} {set w [$wi NextWire $state]} {
   set points {}
   for {set j 0} {$j<[$w GetPointCount $state]} {incr j} {lappend points [join [::DE::point [$w GetPoint $j $state]] ,]}
   set pointString [join $points {;}]
   append wires "\n[tsv [list $pn $pointString [$w GetObjectType] [$w GetLineStyle $state] [$w GetLineWidth $state] [::DE::str $w GetNetName]]]"
   set ai [$w NewAliasesIter $state]
   for {set a [$ai NextAlias $state]} {$a ne "NULL"} {set a [$ai NextAlias $state]} {
    append aliases "\n[tsv [concat [list $pn [::DE::str $a GetName]] [::DE::point [$a GetLocation $state]] [list [$a GetRotation $state] $pointString]]]"
   }
   delete_DboWireAliasesIter $ai
  }
  delete_DboPageWiresIter $wi
  foreach {kind new next del} {global NewGlobalsIter NextGlobal delete_DboPageGlobalsIter port NewPortsIter NextPort delete_DboPagePortsIter offpage NewOffPageConnectorsIter NextOffPageConnector delete_DboPageOffPageConnectorsIter} {
   set oi [$page $new $state]
   for {set o [$oi $next $state]} {$o ne "NULL"} {set o [$oi $next $state]} {
    set name [::DE::str $o GetName]
    set source [::DE::str $o GetSourceSymbolName]
    set net [$o GetNet $state];set nn {}
    if {$net ne "NULL"} {set nn [::DE::str $net GetNetName]}
    append objects "\n[tsv [concat [list $pn $kind $name $source $nn] [::DE::point [$o GetLocation $state]] [::DE::point [$o GetOffsetHotSpot $state]] [list [$o GetRotation $state] [$o GetMirror $state]]]]"
    dict incr totals $kind;dict incr pagecounts $kind
   }
   $del $oi
  }
  append counts "\n[tsv [list $pn [dict get $pagecounts global] [dict get $pagecounts port] [dict get $pagecounts offpage]]]"
 }
 delete_DboSchematicPagesIter $pi
 ::DE::write "$root/net_objects.tsv" $objects
 ::DE::write "$root/aliases.tsv" $aliases
 ::DE::write "$root/wires.tsv" $wires
 ::DE::write "$root/page_object_counts.tsv" $counts
 ::DE::write "$root/design_properties.tsv" $props
 ::DE::state [$session RemoveDesign $design] CloseDesign
 set totals
} result options]
::DE::write "$root/audit_result.tcldict" [dict create code $code result $result options $options]
puts [dict create code $code result $result]
if {$code} {puts [dict get $options -errorinfo]}
exit $code