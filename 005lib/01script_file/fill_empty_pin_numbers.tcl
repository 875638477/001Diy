# fill_empty_pin_numbers.tcl
# If Pin Number is empty, copy Pin Name into Pin Number.
# Name "1" becomes number "1". Existing numbers are left unchanged.
#
# Capture command window:
#   source {D:\001DIY\005lib\01script_file\fill_empty_pin_numbers.tcl}
#
# Open the design first. After the script, Ctrl+S and recreate the netlist.

proc _pinnum_base {name} {
    set dot [string last "." $name]
    if {$dot > 0} {
        set tail [string range $name [expr {$dot + 1}] end]
        if {$tail eq "Normal" || $tail eq "Convert"} {
            return [string range $name 0 [expr {$dot - 1}]]
        }
    }
    return $name
}

proc _pinnum_index_devices {lDesign lStatus lNullObj} {
    set devMap [dict create]
    set lPkgNamesIter [$lDesign NewPackageNamesIter $lStatus]
    set lPkgCS [DboTclHelper_sMakeCString]
    set lNS [$lPkgNamesIter NextName $lPkgCS]

    while {[$lNS OK] == 1} {
        set pkgName [DboTclHelper_sGetConstCharPtr $lPkgCS]
        if {[catch {set lPackage [$lDesign GetPackage $lPkgCS $lStatus]}]} {
            set lNS [$lPkgNamesIter NextName $lPkgCS]
            continue
        }
        if {$lPackage == $lNullObj} {
            set lNS [$lPkgNamesIter NextName $lPkgCS]
            continue
        }

        set devIdx 0
        while {1} {
            if {[catch {set lDevice [$lPackage GetDevice $devIdx $lStatus]}]} { break }
            if {$lDevice == $lNullObj} { break }

            if {[catch {set lCell [$lDevice GetCell $lStatus]}]} {
                incr devIdx
                continue
            }
            if {$lCell == $lNullObj} {
                incr devIdx
                continue
            }

            if {[catch {set lNormalPart [$lCell FindPart $devIdx $lStatus]}]} {
                set lNormalPart $lNullObj
            }
            if {$lNormalPart == $lNullObj} {
                if {[catch {set lNormalPart [$lCell FindPart 0 $lStatus]}]} {
                    set lNormalPart $lNullObj
                }
            }
            if {$lNormalPart == $lNullObj} {
                incr devIdx
                continue
            }

            set lNameCS [DboTclHelper_sMakeCString]
            $lNormalPart GetName $lNameCS
            set cellName [DboTclHelper_sGetConstCharPtr $lNameCS]
            set baseName [_pinnum_base $cellName]
            set entry [list $lDevice $lNormalPart $pkgName]
            dict set devMap $cellName $entry
            dict set devMap $baseName $entry

            incr devIdx
        }

        set lNS [$lPkgNamesIter NextName $lPkgCS]
    }
    return $devMap
}

proc fill_empty_pin_numbers {} {
    puts "=== fill_empty_pin_numbers: start ==="

    set lSession $::DboSession_s_pDboSession
    DboSession -this $lSession
    set lNullObj NULL
    set lStatus [DboState]
    set lDesign [$lSession GetActiveDesign]

    if {$lDesign == $lNullObj} {
        puts "ERROR: no active design. Open the dsn first."
        return
    }

    puts "--- index Package/Device ---"
    set devMap [_pinnum_index_devices $lDesign $lStatus $lNullObj]
    puts "  device entries: [dict size $devMap]"

    set totalFilled 0
    set totalFailed 0
    set processedParts {}
    set failedParts {}

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

            set lPartInstsIter [$lPage NewPartInstsIter $lStatus]
            set lInst [$lPartInstsIter NextPartInst $lStatus]

            while {$lInst != $lNullObj} {
                set lPlacedInst [DboPartInstToDboPlacedInst $lInst]
                if {$lPlacedInst == $lNullObj} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set lPart [$lPlacedInst GetPart $lStatus]
                if {$lPart == $lNullObj} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set lPartNameCS [DboTclHelper_sMakeCString]
                $lPart GetName $lPartNameCS
                set partName [DboTclHelper_sGetConstCharPtr $lPartNameCS]
                set baseName [_pinnum_base $partName]

                if {[lsearch -exact $processedParts $baseName] >= 0} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }
                lappend processedParts $baseName

                set lRefCS [DboTclHelper_sMakeCString]
                $lPlacedInst GetReferenceDesignator $lRefCS
                set refDes [DboTclHelper_sGetConstCharPtr $lRefCS]

                set count [$lInst GetPinCount $lStatus]
                set emptyIdx [dict create]
                set usedNums [dict create]
                for {set i 0} {$i < $count} {incr i} {
                    set portInst [$lInst GetPin $i $lStatus]
                    set pNumber [DboTclHelper_sMakeCString]
                    $portInst GetPinNumber $pNumber
                    set pinNum [DboTclHelper_sGetConstCharPtr $pNumber]
                    if {$pinNum == ""} {
                        dict set emptyIdx $i 1
                    } else {
                        dict set usedNums $pinNum 1
                    }
                }
                if {[dict size $emptyIdx] == 0} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set lDevice $lNullObj
                set lSrcPart $lNullObj
                set pkgName ""
                if {[dict exists $devMap $partName]} {
                    set entry [dict get $devMap $partName]
                    set lDevice [lindex $entry 0]
                    set lSrcPart [lindex $entry 1]
                    set pkgName [lindex $entry 2]
                } elseif {[dict exists $devMap $baseName]} {
                    set entry [dict get $devMap $baseName]
                    set lDevice [lindex $entry 0]
                    set lSrcPart [lindex $entry 1]
                    set pkgName [lindex $entry 2]
                }

                if {$lDevice == $lNullObj || $lSrcPart == $lNullObj} {
                    puts "FAIL: $refDes ($baseName) \[$pageName\] no Package/Device"
                    incr totalFailed [dict size $emptyIdx]
                    lappend failedParts "$baseName (e.g. $refDes)"
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }

                set idx 0
                set partFilled 0
                set partFail 0
                set lPinIter [$lSrcPart NewLPinsIter $lStatus]
                set lPin [$lPinIter NextPin $lStatus]
                while {$lPin != $lNullObj} {
                    if {[dict exists $emptyIdx $idx]} {
                        set lPinNameCS [DboTclHelper_sMakeCString]
                        $lPin GetPinName $lPinNameCS
                        set pinName [string trim [DboTclHelper_sGetConstCharPtr $lPinNameCS]]

                        if {$pinName == ""} {
                            puts "FAIL: $refDes ($baseName) pin $idx empty name"
                            incr totalFailed
                            incr partFail
                        } elseif {[dict exists $usedNums $pinName]} {
                            puts "SKIP: $refDes ($baseName) number '$pinName' already used"
                            incr totalFailed
                            incr partFail
                        } else {
                            set lNew [DboTclHelper_sMakeCString $pinName]
                            set lPinPos [$lPin GetPinPosition $lStatus]
                            set lPinPosInt [DboTclHelper_sMakeInt $lPinPos]
                            set err ""
                            set ok 0
                            if {![catch {$lDevice NewPinNumber $lNew $lPinPosInt 0 -1} err]} {
                                set ok 1
                            } elseif {![catch {$lDevice NewPinNumber $lNew $lPinPosInt 1 -1} err]} {
                                set ok 1
                            }
                            if {$ok} {
                                puts "FIX: $refDes ($baseName) \[$pageName\] '$pinName' -> '$pinName' pkg=$pkgName"
                                dict set usedNums $pinName 1
                                incr totalFilled
                                incr partFilled
                            } else {
                                puts "FAIL: $refDes ($baseName) '$pinName' : $err"
                                incr totalFailed
                                incr partFail
                            }
                        }
                    }
                    incr idx
                    set lPin [$lPinIter NextPin $lStatus]
                }

                if {$partFail > 0 && $partFilled == 0} {
                    lappend failedParts "$baseName (e.g. $refDes)"
                } elseif {$partFilled > 0} {
                    puts "DONE: $baseName filled $partFilled"
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
    puts "========== RESULT =========="
    puts "filled: $totalFilled"
    puts "failed: $totalFailed"
    puts "parts checked: [llength $processedParts]"
    if {[llength $failedParts] > 0} {
        puts "still empty, edit these in Design Cache:"
        foreach item $failedParts {
            puts "  - $item"
        }
    }
    puts "============================"
    puts "Ctrl+S, then create the Allegro netlist again."
}

fill_empty_pin_numbers
