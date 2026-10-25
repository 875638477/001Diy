# 第 20—25 课：电源、滤波、接口与入口保护

日期：2026-10-19（Asia/Shanghai）。本记录与 D15—19 共用 STM32F103C8T6、LQFP48 练习板。已经完成本分工的原厂资料核对、设计计算、器件引脚及子网规格，并独立审查实际 Capture 原生保存重开的电源/接口子网与属性（见 §10）。GUI ERC、PCB 导入/ECO 的各自结果由 D/E 总记录单列；本笔记不把原生数据库读回等同于 GUI 或硬件运行。这里没有打开用户产品工程，没有修改公共库。

机器可读子网和完整 52 个元件列表：[power_interface_spec.json](../examples/de_15_26_20261019/power_interface_spec.json)。生成脚本：[de_power_spec.py](../scripts/de_power_spec.py)。根工程可把语义位号换成 R1/C1 等正式编号，但要保留映射。JSON 中 `pins:null` 是有原因的不连接，不能变成漏接告警后直接忽略。

独立关键规格审查已执行 **40/40 通过**，包括原厂 pin map、BOOT 两端、ESD 同脚等价、独立 CC 下拉、VBUS 与主电源隔离、两个装配 profile 的低阻路径互斥。报告：[power_interface_review.json](../examples/de_15_26_20261019/power_interface_review.json)；审查脚本：[de_power_review.py](../scripts/de_power_review.py)。这是前 CAD 电气规格复核，未声称 Capture ERC 或硬件测量通过。

## 1. 本练习的使用前提

| 项目 | 选定条件 | 为什么要写入原理图/PCB 约束 |
|---|---|---|
| 电源 | 9—16 V、可限流的隔离台源；12 V 为标称值 | 电源输入不承诺汽车负载突降、工业浪涌或任意适配器过压 |
| 电源链 | 入口保险丝/串联防反二极管 → TPS54202 降压 → 约 5 V → TLV75533P → 3.3 V | 不能让 12 V 直接进入 5.5 V 上限的 LDO |
| 总负载 | 3.3 V 正常工况上限 **150 mA**；GPIO 与扩展排针外载合计 ≤10 mA，并计入 150 mA | 初稿120mA未给CAN最坏工况的偏置支路留余量，已修订；芯片额定500mA不是板级热承诺 |
| 环境 | **0—40 °C**，台架使用 | 与150mA最坏LDO耗散一起重新限定；需实板测温再扩范围 |
| USB | USB 2.0 Full Speed、自供电、UFP device，无 PD 协商 | USB-C 是连接器；不能从其外观推断 USB3/PD 能力 |
| CAN | 500 kbit/s、≤1 m 非汽车台架网络；2 个物理端点各 120 Ω | 不把收发器芯片级 ESD 额定值称为整板认证 |
| UART/I²C/SPI | 3.3 V CMOS、短台架连接，不热插拔；不接 RS-232/5 V TTL | 标注电平与上电条件，避免仅看到接口名称就接线 |
| USB/CAN | 默认 USB 配置；CAN 配置与 USB 配置互斥 | PA11/PA12 共用，还存在该 MCU 的 USB/CAN 内部资源限制 |

电源域统一名为 `VIN_RAW`、`VIN_FUSED`、`VIN_PROT`、`V5`、`V3V3`、`USB_VBUS`、`GND`。`USB_VBUS` 只用于连接检测和 ESD rail，绝不连接 `V5`；调试器 Vtarget 和排针 3.3 V 只作为参考/受限输出，禁止反向供电。

## 2. 原厂资料与查阅位置

资料归档在 [sources/de_15_26_20261019](../sources/de_15_26_20261019/)，下载结果、SHA-256、失败原因在 [power_sources/source_manifest.json](../staging/de_15_26_20261019/power_sources/source_manifest.json)。部分站点本地下载超时/403，但官方网页 PDF 已成功读取；不能把这些项目写成已离线保存。

后续补充成功下载的 Coilcraft 原件与同目录其它已存 PDF 的最新哈希，另见 [local_pdf_hashes.json](../staging/de_15_26_20261019/power_sources/local_pdf_hashes.json)；首次批量下载日志与后补归档不是同一次执行。

| 标识 | 原厂资料 | 本次实际核对位置 |
|---|---|---|
| P1 | [TI TPS54202，SLVSD26C，2026-02](https://www.ti.com/lit/ds/symlink/tps54202.pdf) | p3 pin；p4 推荐/绝对额定；p5 限流/反馈/频率；p13—17 应用；p20—21 布局 |
| P2 | [TI TLV755P，SBVS320D，2024-09](https://www.ti.com/lit/ds/symlink/tlv755p.pdf) | p3 DBV pin；p4—6 电容/热/精度；p15—18 电容、反流、耗散；p21—22 布局 |
| P3 | [TI TCAN33x，SLLSEQ7F，2025-05](https://www.ti.com/lit/ds/symlink/tcan332.pdf) | p3 型号差异；p4 引脚；p5—6 边界/电流；p27—30 应用/布局 |
| P4 | [ST USBLC6-2，DS4260 Rev7，2021-12](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) | p1 功能引脚；p2 额定；p9/11 应用/PCB |
| P5 | [GCT USB4105 图纸 RevB4](https://gct.co/files/drawings/usb4105.pdf) | 本地 B10 已有 PDF、16 接点/12 铜焊盘、shell 与信号映射 |
| P6 | [NXP UM10204 Rev7.0，2021-10](https://cache.nxp.com/docs/en/user-guide/UM10204.pdf) | p50 §7.1，上拉电阻上下限、0.8473RC；p54 布线回流 |
| P7 | [Nexperia 2N7002 Rev7](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf) | p1 引脚；p5 Vgs=4.5 V 的 Rds 与阈值 |
| P8 | [Diodes DMP2035U，DS31830 Rev11-2，2025-06](https://www.diodes.com/datasheet/download/DMP2035U.pdf) | p1 顶视端子与订货；p2 -2.5 V/-1.8 V Rds 保证；p6 land |
| P9 | [Vishay SS12—SS16，文档88746](https://www.vishay.com/docs/88746/ss12.pdf) | SS14 40 V/1 A、SMA 阴极色带和 land |
| P10 | [Littelfuse 467，2023-02-27](https://www.littelfuse.com/assetdocs/fuse-467-datasheet?assetguid=4a59f034-1cca-460e-a5ba-e1e66247c76d) | p1 0.500 A/32 V、I²t；p2 温度降额与时间电流；p3 订货 |
| P11 | [ST SMBJxxA，DS1283 Rev14，2026-04](https://www.st.com/resource/en/datasheet/smbj16a.pdf) | p3 同时比较 10/1000 µs 与 8/20 µs 钳位，作为拒选实例 |
| P12 | [Coilcraft XAL60xx，Doc887，2026-02-25](https://www.coilcraft.com/getmedia/ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf) | p1 XAL6060-153，p3 偏置曲线，p4 推荐 land/短引线标记；已成功离线下载 |
| P13 | [ST AN5225 Rev7，2023-06](https://www.st.com/content/ccc/resource/technical/document/application_note/group1/38/94/1d/41/0e/ba/49/21/DM00536349/files/DM00536349.pdf/jcr:content/translations/en.DM00536349.pdf) | p8—10 CC、双 Rd、5.1 kΩ；仅用于此既有功能条件，非最新 PD 合规声明 |
| P14 | [ST AN4879，USB hardware/PCB guidelines](https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf) | USB 特定 MCU 外置上拉、差分回流/ESD/布局方法；配合 F103 数据手册，不跨系列照搬 |
| P15 | [ST DS5319 Rev20，2025-07](https://www.st.com/resource/en/datasheet/stm32f103cb.pdf)；[本地PDF](../sources/de_15_26_20261019/DS5319.pdf) | p40—41 MCU电流条件/表13；p68表41脚注2与p69表42的I²C条件差异，后两页已独立视觉核对 |

本地已视觉复核 P1 p13 参考电路、P2 p3 DBV pin、P3 p4 型号差异和 P12 p4 land；PNG 在 staging 的 `power_sources` 子目录。环境未找到 pdftoppm，本次用现有 PyMuPDF 做只读渲染，并非以抽取文本代替这些图形核对。

## 3. 第 20 课：LDO 电源分配

选用 **TLV75533PDBVR**，DBV 是无 exposed pad 的 5 脚 SOT23；不要套用 DYD 的散热焊盘或 DQN 的 pin map。连接为 1 IN→V5、2 GND→GND、3 EN→V5、4 NC 不连、5 OUT→V3V3（P2 p3）。本次不需要独立关断，所以 EN 明确接 IN。

输入用 2.2 µF/10 V X7R，输出用 4.7 µF/10 V X7R，紧贴相应 pin 与地回流。P2 给出的稳定性条件必须按**有效电容**满足：标称不小于 1 µF，并保证偏压、温度、容差后 >0.47 µF；4.7 µF 的字样不是已经核过具体 MPN 偏压曲线。原理图先写有效值下限，选实料后补充曲线/封装，不能随意换成同标称更小封装。

最终150 mA时，一阶标称耗散 `P=(5−3.3)×0.150=0.255 W`。P2 的 DBV JEDEC RθJA=231.1 °C/W 给出约58.9 °C温升；用最坏 V5=5.14599 V、V3V3=3.2505 V，则 `P≈0.28432 W`、温升约65.71 °C。环境上限收窄为40 °C，对应一阶结温约105.7 °C，尚未计邻近热源，仍待实际PCB测温。100.8 °C/W 的 EVM 数据不能无条件代替实际板；所谓“500 mA LDO”也不意味着 5 V→3.3 V、SOT23 上可持续500 mA。初稿120 mA/0—50 °C的计算已归档，现按本段和§10的电流预算执行。

最坏 V5 最低 4.876 V 仍比 3.3 V 高约 1.58 V，压差充足。实际要确认启动时上游电源没有被电容浪涌拉塌，以及负载跃迁时 V5 不跌入欠压。

**反向供电边界**：该 LDO 不提供反向隔离。外部把 V3V3 拉高、上游 V5 突然被短路、或输出总电容很大且输入快速消失，都可能令 OUT > IN+0.3 V，P2 §7.1.4 明确讨论此问题。P2 的 OUT→IN 外置肖特基方案是分流保护而非反向隔离。本练习禁止排针/SWD 反灌，USB VBUS 不供板电源；电源掉电波形与反流测试仍是实物释放项目，不能凭正常工况连接表宣布已解决所有掉电条件。

## 4. 第 21 课：同步 Buck 与关键回路

选 **TPS54202DDCR**：1 GND、2 SW、3 VIN、4 FB、5 EN、6 BOOT（P1 p3）。BOOT 的 100 nF 接 **BOOT—SW**，不是接地。EN 按手册允许悬空自动使能；本例不用未计算过的外部分压，更不能把 EN 直接接 9—16 V（EN 推荐最高 5.5 V，绝对 7 V）。芯片内部补偿，无外置 COMP pin；仍需检查 L/C 和前馈电容对应的环路。

电源参考起点是 15 µH、两只 22 µF 低 ESR 输出电容、75 pF 前馈（P1 p13—17）。本练习输出分压采用 100 kΩ/13.5 kΩ，均 0.1%，而非把原厂参考值 100 kΩ/13.3 kΩ 标成恰好 5.000 V。

`VOUT=VFB×(1+Rhi/Rlo)`；VFB 的 0.581/0.596/0.611 V 范围和电阻相反方向容差给出：

- 标称：0.596×(1+100/13.5)=5.0108 V。
- 最低：0.581×(1+99.9/13.5135)=4.8761 V。
- 最高：0.611×(1+100.1/13.4865)=5.1460 V。

这是静态范围，尚要给启动/跃迁/纹波留余量，实测 V5 不能超 LDO 推荐上限 5.5 V。上臂取自输出电容的干净电压点，FB 下臂 Kelvin 回芯片 GND；FB 与 75 pF 必须远离 SW。

选定实际电感 **Coilcraft XAL6060-153MEC**：15 µH±20%、DCR max43.75 mΩ@25 °C，Isat 5.8 A 的定义是25 °C、典型电感降30%；Irms 4.5 A/6 A分别对应20 °C/40 °C温升（P12 p1）。它比正常150 mA所需大，目的是不把“负载很小”误当成短路限流也只有150 mA：P1高侧限流max3.9 A，低侧max4.3 A。Isat温度降额及实际故障电流/温升仍需实测，不能把典型饱和点当绝对最大额定。原生L1的REQUIREMENTS保留初稿“covers nominal120mA”历史说明，**120mA不是电感额定值或现负载上限**；真实Isat/Irms不变，最终评审边界为150mA。

P12 p4 顶视 body X=6.36±0.2、Y=6.56±0.2 mm，高 max6.1 mm；双推荐 land 各 1.43×5.50 mm，**中心距 4.04 mm**，不是内边距。图上有 short-lead 标记，接高 dv/dt 端降低 EMI。本地封装约定 pin1 为右侧短引线（+2.02,0）接 SW，pin2 为左侧（−2.02,0）接 V5；这是本地 CAD 编号，原厂方向标记须保留。

CCM的一阶纹波估算：16 V、5 V、15 µH、500 kHz时，`ΔIL≈5×(1−5/16)/(15µ×500k)=0.458 A`；再考虑L−20%与频率最小390 kHz，约0.735 A。**在150 mA等轻载条件下，不应把Iout±ΔI/2算出的负电流当成实际电流**；不同VIN/L/f组合下可能进入脉冲跳跃/DCM，轻载声噪、纹波和采样噪声需看实际波形。

输入 22 µF/35 V X7R 要求 16 V 偏压下有效 ≥10 µF，另放 100 nF/50 V。入口 47 µF/35 V 电解补充电缆储能并提供一定阻尼。输出 2×22 µF/10 V 要求选实料后有效总值 ≥30 µF；75 pF 是官方低 ESR 起点，不是任意输出电容都稳定的证明。

布局顺序：先放 U_BUCK 与输入 HF/陶瓷电容，压缩 `CIN+→VIN→内部高侧/低侧开关→GND→CIN−` 的换流回路；再放 BOOT 小回路、SW 与电感、输出电容；最后放反馈。SW 铜面积适中、短，不穿过 ADC/晶振/反馈区；电感电流不能经细颈借道模拟地。地采用连续参考平面与受控电流路径，不能通过割地制造回流绕路。

## 5. 第 22 课：LC、磁珠与滤波位置

本练习不在整条 V3V3 上随意串“600 Ω@100 MHz”磁珠，也不把它当 600 Ω 直流电阻或固定电感。必须同时查其阻抗的 R/X 随频率变化、额定 DC/温升、偏置衰减、DCR、上游控制环输出阻抗、下游电容以及负载跃迁。器件的标称阻抗不是滤波器插入损耗。

用无损近似说明为什么连接顺序还不够：若 10 µH 与 10 µF 构成额外 LC，`f0=1/(2π√LC)≈15.9 kHz`。若源/绕组 ESR 很低，会在这附近放大而不是衰减纹波；磁珠与 MLCC 在其感性区域也会产生类似峰。应通过 R、适当 ESR 或阻尼支路控制 Q，再评估 DC 压降和负载瞬态，不能用“多放电容”替代阻尼分析。

本板 Buck 的 L/C 是控制环的一部分；入口电缆 L 与 MLCC 又是另一套潜在谐振。47 µF 电解的 ESR 可以改善后者，但不是已定量验证的阻尼结论。MCU 模拟供电若采用 R/磁珠隔离，由 D16/D19 的电流与启动条件决定；滤波器应放在噪声源/敏感负载边界，敏感端电容回流就近返回其供电脚附近的连续地，不能走开关功率换流回路。

信号滤波还要检查传输/时序：I²C 电容增大降低上升速度，SPI RC 会消耗采样建立时间，ADC RC 则同时影响抗混叠和采样电容充电；这些不是同一套“滤波越大越好”的规则。

## 6. 第 23 课：USB-C、差分与自供电

复用 B10 已建立的 **USB4105-GF-A 12land 封装**。12 个信号铜 land 对应 16 个接点，另有 SH1—SH4 本地 shell stake 编号。四个合并 land 为 A1_B12/GND、A4_B9/VBUS、B4_A9/VBUS、B1_A12/GND，不能直接关联未合并 pin 的 generic 16-pin 符号。

CC1 A5 和 CC2 B5 **各自**经 5.1 kΩ/1% 到 GND；不共用一只 Rd、不短接 CC1/CC2（P13 p8—10）。A6/B6 同属 D+，A7/B7 同属 D−，连接器附近短接对应两面信号；A8/B8 SBU 明确不使用。此电路没有 PD controller，不请求高于默认 5 V 或额外电流。

ESD 器件 **USBLC6-2SC6**：1/6 为同一 I/O1，3/4 同一 I/O2，2 GND，5 VBUS（P4 p1）。原理图两只等价脚必须同网；它是流通式布局的并联钳位器件，**不是在两脚间提供隔离、阻抗或串联保护**。本例 I/O1=D+，I/O2=D−。VBUS rail 放 100 nF 到 GND。ESD 器件紧邻连接器，焊盘流通走线，回地短宽，避免把放电电流先送进 MCU 地脚。

MCU PA12/PA11 各通过 22 Ω 到 D+/D−，靠 MCU 放置；这是特定 F103 Full Speed 电路起点，不是所有 USB PHY 都应加的统一电阻。差分网络类需要连续参考、短的支节、对称保护与跨层回流；实际阻抗由后续叠层确定，再生成 90 Ω 差分目标对应线宽/间距，不能现在随便写固定 mil 数。长度差/总长按本 PHY、PCB 和 USB 条件核定，不套用无来源的统一 5 mil/50 mm 门槛。

自供电时，D+ 1.5 kΩ 上拉必须在 VBUS 存在且 MCU 电源/时钟有效时才启用。Q_ATTACH 采用 **DMP2035U-7**：1 G 接 PA8=`USB_ATTACH_N`，2 S 接 V3V3，3 D 经 1.5 kΩ 接 USB_DP；100 kΩ G→S 默认关闭。相较 BSS84，本料有 -2.5 V 甚至 -1.8 V 的 Rds 保证（P8 p2），不是只用阈值宣称导通。

VBUS 检测用 **2N7002**：1 gate 从 USB_VBUS 经 **10 kΩ** 输入，并用 1 MΩ 下拉；2 source=GND；3 drain=`VBUS_PRESENT_N`，10 kΩ 拉到 V3V3，接 PB0。VBUS 最小 4.75 V 时 gate≈4.703 V，因此能对应 P7 Vgs=4.5 V 的 Rds 检查，sink 约 0.33 mA。此前 100 kΩ/1 MΩ 草稿只有 4.318 V，已经改为 10 kΩ，而非把典型曲线当 4.5 V 保证。

所需固件行为记录为：PB0=0且电源/USB时钟有效才 PA8=0；VBUS 丢失及时 PA8=1；复位/未初始化默认 detach；CAN 配置始终 detach。本课不把这段条件文字称为已运行固件。N-MOS 检测避免 VBUS 经分压器直接给掉电 GPIO 注入，但不代表整个 USB PHY 的掉电/热插拔已认证，还要做 DP/DM、MOS body diode、主机异常驱动及电源时序测试。

## 7. 第 24 课：UART、I²C、SPI、CAN

| 接口 | 电路选择 | 使用条件和 PCB 意图 |
|---|---|---|
| UART | PA9 TX 经 33 Ω 到排针；PA10 RX 经 0 Ω，占位并用 10 kΩ 拉高 | 3.3 V CMOS、参考地并行；不能接 RS-232；TX 阻尼电阻靠真正驱动端 |
| I²C | PB6=SCL、PB7=SDA，原版各2.2 kΩ/1%，教学ECO改3.3 kΩ/1% | 开漏；**默认100 kHz**、总线估算≤100 pF；≤400 kHz仅为条件上限/RC预算，外部重复上拉须合并计算 |
| SPI | PA4 NSS、PA5 SCK、PA7 MOSI 各 33 Ω；PA6 MISO 0 Ω；NSS 10 kΩ 拉高 | 先限 ≤1 MHz、外接 ≤10 cm；根据边沿而非仅比特率判断传输线；MISO 阻尼应靠外部从机驱动端 |
| CAN | TCAN332DR、100 nF+1 µF 本地去耦、TXD 10 kΩ 拉高、可选 120 Ω/0.25 W 端接 | 总线两端各 120 Ω、分支短、共模范围受控、另带参考地；不能每个节点都装 120 Ω |

I²C 的算例来自 P6 p50：`Rmax=trmax/(0.8473Cb)`。400 kHz 的 trmax=300 ns、Cb=100 pF 时，Rmax≈3.54 kΩ。保守取器件能保证 sink3 mA、VOL≤0.4 V，V3V3max=3.465 V，则 Rmin≈(3.465−0.4)/3mA=1.022 kΩ。2.2 kΩ/1% 落在区间内，标称 tr≈186 ns；Rmax、最坏 VOL 和静态电流都要与实际节点数量/容差复算。400 pF 时同一 2.2 kΩ 约 746 ns，不能继续宣称满足 400 kHz；要减小电容、改变上拉/模式或使用合适 buffer。

**最后复核补充**：P15同一版DS5319的p68表41脚注2要求400 kHz时PCLK1为10 MHz的整数倍，而p69表42又列出PCLK1=36 MHz、400 kHz、CCR=0x801E，两处条件不一致。本课不自行裁定其优先级，默认100 kHz；400 kHz只保留为RC设计上限，必须再核外设时序/固件及实板。ECO 3.3 kΩ在+1%/100 pF时tr≈282.405 ns，虽小于300 ns，但电容上限仅约106.23 pF，探头/线缆/新节点增加后必须重算。此值只证明RC预算，不证明全部400 kHz时序或已运行通过。

TCAN332DR必须按**332**核pin：1 TXD、2 GND、3 VCC3.3 V、4 RXD、5 NC、6 CANL、7 CANH、8 NC。pin5/8不是同族TCAN334的SHDN/STB。TXD已有内部上拉（P3 p4），另用可见10 kΩ保证默认recessive。P3 p6表5.5给出dominant max55 mA@RL60 Ω、60 mA@RL50 Ω，recessive max3.5 mA；bus fault条件可达180 mA。**初稿120mA不足以同时覆盖MCU50+CAN60+外载10后再加偏置，已修订正常系统上限150mA，故障180mA不属于正常供电/热保证**。

装配 profile：USB 装 R_USB_DP/DM=22 Ω，R_CAN_TX/RX=0 Ω 不装；CAN 时反转。不能四只同时装后靠“软件只开一种”掩盖 RXD 推挽与 USB 物理端相连的问题。即使把 CAN remap 到其他脚，也不能回避该 STM32 的 USB/CAN 同时使用限制；具体 MCU 手册由 D15/D24 主记录引用。

## 8. 第 25 课：入口保护、ESD 与回流边界

实际入口顺序为 **J_PWR → F_IN 500 mA/32 V fast → D_REV SS14 → VIN_PROT 的 bulk/HF 电容与 Buck**。SS14 阴极色带向内部 VIN_PROT，局部 CAD pin1=K、pin2=A。保险丝提供二次过流保护，不负责钳位；输入反接由串联二极管截止。要核启动浪涌与 F_IN 的 I²t/时间电流曲线，不把保险丝额定 500 mA 当精密限流器。本例所选 467.500 的标称 I²t=0.0087 A²s（P10 p1），实际连接电容、台源限流及插拔条件决定是否误断。

**拒选 TVS 的完整理由**：SMBJ16A 的 VRWM=16 V 看似适合输入上限。P11 p3 却给出 10/1000 µs、23.1 A 时 VCL=26 V；8/20 µs、116 A 时 VCL=34.4 V。TPS54202 推荐 VIN≤28 V、绝对最大 30 V，再加线路寄生，不能据前一个 26 V 数字宣布“浪涌保护通过”。本版不默认安装输入 TVS，也不保留一个未经协调就称为保护完成的占位结论；若后续要求外部电缆浪涌，重新确定波形/源阻抗/能量、TVS动态电阻、限流/OVP或更高耐压前级，并测输入峰值。

同理，TCAN332 的 CANH/L 绝对边界是±14 V（P3 p5），不能机械套用 24 V CAN TVS 或 SM712 就认定可承受任意短电源故障。该 IC 的器件级 IEC ESD 条件只是器件指标；本练习对短台架 CAN 不虚构整机浪涌/ESD验证。若要汽车/工业长缆，应更换/核定总线故障耐压更高的收发器与相匹配保护，并重新考虑隔离、共模、终端、机壳参考。

USB shell 的四只 stake 在本台架无独立金属机壳的前提下就近接板 GND；GCT 图纸 shell 标 GND。以后有金属机壳时，应先定义 chassis/信号地和放电回路，再决定直连/电容/RC，不凭经验统一割成悬浮 shield。CC/SBU 没被 USBLC6 的两路数据钳位覆盖；本版 SBU 不用、CC 仅 Rd，没有宣称覆盖 Type-C short-to-VBUS 或所有接点 ESD。需要这样的使用等级时必须另加合适 Type-C port protection，不能增加两只电阻就当全部保护齐全。

## 9. 已学会的复核方法与验收边界

| 课程 | 本次形成的可复核产物 | 尚不能用本笔记替代的工作 |
|---|---|---|
| 20 | 指定 DBV pin、有效电容条件、压差/热计算、反流条件 | 实料偏压曲线、实板热/掉电测量 |
| 21 | 指定 Buck pin、BOOT回路、反馈容差、实料15µH及land、关键回路 | 环路稳定性、DCM纹波/负载跃迁、PCB真实布局 |
| 22 | LC谐振例与阻尼/偏置/源负载分析，不滥加磁珠 | 真实阻抗/器件曲线、台架滤波传递测量 |
| 23 | 12land USB映射、双Rd、自供电sense/attach、ESD等价脚 | USB固件/枚举、眼图/兼容/整机ESD和掉电 |
| 24 | UART/I²C/SPI/CAN明确电平与拓扑、上拉计算、模式表 | 外部实际从机/电缆时序、CAN错误/故障测试 |
| 25 | 入口保护次序、保险丝/反接、TVS拒选、机壳/回流边界 | 已定等级的保护测试；未承诺任何未测认证 |

本次典型错误及纠正已经保留：把 TCAN332 的 NC 当 STB；把 Type-C 16接点直接套12land；把 USBLC6 两端当独立网络；把 TPS54202 EN 接高压 VIN；把 BOOT 接地；把 LDO EVM 热阻当实板；用小负载选择承受不了 IC 限流的电感；只读 TVS 单一波形钳位；VBUS gate 分压后仍引用更高 Vgs 的 Rds 保证。这些检查应继续进入 ERC 解释表及后续 PCB 审查。

继续跟进时先读总记录、最终设计 spec 和原生导出验收结果，再进入 PCB 布局。不要重新以本分工 JSON 覆盖根工程已经合并的 MCU/模拟/调试部分，也不要把 BOM 中待补实料项目解释为制造释放。

## 10. 最终原生工程独立读回、问题修复与电流预算闭环

本节是实际数据库结果；前面40项检查是设计规格检查，两者分别保留。最终文件为 [DE_INTEGRATED_SINGLE.DSN](../examples/de_15_26_20261019/native/DE_INTEGRATED_SINGLE.DSN) 与 [de_integrated_eco_final.dsn](../examples/de_15_26_20261019/native/de_integrated_eco_final.dsn)。它们实际以单个DE_CONTROL页保存并重开；课程模块页名作为语义分组记录，不能把前期多页试验称为最终已经全部读回的六页设计。

根代理用Capture 17.2原生数据库SDK分别在独立进程中保存/重开；本分工只读取其TSV输出，没有调用native API、没有打开GUI。两版全工程均80件、272个物理pin，其中6个明确NC、266条连通成员、69个FlatNet；本次独立审查其中电源/接口的**52件、每版146个物理pin**，并另查12个MCU接口物理脚的关联。

独立脚本以原始power spec及原厂pin表为依据，用`module_id→正式reference`映射，未仅重读根合并后的JSON来宣布正确。最终报告：[power_native_review.json](../logs/de_15_26_20261019/power_native_review.json)，**1577/1577细项通过**，结果为`PASS_WITH_DOCUMENTED_RELEASE_GAPS`；脚本：[de_power_native_review.py](../scripts/de_power_native_review.py)。报告含全部输入文件SHA-256、逐pin证据、两版差异和未释放边界。

实际核对包含：

- 原生pin数量/编号、每pin网络、NC标记；TPS54202的EN明确不连且BOOT电容接SW，LDO的NC4、CAN332的NC5/8正确。
- USB4105的12land合并编号、独立CC1/CC2、双DP/DM、SH1—4及不用的SBU；USBLC6同通道两脚同网；Q1 gate前串阻最终R7=10k。
- MCU物理18/PB0读VBUS、29/PA8控制attach、32/33对应PA11/PA12，UART/I²C/SPI的实际物理脚与子网吻合。
- 原生保存重开后`ASSEMBLY`、`assembly_group`、`source_description`、`REQUIREMENTS`、`MPN_STATUS`以及ECO原因；两版52件的这些属性已经实际导出核对。
- 默认USB装配R5/R6=22Ω装、R12/R13=0Ω不装，CAN装配时反转。原始网表仍包含四只选择电阻，**互斥依赖实际装配**；不是原始网表自动断开了DNP器件。
- ECO R19/R20的Value与当前source_description、BOM Specification均为3.3k/1%，ECO_REASON保留修订依据；原版2.2k/1%仍保留为历史和推荐起点。J13的PB8/9换位不改变本分工接口。

审查发现并完成修复的文档问题：初版BOM只有归一后的Value，遗漏R1/R2的0.1%、C2的35V/X7R、C5/C6的10V/X7R等采购必需信息；随后新增Specification、Procurement_Status、Requirements及Assembly。新拼接又使L1/J2的说明后缀重复，已去重。最终 [BOM_baseline.csv](../examples/de_15_26_20261019/BOM_baseline.csv) 与 [BOM_eco.csv](../examples/de_15_26_20261019/BOM_eco.csv) 的完整规格已经复核，不再把“图上Value正确”当作采购规格完整。修复前审查快照保留在 [power_native_review](../staging/de_15_26_20261019/power_native_review/)。

**第15课的供电预算复审引发了实际边界修订**。P15 p40—41表13的MCU50.0mA条件是72MHz、Flash数据处理、8MHz HSE/PLL、全外设，且I/O静态输入无负载；外部负载不能藏在这个50mA里。P3 p6的CAN最坏正常dominant取60mA，仅50+60+外载10就已耗尽初稿120mA，I²C等支路尚未计算。因此最终采用以下受控分配：

| 正常工况分配项 | mA | 依据/范围 |
|---|---:|---|
| MCU72MHz全外设 | 50.0 | DS5319表13最大值@TA85°C；不是GPIO外部驱动电流 |
| CAN dominant | 60.0 | TCAN332表5.5、RL50Ω最大正常电流；端接电流已含其中，不能再重复加 |
| GPIO与header合计外载 | 10.0 | **合计上限**，包含排针供电与GPIO外部驱动，不能各自再取10mA |
| 两只I²C上拉同时拉低 | 3.2 | 按原版2.2k、−1%、3.465V保守取整；ECO3.3k约2.12mA |
| 其余偏置支路预留 | 3.0 | UART/NSS/TXD/sense/复位与BOOT等，不把这些都当零电流 |
| 模拟电源保守预留 | 5.0 | 工程预算，不是假称手册给出固定5mA；可能与全外设IDD部分重叠，保守保留 |
| 板内开关/未建模项预留 | 5.0 | 工程预算；外部GPIO负载仍受上面合计10mA限制 |
| 分配小计 | **136.2** | 正常CAN配置的保守分配 |
| 至150mA余量 | **13.8** | 后续新增负载必须从余量中扣除 |

USB配置以CAN recessive最大3.5mA代替60mA，另留D+上拉2.4mA，按相同保守分配约82.1mA。CAN bus fault的180mA不属于正常保证，必须另做故障/热/电源行为验证。150mA不是实测功耗，也不是承诺任意固件和外接负载都不超过它；它是后续功耗实测必须满足的设计上限。

与新电流上限一起把环境收窄为0—40°C。LDO按最坏V5max5.14599、V3V3min3.2505、150mA得到0.28432W，JEDEC231.1°C/W一阶升65.71°C，40°C环境下约105.7°C；真实PCB散热、器件容差和邻近热源仍待测试。无需更换原生元件或再次运行native进程。原生L1属性中的nominal120mA仅为初稿历史上下文，实际电感Isat5.8A/Irms4.5A保持不变；当前边界以本节及power spec的150mA/0—40°C为准。

120mA版本的spec、生成器、记录与审查报告已完整备份在 [power_budget_before150mA](../staging/de_15_26_20261019/power_budget_before150mA/)。最终生成器/JSON、设计40项复核及原生1577项复核已经同步新边界；Capture GUI ERC、实板启动/USB枚举/CAN通信、波形与温度、ESD/浪涌均未由这些数据库读回替代。
