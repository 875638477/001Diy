# Isolated native Capture 17.2 database lesson. All paths stay in 01AIEDA.
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
namespace eval ::C11Design {
    variable root {D:/001DIY/005lib/01AIEDA/learning}
    proc cs {v} {return [DboTclHelper_sMakeCString $v]}
    proc ok {s label} {if {[$s Failed]} {error "Native state failed: $label"}}
    proc obj {o s label} {ok $s $label; if {$o eq "NULL"} {error "NULL: $label"}; return $o}
    proc str {o m args} {
        set b [cs {}]; ok [$o $m {*}$args $b] $m
        return [DboTclHelper_sGetConstCharPtr $b]
    }
    proc point {p} {return [list [DboTclHelper_sGetCPointX $p] [DboTclHelper_sGetCPointY $p]]}
    proc snapshot {d path} {
        set s [DboState]
        set top [obj [$d GetRootSchematic $s] $s GetRootSchematic]
        set report [dict create design [str $d GetName] root [str $top GetName] pages {}]
        set it [$top NewPagesIter $s]
        for {set page [$it NextPage $s]} {$page ne "NULL"} {set page [$it NextPage $s]} {
            set rows {}
            set pi [$page NewPartInstsIter $s]
            for {set inst [$pi NextPartInst $s]} {$inst ne "NULL"} {set inst [$pi NextPartInst $s]} {
                set placed [DboPartInstToDboPlacedInst $inst]
                lappend rows [dict create reference [str $inst GetReference] fullReference [str $placed GetReferenceDesignator] location [point [$inst GetLocation $s]] value [str $placed GetPartValue] footprint [str $placed GetPCBFootprint]]
            }
            delete_DboPagePartInstsIter $pi
            dict lappend report pages [dict create name [str $page GetName] instances $rows]
        }
        delete_DboSchematicPagesIter $it
        set f [open $path w]; fconfigure $f -encoding utf-8 -translation lf; puts $f $report; close $f
        return $report
    }
    proc firstInstance {d} {
        set s [DboState]; set top [$d GetRootSchematic $s]
        set page [obj [$top GetPage [cs PAGE1] $s] $s GetPage1]
        set it [$page NewPartInstsIter $s]; set inst [$it NextPartInst $s]
        delete_DboPagePartInstsIter $it
        return $inst
    }
    proc run {} {
        variable root
        set dir "$root/examples/lesson11_capture/final"
        set logs "$root/logs/capture_C_20261019/c11_final"
        file mkdir $dir $logs
        set path "$dir/c11_basics.dsn"
        if {[file exists $path]} {error "Will not overwrite existing lesson design"}
        set s [DboState]; set sess $::DboSession_s_pDboSession; DboSession -this $sess
        set d [obj [$sess CreateDesign $s [cs $path] [cs TOP]] $s CreateDesign]
        set top [obj [$d GetRootSchematic $s] $s GetRootSchematic]
        set p1 [obj [$top NewPage $s [cs PAGE1]] $s NewPage1]
        set p2 [obj [$top NewPage $s [cs PAGE2]] $s NewPage2]
        set lib [obj [$sess GetLib [cs "$root/examples/lesson12_capture/c12_qmi8610_single.olb"] $s] $s GetLib]
        set pkg [obj [$lib GetPackage [cs QMI8610_C12_SINGLE] $s] $s GetPackage]
        set dev [obj [$pkg GetDevice 0 $s] $s GetDevice]
        set cell [obj [$dev GetCell $s] $s GetCell]
        set part [obj [$cell FindPart 0 $s] $s FindPart]
        set inst [obj [$p1 NewPlacedInst $s [cs QMI8610_C12_SINGLE] [cs QMI8610_C12_SINGLE] $part $dev [DboTclHelper_sMakeCPoint 300 300]] $s NewPlacedInst]
        ok [$inst SetReference [cs U101]] SetReference
        ok [$top SavePage $p1] SavePage1
        ok [$top SavePage $p2] SavePage2
        ok [$sess SaveDesign $d] SaveDesign
        snapshot $d "$logs/01_saved.tcldict"
        ok [$sess RemoveDesign $d] CloseBaseline
        ok [$sess RemoveLib $lib] CloseSourceLib
        file copy $path "$dir/c11_basics_baseline.dsn"
        set d [obj [$sess GetDesignAndSchematics [cs $path] $s] $s Reopen]
        snapshot $d "$logs/02_reopened.tcldict"
        set inst [firstInstance $d]
        ok [$inst SetLocation [DboTclHelper_sMakeCPoint 700 500]] MoveUnsaved
        snapshot $d "$logs/03_unsaved_move.tcldict"
        ok [$sess RemoveDesign $d] DiscardUnsaved
        set d [obj [$sess GetDesignAndSchematics [cs $path] $s] $s ReopenDiscarded]
        snapshot $d "$logs/04_discard_reopened.tcldict"
        set inst [firstInstance $d]
        ok [$inst SetLocation [DboTclHelper_sMakeCPoint 500 450]] MoveSaved
        ok [$inst MarkModified] MarkInstanceModified
        set top [$d GetRootSchematic $s]
        set p1 [$top GetPage [cs PAGE1] $s]
        ok [$p1 MarkModified] MarkPageModified
        ok [$top SavePage $p1] SaveMovedPage
        ok [$sess SaveDesign $d] SaveMoved
        snapshot $d "$logs/05_saved_move.tcldict"
        ok [$sess RemoveDesign $d] CloseMoved
        file copy -force "$dir/c11_basics_baseline.dsn" $path
        set d [obj [$sess GetDesignAndSchematics [cs $path] $s] $s ReopenRestored]
        set result [snapshot $d "$logs/06_restored_reopened.tcldict"]
        ok [$sess RemoveDesign $d] FinalClose
        return $result
    }
}
if {![info exists ::C11DefinitionsOnly] || !$::C11DefinitionsOnly} {::C11Design::run}
