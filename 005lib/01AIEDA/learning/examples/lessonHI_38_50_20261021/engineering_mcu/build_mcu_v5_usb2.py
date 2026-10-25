import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
p=json.loads((R/"plans/mcu_critical_routes_v4.json").read_text(encoding="utf-8"));p["status"]="CANDIDATE_V5_NO_OVERLAP_OR_SUB020_IN_COMPLETE_LOCAL_SCREEN_NATIVE_RULES_PENDING"
for o in p["operations"]:
 if o["id"]=="C24_APP_GND":o["xy"]=[34.4,35.7]
 if o["id"]=="C24_APP_GND_TRACE":o["points"]=[[34.8,34.5748],[34.4,34.9748],[34.4,35.7]]
 if o["id"]=="HSE_XTAL_OUT":o["points"]=[[40.2,34.7748],[40.3,34.8748],[40.3,37.7],[42,37.7]]
 if o["id"]=="HSE_OUT_LOAD":o["points"]=[[40.3,37.7],[39.8,37.7]]
p["geometryPrecheckChanges"]+=" v5 moves C24 appGNDvia to34.4,35.7 and XTAL_OUT vertical to40.3, preserving global.3 outside north escape region rather than extending exceptions."
(R/"plans/mcu_critical_routes_v5.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
s=(R/"review_v4_copper.py").read_text(encoding="utf-8").replace("mcu_critical_routes_v4.json","mcu_critical_routes_v5.json").replace("mcu_v4_full_copper_screen.json","mcu_v5_full_copper_screen.json")
(R/"review_v5_copper.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/"review_v5_copper.py"),"exec"))
u=json.loads((R/"plans/usb_critical_routes_v1.json").read_text(encoding="utf-8"));u["status"]="CANDIDATE_V2_MINIMUM_BRANCH_PREFERRED_REFERENCE_AND_MATCHING_EXCEPTIONS_PENDING"
u["rejectedCandidate"]="v1 extra TOP DM U-turn and BOTTOM compensating dogleg reduce branch orientation skew but worsen two-layer reference/pocket topology underhousing; retained original for comparison. Prefer minimumbranch and explicit per-endpoint/connector budget."
for o in u["commonOperations"]:
 if o["id"]=="USB_DP_MIRROR_BOTTOM":o["points"]=[[39.75,5.8],[40.75,5.8]];o["purpose"]="Shortest1mm BOTTOM mirrorcrossing; avoid matching doglegs that damage reference."
 if o["id"]=="USB_DM_A7_MERGE":o["points"]=[[40.25,7.355],[40.25,8.6],[39.25,8.6],[39.25,7.355]];o["purpose"]="ShortestTOPmirrorjoin behindconnector tips; underhousing reference patch avoids extra data U slot."
u["matchingDecision"]="Preferredminimumbranch leaves TypeC A6/A7 orientation entry skew about3.276mm versus B6/B7 .166mm. This is explicit mirrorleaf skew, not fullpath matched. Native E_USB_FS_BUDGET1mm may need endpoint-aware justification or a separate E_USB_CONNECTOR_BUDGET copy only for USB_DP/DM; do not modify USB_SHARED or all classes. Exact worst path, delays, reference and finalrule recorded before approval. Manufacturer/hardware compliance remainsopen."
(R/"plans/usb_critical_routes_v2.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
print("USB minimumbranch v2 saved; original lengths in v1 historical, recompute final from final native.")
