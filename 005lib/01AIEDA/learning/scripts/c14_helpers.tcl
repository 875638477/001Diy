# Lesson 14 research helpers. Definitions only: sourcing performs no CAD edit.
# Native operations must be run by the root agent inside Capture 17.2.
# All output and all mutable designs/libraries must stay under 01AIEDA/learning.
# API references: OrCAD_Capture_TclTk_Extensions.pdf pp.35,198-206,542-545,
# 602-605,724-726 and installed capDB/capExportDesignCache.tcl.

namespace eval ::C14Research {
    variable version 20261019.1
    variable learningRoot {D:/001DIY/005lib/01AIEDA/learning}
}

proc ::C14Research::allowedPath {path} {
    variable learningRoot
    set actual [string tolower [string map {\\ /} [file normalize $path]]]
    set root [string tolower [string map {\\ /} [file normalize $learningRoot]]]
    if {![string match "${root}/*" $actual]} {
        error "C14 path is outside the learning root: $path"
    }
    return [file normalize $path]
}

proc ::C14Research::cstring {value} {
    return [DboTclHelper_sMakeCString $value]
}

proc ::C14Research::readString {object method args} {
    set buffer [DboTclHelper_sMakeCString]
    set code [catch {eval [linsert $args 0 $object $method] [list $buffer]} state]
    if {$code} {
        set value "ERROR:$state"
    } else {
        set value [DboTclHelper_sGetConstCharPtr $buffer]
        if {![catch {$state Failed} failed] && $failed} {
            set value "ERROR:DbStateFailed:$method"
        }
    }
    catch {DboTclHelper_sDeleteCString $buffer}
    return $value
}

proc ::C14Research::readScalar {object method} {
    set status [DboState]
    if {[catch {$object $method $status} result]} {set result "ERROR:$result"}
    catch {$status -delete}
    return $result
}

proc ::C14Research::readPoint {object method} {
    set status [DboState]
    if {[catch {
        set point [$object $method $status]
        set result [list [DboTclHelper_sGetCPointX $point] [DboTclHelper_sGetCPointY $point]]
    } problem]} {set result [list "ERROR:$problem" ""]}
    catch {$status -delete}
    return $result
}

proc ::C14Research::readBoundingBox {object} {
    if {[catch {
        set rect [$object GetBoundingBox]
        set tl [DboTclHelper_sGetCRectTopLeft $rect]
        set br [DboTclHelper_sGetCRectBottomRight $rect]
        set result [list [DboTclHelper_sGetCPointX $tl] [DboTclHelper_sGetCPointY $tl] [DboTclHelper_sGetCPointX $br] [DboTclHelper_sGetCPointY $br]]
    } problem]} {set result "ERROR:$problem"}
    return $result
}

proc ::C14Research::property {object name} {
    set key [cstring $name]
    set value [readString $object GetEffectivePropStringValue $key]
    catch {DboTclHelper_sDeleteCString $key}
    return $value
}

proc ::C14Research::objectProperties {object} {
    set result [dict create]
    foreach name {Value MPN LIB_REV C14_INST_OVERRIDE C14_LIB_ONLY C14_PIN_OVERRIDE} {
        dict set result $name [property $object $name]
    }
    return $result
}

proc ::C14Research::writeTclReport {path value} {
    set path [allowedPath $path]
    if {[file exists $path]} {error "C14 refuses to overwrite report: $path"}
    file mkdir [file dirname $path]
    set stream [open $path w]
    fconfigure $stream -encoding utf-8 -translation lf
    puts $stream [list C14_TCL_REPORT_1 $value]
    close $stream
    return $path
}

proc ::C14Research::probeSignatures {} {
    set result [dict create]
    foreach command {DboLib_UpdateCache DboLib_ReplaceCache DboLib_GetCachedPackage DboDesign_NewCachesIter DboDevice_GetPinNumber DboPlacedInst_GetPCBFootprint XMATIC_ExportDesignInXML} {
        if {[llength [info commands $command]]} {
            catch {eval [list $command]} message
            dict set result $command $message
        } else {dict set result $command MISSING}
    }
    return $result
}

proc ::C14Research::snapshotPackage {package outputPath} {
    set status [DboState]
    set result [dict create kind package name [readString $package GetName] footprint [readString $package GetPCBFootprint] properties [objectProperties $package] devices [list]]
    set devices [$package NewDevicesIter $status]
    set device [$devices NextDevice $status]
    while {$device != "NULL"} {
        set deviceResult [dict create designator [readString $device GetDesignator] parts [list]]
        set cell [$device GetCell $status]
        set parts [$cell NewPartsIter $status]
        set part [$parts NextPart $status]
        while {$part != "NULL"} {
            set partResult [dict create name [readString $part GetName] value [readString $part GetPartValue] bbox [readBoundingBox $part] properties [objectProperties $part] pins [list] vectors [list]]
            set vectors [$part NewVectorsIter $status $::IterDefs_ALL]
            set vector [$vectors NextVector $status]
            while {$vector ne "NULL"} {
                set vt [$vector GetObjectType]
                if {$vt==$::DboBaseObject_LINE} {
                    set line [DboVectorToDboLine $vector]
                    dict lappend partResult vectors [dict create type LINE start [readPoint $line GetStart] end [readPoint $line GetEnd]]
                } else {dict lappend partResult vectors [dict create type $vt]}
                set vector [$vectors NextVector $status]
            }
            delete_DboGraphicObjectVectorsIter $vectors
            set pins [$part NewLPinsIter $status]
            set pin [$pins NextPin $status]
            while {$pin != "NULL"} {
                set position [readScalar $pin GetPinPosition]
                set pinResult [dict create position $position number [readString $device GetPinNumber $position] name [readString $pin GetPinName] type [readScalar $pin GetPinType] visible [readScalar $pin GetIsVisible] numberVisible [readScalar $pin GetIsNumberVisible] noConnect [readScalar $pin GetIsNoConnect] start [readPoint $pin GetStartPoint] hotSpot [readPoint $pin GetHotSpot] properties [objectProperties $pin]]
                dict lappend partResult pins $pinResult
                set pin [$pins NextPin $status]
            }
            catch {delete_DboLibPartPinsIter $pins}
            dict lappend deviceResult parts $partResult
            set part [$parts NextPart $status]
        }
        catch {delete_DboCellPartsIter $parts}
        dict lappend result devices $deviceResult
        set device [$devices NextDevice $status]
    }
    catch {delete_DboPackageDevicesIter $devices}
    catch {$status -delete}
    writeTclReport $outputPath $result
    return $result
}

proc ::C14Research::snapshotPlacedInstance {instance outputPath} {
    set status [DboState]
    set package [$instance GetPackage $status]
    set result [dict create kind instance reference [readString $instance GetReference] refdes [readString $instance GetReferenceDesignator] sourceLibrary [readString $instance GetSourceLibName] sourcePart [readString $instance GetSourcePartName] location [readPoint $instance GetLocation] package [readString $package GetName] footprint [readString $instance GetPCBFootprint] cachedFootprint [readString $package GetPCBFootprint] bbox [readBoundingBox $instance] properties [objectProperties $instance] pins [list]]
    set pins [$instance NewPinsIter $status]
    set pin [$pins NextPin $status]
    while {$pin != "NULL"} {
        set net [$pin GetNet $status]
        set netName ""
        if {$net != "NULL"} {set netName [readString $net GetName]}
        set pinResult [dict create number [readString $pin GetPinNumber] name [readString $pin GetPinName] type [readScalar $pin GetPinType] visible [readScalar $pin GetIsVisible] numberVisible [readScalar $pin GetIsNumberVisible] noConnect [readScalar $pin GetIsNoConnect] hotSpot [readPoint $pin GetHotSpot] net $netName properties [objectProperties $pin]]
        dict lappend result pins $pinResult
        set pin [$pins NextPin $status]
    }
    catch {delete_DboPartInstPinsIter $pins}
    catch {$status -delete}
    writeTclReport $outputPath $result
    return $result
}

proc ::C14Research::snapshotCache {design outputPath} {
    set status [DboState]
    set result [dict create kind cache design [readString $design GetName] objects [list]]
    set iterator [$design NewCachesIter $status]
    set object [$iterator NextCachedObject $status]
    while {$object != "NULL"} {
        set libObject [DboBaseObjectToDboLibObject $object]
        set nameBuffer [DboTclHelper_sMakeCString]
        set sourceBuffer [DboTclHelper_sMakeCString]
        $object GetName $nameBuffer
        set sourceState [$design GetSourceLibName $nameBuffer $libObject $sourceBuffer]
        dict lappend result objects [dict create name [DboTclHelper_sGetConstCharPtr $nameBuffer] type [$object GetObjectType] sourceLibrary [DboTclHelper_sGetConstCharPtr $sourceBuffer]]
        catch {DboTclHelper_sDeleteCString $nameBuffer}
        catch {DboTclHelper_sDeleteCString $sourceBuffer}
        set object [$iterator NextCachedObject $status]
    }
    catch {delete_DboDesignCachesIter $iterator}
    catch {$status -delete}
    writeTclReport $outputPath $result
    return $result
}

proc ::C14Research::assertPracticeDesign {design} {
    set name [readString $design GetName]
    allowedPath $name
    if {![string equal -nocase [file extension $name] .dsn]} {
        error "C14 expected an isolated DSN design; received $name"
    }
    return $name
}

proc ::C14Research::updateCache {design sourceLibrary packageName objectType} {
    assertPracticeDesign $design
    allowedPath $sourceLibrary
    return [$design UpdateCache [cstring $sourceLibrary] [cstring $packageName] $objectType 1]
}

proc ::C14Research::replaceCache {design oldPackage oldLibrary newPackage newLibrary updateCacheFlag preserveRefdesFlag} {
    assertPracticeDesign $design
    allowedPath $oldLibrary
    allowedPath $newLibrary
    if {$preserveRefdesFlag != 1} {error "C14 replacement requires explicit preserveRefdesFlag=1"}
    if {$updateCacheFlag != 0 && $updateCacheFlag != 1} {error "C14 requires an explicit native updateCacheFlag 0 or 1"}
    # Exact native flag mapping to UI property modes must be verified in Capture.
    return [$design ReplaceCache [cstring $oldPackage] [cstring $oldLibrary] [cstring $newPackage] [cstring $newLibrary] $updateCacheFlag $preserveRefdesFlag]
}

set ::C14Research::definitionStatus {DEFINED_ONLY_NOT_NATIVE_EXECUTED}
