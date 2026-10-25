set ::C14DefinitionsOnly 1
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c14_propagation.tcl}
proc ::C14Prop::verifySaved {} {
 set root {D:/001DIY/005lib/01AIEDA/learning}
 set log "$root/logs/lesson14_capture_20261019/independent_natural"
 set sources [list baseline "$root/examples/lesson14_capture/run04/c14_baseline.dsn"]
 foreach mode {update_preserve relocated_preserve replace_properties} {lappend sources $mode "$root/examples/lesson14_capture/final/c14_${mode}.dsn"}
 lappend sources ready "$root/examples/lesson14_capture/final/c14_ready.dsn"
 set s [::C12::session];set st [DboState];set results {}
 foreach {mode source} $sources {
  set design [nn [$s GetDesignAndSchematics [c $source] $st] $st OpenReadOnly]
  set sch [nn [$design GetRootSchematic $st] $st RootSchematic]
  # These are single-page schematics. GetDesignAndSchematics has loaded them;
  # forcing Expand again duplicates containers in this 17.2 SDK environment.
  set rootOccurrence [nn [$design GetRootOccurrence $st] $st RootOccurrence]
  set ni [$design NewFlatNetsIter $st]
  set rows [list "flat_net\treference\tpin_number\tpin_name\tpage"]
  set count 0
  for {set net [$ni NextFlatNet $st]} {$net ne "NULL"} {set net [$ni NextFlatNet $st]} {
   set name [::C14Research::readString $net GetName]
   set oi [$net NewNetOccurrencesIter]
   for {set occ [$oi NextNetOccurrence $st]} {$occ ne "NULL"} {set occ [$oi NextNetOccurrence $st]} {
    set sn [nn [$occ GetNet $st] $st SchematicNet]
    set pi [$sn NewPortInstsIter $st]
    for {set pin [$pi NextPortInst $st]} {$pin ne "NULL"} {set pin [$pi NextPortInst $st]} {
     set inst [nn [$pin GetOwner] $st PinOwner]
     set page [nn [$inst GetOwner] $st InstanceOwner]
     lappend rows [join [list $name [::C14Research::readString $inst GetReference] [::C14Research::readString $pin GetPinNumber] [::C14Research::readString $pin GetPinName] [::C14Research::readString $page GetName]] "\t"]
     incr count
    }
    delete_DboSchematicNetPortInstsIter $pi
   }
   delete_DboFlatNetNetOccurrencesIter $oi
  }
  delete_DboDesignFlatNetsIter $ni
  file mkdir "$log/$mode"
  set f [open "$log/$mode/connectivity.tsv" w]; fconfigure $f -encoding utf-8 -translation lf
  puts $f [join $rows "\n"];close $f
  snapshot $design "$log/$mode/snapshot"
  dict set results $mode [dict create connectedPinRows $count]
  check [$s RemoveDesign $design] CloseReadOnly
 }
 set lib [nn [$s GetLib [c "$root/examples/lesson14_capture/final/library/c14_qmi8610_v2.olb"] $st] $st DeliveryLib]
 set pkg [nn [$lib GetPackage [c QMI8610_C12] $st] $st DeliveryPackage]
 ::C14Research::snapshotPackage $pkg "$log/delivery_olb.tcldict"
 check [$s RemoveLib $lib] CloseDelivery
 return $results
}
::C14Prop::verifySaved
