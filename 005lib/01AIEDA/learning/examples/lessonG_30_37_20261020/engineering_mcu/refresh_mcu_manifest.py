import pathlib,re,json,hashlib,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu")
note=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\notes\lessonG_mcu_20261020.md")
text=note.read_text(encoding="utf-8-sig")
old="仍待主任务原生证据：全部80件布局/高度/机械/引脚与原基线一致，局部铜/过孔/实际地平面读回，三对去耦真实连通与当前规则、USB走廊、HSE/ADC路径预审及全局布局冻结。后续完整布线/参考连续性、晶体实测/ADC精度/热/USB工艺释放、GUI均保持各自待验，不用DRC=0代替。"
new="统一布局阶段的本组24件/96pin已在第8节补上两板原生读回及独立复核；全部80件布局/高度/机械/引脚保持由主任务全板报告负责。尚待单列局部铜/过孔/实际地平面读回、三对去耦真实连通与短颈/最小区域规则，HSE/ADC仍为布局及走廊预审。后续完整布线/参考连续性、晶体实测/ADC精度/热/USB工艺释放、GUI均保持各自待验，不用DRC=0代替。"
if old in text:text=text.replace(old,new)
note.write_text(text,encoding="utf-8")
links=[]
for label,target in re.findall(r"\[([^\]]*)\]\(([^)]+)\)",text):
    if target.startswith(("http://","https://","#")):continue
    resolved=(note.parent/target.split("#")[0]).resolve()
    links.append({"target":target,"exists":resolved.exists()})
assert all(x["exists"] for x in links)
(R/"note_links_check.json").write_text(json.dumps({"links":links,"pass":True,"checked":datetime.datetime.now().astimezone().isoformat()},ensure_ascii=False,indent=2),encoding="utf-8")
manifest={"scope":"engineering_mcu own files and own course note only","status":"COMPLETE_MCU_LAYOUT_AND_LOCAL_COPPER_REVIEW_FULL_BOARD_ROUTING_PENDING","generated":datetime.datetime.now().astimezone().isoformat(),"historicalNonReplayHelper":"finish_mcu_records.py is an archived one-time candidate-stage helper. It expects an old pre-B3 note paragraph and contains superseded manual metric strings. Do not rerun; current note/clock_path_precheck.json plus this refresh script are authoritative.","files":[]}
for f in sorted(R.rglob("*")):
    if f.is_file() and f.name!="artifact_manifest.json":
        manifest["files"].append({"path":str(f),"bytes":f.stat().st_size,"sha256":hashlib.sha256(f.read_bytes()).hexdigest()})
manifest["files"].append({"path":str(note),"bytes":note.stat().st_size,"sha256":hashlib.sha256(note.read_bytes()).hexdigest()})
(R/"artifact_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
assert all(hashlib.sha256(pathlib.Path(x["path"]).read_bytes()).hexdigest()==x["sha256"] for x in manifest["files"])
print(json.dumps({"files":len(manifest["files"]),"localLinks":len(links),"manifestVerified":True,"noteBytes":note.stat().st_size,"noteSHA256":hashlib.sha256(note.read_bytes()).hexdigest()},ensure_ascii=True))
