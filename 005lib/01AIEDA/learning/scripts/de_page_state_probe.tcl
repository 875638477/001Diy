set s [DboState]
set path {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/native/de_integrated_eco.dsn}
set d [::DE::obj [$::DboSession_s_pDboSession GetDesignAndSchematics [::DE::cs $path] $s] $s Open];lappend ::DE::designs $d
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
::DE::obj [$d GetRootOccurrence $s] $s InitializeOccurrence
set i [$top NewPagesIter $s]
set msg [::DE::cs {}];$s Message $msg
set report [dict create iter_failed [$s Failed] iter_code [$s Code] iter_message [DboTclHelper_sGetConstCharPtr $msg]]
set s [DboState]
set p [$i NextPage $s]
$s Message $msg
dict set report page_pointer $p;dict set report page_failed [$s Failed];dict set report page_code [$s Code];dict set report page_message [DboTclHelper_sGetConstCharPtr $msg]
if {$p ne "NULL"} {dict set report page_name [::DE::str $p GetName]}
delete_DboSchematicPagesIter $i
set report
