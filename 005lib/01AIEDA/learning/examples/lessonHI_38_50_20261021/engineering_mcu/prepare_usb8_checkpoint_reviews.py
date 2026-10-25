import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu")
f=R/"review_usb_native_paths.py";s=f.read_text(encoding="utf-8");s=s.replace('start=key("TOP",pin(n,*src));end=key("TOP",pin(n,*dst));','resolve=lambda s: s if isinstance(s[0],(int,float)) else pin(n,*s)\n start=key("TOP",resolve(src));end=key("TOP",resolve(dst));')
s=s.replace('paths={name:graph_path(n,*args) for name,args in requests.items()}','requests.update({"DP_PULLUP_TEE":("USB_DP",(40.455 if variant=="4L" else 40.905,14.6),("R11","2")),"A_DP_TO_SERIES":("USB_DP",("J2","A6"),("R5","2")),"A_DM_TO_SERIES":("USB_DM",("J2","A7"),("R6","2")),"B_DP_TO_SERIES":("USB_DP",("J2","B6"),("R5","2")),"B_DM_TO_SERIES":("USB_DM",("J2","B7"),("R6","2"))})\n paths={name:graph_path(n,*args) for name,args in requests.items()}')
f.write_text(s,encoding="utf-8")
# Reuse independent MCU preservation criteria against later USB snapshots, preserve original script/report.
s=(R/"review_mcu6_native.py").read_text(encoding="utf-8").replace('MCU6_NATIVE_CHECKPOINT_INDEPENDENT_REVIEW_NOT_FINAL_HI_BOARD','MCU6_GEOMETRY_AND_QUIET_ISLAND_PRESERVATION_AFTER_USB8_NOT_FINAL_HI_BOARD').replace('cp=H/f"inventory/checkpoints/mcu_{v}_b006"','stage="usb_esd_4L_b008" if v=="4L" else "usb_esd_2L_b008_bulk"\n cp=H/"inventory/checkpoints"/stage').replace('archive=R/f"review/inputs/mcu_{v}_b006"','archive=R/"review/inputs"/stage').replace('mcu6_independent_native_review.json','mcu_preservation_after_usb8_independent_review.json')
(R/"review_mcu_preservation_usb8.py").write_text(s,encoding="utf-8")
# Formally rebind return geometry case to accepted 2L snapshot without overwriting first-candidate history.
s=(R/"review_actual_return_corridors.py").read_text(encoding="utf-8").replace('R/"review/inputs/usb_failed2L_normalized.json"','H/"inventory/checkpoints/usb_esd_2L_b008_bulk/normalized.json"').replace('usb_actual_return_corridors_01.json','usb_actual_return_corridors_02.json').replace('"2LfirstUSBcandidatephysicalgeometryvalidbutelectrical/classDRCfailed; final2Lmustrecheck"','"2LformalUSB8bulkcheckpoint; finalwholeboardmustrecheck"')
(R/"review_actual_return_corridors_02.py").write_text(s,encoding="utf-8")
print("scripts ready")
