import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
g=json.loads((R/"plans/gpio_north_escape_v3.json").read_text(encoding="utf-8"));g["status"]="CANDIDATE_V4_PC14_EXIT_NORTHWEST_STAR_DIAGONAL_AVOIDED"
for o in g["operations"]:
 if o["id"]=="GPIO_GPIO_PC14_BOTTOM_START":o["points"]=[[41,27.8],[41,28],[39.5,28],[39.5,28.5],[35.8,28.5],[34.7,29.6],[34.5,29.6]];o["to"]=["GPIO_PC14_WEST_EXIT"];o["purpose"]="Explicit northwestoffpadexit avoiding newpower07bdiagonal, thenrootcontinuesTOPtowestheader."
g["operations"] +=[{"type":"via","id":"GPIO_PC14_WEST_EXIT","net":"GPIO_PC14","xy":[34.5,29.6],"padstack":"L28_VIA030_C060","purpose":"OffpadBOTTOM-toTOPwestescape; actualSTAR clearance~.389949mm"},
{"type":"via","id":"GPIO_RETURN_WEST_STAR","net":"GND","xy":[34,30.5],"padstack":"L28_VIA030_C060","purpose":"ApplicationGNDnearPC14westlayertransition .?actualcenter1.029563mm; realplane/patchreachmustverify"}]
g["westContinuation"]={"GPIO_PC13":{"layer":"BOTTOM","xy":[35.8,31.1]},"GPIO_PC14":{"layer":"TOP","xy":[34.5,29.6],"via":"GPIO_PC14_WEST_EXIT"},"GPIO_PC15":{"layer":"BOTTOM","xy":[35.4,30.3]}}
g["twoLayerReferencePatch"]={"layer":"TOP","net":"GND","polygon":[[33.7,27],[42.4,27],[42.4,31.9],[33.7,31.9]],"requirement":"RealfilledcopperclippedaroundallactualTOPpads/paths, connectedvianearsourceandwestexit. Rectangleisnotautomaticreturncontinuity."}
g["newConflictResolved"]="Power07bdiagonalx+y62.7 tooldPC14(35,28.5) linegap.165685<.20/.30. Routekeptabove/rightofdiagonal untiloffpadvia34.5,29.6, thenTOPoverlineinstead oflonggroundcutdetour. OtherGPIOunchanged."
(R/"plans/gpio_north_escape_v4.json").write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8")
for v in("4L","2L"):
 p=json.loads((R/f"plans/combined_v10_screen_{v}.json").read_text(encoding="utf-8"))
 p["operations"]=[o for o in p["operations"] if not o["id"].startswith("GPIO_")]+g["operations"]
 (R/f"plans/combined_v11_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v10_{v}.py").read_text(encoding="utf-8").replace("combined_v10","combined_v11")
 (R/f"review_combined_v11_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v11_{v}.py"),"exec"))
