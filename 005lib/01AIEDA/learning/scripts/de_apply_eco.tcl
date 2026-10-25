set base {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/native}
set source "$base/de_integrated_single.dsn"
set target "$base/de_integrated_eco_final.dsn"
if {[file exists $target]} {error "Refuse to overwrite ECO design"}
file copy $source $target
set s [DboState];set sess $::DboSession_s_pDboSession
set d [::DE::obj [$sess GetDesignAndSchematics [::DE::cs $target] $s] $s OpenECO];lappend ::DE::designs $d
::DE::obj [$d GetRootOccurrence $s] $s InitializeOccurrence
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set pi [$top NewPagesIter $s];set page [::DE::obj [$pi NextPage $s] $s Page];delete_DboSchematicPagesIter $pi
set ii [$page NewPartInstsIter $s];set changed {};set header NULL
for {set i [$ii NextPartInst $s]} {$i ne "NULL"} {set i [$ii NextPartInst $s]} {
 set inst [::DE::obj [DboPartInstToDboPlacedInst $i] $s Placed]
 set ref [::DE::str $inst GetReferenceDesignator]
 if {$ref in {R19 R20}} {
  if {[::DE::str $inst GetPartValue] ne "2.2k"} {error "Unexpected baseline pullup $ref"}
  ::DE::state [$inst SetPartValue [::DE::cs 3.3k]] PullupECO
  ::DE::prop $inst ECO_REASON {I2C pullup change; rise time rechecked at100pF}
  ::DE::state [$inst MarkModified] MarkPullup
  lappend changed $ref
 }
 if {$ref eq "J13"} {set header $inst}
}
delete_DboPagePartInstsIter $ii
if {[lsort $changed] ne {R19 R20} || $header eq "NULL"} {error "ECO targets not found"}
lassign [::DE::point [$header GetLocation $s]] hx hy
set points [dict create];set pins [$header NewPinsIter $s]
for {set p [$pins NextPin $s]} {$p ne "NULL"} {set p [$pins NextPin $s]} {
 set num [::DE::str $p GetPinNumber]
 if {$num in {7 8}} {lassign [::DE::point [$p GetHotSpot $s]] px py;dict set points [list [expr {$hx+$px}] [expr {$hy+$py}]] $num}
}
delete_DboPartInstPinsIter $pins
set edits {};set wi [$page NewWiresIter $s]
for {set wire [$wi NextWire $s]} {$wire ne "NULL"} {set wire [$wi NextWire $s]} {
 set point [::DE::point [$wire GetStartPoint $s]]
 if {![dict exists $points $point]} {continue}
 set num [dict get $points $point];set expected [expr {$num==7 ? "GPIO_PB8" : "GPIO_PB9"}]
 set replacement [expr {$num==7 ? "GPIO_PB9" : "GPIO_PB8"}]
 set ai [$wire NewAliasesIter $s]
 set alias [::DE::obj [$ai NextAlias $s] $s PinAlias]
 if {[::DE::str $alias GetName] ne $expected} {error "Unexpected alias at J13.$num"}
 ::DE::state [$alias SetName [::DE::cs $replacement]] AliasECO
 delete_DboWireAliasesIter $ai
 lappend edits [list J13 $num $expected $replacement]
}
delete_DboPageWiresIter $wi
if {[llength $edits]!=2} {error "Expected exactly two header alias edits"}
::DE::prop $header ECO_REASON {Swap header pin7/8 GPIO PB8/PB9; MCU pin45/46 unchanged}
::DE::state [$header MarkModified] MarkHeader
::DE::save $d
::DE::state [$sess RemoveDesign $d] CloseECO;set ::DE::designs {}
dict create target $target values $changed connections $edits
