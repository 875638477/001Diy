# fix_pin_name_spaces.tcl
# OrCAD Capture Tcl script:
#   1. Replace whitespace in schematic symbol Pin Name with "_"
#   2. Add _2/_3... suffix when the sanitized Pin Name is still duplicated
#
# Usage in OrCAD Capture command window:
#   source {D:\001DIY\005lib\01script_file\fix_pin_name_spaces.tcl}
#
# Notes:
#   - Open the target .opj/.dsn first.
#   - Save a backup before running.
#   - After running, Ctrl+S and re-create Allegro netlist.

proc _sanitize_pin_name {pinName} {
    set newName [string trim $pinName]

    # Convert any consecutive spaces/tabs/newlines to one underscore.
    regsub -all {\s+} $newName {_} newName

    # Avoid empty Pin Name after trimming.
    if {$newName == ""} {
        set newName "PIN"
    }

    return $newName
}

proc fix_pin_name_spaces {} {
    puts "=== fix_pin_name_spaces: starting ==="

    set lSession $::DboSession_s_pDboSession
    DboSession -this $lSession
    set lNullObj NULL
    set lStatus [DboState]
    set lDesign [$lSession GetActiveDesign]

    if {$lDesign == $lNullObj} {
        puts "ERROR: No active design. Please open the target .opj/.dsn first."
        return
    }

    set totalChanged 0
    set totalDuplicateFixed 0
    set processedParts {}

    set lViewIter [$lDesign NewViewsIter $lStatus $::IterDefs_SCHEMATICS]
    set lView [$lViewIter NextView $lStatus]

    while {$lView != $lNullObj} {
        set lSchematic [DboViewToDboSchematic $lView]
        set lPagesIter [$lSchematic NewPagesIter $lStatus]
        set lPage [$lPagesIter NextPage $lStatus]

        while {$lPage != $lNullObj} {
            set lPartInstsIter [$lPage NewPartInstsIter $lStatus]
            set lInst [$lPartInstsIter NextPartInst $lStatus]

            while {$lInst != $lNullObj} {
                set lPlacedInst [DboPartInstToDboPlacedInst $lInst]
                if {$lPlacedInst == $lNullObj} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set lRefCS [DboTclHelper_sMakeCString]
                $lPlacedInst GetReferenceDesignator $lRefCS
                set refDes [DboTclHelper_sGetConstCharPtr $lRefCS]

                set lPart [$lPlacedInst GetPart $lStatus]
                if {$lPart == $lNullObj} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set lPartNameCS [DboTclHelper_sMakeCString]
                $lPart GetName $lPartNameCS
                set partName [DboTclHelper_sGetConstCharPtr $lPartNameCS]

                # Process each library/cache part once, even if it is placed many times.
                if {[lsearch -exact $processedParts $partName] >= 0} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }
                lappend processedParts $partName

                set seen [dict create]
                set lPinIter [$lPart NewPinsIter $lStatus]
                set lPin [$lPinIter NextPin $lStatus]

                while {$lPin != $lNullObj} {
                    set lOldNameCS [DboTclHelper_sMakeCString]
                    $lPin GetPinName $lOldNameCS
                    set oldName [DboTclHelper_sGetConstCharPtr $lOldNameCS]

                    set baseName [_sanitize_pin_name $oldName]
                    set newName $baseName

                    if {[dict exists $seen $baseName]} {
                        set count [dict get $seen $baseName]
                        incr count
                        dict set seen $baseName $count
                        set newName "${baseName}_${count}"
                        incr totalDuplicateFixed
                    } else {
                        dict set seen $baseName 1
                    }

                    if {$newName != $oldName} {
                        set lNewNameCS [DboTclHelper_sMakeCString $newName]
                        if {[catch {$lPin SetPinName $lNewNameCS} err]} {
                            puts "WARN: SetPinName failed: $refDes ($partName) '$oldName' -> '$newName': $err"
                        } else {
                            puts "FIX: $refDes ($partName) '$oldName' -> '$newName'"
                            incr totalChanged
                        }
                    }

                    set lPin [$lPinIter NextPin $lStatus]
                }

                delete_DboSymbolPinsIter $lPinIter
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
    puts "========== FIX SUMMARY =========="
    puts "Pin Names changed: $totalChanged"
    puts "Duplicate Pin Names suffixed: $totalDuplicateFixed"
    puts "Processed unique Parts: [llength $processedParts]"
    puts "================================="
    puts "Please save (Ctrl+S) and re-create Allegro netlist."
}

fix_pin_name_spaces
