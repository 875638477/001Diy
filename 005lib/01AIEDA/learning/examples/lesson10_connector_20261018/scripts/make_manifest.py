import pathlib,hashlib,json,datetime
B=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lesson10_connector_20261018")
N=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\notes\lesson10_connector_20261018.md")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
spec=json.loads((B/"spec.json").read_text(encoding="utf-8"))
val=json.loads((B/"verification/validation.json").read_text(encoding="utf-8"))
assert val["status"]=="PASS" and all(c["pass"] for c in val["checks"])
downloads=[
{"url":"https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/105/105164/1051640001_sd.pdf","status":"failed_timeout","attempts":"initial Invoke-WebRequest was stopped via this task's exec session Ctrl-C; Python urllib timeout30 and curl timeout30 then returned timeout; no successful Molex PDF saved"},
{"url":"https://www.amphenol-cs.com/media/wysiwyg/files/drawing/10118194.pdf","status":"challenge_html_not_pdf","file":"source/10118194_revD.failed.html"},
{"url":"https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/10118194.pdf","status":"challenge_html_not_pdf","file":"source/10118194_revD_cdn.failed.html"},
{"url":"https://gct.co/files/drawings/usb4105.pdf","status":"PDF_downloaded_rendered_read","file":"source/usb4105.pdf","sha256":sha(B/"source/usb4105.pdf"),"bytes":(B/"source/usb4105.pdf").stat().st_size,"revision":"B4 18/12/23","used_page":1},
{"url":"https://gct.co/connector/usb4105","status":"challenge_html_no_STEP","file":"source/gct_usb4105_product.html"},
{"url":"https://gct-embedded.partcommunity.com/3d-cad-models/?info=gct%2Fusb_connector%2Ftype_c%2Ftype_c%2Fhorizontal%2Fusb4105%2Fusb4105.prj","status":"web_search_CAD_service_found_no_STEP_downloaded","note":"Search metadata showed USB4105-15-A-120 stake1.20 variant, not selected GF-A stake.95; no wrong-variant model substituted"}
]
(B/"source/downloads.json").write_text(json.dumps(downloads,ensure_ascii=False,indent=2),encoding="utf-8")
paths=[p for p in B.rglob("*") if p.is_file() and p.name!="manifest.json"]+[N]
items=[{"relative":str(p.relative_to(B)) if p.is_relative_to(B) else "notes/"+p.name,"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p)} for p in sorted(paths)]
for p in paths:assert p.resolve().is_relative_to(pathlib.Path(r"D:\001DIY\005lib\01AIEDA").resolve())
m={"lesson":10,"topic":"真实连接器与机械受限封装","date":"2026-10-18","timezone":"Asia/Shanghai","status":"completed_declared_software_scope","mpn":spec["mpn"],"validation_status":val["status"],"checks_count":val["checks_count"],"record_root":r"D:\001DIY\005lib\01AIEDA","note":str(N),"artifacts":val["native_artifacts"],"files":items,"downloads":downloads,"warning":"Pure NULL NPTH import has intended no-default-internal warning; own importer terminated after committed PAD; native load/save/compile/readback verified. Package DRC0 state=t; PCB stored DRC0 state=nil, not full PCB DRC pass.","not_done":["STEP/full 3D interference","manufacturing/stencil release","Capture logical part","complete USB routing/SI/PI/EMI certification"],"external_user_files_modified":False}
(B/"manifest.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"status":m["status"],"checks":val["checks_count"],"files":len(items),"manifest":str(B/"manifest.json"),"note_bytes":N.stat().st_size,"native_artifacts":val["native_artifacts"]},indent=2))
