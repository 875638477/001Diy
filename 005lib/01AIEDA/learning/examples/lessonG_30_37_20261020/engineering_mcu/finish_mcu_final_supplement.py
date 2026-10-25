import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu")
note=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\notes\lessonG_mcu_20261020.md")
t=note.read_text(encoding="utf-8-sig")
marker="## 9. 最终入口实铜、局部例外与独立复核"
if marker in t:t=t[:t.index(marker)].rstrip()+"\n\n"
header="**当前状态（2026-10-21补验）：** 第8节的reconcile02是无局部铜的历史布局快照；当前两板已包含三对VDD/VSS实铜、C16支路及实际参考地铜，最终新进程重开与区域挑战已通过本子任务第9节专项复核。HSE/ADC仍是布局与走廊预审，完整布线和制造/硬件验收仍待后课。\n\n"
if header not in t:
    before="所有新增PDF、渲染、脚本、候选和记录均在"
    t=t.replace(before,header+before,1)
t=t.replace("cap.1→短本层铜→MCU VDD→芯片内部负载→该对VSS→近旁GND via→**实际连续GND铜**→cap GND via→cap.2，才是完整回路模型。芯片内部路径不可从PCB求得；需要时报告的是外部几何/投影/高度代理，不能给一个凭中心距算出的“真实总电感”。","本表是候选阶段的双地过孔方案：cap.1→短本层铜→MCU VDD→芯片内部负载→该对VSS→近旁GND via→实际连续GND铜→cap GND via→cap.2，是一种完整外部返回路径模型。最终第9节改为VSS到cap.2直接TOP返回、cap侧单过孔支接地平面；高频局部回流不必经平面。芯片内部路径不可从PCB求得；需要时报告的是外部几何/投影/高度代理，不能给一个凭中心距算出的“真实总电感”。")
t=t.replace("4. 原生铺铜后检查两个过孔落在同一连通GND区域、无孤岛/长热焊盘颈/被其他铜间隙隔断；仅创建未铺铜shape或画了参考矩形均不成立。","4. 若采用本节双地过孔候选，原生铺铜后须检查两个过孔落在同一连通GND区域、无孤岛/长热焊盘颈/被其他铜间隙隔断；最终单过孔加本层返回方案按第9节真实拓扑核验。仅创建未铺铜shape或画了参考矩形均不成立。")
t=t.replace("本子任务尚未产生上述实际铜。主任务计划保留三对真实局部演示；未收到原生证据前，本笔记只把它们标为待验方案。","截至本节候选阶段，本子任务尚未收到上述实际铜；当时只将其标为待验方案。后续实铜采用第9节记载的拓扑和局部规则，已用最终新进程读回复核。")
t=t.replace("尚待单列局部铜/过孔/实际地平面读回、三对去耦真实连通与短颈/最小区域规则，HSE/ADC仍为布局及走廊预审。","局部铜/过孔/实际地平面读回、三对去耦真实连通与短颈/区域规则已在第9节单列完成，HSE/ADC仍为布局及走廊预审。")
append="""
## 9. 最终入口实铜、局部例外与独立复核（2026-10-21）

当前两份入口是[current四层板](../examples/lessonG_30_37_20261020/current/G_4L_LAYOUT_v1.brd)与[current两层板](../examples/lessonG_30_37_20261020/current/G_2L_LAYOUT_v1.brd)。它们与第8节PLACEMENT/reconcile02快照身份不同，已经加入本节的局部导体。原生执行由主任务原生代理完成，本子任务没有启动Cadence，而是独立比较最终只读重开产物、真实线段、规则字段与挑战记录；详见[最终MCU专项复核JSON](../examples/lessonG_30_37_20261020/engineering_mcu/local_copper_independent_final_review.json)及[复核脚本](../examples/lessonG_30_37_20261020/engineering_mcu/review_mcu_final_copper.py)。

| 项目 | 四层最终入口 | 两层最终入口 |
| --- | --- | --- |
| SHA256 | 2D4A146A61F92AE6459C9E855AB086ED47B42360409608D8A12E30BB7EA21526 | FC411A509940E8727A8CB62D036324D1A63A60E042F9CC8AEAECE10C0425BE7D |
| 最终新进程证据 | logs/final_reopen_4L_01 | logs/final_reopen_2L_01 |
| 真实参考铜 | ETCH/L2，GND，已填充/生成且非过期 | ETCH/BOTTOM，GND，已填充/生成且非过期 |
| 原生状态 | DYNAMIC_OOD=0、当前DRC=0、只读前后板hash相同 | DYNAMIC_OOD=0、当前DRC=0、只读前后板hash相同 |
| MCU专项独立检查 | 19项通过 | 19项通过 |

本组24件的实际角度、原点、PlaceBound以及96个逻辑pin的网络/坐标/铜bbox，与已复核的reconcile02归档一致；因此加入局部实铜没有悄悄改变MCU候选的整合布局。原生包含80件、69网络；全板80件/272逻辑脚/机械等完整保持核验由主任务独立总报告负责。

**三对回路的实际拓扑。** U1.24→C13.1、U1.36→C14.1、U1.48→C15.1分别有TOP短支路；相应U1.23/.35/.47经TOP直接接各自电容2脚。电容地侧各有一颗GND过孔，在(32.45,25.2748)、(42.3252,19.35)、(47.45,28.7252)，真实支接上述参考地铜；加上继承的(52,35)为**3颗新增+1颗继承，共4颗**。第4/8节的“两侧/两个GND过孔”是原候选，最终没有新增MCU侧地过孔。局部高频cap→VDD→芯片→VSS→cap回流以直接TOP返回为主；原生导电图证明其还连接实际地铜，不能据此说高频电流必经平面。第6节介质高度比较只是不同参考路径的几何背景，不能代替此直接TOP回路的电感测量。

**C16支路已实做。** C15.1(46.5,30.3)到C16.1(49.5,30.3)为0.60mm宽支路；C16.2(49.5,28.268)通过三段0.60mm铜接到现有C15地侧过孔节点(47.45,28.7252)，再通过保留TOP铜接C15.2。这使C16附着于VDD3/p48这一组，符合本电路bulk分支意图，不是把其他两颗100nF串成共用长细供电尾巴。原生最终导电图8个指定目标全部可达（六条pin-cap及C16两支路），并有四条到实际参考铜的可达记录（三个VSS和C15地节点）。这并未认证C16的直流偏压/容差后有效容量已满足原厂至少4.7µF；采购与硬件仍需补验。

**实际线段与短颈口径。** 两板最终TOP均27段局部铜（11段V3V3、16段GND），与独立构造的六条原回路23段加C16四段完全一致；参考层还有64段GND热焊盘生成铜，总91段不能全说成人工布线。三对VDD/VSS共六条细脚脱出，每条从pin中心轴向0.8mm后以(0.4,0.4)斜向脱出，总原生颈长1.365685mm；首段其中0.6000mm位于pad内，外部细颈约0.765685mm。pin中心起线才在原生getconnect图中真实附着；从pad内偏移点起线的早期试验没有附着，不可只靠几何相碰称连接。**整段1.365685mm并不满足原全局1.0mm上限**；最终明确采用下述1.4mm局部工程例外，不用扣掉pad重叠量伪装原规则通过。

**区域与规则的准确范围。** G31_U1_ESCAPE是**一个region group含三个TOP矩形**，不是三个分别命名的region：

- x34.2—36.5、y23.5—25.5。
- x41.5—43.5、y21.2—23.5。
- x43.5—45.8、y28.5—30.5。

本次六个V3V3/GND供电脚锚点正好为U1.23/.24/.35/.36/.47/.48；范围内也有邻近普通信号脚，实际规则要由Region-Class匹配及既有Class-Class优先级决定，区域不是对所有网络豁免。4层NC_POWER_LV_P与独立GND物理类G31_GND_P分别绑定G31_POWER_ESCAPE/G31_GND_ESCAPE；2层使用自己的G31_POWER_P/G31_GND_P及两层原规则。局部物理CSet由对应P_POWER_060/P_GND_PLANE或G2L_POWER_DEMO/G2L_GND_DEMO复制，逐层字段比较仅necklength_max由1.0改1.4；0.60普通宽、0.25最小细颈、允许过孔和层权限均保持。4层另将NC_POWER_LV_S在此TOP区域绑定G31_PIN_ESCAPE，仅smdpin_line/line_line由0.30改0.20mm，其他via/孔间距字段与S_POWER_030一致。全局原规则仍为1.0mm及原间距；现行4层**非GND信号**内层布线仍禁止，GND实际参考铜权限保持。

这里的“对应原规则/parent”表示创建时复制的来源，**不是实时父子继承**。后续修改原CSet必须重新比较并同步相关局部副本；不能假定局部例外会自动追随。尽管副本里各层字段由API写入，实际region几何只在TOP，不能将其理解为全层区域放宽。

**规则确实生效的受控挑战。** [四层挑战日志](../examples/lessonG_30_37_20261020/logs/freeze_4L_02/local_rule_challenges.txt)与[两层挑战日志](../examples/lessonG_30_37_20261020/logs/freeze_2L_02/local_rule_challenges.txt)保存原始细节，不只保存一个0DRC结论。

| 挑战 | 四层 | 两层 |
| --- | --- | --- |
| 原始局部规则 | 0，当前 | 0，当前 |
| 局部间距恢复0.30mm | 30条错误 | 不适用，两层原间距独立为0.20mm |
| 局部max neck恢复1.0mm | 12条，报告实际1.3657mm | 12条，报告实际1.3657mm |
| 区外临时coupon：1.2mm细颈及近邻铜 | 13条；原P_POWER_060的1mm与S_POWER_030线间距均报错 | 9条；原G2L_POWER_DEMO的1mm与两层间距均报错 |
| 回退挑战 | 0，当前 | 0，当前 |

错误条数包含重复落点及其他故意过近的via/线，不能把13/9全归为neck错误。日志中分别有一条区外Maximum Neck Length与一条Line to Line Spacing明确指向原规则，足以证明局部例外未扩到区外。挑战不保存；最终新进程读回没有区外coupon，仍只有上述27段TOP铜与4颗真实GND过孔，hash前后不变。

**本节通过的限度。** 第31课三对VDD去耦及VDD3 bulk支路的指定真实连接、参考地支接、明确短颈例外和生效范围已获得原生读回及独立复核。HSE/ADC/VBAT/复位及其他网络没有因此自动布完；AN2867的局部振荡器安静地、壳体与负载cap不同物理返回、护环等仍只在布局预审/后续计划。还需继续实际细脚扇出、参考连续性、全部走线与未连接审查、晶振启动/驱动/ADC采样和接口硬件验证；本结果不表示完整PI/SI/EMI、90Ω、GUI已掌握或制造放行。
"""
t=t.rstrip()+"\n\n"+append.strip()+"\n"
note.write_text(t,encoding="utf-8")
p=R/"refresh_mcu_manifest.py";s=p.read_text(encoding="utf-8-sig")
s=s.replace('COMPLETE_SOURCE_AND_NATIVE_MCU_LAYOUT_REVIEW_ROUTING_PENDING','COMPLETE_MCU_LAYOUT_AND_LOCAL_COPPER_REVIEW_FULL_BOARD_ROUTING_PENDING')
p.write_text(s,encoding="utf-8")
print("Final MCU note section 9 written.")
