source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
set s [::C12::session];set st [DboState]
set path {D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/final/library/c14_qmi8610_v2.olb}
set lib [::C12::nonnull [$s GetLib [::C12::cstring $path] $st] $st GetDelivery]
set pkg [::C12::nonnull [$lib GetPackage [::C12::cstring QMI8610_C12] $st] $st Package]
set dev [::C12::nonnull [$pkg GetDevice 0 $st] $st Device]
set cell [::C12::nonnull [$dev GetCell $st] $st Cell]
set part [::C12::nonnull [$cell FindPart 0 $st] $st Part]
set pi [$part NewLPinsIter $st]
for {set pin [$pi NextPin $st]} {$pin ne "NULL"} {set pin [$pi NextPin $st]} {
 if {[$pin GetPinPosition $st]==3} {::C12::check [$pin SetIsNumberVisible 1] ShowPin4Number}
}
delete_DboLibPartPinsIter $pi
$part MarkModified
::C12::check [$lib SavePackageAll $pkg] SavePackageAll
::C12::check [$s SaveLib $lib] SaveLib
::C12::check [$s RemoveLib $lib] CloseDelivery
set result [dict create normalized_pin4_number_visible 1 path $path reason {Preserve visible physical numbering; experimental single-pin hiding did not propagate through native ReplaceInst}]
