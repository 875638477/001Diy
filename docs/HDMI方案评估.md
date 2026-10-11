# RK3576 HDMI 方案评估

评估对象是本库中的 RK3576（`005lib/01Psm_lib/soc_rk3576_bga698_16r1x17r2x1r0.txt`，BGA698）以及现有 HDMI 连接器封装。PHY 与控制脚对照公开原理图 [DshanPi-A1 RK3576 SCH V1.1](https://dl.100ask.net/Hardware/MPU/RK3576-DshanPi-A1/DshanPi-A1-RK3576-SCH_V1.1.pdf)；DDC 上拉与专用总线说明对照 [LCB3576 设计指南](https://www.aipaipai.wiki/neardi/rockchip-rk3576/LKB3576/hardware-manual/hardware_design_guide)。连接器侧的 5V、ESD 和交流耦合以 HDMI 源端惯例给出，具体阻容与 ESD 型号以《RK3576 Hardware Design Guide》为准。

## 结论

单路外接显示器，使用 RK3576 原生 HDMI 2.1 直出 Type-A。Combo PHY 固定做 HDMI，eDP 留空。连接器到芯片的差分走线放在同一块板上并尽量短，默认不加 redriver、不加 1 分 2 开关。

必须同时接板载 eDP 屏和外接 HDMI 时，原生 PHY 只有一组，两路不能同时工作。外接口改走 MIPI DSI 转 HDMI，或改用 USB3 OTG0 上独立的 DP 1.4。

## 芯片能力

原理图对这组 Combo PHY 的标注：

| 项目 | 标注 |
| --- | --- |
| 协议 | HDMI 2.1 / eDP 1.3，二选一 |
| 速率 | HDMI 12 Gbps；eDP 5.4 Gbps |
| 分辨率 | HDMI 2.1，最高 4K×2K@120Hz |
| 差分 | D0–D3，共 4 对；边带 SBD（eDP 时为 AUX） |
| 基准电阻 | `HDMI_TX_REXT`，参考图 R44 = 8.2 kΩ、1%、0201 |

四路电源球：

| 信号 | 球位 |
| --- | --- |
| `HDMI_TX_EDP_TX_AVDDD0V75` | 2N11 |
| `HDMI_TX_EDP_TX_AVDDC0V75` | 2P11 |
| `HDMI_TX_EDP_TX_AVDDIO1V8` | 2N10 |
| `HDMI_TX_EDP_TX_AVDDCMN1V8` | 2P10 |

另有 `VDDA0V75_HDMI_S0`，参考图由 RK806 NLDO3 供给。0.22 ?F/0201 去耦放在封装下方，1 ?F 与 4.7 ?F 靠近电源脚。

差分球位与库内符号 `FUNCTION G17` 一致：

| 信号 | 球位 |
| --- | --- |
| D0N / D0P | AK27 / 1AE24 |
| D1N / D1P | AL28 / AK28 |
| D2N / D2P | AK29 / AJ28 |
| D3N / D3P | AK26 / AL26 |
| REXT | 1AA20 |
| SBDN / SBDP | 2U12 / 2T12 |

控制脚在 VCCIO6（1.8 V 或 3.3 V），默认使用 M0：

| 功能 | GPIO | 球位 | 库内符号可见名称 |
| --- | --- | --- | --- |
| CEC | GPIO4_C0 | AK3 | `PWM1_CH5_M1_|_UART11_TX_M2_|_SP` |
| HPD | GPIO4_C1 | AK2 | `PWM0_CH1_M1_|_UART11_RX_M2_|_ED` |
| DDC SCL | GPIO4_C2 | AL2 | `PWM2_CH0_M1_|_UART9_TX_M2_|_CAN` |
| DDC SDA | GPIO4_C3 | 1AE2 | `PWM2_CH1_M1_|_UART9_RX_M2_|_CAN` |

备用组：HPD M1 在 GPIO0_B6，CEC M1 在 GPIO0_C3。SCL/SDA 只有这一对专用脚。

Allegro 器件文件把管脚名截到约 31 个字符，`HDMI_TX_HPDIN_M0`、`HDMI_TX_CEC_M0`、`HDMI_TX_SCL`、`HDMI_TX_SDA` 在符号上不可见。画原理图时按上表球位锁定，避免把这四脚当成普通 PWM 或 UART。

## 方案比较

| 方案 | 适合的产品 | 主要代价 | 建议 |
| --- | --- | --- | --- |
| A. 原生 HDMI 直出 Type-A | 一块外接显示器，需要 4K120 | PHY 不能再做 eDP；走线按 12 Gbps 处理 | 默认采用 |
| B. 同一 PHY 改接 eDP 屏 | 只有板载屏 | 没有 HDMI 座 | 与 A 互斥 |
| C. USB3 OTG0 的 DP 1.4（Type-C Alt Mode） | 需要与板载 eDP 同时存在的外接视频口 | 另做 CC/PD；分辨率能力独立于 HDMI PHY | 作为第二路视频口 |
| D. MIPI DSI 转 HDMI（如 LT8912B、IT6161 一类） | 板载 eDP 已占用 PHY，仍要 HDMI 座 | 多一颗桥、多路电源；常见能力停在 HDMI 2.0、4K60 | 仅在 A 不可用时 |
| E. RK628 | 需要 HDMI 输入，或额外的协议转换 | 独立时钟、电源和驱动；DshanPi 上它是单独功能块 | 本机只做输出时不引入 |
| F. HDMI 开关或 1 分 2 | 两个座子 | 器件要核对是否支持 FRL 12 Gbps；软件和热插拔更复杂 | 单座产品不引入 |
| G. TMDS redriver / retimer | SoC 到座子经过长走线、板对板或线缆 | 多一颗高速器件，供电和摆幅要重调 | 直连且走线短时不引入 |

LCB3576 设计指南把 USB3 OTG0/DP 1.4 与 HDMI2.1/eDP TX 分成两节。DP 可以和 HDMI 同时留在板上；eDP 与 HDMI 共用 D0–D3 和 SBD，不能同时工作。

## 推荐电路

### 直出 Type-A

1. Combo PHY 只接 HDMI。eDP 功能在设备树里关闭。
2. VCCIO6 用 3.3 V。DDC 上拉 2.2 kΩ 接到 VCCIO6。这对脚是 HDMI 控制器内部的 DDC，不改接到通用 I2C，也不与 PMIC 所在的 I2C1 合并。
3. 连接器侧 DDC、HPD、CEC、+5V 按 5 V 域处理。SoC 侧是 VCCIO6，中间用带电平转换的 HDMI ESD 器件，或分立 MOS 电平转换加端口 ESD。HPD 必须进 AK2，供 PHY 判断对端是否插入。CEC 可以留空；若产品要做 CEC，占用 AK3。
4. 连接器第 18 脚 +5V 用限流负载开关。HDMI 源端对这条电源有最小供出电流要求，用开关或自恢复保险丝限制短路电流。
5. 差分阻抗 100 Ω。四对数据加 SBD 同组走线，参考地连续，过孔成对。连接器外壳多点接到机壳地，ESD 放在座子旁边。
6. HDMI 2.1 FRL 为交流耦合。耦合电容容值、位置（靠近座子或靠近芯片）按 Hardware Design Guide 放置，不用 0 Ω 代替。
7. `HDMI_TX_REXT` 用 8.2 kΩ、1%，紧贴 1AA20。
8. 软件 pinctrl 使用 M0：HPD、CEC、SCL、SDA。只做固定分辨率、不读 EDID 时仍保留 HPD。

### 什么时候改方案

- 结构要求板载 eDP，同时又要一个外接口：PHY 给 eDP，外接口用方案 C 或方案 D。优先方案 C，因为它不占用 DSI，也不额外引入 HDMI 桥的带宽上限。
- 座子在另一块板，差分经过板对板连接器：先算通道；插损不够再加支持 12 Gbps FRL 的 retimer。只支持 TMDS 6 Gbps 的 redriver 会把 4K120 卡住。
- 需要采集外部 HDMI：用方案 E，接收 PHY 与 RK3576 的发送 PHY 分开。

## 库内封装

`005lib/01Psm_lib` 里有多套 HDMI 封装，来源混杂（封装字符串里能看到 NVIDIA、Wieson、Winwin、Beagle 等字样）。在选定连接器料号并把焊盘与规格书核对之前，这些封装只作外形参考。

| 库文件 | 观察 | 使用建议 |
| --- | --- | --- |
| `hdmia19_hdmi_01a` | 封装属性写明 23 脚、毫米单位 | 最接近标准 Type-A（19 信号脚加壳体），仍需对规格书 |
| `hdmi_a19p_w`、`hdmii_19p-w`、`hdmi-19pw`、`dip_hdmi-a` | 卧式或插件外形，网格和层名不统一 | 先确认是立式、卧式还是插件，再核对 |
| `hdmi_A_19p-pcb`、`hdmi_a_19p-pcb` | 名称指向 PCB 安装型 Type-A | 与 3D `HDMI_A_19P_PCB.STEP` 可能是一对，需一起核对 |
| `cn_hdmi_19_050` | 焊盘名指向 0.254 mm 级别细间距 | 更像板端细间距座，不是标准 Type-A 母座 |
| `hdmi_19pmini`、`hdmi_mini_19p_w`、`hdmi-mini-w-dip` | Mini HDMI | 整机外接口优先 Type-A；高度不够时再评估 Mini |
| `01_3d_step_lib/hdmi_19p_smt_jxd.stp` 等 | 四个 HDMI STEP | 只用于结构干涉检查，不代替焊盘图 |

Capture 库 `01captureLib` 中没有 HDMI 连接器符号。原理图符号需要按选定料号新做，信号脚顺序与 Allegro 封装脚号一一对应。

## 落地顺序

1. 结构确定 Type-A 立式或卧式料号，按规格书新建或修订封装，并挂上对应 STEP。
2. 原理图按球位表连接 PHY、REXT、四路 PHY 电源和 VCCIO6 的 HPD/DDC/CEC。
3. 连接器页完成 +5V 限流、5 V 到 VCCIO6 的电平转换和 ESD。
4. PCB：100 Ω 差分，耦合电容与 ESD 的位置按设计指南，REXT 与 0.22 ?F 贴近芯片。
5. 设备树固定 M0 pinctrl，并确认 eDP 节点关闭。
