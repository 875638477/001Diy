# Library-only definitions extracted from the executed native operations.
# Does not open or save any file until explicitly called with a DboLib object.
proc m2LibraryChanges {lib} {
 proc m2c {s} {DboTclHelper_sMakeCString $s}
 proc m2check {s} {if {[$s Failed]} {error {Dbo operation failed}}}
 set st [DboState]
 set pkg [$lib GetPackage [m2c {M_2 KEY M}] $st];m2check $st
 set dev [$pkg GetDevice 0 $st];set cell [$dev GetCell $st];set part [$cell FindPart 0 $st]
 foreach {pos number} {71 80 70 79 69 78 68 77 67 76} {
  set b [m2c {}];m2check [$dev GetPinNumber $pos $b]
  if {[DboTclHelper_sGetConstCharPtr $b] ne $number} {error {Expected original 72-pin symbol}}
  m2check [$part DeleteSymbolPinAtPosition $pos]
  m2check [$dev DeletePinNumberAtPosition $pos]
 }
 m2check [$part MarkModified];m2check [$lib SavePackageAll $pkg]
 set pkg [$lib GetPackage [m2c M_2-05NGFF-KEY-M] $st];m2check $st
 set dev [$pkg GetDevice 0 $st];set cell [$dev GetCell $st];set part [$cell FindPart 0 $st]
 m2check [$pkg SetPCBFootprint [m2c md2_NGFF_M_SMT]]
 m2check [$part SetUserPropStringValue [m2c {PCB Footprint}] [m2c md2_NGFF_M_SMT]]
 m2check [$lib SavePackageAll $pkg]
}
