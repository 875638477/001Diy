proc debug_part_hierarchy {} {
    set s $::DboSession_s_pDboSession
    DboSession -this $s
    set st [DboState]
    set dsn [$s GetActiveDesign]
    set lNullObj NULL

    set lVI [$dsn NewViewsIter $st $::IterDefs_SCHEMATICS]
    set lV [$lVI NextView $st]
    set lSch [DboViewToDboSchematic $lV]
    set lPI [$lSch NewPagesIter $st]
    set lPg [$lPI NextPage $st]

    set lPII [$lPg NewPartInstsIter $st]
    set lInst [$lPII NextPartInst $st]

    set found 0
    while {$lInst != $lNullObj && !$found} {
        set lPlaced [DboPartInstToDboPlacedInst $lInst]
        if {$lPlaced != $lNullObj} {
            set rc [DboTclHelper_sMakeCString]
            $lPlaced GetReferenceDesignator $rc
            set ref [DboTclHelper_sGetConstCharPtr $rc]

            set cnt [$lInst GetPinCount $st]
            if {$cnt > 0} {
                set p0 [$lInst GetPin 0 $st]
                set pn [DboTclHelper_sMakeCString]
                $p0 GetPinNumber $pn
                if {[DboTclHelper_sGetConstCharPtr $pn] == ""} {
                    set found 1
                    puts "=== Found problematic instance: $ref ==="

                    puts ""
                    puts "--- DboLibPart from GetPart ---"
                    set lPart [$lPlaced GetPart $st]
                    set nc [DboTclHelper_sMakeCString]
                    $lPart GetName $nc
                    puts "  Part name: '[DboTclHelper_sGetConstCharPtr $nc]'"
                    puts "  Part obj: $lPart"
                    puts "  Part type: [$lPart GetObjectType]"

                    puts ""
                    puts "--- Navigate UP from Part ---"
                    if {[catch {
                        set p1 [$lPart GetParentObj]
                        set n1 [DboTclHelper_sMakeCString]
                        $p1 GetName $n1
                        puts "  Parent1: obj=$p1 name='[DboTclHelper_sGetConstCharPtr $n1]' type=[$p1 GetObjectType]"

                        if {[catch {
                            set p2 [$p1 GetParentObj]
                            set n2 [DboTclHelper_sMakeCString]
                            $p2 GetName $n2
                            puts "  Parent2: obj=$p2 name='[DboTclHelper_sGetConstCharPtr $n2]' type=[$p2 GetObjectType]"

                            if {[catch {
                                set p3 [$p2 GetParentObj]
                                set n3 [DboTclHelper_sMakeCString]
                                $p3 GetName $n3
                                puts "  Parent3: obj=$p3 name='[DboTclHelper_sGetConstCharPtr $n3]' type=[$p3 GetObjectType]"
                            } err]} { puts "  Parent3 FAIL: $err" }
                        } err]} { puts "  Parent2 FAIL: $err" }
                    } err]} { puts "  Parent1 FAIL: $err" }

                    puts ""
                    puts "--- Try GetOwner from Part ---"
                    if {[catch {
                        set ow [$lPart GetOwner]
                        set nw [DboTclHelper_sMakeCString]
                        $ow GetName $nw
                        puts "  Owner: obj=$ow name='[DboTclHelper_sGetConstCharPtr $nw]' type=[$ow GetObjectType]"
                    } err]} { puts "  Owner FAIL: $err" }

                    puts ""
                    puts "--- Try GetContainingLib from Part ---"
                    if {[catch {
                        set cl [$lPart GetContainingLib]
                        set ncl [DboTclHelper_sMakeCString]
                        $cl GetName $ncl
                        puts "  ContainingLib: obj=$cl name='[DboTclHelper_sGetConstCharPtr $ncl]' type=[$cl GetObjectType]"
                    } err]} { puts "  ContainingLib FAIL: $err" }

                    puts ""
                    puts "--- Try GetDevice on DboPartInst ---"
                    if {[catch {
                        set dev [$lInst GetDevice $st]
                        puts "  Device from PartInst: $dev"
                    } err]} { puts "  GetDevice from PartInst FAIL: $err" }

                    puts ""
                    puts "--- Try GetPackage on DboPartInst ---"
                    if {[catch {
                        set pkg [$lInst GetPackage $st]
                        puts "  Package from PartInst: $pkg"
                        if {$pkg != $lNullObj} {
                            set npk [DboTclHelper_sMakeCString]
                            $pkg GetName $npk
                            puts "  Package name: '[DboTclHelper_sGetConstCharPtr $npk]'"
                        }
                    } err]} { puts "  GetPackage from PartInst FAIL: $err" }
                }
            }
        }
        set lInst [$lPII NextPartInst $st]
    }

    if {!$found} { puts "No problematic instance found on first page" }

    delete_DboPagePartInstsIter $lPII
    delete_DboSchematicPagesIter $lPI
    delete_DboLibViewsIter $lVI
}

debug_part_hierarchy
