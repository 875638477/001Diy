# Capture 17.2 internal Tcl helpers for lesson 12.
# Source defines procedures only. It does not create or open a library.
# Official creation model: PwlORSymbolCreate.tcl in the installed PWL/OR example.
# Only the root agent owns the Capture process and invokes these procedures.
namespace eval ::C12 {
    variable learningRoot {D:/001DIY/005lib/01AIEDA/learning}
    variable footprint {qmi8610_lga16_3d3_p0d5}
}

proc ::C12::safe_path {path} {
    variable learningRoot
    set full [string map {\\ /} [file normalize $path]]
    set base [string tolower [string map {\\ /} [file normalize $learningRoot]]]
    if {![string match "${base}/*" [string tolower $full]]} {
        error "C12 output must stay inside learning: $full"
    }
    return $full
}

proc ::C12::cstring {value} {return [DboTclHelper_sMakeCString $value]}
proc ::C12::check {state context} {
    if {[$state Failed]} {error "DboState failed: $context"}
    return $state
}
proc ::C12::nonnull {object state context} {
    ::C12::check $state $context
    if {$object eq "NULL" || $object eq ""} {error "NULL Dbo object: $context"}
    return $object
}
proc ::C12::session {} {
    if {![info exists ::DboSession_s_pDboSession]} {error "Run inside Capture, not plain tclsh"}
    set session $::DboSession_s_pDboSession
    DboSession -this $session
    return $session
}

# Resolve installed enums, checking the expected 17.2 numeric encoding.
# The enum names occur in the installed orPrmDboStreamer.tcl example.
proc ::C12::type_code {kind} {
    switch -- $kind {
        INPUT {set names {::DBO_IN ::DboValue_INPUT}; set expected 0}
        BIDIRECTIONAL {set names {::IO ::DboValue_BIDIRECTIONAL}; set expected 1}
        OUTPUT {set names {::DBO_OUT ::DboValue_OUTPUT}; set expected 2}
        PASSIVE {set names {::PAS ::DboValue_PASSIVE}; set expected 4}
        POWER {set names {::POWER ::DboValue_POWER}; set expected 7}
        default {error "Unknown C12 pin kind: $kind"}
    }
    foreach name $names {
        if {[info exists $name]} {
            set actual [set $name]
            if {$actual != $expected} {error "Unexpected enum $name=$actual, expected $expected"}
            return $actual
        }
    }
    error "Installed pin enum missing for $kind; probe enums before creation"
}

# number, visible name, electrical type, no-connect flag, source PDF page.
# HOST_I2C is the default; the mode is also saved as a part property.
# RESERVED pin1 must be grounded. Only pin4 and pin5 are NC.
proc ::C12::spec_rows {{mode HOST_I2C}} {
    if {$mode ni {HOST_I2C HOST_SPI4}} {error "Supported interface profiles: HOST_I2C HOST_SPI4"}
    set pin9type INPUT
    set pin13type BIDIRECTIONAL
    if {$mode eq "HOST_SPI4"} {set pin9type OUTPUT; set pin13type INPUT}
    return [list \
        [list 1 RESV3 PASSIVE 0 8] \
        [list 2 VDDa POWER 0 8] \
        [list 3 GNDa POWER 0 8] \
        [list 4 RESV2 PASSIVE 1 8] \
        [list 5 RESV1 PASSIVE 1 8] \
        [list 6 SDA2 BIDIRECTIONAL 0 8] \
        [list 7 SCL2 OUTPUT 0 8] \
        [list 8 VDDd POWER 0 8] \
        [list 9 SA0/SDO $pin9type 0 8] \
        [list 10 CS INPUT 0 9] \
        [list 11 INT2/DRDY OUTPUT 0 9] \
        [list 12 INT1/CLKout OUTPUT 0 9] \
        [list 13 SDA/SDI/SDIO $pin13type 0 9] \
        [list 14 SCL/SPC INPUT 0 9] \
        [list 15 GNDd POWER 0 9] \
        [list 16 RST INPUT 0 9]]
}

proc ::C12::pin_points {number} {
    # Schematic drawing coordinates, not mechanical package coordinates.
    if {$number <= 8} {
        set y [expr {20*$number}]
        return [list 0 $y -20 $y]
    }
    set y [expr {20*($number-8)}]
    return [list 220 $y 240 $y]
}

proc ::C12::string_value {object method args} {
    set buffer [::C12::cstring ""]
    ::C12::check [$object $method {*}$args $buffer] "$method"
    return [DboTclHelper_sGetConstCharPtr $buffer]
}

proc ::C12::point_list {point} {
    return [list [DboTclHelper_sGetCPointX $point] [DboTclHelper_sGetCPointY $point]]
}

proc ::C12::user_prop {object key value} {
    set state [DboState]
    set property [$object NewUserProp [::C12::cstring $key] [::C12::cstring $value] $state]
    ::C12::nonnull $property $state "NewUserProp $key"
    return $property
}

proc ::C12::display_prop {part key x y} {
    set state [DboState]
    set font [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16]
    set prop [$part NewDisplayProp $state [::C12::cstring $key] [DboTclHelper_sMakeCPoint $x $y] 0 $font 48]
    ::C12::nonnull $prop $state "NewDisplayProp $key"
    ::C12::check [$prop SetDisplayType 1] "SetDisplayType $key"
    # Installed example calls this setter without treating its result as DboState.
    $prop SetHorizontalTextJustification 0
    return $prop
}

proc ::C12::CreateQmi8610 {libraryPath {partName QMI8610_C12} {mode HOST_I2C}} {
    variable footprint
    set libraryPath [::C12::safe_path $libraryPath]
    if {[file exists $libraryPath]} {error "Refusing to overwrite existing C12 library: $libraryPath"}
    file mkdir [file dirname $libraryPath]
    set session [::C12::session]
    set state [DboState]
    set openLib [$session GetOpenLib [::C12::cstring $libraryPath] $state]
    if {$openLib ne "NULL"} {error "Target library already open: $libraryPath"}
    set rows [::C12::spec_rows $mode]
    foreach row $rows {::C12::type_code [lindex $row 2]}
    set lib [$session CreateLib [::C12::cstring $libraryPath] $state]
    ::C12::nonnull $lib $state CreateLib
    set package [$lib NewPackage [::C12::cstring $partName] $state]
    ::C12::nonnull $package $state NewPackage
    ::C12::check [$package SetReferenceTemplate [::C12::cstring U]] SetReferenceTemplate
    ::C12::check [$package SetPCBFootprint [::C12::cstring $footprint]] SetPCBFootprint
    set cell [$lib NewCell [::C12::cstring $partName] $state]
    ::C12::nonnull $cell $state NewCell
    set part [$lib NewPart [::C12::cstring "$partName.Normal"] $state]
    ::C12::nonnull $part $state NewPart
    ::C12::check [$cell AddPart $part] AddPart
    $part SetCellPtr $cell
    $part SetPackagePtr $package
    ::C12::check [$part SetBoundingBox [DboTclHelper_sMakeCRect 0 0 220 180]] SetBoundingBox
    ::C12::check [$part SetPartValue [::C12::cstring QMI8610]] SetPartValue
    ::C12::check [$part SetReference [::C12::cstring U]] SetReference
    ::C12::check [$part SetPinNamesAreVisible 1] SetPinNamesAreVisible
    ::C12::check [$part SetPinNumbersAreVisible 1] SetPinNumbersAreVisible
    ::C12::check [$part SetPinNamesAreRotated 0] SetPinNamesAreRotated
    foreach segment {{0 0 220 0} {220 0 220 180} {220 180 0 180} {0 180 0 0}} {
        lassign $segment x1 y1 x2 y2
        set line [$part NewLine $state [DboTclHelper_sMakeCPoint $x1 $y1] [DboTclHelper_sMakeCPoint $x2 $y2] 0 0]
        ::C12::nonnull $line $state NewLine
    }
    foreach {key value} [list \
        Manufacturer QST \
        {Manufacturer Part Number} QMI8610 \
        {PCB Footprint} $footprint \
        {Interface Profile} $mode \
        {Symbol Revision} C12_REV1 \
        {Source Revision} {13-52-14 Rev A, 2018-05-10} \
        {Datasheet} {QMI8610 Datasheet Rev. A.pdf} \
        {Reserved Pin Policy} {Pin1 RESV3 connect GND; pin4/5 NC; no center/EP17}] {
        ::C12::user_prop $part $key $value
    }
    ::C12::display_prop $part {Part Reference} 0 -20
    ::C12::display_prop $part Value 100 200
    foreach row $rows {
        lassign $row number name kind noConnect page
        set position [expr {$number-1}]
        lassign [::C12::pin_points $number] sx sy hx hy
        set pin [$part NewSymbolPinScalar $state [::C12::cstring $name] [::C12::type_code $kind] \
            [DboTclHelper_sMakeCPoint $sx $sy] [DboTclHelper_sMakeCPoint $hx $hy] 1 $position]
        ::C12::nonnull $pin $state "NewSymbolPinScalar $number"
        # The first native 17.2 saved/reopened run reports POWER IsGlobal=1
        # while visible=1. This metadata bit is not a wired-net scope test.
        set rawGlobal [expr {$kind eq "POWER"}]
        foreach {method value} [list SetIsLong 1 SetIsClock 0 SetIsDot 0 SetIsLeftPointing 0 \
            SetIsRightPointing 0 SetIsNetStyle 0 SetIsNoConnect $noConnect SetIsGlobal $rawGlobal \
            SetIsVisible 1 SetIsNumberVisible 1] {
            ::C12::check [$pin $method $value] "$method pin $number"
        }
    }
    set device [$package NewDevice [::C12::cstring 1] 0 $cell $state]
    ::C12::nonnull $device $state NewDevice
    foreach row $rows {
        set number [lindex $row 0]
        set positionPtr [DboTclHelper_sMakeInt [expr {$number-1}]]
        ::C12::check [$device NewPinNumber [::C12::cstring $number] $positionPtr 0 -1] "NewPinNumber $number"
    }
    ::C12::check [$lib SavePackageAll $package] SavePackageAll
    ::C12::check [$session SaveLib $lib] SaveLib
    ::C12::check [$session RemoveLib $lib] RemoveLib
    # Returned pointers would be stale after RemoveLib. Return names/paths only.
    return [dict create path $libraryPath package $partName part "$partName.Normal" device 1 mode $mode]
}

proc ::C12::ReadQmi8610 {libraryPath partName reportDirectory {mode HOST_I2C} {closeAfter 1}} {
    set libraryPath [::C12::safe_path $libraryPath]
    set reportDirectory [::C12::safe_path $reportDirectory]
    file mkdir $reportDirectory
    set session [::C12::session]
    set state [DboState]
    set lib [$session GetLib [::C12::cstring $libraryPath] $state]
    ::C12::nonnull $lib $state GetLib
    set package [$lib GetPackage [::C12::cstring $partName] $state]
    ::C12::nonnull $package $state GetPackage
    set device [$package GetDevice 0 $state]
    ::C12::nonnull $device $state GetDevice
    set cell [$device GetCell $state]
    ::C12::nonnull $cell $state GetCell
    set part [$cell FindPart 0 $state]
    ::C12::nonnull $part $state FindPart
    set rows [::C12::spec_rows $mode]
    set report [open [file join $reportDirectory c12_pins.tsv] w]
    fconfigure $report -encoding utf-8 -translation lf
    puts $report "number\tposition\tname\ttype\tvisible\tnumberVisible\tglobal\tnoConnect\tstartX\tstartY\thotX\thotY"
    set errors {}
    set seen {}
    set iter [$part NewLPinsIter $state]
    set pin [$iter NextPin $state]
    while {$pin ne "NULL"} {
        set position [$pin GetPinPosition $state]
        set number [::C12::string_value $device GetPinNumber $position]
        set name [::C12::string_value $pin GetPinName]
        set type [$pin GetPinType $state]
        set visible [$pin GetIsVisible $state]
        set numberVisible [$pin GetIsNumberVisible $state]
        set global [$pin GetIsGlobal $state]
        set noConnect [$pin GetIsNoConnect $state]
        set start [::C12::point_list [$pin GetStartPoint $state]]
        set hot [::C12::point_list [$pin GetHotSpot $state]]
        puts $report [join [concat [list $number $position $name $type $visible $numberVisible $global $noConnect] $start $hot] "\t"]
        if {![string is integer -strict $number] || $number<1 || $number>16} {
            lappend errors "Unexpected physical pin $number"
        } else {
            set expected [lindex $rows [expr {$number-1}]]
            if {$number in $seen} {lappend errors "Duplicate physical pin $number"}
            lappend seen $number
            if {$position != $number-1} {lappend errors "Pin $number position $position"}
            if {$name ne [lindex $expected 1]} {lappend errors "Pin $number name $name"}
            if {$type != [::C12::type_code [lindex $expected 2]]} {lappend errors "Pin $number type $type"}
            if {$visible!=1 || $numberVisible!=1} {lappend errors "Pin $number visibility flags"}
            set expectedRawGlobal [expr {[lindex $expected 2] eq "POWER"}]
            if {$global!=$expectedRawGlobal} {lappend errors "Pin $number raw global=$global, expected $expectedRawGlobal"}
            if {$noConnect != [lindex $expected 3]} {lappend errors "Pin $number noConnect $noConnect"}
            if {[concat $start $hot] ne [::C12::pin_points $number]} {lappend errors "Pin $number start/hot geometry"}
        }
        set pin [$iter NextPin $state]
    }
    close $report
    delete_DboLibPartPinsIter $iter
    if {[llength $seen]!=16 || [lsort -integer -unique $seen] ne {1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16}} {
        lappend errors "Expected exactly physical pins 1..16, no EP17"
    }
    set namesVisible [$part GetPinNamesAreVisible $state]
    set numbersVisible [$part GetPinNumbersAreVisible $state]
    if {$namesVisible!=1 || $numbersVisible!=1} {lappend errors "Part-wide pin visibility differs"}
    set propertyReport [open [file join $reportDirectory c12_properties.tsv] w]
    fconfigure $propertyReport -encoding utf-8 -translation lf
    puts $propertyReport "property\tvalue"
    foreach key {Manufacturer {Manufacturer Part Number} {PCB Footprint} {Interface Profile} {Symbol Revision} {Source Revision} Datasheet {Reserved Pin Policy}} {
        set val [::C12::cstring ""]
        ::C12::check [$part GetUserPropStringValue [::C12::cstring $key] $val] "Read property $key"
        puts $propertyReport "$key\t[DboTclHelper_sGetConstCharPtr $val]"
    }
    puts $propertyReport "packagePCBFootprint\t[::C12::string_value $package GetPCBFootprint]"
    puts $propertyReport "partValue\t[::C12::string_value $part GetPartValue]"
    puts $propertyReport "partPinNamesVisible\t$namesVisible"
    puts $propertyReport "partPinNumbersVisible\t$numbersVisible"
    close $propertyReport
    set vectorCount 0
    set actualSegments {}
    set vectorReport [open [file join $reportDirectory c12_vectors.tsv] w]
    fconfigure $vectorReport -encoding utf-8 -translation lf
    puts $vectorReport "type\tstartX\tstartY\tendX\tendY"
    set vectorIter [$part NewVectorsIter $state $::IterDefs_ALL]
    set vector [$vectorIter NextVector $state]
    while {$vector ne "NULL"} {
        incr vectorCount
        set vectorType [$vector GetObjectType]
        if {$vectorType==$::DboBaseObject_LINE} {
            set line [DboVectorToDboLine $vector]
            set segment [concat [::C12::point_list [$line GetStart $state]] [::C12::point_list [$line GetEnd $state]]]
            lappend actualSegments $segment
            puts $vectorReport [join [concat [list LINE] $segment] "\t"]
        } else {lappend errors "Unexpected body vector type $vectorType"}
        set vector [$vectorIter NextVector $state]
    }
    close $vectorReport
    delete_DboGraphicObjectVectorsIter $vectorIter
    if {$vectorCount!=4} {lappend errors "Expected four body line vectors, got $vectorCount"}
    if {[lsort $actualSegments] ne [lsort {{0 0 220 0} {220 0 220 180} {220 180 0 180} {0 180 0 0}}]} {
        lappend errors "Body line endpoints differ from planned rectangle"
    }
    set displayCount 0
    set actualDisplayProps {}
    set displayReport [open [file join $reportDirectory c12_display_properties.tsv] w]
    fconfigure $displayReport -encoding utf-8 -translation lf
    puts $displayReport "name\tx\ty\tdisplayType"
    set displayIter [$part NewDisplayPropsIter $state]
    set prop [$displayIter NextProp $state]
    while {$prop ne "NULL"} {
        incr displayCount
        set displayName [::C12::string_value $prop GetName]
        set displayLocation [::C12::point_list [$prop GetLocation $state]]
        set displayType [$prop GetDisplayType $state]
        lappend actualDisplayProps [concat [list $displayName] $displayLocation [list $displayType]]
        puts $displayReport [join [concat [list $displayName] $displayLocation [list $displayType]] "\t"]
        set prop [$displayIter NextProp $state]
    }
    close $displayReport
    delete_DboDisplayPropsIter $displayIter
    if {$displayCount!=2} {lappend errors "Expected reference/value display properties, got $displayCount"}
    if {[lsort $actualDisplayProps] ne [lsort {{{Part Reference} 0 -20 1} {Value 100 200 1}}]} {
        lappend errors "Reference/value display property fields differ"
    }
    set result [dict create pins [llength $seen] bodyVectors $vectorCount displayProperties $displayCount errors $errors]
    set summary [open [file join $reportDirectory c12_readback_result.tcldict] w]
    fconfigure $summary -encoding utf-8 -translation lf
    puts $summary $result
    close $summary
    if {$closeAfter} {::C12::check [$session RemoveLib $lib] RemoveLib}
    if {[llength $errors]} {error "C12 readback failed: $errors"}
    return $result
}

# A separate, disposable OLB to distinguish setter order from persistence
# normalization. Never pass an existing library: CreateQmi8610 refuses it.
proc ::C12::ProbePowerFlags {libraryPath reportPath} {
    set libraryPath [::C12::safe_path $libraryPath]
    set reportPath [::C12::safe_path $reportPath]
    if {[file exists $reportPath]} {error "Refusing to overwrite power probe report: $reportPath"}
    ::C12::CreateQmi8610 $libraryPath QMI8610_POWER_PROBE HOST_I2C
    file mkdir [file dirname $reportPath]
    set fh [open $reportPath w]
    fconfigure $fh -encoding utf-8 -translation lf
    puts $fh "stage\tnumber\ttype\tvisible\trawGlobal"
    set session [::C12::session]
    set state [DboState]
    set lib [$session GetLib [::C12::cstring $libraryPath] $state]
    ::C12::nonnull $lib $state GetLib
    set package [$lib GetPackage [::C12::cstring QMI8610_POWER_PROBE] $state]
    set device [$package GetDevice 0 $state]
    set cell [$device GetCell $state]
    set part [$cell FindPart 0 $state]
    set sequences(2) {{SetIsGlobal 0} {SetIsVisible 1}}
    set sequences(3) {{SetIsVisible 1} {SetIsGlobal 0}}
    set sequences(8) {{SetIsVisible 0} {SetIsGlobal 0} {SetIsVisible 1} {SetIsGlobal 0}}
    set sequences(15) [list [list SetPinType [::C12::type_code INPUT]] \
        {SetIsGlobal 0} {SetIsVisible 1} [list SetPinType [::C12::type_code POWER]] {SetIsGlobal 0}]
    set iter [$part NewLPinsIter $state]
    set pin [$iter NextPin $state]
    while {$pin ne "NULL"} {
        set position [$pin GetPinPosition $state]
        set number [::C12::string_value $device GetPinNumber $position]
        if {[info exists sequences($number)]} {
            puts $fh [join [list before $number [$pin GetPinType $state] [$pin GetIsVisible $state] [$pin GetIsGlobal $state]] "\t"]
            set step 0
            foreach operation $sequences($number) {
                lassign $operation method value
                ::C12::check [$pin $method $value] "Probe $method $number"
                incr step
                puts $fh [join [list "${step}_${method}_${value}" $number [$pin GetPinType $state] [$pin GetIsVisible $state] [$pin GetIsGlobal $state]] "\t"]
            }
        }
        set pin [$iter NextPin $state]
    }
    delete_DboLibPartPinsIter $iter
    ::C12::check [$lib SavePackageAll $package] SavePackageAll
    ::C12::check [$session SaveLib $lib] SaveLib
    ::C12::check [$session RemoveLib $lib] RemoveLib
    set lib [$session GetLib [::C12::cstring $libraryPath] $state]
    ::C12::nonnull $lib $state ReopenProbe
    set package [$lib GetPackage [::C12::cstring QMI8610_POWER_PROBE] $state]
    set device [$package GetDevice 0 $state]
    set cell [$device GetCell $state]
    set part [$cell FindPart 0 $state]
    set iter [$part NewLPinsIter $state]
    set pin [$iter NextPin $state]
    while {$pin ne "NULL"} {
        set number [::C12::string_value $device GetPinNumber [$pin GetPinPosition $state]]
        if {[info exists sequences($number)]} {
            puts $fh [join [list reopened $number [$pin GetPinType $state] [$pin GetIsVisible $state] [$pin GetIsGlobal $state]] "\t"]
        }
        set pin [$iter NextPin $state]
    }
    delete_DboLibPartPinsIter $iter
    close $fh
    ::C12::check [$session RemoveLib $lib] RemoveLib
    return $reportPath
}

package provide c12_helpers 1.0
