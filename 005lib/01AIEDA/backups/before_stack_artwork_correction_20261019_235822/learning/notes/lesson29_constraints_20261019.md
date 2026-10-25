# 第29课：Constraint Manager、网络分类与真实规则验证

日期：2026-10-19（Asia/Shanghai）。本课已完成原生CAD范围：真实规则写入、保存重开、分类与继承读回、受控违规和回退、独立长度规则样板及官方技术约束导出。未将未布局的主板称为整板布线或SI／PI／EMI验收通过。

## 1. 当前入口与文件身份

全部学习文件均在 D:\001DIY\005lib\01AIEDA 内。本课未修改公共库、01env、HOME、快捷方式或用户实际工程。

| 内容 | 当前文件 |
| --- | --- |
| 后续四层布局起点 | [F29_CONSTRAINTS_v3.brd](../examples/lesson29_constraints_20261019/native/F29_CONSTRAINTS_v3.brd) |
| 已应用规格与工程依据 | [constraint_spec.json](../examples/lesson29_constraints_20261019/constraint_spec.json) |
| 独立验收 | [validation.json](../examples/lesson29_constraints_20261019/validation.json)：543项通过 |
| 另一路独立审查 | [审查笔记](lesson29_independent_review_20261019.md)、[review_final.json](../examples/lesson29_constraints_20261019_review/review_final.json)：937项通过，计数不与本课相加 |
| 原生只读证据 | [read_final02](../examples/lesson29_constraints_20261019/logs/read_final02)、[机械/焊盘补读](../examples/lesson29_constraints_20261019/logs/read_geometry) |
| 受控规则验证 | [challenge04/challenges.txt](../examples/lesson29_constraints_20261019/logs/challenge04/challenges.txt) |
| 长度规则校准板 | [F29_PHASE_COUPON.brd](../examples/lesson29_constraints_20261019/native/F29_PHASE_COUPON.brd)、[创建记录](../examples/lesson29_constraints_20261019/logs/coupon_build.txt) |
| 官方技术约束文件 | [F29_RULES.tcf](../examples/lesson29_constraints_20261019/exports/F29_RULES.tcf)、[原生比较报告](../examples/lesson29_constraints_20261019/exports/techfile_run/compare_techfile.log) |
| 规则预览 | [PNG](../examples/lesson29_constraints_20261019/constraint_overview.png)、[SVG](../examples/lesson29_constraints_20261019/constraint_overview.svg)，为原生数据整理图，不是软件界面截图 |
| 来源与失败历史 | [本机官方资料索引](../examples/lesson29_constraints_20261019/source/official_local_sources.json)、[失败与修正](../examples/lesson29_constraints_20261019/failure_history.json) |
| 完整文件身份清单 | [artifact_manifest.json](../examples/lesson29_constraints_20261019/artifact_manifest.json) |

最终主板SHA256：6276201EF1750D3A318D901CCF1ADFBB1CA41A4301329CD21E32A0E22B3FA607。它由第28课四层板副本继续，原输入F28_4L.brd的SHA256为F004184D46B86A7CF56FFA05C33418A6BEEFA508A3043A3442540B69AFA558D6，输入保持不变。v1、v2、DOMAIN_PROBE、CHALLENGE等文件保留作历史／校验，不能替代v3继续主线。

## 2. 学习依据与适用条件

主要接口依据为本机Cadence17.2官方axlCNSCreate／Get／Set、NetClass、DiffPair、ECSet、DRCUpdate、DBAssignNet、PinsOfNet帮助及官方dbcreate/pad.il实例；路径和SHA均在来源索引中。没有凭名称猜测Constraint API。

电路沿D/E基线：STM32F103C8T6、正常V3V3总预算150mA、0—40℃、GPIO及header外载合计≤10mA；受控9—16V输入，500mA保险丝。USB为自供电Full Speed，CAN与USB互斥装配/运行；UART、I2C默认100kHz、SPI≤1MHz按既有教学条件。上述预算不是实测电流或热验收。

本规则档只适用于第28课的四层JLC目标：TOP-L2-L3-BOTTOM，外铜0.035mm，TOP至L2介质0.2104mm／Dk4.4，内铜0.0152mm，core1.065mm／Dk4.6。材料频率与阻抗工艺仍有待厂商确认项。本课0.15mm颈缩不能原样用于OSH Park两层板，其公开最小线宽0.1524mm；两层板后续应建立独立规则档。

[ST AN4879 Rev12，2026-06](https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf)用于USB器件和上拉／VBUS条件复核。该版已不包含早期PCB长度章节，不能把旧版尺寸当作本版强制规则；网页可读，shell下载HTTP567失败记录保留，没有假称PDF已离线下载。

[TI USB布局教学](https://www.ti.com/video/6087491555001)与[SPRAAR7J原厂指南](https://www.ti.com/lit/an/spraar7j/spraar7j.pdf)用于连续参考、短而对称的路径、局部匹配和接口保护的设计理由。后者已离线保存并看过相关图页；其特定高速SoC附表不直接套用到F103。

## 3. 实际分类与层级

69个真实网络分为9种功能，物理／间距／电气域各用一个独立网类，共27个原生NETCLASS对象、207条网类成员关系。每个网络保存重开后都能通过axlNetClassGet在三个域找到对应类。

| 功能 | 网络数 | 物理CSet／间距CSet |
| --- | --- | --- |
| POWER_INPUT | 3 | P_POWER_060／S_POWER_030 |
| POWER_LV | 4 | P_POWER_060／S_POWER_030；GND、VDDA有下面的直接例外 |
| SWITCHING | 2 | P_SWITCH_060／S_POWER_030 |
| ANALOG_SENSITIVE | 3 | P_ANALOG_020／S_ANALOG_030 |
| OSCILLATOR | 3 | P_OSC_020／S_ANALOG_030 |
| USB_FS | 4 | P_USB_PROVISIONAL／S_USB_015 |
| CAN_BUS | 2 | P_CAN_025／S_CAN_025 |
| USB_AUX | 3 | P_SIGNAL_020／DEFAULT |
| DIGITAL_GENERAL | 45 | P_SIGNAL_020／DEFAULT |

本案例实际验证的关系是：DEFAULT回退值 → 所属域NetClass引用CSet → 更具体的net CSet或属性覆盖；class-class表规定特定类之间的间距。USB电气ECSet附于两个差分组，再由成员网络继承。不能把查询一个CSet的数值当作某个net已经应用该值的证据，也不能忽略直接override或更具体的区域规则。本课没有在尚未定位的MCU周围凭空保存“逃线区域”。

普通电气域分类只用于组织，不强加无依据的延时或等长。USB的电气约束实际来自pair上的E_USB_FS_BUDGET，不是虚构每个普通网络都需要时序匹配。

## 4. 已实际保存的规则

当前共有10个物理CSet（9个命名集＋DEFAULT）、7个间距CSet（6个命名集＋DEFAULT）和1个电气CSet。逐层原始数值见physical_csets.tsv／spacing_csets.tsv／electrical_csets.tsv。

| 用途 | 普通线宽 | 最小颈宽 | 最大颈长 |
| --- | --- | --- | --- |
| DEFAULT、普通／模拟／晶振 | 0.20mm | 0.15mm | 1mm |
| 电源主干、SW、GND | 0.60mm | 0.25mm | 1mm |
| VDDA支路 | 0.30mm | 0.20mm | 1mm |
| CAN | 0.25mm | 0.20mm | 1mm |
| USB暂定几何 | 0.20mm | 0.15mm | 1mm |

普通铜间距0.20mm；电源和敏感类线到线间距0.30mm；USB暂定线间距0.15mm；CAN0.25mm。SWITCHING至模拟／晶振／USB三个类的class-class间距为1mm；USB至普通数字类为0.50mm。四张表的两端确属spacing域，原生DRC实际命中了S_ISOLATE_100。具体pad-pad、hole和shape项目保留各自值，不能用这几行简表替代全部矩阵。

这些值是根据制造能力、现有接口、供电预算和空间预分配确定的教学工程规则，不是把某个铜宽等同额定载流量，也不是把1mm隔离等同EMI认证。封装逃线、功率瓶颈和回流要在后续真实布局中再核。

所有物理CSet的合法via列表只有L28_VIA030_C060：钻0.30mm、铜0.60mm、Through_via。native字符串可能带colon尾分隔符，应解析为列表。原板(52,35)的GND教学via确为**一个唯一dbid对象**，不是仅按同坐标去重；它用于层映射，尚未批准为最终回流via位置。

内层L2／L3留作连续GND参考，普通信号和所有非GND供电CSet均禁止内层etch；GND通过net直接引用P_GND_PLANE允许地铜及地连接。VDDA直接引用P_VDDA_030。USB当前只允许TOP。主板尚未铺实际地铜，L2/L3的“连续”是后续必须落实的意图；底层路线还要检查真实L3覆盖，不能仅因层功能命名就当回流完整。

## 5. USB完整路径、差分及长度规则

已建立3个真实差分对象：

- DP_USB_CONNECTOR：USB_DP／USB_DM。
- DP_USB_MCU_SIDE：PA12_SHARED／PA11_SHARED。
- DP_CAN_BUS：CAN_H／CAN_L；没有继承USB的90Ω或相位预算。

必须同时审查串阻两侧。USB_DP包含J2.A6/B6、U4.1/6、R5.2和R11.2；USB_DM包含J2.A7/B7、U4.3/4和R6.2。MCU侧PA12_SHARED包含U1.33/R5.1/R12.1，PA11_SHARED包含U1.32/R6.1/R13.1。连接器重复pad汇接、ESD流通、上拉短支路和DNP CAN焊盘支节都是真实几何问题，不能因为建了pair就称无分支点对点线路。

D/E的22Ω串阻保留为历史未验证工程取值。当前DS5319和AN4879未找到它的特定强制依据，AN4879说明PHY有内部匹配；后续布局/生产前应按原厂意见评估0Ω／跳接或经实测选择。此课没有静默改原理图、网表或A4工程，因此PCB仍保持基线身份。

USB的90Ω是设计目标；0.20mm宽／0.15mm隙尚未取得匹配该层叠的厂商阻抗确认，CSet名称明确PROVISIONAL。没有把这些数值称为已经实现90Ω。

E_USB_FS_BUDGET实际存入Maximum_Via_Count=2、Phase_Tolerance=“1 MM”、Max_Uncoupled_Length=“6 MM”，两个USB pair的四个成员通过axlNetEcsetValueGet确实继承。1mm和6mm是本教学项目的预算，不是F103/USB硬性门槛；不要为凑数字添加多余蛇形。没有对UART、I2C、ADC、晶振等统一套用等长或最大延时。

## 6. 真实违规、回退与独立长度样板

正式验证在最终板的可丢弃副本进行。每项都全量更新DRC，查看实际source／expected／actual，然后事务回退；最后currentDRC=0、state=t，副本SHA不变。未关闭检查来取得0DRC。

| 刺激 | 原生实际结果 |
| --- | --- |
| 普通信号0.10mm窄线 | Minimum Neck Width，要求0.15mm／实际0.10mm |
| 电源0.30mm线延伸10mm | Maximum Neck Length，要求1mm／实际10mm，source=P_POWER_060 |
| 同一线临时给net加MIN_LINE_WIDTH=0.20mm | 该违规消失；回退后临时override不存在 |
| 两线边缘间距0.10mm | Line to Line，要求0.20mm／实际0.10mm |
| SW至ADC边缘距0.50mm | class-class要求1mm／实际0.50mm |
| 不在列表的合法结构via | 四个层各产生Via List DRC，合计4条 |
| USB_DP放3个via | Maximum Via Count，ECSet要求2／实际3 |
| L2布V3V3线 | Allow on ETCH Subclass违规 |
| L2建立明确GND的填充shape | 允许，0DRC；回退后主板未残留该铜 |

前两项验证的是普通宽度和颈缩预算的联合作用，不能改写成“直接命中0.20／0.60mm普通最小线宽DRC”。

主板多数器件未放置，另建一个独立校准板验证长度规则，而没有布完80件。该样板是自定义校准端点，2器件／4引脚／2网络，非真实USB器件。P走20mm、N走27.6mm时，原生Phase Tolerance明确报告要求1mm、实际7.6mm；Uncoupled Length报告要求6mm、实际10mm及17.6mm。回退并改为两条20mm平行线后0DRC/state=t，保存独立重开。

进一步用axlPinsOfNet读得每网2pin、unconnected=0、unplaced=0；四个实际pin坐标与两条原生20mm线端点逐一一致。net->pins在该样板中返回0，不能用这个属性单独推断断开。

该原生电气DRC内部自动尝试bem2d，日志有Field solution failed。记录保留；这里采用的是与独立几何一致的**纯长度规则作用证据**，没有拿内部求解失败输出证明阻抗、传播延时或SI/PI波形。也没有因此屏蔽合法DRC。曾准备安全停止时进程已自行正常退出，身份检查未匹配，实际上没有停止任何进程。

## 7. 实操路径与复现要点

本机实际使用Allegro17.2 S045官方-nographic/SKILL通道；桌面native pipe尚未恢复，不能说已经点击过CM菜单。已熟悉的菜单对应关系来自官方文档：Physical／Spacing CSet与Net工作表、Electrical Routing／Differential Pair、Analysis Modes和File→Export→Constraints，GUI操作另列待补。

实际步骤：

1. 只读盘点第27／28课输入、当前许可可用constraint names和modes；校验源板SHA。
2. 复制第28四层板到本课native目录；写入DEFAULT、命名CSet、单域网类、实际net成员、类间关系、差分组和ECSet。
3. 写后检查真实属性及成员域；保存后另起进程逐网络、逐层读回，确认不是只建立了空分组。
4. 按实际地参考意图补GND独立CSet，禁止其他供电线穿内层。
5. 在隔离副本进行上述挑战和回退；建立全连接长度校准板。
6. 用官方techfile.exe -w导出TCF，再用-w所得TCF执行-c比较，报告“No objects were updated.”，源板SHA不变。
7. 独立核对69net／272逻辑pin、全部已放物理pin和pad、板框/keepin/keepout、完整层叠及唯一via；完成验证、预览和SHA清单。

TCF是技术约束导出，不将它冒称含全部net对象的完整DCF。实际net/class/pair/继承关系另有原生TSV。CM GUI的完整DCFX导出尚未实操。复现时先读spec、input_identity和failure_history，创建新的目标副本、SCR输出路径及日志目录；不要直接重放历史固定输出路径覆盖验收证据。脚本、原生启动参数和实际exitCode均保留在scripts／logs中。

## 8. 本课发现的失误及长期规则

1. 本机' all及多域列表创建NETCLASS虽返回group，域flags却全nil，属性返回(nil nil)。后者在SKILL里仍是真值。已改为单独physical／spacing／electrical域，逐net检查实际类及实际CSet，保存重开再验。不是“setter没有抛错就已应用”。
2. AddProp应使用list(dbid)和嵌套name/value pairs；flat四项不能当作成功设置两个属性。
3. 官方接口说明的一段将drill结构误写为make_axlPadStackPad；本机官方实例用make_axlPadStackDrill，已按实例修正。正方形用SQUARE，等宽高RECTANGLE曾被拒绝；原生缩放舍入警告保留。
4. 本版本axlNetEcsetValueGet的字符串net名用法被拒绝，改传dbid；失败事务自动取消，不当作完整挑战。
5. 初次完整挑战耗61秒，超过旧55秒启动器窗口。该次exitCode未知仍保留，未倒填成功。最终120秒窗口内实测111秒正常exit0，COMPLETE、回退和SHA均齐。
6. 自定义验收器初版错误解除了SKILL字符串引号，截断MKS单位，并误判via列表尾colon；已保留失败报告，修复解析后543项通过。不能为了PASS放弃单位核对。
7. fgeo_bv通用映射不包含真正DESIGN_OUTLINE；最终直接读取root板框/keepin对象，并与第28的机械专用导出逐字节比较。几何未变的结论覆盖22个已放物理pin及其逐层pad，不只看272个逻辑引脚。
8. 两层与四层制造条件分别建规则；“基本能制造”不等于阻抗、回流和装配已经合格。

本课的完成边界为建板约束与规则运用。下一阶段从最终v3继续真实器件布局，把去耦供电回路、buck热回路/小SW面积、晶振与ADC保护、USB保护顺序和连续地参考落实到实际位置、铜和路径；尚未布局的主板0DRC不能替代这些工作。
