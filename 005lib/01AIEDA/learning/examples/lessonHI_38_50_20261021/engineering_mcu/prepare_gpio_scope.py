import pathlib,json,hashlib
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
n=json.loads((H/"inventory/checkpoints/usb_esd_4L_b008/normalized.json").read_text(encoding="utf-8"));nw=json.loads((H/"inventory/checkpoints/usb_esd_4L_b008/networks.json").read_text(encoding="utf-8"));pol=json.loads((H/"plans/ordinary_policy_4L_v5.json").read_text(encoding="utf-8"));terms=[]
for q in nw["nets"]:
 if q["net"].startswith("GPIO_"):
  terms.append({"net":q["net"],"minTerminalJoins":q["minTerminalJoins"],"terminals":[{k:t.get(k) for k in("key","xy","through")} for c in q["components"] for t in c["terminals"]]})
print(json.dumps(terms,ensure_ascii=True));print("POLICYKEYS",list(pol));print("AREAS",json.dumps(pol.get("reservedAreas"),ensure_ascii=True));print("ANCHORS",json.dumps(pol.get("componentAnchors"),ensure_ascii=True))
(R/"plans/gpio_scope_preplanning_01.json").write_text(json.dumps({"status":"PREPARATION_ONLY_WAIT_IMMUTABLE_07b_V306b_GPIO6_source5_CHECKPOINT","nets":terms,"inputBaselineSHA256":hashlib.sha256((H/"inventory/checkpoints/usb_esd_4L_b008/normalized.json").read_bytes()).hexdigest(),"constraints":["Preserve actualPC13/PC15BOTTOMpartialends; PC14TOP45.6,25.2","Do not cross HSE island/guard/applicationmoat norADC RC/supply/input sensitive corridors","Do not occupy SPI sourcebankx33.5..35.4/y26.5..33.5","WaitnativefreshcheckpointforactualreferenceCopperScene/DRCprovenance; do notcallpreplanningnativepassed"]},ensure_ascii=False,indent=2),encoding="utf-8")
