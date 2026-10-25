set base {D:/001DIY/005lib/01AIEDA/learning/staging/de_15_26_20261019/minimal_res}
file mkdir $base
set sess $::DboSession_s_pDboSession;set s [DboState]
set lib [::DE::obj [$sess GetLib [::DE::cs {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/library/de_training_baseline.olb}] $s] $s OpenLib]
lappend ::DE::libs $lib
set pkg [::DE::obj [$lib GetPackage [::DE::cs DE_RES] $s] $s Package]
set dev [::DE::obj [$pkg GetDevice 0 $s] $s Device]
set cell [::DE::obj [$dev GetCell $s] $s Cell]
set part [::DE::obj [$cell FindPart 0 $s] $s Part]
set d [::DE::obj [$sess CreateDesign $s [::DE::cs "$base/DE_MIN_RES.dsn"] [::DE::cs TOP]] $s CreateDesign]
lappend ::DE::designs $d
set sch [::DE::obj [$d GetRootSchematic $s] $s Root]
set page [::DE::obj [$sch NewPage $s [::DE::cs PAGE1]] $s Page]
set inst [::DE::obj [$page NewPlacedInst $s [::DE::cs DE_RES.Normal] [::DE::cs DE_RES] $part $dev [::DE::pt 500 500]] $s Inst]
::DE::state [$inst SetReference [::DE::cs R1]] SetRef
set f [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16]
foreach {x1 x2 name} {480 350 LEFT 600 730 RIGHT} {
 set w [::DE::obj [$page NewWireScalar $s [::DE::pt $x1 520] [::DE::pt $x2 520]] $s Wire]
 ::DE::obj [$w NewAlias $s [::DE::cs $name] [::DE::pt [expr {min($x1,$x2)+20}] 520] $f 0 0] $s Alias
}
::DE::state [$sch SavePage $page] SavePage
::DE::state [$sess SaveDesign $d] SaveDesign
::DE::state [$sess RemoveDesign $d] CloseDesign;set ::DE::designs {}
::DE::state [$sess RemoveLib $lib] CloseLib;set ::DE::libs {}
list MINIMAL_RES_SAVED
