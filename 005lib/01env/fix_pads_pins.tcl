# fix_pads_pins.tcl
# Batch fix PADS-imported symbols in OrCAD Capture:
#   1. Set Pin Number = Pin Name for empty Pin Numbers
#   2. Add suffix to duplicate Pin Names
#
# Safe approach:
#   Phase 1: READ via instance API to find which Parts need fixing
#   Phase 2: Iterate ALL Packages, navigate to Part, match against fix list,
#            then use Device.NewPinNumber (official Cadence API)
#   Phase 3: Fix duplicate Pin Names via GetPart → SetPinName

proc fix_pads_pins {} {
    puts "=== fix_pads_pins: starting ==="

    set lSession $::DboSession_s_pDboSession
    DboSession -this $lSession
    set lNullObj NULL
    set lStatus [DboState]
    set lDesign [$lSession GetActiveDesign]

    if {$lDesign == $lNullObj} {
        puts "ERROR: No active design."
        return
    }

    # ============================================================
    # PHASE 1: Scan instances to collect Part names needing fix
    # ============================================================
    puts ""
    puts "--- Phase 1: Scanning for parts with empty Pin Numbers ---"

    set partsNeedFix [dict create]
    set scannedParts {}

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

                set lPart [$lPlacedInst GetPart $lStatus]
                if {$lPart != $lNullObj} {
                    set lPartNameCS [DboTclHelper_sMakeCString]
                    $lPart GetName $lPartNameCS
                    set partName [DboTclHelper_sGetConstCharPtr $lPartNameCS]

                    if {[lsearch -exact $scannedParts $partName] < 0} {
                        lappend scannedParts $partName

                        set count [$lInst GetPinCount $lStatus]
                        for {set i 0} {$i < $count} {incr i} {
                            set portInst [$lInst GetPin $i $lStatus]
                            set pNumber [DboTclHelper_sMakeCString]
                            $portInst GetPinNumber $pNumber
                            if {[DboTclHelper_sGetConstCharPtr $pNumber] == ""} {
                                dict set partsNeedFix $partName 1
                                set lRefCS [DboTclHelper_sMakeCString]
                                $lPlacedInst GetReferenceDesignator $lRefCS
                                puts "  Need fix: '$partName' (e.g. [DboTclHelper_sGetConstCharPtr $lRefCS])"
                                break
                            }
                        }
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

    set numToFix [dict size $partsNeedFix]
    puts "  Parts needing Pin Number fix: $numToFix"

    # ============================================================
    # PHASE 2: Iterate ALL Packages, navigate down to Part,
    #          match Part name against fix list, then NewPinNumber
    # ============================================================
    puts ""
    puts "--- Phase 2: Fixing Pin Numbers via Package/Device API ---"

    set totalFixedNum 0
    set matchedPkgs 0

    set lPkgNamesIter [$lDesign NewPackageNamesIter $lStatus]
    set lPkgCS [DboTclHelper_sMakeCString]
    set lNS [$lPkgNamesIter NextName $lPkgCS]

    while {[$lNS OK] == 1} {
        set pkgName [DboTclHelper_sGetConstCharPtr $lPkgCS]

        if {[catch {
            set lPackage [$lDesign GetPackage $lPkgCS $lStatus]
        } err]} {
            set lNS [$lPkgNamesIter NextName $lPkgCS]
            continue
        }
        if {$lPackage == $lNullObj} {
            set lNS [$lPkgNamesIter NextName $lPkgCS]
            continue
        }

        set devIdx 0
        while {1} {
            if {[catch {set lDevice [$lPackage GetDevice $devIdx $lStatus]} err]} { break }
            if {$lDevice == $lNullObj} { break }

            if {[catch {set lCell [$lDevice GetCell $lStatus]} err]} {
                incr devIdx; continue
            }
            if {$lCell == $lNullObj} { incr devIdx; continue }

            if {[catch {set lNormalPart [$lCell FindPart $devIdx $lStatus]} err]} {
                incr devIdx; continue
            }
            if {$lNormalPart == $lNullObj} {
                if {[catch {set lNormalPart [$lCell FindPart 0 $lStatus]} err]} {
                    incr devIdx; continue
                }
                if {$lNormalPart == $lNullObj} { incr devIdx; continue }
            }

            set lCellPartNameCS [DboTclHelper_sMakeCString]
            $lNormalPart GetName $lCellPartNameCS
            set cellPartName [DboTclHelper_sGetConstCharPtr $lCellPartNameCS]

            if {[dict exists $partsNeedFix $cellPartName]} {
                puts "  MATCH: Package '$pkgName' -> Part '$cellPartName'"
                incr matchedPkgs

                set lPinIter [$lNormalPart NewLPinsIter $lStatus]
                set lPin [$lPinIter NextPin $lStatus]

                while {$lPin != $lNullObj} {
                    set lPinNameCS [DboTclHelper_sMakeCString]
                    $lPin GetPinName $lPinNameCS
                    set pinName [DboTclHelper_sGetConstCharPtr $lPinNameCS]

                    if {$pinName != ""} {
                        set lPinPos [$lPin GetPinPosition $lStatus]
                        set lPinPosInt [DboTclHelper_sMakeInt $lPinPos]
                        set lNewNumCS [DboTclHelper_sMakeCString $pinName]

                        if {[catch {$lDevice NewPinNumber $lNewNumCS $lPinPosInt 1 -1} err]} {
                            puts "    FAIL: '$pinName' pos=$lPinPosInt: $err"
                        } else {
                            puts "    FIX: '$pinName' -> '$pinName'"
                            incr totalFixedNum
                        }
                    }

                    set lPin [$lPinIter NextPin $lStatus]
                }

                dict unset partsNeedFix $cellPartName
            }

            incr devIdx
        }

        set lNS [$lPkgNamesIter NextName $lPkgCS]
    }

    set unmatched [dict size $partsNeedFix]
    if {$unmatched > 0} {
        puts "  WARNING: $unmatched parts not found in any Package:"
        dict for {nm dummy} $partsNeedFix {
            puts "    - '$nm'"
        }
    }

    puts "  Packages matched: $matchedPkgs"
    puts "  Pin Numbers fixed: $totalFixedNum"

    # ============================================================
    # PHASE 3: Fix duplicate Pin Names via GetPart API
    # ============================================================
    puts ""
    puts "--- Phase 3: Fix duplicate Pin Names ---"

    set totalFixedName 0
    set processedParts {}

    set lViewIter2 [$lDesign NewViewsIter $lStatus $::IterDefs_SCHEMATICS]
    set lView2 [$lViewIter2 NextView $lStatus]

    while {$lView2 != $lNullObj} {
        set lSch2 [DboViewToDboSchematic $lView2]
        set lPagesIter2 [$lSch2 NewPagesIter $lStatus]
        set lPage2 [$lPagesIter2 NextPage $lStatus]

        while {$lPage2 != $lNullObj} {
            set lPII2 [$lPage2 NewPartInstsIter $lStatus]
            set lInst2 [$lPII2 NextPartInst $lStatus]

            while {$lInst2 != $lNullObj} {
                set lPI2 [DboPartInstToDboPlacedInst $lInst2]
                if {$lPI2 == $lNullObj} {
                    set lInst2 [$lPII2 NextPartInst $lStatus]
                    continue
                }

                set lRefCS2 [DboTclHelper_sMakeCString]
                $lPI2 GetReferenceDesignator $lRefCS2
                set refDes [DboTclHelper_sGetConstCharPtr $lRefCS2]

                set lPart2 [$lPI2 GetPart $lStatus]
                if {$lPart2 == $lNullObj} {
                    set lInst2 [$lPII2 NextPartInst $lStatus]
                    continue
                }

                set lPN2 [DboTclHelper_sMakeCString]
                $lPart2 GetName $lPN2
                set partName2 [DboTclHelper_sGetConstCharPtr $lPN2]

                if {[lsearch -exact $processedParts $partName2] >= 0} {
                    set lInst2 [$lPII2 NextPartInst $lStatus]
                    continue
                }
                lappend processedParts $partName2

                set seen [dict create]
                set lpIt [$lPart2 NewPinsIter $lStatus]
                set lP [$lpIt NextPin $lStatus]

                while {$lP != $lNullObj} {
                    set lN [DboTclHelper_sMakeCString]
                    $lP GetPinName $lN
                    set pn [DboTclHelper_sGetConstCharPtr $lN]

                    if {[dict exists $seen $pn]} {
                        set sc [dict get $seen $pn]
                        incr sc
                        dict set seen $pn $sc
                        set newName "${pn}_${sc}"
                        set lNewN [DboTclHelper_sMakeCString $newName]
                        if {[catch {$lP SetPinName $lNewN} err]} {
                            puts "  WARN: SetPinName fail: $refDes '$pn': $err"
                        } else {
                            puts "  FIX PinName: $refDes ($partName2) '$pn' -> '$newName'"
                            incr totalFixedName
                        }
                    } else {
                        dict set seen $pn 1
                    }

                    set lP [$lpIt NextPin $lStatus]
                }
                delete_DboSymbolPinsIter $lpIt

                set lInst2 [$lPII2 NextPartInst $lStatus]
            }
            delete_DboPagePartInstsIter $lPII2
            set lPage2 [$lPagesIter2 NextPage $lStatus]
        }
        delete_DboSchematicPagesIter $lPagesIter2
        set lView2 [$lViewIter2 NextView $lStatus]
    }
    delete_DboLibViewsIter $lViewIter2

    puts ""
    puts "========== FIX SUMMARY =========="
    puts "Pin Numbers fixed: $totalFixedNum"
    puts "Pin Names fixed: $totalFixedName"
    puts "================================="
    puts ""
    puts "Please save (Ctrl+S) and re-generate netlist to verify."
}

fix_pads_pins
