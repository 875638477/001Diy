# HI 第38—50课：电源、ESD与普通接口精细走线专项记录（2026-10-21）

## 1. 本记录的范围与当前状态

本专项负责工程路径、线宽/分层/过孔及实际返回检查；f29 是唯一 Cadence 原生执行者，根任务负责全板合并和最终课程验收。本记录不得用来将“电源阶段通过”替代“整板已完成”。所有源码、中转、失败方案、原厂资料和审查结果均在 01AIEDA 内。

当前已独立核验到 **03c 电源/母线检查点**：两板均 80 个逻辑器件、69 个实际网络、272 个逻辑引脚（其中6个NC伪网端子，实际有网266端子），剩余连接137；这显然不是整板布通。02d 专项1798项、03c 专项1880项均0失败，只代表各自明确范围。

后续候选入口（原生执行前仍须合并和DRC）：

| 文件 | 作用 | 当前身份 |
| --- | --- | --- |
| power_critical_paths_01.json | 输入C3微移、VIN/SW/BOOT和近地过孔 | 已实际实施并在后续检查点保留 |
| power_paths_02d.json | 输入保护、输出C5/C6、LDO、反馈与取样返回桥 | 已实际实施 |
| power_star_03c.json | MCU内向0.6母线、局部逃线及模拟滤波前供电 | 已实际实施 |
| rules_profile_2L_69nets.json | 两层69网分组及完整物理/间距规则 | 已原生应用，逐网/逐层核对 |
| interface_CAN_routes_04.json | CAN_H/L、R15终端至J3及TX空闲支路 | 具体几何候选 |
| CAN_local_supply_05.json | C11/C12/U5供电、直接TOP地返回和双地过孔 | 具体几何候选 |
| V3_peripheral_distribution_06b.json | CAN/headers/上拉与调试等全部外设V3分发 | 具体几何候选 |
| ESD_ground_routes_04c.json | U4/C10实际地返回和跨DP列的VBUS桥 | 已完成全组合几何筛查，待原生与真实参考面审查 |
| routing_policy_interfaces_04.json | CAN/UART/I2C/SPI/SWD/BOOT/USB辅助约束 | 普通信号路径规划依据 |

上述文件均在 [本次专项目录](../examples/lessonHI_38_50_20261021/engineering_power/)；旧02/02b/02c、03/03b、ESD04/04b是失败/过渡历史，不作为当前执行入口。

## 2. 真实输入、原厂依据和身份

输入沿用 G 最终板，不重新虚构网表或只凭封装中心定位。G 两板均80×60mm、四个安装孔(5,5)/(75,5)/(75,55)/(5,55)，J2(40,3.675)开口朝−Y。器件具体引脚、焊盘边界、已有27段TOP局部铜、原地过孔和真实参考面均从原生重新导出的 normalized/TSV 取得。

03c固定文件：

- 两层 native/HI_2L_power_2L_b003c.brd，SHA256 A86488E37C98A7135BECF48DC7130D2461F0DCA12E5E6A53CD52EBA77CBE6082。
- 四层 native/HI_4L_power_4L_b003c.brd，SHA256 F673C67C06BF169626A5D08E05FE4D541CAC9241020152C1A76AAA65B10A5392。
- 冻结输入在 inventory/checkpoints/power_2L_b003c 与 power_4L_b003c；不能用不断更新的 current 反向冒充这次审查输入。

[工程原厂资料清单](../examples/lessonHI_38_50_20261021/engineering_power/source/engineering_sources_manifest.json) 保存文件SHA、原副本、原厂URL及页/章节。TPS54202 RevC布局图、TLV755P RevD布局/热条件、TCAN33x RevF 7.4/7.5、原DE电路与mcu契约分别作为依据。原厂图给回路/电容/引脚布局要求，本文坐标是针对本板的工程选择，并非声称厂商推荐了本板坐标。

## 3. buck输入热回路、SW/BOOT、输出取样与LDO

1. C3从(26.2,18.6)180°微移为(26.2,18.0)180°，真实正端(26.0984,18.0)、负端(24.5236,18.0)。这一移动打开VIN正常0.6mm通道，而不是凭电容中心“看起来近”。
2. U2 VIN3(24.2,20.05)先0.25mm短逃0.95mm，之后0.6mm到C3；U2 GND1(24.2,21.95)先0.25mm短逃0.6mm，再0.6mm到(23.7,22.55)/(23.7,23.35)双过孔。C3负端0.6mm接(23.2,18)/(23.2,18.8)双过孔。
3. SW始终TOP：U2.2先0.25mm短逃1.15mm后扩0.6mm至L1短引脚。只在 HI_U2_SW_ESCAPE 小区域把最大颈长1.0调整为1.2，其他线宽/间距/过孔及全局1.0不动。BOOT经C4回SW，**C4.2不是GND**，不能把自举电容误画成普通旁路地电容。
4. L1输出到C5/C6正端0.8mm；两个输出电容负端有直接0.8mm TOP连接和地过孔。输出储能电容、电感/电容具体MPN和有效电容量仍按原开放项核查。
5. R1/C7/R2及U2.4反馈保持安静TOP短连接，R2地在反馈侧接近地过孔；未声称严格独立Kelvin地或完成补偿环稳定性测试。
6. V5取样先从C5正端接过孔(15.5,22)，BOTTOM经y12至(31.8,19.1)再回TOP接R1。此处是低阻输出电压的取样前馈支路，敏感FB节点本身未拖成长底线。为跨越它在两层底地的切口，真实TOP GND从C1地过孔(13.8,18.3)经(13.8,15.5)到(16.5,15.5)过孔，不能只说底层“有整面地”。
7. LDO输入主干0.6mm从输出C5到C8，再入U3.1并使能U3.3；输出U3.5到C9正端0.6mm。C8/C9负端通过直接TOP0.6mm铜与U3.2相连，各有近地过孔。采用真实DBV引脚位置，没有把原点当封装中心，也没有误接NC4。
8. TLV755无反向阻断。SWD/排针只允许VTREF/电源参考输出，禁止外部回灌；正常总负载150mA、环境0—40℃仍是设计边界，实际铜散热与温升未测试。

两层TOP到底地介质约1.524mm，四层TOP到L2约0.2104mm。相同端点连通不代表相同高频回流、环路面积或EMI表现。本轮四层02d已真实生成L3 GND，不能把“层功能写GND”当已铺铜。

## 4. MCU分发、局部例外与外设供电

C9先以0.6mm到过孔(30.7,32)，BOTTOM0.6mm经(30.7,24)到(37,24)，回TOP后在MCU体内形成南侧/右侧0.6mm母线。U1.24/.36/.48仅各1.25mm的0.25mm内向逃线，VBAT逃线1.453553mm，保留原有外向去耦回路与C17支路。

03b原生出现的2条Max Neck，不是内外两边被合成2.6mm，而是新LEFT/SOUTH区域1.3误收紧了原G31外向实际1.3657mm。03c仅这两局部恢复既有1.4预算，NE仍1.5、全局仍1.0；严格1.3产生2DRC、恢复1.4后0DRC的证据保留在原生批次日志。没有静默扩大全局线宽例外。

间距域不能按类名猜成员：四层GND和V3V3共用 NC_POWER_LV_S，因此同一POWER间距区域覆盖两者；两层使用独立 GROUND 与 POWER 两份源复制。独立审查核实每份实际只把 smdpin_line/line_line 改0.2，其余字段原样保留；物理副本只改声明的最大颈长。

两层底层V3桥会局部割地，已实际增加0.6mm TOP地桥，从C13地过孔(32.45,25.2748)至C9地。审查排除所有平面，仅合并真实TOP GND线/焊盘/过孔铜环，仍证实两点处于同一TOP铜连通块，防止用“同GND网”代替实际短返回。

滤波前模拟供电从C9左绕J10：(28.4,32.35)→(22,32.35)→(22,37)→R26.1。它在滤波前多一些长度，保持ADC输入TOP短路径；R26后的VDDA不供数字负载。

外设供电06初稿从C9的0.6主干在(33.3,24)直接分支，经过孔(33.3,22.5)转TOP外围y1→右边x78.2→北侧y58.2→左侧x1.8，J6只在y26进入，不占SPI的x7..35/y27..36。所有主干及支路0.6mm，无新增细颈；CAN、7个headers、I²C/复位/BOOT/USB控制上拉均列真实端点。CAN电流、排针负载不得经MCU焊盘0.25mm颈部。长外围铜必须有邻近真实地参考，不能把“走外围”本身当EMI优势。正常外部GPIO+排针总负载仍为10mA合计；铜压降示例只用于估算，非温升/载流认证。

CAN局部05明确C12→C11→U5 VCC正常0.6mm，U5 GND→C11/C12负端直接0.6mm TOP返回，配(62.6,14.73)/(60.8,15.8348)双地过孔。不是将去耦电容只连到远处大地。

## 5. ESD、USB辅助与接口拓扑

ESD04c的前提是U4移至(40.25,11.4)180°，GND2为(40.25,12.7)；旧U4位置不能直接执行此文件。地回路向体内到(40.0,11.4)/(40.5,11.6)双过孔，避开D+/D−贯通列。C10负端0.6mm到(43.8,10.7764)/(43.8,11.5764)双过孔。

U4 VBUS5先正常0.4mm直下到(40.25,9.3)过孔，BOTTOM0.6mm短桥至(43.8,9.2016)过孔再TOP到C10正端。不能在TOP直接穿D+列。四层TOP仍看真实L2；两层BOTTOM VBUS桥会在TOP数据线下形成有限参考缺口，后续须核真实fill/近地返回，不能称等同四层或已证明90Ω。新左过孔铜环与自身VBUS焊盘搭0.05mm，钻孔距SMT铜边0.10mm；实际阻焊孔/盖油/吸锡工艺尚需专门确认，不能只凭几何称装配合格。

接口政策按各自拓扑：

- CAN为500kbps、≤1m非汽车台架；H/L在U5→R15终端焊盘→J3直接短走，R15仅物理总线两端装120Ω，中间节点DNP；无强行蛇形等长，板上差分阻抗未认证。两层普通间距0.2，四层实际CAN类间距0.25，不能把四层降为0.2。
- CAN TX/RX经R12/R13选择，USB与CAN互斥装配。DNP不删除铜支节，须度量仍存在的PA11/12选择支路。R14是10k空闲上拉，不是源阻尼。
- UART TX先走MCU→近端R16 33Ω，再长走至J4。RX的R17=0Ω在接收端，不能称外部驱动器的源端终端；R18空闲上拉可短分支。115200bps/短线只是建议初次台架条件，原契约没有已认证速率/线长。
- SPI契约≤1MHz、外线≤10cm；SCK/MOSI/NSS分别先经近MCU R21/R22/R23 33Ω再到J6，MISO R24=0Ω在MCU侧不能冒称外部源端阻尼。不对四条SPI线随意统一等长；需结合真实边沿、外部时序/负载/线缆再定偏斜预算。
- I²C默认100kHz、2.2k上拉，≤100pF是包括PCB/器件/连接器/线缆的总预算。≤400kHz仅RC设计包络，DS5319 Rev20 Table41脚注与Table42条件差异保留，硬件/固件Fast-mode未验证。无SCL/SDA等长要求。
- SWD使用自定义1×6引脚表，VTREF只检测，SWCLK与SWDIO不接普通GPIO负载；J7为复位跳帽/排针，不是实体按键。BOOT默认下拉，服务跳帽经1k到3.3V；F103C8系统ROM是USART1引导，不能把USB插口称ROM USB DFU。
- CC1/CC2分别有独立Rd，不能合并；USBLC6只保护本数据/电源钳位网络，不能宣称CC/SBU也受其完整保护。VBUS仅检测/ESD轨，不能并入V5。Q2默认关断、R11上拉支路需短，控制线避开数据对。

波特率低不等于边沿慢；GPIO必须用满足时序的最低合适驱动速度并实测，当前未写固件，不能默认已配置2MHz输出模式或保证了某个slew。

## 6. 实际失败、修正与审查方法

| 失败版本/问题 | 发现与修正 | 保留证据 |
| --- | --- | --- |
| 电源02 TOP V5取样 | 与VIN主线交叉；改明确BOTTOM取样 | rejected_V5_sense_TOP及02历史 |
| 02b VIN y13 | 穿C2地过孔/地线，真实短路 | 失败几何JSON、root交叉预审 |
| 02c VIN y11.95 | 未选用，避免与BOTTOM y12取样长距离正反面重叠 | 候选保留；02d改y10.6 |
| 03原模拟供电x28.4 | 与ADC输入y34横段交叉；03b左绕x22 | 原方案、全组合预审记录 |
| 03b局部颈长1.3 | 覆盖原G31实际1.3657；03c仅局部恢复1.4 | 原生2DRC及恢复0的对照 |
| 旧ESD地via40.9/11.5 | 会撞D+贯通列；改体内40.0/40.5 | 04候选及跨组通信 |
| ESD04b VBUSvia40/8.95 | 局部审查漏DM merge y8.6，完整合并发现短路；04c改40.25/9.3 | 04b历史、f27 combined_v8 |
| 审查器Lisp nil | null与False比较造成假失败，曾误报BOTTOM允许；核raw后纠正，实际原生规则正确，无需放宽 | review_power02d_failed_parser_v1.json |
| 逻辑引脚/层映射计数 | J2含两个机械孔，需排除后才272；两层via导出L2/L3为figure=nil，不能当真实新增铜层 | 修正脚本与原始读回 |
| 整个洞bbox过估 | V5取样产生L形void，整bbox误包围CIN地返回；按官方弧规则重建后核真实面积 | 原失败及官方axlPolyFromDB副本 |

官方 axlPolyFromDB 的半径属于“前一个点→当前点”，正数圆弧在局部Y轴左侧、负数在右侧，圆弧不跨象限。不是把半径绑定到下一段，也不是KiCad bulge。已封装 [cadence_poly.py](../examples/lessonHI_38_50_20261021/engineering_power/scripts/cadence_poly.py)，0.5°分段后面积与原生值差<0.01mm²，再把洞外扩/外边内缩0.0001mm作保守返回覆盖。只读几何近似，不是电磁/电流仿真。

## 7. 验收证据及边界

[02d独立审查](../examples/lessonHI_38_50_20261021/engineering_power/readouts/review_power02d.json) 1798项0失败；[03c独立审查](../examples/lessonHI_38_50_20261021/engineering_power/readouts/review_power03c.json) 1880项0失败。检查了实际逐段线宽/坐标/过孔层映射、native端点证明、69网两层规则、局部复制字段、CIN至U2地过孔之间0.6mm真实参考面直返回条带、关键地过孔整个0.6mm铜盘在真实地面内以及TOP返回桥。关键电源过孔未只剩一条细热焊盘辐条；所导出的参考层GND连接线宽均≥0.6mm。

CAN04+05对03c实际铜8239项预审无问题；加V3分发06后24532项预审无问题，均仍标“候选需原生”。这些数目是脚本检查项，不应包装成覆盖全部工程物理条件的认证。后续任何MCU/USB/普通信号走线或挖铜后，必须重新核回流、GND连通块/瓶颈、最窄铜颈、热焊盘、参考面缺口，不可沿用旧PASS证明新版本。

DRC0、无飞线、同网/最小连接数一致，均只是必要条件；不能替代真实回流设计、纹波/温升/稳定性、USB通信/ESD/EMI实测。

## 8. 持续保留的制造和硬件开放项

USB4105默认S=0.95mm从器件安装基准面计，并非“从PCB底面突出0.95mm”，与1.6mm板的穿透/焊接工艺尚未匹配。两层OSH公开阻焊桥下限0.1016mm与继承USB名义0.100mm差异仍未关闭。USB历史22Ω及实际差分阻抗/板厂确认未关闭。具体R/C/headers物料的高度、容差、DC偏压下有效电容/ESR及LDO实际热条件仍未测。默认package height=1mm只是一项默认数据库值，不能证明实物装配合格。

输入9—16V仅隔离限流台架，0.5A保险丝不是精密限流器；无任意TVS替代故障电压验证。TCAN332总线故障边界±14V，器件内部ESD额定不证明整板系统合规。不增加未经匹配的TVS/CMC、LC或随意改变原理图来“消除”布线问题。


## 9. H45实际返工：已通过DRC的供电路径仍可能阻断接口走廊

根任务在真实SPI规划中发现：03c BOTTOM x30.7/y24—32的垂直0.6mm V3主干，将西侧MOSI/SPI出口挡住；TOP同区已有C9焊盘与C13-C9地桥，几何搜索被迫把MOSI绕到y13、约80mm。该自动候选未被接受。问题是可布通性/功能分区的联动，不是用“03c DRC0”证明整板布局走线已经合理。

当时返工候选为 **STAR_reroute_07b.json**（现为失败历史，最终07c见第12节），配 **V3_peripheral_distribution_06b.json**，替代06的旧取电支路；07原版仅为失败历史。

- 按net=V3V3、BOTTOM、width0.6和两端点唯一匹配，删除原(30.7,32)→(30.7,24)及(30.7,24)→(37,24)两段。仅删除这两条真实segment，不能删整个合并path而带走其他电源支路，也不能只加新铜留下并联回路。
- 新BOTTOM主干(30.7,32)→(37,25.7)→(37,24)，全0.6mm；让出SPI从x31.65/y27.9向左的空间。
- 外设改从已有STAR过孔(37,24)在TOP全0.6mm到(33.3,24)→(33.3,22.5)，不再增加原06计划的第二个过孔或BOTTOM横支路，仍不经MCU细颈取电。06b其余外围分发保留。
- 新BOTTOM槽形状改变，须同时审实际返回。保留C13—C9直接TOP地桥，并增加U1.23→(36.48,24.75)→(37,25.27)→新地过孔(38,25.27)，分别0.25/0.25/0.6mm，跨过BOTTOM x37电源竖槽回到东侧真实地面。
- 最初“从GND脚直接0.6”会对相邻VDD焊盘只留0.05mm；原07改成短颈后仍太早上转，靠近GPIO22且正常地段到已保留V3端部仅0.10mm。真实焊盘和所有既有铜比较后才得出07b。新0.25mm地颈实际1.465391mm，因此仅GND的 HI_STAR_RETURN_GND 小TOP区域最大颈长1.5mm；其他全局/电源规则、全部间距字段不动。不是将1.0全局放宽。
- 07b+06b+CAN04/05与冻结MCU6实际铜预审31359项0问题；根任务还须核最终USB/GPIO/SPI/机械并执行原生重布。此条为候选证据，不把未执行返工写成最终完成。之后必须重新fill并验证删段确实消失、关键端点不丢、实际地桥与参考面瓶颈、规则挑战和新进程重开。


## 10. SPI源端/上拉与滤波前支路的再次协调（跨日继续）

根任务的普通搜索先连接R25上拉与R23源端时，会在BOTTOM x29.95/y26.8—32.35竖起一堵新信号墙，再次阻断SPI。该候选未接受，改为明确MCU→近端串阻的源端顺序，再单独走上拉服务支路。

最新根计划 plans/SPI_source_explicit_v5.json 的10操作已独立读取并保存源副本。SCK使用TOP x34.385，真实R24.1焊盘右边和NSS x34.8竖线之间各有0.215mm铜间距；MISO先水平到33.6,28.25再竖向，不用斜线去挤SCK。MOSI/NSS同样保持直接TOP源端，未为了A*网格限制给这三条源端线硬加过孔。R24仍是外部MISO接收端0Ω位置，不因此变成源阻尼。

NSS上拉支路从MCU向内，经(39,26.2)过孔、BOTTOM至(32.2,22.0)过孔，再TOP到R25.2；近地过孔(31,21.6)。原signal via(32,22.2)到R29.1 BOOT1真实焊盘仅0.114418mm，不满足smdpin_via=0.2，被独立筛出并改动；原ground via(32,23.2)会直接碰BOOT1，亦保留否决记录。新的地via至R25 NSS pad仅约0.2642，但实际原生smdpin_via=0.2，不能套用“所有电源间距都0.3”的简化判断误报。内侧过孔到07b地返回via中心约1.366mm；西侧信号/地过孔中心约1.265mm。约19mm、2via的上拉分支在33Ω之前，仍需结合低输出边沿、SPI≤1MHz及实际参考检查，不把电阻或低频率当成支节不存在。

另一项参考面冲突是BOTTOM SCK沿y32.75时，会长期贴原TOP V3预滤波供电y32.35横段。不能为连通留下约6.4mm缺参考后仍称“基本回流已满足”。把整段TOP移到y31.95也不可行：C8 V5 0805焊盘上边31.508，0.6mm线下边31.65，仅0.142mm，低于0.3；只检查相邻0.6mm线会漏掉真正焊盘。

独立预案 VDDA_prefilter_reroute_08.json：

- 精确删除旧TOP预滤波3段，保留22,37至R26.1的原横段，不留下旧x22悬空电源铜桩。
- C9→TOP(28.8,31.95)过孔，BOTTOM正常0.6到(9,31.95)过孔，TOP x9上至37再到22,37。R26后的VDDA/本地电容/VSSA完全不变。
- 若left via仍在22，则TOP x22纵向供电仍会在SCK下产生一次约1.2mm参考槽；优选x9在SCK x11..31左外侧，避免把小缺口默认当作已关闭。
- 两个共地stitch在(27.5,31.05)/(10.2,31.05)，距各电源过孔约1.581/1.50mm，前者略大于一般1.5mm审查目标，明确记录而非伪称都小于目标。后续需实际TOP地生成和参考条带覆盖证明。
- SCK优先y33.05，与BOTTOM电源y31.95的铜间距0.70；源端33Ω顺序不变。新增约26mm只在低电流模拟滤波前，名义铜阻约0.021Ω，未据此认证模拟精度/温升。该方案仍为候选，须等外部SPI路径合并再决定是否原生实施，避免只看局部又制造长桥。

SPI v5 +上述08候选+07b/06b/CAN04/05，对冻结USB8所有实际铜的独立预审50629项0问题。它没有涵盖尚未实际实施的GPIO6/全部外部长线，不能扩大成全板验收。GPIO6已由另一专项将PC14改东侧出口，避免新STAR对角与旧PC14西端仅0.165685mm的真实斜向近距。

## 11. ESD过孔阻焊实际读回：名义零余量已明确

logs/reopen_usb_esd_4L_b008/hi_usb_key_mask_apertures.tsv 实读：

- U4.5中心y10.1，PIN/SOLDERMASK_TOP半高0.65，开窗下边9.45。
- VBUS左过孔中心y9.3、钻孔半径0.15，孔上边也是9.45。
- 此过孔VIA CLASS的TOP/BOTTOM开窗均为NULL，只表示无独立via开窗；邻近器件焊盘开窗与孔边仍名义相切，不能据此声称孔可靠盖油或防吸锡已确认。
- 铜环搭自身land 0.05、钻孔到SMT铜边0.10仍是正确的铜几何描述；制造上还要考虑阻焊注册、钻位公差、tent/填孔/装配工艺，当前不能释放生产。

四层USB8原生0DRC和只读重开并不关闭这一制造条件，field-solver自动失败也不提供SI认可。本专项保留具体开放项，不用临时改阻焊去掩盖。


## 12. 2026-10-22：07c真实验收及两层SPI协同设计

07b的独立几何比较没有发现间距问题，但原生postcritical b009报出唯一MaxNeck：新返回细颈1.4654mm在旧G31_GND_ESCAPE的1.4mm区域内，新小区1.5mm不能覆盖旧区更严限制。不能据此扩大旧G31或全局预算。07c把正常0.6mm起点提前到(36.952,25.222)，保留(36.48,24.75)前一拐点；完整0.25mm新颈长1.397508801mm，处于原1.4mm内，新小区也改1.4。与b009真实全部铜只读预审966项通过；b010从USB8稳定源重新执行而非叠加失败候选。

原生两板postcritical b010均0DRC且新进程只读重开/hash稳定：

- 4L native/HI_4L_postcritical_4L_b010.brd，SHA256 A9215927856EF4D3AD6D6CBAE3F227365EE09640821C8403336863C0A35F9437，473段/58via/63remaining。
- 2L native/HI_2L_postcritical_2L_b010.brd，SHA256 76ED85DA3999A7DAFBDF9EB99EEC425B480A5EAEB49843BF970F8664707DE0AF，58via/62remaining；actual410 ETCH segments含生成热焊盘，不把总段数当手工走线数。
- 04/05 CAN、06b外设取电、07c返工及根source5等已实际执行。上述是固定历史检查点，后续b011增加地stitch及其他数字线时仍以最新native/current为主。

两层外部SPI起初按根v5电气候选评估：SCK BOTTOM y29.95下方有U3 VIN/EN/VOUT铜，MISO y30.8下方有C8/C9正端；即使后面铺TOP GND，也无法在真实电源焊盘上变出参考地。把四层SCK via单独搬到(31,29.95)又会与两层MISO via(31.5,29.85)相交，这个跨变体单点照搬建议没有执行。后续必须把四线和返回一起设计。

本专项产出 SPI_external_2L_engineered_v9.json（35操作：3条精确删铜、15route、8signalvia+9GNDvia）。按b010真实铜/过孔/保守焊盘AABB比较28656次0问题；MCU专项另作27441次独立比较，无小于0.2mm异网铜间距，无钻孔进入SMD pad，离HSE moat最近6.489mm。两份预审均不是原生全板验收。

- 源端source5不改，串阻顺序保留。SCK局部BOTTOM桥8.95mm在y29.95，之后回TOP并在西侧早降至J6.2；源via(30.8,29.95)与MISO via(31.65,29.77)联合定位。
- MOSI局部BOTTOM先y28.3再28.5，避开L1 SW copper land投影和C8/C9既有GND via；之后回TOP到J6.3。仍有TOP V5投影，不声称对面全地。
- MISO BOTTOM y30.8→TOP到J6.4；NSS BOTTOM y32.3，避J10接地stub(23.73,33.052..34)，再TOP到J6.5。MISO的外部接收端0Ω不等于源阻尼。
- 第一根0.6mm BOTTOM guard y29.25从既有C9共地via(28.6,29)引出，为clock/MOSI局部提供同层返回；第二根y31.55、0.6mm guard直连(27.1,31.55)/(21,31.55)两个GNDvia，位于MISO/NSS之间。
- 仅把低电流、10Ω前的TOP V3预滤波横排y32.35上移0.20至32.55、拐点28.4改28.2，给第二guard地via提供真实间距。精确删原3段，不留电源铜桩；R26后VDDA/ADC/本地滤波不变。原08长BOTTOM电源桥没有采用。

返回专项 readouts/SPI_external_2L_v9_return_plan.json 的8个signalvia最近GNDvia中心距0.856—1.490mm。冻结真实BOTTOM地面减去新信号线0.3mm保守halo和signalvia半径0.6mm切口，再合入合法GND guard/via，全部新GNDvia和两根guard在同一预测common GND连通块中。这仍是几何规划，需原生动态铜刷新后以实际铜重做。

为避免把“地网连通”当成返回合格，另将预测common GND腐蚀0.299mm，寻找至少0.598mm宽的地通道核心，沿桥每0.1mm采样（端部0.7mm过孔转换区单列）。SCK/MOSI/NSS中心至最近宽地核心最坏0.699/0.714/0.699mm；MISO源侧拥挤拐角局部为1.642mm，坐标约(30.893,30.757)，需最终真实填铜审查并明确条件。此数值不是板厂阻抗/高速认证，也不隐藏成“全程等距参考”。SPI初始<=1MHz并采用最低足够GPIO输出边沿，仍须看实际边沿/负载，低时钟频率不能消除快速边沿反射。

TOP异网铜加0.3mm预计GND让位区，与上述BOTTOM桥中心线重合长度分别5.70/12.53/6.80/7.84mm（SCK/MOSI/MISO/NSS）。这组数值明确记录其同层返回意图，不把这些区域宣称为连续TOP参考。J6仅pin6为地，外部排线/负载回流、引脚次序和边沿仍有限制；未改变原理图或伪造相邻地脚。

四层原根外SPI v5另审：对b010原生已生成L2/L3地铜投影，全部0.2mm信号铜足迹除自身J6 THT正常反焊盘外均被真实参考覆盖。只排除实际自身pad AABB+0.301mm，原始缺口面积仍保留。新signalvia antipad尚未生成，最终刷新、返回stitch及近SW MOSI耦合仍需核，不能靠层名宣称完整性。报告 readouts/SPI_external_4L_v5_actual_L3_projection.json。

局部via均没有钻入实际SMD铜，但bodyExtent/PlaceBound并非已核MPN实体外形。特别C9附近via钻边与库包围范围有约0.039mm投影重叠，真实物料实体/tenting/贴装吸锡及容差需保留；不能将数据库包围框直接称实物合格或判定必然撞本体。

## 13. 原生地铜小圆弧舍入与审查工具勘误

cadence_poly.py继续按官方axlPolyFromDB半径属于前点→当前点、正负表示圆心局部Y轴左右以及象限切分语义处理。b010有两条极短水平弦在舍入后使两个圆心的左右判别均满足浮点符号，旧断言因此拒绝读取；没有据此忽略整个孔洞。保留原解析器cadence_poly_v1_before_rounded_arcs.py，仅在模糊弧的最大弓高<=1e-5mm（10nm）时用弦，并在ROUNDED_ARC_FLATTENED逐项记录。正常弧保持原方法，其他歧义仍报错。

arc_b010_area_audit.json涵盖两板10个真实平面，实际被折弦的最大弓高5.43nm，小于保守外缩/孔扩0.0001mm（100nm）；最大原生面积与转换面积差0.003342mm²。孔列表nil也必须显式转为空列表，不能将nil误当有孔或漏掉全平面。SPI预审脚本中一次PowerShell多行替换误加首尾引号产生SyntaxError，已修复并重跑；没有因此修改设计或放宽原生规则。

本节新增全部方案仍属于独立工程准备/预审。最终完成必须有当前原生板、全量DRC、实际地面/护线/参考缺口验证、连接证明和新进程重开；不可用此目录候选或旧manifest的PASS替代最终状态。

## 14. SPI候选到真实b012的阶段性完成（2026-10-22）

最终实际采用SPI_external_2L_engineered_v10.json（35操作）及SPI_external_4L_engineered_v6.json（20操作）。v9、08及其他失败候选仅留历史。v10把MISO源侧预测至宽地核心最坏距离从1.642mm改善为约1.453mm；这仍是预估值，不能改写成电磁仿真或阻抗认证。

原生执行者提供了全板DRC计数、模式与时间戳；两板执行均0DRC，四条SPI真实端点、guard及新增地过孔图连接证明通过，HSE删唯一anchor负测试通过，轻量新进程重开源SHA稳定且branch orphan=0。固定实际检查点：

- 2L：inventory/checkpoints/SPI_external_2L_b012，SHA256 24DDF112FFCC9B7A8F44401B406BBBCEC7523B3A5F42E73A816A7D3349BCF602；58剩余连接、76个via。
- 4L：inventory/checkpoints/SPI_external_4L_b012，SHA256 DB0FB0243BA036E986976862DD00389A41F79FBF8E6592CD4243590EAB7338BD；59剩余连接、68个via。

这里完成的是指定SPI布线批次，尚未完成全板布线。最终所有普通数字线加入并刷新铜后仍须复核真实回流与共地宽颈；不能把上述历史DRC0扩大为后续板版的最终验收。

## 15. MCU右侧10脚联合返工的失败与当前边界

实际PC14旧末过孔挡住SWO、R28原地焊盘挡住PB5、旧quiet stem及C15地线挡住PB9，须联合微调PC14末路、R28、C15与晶振岛唯一接地stem。只核单脚0碰撞或最近地过孔距离，不能证明其他9脚还能接通；source v1/v2/v3在逐条长路规划时封闭口袋，保留为失败历史。v2为满足1.5mm目标加入的三颗小地via反而封路，已撤销，1.5mm是工程审查目标而非任意制造DRC。

v4把PB9改TOP连续并较大移动C15/C16，电源回路中心线总长由约4.849mm变8.040mm、几何围面积由2.269mm²变3.500mm²，属于不利代价，未作为终版采用。当前源端草案v5保留C16原位、C15仅移至x47.3；TOP连续引脚不保留闲置信号via或BOTTOM死端，真实需要换层的脚才用私有小通孔。

私有HI_VIA026_C052_TENT为机械钻通孔：0.26mm钻孔、0.52mm铜、名义环0.13mm、独立mask=NULL；原生两板嵌入定义已验证。21字符旧名字TENTED超过PADLIB20字符限，正式采用19字符TENT。允许小via必须在全部实际导体层局部region批准；neck/spacing例外只限外层，不能为过孔许可开启L2/L3信号etch。

当前quiet岛重构候选的唯一anchor为(46.35,29.4)。VDD48/局部3V3粗支路和VBAT脚源支路对窄stem有有限投影，不能仅写VBAT或宣称整个投影无其他铜。普通I2C/GPIO仍禁止穿岛及真实guard加0.3mm间隔的shadow；最终全局TOP地也须沿guard铜完整避让，不能造成第二接地点。只有新原生板上删除此唯一anchor后，quiet电容/护地保持局部连通但与application GND完全断开，再还原并DRC，才可接受新方案。

长路联合预审发现SCL最初撞R30的3V3供电，绕行又遇BOOT_SERVICE过孔；不能用仅源端PASS掩盖这些实际冲突。当前仍在source+全部10长路联合设计，未运行Cadence、未声称该候选完成。最后基线已切到原生USBaux b014，旧b013失败6DRC不作为输入。
## 16. 右侧完整v10候选冻结：源端、长路、返回与制造范围一起审核

当前候选RIGHT10_FULL_2L_v10.json和RIGHT10_FULL_4L_v10.json各88操作，以原生USBauxb014为只读基线。两板actual铜/过孔/真实pad AABB独立比较102200/100438对0问题；16个旧对象删除均唯一匹配，无钻孔入SMD pad、无新body overlap、无普通信号穿新岛/实际guard shadow。独立铜几何DSU检查12条信号端点均通且新操作无孤枝。候选不是原生板，尚不能把DRC/回流/全板验收写成完成。

- 10个MCU脚到远端J9/J13/J5/J8完整连接，I2C同时经过R19/R20上拉节点；R28地另供，C15/C16供地保持原网。I2C远端已包含，根计划必须剔除rootMustExcludeDuplicateOperations中的旧段，避免平行重复环。
- 手工先定TOP横向引出/BOTTOM北向主路，再在明确通道内找远端线；单纯逐网最短搜索会用第一条斜线封闭下一脚的口袋。PA15/PB4先给远端通道，PB5/PB8用真实换层过TOP横跨其他BOTTOM路，PB9绕HSE东侧/guard上方，未使用L2/L3信号。
- SWCLK保留最短实用全TOP路径，去掉原仅作锚点却又返回TOP的闲置PTH/BOTTOM死端；BOOT0保持全TOP，去掉不必要的两个桥接via。源bank保留的5个私有signalvia都在真实换层路径中。
- 四层原root v7 SDA远端BOTTOM长横线会穿新PA15/PB4/PB5/PB8底层主路。v8/v9因此失败留历史，v10采用与两层联合核过的TOP远段；不把仅四层更换层数当作可原样照搬任一路径。
- 每板8个新共地返回via已对实际b014及声明的north02/south05/root远段全future铜筛选，并要求铜盘在实际common参考区内。密集source5个换层最近共地2.006—2.585mm，明确未达到一般1.5mm目标。未为凑距离制造地via墙；此候选限定GPIO静态/≤1MHz且最低足够slew、I2C先100kHz，SWO默认关闭。固件尚未配置/验证这些条件，不能默认已实现；如需高边沿/高速外设，应重新评估拓扑/参考或重布。
- 全局TOP application GND还未因此生成。两层BOTTOM长路的真实返回需要最终TOP填铜、各电源横排有限投影槽及共地宽颈核查。四层需要读回L2/L3实际新反焊盘/quiet void；layername、同网及via距离均不足以宣称完整性。

新island窄stem/唯一anchor(46.35,29.4)、PC14末via(49.2,25.2)及返回地(48.2,25.0)、R28(53,28)180°、C15x47.3/C16原位构成同一返工组。旧岛/永久void/约束区必须精确替换；新原生删anchor负测试及重开是必需证据。VDD48/局部3V3与VBAT对窄stem有有限投影，已明确记录，不只写VBAT。

C15回路代价readouts/RIGHT10_v10_C15_loop_tradeoff.json：供地中心线合计4.8494→6.7399mm，围面积2.2693→2.8646mm²。VDD/VSS细颈保守上界1.2985/1.2536mm，仍以旧G31 1.4mm原生计数为准，不能暗增预算。正常供地0.6mm；C16不移动。二维几何量只用于比较布局让位代价，不是电感或PI合格证明。

原始全future粗审165752/162915对中，涉及本组/本组移动器件0问题；其他组38/35项简化字段报告保留，并未整体标PASS。其源短颈/G31各field须根任务/原生按真实作用域判定，不得因这份简化审查而全局放宽或抹掉失败。当前完整计划SHA：2L 414DF2C319A6860276960DC70AC3691E080A90D6EF1826276FE5EA6C99C90C9A；4L 408341C75236D85B4D8551145F975FC61CE26EB5E0B6227AA142EBAEA5D8466A。

## 17. 右侧完整 v11 与 SWCLK/SWDIO 联合修正

RIGHT10_FULL_2L_v11.json 与 RIGHT10_FULL_4L_v11.json 各95操作，替代第16节 v10 候选。v10 的 SWCLK 全TOP东段与根任务后加入的 SWDIO 服务线相交，不能继续称为当前可执行版本。v11 改 SWCLK 为实际需要的短 BOTTOM 桥，新增两信号过孔及三个配对共地过孔，同时修改 PC14 的底层绕路；五个密集源端小通孔仍用于真正换层。它不是为保留旧锚点而添加的闲置过孔。

SWCLK 桥两端为 (47.95,22.4)/(57.4,20.8)，中段通过 BOTTOM y23.1→y21.2 绕开 SWDIO TOP 服务段。新回流点 (46.8,22.5)/(52.8,22.8)/(57.35,19.31) 与完整源/长路一起预审。源组仍要求原生实际替换 quiet 岛、各层永久 void 与唯一 anchor，执行删除新 anchor 的负测试，再刷新铜与完整DRC。文件 SHA：2L 3F616508C7D06A8B8E86FC01D4C718E1FC20B35DA4FF6206715692FE53FF469A；4L B3E053D45D702C34571EBD608F05EDE7928D63DA82F21CB23EFE4C297D981EF2。

第16节的 v10 资料、8个新共地过孔与“SWCLK全TOP”均为该历史版本的事实，不代表 v11 当前操作数/回流过孔数。本次 v11 新增回流点须与全组服务线一起核对；不能把 v10 manifest 当成 v11 证据。根任务已冻结 v11、South9、services18、NSS04，后续只能新建 delta，不能原名覆写。

## 18. UART_RX 接收端出口与短换层桥候选 03

原 R17 接收端电阻 pin2 被 PA15 TOP 横线、SWCLK BOTTOM 桥及 SWO/地返回封住，逐网几何搜索只有1063个可达单元。这是实际出口拥塞，不能简单让自动布线多跑。根任务提出 R17 旋90°移到 (50.12,23.361)，pin1 PA10=(50.12,23.4626)、pin2 UART_RX=(50.12,25.0374)，PA15 y24.25 可从两焊盘间通过，名义铜间距0.2175mm；移动焊盘及 PlaceBound 已由根任务预审。

完整新 delta 为 UART_RX_receiver_bridge_2L_03.json 与四层同名变体，各9操作加 R17 姿态。包含精确删除原 PA10 两段TOP铜、连接新 pin1，以及 R17.2 到 R18.1 的完整接收支路。为绕过 (56.757,25.092) 的既有 PB5 回流地过孔，使用两个正常 L28 过孔 (55.7,25.05)/(57.8,25.05) 和 BOTTOM 短桥，经 (56.45,24.3)/(57.05,24.3)；其余接收线TOP为0.20mm。桥两端距保留地孔分别1.0578/1.0438mm，需最终实际地铜与转换回流审查。

仅删除冗余 PB4 远端地孔 (61.8,24.95)。PB4信号过孔 (61.8,25.85) 仍有更近的保留共地孔 (62.6,25.65)，距离0.8246mm，因此没有以移除唯一回流来换通路。接收线东段改 y24.93，到该保留地孔铜间距0.32mm，到 PA15 信号过孔铜间距0.28mm。所有其他回流地孔及其位置保持。

两板对实际 USBaux b014 加冻结各组及 root_remaining18 进行完整组合预审，均无 definite overlap，新增 UART 操作没有基线间距警告；其他组60/62项规则域简化警告保留，不能因此把全板标成PASS。报告 readouts/UART_RX_receiver_bridge_03_review.json 与 UART_RX_bridge03_full_*.json。03本身仍是待原生重基/端点/真实参考验证的候选，不能称最终完成。

记录两项被否决方案：拟将 PB5地孔移到 (55.4,27.25) 会撞 TOP SCL 斜段与 BOTTOM SDA 横线；桥02的第二段底层绕路会碰 NRST BOTTOM x60.25。均未执行，原方案及失败读回保留。03取消第二座桥，保留 PB5 地孔，仅删已有更近替代地的冗余 PB4 地孔。

原生集成必须先确认 b015 输入 SHA 与 R17 实际姿态。若执行的仍是 services18，仅应用精确两段旧铜删除、R17移动及新线路，不重做整个 SOURCE；若 services19 已应用，显式省略已完成的姿态/PA10替换并记录原因。最终还需新进程读回、完整DRC、两条真实端点证明、无新孤枝，以及2L桥上方TOP实际地缺口/4L真实L2和L3反焊盘及共地宽颈复查。UART默认初次115200bps不代表外部边沿已受限或信号完整性已经认证。

## 19. 主供电返工暂停与搜索归因勘误

NSS源端返工期间曾推测 MCU BOTTOM STAR 大对角是剩余13条GPIO无法合理引出的必然原因，提出把 C9→MCU 主供电改走 TOP。初稿 NSS_pullup_local_relayout_03.json 真实穿 C9.2 GND 焊盘并撞 buck反馈/地，已被实际铜审查否决，绝不执行。

随后完整顺序对照在保留原 STAR 的条件下也找到了 PB12；此前约10秒没有工具输出被误判为搜索失败。逐网贪心失败或暂时无输出，不能证明必须大改关键供电。当前暂停为GPIO单独重构主feed，NSS_pullup_local_relayout_04_SOURCE_ONLY.json 保持原供电与 SPI guard，改做联合出口、预留和回溯。未执行 C9旋转、U3下移或 R29改位等推演，不能写成已优化完成。原07c主供电、外设低阻分发及既有去耦返回继续保留；后续只有在真实几何证明必要时才重新评估供电返工。


## 20. 原生 BOOT0 创建失败、真实间距遗漏与动态地铜施工顺序

冻结 RIGHT11 的 BOOT_DIRECT_TOP 曾沿 y27.3 经过 R28.2 GND 焊盘下方，净距仅0.1935mm，低于该处实际 GND smdpin_line=0.3mm。原粗组合报告中已经保留该警告，但未在交付冻结候选前修掉，这是本次专项审查的遗漏；不能用“所有源短颈都允许0.16mm”或“警告已保存”替代修正该非局部规则的真实间距。修正路径为 (46.8,27.65)→(47.27,27.18)→(52.8984,27.18)→R28.1(52.8984,28)，正常0.20mm，对R28地焊盘净距增至0.3135mm，其余规则不变。冻版原文件不覆写，由执行者显式记录单操作适配。

原生 axlDBCreatePath 仍在该水平段返回nil/SPMHSY-49 Error9。分段实验先证明 R28.1 到 y27.18 的竖段可创建，BOOT0网络身份正确；因此不能把“去掉焊盘内折回”当作已证明的根因。执行者导出 try07 实际失败时刻的80件、611段、112过孔及8个真实多边形。独立对真实铜重查发现：水平段没有碰其他网的焊盘/走线/过孔，但与 TOP 已生成的 GND 碎片交叠0.061683mm²；该片bbox约(46.7602,26.8502)至(47.5,28.128)，面积0.5714232mm²，母dynamic boundary为(39.2,24.6)至(47.5,28.4)。该片不是静态晶振quiet岛。

工程诊断证据为 readouts/actual_BOOT_failure07_geometry.json，原始失败快照由native执行者保留在HI/review/PROVISIONAL_FAILED_BOOT_2L_GEOMETRY.json，明确是未保存、未通过DRC的诊断态。try08采用“精删需要重裁的旧dynamic boundary→创建源/服务真实铜→用新polygon恢复dynamic并更新”的施工顺序，随后相同BOOT段原生成功且actualNet=BOOT0，272引脚身份及新quiet唯一anchor负测通过；截至本次记录，全板fullDRC和正式新进程验收仍由native执行者继续，不能把这些中间成功冒充b015已正式发布。

这项对照支持旧generated GND铜在该操作顺序中是触发因素，不泛化为所有 axlDBCreatePath nil 都由铜皮导致。官方17.2安装API已完整复制到 source/official_BOOT_diagnostic：CreatePath说明etch取首次接触网络且nil不能当成功；DBControl的dynamicFillMode与drcEnable是不同控制；ShapeDynamicUpdate支持强制voiding、smoothing和thermal生成。实际try08没有依靠关闭DRC、修改全局规则或永久改变dynamic模式来通过。后续仍需检查实际网络、最终dynamic fill、完整DRC与重开，不能绕过失败后只记连接成功。

## 21. remaining19 普通信号换层的共地返回组02

两层 remaining_returns_2L_v19_02.json 提供三个普通共地过孔：NRST(39.55,42.8)、UART_TX(54.75,19.75)、VBUS_PRESENT_N(50.95,12.5)，距各信号过孔分别0.8602/0.8062/0.8246mm。四层同名文件提供 NRST(39.85,42.5)、UART_TX(54.75,19.85)、CAN源(61.85,11.4)、CAN目的端(37.65,15.8)、VBUS检测(51.25,13.65)，距离0.8944/0.9055/0.8944/0.9000/0.8944mm。

全部使用正常L28通孔、没有新规则例外。对实际规则全部相关字段、未来SOURCE21、UART03及remaining19一起筛选，排除了钻进SMD、孔间距冲突、晶振application void/guard shadow及非共地来源。历史实际BOTTOM或L2/L3 common面覆盖各0.6mm铜环，但此覆盖仍需最终刷新新反焊盘后的实际铜复核，不能写成新板完成。全组预审无交叠，新返回操作没有间距警告；其他源组59/61条简化字段警告继续保留，不能整体标成最终通过。

父任务最初的候选点也逐一检查：NRST(40.1,42.2)到信号线仅0.25mm小于0.3mm，UART地(54.45,17.8)到CAN_TX仅0.1mm，两板VBUS地候选均碰实际V3铜，因此全部被拒而重新选点。不能凭“距信号via小于1.5mm”认为地过孔可用。静态晶振电容孔即使最终同GND网，也不能拿来当普通共地返回点；必须排除局部quiet域。

## 22. 两层 CAN_RXD 07：完整信号路径与有限参考跨槽返回

当前候选 CAN_RXD_2L_engineered_07.json 含10操作，CAN_RXD从U5.4到R13.2的中心线总长52.3953mm，仅两个真实信号换层过孔。它是数字接收逻辑网，并非CAN_H/L差分对；不强行等长，不凭500kbps假设宣称器件输出边沿慢。SOURCE/USB关键铜/主供电/HSE不变。

BOTTOM从PHY (61.45,12.2)绕到USB壳下，中央y2.2，只有绕SH3/SH4时使用短y1.4段，避免TOP壳内走线；西端过孔(34.45,1.95)后TOP沿x34.05至y16.05，再斜接R13.2(36.3236,18.3)。TOP西线距实际V3总干铜边0.35mm，不能沿原x33.3短接V3。原04的SH3斜边对矩形壳脚拐角净距只有0.1263mm，小于两层thrupin_line=0.16mm；07把该斜边向右0.12mm，净距0.2111mm，水平壳脚段净距0.20mm。按真实矩形焊盘而非圆形或名义中心距离核查。

西端换层返回采用已有实际common GND组中的J2.SH3 plated壳脚，距信号孔1.391mm；不再把新地孔塞进板边V3供电。PHY新增地孔(61.7,11.2)距信号孔1.0308mm。壳下短y1.4段到名义BOTTOM地边0.5mm之间仅约0.5mm返回条带，中央y2.2扩大至约1.3mm，必须在最终实际填铜中测宽颈/连通及壳脚共地，不称整条是无限连续参考平面。

原低速VBUS检测BOTTOM x34.55纵段贴近TOP CAN西线。07只替换尚未执行的 HI_2L_VBUS_PRESENT_N_1_R1：检测网在y9.3..17.25移到x35.3，在y18.15..22.8移到x34.4。原pending操作必须明确排除一次，绝不能新旧并画成环；若集成时旧线已经实际写入，就必须另做唯一实际段精删delta。改后CAN右边到检测网参考让位区左边的名义地带增加约0.75mm，末端仍有一处有限交叉，不能称为整段完整微带。

该交叉配0.6mm TOP共地桥 (34.25,17.25)→(35.2,18.2)→(35.2,18.5)，两端各正常GND过孔，跨过BOTTOM检测网槽并与真实common面连接。桥与CAN平行段铜间距0.3071mm；它提供有限局部返回，不替代实际平面刷新/铜颈与时域边沿验证。早期05把检测线移x36.05撞R3共地孔(36.1,11.6764)，06仍有0.25<0.3mm，均留失败历史；07不以降低规则消除这些错误。

完整预审纳入 J2_GND_entry_2L_01.json 的四个新入口操作。原J2.A1_B12/B1_A12在b014终端图曾孤立，不能因SH1..4已共地便假称信号侧GND焊盘本来已通。当前243操作/504铜片组合无交叠，新CAN及检测网替换没有任何基线间距警告，其余源组59条继续保留。实际回流、GND图、入口端点、动态铜、HSE负测试及新进程完整DRC仍是原生验收要求。候选SHA D331E853C55FCB367530EE560DFA56D1DC12CEC90FAB33759812FAB970E040C5。

## 23. 普通GPIO可用的局部电源区域通道研究

应MCU组请求，只读评估粗SWITCHING_BLOCK矩形是否过度封锁。保留TOP热区、实际输入热环、L1本体投影与SW/BOOT/FB≥1mm避让，只研究BOTTOM有限窗口x28.3..30.9/y23.2..26.5。7条0.2mm/0.2mm直列中心x28.4、28.8、29.2、29.6、30.0、30.4、30.8，在两层y23.3..26.4局部均满足实际几何字段，距SW/BOOT/FB铜最少1.2316mm；TOP其他异网铜+0.3mm投影前6列为0，最右列约0.3765mm，仍需实际TOP地。

四层不能直接照搬同一端点：真实SPI_MOSI在BOTTOM y26.25横穿，初版研究因此失败。把四层窗口端点止于25.8后局部列才均清，若要继续向北必须在该SPI线之前真实换到TOP。readouts/PB_local_switch_corridor_02.json 明确区分两板，初版01保留。

这些结果只证明有限局部列，不证明七条GPIO源端能进入、过孔阵列能放下或北端能全部穿越SPI。V3过孔(33.3,22.5)与BOOT1孔(32.5,23.7)还夹住下侧入口，需联合源/桥拓扑。没有把这项研究写为可直接执行的全板走线、没有修改主feed或已冻源，也不把贪心搜索失败当成必须大改供电的证据。

## 24. 原生 source b015 暴露的右侧间距与 21 操作局部修正

source_2L_b015_DRC_PENDING 与四层同名 checkpoint 是实际原生候选，尚有 cached DRC，不能以候选几何零交叠称最终通过。实际右侧新 anchor 粗GND对 PB9 小孔及正常 VDD 粗线有0.28/0.2526mm等小于0.3mm的间距；此外四层小孔的内层铜环也须参与 via_via 检查，外层0.16mm例外不能自动覆盖内层。

冻结 delta 为 engineering_power/RIGHT_actual_clearance_2L_01.json 与四层同名文件，各21操作。仅唯一精删既有铜/孔并替换 GND/VDD/VBAT 局部路径和 PB9 孔；所有器件、唯一 quiet anchor(46.35,29.4)、岛/永久void/guards均不移动。PB9孔从(45.7,28.65)改(45.65,28.65)，相邻 PB8 孔所有真实铜层净距0.223303mm≥0.2mm，无需放宽RIGHT内层间距；早期改Y到28.6的方案只有0.1906mm，已否决。各层局部许可via-only box随孔位重定位，保持其它PSet字段及内层禁止非GND走线。

GND粗线提高到y29.54，VDD粗线提高到y30.46；VBAT正常支路同步提高到y31.40，避免只抬VDD又撞VBAT。正常GND/VDD最小0.32mm，VDD/VBAT最小0.34mm。VSS/VDD/VBAT细颈保守中心线总上界分别1.282884/1.379570/0.813941mm，仍使用旧1.4/1.4/1.0mm预算，原生计数为准。不是通过扩大区域或预算消除真实违规。

对实际b015加LEFT_NORTH09、rootcleanup01、remaining聚合的组合预审零交叠；RIGHT涉及的六条简化基线警告分别已有dense source 0.16、G31 0.2或MCU_NORTH 0.2的具体字段作用域，必须由原生实际区域验证，不能笼统称所有POWER到信号均0.16。两板SHA分别6530E317B3CB9646372C3610A2D24ED3567CF8F6B8C9B0D59637D75D2E2373C0 / 72E44687F4B71D381F89BB7A6F27F2CB44872F994FA30B006B4FD6AD1BF2FA13。b016执行由唯一native代理负责。

## 25. J12南移的供电条件研究与实际引脚纠正

MCU组研究把J12从(40,55)移到(18,9)，保持实际rotation90°及pinout。第一次口头误写r0和GND/V3互换，复读实际原生立即纠正：新pin1=V3V3(9.11,9)，pin2=GND(11.65,9)，PlaceBound约(7.74,7.63)..(28.29,10.37)。这些纠正发生在执行前，不能按口头图推导供电。

J12_south_supply_study_*_01.json仅为条件候选：精删旧TOP V3支干(31.11,58.2)→(31.11,55)，保留北侧y58.2总干两边；从现有低阻V3(33.3,1)沿TOP 0.6mm到(9.11,1)再到新pin1，新增32.19mm、无需新via，不经过MCU细颈。新pad顶到VIN主线铜间距0.538mm。以名义35um铜、20℃计算约26.43mΩ，20mA例子约0.529mV，仅为DC量级比较，不是温升或载流批准。实际铜厚/温度/接口总电流另核。

J12新GND必须用真实BOTTOM或L2/L3填铜/端点图证明，旧北孔的连通图不适用于新坐标；实体高度、插拔和装配空间仍待MCU/机械全组审。【随后原生累计供电证明发现错误，以上删除建议撤销】曾把TOP V3(31.11,55)→(31.11,47)→(38.1016,47)共14.9916mm称为旧R25无用枝，这是只看中间端点无pin而漏沿后续竖段的错误：它仍经过x38.1016从y47向下供R27.NRST上拉pin1(38.1016,41.3)。尤其四层实际没有等效新feed，必须恢复该LIVE2段或先完成并证明合法替代供电，不能删除后假称电源所有端点保持。36/N37/N41派生场景继承该错误删除，后续全部需恢复并重新组审。累计原生proof阻止了错误保存；保留失败候选和身份勘误，不以“精删唯一命中”代替其电气用途判断。

## 26. 原生圆弧导出重合端点：保留孔洞的解析修正

source2L实际BOTTOM generated plane的359点hole，在索引164/165连续导出同XY(39,21.7602)，半径约±0.5602058，下一点为(39.0896,21.753)。旧cadence_poly.py因d=0除零并停止渲染，不能静默扔掉整孔后声称返回平面连续。官方axlPolyFromDB说明radius对应前点到本点且弧不能跨quadrant；此记录是四位小数导出弧交界收敛，不是用两个重复点表示完整圆。

保留旧解析器副本，新处理只展平该零导出弦边，保留重复顶点及整个hole，并要求至少4点/3个不同XY等结构。按mm4量化，弦长上界sqrt(2)*0.0001mm，半径约0.5602时弓高上界4.46e-9mm，点位偏差上界0.0000707151mm，小于审查采用的0.0001mm保守扩缩。越界/不满足结构仍报错，不普遍吞掉异常。

readouts/arc_source_b015_area_audit.json对两板9个实际plane逐一保留孔数并比原生面积，最大绝对差0.0031297507mm²<0.01mm²；因此修的是解析/近似，不修改native工程。cadence_poly.py当前SHA631120DF7C97FA9A21F9905A01AB14C7AD9B5D50E214D781B8BAA4A1C5D62C48。根渲染器另按实际pad读取小孔半径，不再统一当0.3mm。

## 27. 最终TOP共地候选的quiet排除范围预审

readouts/final_TOP_GND_engineering_review_02.json仅PASS_SCOPED_TOP_QUIET_EXCLUSION_GEOMETRY_ACTUAL_RETURN_PENDING。root最终TOP候选把新quiet moat与7条实际guard中心线buffer0.6mm合并为27顶点、90.0300125mm²永久void；0.6来自guard铜半宽0.3+工程间隔0.3。全部7条guard及两quiet cap孔完整铜盘均包含于void，普通case共地点在void之外。北侧guard中心y39.8，排除到y40.4，保留x42.8..43.6的case开口。首轮用多边形二次miter buffer导致微小人工外突而误报，02直接以实际中心线+宽度构造检查，失败01保留。

2L需精确替换3个已有TOP dynamic母边界，4L实际无旧TOP母边界。必须等全部manual铜后重基，先永久void后fill，重做删唯一anchor负测；同GND网不等于没有高频绕流或第二条quiet连接。最终实际C3/U2、LDO/C9、MCU去耦spoke和宽颈、J12/Q1/R8/R29地终端、实际L2/L3必须另核。TOP共地不会消除2L USB_TOP参考BOTTOM VBUS桥造成的有限缺口，不能把填铜或零DRC写成SI/PI/EMI认证。

## 28. 北6 GPIO联合路由研究开始：共享场景身份与失败留存

当前只读研究来自实际source b015加声明的局部修正/remaining/J12条件供电，干净derived场景为MCU组GPIO_future_*_36。35曾夹带失败N35候选，已明确禁用。北6为PA1/PA2/PA3/PC13/PC14/PC15，目标J11.6/.7/.8/.3/.4/.5，保ADC/C9/主feed/晶振域。

N37先研究精删PC13与PC15两个BOTTOM长bar及PC14远端4段/49.2孔，保原MCU TOP到实际sourcevia，释放内部共享走廊。它仅隔离候选，不能执行单独删而断线；必须北6完整替代及south7全组审后才交native。次序PC15先会堵PC13/14，改PC13→PC14→PC15可达前三但PA3最后又被封，失败候选均存N37_search文件。不能由单次贪心失败断言必须重构电源或搬ADC/C9；最终仍需联合层桥/顺序和真实返回审查。
## 29. b016真实共地守卫：WEST先失连后自然恢复，SH2须实际TOP铜桥

2L try09已有各变更网scoped DRC=0及quiet负测，但旧WEST小地孔(35.8,21.95)成为2对象孤岛，累计共地proof阻止保存。最小候选是TOP0.6mm到新stock地孔(35.8,20.5)，实际最紧PB12 BOTTOM净距0.35mm≥0.3；新孔整个盘在actual大BOTTOM地片内，原生图该大片与VSS23处于同component1。只记录成readouts/B016_WEST_COMMON_BRIDGE_01.json候选，没有冒称修复已执行。

随后精删南侧8条没有硬件终端的信号尾线并重填，WEST自然恢复共地，因此未添加该多余桥/孔；不是忽略旧proof，也不是提前铺全TOP掩盖问题。尾线清理是按实际物理pin/路径审核，不能与第25节误删LIVE V3混为一谈。

try11又发现C1.2→J2.SH2失连而SH1仍通；J2数据侧地到SH2自身虽通，也不能据此认为已接application ground。独核actual native hi_graph：SH4真中心(44.32,2.6)属于common component1，SH2真中心(44.32,6.78)属于孤component2。最小完整方案SH2_common_return_2L_01.json只有一条TOP0.6mm、长4.18mm的真实PCB铜桥SH2→SH4。它沿两实际PTH shield lands连接，不假定连接器内部金属为PIN_SHORT，亦无新增钻孔。此前口头6.295仅是land内点，真实中心6.78已核并纠正。

全actual铜/孔/间距字段与真实ROUTE_KEEPOUT检查无违规；往C10的TOP x45.3近路穿CC2电阻焊盘及来线，已否决。候选新孔(46.8,2.2)虽几何可行，但已有SH4真实common，故无须多孔。原生try12随后实际写桥、保存及新进程验证C1.2↔SH2/SH4/数据地均真共地，304累计proof/272引脚身份通过，18变更网scoped0、SMT严格挑战恢复及HSE负测通过。2L b016板SHA4AC553CF77DA21A3BA7E2B4E9142DDE1707571B7E4A80B17FCA975C46876D6A5；4L FD5D93BED7E64FEF14CEBB17FF103443FA29E0CEDF60EEA26B79D9F8D091B1B7。均仍wholeDRC=null/DRC_PENDING，16joins/14split，不能称整板布线完成。

## 30. 北6最终51：完整源、平行扇出、远端及真实端点证明

最终冻结文件GPIO_NORTH6_2L_51.json与四层同名，以各自最新actual clearance_b016为输入，J12保持原北位，R27的3段LIVE V3完全保留；先前南移study和错误删枝场景只作被撤销历史。未动ADC/C9/主feed或晶振域。

联合方式先移除PC13/15底层长bar及PC14远端绕路，再手工设平行局部通道与错开的外侧拐点。PA3保原via(35.2,31.65)，只先NE小转抬trunk sum至67.25；PA2为67.85，PA1为68.45，给南侧PB1/PB10正常0.2mm信号留下容量。外侧bar分别错开y33.15/33.6/34.05/34.5/34.95，避免先走的一条横向封闭后路；C24真实GND孔与VDDA供电不移动。源前缀通过真实连续几何后，才在该固定通道内求远端路线。

每板固定39操作：2个旧PC14孔删除+11段旧铜唯一删除，17条新增route、5颗新signal stock via、4颗新commonGND stock via。全部新增信号正常0.20mm，PTH为L28_VIA030_C060，已有全层许可；没有新增全局/局部规则、privatevia许可或内层走线权限。PC14删旧41,27.8与49.2,25.2两孔以及3TOP/4BOTTOM旧线，直接由真实U1.3 TOP接新sourcevia(41.5,29.65)，不用闲置过孔或重叠尾线充当锚点。PC13/15/PA1/2/3原sourcevia保留。

六条真实端点为U1.2→J11.3、U1.3→J11.4、U1.4→J11.5、U1.11→J11.6、U1.12→J11.7、U1.13→J11.8。新旧保留源线相加的平面完整长度约37.33—47.63mm，具体每板/每网数值在completePlanarRouteLengthsMM；不包括孔桶竖向距离、键合线或外部线缆，不据此等长或延时认证。两板actual重基13项删除全部唯一、所有新path/孔/真实keepout检查无issue，仍待south7全组相容及native完整验证。

两层冻结SHA FA3723EAF775A4BF5B959C101A8C4EFD893043631D9FA59EB6F91676D6F69D2C；四层BA259F4DE5438F3F0547911335937BEB42B01A8AED4D0C0B5585C76B43C10FC3。信号从50到51不变，只改源端GND返回位置，已明确同步MCU南组。

## 31. 北6返回与特殊GPIO条件：不以距离代替实际铜图

新PC14源换层的近端GND选(41.4,28.15)，距signalvia1.50333mm；最近对PC13 BOTTOM线净距0.35mm≥0.30。旧信号孔(41,27.8)计划已删，但历史fill仍有它的anti，故冻结面不能满足新GND盘全覆盖；新盘与实际common已有铜交叠0.115745mm²（全盘0.282693），原生需删除旧孔后重填并证明新地孔到C1.2真实共地。这比为满足旧像素盘全覆盖而在2.28mm处额外堆孔更合理，但不是把历史交叠当最终HF回流通过。

其余4个新signalvia由3颗外侧GND孔返回，其中PC13/PC14两处共用同一地孔，距离约0.922—1.25mm。所有孔需最终native共地图、实际填铜与铜颈复核；2L后续TOP共地才有完整外侧BOTTOM线参考可审，4L需核真实L2/L3及其反焊盘。不得取quiet电容孔当common返回，或因同网/距离便宣称SI合格。

STM32F103C8T6的PC13/14/15受backup供电开关限制。root核ST DS5319 Rev20（2025-07）Pinouts footnote5及5.3.13：输出频率≤2MHz、负载≤30pF、backup开关限制3mA且不得作为电流源驱LED。此前若记2mA是错误。外部header/线缆负载未验证30pF，普通1MHz时钟也不能代替mode、slew、负载要求；普通GPIO同样先采用足够低slew，实际固件尚未验证。公开原厂入口https://www.st.com/resource/en/datasheet/stm32f103c8.pdf，版本与页证据由root保存。

## 32. 北6旧alias退役合同：更换真实路径，不让旧XY假通过

附加GPIO_NORTH6_51_native_contract.json（SHA7F5CD1EAA62849ABA2D813E00481BBC69F2140D22B55929E4BFBD513BF48404C）不修改冻结51文件或铜。PC14旧source41,27.8迁移到新真实via41.5,29.65；旧far49.2,25.2与历史RIGHT_PC14_SOUTH_BYPASS43.6,25.2由真实J11.4完整证明取代；PC13旧35.8,31.1、PC15旧35.4,28.75（B016_NODE_176）分别退役到真实J11.3/.5证明。只匹配实际active alias的准确net+旧XY+类型并记录旧id/新目标，不做字符串泛匹配或旧XY假通。

原272引脚身份、172已连真实pin物理边及其它关键/地proof均须保持，加六条新的真实U1→header。保留PC13/15/PA1/2/3原sourcevia；GND RIGHT_PC14_RETURN(48.2,25)并未因关联PC14改路而删除。新四颗GND孔逐个到C1.2，PC14新sourcevia到U1.3，HSE唯一anchor负测及finalfill后全部累计证明都要通过。原生wholeboard freshDRC仍是后续独立验收条件。
## 33. b016两层USB参考缺口的actual common预审：必须继续复核

root的reference_projection_screen_b016.json按actual plane+holes/官方弧几何筛投影，明确不含同层地、孔/trace铜，也不证明common/HF回流。结果不能被finalTOP掩盖：2L PA11_SHARED TOP平面长度6.453mm中BOTTOM投影缺3.8235mm，PA12_SHARED约6.380mm缺4.6208mm；主要是MCU南侧y18.3984..22附近实际BOTTOM开口/信号阻挡。USB_DP TOP另缺2.5426mm（入口anti约1.2mm与VBUS处约1.3424mm），BOTTOM约1mm入口桥处于反焊盘区。常见反焊盘和需要真实绕行审查的缺口必须分开，不能把所有缺口视为相同或自动合格。

本专项进一步读取原生hi_graph的GND component1，把真实manual GND cline、pad、via及generated common铜纳入同层边距检查，仍排除quiet静态岛，即使它最终也是GND网。readouts/USB_b016_actual_common_pre_audit.json保存每段缺口、附近对面异网铜及同层最近common点。当前2L缺口段的signal中心到已有同层common GND边约PA11 0.70—1.43mm，PA12 0.65—1.25mm；实际数据中主要由C14等供地铜提供有限邻近返回，不能据边距就声称连续参考或阻抗通过。

四层两条shared TOP在actual L2下均全覆盖，USB_DP只余入口反焊盘/换层处局部投影。它仍需核真实L2/L3/孔附近共地和最终填铜，不是层数本身自动认证。两层TOP新增地不会把TOP_USB下面的BOTTOM参考面补回；它可能提供真实同层共地边和跨BOTTOM槽返回，必须在实际生成后量宽颈、连接、绕行与唯一HSE隔离，而非脑补。

root准备在North原生实证之后于独立候选先生成TOP globalGND，South尚未完成时明确是临时阶段，用来取得上述actual coplanar边/宽颈及剩余3个GND端点接入的真实数据；South最后仍需重填/全proof/HSE负测/全板freshDRC。当前尚未进行该临时生成，不改USB数据路线或放宽规则，不把2L bulk1.15/0.16几何或公开90Ω目标当整路认证。外部USB线缆/负载、上拉/历史22Ω器件和制造条件继续开放。
## 34. North51 实施后才确认的地连接失败与 TOP 实铜阶段

第33节是 b016 时点的预审；其“尚未生成 TOP”现已由本节后续实际阶段更新。四层 North51 独立保存/重开 b017 成功；两层 North 单独施工时，虽然七个变更信号网的 scoped DRC 和 HSE 负测通过，旧 R28.2→U1.23 共地证明实际失败，守卫拒绝保存。因此不能写“两层 b017 通过”，也不能用七条信号都接通代替旧地网络保真。

随后在独立候选组合 North 与 TOP common GND，要求保全旧真实端点边、56个实际GND引脚、全部实际GND过孔、无孤铜和 HSE 唯一anchor。四层实际 b018 正式只读输入为 inventory/checkpoints/TOP_trial_4L_b018_PRE_ALL69_DRC_PENDING，板 SHA256=412F67C2A799DE1EB413BA88F7AE2B6825EDC854D41F69AA5523BBA54ED902B8：56 GND pins、76 GND vias、22块实际GND铜全部到C1.2，0无终端分支/0 OOD，461端点证明与272引脚身份及HSE通过；还剩 South7，69网 scoped和全板 fresh DRC 尚未重算，不能称整板电气最终通过。

初次TOP生成有15块无终端孤铜，健康门拒绝保存。执行者采用 axlDBCreateVoid(BOUNDARY, actual arc polygon)，针对这15块真实孤铜生成永久void后重填；并未调用GUI island_delete，也未宣称自动具有 DYN_DELETED_ISLAND 属性。原 quiet 排除几何90.0300125mm²保持。每个新增void的真实polygon、母形、area和创建返回在 hi_batch_execution.txt/阶段清单。后续South路由后，若这些void过时，应按阶段精确身份重审/重生成，不能全删永久void伤及quiet，也不能以IGNORE_SHAPE_ISLAND隐藏健康问题。

官方安装文档 algPN/algPN.html 的 Automatic Island Deletion 与 algroshapes/algroshapes.html 的传统 Delete Islands 语义不同：前者可在动态更新删除未连接碎片，后者用永久void留下抑制区域。axlParamShapeDoc 的 areaSuppress 是边长平方阈值，不能把它当成只按连接性删除孤铜的参数；此轮并未盲设该值。

## 35. 四层 b018 实际参考铜：中心线覆盖并不等于整个线宽无缺口

独立只读脚本 scripts/audit_actual_TOP_b018.py 从原生 hi_graph_objects.tsv 找C1.2实际GND component，再纳入其 generated铜、manual cline与pad/via；静态晶振quiet岛即使同GND网也排除。所有22块原生多边形保留holes和带符号弧，解析面积误差最大0.00424mm²，小于0.01；报告 readouts/TOP_b018_4L_actual_reference_audit.json，实铜图 readouts/TOP_b018_4L_USB_NORTH_actual.png。

PA11_SHARED 的TOP中心线6.4531mm和 PA12_SHARED 的6.3804mm均在L2平面投影内；但PA11竖段x40.6/y20.247..20.753的西侧约0.0602mm带被PA10 tinyvia(40,20.5)反焊盘咬入；PA12竖段及拐点受SWDIO tinyvia(41.52,21.25)反焊盘影响，线宽投影缺失约0.0385mm²。故把之前“中心线全部覆盖”扩写成“整线宽连续完整参考”是不准确的。不能仅凭这些面积计算90Ω或认定USB认证通过。

USB_DP仍有接口两颗信号via反焊盘处TOP投影缺失合计1.2002mm，以及BOTTOM 1mm桥整段落在相交反焊盘区；DM TOP没有中心线缺失。DP入口两via(39.75/40.75,5.8)最近实际common GNDvia距离分别1.60/0.95mm，不把1.5mm当无条件合格阈值。这里存在有限参考绕行/层转换，须与数据对拓扑、同层地和实际层叠一同看；不因位于接口就自动认证为合格。

北侧新增4个实际GND返回孔全部native common，4L L2/L3局部2D宽核诊断在0.05..0.60mm测试下仍从孔邻域连接到1.9mm外的实际铜；这是形态学几何筛查，使用实体盘邻接而未建钻孔/孔壁/三维电感模型，不能称其已测得最小制造铜颈为0.60mm或HF回流通过。普通信号via反焊盘使North各网局部中心线在参考层中缺口，逐段位置/长度及附近common返回孔全部保留在报告，不能只报全部GND已连通。

四层普通 BOTTOM 走线越过 TOP_USB 的XY投影，不等于越过自己的L3实际参考裂缝。仅在实际L2/L3屏蔽/参考保持的条件下，可撤过严的普通BOTTOM trace shadow；TOP真实USB铜间距、HSE双面quiet/guard保护和信号通孔在L2/L3造成的反焊盘保护仍保留。两层仍须按对面实际地与同层跨槽返回审查，不能照搬四层撤限。South后续手工铜和最终填铜将改变本阶段结果，须重新审查。

## 36. PB11 人工走廊研究交接：找到路径不等于布局质量合格

按窄分工，研究 U1.22/source tinyvia(33.7,25.3)到原J12.5(41.27,55)。PB11_61曾用跨R27供电的短桥与GNDguard，虽然单条几何可达，却挡住其余South目标bank；PB11_63的y42桥撞实际NRST斜线/长横段，均保留失败，不执行。

PB11_65两板在实际b016+North51派生场景及其它6个TARGET63目标作为障碍下找到完整信号前缀，末接BOTTOM(36.2,43.9)→(36.2,49.93)→真实J12.5。但路线绕x13再北返，整体过长，MCU组已明确不采用为最终。它只是可比较的走廊证据，未native、未补最终返回，不是已经布完PB11。搜索JSON中的历史requiredFutureSources不能照单重放，因为这些Source已实际在板；pending其它目标也仅是障碍，不属于PB11操作。

MCU组继续完整South7与J12保持/南移方案的成组比较；任何J12布局比较都必须保原R27 LIVE V3供电三段，不再沿用第25节已纠正的“死枝”推断。当前转回本专项实际TOP/USB/North参考审查，PB11资料由MCU组接续。

## 37. 两层 b018 实铜复核与短切线弧解析边界

两层 b018 原生保存并fresh：板SHA D229F4A52025454CC81A627DA4BA7E3BB9E7A222235C33A3DC090F901B8CEF96，56实际GND pin/84 GND via/26实际GND铜全部native common，0孤铜/OOD/无端，剩7条South。两层单独North失败未被覆写；b018是North+真实TOP的组合阶段。原BOTTOM母框和HSE void保留，North造成的BOTTOM狭长孤铜用实际含弧polygon精确建void清理，不是任意忽略。

readouts/TOP_b018_2L_actual_reference_audit.json 保留完整孔洞和共地铜，26形解析面积最大误差0.002682mm²。TOP全局地之后，PA11_SHARED/PA12_SHARED下方BOTTOM中心线缺口仍为3.823476/4.620783mm，线宽投影缺口0.769052/0.922434mm²，不能把同层地改善写成已恢复对面参考。实际TOP最近common边距在主要源竖段仍约PA11 0.760..1.362mm、PA12 0.400..1.025mm。北侧新GND返回孔native common且局部几何宽核连通，但多条BOTTOM North线的TOP投影仍受实际signal/power/quiet void影响；全部共地不代表各段均连续参考。

本次原生mm4输出又出现短切线弧退化：端点(43.6435,23.9399)→(43.6414,23.9399)，radius=-0.05079927，两半平面候选中心在舍入后无法唯一选择，sagitta=0.0000108527mm，略超原人为1e-5阈值。保留 cadence_poly_v3_before_tangent_bound_20261022.py，新分支仅在“端点量化上界0.0001/√2+sagitta≤0.0001mm”时展平该一条短弧，其余完整polygon/hole不丢；本例总界0.0000815634mm。所有事件记录到polygonParserDiagnostics，超界仍拒解析，并对26/22全部原生面积独立核对。不能把本次数值修正泛化为跳过任意弧或整个孔。

## 38. b019 焊盘内路径规范化：三个不同的细颈长度

两板65非USB网逐项报告最终揭示同四网超限：BOOT0、GPIO_PA15、GPIO_PB4、I2C_SCL的原生MaxNeckLength actual2.1414mm>2.0。早先仅看报告尾部一个CAN0而简报四层65全0不充分，已由执行者和root纠正；b018违规历史保留。

这四个U1真实land均x43.65..44.85、宽0.30mm。原.16 path从pin中心x44.25起，经45→45.1微斜到46.35，长度0.75+√0.02+1.25=2.141421；其中0.60mm在同网实体pad内部，真正外露细颈为1.541421mm。直接把.20 flare提前到46.15会挤入相邻tinyvia夹槽（两Cu盘间0.48mm，.20正常线+两侧.16需0.52），因此不是合法快捷修法。

root批准保显式pin中心锚点：精删每网首段44.25→45，改44.25→44.65的.20 normal（含圆头完全埋在实际.30mm宽land）及44.65→45的.16，后续不动。每板12op，P/S/E、2.0mm预算、过孔、真实外部铜边界全部不变。原生strict暂设1.7实际抓到1.7414，再恢复2.0与全部原TOP字段，65网逐项全0。不能称物理细颈缩短：规范后路径对象1.741421、外露仍1.541421、原对象2.141421是三个量。

当前正式fresh阶段为 inventory/checkpoints/padentry_{2L,4L}_b019_DRC_PENDING。2L板SHA AA3BFC0E01B06CB1058462439C71E56BC316F1F2929859B6A224320BE1013420；4L B7A32330992F49609339E33C00BE92D989D0EA0C4AF64ED2763D0678DE14B501。全部465累计端点、GND与HSE保持；仍7South，USB四网及wholeDRC尚未完成。独立 readouts/B019_padentry_independent_actual_review.json 40checks通过：声明4rip+8new以外所有manual铜保真，四网实际pad+route铜对称差0、80pose/272padnet/全部via/GND铜、P/S/E/group/netrule/stackup/全部Film原文不变。执行者严格挑战原文与各65结果见HI/review/b019_native_report.json。

## 39. 实际整板/源端人工视图与输入身份

为避免只让逐网搜索试错，输出真实铜图 readouts/B018_2L_wholeboard_South7_manual_map.png/.svg，TOP/BOTTOM分面、5mm坐标格、实际80器件ref、原J12/J13 pin与net、七个未接source和真实xy、原生pad/via/drill尺寸、淡色实际GND、HSE实际永久void与USB工程保护overlay。J12(18,9)/90°仅橙色ghost，不是已改布局，不包含任何候选铜。两面均相同TOP视角XY，BOTTOM未镜像。

更细图 readouts/B019_2L_sourcebank_actual_zoom.png/.svg 及各TOP/BOTTOM单面PNG：x32..48/y18..33，0.5mm网格，1mm标注，U1真实pad编号、S1..S7与实际U1 pin/xy表、F1..F19实际GND/V3过孔坐标及库名。b019 pad内部规范化的铜并集与b018相同，整板图外观仍适用；实际source放大图以b019新SHA为准。SVG文字描边在渲染器产生重复显示已去除，PNG已目视核对。显示采用native非圆形regular pad变换后bbox近似，不是阻焊或装配/真实MPN外形认证。

## 40. PA9/PA10 参考改善只读比较与完整缺口归因

在不动关键USB/C14/HSE的范围内，提出仅普通UART源局部避让比较。01新RXvia(39.78,20.37)被实际BOTTOM ATTACH斜线净距0.0996否决；02新TX斜段至RXvia仅0.1915<0.20，均保留失败。03采用RXvia(39.8,20.52)，TX BOTTOM由(39.7,21.7)→(40.08,21.32)→(40.08,21.07)→(40.45,20.7)→(40.95,20.7)，替代原x40.8长平行腿；RX pad内增加normal锚点使现有2.4mm预算仍满足估计对象2.0164。两板各16op实际Cu无交叠，四base warning仅继承USB_SHARED全局.5与现有局部dense .16的区别，仍须核实际区域/新tinyvia全导体许可。

readouts/USB_RETURN_SOURCE_COMPARE_*_03_reference_potential.json 只是局部布尔回填潜力，不是实际fill：2L PA11中心线缺口可能3.8235→2.9672、线宽缺口0.7691→0.5962；PA12可能4.6208→4.0388、0.9224→0.8369；4L仅RXvia反焊盘咬PA11边0.02045mm²可能消失，PA12的SWDIO咬边未消失。不得把有限改善称整路径参考修好，没有原生执行或采纳。

完整只读归因报告 readouts/USB_shared_b019_obstacles_and_actual_ground_corridors.json 按实际14段缺口列精确xy、关联BOTTOM ATTACH、PA9_UART_TX、PA10_UART_RX、SWDIO路径/反焊盘、直接铜投影与0.3002mm净距壳关联，并检查同XY换TOP桥的真实冲突。原位改TOP会碰关键USB/现有Cu，并非把某BOTTOM段直接换TOP即可补好。净距壳只能称关联，不是Cadence精确cause getter；多障碍可重叠，长度不能相加。

真实C14.2→U1.35的TOP normal地与.25有限细颈保持，是跨控制网BOTTOM槽的已有物理返地支路，但不能据此称各信号正下方连续平面。进一步用真实common Cu做0.05mm网格的多目标几何诊断，目标为实际MCU GND pin23/35/47，避免只盯一个GND脚误判：有限窗口内BulkBelowR5_6到最近VSS23约12.69/12.85mm（.10/.20测试走廊）；SourceNorthSlots约6.70/6.67mm，使用现有实际GNDvia(38,25.27)附近。它不是EM高频电流解、全局最短路、延时或认证；实体via盘近似忽略钻孔、窗口/网格/端点吸附均已列出。更早固定VSS35-normal目标得到22/32mm，不能当成全电路实际最小回流长度。

只读返地新增孔/桥比较也保留：单stitch42.35,17.0虽上下盘都落已有common铜、几何0warning，但不能跨越TOP DNPstub与BOTTOM ATTACH相互错位的墙。strap02撞实际TOP CAN_TXD y18.3，被拒；03改stock孔(45.65,15.5)/(45.65,17.58)+TOP.6正常桥2.08mm，0warning；配合LOCAL02小GND孔(42.25,21.47)接现VSS35支路，只有TOP SWDIO已有局部.2相对全局.3警告，其余名义GND/POWER最紧约.308..310mm，保留约.008mm紧余量。新private孔仍需全导体point许可与正确G31_GND1.4 parent，未获执行授权。多目标实际/派生返地比较 readouts/USB_b019_return_multiterminal_actual_vs_derived_03.json 未显示最近MCUGND走廊净改善，因此建议拒采这四操作，避免为某单目标数字堆无收益孔；未native。

当前完整连续参考不能在“关键USB/C14/HSE不动、只局部单桥”的范围确认；需后续普通source联合重排/可选电阻布局走廊等完整取舍。现阶段精确列出实际返地、局限和未确认项，不以低频率/全共地/一条centerline统计代替基本回流审查。

## 41. South 门户的供电/参考只读边界勘误

抬MCU内部TOP V3 bar到y24.8的概念会短现07c TOP GND normal桥y25.27（两宽.6中心距.47<.6），不能声称PI/return不变。退为bar y24.2、PB14 TOP y23.62东逃的概念仍会在(42.75,23.62)穿实际U1.36 VDD inward .25支路；U1.36不是口头误称的VBAT1。原位小via43.38,23.0对VDD36 pad约.22<POWER.3；新wire名义.17 pad间距也超出原sourceSP区y≤23.4，不能静默套局部.16。bar上移还令VDD36真实外露细颈约增加.20mm，虽然原生path对象1.25不变。该概念列失败，不继续冲PI；供电和直接去耦未改。

root/MCU组随后改普通外向source门户。BOTTOM跨线放y≥23.8，即把跨越移到实际TOP USB SMD pad末端23.35之后：.20线+.30GND形状间距的理想void下缘约23.3998，名义距pad末端.0498mm，需native actualfill、圆角与全部实际铜复核。不能仍把旧reserved凸buffer当实体墙。但若新GPIO BOTTOM y23.8沿x38..43长横，自己会落TOP V3铜23.7..24.3及groundclearance影子23.4..24.6下，普通GPIO自身参考不连续必须另列；优先短斜跨条再去有actualTOP common的区长横，或明确有限GPIO慢边沿/真实同层回流与宽颈，不能因保护了USB引用就称GPIO参考自动通过。所有上述门户仍是root/MCU组待筛候选，本专项未运行Cadence。
