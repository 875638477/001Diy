set path {D:/001DIY/005lib/01AIEDA/learning/staging/de_15_26_20261019/minimal_factory/native/de_integrated_two_res.dsn}
set sess $::DboSession_s_pDboSession;set s [DboState]
set d [::DE::obj [$sess GetDesignAndSchematics [::DE::cs $path] $s] $s ReadDesign];lappend ::DE::designs $d
set sch [::DE::obj [$d GetRootSchematic $s] $s Root]
set it [$sch NewPagesIter $s];set rows {}
for {set page [$it NextPage $s]} {$page ne "NULL"} {set page [$it NextPage $s]} {
 set pn [::DE::str $page GetName];set wires [$page NewWiresIter $s];set count 0;set points {}
 for {set w [$wires NextWire $s]} {$w ne "NULL"} {set w [$wires NextWire $s]} {
  incr count;lappend points [list [::DE::point [$w GetStartPoint $s]] [::DE::point [$w GetEndPoint $s]]]
 }
 delete_DboPageWiresIter $wires
 lappend rows [list $pn wires $count points $points pageNumber [$page GetPageNumber $s]]
}
delete_DboSchematicPagesIter $it
::DE::state [$sess RemoveDesign $d] Close;set ::DE::designs {}
set rows
