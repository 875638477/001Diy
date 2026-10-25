import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");note=R.parents[2]/"notes/lessonHI_mcu_20261021.md";s=note.read_text(encoding="utf-8")
s=s.replace('[USB v7](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v7.json)','[USB v8](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v8.json)',1).replace('[GPIO north v3](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/gpio_north_escape_v3.json)','[GPIO north v6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/gpio_north_escape_v6.json)',1)
s=s.replace('USB/GPIO当下为已做实际铜几何预审、待原生验证方案。','USB四层v8已原生保存重开且DRC0，专项实际路径/铜参考已开始独立复核；两层最终及GPIO6仍待原生，详见第12—14节。')
s+="""

## 12. USB8实际路径、局部预算与四层重开（2026-10-22）

USB8修订共享DM主干：四层x40.60、直gap.15，45°弯角错位后最小约.1500179 mm；两层x40.59、gap.16，角部约.1600588 mm。原稿把相同斜向转角放同一y，会把角部间距压窄；正确的offset不能靠“中心距减线宽”一句覆盖所有方向。

此修改让约1.45 mm共享主干真正进入耦合间距范围，原E_USB_FS_BUDGET的**phase1 mm、uncoupled6 mm、maxVia2均保留**。四层原生0DRC证明本次共享DNP路径不再需要放宽6 mm。DNP短支路实际仍有DP1.842359/DM1.542359 mm，不用忽略DNP焊盘消除告警。

连接器这对网单独建立静态副本HI_E_USB_CONNECTOR_4L：phase4 mm、uncoupled13.5 mm、maxVia2。原生pair绑定只在DP_USB_CONNECTOR（USB_DP/USB_DM）；DP_USB_MCU_SIDE仍绑原E_USB_FS_BUDGET。来源与副本读回仅上述两个字段不同，不能视为全局USB预算放宽。首轮原生实际值：四层phase3.2757、uncoupled12.6858/9.4101；两层首轮phase3.2757、uncoupled11.5394/8.2637。数值来自真实分叉路径，4/13.5是带几何余量的教学检查阈值，**不是USB规范时延/不耦合允许值或合规证明**。

四层正式板为native/HI_4L_usb_esd_4L_b008.brd，SHA256=4E4C3AE7C6B8DF95D5E9433DCA4F27FA4261EB3C6DD81269D868FB50FB73DAA9；原生logs/reopen_usb_esd_4L_b008读取0DRC、32指定端点及HSE隔离负测试均通过。该板仍不是整板最终走线，后续普通接口与地铜改变须再次核参考。

[实际USB路径复核](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_native_usb_esd_4L_b008.json)使用原生centerline做分层分网图、相交处拆边、最短端点路径，不访问未经过的叶支路。实测几何重现全部两插向入口、两条2.6 mm U4流通铜、受保护段各4.699357 mm、共享段4.537996/4.910788 mm以及DNP残桩。R11从U4到tee总路径3.053589 mm，不能把总路径当tee本身；实际tee仍约.845 mm。

两层DM竖逃线x39.25到CC1(A5)焊盘只有.25 mm，而两层USB↔USB_AUX全局规则为.50 mm。因此USB8仅在TOP x38.95—39.55、y7.25—8.55的小源端区域，将HI2L_USB_FS_S↔HI2L_USB_AUX_S副本的smdpin_line改.20；其它字段和区外.50不改。四层不随意复制此例外。具体native生效仍以两层最终读回和区内外挑战为准。

## 13. 参考开口与实际可用返回铜：不只算覆盖率

实际shape圆弧、void、GND线与真实逐层via/pin铜合并后，对路径的投影检查发现：两板1.0 mm BOTTOM镜像桥都没有正下方参考平面铜覆盖，因为两个signal-via半径约.6002 mm的反焊盘相交；两条TOP下钻脚末端也各有.6002 mm投影开口。这是有限过孔过渡，不能把TOP地片或四层L3的存在写成“这1 mm为连续微带”。

两层还因BOTTOM VBUS桥，在TOP DP入口产生约1.34262 mm连续投影空缺，约从(40.83337,8.68337)经(41.2,9.05)到(41.2,9.87413)。四层TOP主线参考L2，未被BOTTOM VBUS桥直接切开。两层保护侧宽对/U4流通/共享主路径的中心线在本次几何范围有覆盖；覆盖为0缺口仍不等于阻抗/EMI已证实。

进一步核了实际返回，而不是只报百分比：[可用返回走廊报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_actual_return_corridors_01.json)。

- 镜像区在四层真实L3、两层真实TOP都有完整0.40 mm宽铜走廊。取signal-via南0.9 mm附近点，经y4.9的地带接两枚返回GND via，左路径2.02154 mm、右1.53489 mm；左右返回之间同一0.40 mm地走廊长4.55642 mm，整个buffer缺铜面积0。
- 左返回孔当前(38.15,5.8)到A6 DP via中心1.60 mm，略超本轮1.5 mm布置目标；右孔到B6 via为.95 mm。[左孔微调候选](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_left_return_move_proposal.json)改(38.30,5.8)可至1.45 mm，已全铜/NPTH筛查，无新增交叠；尚未为此单独重建USB8，最终位置按根整合实际读回。
- 两层VBUS底槽左端外，BOTTOM实际存在0.30 mm宽路径：(40.7,8.4)→(39.4,8.4)→(39.4,10.1)→(41.2,10.1)，长4.8 mm且整个buffer缺铜面积0。这提供有限绕行，不能改写成直接投影开口被消除。

这些是**实际存在的几何走廊和长度上界**，不是电磁场求得的最短路径，不表示高频电流必经该折线；起点也不是signal-via电流注入地铜。未进行SI/PI仿真。两层报告目前基于首轮物理铜正确但电气/局部间距失败候选，最终两层必须重核，不能冒作正式最终入口。

## 14. GPIO6功能避让、候选失误与运行时诊断（2026-10-22）

新电源STAR07b BOTTOM对角x+y=62.7，距旧PC14西端(35,28.5)实际只有.165685 mm铜净距。仅比较同y水平距离会漏斜向最近点，是本次预审需纠正的错误。西北换TOP候选随后又占SPI_NSS/SCK/MISO源端x33.5—35.4、y26.5—33.5窄通道；两个候选地via还分别触碰R21/靠近R24，已保留失败v11/v12报告，未执行。候选必须纳入所有组的真实/计划铜，不能局部自洽就交native。

采纳根统一功能分区后，[GPIO6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/gpio_north_escape_v6.json)取消PC14所有西向partial，保留原U1.3内侧TOP扇出及via(41,27.8)，BOTTOM走(41,27.8)→(43.6,25.2)→新signal-via(45.6,25.2)，TOP从东侧绕HSE接J11。新application-GND via=(46.95,24.9)，信号/地孔中心距1.38293 mm；PC13/PC15原BOTTOM出口不变。整合MCU6、USB8、ESD04c、STAR07b及外围3V3 06b后，两板[v13几何报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/combined_v13_copper_screen_4L.json)及[两层报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/combined_v13_copper_screen_2L.json)无异网重叠、普通网无小于.20 mm铜净距；原生仍待完成。

两层此BOTTOM段跨TOP x43供电竖干投影，需要实际TOP地片、近旁GND via与BOTTOM全局铜构成有限返回，不能称统一连续参考；四层实际L3独立处理。信号优先级允许普通GPIO绕行，不能为它穿过HSE/ADC或破坏关键SPI源脚。

Cadence内部在差分重新计算时反复发起bem2d STL场解并失败，虽然MM几何字段仍可读，不能把失败场解当阻抗/时延成果。[只读诊断](../examples/lessonHI_38_50_20261021/engineering_mcu/review/cadence_fieldsolver_readonly_diagnostic.json)保存本机官方文档和可执行文件身份：bem2d/bem2d2/bem2d3都存在且是x64；直接导入DLL在安装bin或System32可找到，未发现显式执行ACL拒绝。但本工具壳which(bem2d)=null、launcher原先未显式补bin到子进程PATH；应先由原生执行者检查实际子进程PATH，不能臆测许可或DLL根因。

官方cmref/analyze.html与ccoms/cchap.html确认length/time两种约束及Z Axis Delay默认关闭；MM长度不含Z解释本次phase数值，却不保证完全不调用内部场解。没找到保留全部diffpair检查同时跳过bem2d的官方开关，未猜变量，也未关闭物理或差分DRC。实际运行时修订与是否解决应以根/原生日志后补。内部场解失败、UI待验、制造及硬件条件继续单列。
"""
note.write_text(s,encoding="utf-8");print(note.stat().st_size)
