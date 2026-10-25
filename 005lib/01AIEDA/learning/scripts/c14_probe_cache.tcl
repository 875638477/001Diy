source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
set C14s [::C12::session]; set C14st [DboState]
set C14des [$C14s GetOpenDesign [::C12::cstring D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/run02/c14_baseline.dsn] $C14st]
set C14r [list session $C14s design $C14des]
foreach C14o [list $C14s $C14des] {catch {$C14o BAD} C14err; lappend C14r $C14err}
set C14r
