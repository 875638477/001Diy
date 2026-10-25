import pathlib,json,datetime,hashlib
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
p=R/"plans/usb_critical_routes_v6.json";u=json.loads(p.read_text(encoding="utf-8"));mapping=[]
for o in u["commonOperations"]:
 if o["type"]=="via" and "OR_VERIFIED" in o["padstack"]:
  mapping.append({"id":o["id"],"source":o["padstack"],"actual":"L28_VIA030_C060","reason":"Native axlDBCreateVia expects an existing exact padstack name; choice prose cannot be executable string."});o["padstack"]="L28_VIA030_C060"
u["status"]="CANDIDATE_V7_EXECUTABLE_EXACT_PADSTACK_NAME_GEOMETRY_UNCHANGED"
u["viaIdentifierCorrection"]={"source":"v6","nativeFirstFailure":"Non-existent placeholder literal caused axlDBCreateVia=nil; stopped before saved source changed, preserve native log.","mapping":mapping,"cadMaskRequirement":"Use actual L28_VIA030_C060 CAD pad definition; retain mustBeTented flag and audit actual soldermask aperture/artwork, no manufacturer tenting certification."}
out=R/"plans/usb_critical_routes_v7.json";out.write_text(json.dumps(u,ensure_ascii=False,indent=2),encoding="utf-8")
(R/"review/usb_v6_native_adapter_mapping.json").write_text(json.dumps({"sourceFile":str(p),"sourceSHA256":hashlib.sha256(p.read_bytes()).hexdigest(),"actualFile":str(out),"actualSHA256":hashlib.sha256(out.read_bytes()).hexdigest(),"mapping":mapping,"geometryChanges":[]},ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"file":str(out),"mappingCount":len(mapping),"geometryChanges":0},ensure_ascii=True))
