# diagnose_pins.tcl
# Scan all pages/parts/pins in the active OrCAD Capture design
# Report: empty Pin Numbers and duplicate Pin Names
# Read-only -- does NOT modify anything

proc diagnose_pins {} {
    puts "=== diagnose_pins: starting ==="

    set lSession $::DboSession_s_pDboSession
    DboSession -this $lSession
    set lNullObj NULL
    set lStatus [DboState]
    set lDesign [$lSession GetActiveDesign]

    if {$lDesign == $lNullObj} {
        puts "ERROR: No active design."
        return
    }

    set totalEmptyNum 0
    set totalDupName 0

    set lViewIter [$lDesign NewViewsIter $lStatus $::IterDefs_SCHEMATICS]
    set lView [$lViewIter NextView $lStatus]

    while {$lView != $lNullObj} {
        set lSchematic [DboViewToDboSchematic $lView]
        set lPagesIter [$lSchematic NewPagesIter $lStatus]
        set lPage [$lPagesIter NextPage $lStatus]

        while {$lPage != $lNullObj} {
            set lPageNameCS [DboTclHelper_sMakeCString]
            $lPage GetName $lPageNameCS
            set pageName [DboTclHelper_sGetConstCharPtr $lPageNameCS]
            puts "Scanning page: $pageName"

            set lPartInstsIter [$lPage NewPartInstsIter $lStatus]
            set lInst [$lPartInstsIter NextPartInst $lStatus]

            while {$lInst != $lNullObj} {
                set lPlacedInst [DboPartInstToDboPlacedInst $lInst]
                if {$lPlacedInst == $lNullObj} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set lRefDesCS [DboTclHelper_sMakeCString]
                $lPlacedInst GetReferenceDesignator $lRefDesCS
                set refDes [DboTclHelper_sGetConstCharPtr $lRefDesCS]

                set count [$lInst GetPinCount $lStatus]
                set emptyNums {}
                set pinNameCount [dict create]

                for {set i 0} {$i < $count} {incr i} {
                    set portInst [$lInst GetPin $i $lStatus]
                    set pName [DboTclHelper_sMakeCString]
                    set pNumber [DboTclHelper_sMakeCString]
                    $portInst GetPinName $pName
                    $portInst GetPinNumber $pNumber
                    set pinName [DboTclHelper_sGetConstCharPtr $pName]
                    set pinNum [DboTclHelper_sGetConstCharPtr $pNumber]

                    if {$pinNum == ""} {
                        lappend emptyNums $pinName
                        incr totalEmptyNum
                    }

                    if {[dict exists $pinNameCount $pinName]} {
                        dict set pinNameCount $pinName [expr {[dict get $pinNameCount $pinName] + 1}]
                    } else {
                        dict set pinNameCount $pinName 1
                    }
                }

                set dupNames {}
                dict for {name cnt} $pinNameCount {
                    if {$cnt > 1} {
                        lappend dupNames "${name}(x${cnt})"
                        set totalDupName [expr {$totalDupName + $cnt}]
                    }
                }

                if {[llength $emptyNums] > 0 || [llength $dupNames] > 0} {
                    puts "  $refDes ($pageName): pins=$count"
                    if {[llength $emptyNums] > 0} {
                        puts "    Empty PinNumber ([llength $emptyNums]): $emptyNums"
                    }
                    if {[llength $dupNames] > 0} {
                        puts "    Duplicate PinName: $dupNames"
                    }
                }

                set lInst [$lPartInstsIter NextPartInst $lStatus]
            }
            delete_DboPagePartInstsIter $lPartInstsIter
            set lPage [$lPagesIter NextPage $lStatus]
        }
        delete_DboSchematicPagesIter $lPagesIter
        set lView [$lViewIter NextView $lStatus]
    }
    delete_DboLibViewsIter $lViewIter

    puts ""
    puts "========== DIAGNOSIS SUMMARY =========="
    puts "Total pins with empty Pin Number: $totalEmptyNum"
    puts "Total pins with duplicate Pin Name: $totalDupName"
    puts "======================================="
}

diagnose_pins
