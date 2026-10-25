import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
g=json.loads((R/"plans/gpio_north_escape_v3.json").read_text(encoding="utf-8"));g["status"]="CANDIDATE_V6_PC14_EAST_EXIT_PRESERVE_SPI_SOURCE_BANK"
for o in g["operations"]:
 if o["id"]=="GPIO_GPIO_PC14_BOTTOM_START":o["points"]=[[41,27.8],[43.6,25.2],[45.6,25.2]];o["to"]=["GPIO_PC14_EAST_EXIT"];o["purpose"]="Rootrequested southeastBOTTOMescape; no weststub acrossnewSTARorSPIbank."
g["operations"] +=[{"type":"via","id":"GPIO_PC14_EAST_EXIT","net":"GPIO_PC14","xy":[45.6,25.2],"padstack":"L28_VIA030_C060","purpose":"OffpadBOTTOM-toTOP eastanchor, thenrootroutesoutsideHSEtoJ11; no danglingweststub"},
{"type":"via","id":"GPIO_RETURN_EAST_EXIT","net":"GND","xy":[46.95,24.9],"padstack":"L28_VIA030_C060","purpose":"ApplicationGNDnearPC14easttransition distance1.382932mm; realreferenceandplaneproofrequired"}]
g["continuation"]={"GPIO_PC13":{"layer":"BOTTOM","xy":[35.8,31.1]},"GPIO_PC14":{"layer":"TOP","xy":[45.6,25.2],"via":"GPIO_PC14_EAST_EXIT"},"GPIO_PC15":{"layer":"BOTTOM","xy":[35.4,30.3]}}
g["twoLayerReferencePatches"]=[{"layer":"TOP","net":"GND","polygon":[[35.8,27],[42.4,27],[42.4,31.9],[35.8,31.9]]},{"layer":"TOP","net":"GND","polygon":[[39.2,24.6],[47.5,24.6],[47.5,28.4],[39.2,28.4]]}]
g["referenceLimitation"]="2LnewBOTTOMPC14crossesprojectionofTOPV3starx43; realTOPGNDsplitbyrailmustconnectthroughnearGNDviasandBOTTOMglobalcopper, NOTuniformmicrostripclaim. Actualgap/returnreviewrequired;4LactualL3referenceindependent. TOPpatchescliprealpads/linesandstopbelowquietanchormoat."
g["supersedes"]="GPIO3westPC14netwouldapproachnewSTAR. v4/v5westexitwouldoccupyrootSPI_NSS/SCK/MISObankx33.5..35.4/y26.5..33.5; rejectedbeforeexecution. No SPIbankviainv6."
(R/"plans/gpio_north_escape_v6.json").write_text(json.dumps(g,ensure_ascii=False,indent=2),encoding="utf-8")
for v in("4L","2L"):
 p=json.loads((R/f"plans/combined_v10_screen_{v}.json").read_text(encoding="utf-8"));p["operations"]=[o for o in p["operations"] if not o["id"].startswith("GPIO_")]+g["operations"]
 (R/f"plans/combined_v13_screen_{v}.json").write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding="utf-8")
 s=(R/f"review_combined_v10_{v}.py").read_text(encoding="utf-8").replace("combined_v10","combined_v13")
 (R/f"review_combined_v13_{v}.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/f"review_combined_v13_{v}.py"),"exec"))
