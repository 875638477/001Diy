# H/I 第38—50课：MCU、振荡器、复位、ADC与USB路由专项

日期：2026-10-21（Asia/Shanghai）。所有资料、脚本、候选、失败和审查均在01AIEDA。本笔记是合并课程的工程子记录；课程总状态由根笔记/索引逐项验收，不能凭本专项宣布13课全部完成。

## 当前入口与证据身份

本次从G阶段冻结的80器件、272逻辑脚、69网络、80×60 mm教学板继续；J2板边、四安装孔与机械基准保持。基线供电去耦已有三组TOP真实闭环及C16支路，不把它们重新当未布线空气线。输入版本和原厂PDF身份见[输入清单](../examples/lessonHI_38_50_20261021/engineering_mcu/input_manifest.json)。

本专项负责工程路由方案及原生导出后的独立几何/返回审查；**没有启动Cadence**。所有原生操作由合并课程的原生执行者完成。桌面控制/GUI逐段拖线未在本轮获得证据；官方SKILL精确建线、事务、DRC、导电图、保存重开应分别记录，不能称GUI已掌握。

当前冻结候选为[MCU v6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/mcu_critical_routes_v6.json)、[USB v8](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v8.json)与[GPIO north v6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/gpio_north_escape_v6.json)。v1—v5等旧稿保留作过程证据，不能直接重放。MCU v5原生两板的32指定端点和HSE隔离挑战已由原生执行者报告成功，但存在两条真实间距错误，故不能把v5称最终通过；v6只做对应最小修正，其原生新进程读回和独立82项专项检查已通过，详见第11节。USB四层v8已原生保存重开且DRC0，专项实际路径/铜参考已开始独立复核；两层最终及GPIO6仍待原生，详见第12—14节。

[组合v8四层几何报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/combined_v8_copper_screen_4L.json)及[两层报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/combined_v8_copper_screen_2L.json)使用当前原生实际铜、所有真实焊盘、过孔，以及power03b、MCU6、USB6、GPIO3和ESD04c改点候选一起筛查。两板无异网铜重叠；除USB两根本身的耦合间距外，普通不同网络不小于0.20 mm。该几何筛查**不等于原生DRC或参考连续性验收**，也没有代替Class-Class/Region-Class优先级与制造检查。

## 1. 原厂依据与使用条件

| 来源 | 本轮核对内容 | 使用边界 |
| --- | --- | --- |
| [ST DS5319，STM32F103C8](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf)，继承Rev20/2025-07 | 48脚映射、实际供电脚、HSE/ADC/NRST、USB表46 | 具体封装与电压/负载条件一起用，器件数据不等于本板认证 |
| [ST AN2586](https://www.st.com/resource/en/application_note/cd00164185-getting-started-with-stm32f10xxx-hardware-development-stmicroelectronics.pdf)，Rev8/2022-12 | 每VDD对100nF及储能电容、分区、真正返回回路 | 不把器件中心距离当回路电感或固定万能距离 |
| [ST AN2867](https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf)，Rev24/2026-02，PDF第45—47页 | 独立振荡器下方地、最近MCU地连接、金属壳与振荡地分开、示例条件 | 统一L2 GND不能自动满足这些局部要求；必须按实际铜验证 |
| [ST AN2834](https://www.st.com/resource/en/application_note/an2834-how-to-optimize-the-adc-accuracy-in-the-stm32-mcus-stmicroelectronics.pdf)，Rev10/2024-10 | ADC源阻抗、采样、敏感模拟/数字返回及分区条件 | 文档确实讨论模拟/数字分地/星形；本板同GND分区是具体工程选择，不能改写成ST一律禁止分地 |
| [Abracon ABM3B](https://abracon.com/Resonators/abm3b.pdf)，继承RevU/2024-08 | pin1/3谐振端，2/4壳；5×3.2、最大高1.1 mm | 负载/起振/驱动需按选定料号与杂散条件，未靠布线证明 |
| [ST USBLC6-2 DS4260](https://www.st.com/resource/en/datasheet/usblc6-2.pdf)，Rev7/2021-12 | PDF1/6页：1/6为同通道，3/4为另一通道，2为GND、5为VBUS；ESD物理布局 | 仍画真实PCB流通铜；芯片内部通路不拿来假装板上连通，器件ESD等级不代表系统等级 |
| [TI SLVA531A](https://www.ti.com/lit/an/slva531a/slva531a.pdf)，PDF15页 | 直线边耦合microstrip近似公式 | 仅分析前估算，无焊阻、蚀刻、铜粗糙度、邻地、过孔/焊盘/弯角建模，不是阻抗认证 |

已下载原PDF/提取文本，TI公式和USBLC6原理/布局页已渲染并目视。资料本地入口与SHA在输入清单；不能只凭网页摘要编造图号/规则。AN2867沿用完整条件，没有从一句“短”推出统一长度上限。

## 2. 实际MCU引脚与优先次序

U1=STM32F103C8T6，(40,27)、270°，native实际焊盘变换已由G阶段读回。三对VDD/VSS为24/23、36/35、48/47；VBAT=1，VDDA/VSSA=9/8。该型号无VCAP引脚，不造裸露地焊盘。

| 功能 | 实际脚/坐标（mm） | 路径处理 |
| --- | --- | --- |
| HSE IN | U1.5=(40.75,31.25) | TOP短路到Y1.1，负载C22回专用quiet地 |
| HSE OUT | U1.6=(40.25,31.25) | TOP先到R31.1，R31.2至Y1.3/C23 |
| 复位 | U1.7=(39.75,31.25) | C21朝脚端翻转，主线与VDDA/OSC分开；R27/J7/J9服务支路后续接续 |
| VSSA/VDDA | U1.8=(39.25,31.25)；.9=(38.75,31.25) | VDDA先接近端100nF，独立GND返回；不把数字负载串在滤波后 |
| ADC0 | U1.10=(38.25,31.25) | C24近MCU，R32朝外部输入；主ADC路径保持TOP |
| USB DM/DP | U1.32=(40.75,22.75)；.33=(41.25,22.75) | 面向下边USB的真实直出，细脚局部间距例外有范围 |
| GPIO PC13/14/15 | .2=(42.25,31.25)、.3=(41.75,31.25)、.4=(41.25,31.25) | 先向封装内侧、离开焊盘后换BOTTOM向西，避免向北跨HSE |

优先保护已存在的三VDD去耦闭环、HSE局部地、ADC本层路径、USB实际过流/参考。普通GPIO从明确出口接续，避免自动寻路穿过保留区。内部3V3星形由电源组制定：TOP y24母线/x43竖干；GPIO扇出用x≤42.35一侧避让，不能仅比较封装原点。

## 3. HSE路径、局部地与真实单点连接

Y1=(43.2,35.7)、90°。主IN是U1.5→(40.75,32.3)→(43,32.3)→Y1.1(44.4,33.7)，.20 mm。OUT是U1.6→R31.1(40.2,33.2)，R31.2(40.2,34.7748)再沿x40.3向北到Y1.3(42,37.7)，C23从此节点短接。x40.3偏置是在实际NRST电容铜边审查后采用，不能按PlaceBound看无交叠就说净距通过。

C22/C23地采用真实quiet铜，2L在BOTTOM、4L在L2。island与application-ground void的**精确多边形**在MCU6的oscillatorReference；外围最小几何moat=0.35 mm。TOP guard并非闭合环，北侧x42.2—44.2有壳地出口，守卫、负载cap与下面island相连。两颗负载cap侧via分别(47.1,35.5748)、(37.7,37.7)。

最终规划唯一接点是**quiet anchor through-via=(45.45,28.85)**，在保留的U1.VSS47→C15.GND真实TOP线拐点上。既有C15 application-GND via=(47.45,28.7252)不删除；没有另画一条TOP线横跨VDD支路去接地。anchor的所有非quiet参考层铜焊盘均需实际void，不能因网络也叫GND就自动短入全板L3/BOTTOM。

与该anchor最近的异网实际铜：U1.46焊盘约0.3000 mm、保留VDD拐角铜约0.559923 mm。这个数比较的是真实pad/line/via，而非器件中心。局部stem在MCU供电脚投影附近有明确有限的源脚交互，不宣称整个island上方绝无其他铜。

Y1.2/.4金属壳通过TOP application-GND路径汇至(43.2,40.8)独立via，位于quiet void外；不把壳端自动并入负载电容的振荡地。局部guard与壳返回相互留空。AN2867条件必须由真实多边形、所有through-via层焊盘与导电图共同验证。

**受控负测试验收**：删除唯一anchor via，C22.2、C23.2、local island、三个guard末端仍应互连，但全部不达全局GND/VSS47/壳；壳与VSS47/C15/global仍应互连。恢复via、重铺、DRC、保存、换进程重开。原生执行者已报告v5两板该测试成立；正式独立复核仍需逐项读原始日志和最后版本，不能只引用一句PASS。

晶体CL、实际杂散电容、起振裕量/驱动、温漂仍待硬件；16pF负载电容并非统一推荐值。专用铜的实现也不证明电磁场完全隔离。

## 4. ADC、模拟供电、复位与细脚例外

VDDA主路由U1.9到C18.1，前段.25 mm细颈、随后.60 mm；100nF近脚，后续C19/C20和R26滤波供电顺序完整，不把高di/dt开关回路经过这组返回。VSSA先向MCU内侧，via=(38.7,29.5)，避开GPIO和星形3V3。C18/C19/C20/C24/C21各有明确application-GND返回via，不借用quiet island。

本轮小范围布局修正：
- C21=(39.478,36.25)、180°，NRST端向右、地端向左；这是翻转端点，并非新增电路。
- C24=(34.8,32.8984)、90°，为VDDA粗铜留走廊。
- R23=(32.9,33.02)、180°，原理图作用/网络不变；y增加.02 mm只为避原生POWER.3间距边界。
- R23/C21等PlaceBound仅为教学放置包围框，~0.10 mm框间距不能称真实零件body余量；实际料号/贴装条件另验。

ADC0：U1.10→(38.25,32.2)→(37.8,32.2)→(37.7,32.3)→(35.5,32.3)→C24.1(34.8,33)→R32.2。只在离开北部细脚区域时抬高.10 mm，不把近端整段抬高去挤VDDA斜向.60铜。外部J10.1(26.27,34)→(29.8,34)→R32.1。电源组原预滤波3V3 x28.4竖支路会穿这条ADC输入，已改03b从x22绕J10西侧，不为供电方便而把ADC放BOTTOM切地。

NRST主路沿x39.35位于VDDA东侧，接C21.1(39.3764,36.25)；(38.7,35.3)服务via给后续R27/J7/J9分支接续。J7是复位跳帽/连接器，不是实体按键。复位/BOOT时序与外部干扰仍待硬件。

ADC使用条件沿用教学需求：0—3 V、≤1 Hz、源阻抗≤1kΩ，含串R后按2kΩ前提核采样；ADC12MHz/71.5周期/100Sps。1kΩ与100nF的极点约796—1592Hz（含源阻抗范围），并不是已覆盖50Hz奈奎斯特界限的100Sps完整抗混叠滤波，也不提供外部过压保护。未实测ADC精度。

U1 .5 mm节距细脚，.30 mm焊盘加.20 mm线的邻脚净距只有.25 mm；POWER/ANALOG/OSC全局.30及USB-普通数字全局.50在此无解。采用明确**TOP局部Region-Class/Region-Class-Class静态CSet副本**，只改必要源脚smdpin_line/line_line至.20，离开区域恢复原全局值；保留via、hole、普通线宽/层权限。实际原生API字段、规则优先级、区域内外挑战和版本必须由最终报告绑定。所谓parent是创建时复制的来源，不是动态继承；不全局改规则来掩盖违规。

## 5. PC13/14/15实际逃线与参考切换

本节v3表为旧电源路径检查点的历史预审，已被第14节GPIO6替代；当前PC14西向partial必须取消，不能在STAR07b上重放此表。

GPIO3是独立可执行文件，替代MCU旧稿内所有描述性GPIO建议。三脚先沿TOP向封装内侧轴向走，等完全离开相邻OSC焊盘再西偏；不使用via-in-pad，也不把整个MCU body粗暴设成禁布从而拒绝合理内侧扇出。

| 网络 | 信号via | BOTTOM接续终点 |
| --- | --- | --- |
| PC13 | (42,28.9) | (35.8,31.1) |
| PC14 | (41,27.8) | (35,28.5) |
| PC15 | (40.3,28.9) | (35.4,30.3) |

两枚application-GND return via=(42,27.9)/(39.8,27.3)，x43电源竖干、既有VSSA路径及相互交叉已纳入整合筛查。这里仍是局部扇出：不代表三条网已通到所有header，后段由根接续。

4L BOTTOM信号需要真实L3 GND，不能只说“L3将铺地”；2L BOTTOM扇出需要实际TOP应用地作为参考。候选TOP ground patch在MCU内部会受供电母线、SMD引脚、其它fanout挖空，因此矩形定义和两个return via不能证明参考连续：需读实际filled polygons与void，量化最长开口/颈缩，必要时重布或加近旁返回。所有GPIO避开HSE island/guard投影，不穿quiet moat。

## 6. USB真实接点、保护、DNP支路与换层

J2并非两根简单相邻信号：y7.355处从左到右DM B7(x39.25)、DP A6(39.75)、DM A7(40.25)、DP B6(40.75)。直接TOP把两个DP和两个DM横向相并必交叉，不能用网络名一样或软件PIN_SHORT跳过。

方案采用DP A6/B6各TOP下到y5.8的through-via，BOTTOM仅1.0 mm短镜像桥；DM A7/B7在TOP y8.6直接相汇。两信号via在连接器金属壳投影内，要求实际两面阻焊不出开窗，并检查Artworks drawMissingPadApertures。padstack NULL mask字段本身不是tented制造证明；必要的新pad只建HI私有库并明确approved-via，不修改公共库。

U4北移到(40.25,11.4)、180°，输入DP6/DM4在y10.1，输出DP1/DM3在y12.7，避免原U4和J2铜尖只差.22 mm而无真实保护/回流走廊。**实际TOP铜**DP6↔1、DM4↔3沿两列直通；不假设芯片内部导体已让PCB两分量自动消失。U4.GND2的.60 mm短泄放经(40.25,11.8)到两枚application-GND via；C10.VBUS旁另两地via。器件SOT23内无EP，体下offpad via仍需真实钻孔/焊阻和装配核验。

VBUS必须越过U4 DP列，电源组ESD04b旧左via=(40,8.95)与DM y8.6横段实际短路，已否决。新候选=(40.25,9.3)，U4.5沿TOP .40 mm直下，再BOTTOM到(43.8,9.2016)，回TOP接C10.1。新via到DM桥净距=.30 mm，整合铜筛查无交叠；own-VBUS-pad铜环相搭、钻孔offpad的mask/装配条件仍单列。2L此BOTTOM VBUS桥会在TOP数据下方形成局部参考缺口，必须用实际地铜/近旁ESD返回量化；4L TOP数据看L2，不因此受BOTTOM桥直接割开，但BOTTOM桥本身参考L3仍要真实铜。

R5移至(41.1,18.5)，R6保留(39.4,18.5)。R12/R13 DNP CAN支路分别从共享端短接，不让USB主路径经过DNP电阻；DNP只是不装电阻，**PCB铜/焊盘stub仍存在**。候选共享stub约DP1.84236 mm、DM1.54236 mm，后续实际native图再核，不能称stub=0。

R11移到(42.9764,14.6)、180°，DP端(41.3,14.6)，源端(42.8748,14.6)。.94 mm宽0603焊盘不能直接压在4L中心距.41 mm的紧耦合对上，否则碰DM；采用紧邻主DP的短tee：4L .845 mm，2L .395 mm，源侧到Q2可稍远，不把长USB数据支路留在原坐标。

## 7. 两层与四层的真实几何差别

| 项目 | 两层 | 四层 |
| --- | --- | --- |
| 层名/主TOP参考 | TOP-BOTTOM，BOTTOM实际GND | TOP-L2-L3-BOTTOM，L2实际GND |
| 材料前提 | core H=1.524 mm、T=.0356、Er=4.5（来源10MHz条件） | TOP-L2 H=.2104、T=.035、Er=4.4（公开频率条件不全） |
| 受保护侧主宽对 | w1.15/gap.16 mm，从y14.2延到R5/R6 USB pad2，中心线约2.70437 mm | w.26/gap.15 mm，局部两段fanout与直耦合段 |
| TI公式直线估算 | 约91.36Ω | 约89.96Ω |
| MCU共享对角部 | 最终v8实际最紧gap约.160059 mm | 最终v8角部约.150018 mm |
| BOTTOM短桥参考 | TOP实际接地片、信号过孔反焊盘/开口逐一查 | L3实际GND及邻近返回via逐一查 |
| 不连续处 | U4窄端口、pad/via/弯角、VBUS底桥及连接器镜像 | 同样存在端口、器件与镜像过孔，不是全路径同阻抗 |

[估算JSON](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_impedance_estimate.json)完整保留公式、单位、未建模因素与否决案例。曾使用2L gap.15 mm，小于所选OSH公开最小.1524 mm，不能忽略2.4µm差值；现用.16重算。四层.15来自独立工艺，不能不分层叠统一改。

公式约90Ω仅适用于上述假设的直线段，没有涵盖整条线路。2L仍有U4约1.62 mm窄端口以及连接器/MCU窄线；4L .26/.15也有局部不耦合扇出、焊阻/同层地影响。板厂受控阻抗与真实公差尚未确认，本板不标90Ω已实现。

## 8. 两插向路径预算与匹配取舍

以共同汇合节点分段，不能把未经过的B7叶支路来回计入A7路径。候选几何：
- B插向J2.B6→U4.6=2.931396 mm；B7→U4.4=2.765711 mm，DP-DM=.165685 mm。
- A插向A6→U4.6平面=7.041396 mm；A7→U4.4=3.765711 mm，平面差3.275685 mm；DP另有2个贯穿barrel。
- U4流通PCB铜两边均2.6 mm、后续受保护段对称，候选共享MCU侧DP4.537996/DM4.910788，差−.372792 mm。两层DM微调保持此总长度；两插向全平面差分别−.207107/2.902893 mm，R5/R6器件内部传播不作为铜线长度。

以εeff=2.8—3.5作传播数量级，3.275685 mm约18.3—20.4 ps；2个全厚贯穿barrel用Er4.5/实际铜介质总厚估约22.4—22.6 ps。A插向入口合计估约40.7—43.0 ps，整条数据路径含共享侧估约38.7—40.7 ps。该估算不是仿真或USB允许偏差规范。MCU DS5319表46所列4—20 ns上升/下降时间有CL50pF等条件、设计保证/非逐片测试，USB FS12Mbps的83.3ns位周期也不是板上phase许可。

原稿为“1 mm预算”在DM刻意绕U形，虽数值匹配，却把连接器下面TOP地挤出狭窄口袋，返回更差，已否决。最终优先保留最短DP镜像桥+DM直汇，并对**仅USB_DP/USB_DM这对PCB网络**建立有实际路径/过孔口径依据的phase预算副本；MCU共享对原预算不一起放宽，最大via/其它字段不顺手改。最终API phase是否计barrel、实际total/uncoupled必须以原生计算为准，不能用候选中心线替代native电气字段。

## 9. 本轮错误与避免再次发生

1. anchor早稿(43,29.25)撞新3V3星形，次稿(45.45,30.1)几乎与保留VDD拐角重合。最初审查只重视pad/PlaceBound，漏实际旧铜，是本专项失误；原生执行前由同组发现。以后所有via/移动必须核所有已有及候选线、via、pad、shape。
2. ADC整段从y32.2升32.3会挤VDDA粗斜线；即使能修一条DRC，也可能制造另一处错误。最终只在源脚区域出口分段抬高，先全铜复核再提交原生。
3. VBUS04b通过器件/输入列几何，却漏DM y8.6横向合并段，产生真实via短路；没有执行该候选。改点后重新合并所有USB/ESD铜，不能只看单组。
4. USB A7旧候选长度错误计入未经过的B7支路来回，现按共同节点最短路径改正。PCB执行不曾依赖错值，最终仍以native实际导电图为准。
5. PC15过早45°向西，和OSC_IN pad仅约.006 mm；后稿又接近VSSA及彼此底线交叉，均保留失败报告。现先轴向走到邻pad下方再转。
6. 所选2L .15 mm间距与公开.1524下限矛盾，改.16；共享45°角实际.153553虽勉强高于公开最小，仍低于本轮.16规则，单独修成.167696而非豁免。
7. 旧PowerShell stdin管道使中文路径编码成问号、一次候选脚本缺失字典键，属于构建失败，未生成CAD变更。脚本改UTF-8文件、失败原件/运行输出保留，不把退出0单独当课程成功。

## 10. 后续原生验收清单与课程对应

38/39：逐段真实pin中心附着、线宽/转角/过孔读回、改线可回退；GPIO/敏感脚拥塞按实际铜解决。40由电源组主审，保留MCU去耦闭环和供电星形，不仅看V3V3连通。41/42：actual dynamic shape、quiet/application铜隔离、唯一via负测试、ADC/NRST/晶振真实路径。43/49：USB两插向/分叉/实际差分几何/端口/phase预算有明确依据。44根完成普通接口接续，并避已定义关键走廊。45/50必须全板连通、当前DRC、实际返回三方面共同核验；本专项局部完成不代替整板结果。46—48必须分别看4L真实L2/L3、2L TOP/BOTTOM，覆盖参考开口、层切换与返回，不从同XY推同质量。

最终应追加：两板BRD和normalized身份/只读前后SHA、每个关键端点实际导电路径、所有via逐层pad/真实shape、最长参考缺口/替代返回、局部规则内外挑战与恢复、两插向实际长度/phase/uncoupled、DNP stub/上拉tee、与预案差异、完整性边界。全板制造、EMI辐射、起振/ADC/USB实测和GUI均独立待验；DRC=0不替代它们。


## 11. MCU6正式检查点：两板独立82项通过

本节是MCU局部检查点，尚余112处最少连接，不是完整HI布线入口。原生读取后导出保存到immutable checkpoint，本专项另存关键输入副本与hash，详见[独立报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/mcu6_independent_native_review.json)和[复核脚本](../examples/lessonHI_38_50_20261021/engineering_mcu/review_mcu6_native.py)。

| 项目 | 四层 | 两层 |
| --- | --- | --- |
| 检查点 | inventory/checkpoints/mcu_4L_b006 | inventory/checkpoints/mcu_2L_b006 |
| 独立检查 | 41/41 | 41/41 |
| 原生状态 | 80件/69网、DRC0且current | 80件/69网、DRC0且current |
| MCU6计划铜 | 67段全部几何覆盖、12via准确 | 同左 |
| quiet实际层/面积 | L2、62.31 mm² | BOTTOM、62.31 mm² |
| 单via负测试 | 6组正/负端点、3guard成功，恢复0DRC | 同左 |

HSE_CASE4地线被native在Y1.2汇入的y38.9处分割为36→38.9→40.8；独立检查按同宽同网同层线段并集核整个计划区间覆盖，不把正常CAD分段错判缺线。并检查三处器件移动、quiet真实polygon、应用地真实void/无重叠及quiet via实际每层铜。

实际铜polygon包含圆弧，采用本机Cadence 17.2官方algroskill/20plyopr.html中vertices说明：半径属于前一点到本点的段，正负表示圆心竖轴左右侧；不把半径丢掉当直边。独立展开每弧最大弦高误差0.00002 mm，实际global面积与native打印面积差约0.004—0.006 mm²，归于几何量化/打印与离散口径，采用0.01 mm²面积核对容限；island无圆弧，面积误差为数值舍入。详见[圆弧展开核验](../examples/lessonHI_38_50_20261021/engineering_mcu/review/mcu6_native_polygon_flattening_check.json)。这不把弦高精度说成板厂制造公差。

还发现两层旧normalized.vias[].pads显示L2/L3，但原始physical_pad_layers.tsv仅TOP/BOTTOM。实际crosssection没有内层，本专项按真实逐层pad文件核验，不把normalizer盲点解释为两层板额外铜层。已通知原生执行者修后续normalizer，保留旧immutable checkpoint身份，不静默改历史证据。

USB首次原生执行使用v6中的“L28_VIA030_C060_OR_VERIFIED_TENTED_PRIVATE_VARIANT”占位选择文字，axlDBCreateVia返回nil，执行停止、源稳态未保存为错误板。该字符串不是软件里真实存在的封装，是本专项交可执行方案时的失误；现[USB7](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v7.json)四枚via均用准确名字L28_VIA030_C060，几何没有改变，且保留[映射/身份](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_v6_native_adapter_mapping.json)。以后“待选A或B”只放purpose/prerequisites，执行字段必须是已盘点真实对象。tented实际mask/artwork验证仍独立保留。


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


## 15. 两层USB8正式检查点及专项复核补充（2026-10-22）

两层正式板native/HI_2L_usb_esd_2L_b008_bulk.brd，SHA256=90E8AC3413332098A4D86E035E5200B955F8385003D9628C5F396FB2F8161739；新进程logs/reopen_usb_esd_2L_b008_bulk完成32端点、HSE唯一via负测、DRC0/current。独立[两层实际路径](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_native_usb_esd_2L_b008_bulk.json)及[四层实际路径](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_native_usb_esd_4L_b008.json)各18条全部可达；两层保护侧各4.326565 mm，R11真正tee=.395 mm；四层各4.699357 mm、tee=.845 mm。此前计划与实际一致，phase检查仍是平面长度口径。

[MCU/quiet保持复核](../examples/lessonHI_38_50_20261021/engineering_mcu/review/mcu_preservation_after_usb8_independent_review.json)在USB8后两板各41项再通过。两层bulk优化只在成组操作/导电图试验时暂缓更新，wrapper明确恢复drcEnable，再axlDRCUpdate(t)，再导出当前0DRC；HSE图恢复日志先写FULL_DRC_REQUIRED，不能把这个中途状态本身当0DRC。

受控电气规则挑战：把connector phase4临时收紧至3 mm，原生报实际3.2757；把共享pair uncoupled6临时收紧至1 mm，报4.9931/4.9204；恢复两份各自4/13.5与1/6后DRC0。差分规则确实工作，共享预算未为DNP长枝而放宽。当前2L via pad层表按实际crosssection过滤为TOP/BOTTOM，原raw内非存在层查询仍保留，避免静默抹历史。

正式[返回走廊02报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_actual_return_corridors_02.json)已改绑定正式两板，几何结论与首轮相同：镜像区0.40 mm实际地走廊存在，2L VBUS底槽可用0.30 mm绕左端地走廊存在，直接投影开口保留。真实图见[参考/返回预览02](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_reference_return_actual_02.png)和[SVG](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_reference_return_actual_02.svg)。图表示实际铜和可用路径，不是电流仿真；整板后续铺铜变化还要再核。

子进程PATH已由原生执行者实测纠正：bem2d解析从null变为安装bin中的bem2d.EXE，只影响该子进程，无系统/用户PATH修改。纠正后内部STL场解仍反复失败，故PATH问题只是已验证的一个启动环境问题，**不是已经解决全部场解失败或已找到唯一根因**。没有使用失败场解数值作SI/时延验收。

GPIO6候选TOP参考片与既定application-ground moat有部分重叠；原生执行者采用原moat多边形做实际差集，保留原候选/差集/SHA，并继承HSE单anchor负测。即便不直接碰quiet via，也不能把应用地偷偷铺进已声明moat。当前GPIO6及后续普通接口/最终整板审查未因USB8检查点而自动通过。


## 16. 普通 GPIO 之前先联合扇出与源端可接续性（2026-10-22，进行中）

本节是工程候选与纠错记录。第 11—15 节的 MCU6、USB8 是各自不可变原生检查点的历史证据；后续器件移动、供电改线、地形变化必须重新验证。不能把历史 0 DRC 或 USB 参考走廊覆盖到尚未执行的新源端/普通网络。

本轮按原生 b014 真实焊盘、272 个逻辑引脚、实际过孔、全部手工/固定铜线及机械孔建几何障碍。GND 同网不代表安静振荡地与应用地可以直接相连；HSE 原有真实 guard 的铜宽加工程余量也在 TOP/BOTTOM 普通信号禁穿区内。机械 J2 空位号的两颗 Ø0.65 对位孔必须单独读实际钻孔，不能因 regular pad 为 NULL 而漏掉。

### 16.1 源端要给后续网络留出口

- 北侧拟定 [north02](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_north_joint_fanout_02.json)：PA1/PA2/PA3 分别给明确出层点，PC15 的原底层折线也联合调整。PA2 先接续再处理 PA1，可以避免先走 PA1 把 PA2 夹在 PC13 partial 与自身新线之间。顺序只是候选求解策略，最终仍逐段复核，不称自动布线即可完成工程设计。
- 左侧 [left07](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_left_joint_fanout_07.json) 联合 PB1/PB10/PB11/BOOT1 与 pin18 VBUS_PRESENT_N。PB11 出层点改为 (33.7,25.3)，PB1 改从内侧到 (38.3,27.35)，给 pin18 外侧 (34.6,26.85) 留真实可接续出口。PB1 的短窄线全长约 2.7542 mm，其中一段按两颗实际过孔间隙采用非 45° 斜段，必须记录其几何原因，不能隐瞒为全板 45° 标准走线。
- 为达“地孔距离 ≤1.5 mm”而先放地孔，会把普通信号出层点封成口袋。原 left04/05 拟加 GNDvia(33.28,26) 因此取消。PB11 仍靠继承 C13 应用地孔，PB1 的实际返回则须在全长路和填铜后核，不机械地追求一个距离数字。
- 南侧 PB15 原下行底层短颈与根组后来挪至 (38.8,19.7) 的 GNDvia 实铜重叠，不能只审查新服务线。已记录 [PB15 上行替换 delta](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_PB15_bottom_exit_delta_01.json)，用 BOTTOM (38.5,20.7)→(38.5,22.3)、宽 .16、长 1.6 mm、局部 maxneck2.4；只在 PB14/USB_ATTACH_N 两个邻过孔的有限 via_line 字段用 .16。没有保留原下行死端。

这些小孔使用原生已核的私有 `HI_VIA026_C052_TENT`，Ø.26 钻孔、Ø.52 铜、单边环 .13、mask NULL。最初 `hi_via026_c052_tented` 为 21 字符，超过本机官方 PADLIB 20 字符限制，已缩为 19 字符并保留映射/失败准备源。不是通过改公共库解决。两层 OSH 已公开孔最小 .254、环最小 .127，当前仅 .006/.003 的名义裕量；实际刀具、成品孔口径、公差、帐篷阻焊仍是制造待确认。四层 JLC 公开多层孔/铜环能力分别核，不沿用两层认证。

原生许可预审进一步证明：through via 的 approved list 要在每个实际铜层有正确作用域，只放 TOP 小区域会在四层 L2/L3/BOTTOM 继续报 ViaList。只增加小孔许可的区域逐层复制真实父 Physical CSet，其它线宽、颈长、层许可不改。实际区域交叠会采用更严格预算，不能把 JSON 中写了 2.8 就当原生已生效。

### 16.2 长 NSS 上拉支路应先改布局，不能靠绕全板挤 GPIO

NSS 上拉支路虽然直流电流小，其铜线仍是 NSS 信号残桩。原内侧 TOP 加 BOTTOM 约 19 mm 的支路，与 TOP MCU 电源横干共同围住普通信号；找到 83—119 mm 绕 USB/板边的候选不能作为合理设计交付。

冻结的 [NSS04_SOURCE_ONLY](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_local_relayout_04_SOURCE_ONLY.json) 将 R25 置于主 NSS 节点附近，残桩中心线约 1.89906 mm。必要布局为 R21(33.7016,30.7)180°、R23(33.5,32.1)180°、R25(31,33.7)0°、R32(31,35.5)0°。保持 R21/R23/R25/R32 的原理逻辑/值，精确删除原 SPI 源侧和接口侧相关旧段并重接，不能只拖器件留旧铜。

MCU U1.10→C24.1 的 ADC 主路径原样保留。移动 R32 后，只重做输入端与 R32→C24 的 RC 前级铜；新 ADC0 竖向段 x33.65 是为避让 C24 真实 .6 GND 返回及 R25 焊盘，不是凭器件中心拉一条直线。新的输入/串阻路径与相应参考保护区须一并更新，不能拿旧路径的参考审查替代。

[四层原类别/真实焊盘检查04](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_relayout_class_review_4L_04.json) 29,042 对、[两层检查04](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_relayout_class_review_2L_04.json) 29,380 对，无名义类别间距违规；此结果包括移动后的元件焊盘，并非只检查新增线。原生连接图、真实 CSet、填铜、重开和 HSE 单 anchor 负测仍待完成，不能将此称作原生 DRC 通过。

Source04 特意保持原 C9via(30.7,32)、原 C9 TOP feed、原 BOTTOM STAR 对角和 37,24 via、原 SPI guard。它仅从原 C9via 加 R25 的短电源支路。后续若更换主供电入口，独立 delta 应按实际原生对象删除原 STAR 两段/末端 via，不能重复套用此前被否决版本的移孔操作。

### 16.3 已发现并保留的失误

1. left04 的 PB11 出层原拟 (33.5,25.3)，基于较早 b010 场景看似可用；SPI b012 新增 GNDvia(32.8,25.3) 后，.52 信号孔对 .6 地孔铜间距只 .14，低于两层公开工艺 .1524。改 (33.7,25.3) 后铜距 .34。每次新原生检查点都必须重纳所有旧/新过孔，不能只比本组旧板。
2. left03 曾出现“输出 anchor 改了，但实际 via op 未同步”的脚本替换问题。交执行前增加 source op 与 partialEndpoint 坐标一致断言，旧候选保留，不冒充已经创建的原生孔。
3. NSS01 的 R21 y30.6 新输出焊盘与两层真实 MISOvia(31.65,29.77) 只有 .1235，检查制造最小距离或只看新线均不足。按原类别+移动焊盘补查后，改 R21y30.7 恢复 .2235，邻 R23 也联合挪位。
4. [NSS03](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_local_relayout_03.json) 曾手拟主电源沿 x29.8 直下，在未先逐一核 C9.2 与 buck 反馈/地焊盘时猜了路径。真实铜审查发现跨 C9 GND 焊盘/地线及 R2 反馈区，明确否决，未交原生执行。以后先由实际焊盘/线/孔建完整障碍，再规划电源路径；不能依靠封装原点或记忆猜净空。主 feed 改道交电源组按实际铜设计。
5. 原型搜索把整块 SPI bank 或 ADC 任意 buffer 当硬禁布，会把合理局部跨层判为“无解”。它们不等同用户/制造硬约束。HSE 主 quiet/moat/真实 guard 的禁入继续严格；其它投影交叉要按实际有限开口、同层地、近返回与线路优先级审查，也不能反过来称所有投影交叉都没有影响。

### 16.4 当前未完成项与验收边界

13 路普通 GPIO 全长路仍在联合规划。旧搜索的“找到/失败”只是候选，不是实际通断；曾发现 source 颈线 .16 合法而强制按 .20 倒走同路径扩大铜宽造成假封口，也发现栅格过保守膨胀误挡有限间隙。候选改为精细名义掩模后，仍对每段做连续几何验证；不能用降低栅格安全余量替代原生 DRC。

为与电源组协作，另有明确标为 `CONTINGENT_GPIO_CORRIDOR_STUDY_MAIN_POWER_NOT_COMPLETE` 的抽象场景，暂移除原 STAR 大对角观察普通 GPIO 走廊。该场景电源尚未接回，绝不是可用 PCB 或电气完整设计；必须有合法新主 feed、实际地返回及全组几何后才可转成原生批次。

最终还要逐板验证：全部逻辑引脚/80 件/69 网保持；13 GPIO 每个 U1→header 真图；新小孔全实际层许可；每条短颈/区域内外挑战；GND 无孤岛/孤枝；HSE 唯一 anchor 断开后局部岛保持互连但不达应用地/壳地，恢复后重新通；USB 两插向主铜和 DNP 残桩/参考；新 ADC、晶振护地及电源/接口有限返回。不会从“全部连通”或“0 DRC”推出制造、90Ω、USB、ADC、SI/PI、EMI 辐射或硬件性能已通过。


### 16.5 搜索失败不能证明必须更改主电源

早期 GPIO 搜索在固定 partial 端点与过粗禁入区下失败，我一度推测 BOTTOM STAR 主 feed 必须重构。后来保留原 STAR、仅调整接续起点/顺序，已经找到 PB12 等候选；删除 STAR 的不完整研究也未改善完整组结果。该归因过早，已向根与电源组纠正。`GPIO13_*_corridor_contingent_18/19.json` 没有接回主供电，只是失败/抽象比较资料，不能作为板文件交付。`GPIO13_*_original_feed_order_20.json` 保留反例。

后续 N37 去除不再使用的 PC13/PC15 底层教学长尾，并从真实已连接过孔选择 TOP/BOTTOM 出口后，PB1 在正常 .2 mm 线宽下可以接出。这证明先前的“封闭”只属于当时冻结 partial/出入口下的几何搜索结果，不能等同于物理无解或必须重构电源。所有不再使用的教学尾线要先严格核实并精删，不能只改虚拟 anchor 又保留旧铜。

### 16.6 b015 实际 DRC 与几何筛查范围纠正

b015 是 `DRC_PENDING`，两层 raw14、四层 raw20，完整原生 DRC 尚未通过。先前“无重叠”与 .1524 mm 制造底线筛查没有覆盖全部 .2/.3/.5 mm 原生类别规则，因此不能冒称该源组已通过。实际 PB1/PB10 线距 .19＜.20，以及 PC15 BOTTOM 到 GNDvia 的 .20＜.30，均是真实问题。

[LEFT_NORTH09](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_LEFT_NORTH_spacing_fix_09.json) 将 PB10 末 via/尾线移至 (38,26.3)，PC15 横段调整至 y28.75，保持原有类别间距，不改全局规则。四层 all-layer 小孔许可也不等于 via-via 间距已经合格，.1871＜.2 的原生问题必须按实际孔位修正或有明确有限例外，不能因为外层无短路而忽略内层。

原生另发现 VDD24 细颈 1.3192 mm 超出该位置 max1。采用 [局部扩宽修复](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/VDD24_neck_geometric_fix_2L_01.json)，把 (35.1,23.6)→(35.1,23.2) 从 .25 扩为正常 .6 mm，余对角细颈 .919239 mm；两板原生 scoped DRC 已确认通过，不扩大电源颈线规则。DRC 定位 (35.1,23.35) 不是 R21 电源引脚，R21 实际属于 SPI_SCK；应按实际对象身份记录。

### 16.7 R27 真实供电误判及 J12 布局比较的边界

此前电源研究把 TOP V3V3 的 (31.11,55)→(31.11,47)→(38.1016,47) 误判成原 R25 的死枝，我的场景36/N37直接继承这一结论。实际还有 (38.1016,47)→R27.1(38.1016,41.3)，两板均是 NRST 上拉电阻的有效供电。只看到 y47 端点没有器件，不能判断整条连接图是死枝。原生累计硬件终端检查抓住 R27 断供，失败板未作为合格结果保存。后续场景恢复两段，并保留上方共享 vertical，不再称“旧 R25 死枝”。

J12 南移供电研究中拟删除 (31.11,58.2)→(31.11,55) 也会切断该共享 R27 供电；原供电假设不完整，南移方案未执行。现在优先保原 J12(40,55)、90° 比较完整 GPIO 路径，主电源/ADC 不变；不能以搜索失败证明必须搬排针。

另有一次口头 pinout/orientation 失误已在任何执行前纠正：实际 J12 是 90°，pin1=V3V3、pin2=GND，不能对换。原位 pin1=(31.11,55)、pin2=(33.65,55)；南移候选 (18,9)90° 时依次为 (9.11,9)/(11.65,9)。南移候选尚未完成完整 13 路、供电和返回验证，不是最终布局。

### 16.8 冻结教学尾线清理合同，保留真实硬件终端

[两层清理合同](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/South_UNUSED_BOTTOM_PARTIALS_2L_01.json) 与[四层合同](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/South_UNUSED_BOTTOM_PARTIALS_4L_01.json) 各自只精删 PB12/13/14/15 的 8 个 BOTTOM 教学尾线段，保所有 MCU→sourcevia 的 TOP 铜及 sourcevia 本体。逐网核实尾线是单路径、一个真实 sourcevia 接入、另一端无硬件终端，并保存全部真实引脚和 TOP 对象身份；这与之前仅看 R27 中间端点的误判有明确不同。

旧的虚拟 partial-end 证明退休，替换为 U1.25/.26/.27/.28 到真实 sourcevia 的原生导电图；完整 U1→header 合同继续保留，不能用“源 via 可达”代替全长路。两层删尾后应重新填铜验证 WEST GND 的真实应用地连接，不能为了保存中间板先不断加地孔把 GPIO 口袋封死。普通 MID GND 的删/移只是派生比较，尚未随此清理合同交原生；若最终需调整，必须验证真实地平面/BFS、有限返回距离与 HSE 单 anchor。

其他 GPIO 顺序、细孔、C9/U3/ADC 调整、TOP V3bar 换层、南排针等失败比较文件保留，全部是派生工程探索。全长路、全规则、实际参考/返回、重新打开、GUI 与制造/硬件条件尚未因这些候选自动通过。

## 17. 2026-10-22 后半程：手动门户、布局比较与尚未通过的条件

本节是工程探索记录，不是完成验收。当前真实板仍是 `padentry_*_b019_DRC_PENDING`：两板各有 7 个 South GPIO 待接，65 个非 USB 网络逐网 scoped DRC 为 0；完整 USB/整板检查未通过验收。2L SHA256=`AA3BFC0E01B06CB1058462439C71E56BC316F1F2929859B6A224320BE1013420`，4L=`B7A32330992F49609339E33C00BE92D989D0EA0C4AF64ED2763D0678DE14B501`。下面所有 80—92 派生几何均没有写入这些原生板；派生 snapshot 中继承的字段名不能作为原生执行证据。

### 17.1 改用人工短门户，并纠正坐标和人工墙

原位/南置比较中，[独立与联合状态](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO7_comparison_state_20261022.json) 保留了每次路线、失败与条件。独立七网各自能找到路径，并不表示组合后能共存；12 轮拥塞搜索仍有交叉，不能通过增加搜索次数把它称为 PCB 已设计完成。之后停止广域 negotiated 搜索，改成源、短换层窗口、主走廊、目的端分别手动核。

必须从实际过孔读坐标：PA9_UART_TX 是 `(39.7,21.7)`，USB_ATTACH_N 是 `(39,21.2)`，PB14 是 `(38,21.25)`；此前口头分析误用 UART_TX `(39.55,20.7)` 的设想已废弃。4L PB13/PB15 源孔分别为 y20.725/y20.675；2L 则为 y20.75/y20.7。不能用虚拟尾线端点替代真实源孔，不能由封装中心推测焊盘位置。

[PB1 80 候选](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_PB1_inward_4L_80_delta.json) 保留原电源/ADC/HSE，只研究 TOP 源弧与普通返回孔的小修改。它仍改变了通用 V3 入口：PTH `(37,24)` 移到 `(37.2,24.3)`，TOP 新 .6 mm stub 长 .38284 mm；BOTTOM 末段从 1.7 mm 改成 1.48284 mm。不得把它写成供电/去耦路径完全没有变化。原直接去耦铜虽保留，完整供电图、入口电感、过孔 alias 和实际回流仍须原生核验。2L 普通 GND 37.4,27.4 的迁移也必须逐一解释其原 PB10 返回角色及替代共地路径，不能只凭同 GND 网络删除。

80 的 BOTTOM L 又会把 PB10/其它源封在里面，不能把新候选冻结成物理墙。最小左绕替代为 `(41.9,26.79)→(40.8,25.69)→(40.8,23.55)→(36.7,23.55)`；TOP 和原 PB1 孔不变。它仍只是候选，PB14 的北向门若需要穿过该横段，还必须联合调整。普通源需一组设计，不能完成一脚便把其余脚的通道封死。

North51 的 PA3 不是整路 x+y=67.25：它先有横段，再长 NW 时实际 x+y=65.9。仅按一个源段的斜线常数设计 PB1/PB10 会撞真实长尾。原 R25 新 V3 支路 BOTTOM x31,y32.3..33.7 也是实际障碍，不能只因与主 STAR 平行就声称 NW 门户已全通。

### 17.2 单移 ATTACH .14 mm 的真实局部门户

[87 两层检查](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_attach_2L_87_check.json) 与 [四层检查](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_attach_4L_87_check.json) 在加入全部新铜后同时检查，避免先查 via 再加相邻新线的顺序盲点。

- USB_ATTACH_N 源孔从 `(39,21.2)` 移到 `(39.14,21.2)`；TOP .16 源为 `(39.25,22.75)→(39.25,22.1)→(39.14,21.99)→(39.14,21.2)`；BOTTOM .2 接 `(39.14,20.44)→(39.7,19.88)→(39.7,18.6)`，接回原远端。
- PB14/PB15 原孔及 MID/EAST 普通地孔均保留。PB15 正常 .2 BOTTOM 能沿 x38.57 穿过原 PB14 与新 ATTACH 孔之间，正常名义铜距约 .21/.212 mm，再北绕东达 `(47.1,23.3)`。4L 全部新外层铜几何检查通过；这不等于完整 PB15 长路，更不等于原生 DRC。
- 2L 没有真实异网铜碰撞，但新 PB15 穿过 TOP USB pad 对面参考保护区；ATTACH 的新腿也与原 USB DM/DNP 附近参考范围相交。这些是实际参考与局部回流待审，不能通过删除保护区域就称通过。
- 更大的 ATTACH 迁移到 `(39,18.6)` 曾直接落入 R6 的 PA11_SHARED 真 SMD 焊盘，已否决；迁至 `(39.38,21.07)` 的方案又遇 UART_TX/RX 源与返回，均未执行。小移动避免了这些实际对象，不能把大移动的一部分名义间距作为完整通过。

USB pad 的实际北端为 y23.35。BOTTOM 线 y23.8、宽 .2、按 .3002 地间距产生的参考 void 下缘为23.3998，只有约 .0498 mm 名义余量；需 native actual fill 验证。其自身又可能长期在 TOP V3 条/地避让投影下，必须单列电源耦合/同层共地返回，不能说通过 USB 投影就有完整 GPIO 参考。

### 17.3 四层 PB15 完整短内层桥比较，不擅改变层功能

[89 完整路径比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_4L_short_L2_comparison_89.json) 只作为 root 选择的工程备选：接87源门后，BOTTOM 到新孔 `(48.9,23.68)`，L2 .2 沿 `(49.1,23.88)→(49.1,28.9)→(51.6,31.4)`，再 BOTTOM 北行；在 NRST 的 BOTTOM y41.55 附近用 TOP 1.7 mm 短桥，最后 BOTTOM 至 J13.3。

完整 U1.28→J13.3 中心线为50.61514 mm；其中 L2 8.83838 mm，新增4个 signal PTH、3个 stock GND return PTH。源换层至原应用地孔 `(48.2,25)` 为1.4948 mm，其余返回为 .9/.8/1.1 mm。全部新外层铜/保守穿层 pad 检查12项无异网违规；最后一个地孔最初距新斜线只有 .1657<.3，已改到 `(53.4,42.4)`，不能漏查本批新增铜彼此的关系。

此方案没有 native 执行、没有内层许可批准，也未认证 SI。采用时必须显式设有限 L2 allowEtch 及 .2 线宽/原间距，小孔许可覆盖四实际铜层；全局其它信号的内层禁布仍保持。L3 必须是真实连续的应用地参考，L2 新 slot 对 TOP 普通信号和去耦投影的影响需逐点审查；不能把原两块 GND plane 的设计意图当成已实现原样不变。2L 完全不能套用这个内层桥。

### 17.4 PB10 门户和排针布局的真实代价

原生组提供的 [PB10 v46 门户](../examples/lessonHI_38_50_20261021/review/b020_engineering/PB10_NW_North4_repack_v46.json) 使用实际 b019，普通 North4 长尾重新压紧，并将 PC13 接收孔移到 `(29.25,40.05)`。PB10 保留源孔 `(38,26.3)`，到 BOTTOM `(38,27.72)→(30,35.72)`，经 stock 孔转 TOP 至 `(28,36.1)`。这只是源到门户，不是 U1→J12 完整验收；旧 TOP/参考缺口分别按两层/四层记录，不能把两板几何互相替代。

[92 两层南置完整比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB10_south_2L_92_candidate.json) 接上该门户，保81已成四网和87源修改，在不穿 buck 热区的条件下，经左侧至南置 J12.4，完整 U1.21→J12.4 几何长77.55685 mm；本批远续60.21995 mm、2个新 signal PTH/2个 GND return，7项新外层铜检查无问题。它只是能比较的偏长候选；目标南置需要避 buck、其它目标 bank 和实际排针电源孔，不因已成四网便声称这种布局是优选。4L 同形会碰真实 SPI BOTTOM 线，91失败资料保留，禁止套用两层通过。

J12南置的 V3 .6 新支路32.19 mm仍是额外代价，原 R27 LIVE 全部铜必须保留。原北排针、南置、必要中北空区的小移应按全部7路长度/过孔/实际返回、供电/GND与插拔空间比较；搜索失败不是用户要求搬排针。所有 GPIO 的源边沿/实际负载、串联终端需求仍待接口定义，不能从直流连通或慢时钟数字推断长线不会反射/辐射。


### 17.5 补充比较：保原北排针与避免去耦下方内层 slot

后续 [94 两层原北 J12 完整比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB10_original_header_2L_94.json) 和 [94 四层比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB10_original_header_4L_94.json) 在 f29 v46 源门户基础上，完成 U1.21→原北 J12.4 的手动几何路径，长度均46.06476 mm，比南置92少31.49209 mm；需要5个新增 private signal PTH，以及6个 GND return PTH/两条 BOTTOM .6 返回桥。它们尚未组合其余6个 South GPIO 长路，不能与南置81混成“全7路”。全部22项新增外层对象检查通过，仍不是原生 DRC。

94 还把 PC13 接收孔从 v46 的 `(29.25,40.05)` 移到 `(29.25,40.95)`，TOP 前段到 `(24,46.2)` 后，必须横到 `(23,46.2)` 接回原 x+y=69.2 长尾。曾错接到69.3，导致邻 GND16.9,53.3 铜距仅 .2364<.3、邻 PA2 孔仅 .1657<.2，已在同轮几何核中修正，未执行原生。PB10 一个转层到既有共地孔约2.57 mm，并未实现所有过孔返回≤1.5 mm；实际 TOP 同层共地/返回绕行仍需补验。

[95 更新后的四层 PB15 比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_4L_short_L2_comparison_95.json) 取代89作为内层对比的首选读物，89保留历史。89虽外层检查无碰撞，其 L2 走向会投到 C16 的供电/地 pad 下方；这说明只检查外层 DRC 不能证明电源回路和参考条件良好。95 绕开 C15/C16/R17 pad，L2 增至9.33543 mm，完整PB15=51.11220 mm，仍12项几何检查通过，没有原生执行/内层许可批准。

[95 实际参考几何审查](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_4L_L2_reference_95.json) 使用实际 b019 的 L3 GND 填铜：候选内层线及 .2铜宽投影原先全部覆盖；按新 signal PTH 半径.26加保留.30 GND间距，估计两端共1.15206 mm参考开口。该 anti-pad 是明确平面估计，实际 native repour 仍必须读回。计划 L2 slot 会使 TOP 的 BOOT0约1.1314 mm、PA15 .8 mm、PB4约1.0528 mm、SCL约1.1314 mm、GND支路约 .6255 mm中心线投影失去原L2参考；不能因为新L2线能参考L3，就忽略原TOP线受到的影响。C16地 pad 到计划slot最近仅 .21872 mm，仍是需要PI/场宽复核的边界，不称性能合格。

截至本补记，所有95/94/92/87均为只读工程比较；最新真实板保持b019、两板各7个待接GPIO。root已在当前用户状态回复中明确未完成整板验收。本阶段不再扩大无收益的广域搜索；下一轮应由root统一选择可解释的布局/层功能取舍，再叠全7路径、做完整回流与原生验收。
