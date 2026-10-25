import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
u=json.loads((R/"plans/usb_critical_routes_v8.json").read_text(encoding="utf-8"))
u["sourceEscapeException2L"]={"group":"HI_USB_J2_SOURCE_ESCAPE","layer":"TOP","polygon":[[38.95,7.25],[39.55,7.25],[39.55,8.55],[38.95,8.55]],"classPair":["HI2L_USB_FS_S","HI2L_USB_AUX_S"],"copyFrom":"HI2L_S_CLASSCLASS_10","changes":{"smdpin_line":.20},"preserved":"Allotherfieldsandglobal.5 USB-vsUSB_AUX remain; only2LlocalTOPsourceescape","actualTrigger":"J2.B7DMverticalx39.25 versusCC1(A5)pad actual.25<global.5. Copperitselfhasordinary.20margin, no globalreduction."}
u["electricalBudgetCandidate"]["native2L"]={"phase_mm":3.2757,"max_uncoupled_DP_mm":11.5394,"max_uncoupled_DM_mm":8.2637,"connectorClone4_13p5Covers":True}
(R/"plans/usb_critical_routes_v8.json").write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
# Mark retained quiet copper already present in current checkpoint with its real role before checking against same plan.
for v in("4L","2L"):
 f=R/f"review_combined_v9_{v}.py";s=f.read_text(encoding="utf-8").replace("from shapely import affinity","from shapely import affinity\nfrom shapely.ops import unary_union")
 insertion=''' quietCenter=unary_union([LineString(o["points"]) for o in p["operations"] if o["type"]=="route" and o["id"].startswith(("HSE_GUARD","HSE_C22_RETURN","HSE_C23_RETURN"))])
 for z in obs:
  if z["net"]!="GND":continue
  if z["kind"]=="route" and z["layer"]=="TOP" and LineString(z["points"]).difference(quietCenter.buffer(.000001)).length<.000001:z["groundRole"]="quiet"
  if z["kind"]=="via":
   for o in p["operations"]:
    if o["type"]=="via" and o["id"] in("HSE_LOCAL_C22","HSE_LOCAL_C23","HSE_SINGLE_ANCHOR") and z["shape"].centroid.distance(Point(o["xy"]))<.000001:
     z["groundRole"]="bridge" if o["id"]=="HSE_SINGLE_ANCHOR" else"quiet"
'''
 s=s.replace(" anchor=next(x for x in new",insertion+" anchor=next(x for x in new")
 f.write_text(s,encoding="utf-8");exec(compile(s,str(f),"exec"))
