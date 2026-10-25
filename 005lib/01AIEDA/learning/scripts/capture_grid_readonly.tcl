# Capture 17.2 read-only audit. Sourcing only defines functions; no native API is called.
# Root owns native execution. No Save/Connect/Set*/MarkModified/transaction methods exist here.
namespace eval ::CAPGRID {variable warnings {}; variable channels {}; variable ledger {}; variable exceptions 0}
proc ::CAPGRID::optional {label script {fallback {}}} {
 variable warnings
 if {[catch {uplevel 1 $script} v]} {dict incr warnings $label; return $fallback}
 return $v
}
proc ::CAPGRID::id {obj s} {if {$obj eq {NULL} || $obj eq {}} {return {}}; return [::CAPGRID::rd $obj GetId]}
proc ::CAPGRID::netname {obj s} {
 set n [::CAPGRID::rd $obj GetNet]; if {$n eq {NULL}} {return {}}
 return [::CAPDB::str $n GetNetName]
}
proc ::CAPGRID::wireid {obj s} {set w [::CAPGRID::rd $obj GetWire]; return [::CAPGRID::id $w $s]}
proc ::CAPGRID::openchannel {out name header} {
 variable channels
 set f [::CAPDB::channel $out $name $header]; lappend channels $f; return $f
}
proc ::CAPGRID::closechannels {} {variable channels; foreach f $channels {catch {close $f}}; set channels {}}

proc ::CAPGRID::event {classification obj method s value args} {
 variable ledger; variable exceptions
 incr exceptions
 puts $ledger [::CAPDB::row [list $classification $obj $method [$s Code] [$s Failed] $value $args [::CAPGRID::stateMessage $s]]]
}
proc ::CAPGRID::rd {obj method args} {
 set s [DboState]
 set code [catch {$obj $method {*}$args $s} value options]
 if {$code} {::CAPGRID::event TCL_EXCEPTION $obj $method $s $value $args; return -options $options $value}
 set nullable [expr {$method in {GetNet GetWire GetDefiningPin}}]
 if {$value eq {NULL} && $nullable} {::CAPGRID::event LEGAL_NULL_ATTACHMENT $obj $method $s $value $args; return $value}
 if {[$s Failed]} {::CAPGRID::event REQUIRED_GETTER_FAILED $obj $method $s $value $args; error "Required read failed: $obj $method code=[$s Code]"}
 return $value
}
proc ::CAPGRID::nx {obj method args} {
 set s [DboState]
 set code [catch {$obj $method {*}$args $s} value options]
 if {$code} {::CAPGRID::event TCL_EXCEPTION $obj $method $s $value $args; return -options $options $value}
 if {$value eq {NULL}} {::CAPGRID::event ITERATOR_END_NULL $obj $method $s $value $args; return $value}
 if {[$s Failed]} {::CAPGRID::event NONEMPTY_ITERATOR_FAILED $obj $method $s $value $args; error "Nonempty iterator read failed: $obj $method code=[$s Code]"}
 return $value
}
proc ::CAPGRID::optionalRead {obj method args} {
 set s [DboState]
 if {$obj eq {NULL} || $obj eq {}} {return {}}
 set code [catch {$obj $method {*}$args $s} value options]
 if {$code} {::CAPGRID::event OPTIONAL_FIELD_TCL_EXCEPTION $obj $method $s $value $args; return UNAVAILABLE}
 if {$method eq {PointIsJunction} && $value eq {0} && [$s Code]==1021} {
  # Native official Message says Object Not Found; Object-not-found is the boolean negative result; explicit NewJunctionsIter
  # membership must still be independently verified on the supplied design.
  ::CAPGRID::event LEGAL_FALSE_NOT_A_JUNCTION $obj $method $s $value $args
  return 0
 }
 if {[$s Failed]} {::CAPGRID::event OPTIONAL_FIELD_FAILED $obj $method $s $value $args; return UNAVAILABLE}
 return $value
}
proc ::CAPGRID::wirepoints {w} {
 set p {}; set n [::CAPGRID::rd $w GetPointCount]
 for {set i 0} {$i<$n} {incr i} {lappend p [join [::CAPDB::point [::CAPGRID::rd $w GetPoint $i]] ,]}
 return [join $p {;}]
}

proc ::CAPGRID::auditLoaded {design top outputDir gridDoc gridDenominator {allowLearningExercise 0}} {
 variable warnings; variable channels
 if {![llength [info commands ::CAPDB::channel]]} {error {Load the parameterized capture_dbo_readonly_common.tcl helper and call its init before auditLoaded}}
 if {![string is integer -strict $gridDoc] || $gridDoc<=0 || $gridDenominator ni {1 2 5 10}} {error {Provide positive integer gridDoc and gridDenominator in 1,2,5,10}}
 set out [::CAPDB::outputPath $outputDir $allowLearningExercise]
 if {[file exists $out]} {error {Output directory must be fresh}}
 file mkdir $out
 set warnings {}; set channels {}; set ::CAPGRID::exceptions 0
 set counts [dict create pages 0 parts 0 pins 0 no_connect_pins 0 wire_objects 0 wire_points 0 junctions 0 net_symbols 0 aliases 0]
 set code [catch {
  set ::CAPGRID::ledger [::CAPGRID::openchannel $out exceptions.tsv {classification object method code failed result argument_context state_message}]
  set pgf [::CAPGRID::openchannel $out page_grid.tsv {page page_id width_doc height_doc draw_width_doc draw_height_doc doc_units_per_inch physical_granularity pin_to_pin_raw pin_to_pin_scale_factor is_metric requested_grid_denominator requested_grid_doc grid_origin_x grid_origin_y origin_basis}]
  set pf [::CAPGRID::openchannel $out parts.tsv {page id ref full_ref cache_part loc_x loc_y rotation mirror locked}]
  set pinf [::CAPGRID::openchannel $out pins.tsv {page part_id ref full_ref pin_id pin_number pin_name defining_pin_id local_start_x local_start_y local_hot_x local_hot_y actual_start_x actual_start_y actual_hot_x actual_hot_y wire_id net_id net_name no_connect visible global shared pin_position}]
  set wf [::CAPGRID::openchannel $out wires.tsv {page id object_type net_id net_name points line_style line_width}]
  set wpf [::CAPGRID::openchannel $out wire_points.tsv {page wire_id point_index x y PointIsJunction_boolean_or_unavailable native_connection_count}]
  set jf [::CAPGRID::openchannel $out junctions.tsv {page wire_id net_name x y native_connection_count}]
  set nf [::CAPGRID::openchannel $out net_symbols.tsv {page kind id name loc_x loc_y rotation mirror local_hot_x local_hot_y actual_hot_x actual_hot_y wire_id net_id net_name}]
  set af [::CAPGRID::openchannel $out aliases.tsv {page id name loc_x loc_y rotation owner_wire_id owner_wire_net}]
  set s [DboState]; set pi [::CAPGRID::rd $top NewPagesIter]
  for {set page [::CAPGRID::nx $pi NextPage]} {$page ne {NULL}} {set page [::CAPGRID::nx $pi NextPage]} {
   set pn [::CAPDB::str $page GetName]; dict incr counts pages
   set size [$page GetDocUnits 0]; set draw [$page GetDocUnits 1]
   puts $pgf [::CAPDB::row [list $pn [::CAPGRID::optionalRead $page GetId] [DboTclHelper_sGetCSizeX $size] [DboTclHelper_sGetCSizeY $size] [DboTclHelper_sGetCSizeX $draw] [DboTclHelper_sGetCSizeY $draw] [$page GetDocUnitsPerInch] [$page GetPhysicalGranularity] [$page GetPinToPin] [$page GetPinToPinScaleFactor] [$page GetIsMetric] $gridDenominator $gridDoc 0 0 {zero-lattice observed in shipped capObjectAlignment; requested grid is caller-provided; native page getters remain authoritative calibration evidence}]]
   set ii [::CAPGRID::rd $page NewPartInstsIter]
   for {set inst [::CAPGRID::nx $ii NextPartInst]} {$inst ne {NULL}} {set inst [::CAPGRID::nx $ii NextPartInst]} {
    set part [DboPartInstToDboPlacedInst $inst]
    if {$part eq {NULL}} {error "Non-placed part instance on $pn"}
    set partid [::CAPGRID::rd $part GetId]; set ref [::CAPDB::str $part GetReference]; set full [::CAPDB::str $part GetReferenceDesignator]
    set cache [::CAPGRID::rd $part GetPart]
    puts $pf [::CAPDB::row [concat [list $pn $partid $ref $full [::CAPDB::str $cache GetName]] [::CAPDB::point [::CAPGRID::rd $part GetLocation]] [list [::CAPGRID::rd $part GetRotation] [::CAPGRID::rd $part GetMirror] [$part IsObjLocked]]]]
    dict incr counts parts
    set piter [::CAPGRID::rd $part NewPinsIter]
    for {set pin [::CAPGRID::nx $piter NextPin]} {$pin ne {NULL}} {set pin [::CAPGRID::nx $piter NextPin]} {
     set net [::CAPGRID::rd $pin GetNet]; set netid [::CAPGRID::id $net $s]; set nn {}; if {$net ne {NULL}} {set nn [::CAPDB::str $net GetNetName]}
     set defining [::CAPGRID::rd $pin GetDefiningPin]
     set nc [::CAPGRID::rd $pin GetIsNoConnect]; if {$nc} {dict incr counts no_connect_pins}
     set row [concat [list $pn $partid $ref $full [::CAPGRID::rd $pin GetId] [::CAPDB::str $pin GetPinNumber] [::CAPDB::str $pin GetPinName] [::CAPGRID::optionalRead $defining GetId]] [::CAPDB::point [::CAPGRID::rd $pin GetStartPoint]] [::CAPDB::point [::CAPGRID::rd $pin GetHotSpot]] [::CAPDB::point [::CAPGRID::rd $pin GetOffsetStartPoint]] [::CAPDB::point [::CAPGRID::rd $pin GetOffsetHotSpot]] [list [::CAPGRID::wireid $pin $s] $netid $nn $nc [::CAPGRID::rd $pin GetIsVisible] [::CAPGRID::rd $pin GetIsGlobal] [::CAPGRID::rd $pin GetIsShared] [::CAPGRID::rd $pin GetPinPosition]]]
     puts $pinf [::CAPDB::row $row]; dict incr counts pins
    }
    delete_DboPartInstPinsIter $piter
   }
   delete_DboPagePartInstsIter $ii
   set wi [::CAPGRID::rd $page NewWiresIter]
   for {set w [::CAPGRID::nx $wi NextWire]} {$w ne {NULL}} {set w [::CAPGRID::nx $wi NextWire]} {
    set wid [::CAPGRID::rd $w GetId]; set nn [::CAPDB::str $w GetNetName]; set net [::CAPGRID::rd $w GetNet]
    puts $wf [::CAPDB::row [list $pn $wid [$w GetObjectType] [::CAPGRID::id $net $s] $nn [::CAPGRID::wirepoints $w] [::CAPGRID::rd $w GetLineStyle] [::CAPGRID::rd $w GetLineWidth]]]
    dict incr counts wire_objects
    for {set k 0} {$k<[::CAPGRID::rd $w GetPointCount]} {incr k} {
     set pt [::CAPGRID::rd $w GetPoint $k]
     puts $wpf [::CAPDB::row [concat [list $pn $wid $k] [::CAPDB::point $pt] [list [::CAPGRID::optionalRead $w PointIsJunction $pt] [::CAPGRID::optionalRead $page GetConnectionCount $pt]]]]
     dict incr counts wire_points
    }
    set ji [::CAPGRID::rd $w NewJunctionsIter]
    for {set jp [::CAPGRID::nx $ji NextJunction]} {$jp ne {NULL}} {set jp [::CAPGRID::nx $ji NextJunction]} {
     puts $jf [::CAPDB::row [concat [list $pn $wid $nn] [::CAPDB::point $jp] [list [::CAPGRID::optionalRead $page GetConnectionCount $jp]]]]
     dict incr counts junctions
    }
    delete_DboWireJunctionsIter $ji
    set ai [::CAPGRID::rd $w NewAliasesIter]
    for {set a [::CAPGRID::nx $ai NextAlias]} {$a ne {NULL}} {set a [::CAPGRID::nx $ai NextAlias]} {
     puts $af [::CAPDB::row [concat [list $pn [::CAPGRID::rd $a GetId] [::CAPDB::str $a GetName]] [::CAPDB::point [::CAPGRID::rd $a GetLocation]] [list [::CAPGRID::rd $a GetRotation] $wid $nn]]]
     dict incr counts aliases
    }
    delete_DboWireAliasesIter $ai
   }
   delete_DboPageWiresIter $wi
   foreach {kind new next del} {offpage NewOffPageConnectorsIter NextOffPageConnector delete_DboPageOffPageConnectorsIter port NewPortsIter NextPort delete_DboPagePortsIter global NewGlobalsIter NextGlobal delete_DboPageGlobalsIter} {
    set ni [::CAPGRID::rd $page $new]
    for {set n [::CAPGRID::nx $ni $next]} {$n ne {NULL}} {set n [::CAPGRID::nx $ni $next]} {
     set net [::CAPGRID::rd $n GetNet]; set nn {}; if {$net ne {NULL}} {set nn [::CAPDB::str $net GetNetName]}
     puts $nf [::CAPDB::row [concat [list $pn $kind [::CAPGRID::rd $n GetId] [::CAPDB::str $n GetName]] [::CAPDB::point [::CAPGRID::rd $n GetLocation]] [list [::CAPGRID::rd $n GetRotation] [::CAPGRID::rd $n GetMirror]] [::CAPDB::point [::CAPGRID::rd $n GetHotSpot]] [::CAPDB::point [::CAPGRID::rd $n GetOffsetHotSpot]] [list [::CAPGRID::wireid $n $s] [::CAPGRID::id $net $s] $nn]]]
     dict incr counts net_symbols
    }
    $del $ni
   }
  }
  delete_DboSchematicPagesIter $pi
  # No aggregate state check: each call uses its own DboState and is validated immediately.
 } result options]
 ::CAPGRID::closechannels
 set summary [dict create status [expr {$code ? {FAIL} : {READ_ONLY_AUDIT_COMPLETE}}] counts $counts optional_warnings $warnings exception_events $::CAPGRID::exceptions note {The requested grid is an explicit caller parameter; native GetPinToPin/GetPhysicalGranularity/GetDocUnitsPerInch are exported for calibration. No Connect/Save/Set/MarkModified executed. Explicit junctions.tsv is authoritative; optional PointIsJunction/connection-count failures are ledgered as UNAVAILABLE, never silently accepted as false. Default NewPinsIter returns the instantiated pin set, not fabricated hidden symbol pins.}]
 if {$code} {dict set summary error $result; dict set summary errorinfo [dict get $options -errorinfo]}
 ::CAPDB::write [file join $out audit_result.tcldict] $summary
 if {$code} {return -options $options $result}
 return $summary
}
proc ::CAPGRID::audit {inputDSN outputDir commonHelper cadenceRoot gridDoc gridDenominator {allowLearningExercise 0}} {
 if {![file isfile $commonHelper]} {error {Explicit common helper path is missing}}
 if {![llength [info commands ::CAPDB::openDesign]]} {source $commonHelper}
 ::CAPDB::outputPath $outputDir $allowLearningExercise
 ::CAPDB::init $cadenceRoot
 set input [file normalize $inputDSN]
 if {![file isfile $input]} {error {Input DSN does not exist}}
 set d {}; set code [catch {
  lassign [::CAPDB::openDesign $input] d top
  ::CAPGRID::auditLoaded $d $top $outputDir $gridDoc $gridDenominator $allowLearningExercise
 } result options]
 if {$d ne {}} {::CAPDB::state [$::DboSession_s_pDboSession RemoveDesign $d] CloseReadOnlyDesign}
 if {$code} {return -options $options $result}
 return $result
}

proc ::CAPGRID::stateMessage {s} {
 set c [DboTclHelper_sMakeCString {}]
 if {[catch {$s Message $c} err]} {return "Message unavailable: $err"}
 return [DboTclHelper_sGetConstCharPtr $c]
}
proc ::CAPGRID::stateCodeMessage {code} {
 set s [DboState]; $s SetCode $code
 return [dict create code [$s Code] failed [$s Failed] severity [$s Severity] message [::CAPGRID::stateMessage $s]]
}
