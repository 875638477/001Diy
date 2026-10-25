import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");d=json.loads((R/"review/usb_native_usb_failed2L.json").read_text(encoding="utf-8"))
print(json.dumps({k:[e for e in d["paths"][k]["referenceCoverage"] if e["projectedCenterlineUncoveredLength"]>.001] for k in("A_DP_ENTRY","B_DP_ENTRY")},ensure_ascii=True))
