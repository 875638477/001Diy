import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
g=json.loads((R/"plans/gpio_north_escape_v2.json").read_text(encoding="utf-8"))
top={"GPIO_PC13":[[42.25,31.25],[42.25,29.15],[42,28.9]],"GPIO_PC14":[[41.75,31.25],[41.75,29.8],[41,29.8],[41,27.8]],"GPIO_PC15":[[41.25,31.25],[41.25,30.25],[40.3,30.25],[40.3,28.9]]}
bottom={"GPIO_PC13":[[42,28.9],[42,31.1],[35.8,31.1]],"GPIO_PC14":[[41,27.8],[41,28.0],[39.5,28.0],[39.5,28.5],[35,28.5]],"GPIO_PC15":[[40.3,28.9],[40.3,30.3],[35.4,30.3]]}
for o in g["operations"]:
 if o["net"] in top:
  if o["type"]=="via":o["xy"]=top[o["net"]][-1]
  else:o["points"]=top[o["net"]] if o["layer"]=="TOP" else bottom[o["net"]]
g["status"]="CANDIDATE_V3_AXIAL_PAD_CLEARANCE_AND_VSSA_ROUTE_AVOIDED";g["supersedes"]+=" v2 furtherwestPC15path approachedactualVSSAground .05mm andBOTTOMpartialroutes crossed; v3 shiftsviasandusesparallelwestrowswithexplicitVSSA/returnviaavoidance."
(R/"plans/gpio_north_escape_v3.json").write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8")
s=(R/"build_combined_v5.py").read_text(encoding="utf-8")
# Reuse only the existing already-combined plan, substituting GPIO operations.
for v in ("4L","2L"):
 p=json.loads((R/f"plans/combined_v5_screen_{v}.json").read_text(encoding="utf-8"))
 p["operations"]=[o for o in p["operations"] if not o["id"].startswith("GPIO_")]+g["operations"]
 (R/f"plans/combined_v6_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 q=(R/f"review_combined_v5_{v}.py").read_text(encoding="utf-8").replace(f"combined_v5_screen_{v}.json",f"combined_v6_screen_{v}.json").replace(f"combined_v5_copper_screen_{v}.json",f"combined_v6_copper_screen_{v}.json")
 (R/f"review_combined_v6_{v}.py").write_text(q,encoding="utf-8")
 exec(compile(q,str(R/f"review_combined_v6_{v}.py"),"exec"))
