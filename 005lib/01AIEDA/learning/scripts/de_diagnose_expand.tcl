set s [DboState]
set p {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/native/de_integrated_baseline.dsn}
set d [::DE::obj [$::DboSession_s_pDboSession GetDesign [::DE::cs $p] $s] $s Open]
lappend ::DE::designs $d
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set r [$top Expand]
set msg [::DE::cs {}];$r Message $msg
set result [dict create failed [$r Failed] code [$r Code] severity [$r Severity] message [DboTclHelper_sGetConstCharPtr $msg]]
::DE::write {D:/001DIY/005lib/01AIEDA/learning/logs/de_15_26_20261019/expand_state.tcldict} $result
set rows "name\tpage_number\tid\tinstances\twires"
set pi [$top NewPagesIter $s]
for {set page [$pi NextPage $s]} {$page ne "NULL"} {set page [$pi NextPage $s]} {
 set ii [$page NewPartInstsIter $s];set ni 0
 for {set i [$ii NextPartInst $s]} {$i ne "NULL"} {set i [$ii NextPartInst $s]} {incr ni}
 delete_DboPagePartInstsIter $ii
 set wi [$page NewWiresIter $s];set nw 0
 for {set w [$wi NextWire $s]} {$w ne "NULL"} {set w [$wi NextWire $s]} {incr nw}
 delete_DboPageWiresIter $wi
 append rows "\n[join [list [::DE::str $page GetName] [$page GetPageNumber $s] [$page GetId $s] $ni $nw] \t]"
}
delete_DboSchematicPagesIter $pi
::DE::write {D:/001DIY/005lib/01AIEDA/learning/logs/de_15_26_20261019/page_inventory.tcldict} $rows
set result
