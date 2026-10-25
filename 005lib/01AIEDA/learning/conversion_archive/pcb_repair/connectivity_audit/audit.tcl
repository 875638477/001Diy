load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set root {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/connectivity_audit}
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
 set counts "page\tglobals\tports\toffpages"
 set props "object\tname\tvalue"
 append props [effectiveprops $design design]
 append props [effectiveprops $top schematic]
 set totals [dict create global 0 port 0 offpage 0]
 set pi [$top NewPagesIter $state]
 for {set page [$pi NextPage $state]} {$page ne "NULL"} {set page [$pi NextPage $state]} {
  set pn [::DE::str $page GetName]
  set pagecounts [dict create global 0 port 0 offpage 0]
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
 ::DE::write "$root/page_object_counts.tsv" $counts
 ::DE::write "$root/design_properties.tsv" $props
 ::DE::state [$session RemoveDesign $design] CloseDesign
 set totals
} result options]
::DE::write "$root/audit_result.tcldict" [dict create code $code result $result options $options]
puts [dict create code $code result $result]
if {$code} {puts [dict get $options -errorinfo]}
exit $code