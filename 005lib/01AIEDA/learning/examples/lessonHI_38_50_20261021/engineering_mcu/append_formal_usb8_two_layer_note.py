import pathlib,json,re,hashlib,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent;note=R.parents[2]/"notes/lessonHI_mcu_20261021.md"
f=R/"review_mcu_preservation_usb8.py";s=f.read_text(encoding="utf-8").replace("HI wholeboard still remaining112; USB/GPIO laterbatchesnotincluded","HI wholeboard remains unfinished; USB8 included, GPIO6 and laterordinary routes notincluded");f.write_text(s,encoding="utf-8")
j=R/"review/mcu_preservation_after_usb8_independent_review.json";d=json.loads(j.read_text(encoding="utf-8"));d["limitations"][0]="HI wholeboard remains unfinished; USB8 included, GPIO6 and laterordinary routes notincluded";j.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
f=R/"render_usb_reference_actual.py";s=f.read_text(encoding="utf-8").replace('R/"review/inputs/usb_failed2L_normalized.json"','H/"inventory/checkpoints/usb_esd_2L_b008_bulk/normalized.json"').replace("First USB geometry snapshot; final 2L must be rechecked.","Formal USB8 checkpoint; final whole board must be rechecked.").replace("usb_reference_return_actual_01","usb_reference_return_actual_02").replace("White: holes / reference voids.","White: holes / reference voids. Orange: VBUS via pads.")
(R/"render_usb_reference_actual_02.py").write_text(s,encoding="utf-8");exec(compile(s,str(R/"render_usb_reference_actual_02.py"),"exec"))
s=note.read_text(encoding="utf-8").replace("## 5. PC13/14/15实际逃线与参考切换","## 5. PC13/14/15实际逃线与参考切换\n\n本节v3表为旧电源路径检查点的历史预审，已被第14节GPIO6替代；当前PC14西向partial必须取消，不能在STAR07b上重放此表。")
s=s.replace("DM略左.02 mm，实际最紧gap约.167696 mm | 原最紧gap约.153553 mm","最终v8实际最紧gap约.160059 mm | 最终v8角部约.150018 mm")
s+="""

## 15. 两层USB8正式检查点及专项复核补充（2026-10-22）

两层正式板native/HI_2L_usb_esd_2L_b008_bulk.brd，SHA256=90E8AC3413332098A4D86E035E5200B955F8385003D9628C5F396FB2F8161739；新进程logs/reopen_usb_esd_2L_b008_bulk完成32端点、HSE唯一via负测、DRC0/current。独立[两层实际路径](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_native_usb_esd_2L_b008_bulk.json)及[四层实际路径](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_native_usb_esd_4L_b008.json)各18条全部可达；两层保护侧各4.326565 mm，R11真正tee=.395 mm；四层各4.699357 mm、tee=.845 mm。此前计划与实际一致，phase检查仍是平面长度口径。

[MCU/quiet保持复核](../examples/lessonHI_38_50_20261021/engineering_mcu/review/mcu_preservation_after_usb8_independent_review.json)在USB8后两板各41项再通过。两层bulk优化只在成组操作/导电图试验时暂缓更新，wrapper明确恢复drcEnable，再axlDRCUpdate(t)，再导出当前0DRC；HSE图恢复日志先写FULL_DRC_REQUIRED，不能把这个中途状态本身当0DRC。

受控电气规则挑战：把connector phase4临时收紧至3 mm，原生报实际3.2757；把共享pair uncoupled6临时收紧至1 mm，报4.9931/4.9204；恢复两份各自4/13.5与1/6后DRC0。差分规则确实工作，共享预算未为DNP长枝而放宽。当前2L via pad层表按实际crosssection过滤为TOP/BOTTOM，原raw内非存在层查询仍保留，避免静默抹历史。

正式[返回走廊02报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_actual_return_corridors_02.json)已改绑定正式两板，几何结论与首轮相同：镜像区0.40 mm实际地走廊存在，2L VBUS底槽可用0.30 mm绕左端地走廊存在，直接投影开口保留。真实图见[参考/返回预览02](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_reference_return_actual_02.png)和[SVG](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_reference_return_actual_02.svg)。图表示实际铜和可用路径，不是电流仿真；整板后续铺铜变化还要再核。

子进程PATH已由原生执行者实测纠正：bem2d解析从null变为安装bin中的bem2d.EXE，只影响该子进程，无系统/用户PATH修改。纠正后内部STL场解仍反复失败，故PATH问题只是已验证的一个启动环境问题，**不是已经解决全部场解失败或已找到唯一根因**。没有使用失败场解数值作SI/时延验收。

GPIO6候选TOP参考片与既定application-ground moat有部分重叠；原生执行者采用原moat多边形做实际差集，保留原候选/差集/SHA，并继承HSE单anchor负测。即便不直接碰quiet via，也不能把应用地偷偷铺进已声明moat。当前GPIO6及后续普通接口/最终整板审查未因USB8检查点而自动通过。
"""
note.write_text(s,encoding="utf-8")
bad=[]
for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)",s):
 target=m.group(1)
 if re.match(r"https?://",target):continue
 p=(note.parent/target.split("#")[0]).resolve()
 if not p.exists():bad.append({"link":target,"resolved":str(p)})
report={"date":datetime.datetime.now().astimezone().isoformat(),"note":str(note),"sha256":hashlib.sha256(note.read_bytes()).hexdigest(),"brokenLinks":bad,"count":len(re.findall(r"\[[^\]]*\]\(([^)]+)\)",s))}
(R/"review/note_link_check.json").write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps({"noteBytes":note.stat().st_size,"brokenLinks":bad},ensure_ascii=True))
