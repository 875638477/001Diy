# Keep right-facing connector text clear of its arrow for long network names.
set s [DboState]
set d [::DE::obj [$::DboSession_s_pDboSession GetDesignAndSchematics [::DE::cs {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/a4_review/native/de_integrated_a4.dsn}] $s] $s Open]
lappend ::DE::designs $d
::DE::obj [$d GetRootOccurrence $s] $s Initialize
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set pi [$top NewPagesIter $s];set n 0
for {set p [$pi NextPage $s]} {$p ne "NULL"} {set p [$pi NextPage $s]} {
 set oi [$p NewOffPageConnectorsIter $s]
 for {set o [$oi NextOffPageConnector $s]} {$o ne "NULL"} {set o [$oi NextOffPageConnector $s]} {
  set name [::DE::str $o GetName]
  set dp [::DE::obj [$o GetDisplayProp [::DE::cs Name] $s] $s Name]
  lassign [::DE::point [$o GetHotSpot $s]] hx hy
  set tx [expr {$hx==0 ? 12 : -max(77,7*[string length $name]+15)}]
  ::DE::state [$dp SetLocation [::DE::pt $tx 5]] NamePosition
  ::DE::state [$dp SetFont [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16]] NameFont
  ::DE::state [$o MarkModified] Modified
  incr n
 }
 delete_DboPageOffPageConnectorsIter $oi
}
delete_DboSchematicPagesIter $pi
::DE::save $d
dict create named_ports $n
