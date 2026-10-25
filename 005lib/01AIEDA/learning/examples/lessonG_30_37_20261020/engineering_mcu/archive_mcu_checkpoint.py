import pathlib,json,shutil,hashlib
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu");G=R.parent
f=R/"review_mcu_global_geometry.py"
s=f.read_text(encoding="utf-8-sig")
s=s.replace('f=G/f"inventory/normalized_actual_{variant}.json"','f=R/f"native_snapshot_{variant}_reconcile02.json"')
s=s.replace('inner routing layers presently disallowed, changing permission needs explicit plan update.','inner non-GND signal routing presently disallowed, changing permission needs explicit plan update.')
s=s.replace('当前4层内部布线权限仍禁止','当前4层非GND信号的内部布线权限仍禁止')
f.write_text(s,encoding="utf-8")
for v in ("4L","2L"):
    src=G/f"inventory/normalized_actual_{v}.json"
    d=json.loads(src.read_text(encoding="utf-8-sig"))
    assert pathlib.Path(d["readbackDirectory"]).name==f"reconcile_{v}_02","Do not archive wrong checkpoint"
    dest=R/f"native_snapshot_{v}_reconcile02.json"
    shutil.copyfile(src,dest)
preview=R/"native_mcu_reconcile02_preview.png"
shutil.copyfile(G/"review_figures/mcu_decoupling_clock.png",preview)
review=R/"native_mcu_placement_review.json"
d=json.loads(review.read_text(encoding="utf-8-sig"))
for v,item in d["nativeSnapshots"].items():
    dest=R/f"native_snapshot_{v}_reconcile02.json"
    assert hashlib.sha256(dest.read_bytes()).hexdigest()==item["snapshotSHA256"]
    item["originalWorkingSnapshot"]=item["snapshot"]
    item["snapshot"]=str(dest)
d["previewInspected"]=str(preview)
assert hashlib.sha256(preview.read_bytes()).hexdigest()==d["previewSHA256"]
for x in d["routingOpenItems"]:
    x["rule"]=x["rule"].replace("inner routing layers presently disallowed","inner non-GND signal routing presently disallowed")
review.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
note=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\notes\lessonG_mcu_20261020.md")
s=note.read_text(encoding="utf-8-sig")
s=s.replace("R27/服务按键是现有电路选择","R27与J7复位跳帽是现有电路选择")
s=s.replace("当前4层内部布线权限仍禁止","当前4层非GND信号的内部布线权限仍禁止")
s=s.replace("证据、输入hash与逐pin结果保存在[MCU专项原生复核JSON]","两份normalized和本次预览已复制到本子目录固定为reconcile02历史快照，避免工作入口以后被current final覆盖；证据、输入hash与逐pin结果保存在[MCU专项原生复核JSON]")
note.write_text(s,encoding="utf-8")
print("Checkpoint archives and wording corrections saved.")
