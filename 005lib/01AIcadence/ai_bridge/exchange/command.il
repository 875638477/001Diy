; poll: does the test path still exist?
printf("TEST obj alive: nSegs=%L net=%L bbox=%L\n"
    AIB_testObj->nSegs AIB_testObj->net->name AIB_testObj->bBox)
axlClearSelSet()
axlSetFindFilter(?enabled list("noall" "clines") ?onButtons list("noall" "clines"))
axlAddSelectAll()
AIB_found = 0
foreach(o axlGetSelSet()
    when( o->net && o->net->name == "WIFI_BT_RSTN/1V8" && o->layer == "ETCH/L8"
        AIB_found = AIB_found + 1
    )
)
printf("L8 WIFI clines found by selectAll: %d\n" AIB_found)
axlClearSelSet()
printf("done\n")
