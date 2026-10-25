set s [DboState]
set path {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/a4_review/native/de_integrated_a4.dsn}
set d [::DE::obj [$::DboSession_s_pDboSession GetDesignAndSchematics [::DE::cs $path] $s] $s OpenA4]
lappend ::DE::designs $d
::DE::obj [$d GetRootOccurrence $s] $s Initialize
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set pi [$top NewPagesIter $s];set n 0
for {set p [$pi NextPage $s]} {$p ne "NULL"} {set p [$pi NextPage $s]} {
 incr n;set name [::DE::str $p GetName]
 foreach {x y text height} [list 50 35 "STM32F103C8T6  |  $name" -16 50 790 "Training schematic  |  A4 297 x 210 mm  |  Rev A4-01  |  Sheet $n / 12" -10] {
  set comment [::DE::obj [$p NewGraphicCommentTextInst $s [DboTclHelper_sMakeCRect 0 0 1050 25] [::DE::pt $x $y] [::DE::cs $text] [DboTclHelper_sMakeLOGFONT Arial $height 0 0 0 400 0 0 0 0 7 0 1 16] 0] $s PageHeading]
  ::DE::state [$comment MarkModified] HeadingModified
 }
}
delete_DboSchematicPagesIter $pi
if {$n!=12} {error "Unexpected page count $n"}
::DE::save $d
dict create pages $n headings 24
