namespace eval ::C13Probe {
set session $::DboSession_s_pDboSession
set s [DboState]
set result {}
foreach pair {{hc C:/Program0/Cadence/spb172/tools/capture/library/pspice/74hc.olb} {cap C:/Program0/Cadence/spb172/tools/capture/library/capsym.olb}} {
  lassign $pair tag path
  set lib [$session GetLib [DboTclHelper_sMakeCString $path] $s]
  dict set result $tag lib $lib
  if {$tag eq "hc"} {
    foreach nm {74HC00 74HC00.Normal 74HC00.Normal_A 7400} {
      dict set result $tag package $nm [$lib GetPackage [DboTclHelper_sMakeCString $nm] $s]
      dict set result $tag part $nm [$lib GetPart [DboTclHelper_sMakeCString $nm] $s]
    }
    set it [$lib NewPackagesIter $s]; set names {}
    for {set p [$it NextPackage $s]} {$p ne "NULL"} {set p [$it NextPackage $s]} {set n [DboTclHelper_sMakeCString]; $p GetName $n; lappend names [DboTclHelper_sGetConstCharPtr $n]}
    dict set result hc names $names
  } else {
    foreach nm {VCC GND GND_POWER VCC_BAR} {dict set result cap global $nm [$lib GetGlobalSymbol [DboTclHelper_sMakeCString $nm] $s]}
    foreach nm {OFFPAGELEFT-L OFFPAGERIGHT-R OFFPAGELEFT OFFPAGERIGHT} {dict set result cap offpage $nm [$lib GetOffPageSymbol [DboTclHelper_sMakeCString $nm] $s]}
    foreach nm {PORTLEFT-L PORTRIGHT-R PORTLEFT PORTRIGHT} {dict set result cap port $nm [$lib GetPortSymbol [DboTclHelper_sMakeCString $nm] $s]}
  }
}
set out $result
}
set ::C13Probe::out
