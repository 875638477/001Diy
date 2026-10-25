# G阶段电源、接口与装配学习记录（2026-10-20）

范围补充：本文3916项只审 native/G_*_PLACEMENT_v3.brd 布局checkpoint。后续 current/G_*_LAYOUT_v1.brd 的三组MCU局部铜与实际参考面，以[主记录的保存重开结果](lessonG_30_37_20261020.md)为准；本文“无实际铜/只有1颗继承via”的描述仅对应旧checkpoint，不否定后续另存演示。buck、LDO、USB/ESD、HSE及ADC尚无完整已验铜路径的边界仍然保留。

本记录负责第32、34、37课的工程依据、40件电源/接口坐标及两层/四层回流要求。已完成原厂资料核对、原生逐pin映射和布局建议；最终80件原生布局checkpoint已独立通过3916项核验，回流/实际走线仍是后续保持项。这里的距离是焊盘几何下界，不是实际线长、阻抗或EMI验收。

全部产物在 [engineering_power](../examples/lessonG_30_37_20261020/engineering_power/)，核心有 placement_power.json、engineering_checklist.json、readouts/pin_and_geometric_review.json、readouts/final_plan_geometric_review.json。当前40件建议已由root合入全板plan；root调整优先，初版不得覆盖最终native坐标。

## 输入、网络和边界

4层输入F29_CONSTRAINTS_v4 SHA256=18ED6701C902A0918558AB13072290046F88299D73432C6882239919CD3C0233；2层F28_2L_USERFIX SHA256=A8E00C31A0B1D16FCF24972518244580244025164F0898CA760F31AFA559CCFB。80×60mm/四角C2、四个Ø2NPTH，J2(40,3.675)开口−Y、低型区x10..30/y42..52禁止z>=2。

采用DE_CURRENT baseline：9–16V限流隔离台架，3.3V正常负载<=150mA/Ta0..40°C，外接GPIO+headers合计10mA计入该预算。USB_VBUS仅检测和ESD，SWD/headers Vref不得反供电。I2C为2.2kΩ基线，历史ECO不作当前输入。

inventory_4L中80件272逻辑pin与integrated_circuit逐脚比对，127项通过。原点不是body中心：SO8原点在pin1、通用R/C原点多在pin1附近。localXY只施加元件旋转；初始regularPadBBox已含pin局部旋转，只再施加元件旋转；actual导出的pad bbox已含实际全部旋转，只平移到绝对pin位置。不能重复旋转或按绘图视觉猜引脚。NC真实为null；DNP字段为“DNP default USB mode”。解析器曾误判这两项，已修正并留失败候选。

## 第32课：buck、LC和LDO

[TI TPS54202 RevC](https://www.ti.com/lit/ds/symlink/tps54202.pdf) p20–21已渲染阅读。输入换相回路是CIN+→VIN3→内部高侧/SW/低侧→GND1→CIN−，不是L/COUT整个能量回路。U2转270°后GND/SW/VIN在左、FB/EN/BOOT在右。C3是最近100nF，C2是22uF局部储能；C4接BOOT6与SW2，不接地。反馈R1/R2/C7在安静右侧，V5从C5正端滤波后单独取样，R2地Kelvin回U2.1，避免大电流共颈。

当前C3 p1VIN=(26.0984,18.6)、p2GND=(24.5236,18.6)，U2VIN=(24.2,20.05)、GND=(24.2,21.95)。其地路径需近旁地过孔加连续参考平面才能合理；未实走线，不能只用电容中心距离宣称热回路已紧凑。SW到L1约5.18mm Manhattan几何访问距离，BOOT应从U2右/上方绕到SW，不能错误接地。

TI示例使用internal/bottom SW铜。本板四层内层意图连续GND且规则只允许GND进入内层，因此改为TOP短宽SW和独立返回，实际铜面积/回路在走线课验收，不照搬示例层用法。[Coilcraft Doc887](https://www.coilcraft.com/getmedia/ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf) p4已视觉核对：short lead侧为L1.1 BUCK_SW朝U2，land中心距4.04mm，真实max高度6.1mm。电感能力大不解除整板150mA热边界。

[TI TLV755P RevD](https://www.ti.com/lit/ds/symlink/tlv755p.pdf) p21和p44已视觉核对。DBV5为1IN/2GND/3EN/4NC/5OUT，无exposed pad，不复制其他封装中心散热焊盘。C8/C9分别靠输入/输出，公共地短宽。root最终移动LDO组以避SPI；输出C9翻270°可将地脚朝U3，避免原90°地脚朝外。U3真实max1.45mm，库默认1mm不能当物料高度合格依据。

C2有效>=10uF@16V、C5+C6有效>=30uF@5V、C9最坏有效>0.47uF仍需准确MPN/DC-bias/温度/容差核定。最坏LDO耗散约0.284W；JEDEC热阻初估不等于当前PCB热测，器件无反向阻断。C1的11mm仍是教学包络，准确电解型号未选。

## 第34课：接口和保护

[ST DS4260 Rev7](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) 官方文字已核pin/短路径要求。U4是USBLC6-2SC6，1/6同DP、3/4同DM、2地、5VBUS。180°使连接器侧6/4朝下、protected侧1/3朝上；C10就近。ESD路径要短，放电地不绕经MCU地细颈；两路器件不代表CC/SBU全部保护。

J2数据触点在同排交错，需要明确短合并及必要换层。USB默认装R5/R6、DNP R12/R13，CAN反选，四个不能全装；未装焊盘仍是铜枝节。历史22Ω未被证明F103必需，改值需ECO。90Ω是待板厂确认的目标，长度DRC不等于阻抗认证。CC1/CC2各自5.1k，不能合并；USB_VBUS不得接V5/V3V3。

[TI TCAN332 RevF](https://www.ti.com/lit/ds/symlink/tcan332.pdf) p29–30已视觉核对：U5左digital朝MCU、右CANH7/CANL6朝J3。C11先近VCC3、C12邻近，参考平面连接需多过孔降低寄生。R15仅总线物理两端装；家族图中的split端接/其他型号模式脚不属于本电路，不擅增。当前没有验证过的外部CAN TVS/CMC，<=1m/500kbit/s台架；内部ESD额定不等于系统合规。

J1→F1→D1→VIN_PROT的SS14 pin1K/pin2A以[Vishay原厂图](https://www.vishay.com/docs/88746/ss12.pdf)确认。0.5A保险丝不是精密限流器，未配置已验证输入TVS。UART R16初版PA9到焊盘下界6.3545mm超过本课4mm源端访问目标；root改pin1到(37.5,21)后最终plan通过。该目标是工程预算，不是原厂强制mm阈值。

## 第37课：装配和可测试

[GCT USB4105 RevB4](https://gct.co/files/drawings/usb4105.pdf) p1已重新视觉核对。Shell stake S=.95±.15从seating面量到脚尖，不是成品PCB底面突出。.95脚与1.6mm板焊接工艺未匹配，不能宣称装配释放。图示plug max6.5mm和1.85min不代替准确插头包胶/外壳模型。保留前方教学访问区，最终仍需具体机械模型。

4孔2.5mm禁布和低型区保持；螺钉/垫圈/工具/外壳未定，现半径不能证明全部安装件适用。generic电阻/电容/header默认height1mm不证明实际高度。U3/U4真实max1.45、L1max6.1有依据；C1等仍须确切型号。

J9是自定义1x6，非标准ARM键位。pin1/GND/Vref/NRST/BOOT标签、shunt操作、排针插拔和弯线需审查；不虚构统一5mm就够。未新增TP，电容/J1可规划量测但小SMD焊盘不等于制造探针点。USB/晶体/FB/SW不加长测试枝节；电源波形用短地弹簧。温升、纹波、插拔/ESD和CAN实测仍属后续实板验证。

## 两层/四层与未解决项

两层TOP-BOTTOM，BOTTOM尽量连续地，逐条检查被信号切断的回流，换层近GND缝合。四层TOP-L2-L3-BOTTOM，L2/L3功能意图连续GND但尚未全铺铜；GND-only内层规则保留。层名不是铜平面，0DRC不等于SI/PI/EMI合格。

2L OSH公开mask bridge .1016mm与继承USB名义.100mm差异保留；4L板厚/铜厚/有色阻焊条件另核；90Ω及USB板厚脚长未匹配。它们不妨碍隔离教学布局，阻止直接宣称可生产发布。

## 资料、失败与复核

sources/source_manifest.json保存六份本地成功原厂PDF、原路径、SHA256和页码；rendered为实际核图页面。ST官方与备用PDF直链均HTTP567，sources/st_download_retry.json保留失败，没有冒称离线齐全。官方网页文字可读，图形视觉核查不足在此明示。

脚本写入曾因Windows命令过长失败，改分段写入；PowerShell JSON大小写重复键改Python。上述失败未写入Temp/cwd，也不改变工程。最终native专项结果见下节。

## 最终布局checkpoint独立审查（已完成）

正式读回是 logs/reconcile_2L_02 与 logs/reconcile_4L_02，板为 native/G_2L_PLACEMENT_v3.brd 和 native/G_4L_PLACEMENT_v3.brd。结果见 [final_native_power_review.json](../examples/lessonG_30_37_20261020/engineering_power/readouts/final_native_power_review.json)：PASS_INDEPENDENT_POWER_INTERFACE_LAYOUT_REVIEW，3916项、0失败。

不是仅比对归一化表：脚本直接解析原生 g_actual_symbols/g_actual_pins，再与原电路、原始封装inventory、全板80件最终plan以及normalized表交叉验证。覆盖80件位置/旋转/body、272pin网络/坐标/padstack与真实旋转pad bbox、69net、四孔与板框8顶点。checkpoint快照另存本专项目录readouts/layout_checkpoint_actual_2L/4L.json及layout_checkpoint_plan.json，后续去耦demo不得覆盖本次证据。

最终采用U3(27,29)0°、C8(24.2,31)270°、C9(29.8,30.95)270°；C9从90°翻270°改善地返回，但第一次flip使地焊盘靠U3 NC脚间距.1374<.2，root再将x移至29.8解决，最终原生DRC=0。C8曾有.1773<.2，左移.2解决。这说明body bbox无重叠仍不足以替代真实铜焊盘间距。UART R16最终pin1(37.5,21)，PA9到该焊盘几何下界1.7916mm，满足本课提出的4mm布局目标；USB R5/R6到MCU的下界分别3.2816/3.3762mm，仍待实际路径验证。

19组几何下界均在本课布局目标内：C3-VIN约1.1508mm、C3-GND到U2GND约2.6435mm，L1SW焊盘到U2SW约.915mm；这些数是AABB下界，可能穿过障碍，不能称真实线长/热回路通过。输入主电容C2到VIN下界3.55mm。C4两端网络已确认BOOT/SW；R2/FB仍需quiet和Kelvin实现。

该checkpoint无ETCH走线、无实际铺铜，仅继承一个(52,35)的GND通孔，C3地到最近已有GND孔中心约31.9986mm，U2GND约30.7106mm。它们显然不能冒充电源局部回流。因此第32/34课完成的是布局与具体返回方案：后续须在C3负端/U2.1邻近分别布地连接、靠连续地闭合换相回路；LDO、ESD、CAN也要自己的近地连接。后续MCU三回路/参考地演示另存后另加追补，不把它说成buck、ESD已经走通。

第二轮解析发现原始源NC=null、原生actual export为空字符串；仅对空网名做None规范化，不改变任何板上网络。pad bbox按原生实际旋转后bbox平移，不能再重复旋转；初始package bbox已含pin局部旋转，只再叠加元件旋转。已逐272pin×两板验证归一化，不把错误的NC解析当板上错误。

U2高度补证：TPS54202DDCR官方p28 DDC0006A图已渲染视觉核对，max1.1mm；见rendered/tps54202_revC_p28.png。不能套用U3/U4的1.45mm或native默认1mm。

## 全局记录一致性审查（2026-10-20收尾）

已只读核对主G笔记、MCU笔记、本文与learning_plan。网络、供电边界、MPN/高度、板厚脚长、阻焊桥和未布线范围未发现实质冲突。收尾消歧建议已交主任务：L2/L3功能意图与本轮只实际铺L2分开；LDO与ESD段明确写“网络/布局已核、后续铜路径要求”；J7为复位跳帽/排针而非实体按键。MCU作者已确认修正，并将旧双via候选与最终TOP直接VSS-cap返回、单cap侧via接参考面分开记录。图中连通参考面不表示高频返回电流必然经过该面。

本轮全局文字核对不重复认可最终三回路/区域规则；其独立证据由MCU专项与主任务最终原生报告承担。本文的布局3916项仍是固定checkpoint，未用后续演示扩大审查结论。
