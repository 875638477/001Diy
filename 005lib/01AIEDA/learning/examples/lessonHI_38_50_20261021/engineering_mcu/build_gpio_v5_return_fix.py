import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
g=json.loads((R/"plans/gpio_north_escape_v4.json").read_text(encoding="utf-8"));g["status"]="CANDIDATE_V5_PC14_STAR_AVOIDANCE_WITH_ACTUAL_GND_RETURN_PAD_CLEARANCE"
for o in g["operations"]:
 if o["id"]=="GPIO_RETURN_WEST_STAR":o["xy"]=[34.7,30.5];o["purpose"]="ActualallcoppergridselectedGNDreturn .92195mm toPC14exit; minothernet~.32196; old34.0,30.5 hitR21.1 andwasrejectedbeforeexecution."
g["rejectedV4Return"]="GNDvia34.0,30.5 overlapped actualR21.1; retained failurev11report. New34.7,30.5 screenedallpads/oldandnewtraces/vias."
(R/"plans/gpio_north_escape_v5.json").write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8")
for v in("4L","2L"):
 p=json.loads((R/f"plans/combined_v11_screen_{v}.json").read_text(encoding="utf-8"))
 for o in p["operations"]:
  if o["id"]=="GPIO_RETURN_WEST_STAR":o["xy"]=[34.7,30.5]
 (R/f"plans/combined_v12_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v11_{v}.py").read_text(encoding="utf-8").replace("combined_v11","combined_v12")
 (R/f"review_combined_v12_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v12_{v}.py"),"exec"))
print("GPIO5 operations",len(g["operations"]))
