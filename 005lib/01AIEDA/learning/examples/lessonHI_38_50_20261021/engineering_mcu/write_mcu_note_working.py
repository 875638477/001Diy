import pathlib,datetime,json,hashlib
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
note=R.parents[2]/"notes/lessonHI_mcu_20261021.md"
body="""# H/I 第38—50课：MCU、振荡器、复位、ADC与USB路由专项

日期：2026-10-21（Asia/Shanghai）。所有资料、脚本、候选、失败和审查均在01AIEDA。本笔记是合并课程的工程子记录；课程总状态由根笔记/索引逐项验收，不能凭本专项宣布13课全部完成。

## 当前入口与证据身份

本次从G阶段冻结的80器件、272逻辑脚、69网络、80×60 mm教学板继续；J2板边、四安装孔与机械基准保持。基线供电去耦已有三组TOP真实闭环及C16支路，不把它们重新当未布线空气线。输入版本和原厂PDF身份见[输入清单](../examples/lessonHI_38_50_20261021/engineering_mcu/input_manifest.json)。

本专项负责工程路由方案及原生导出后的独立几何/返回审查；**没有启动Cadence**。所有原生操作由合并课程的原生执行者完成。桌面控制/GUI逐段拖线未在本轮获得证据；官方SKILL精确建线、事务、DRC、导电图、保存重开应分别记录，不能称GUI已掌握。

当前冻结候选为[MCU v6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/mcu_critical_routes_v6.json)、[USB v6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v6.json)与[GPIO north v3](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/gpio_north_escape_v3.json)。v1—v5等旧稿保留作过程证据，不能直接重放。MCU v5原生两板的32指定端点和HSE隔离挑战已由原生执行者报告成功，但存在两条真实间距错误，故不能把v5称最终通过；v6只做对应最小修正，正式结果仍需新进程读回。USB/GPIO当下为已做实际铜几何预审、待原生验证方案。

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
| MCU共享对角部 | DM略左.02 mm，实际最紧gap约.167696 mm | 原最紧gap约.153553 mm |
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
"""
note.write_text(body,encoding="utf-8")
print(json.dumps({"note":str(note),"bytes":note.stat().st_size,"sha256":hashlib.sha256(note.read_bytes()).hexdigest()},ensure_ascii=True))
