set report [dict create session $::DboSession_s_pDboSession]
foreach name {::DBO_IN ::IO ::DBO_OUT ::PAS ::POWER ::DboValue_INPUT ::IterDefs_ALL} {
    dict set report $name [expr {[info exists $name] ? [set $name] : {NOT_DEFINED}}]
}
foreach command {DboSession_CreateDesign DboDesign_NewSchematic DboSchematic_NewPage DboPage_NewPlacedInst DboPage_NewWireScalar DboPage_NewWireBus DboPage_NewAlias DboPage_NewOffPageConnector DboPage_NewGlobal DboDrawnInst_SetIsPrimitiveProp} {
    set code [catch {$command} result]
    dict set report $command [list code $code result $result]
}
set report
