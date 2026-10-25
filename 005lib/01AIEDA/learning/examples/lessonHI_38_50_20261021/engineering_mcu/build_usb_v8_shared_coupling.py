import pathlib,json,math,hashlib,copy
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
u=json.loads((R/"plans/usb_critical_routes_v7.json").read_text(encoding="utf-8"))
u["status"]="CANDIDATE_V8_SHARED_DM_COUPLED_TRUNK_PRESERVE_MCU_ELECTRICAL_BUDGET"
newpoints={"4L":[[39.4,18.3984],[39.4,18.95],[40.6,20.15],[40.6,21.745],[40.75,21.895],[40.75,22.75]],"2L":[[39.4,18.3984],[39.4,18.95],[40.59,20.14],[40.59,21.7492],[40.75,21.9092],[40.75,22.75]]}
for v in("4L","2L"):
 for o in u["variantOperations"][v]:
  if o["id"]=="USB_SHARED_DM":
   o["points"]=newpoints[v];o["purpose"]="Make actual straighttrunk edgegap.15(4L)/.16(2L) with correctly staggered45degreebend; preserve sharedpair originaluncoupled6/phase1. Allgeometryscreen andnativeactualrequired."
le=lambda p:sum(math.dist(a,b) for a,b in zip(p,p[1:]))
dp=next(o for o in u["commonOperations"] if o["id"]=="USB_SHARED_DP")
u["candidateLengths"]["sharedMCUSideByVariant"]={v:{"DP":le(dp["points"]),"DM":le(newpoints[v]),"DPminusDM":le(dp["points"])-le(newpoints[v])} for v in("4L","2L")}
u["candidateLengths"]["mainWholePlanarSkewByVariant"]={v:{orient:u["candidateLengths"][orient]["DPminusDM" if orient=="orientationB" else"DPminusDM_planar"]+x["DPminusDM"] for orient in("orientationA","orientationB")} for v,x in u["candidateLengths"]["sharedMCUSideByVariant"].items()}
u["electricalBudgetCandidate"]={"status":"ROOT_APPROVED_ONLY_CONNECTOR_COPY_NATIVE_FIELD_CHECK_PENDING","connectorDiffpair":"DP_USB_CONNECTOR","copyFrom":"E_USB_FS_BUDGET","changes":{"phase_mm":4.0,"max_uncoupled_mm":13.5},"preserved":["maxVia2","other electrical fields","MCUshared originalphase1/maxUncoupled6 andviaunchanged"],"basis":{"native4L_phase_A6_A7":3.2757,"native4L_uncoupled_DP":12.6858,"native4L_uncoupled_DM":9.4101,"phaseMargin":.7243,"uncoupledMarginDP":.8142},"meaning":"Pedagogical planar nativepath thresholds with explicitbranch/geometricbasis. Notsignalflighttime certification, nativephaseexcludedbarrel; independentlyestimateextra2fullthroughbarrels.","2L":"Sameconnectorbranchesandshorteruncoupledwidebulkexpected; confirmactualnativeafterroute beforeaccept.","MCUsharedChange":"Geometrymakes1.45mm-ish trunk genuinelycoupled; doNOTincreaseMCUpair6mmuncoupled simplytohideDNPbranch."}
u["delayScaleEstimate"]["orientationA_wholeDataPathSkew_ps_range"]={v:[u["candidateLengths"]["mainWholePlanarSkewByVariant"][v]["orientationA"]*math.sqrt(er)/.299792458+y for er in(2.8,3.5)] for v,y in u["delayScaleEstimate"]["extraBarrelDelay_ps"].items()}
u["nativeV7Observation"]="Physical/spacing0; electricalconnectorphase3.2757/uncoupled12.6858/9.4101 actualplanned. SharedDNPuncoupled6.4531/6.3804 becauseoldgap.30 trunk notcoupled. v8 changesonlysharedDMandexplicitconnectorbudget, no globalrelaxation."
(R/"plans/usb_critical_routes_v8.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
m=json.loads((R/"plans/mcu_critical_routes_v6.json").read_text(encoding="utf-8"));power=json.loads((H/"engineering_power/power_star_03b.json").read_text(encoding="utf-8"));gp=json.loads((R/"plans/gpio_north_escape_v3.json").read_text(encoding="utf-8"));esd=json.loads((H/"engineering_power/ESD_ground_routes_04c.json").read_text(encoding="utf-8"))
for v in("4L","2L"):
 p=dict(m);p["placementChanges"]=m["placementChanges"]+u["placementChanges"];p["operations"]=m["operations"]+u["commonOperations"]+u["variantOperations"][v]+power["operations"]+gp["operations"]+esd["operations"]
 (R/f"plans/combined_v9_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v8_{v}.py").read_text(encoding="utf-8").replace("combined_v8","combined_v9")
 (R/f"review_combined_v9_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v9_{v}.py"),"exec"))
print(json.dumps(u["candidateLengths"]["sharedMCUSideByVariant"],ensure_ascii=True))
