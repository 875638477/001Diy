import pathlib,json,sys
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
p=json.loads((R/"plans/mcu_critical_routes_v3.json").read_text(encoding="utf-8"))
p["status"]="CANDIDATE_V4_FULL_COPPER_SCREEN_PENDING"
p["placementChanges"][0]={"ref":"C21","xy":[39.478,36.25],"rotation":180,"purpose":"Same PlaceBound as37.7,36.25 r0 but swap pad ends: NRST39.3764,right / GND37.8016,left. Removes VDDA/ground route crossings. PlaceBound spacing is not actual body/assembly qualification."}
p["placementChanges"].append({"ref":"R23","xy":[32.9,33.0],"rotation":180,"purpose":"Move SPI NSS series resistor left.8016mm; frees ADC0 diagonal to shiftedC24 without less-than.3 coppergap. Preserve electrical role/value."})
for o in p["operations"]:
 if o["id"]=="NRST_PIN_CAP":o["points"]=[[39.75,31.25],[39.75,32.05],[39.35,32.45],[39.35,35.3],[39.35,36.2236],[39.3764,36.25]]
 if o["id"]=="C21_APP_GND":o["xy"]=[36.95,36.25]
 if o["id"]=="C21_APP_GND_TRACE":o["points"]=[[37.8016,36.25],[36.95,36.25]]
 if o["id"]=="NRST_SERVICE":o["xy"]=[38.7,35.3]
 if o["id"]=="NRST_SERVICE_TAP":o["points"]=[[39.35,35.3],[38.7,35.3]]
p["geometryPrecheckChanges"]="Full-copper v3 screen found four NRST/VDDA/GND overlaps plus ADC-vsR23.1 spacing. Flipped moved C21 ends, rerouted NRST east of VDDA, moved service/GND vias and shifted R23left to resolve. Exact screen saved separately."
(R/"plans/mcu_critical_routes_v4.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
s=(R/"review_v3_copper.py").read_text(encoding="utf-8")
prefix=s[:s.index('p=json.loads')]
tail=s[s.index('report={"status"'):]
tail=tail.replace("mcu_v3_full_copper_screen.json","mcu_v4_full_copper_screen.json")
s=prefix+'p=json.loads((R/"plans/mcu_critical_routes_v4.json").read_text(encoding="utf-8"))\n'+tail
(R/"review_v4_copper.py").write_text(s,encoding="utf-8")
exec(compile(s,str(R/"review_v4_copper.py"),"exec"))
