set s [DboState]
set lib [::DE::obj [$::DboSession_s_pDboSession GetLib [::DE::cs {C:/Program0/Cadence/spb172/tools/capture/library/capsym.olb}] $s] $s Capsym]
lappend ::DE::libs $lib
set i [$lib NewSymbolsIter $s]
set names {}
for {set o [$i NextSymbol $s]} {$o ne "NULL"} {set o [$i NextSymbol $s]} {lappend names [::DE::str $o GetName]}
delete_DboLibSymbolsIter $i
set names
