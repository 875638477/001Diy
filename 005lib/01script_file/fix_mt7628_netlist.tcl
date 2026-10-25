# fix_mt7628_netlist.tcl
# Fix PADS -> OrCAD Capture netlist blockers in the active design:
#   1. PCB Footprint names: replace characters Allegro rejects with "_"
#   2. Empty Pin Numbers: set Pin Number from Pin Name
#   3. Duplicate Pin Names: append _2, _3, ...
# Then save the design.
#
# Allegro footprint names may contain only A-Z, a-z, 0-9, "_" and "-".

proc _fp_sanitize {name} {
    set out ""
    foreach ch [split $name ""] {
        if {[regexp {^[A-Za-z0-9_-]$} $ch]} {
            append out $ch
        } else {
            append out "_"
        }
    }
    return $out
}

proc _log {fh msg} {
    puts $msg
    puts $fh $msg
    flush $fh
}

proc fix_mt7628_netlist {} {
    set logPath {D:/001DIY/016WIFI/MT7628/MT7628DAN/01SCH/fix_netlist_result.txt}
    set fh [open $logPath w]
    fconfigure $fh -buffering line
    _log $fh "=== fix_mt7628_netlist: starting ==="

    set lSession $::DboSession_s_pDboSession
    DboSession -this $lSession
    set lNullObj NULL
    set lStatus [DboState]
    set lDesign [$lSession GetActiveDesign]
    set designPath {D:/001DIY/016WIFI/MT7628/MT7628DAN/01SCH/MT7628DAN.DSN}

    if {$lDesign == $lNullObj} {
        _log $fh "No active design, opening $designPath"
        set lDesignPath [DboTclHelper_sMakeCString $designPath]
        set lDesign [DboSession_GetDesignAndSchematics $lSession $lDesignPath $lStatus]
    }

    if {$lDesign == $lNullObj} {
        _log $fh "ERROR: Cannot open design."
        _log $fh "DONE"
        close $fh
        return
    }

    set fpPkgFixed 0
    set fpInstFixed 0
    set pinNumFixed 0
    set pinNumFail 0
    set pinNameFixed 0

    # ----------------------------------------------------------------
    # 1. Package PCB Footprint
    # ----------------------------------------------------------------
    _log $fh "--- Package PCB Footprint ---"
    set seenPkgFp {}
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

        set lFpCS [DboTclHelper_sMakeCString]
        if {[catch {$lPackage GetPCBFootprint $lFpCS} err]} {
            _log $fh "  WARN GetPCBFootprint package '$pkgName': $err"
            set lNS [$lPkgNamesIter NextName $lPkgCS]
            continue
        }
        set oldFp [DboTclHelper_sGetConstCharPtr $lFpCS]
        if {$oldFp != "" && [regexp {[^A-Za-z0-9_-]} $oldFp]} {
            set newFp [_fp_sanitize $oldFp]
            set key "$pkgName|$oldFp"
            if {[lsearch -exact $seenPkgFp $key] < 0} {
                lappend seenPkgFp $key
                set lNewCS [DboTclHelper_sMakeCString $newFp]
                if {[catch {$lPackage SetPCBFootprint $lNewCS} err]} {
                    _log $fh "  FAIL package '$pkgName': '$oldFp' -> '$newFp': $err"
                } else {
                    _log $fh "  FIX package '$pkgName': '$oldFp' -> '$newFp'"
                    incr fpPkgFixed
                }
            }
        }
        set lNS [$lPkgNamesIter NextName $lPkgCS]
    }

    # ----------------------------------------------------------------
    # 2. Instance PCB Footprint + empty Pin Number + duplicate Pin Name
    # ----------------------------------------------------------------
    _log $fh "--- Instances ---"
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

                # Instance footprint, then the effective PCB Footprint property.
                set lPropName [DboTclHelper_sMakeCString "PCB Footprint"]
                foreach getter {inst prop} {
                    set oldFp ""
                    if {$getter eq "inst"} {
                        set lFpCS [DboTclHelper_sMakeCString]
                        if {[catch {$lPlacedInst GetPCBFootprint $lFpCS} err]} {
                            continue
                        }
                        set oldFp [DboTclHelper_sGetConstCharPtr $lFpCS]
                    } else {
                        set lPropVal [DboTclHelper_sMakeCString]
                        if {[catch {$lPlacedInst GetEffectivePropStringValue $lPropName $lPropVal} err]} {
                            continue
                        }
                        set oldFp [DboTclHelper_sGetConstCharPtr $lPropVal]
                    }
                    if {$oldFp == "" || ![regexp {[^A-Za-z0-9_-]} $oldFp]} {
                        continue
                    }
                    set newFp [_fp_sanitize $oldFp]
                    set lNewCS [DboTclHelper_sMakeCString $newFp]
                    set ok 0
                    if {[catch {$lPlacedInst SetPCBFootprint $lNewCS} err]} {
                        _log $fh "  WARN SetPCBFootprint $refDes '$oldFp': $err"
                    } else {
                        set ok 1
                    }
                    if {[catch {$lPlacedInst SetEffectivePropStringValue $lPropName $lNewCS} err]} {
                        if {!$ok} {
                            _log $fh "  FAIL footprint $refDes '$oldFp' -> '$newFp': $err"
                        }
                    } else {
                        set ok 1
                    }
                    if {$ok} {
                        catch {$lPlacedInst MarkModified}
                        _log $fh "  FIX footprint $refDes ($getter): '$oldFp' -> '$newFp'"
                        incr fpInstFixed
                    }
                }

                set lPart [$lPlacedInst GetPart $lStatus]
                if {$lPart == $lNullObj} {
                    set lInst [$lPartInstsIter NextPartInst $lStatus]
                    continue
                }
                set lPartNameCS [DboTclHelper_sMakeCString]
                $lPart GetName $lPartNameCS
                set partName [DboTclHelper_sGetConstCharPtr $lPartNameCS]

                if {[lsearch -exact $processedParts $partName] < 0} {
                    lappend processedParts $partName

                    # Empty pin numbers on the symbol, then on this instance's ports.
                    set lPinIter [$lPart NewPinsIter $lStatus]
                    set lPin [$lPinIter NextPin $lStatus]
                    set pinIdx 0
                    set seenNames [dict create]
                    while {$lPin != $lNullObj} {
                        set lNameCS [DboTclHelper_sMakeCString]
                        $lPin GetPinName $lNameCS
                        set pinName [DboTclHelper_sGetConstCharPtr $lNameCS]

                        set lNumCS [DboTclHelper_sMakeCString]
                        set pinNum ""
                        if {![catch {$lPin GetPinNumber $lNumCS} err]} {
                            set pinNum [DboTclHelper_sGetConstCharPtr $lNumCS]
                        }
                        if {$pinNum == ""} {
                            if {$pinName != ""} {
                                set want $pinName
                            } else {
                                set want [expr {$pinIdx + 1}]
                            }
                            set lWantCS [DboTclHelper_sMakeCString $want]
                            if {[catch {$lPin SetPinNumber $lWantCS} err]} {
                                _log $fh "  FAIL symbol pin number $refDes ($partName) '$pinName': $err"
                                incr pinNumFail
                            } else {
                                _log $fh "  FIX symbol pin number $refDes ($partName) '$pinName' -> '$want'"
                                incr pinNumFixed
                            }
                        }

                        # Duplicate pin names on the symbol.
                        if {$pinName != ""} {
                            if {[dict exists $seenNames $pinName]} {
                                set sc [dict get $seenNames $pinName]
                                incr sc
                                dict set seenNames $pinName $sc
                                set newName "${pinName}_${sc}"
                                set lNewName [DboTclHelper_sMakeCString $newName]
                                if {[catch {$lPin SetPinName $lNewName} err]} {
                                    _log $fh "  FAIL pin name $refDes ($partName) '$pinName': $err"
                                } else {
                                    _log $fh "  FIX pin name $refDes ($partName) '$pinName' -> '$newName'"
                                    incr pinNameFixed
                                }
                            } else {
                                dict set seenNames $pinName 1
                            }
                        }

                        incr pinIdx
                        set lPin [$lPinIter NextPin $lStatus]
                    }
                    delete_DboSymbolPinsIter $lPinIter
                }

                # Instance ports: cover flat parts whose symbol pin has no SetPinNumber.
                set count [$lInst GetPinCount $lStatus]
                for {set i 0} {$i < $count} {incr i} {
                    set portInst [$lInst GetPin $i $lStatus]
                    if {$portInst == $lNullObj} {
                        continue
                    }
                    set lNumCS [DboTclHelper_sMakeCString]
                    $portInst GetPinNumber $lNumCS
                    set pinNum [DboTclHelper_sGetConstCharPtr $lNumCS]
                    if {$pinNum != ""} {
                        continue
                    }
                    set lNameCS [DboTclHelper_sMakeCString]
                    $portInst GetPinName $lNameCS
                    set pinName [DboTclHelper_sGetConstCharPtr $lNameCS]
                    if {$pinName != ""} {
                        set want $pinName
                    } else {
                        set want [expr {$i + 1}]
                    }
                    set lWantCS [DboTclHelper_sMakeCString $want]
                    if {[catch {$portInst SetPinNumber $lWantCS} err]} {
                        _log $fh "  FAIL port pin number $refDes pin '$pinName': $err"
                        incr pinNumFail
                    } else {
                        _log $fh "  FIX port pin number $refDes '$pinName' -> '$want'"
                        catch {$lPlacedInst MarkModified}
                        incr pinNumFixed
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

    # ----------------------------------------------------------------
    # 3. Device.NewPinNumber for parts that still have a real package
    # ----------------------------------------------------------------
    _log $fh "--- Device pin numbers for parts still empty ---"
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
                if {$lPlacedInst != $lNullObj} {
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
                                    break
                                }
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

    set devFixed 0
    if {[dict size $partsNeedFix] > 0} {
        set lPkgNamesIter [$lDesign NewPackageNamesIter $lStatus]
        set lPkgCS [DboTclHelper_sMakeCString]
        set lNS [$lPkgNamesIter NextName $lPkgCS]
        while {[$lNS OK] == 1} {
            if {[catch {set lPackage [$lDesign GetPackage $lPkgCS $lStatus]} err]} {
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
                if {[catch {set lCell [$lDevice GetCell $lStatus]} err]} { incr devIdx; continue }
                if {$lCell == $lNullObj} { incr devIdx; continue }
                if {[catch {set lNormalPart [$lCell FindPart $devIdx $lStatus]} err]} { incr devIdx; continue }
                if {$lNormalPart == $lNullObj} {
                    if {[catch {set lNormalPart [$lCell FindPart 0 $lStatus]} err]} { incr devIdx; continue }
                    if {$lNormalPart == $lNullObj} { incr devIdx; continue }
                }
                set lCellPartNameCS [DboTclHelper_sMakeCString]
                $lNormalPart GetName $lCellPartNameCS
                set cellPartName [DboTclHelper_sGetConstCharPtr $lCellPartNameCS]
                if {[dict exists $partsNeedFix $cellPartName]} {
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
                                _log $fh "  FAIL device pin '$cellPartName' '$pinName': $err"
                            } else {
                                _log $fh "  FIX device pin '$cellPartName' '$pinName'"
                                incr devFixed
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
        dict for {nm dummy} $partsNeedFix {
            _log $fh "  STILL EMPTY (no package device): '$nm'"
        }
    } else {
        _log $fh "  No remaining empty pin numbers on instances."
    }

    _log $fh "--- Save ---"
    set saved 0
    if {[catch {
        $lSession MarkAllLibForSave $lDesign
        $lSession SaveDesign $lDesign
    } err]} {
        _log $fh "SAVE FAIL: $err"
    } else {
        set saved 1
        _log $fh "SAVE OK"
    }

    _log $fh "========== SUMMARY =========="
    _log $fh "Package footprints fixed: $fpPkgFixed"
    _log $fh "Instance footprints fixed: $fpInstFixed"
    _log $fh "Pin numbers fixed: $pinNumFixed"
    _log $fh "Pin number failures: $pinNumFail"
    _log $fh "Device pin numbers fixed: $devFixed"
    _log $fh "Duplicate pin names fixed: $pinNameFixed"
    _log $fh "Saved: $saved"
    _log $fh "DONE"
    close $fh
}

fix_mt7628_netlist
