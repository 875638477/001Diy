set s [DboState]
set d [::DE::obj [$::DboSession_s_pDboSession GetDesignAndSchematics [::DE::cs {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/a4_review/native/de_integrated_a4.dsn}] $s] $s Open]
lappend ::DE::designs $d
::DE::obj [$d GetRootOccurrence $s] $s Initialize
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set pages [$top NewPagesIter $s];set p [$pages NextPage $s]
set ports [$p NewOffPageConnectorsIter $s]
set rows "net\tproperty\ttype\tx\ty"
for {set o [$ports NextOffPageConnector $s]} {$o ne "NULL"} {set o [$ports NextOffPageConnector $s]} {
 set di [$o NewDisplayPropsIter $s];set num 0
 for {set dp [$di NextProp $s]} {$dp ne "NULL"} {set dp [$di NextProp $s]} {
  incr num
  append rows "\n[join [concat [list [::DE::str $o GetName] [::DE::str $dp GetName] [$dp GetDisplayType $s]] [::DE::point [$dp GetLocation $s]]] \t]"
 }
 if {!$num} {append rows "\n[::DE::str $o GetName]\t__NO_DISPLAY_PROPS__\t\t\t"}
 delete_DboDisplayPropsIter $di
}
delete_DboPageOffPageConnectorsIter $ports
delete_DboSchematicPagesIter $pages
::DE::write {D:/001DIY/005lib/01AIEDA/learning/staging/a4_review_20261019/port_display_props.tsv} $rows
set rows
