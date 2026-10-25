import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
m=json.loads((R/"plans/mcu_critical_routes_v6.json").read_text(encoding="utf-8"))
for o in m["operations"]:
 if o["id"]=="ADC_PIN_CAP":o["points"]=[[38.25,31.25],[38.25,32.2],[37.8,32.2],[37.7,32.3],[35.5,32.3],[34.8,33]]
m["nativeV5Corrections"]["4L_and_2L_failures"][1]["solution"]="Keep sourcecorner38.25,32.2 toavoidVDDA.6diag; raisefrom37.8,32.2 to37.7,32.3 thenhorizontal y32.3; preserve global.3 outside x37.7."
(R/"plans/mcu_critical_routes_v6.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
u=json.loads((R/"plans/usb_critical_routes_v6.json").read_text(encoding="utf-8"))
power=json.loads((H/"engineering_power/power_star_03b.json").read_text(encoding="utf-8"))
esd=json.loads((H/"engineering_power/ESD_ground_routes_04b.json").read_text(encoding="utf-8"))
for o in esd["operations"]:
 if o["id"]=="V_HI_ESD_VBUS_LEFT":o["xy"]=[40.25,9.3]
 if o["id"]=="ESD_VBUS_U4_ESCAPE":o["points"]=[[40.25,10.1],[40.25,9.3]];o["width"]=.4;o.pop("widths",None)
 if o["type"]=="route" and o["layer"]=="BOTTOM" and o["net"]=="USB_VBUS":o["points"][0]=[40.25,9.3]
(R/"plans/ESD04c_proposed_for_power_review.json").write_text(json.dumps(esd,ensure_ascii=False,indent=2),encoding="utf-8")
gp=json.loads((R/"plans/gpio_north_escape_v3.json").read_text(encoding="utf-8"))
for v in("4L","2L"):
 p=dict(m);p["placementChanges"]=m["placementChanges"]+u["placementChanges"];p["operations"]=m["operations"]+u["commonOperations"]+u["variantOperations"][v]+power["operations"]+gp["operations"]+esd["operations"]
 (R/f"plans/combined_v8_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v6_{v}.py").read_text(encoding="utf-8").replace("combined_v6","combined_v8")
 (R/f"review_combined_v8_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v8_{v}.py"),"exec"))
