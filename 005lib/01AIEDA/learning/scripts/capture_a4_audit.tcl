set s [DboState]
set root {D:/001DIY/005lib/01AIEDA/learning/staging/a4_review_20261019}
if {![info exists auditLabel]} {set auditLabel before}
if {![info exists dsnPath]} {set dsnPath "$root/baseline_snapshot.dsn"}
set d [::DE::obj [$::DboSession_s_pDboSession GetDesignAndSchematics [::DE::cs $dsnPath] $s] $s OpenSnapshot]
lappend ::DE::designs $d
::DE::obj [$d GetRootOccurrence $s] $s Initialize
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set pages "page\tsize\tmetric\twidth_native\theight_native\tpintopin\tdoc_per_inch\tgranularity\tdoc_width\tdoc_height\tdraw_width\tdraw_height"
set instances "page\treference\tvalue\tx\ty\tleft\ttop\tright\tbottom\tfootprint"
set pins "page\treference\tnumber\tname\tnc\tnet\thotx\thoty"
set wires "page\tx1\ty1\tx2\ty2"
set aliases "page\tname\tx\ty\tfont_height"
set offpages "page\tname\thotx\thoty\tleft\ttop\tright\tbottom\tname_x\tname_y\tname_display_type"
proc bounds {o} {
 set b [$o GetBoundingBox]
 concat [::DE::point [DboTclHelper_sGetCRectTopLeft $b]] [::DE::point [DboTclHelper_sGetCRectBottomRight $b]]
}
set it [$top NewPagesIter $s]
for {set p [$it NextPage $s]} {$p ne "NULL"} {set p [$it NextPage $s]} {
 set pn [::DE::str $p GetName]
 set full [$p GetDocUnits];set draw [$p GetDocUnits 1]
 append pages "\n[join [list $pn [::DE::str $p GetSizeName] [$p GetIsMetric] [$p GetPageWidth] [$p GetPageHeight] [$p GetPinToPin] [$p GetDocUnitsPerInch] [$p GetPhysicalGranularity] [DboTclHelper_sGetCSizeX $full] [DboTclHelper_sGetCSizeY $full] [DboTclHelper_sGetCSizeX $draw] [DboTclHelper_sGetCSizeY $draw]] \t]"
 set ii [$p NewPartInstsIter $s]
 for {set i [$ii NextPartInst $s]} {$i ne "NULL"} {set i [$ii NextPartInst $s]} {
  set placed [DboPartInstToDboPlacedInst $i]
  if {$placed eq "NULL"} {error "Non-placed part"}
  set ref [::DE::str $placed GetReferenceDesignator]
  append instances "\n[join [concat [list $pn $ref [::DE::str $placed GetPartValue]] [::DE::point [$i GetLocation $s]] [bounds $i] [list [::DE::str $placed GetPCBFootprint]]] \t]"
  set pii [$i NewPinsIter $s]
  for {set pin [$pii NextPin $s]} {$pin ne "NULL"} {set pin [$pii NextPin $s]} {
   set nc [$pin GetIsNoConnect $s]
   set net [$pin GetNet $s];set netname {}
   if {$net ne "NULL" && !$nc} {
    if {[catch {::DE::str $net GetNetName} netname]} {error "Read net failed for $pn $ref pin [::DE::str $pin GetPinNumber], nc=$nc: $netname"}
   }
   append pins "\n[join [concat [list $pn $ref [::DE::str $pin GetPinNumber] [::DE::str $pin GetPinName] $nc $netname] [::DE::point [$pin GetOffsetHotSpot $s]]] \t]"
  }
  delete_DboPartInstPinsIter $pii
 }
 delete_DboPagePartInstsIter $ii
 set wi [$p NewWiresIter $s]
 for {set w [$wi NextWire $s]} {$w ne "NULL"} {set w [$wi NextWire $s]} {
  append wires "\n[join [concat [list $pn] [::DE::point [$w GetStartPoint $s]] [::DE::point [$w GetEndPoint $s]]] \t]"
  set ai [$w NewAliasesIter $s]
  for {set a [$ai NextAlias $s]} {$a ne "NULL"} {set a [$ai NextAlias $s]} {
   append aliases "\n[join [concat [list $pn [::DE::str $a GetName]] [::DE::point [$a GetLocation $s]] [list -10]] \t]"
  }
  delete_DboWireAliasesIter $ai
 }
 delete_DboPageWiresIter $wi
 set oi [$p NewOffPageConnectorsIter $s]
 for {set o [$oi NextOffPageConnector $s]} {$o ne "NULL"} {set o [$oi NextOffPageConnector $s]} {
  lassign [bounds $o] ol ot or ob
  lassign [::DE::point [$o GetLocation $s]] ox oy
  set dp [::DE::obj [$o GetDisplayProp [::DE::cs Name] $s] $s OffPageNameDisplay]
  lassign [::DE::point [$dp GetLocation $s]] nx ny
  append offpages "\n[join [concat [list $pn [::DE::str $o GetName]] [::DE::point [$o GetOffsetHotSpot $s]] [list [expr {$ox+$ol}] [expr {$oy+$ot}] [expr {$ox+$or}] [expr {$oy+$ob}] [expr {$ox+$nx}] [expr {$oy+$ny}] [$dp GetDisplayType $s]]] \t]"
 }
 delete_DboPageOffPageConnectorsIter $oi
}
delete_DboSchematicPagesIter $it
foreach {name value} [list pages $pages instances $instances pins $pins wires $wires aliases $aliases offpages $offpages] {::DE::write "$root/${auditLabel}_$name.tsv" $value}
dict create snapshot $dsnPath pages_report "$root/${auditLabel}_pages.tsv" read_only 1
