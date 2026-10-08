# USB/IP 方案评估

更新时间：2026-10-08

## 1. 项目目标

设计一款运行 OpenWrt/Linux 的 USB/IP 设备，将本地 USB 外设通过有线网络或 5 GHz Wi-Fi 提供给远端主机使用。

主要需求：

- 必须具备 USB Host；
- 优先支持 USB 3.0；
- 最好具备 PCIe，用于扩展无线网卡等设备；
- 优先选择封装内置 DDR 的 SoC，以降低 PCB 层数和布线难度；
- OpenWrt 和 Linux 驱动应尽量成熟；
- 希望获得硬件参考设计，最好是 Cadence OrCAD/Allegro 格式；
- 曾考虑将整机做成 PCIe 插卡，因此需要确认 SoC 是否支持 PCIe Endpoint。

## 2. 需求演变记录

1. 初始参考为 MT7628DAN：内置 DDR、2.4 GHz Wi-Fi、USB 2.0 Host，但缺少 5 GHz Wi-Fi。
2. 寻找同时具备 5 GHz Wi-Fi、USB Host 和较好 OpenWrt 支持的芯片。
3. 扩大范围至带 PCIe 的全志、瑞芯微及老款网络 SoC。
4. 增加“最好内置 DDR”的要求。
5. 考虑 `RK3528 + RTL8852BE`。
6. 明确核心用途实际是 USB/IP，而不是普通无线路由。
7. 考察 MT7621DA/MT7621DAT 的硬件参考设计。
8. 确认 MT7621DA 能否作为 PCIe Endpoint 插入 PC 主板。

## 3. USB/IP 对硬件的真正要求

USB/IP 服务端的关键不是 PCIe 本身，而是：

- 稳定的 USB Host 控制器；
- 足够的 CPU 单核性能和内存；
- 稳定的千兆以太网或 5 GHz Wi-Fi；
- Linux `usbip-host`、`usbipd` 和对应 USB Host 驱动；
- 足够可靠的 USB 5 V供电、限流和浪涌处理。

PCIe 仅在以下情况必要：

- 外接 5 GHz/Wi-Fi 6 网卡；
- 外接额外以太网控制器；
- 计划实现 PCIe Endpoint 直连 PC。

## 4. 候选方案对比

| 方案 | DDR | USB | 网络/无线 | OpenWrt成熟度 | 主要问题 |
| --- | --- | --- | --- | --- | --- |
| MT7628DAN | 封装内置 | USB 2.0 Host | 2.4 GHz、百兆网络 | 高 | 没有5 GHz，性能低 |
| MT7621DAT + MT7613/MT7615 | 内置128 MB DDR3 | USB 3.0/2.0 Host | 五口千兆交换机，PCIe无线 | 很高 | CPU较老，内存固定 |
| MT7981B + MT7976 | 外置DDR3/DDR4 | USB 3.0 Host | 原生双频Wi-Fi 6、千兆/2.5G | 很高 | 需要外置DDR |
| RK3528 + RTL8852BE | 外置DDR | PCIe启用后主要保留USB 2.0 | PCIe Wi-Fi 6、原生GMAC | 提升中 | PCIe与USB3复用PHY；Realtek AP驱动一般 |
| RK3568 + PCIe Wi-Fi | 外置DDR | 可配置USB 3.0 | 双GMAC、多个PCIe资源 | 较高 | PCB、PMIC、DDR复杂 |
| 全志A523/T527 | 外置DDR | USB3与PCIe复用 | PCIe 2.1 x1 | 较新 | PCIe和USB3不能同时使用，支持仍在完善 |

## 5. 推荐方案

### 5.1 低成本、内置DDR：MT7621DAT

推荐结构：

```text
MT7621DAT
├── 内置128 MB DDR3 KGD
├── SPI NOR或SPI NAND
├── USB 3.0 Host ── USB/IP目标设备
├── PCIe ── MT7613/MT7615无线芯片
└── 内置千兆交换机 ── 有线网络
```

优势：

- 封装内置128 MB DDR3，不需要在主板上布DDR；
- 三路PCIe Host；
- USB 3.0和PCIe可以同时使用；
- 内置五口千兆交换机；
- OpenWrt `ramips/mt7621` 支持成熟；
- USB/IP官方软件包可用；
- 成本和PCB复杂度相对较低。

局限：

- 双核MIPS 880 MHz平台较老；
- 128 MB内存固定，软件包需要控制规模；
- USB/IP、TCP和USB Host中断会占用CPU，高速USB实际性能需打样测试；
- 不适合需要高速存储级吞吐或大量并发客户端的场景。

无线建议：

- MT7613：Wi-Fi 5 2×2，适合低成本5 GHz；
- MT7615：成熟的双频Wi-Fi 5方案；
- MT7915：可以实现Wi-Fi 6，但128 MB内存较紧，需要严格裁剪固件。

### 5.2 综合性能优先：MT7981B + MT7976

如果可以接受外置DDR，MT7981B更适合作为新设计：

- 双核Cortex-A53约1.3 GHz；
- 原生2.4/5 GHz Wi-Fi 6，不占用PCIe；
- USB 3.0 Host；
- 千兆和2.5G网络能力；
- OpenWrt `mediatek/filogic` 主线支持成熟；
- 建议配置512 MB DDR4。

现成验证平台可使用 GL.iNet GL-MT3000。该平台具有USB 3.0、双频Wi-Fi 6、千兆/2.5G网口和主线OpenWrt支持。

## 6. RK3528 + RTL8852BE评估

该组合硬件上能够连接：

- RK3528提供PCIe 2.1 x1；
- RTL8852BE是PCIe Wi-Fi 6 2×2芯片；
- PCIe 2.1 x1带宽足够RTL8852BE使用。

但它不适合作为本项目首选：

1. RK3528的PCIe和USB 3.0使用同一Combo PHY，启用PCIe连接RTL8852BE后不能同时使用该USB 3.0 PHY。
2. 独立USB 2.0 Host仍可使用，因此仅适合USB 2.0目标设备。
3. RTL8852BE定位偏笔记本网卡；Linux `rtw89` 的客户端模式较好，但AP、多SSID和STA+AP并发不如路由器专用MediaTek无线方案成熟。
4. RK3528需要外置DDR。
5. RK3528的OpenWrt PCIe、Combo PHY和板级支持比MT7621/MT7981更新，量产前需要更多验证。

## 7. USB/IP软件方案

OpenWrt 24.10软件包：

```sh
opkg update
opkg install kmod-usb3 usbip-server usbip-client
```

服务端基本操作：

```sh
usbip list -l
usbip bind -b <BUSID>
/etc/init.d/usbipd enable
/etc/init.d/usbipd start
```

Linux客户端：

```sh
modprobe vhci-hcd
usbip list -r <服务器IP>
usbip attach -r <服务器IP> -b <BUSID>
```

USB/IP特性及限制：

- 一个已导出的USB设备通常由一个客户端独占；
- 基于TCP传输，延迟、抖动和重传会影响实时USB设备；
- 网络异常时，远端系统看到的效果类似USB设备突然拔出；
- 不建议将未经保护的USB/IP端口直接暴露在互联网；
- 推荐在可信局域网、WireGuard或其他受控隧道内使用。

适合的USB设备：

- USB转串口；
- JTAG、烧录器；
- 加密狗；
- 打印机；
- HID；
- CAN、RS485适配器。

需要重点验证的设备：

- USB声卡和摄像头等同步/等时设备；
- U盘、移动硬盘等文件系统设备；
- 高速数据采集卡；
- 对延迟、断线恢复敏感的专用设备。

## 8. USB供电设计要求

USB/IP设备往往长期无人值守，USB供电不能直接依赖简单的5 V直连。

建议：

- 每个外部USB端口使用带限流、过流和热保护的高侧电源开关；
- USB 3.0端口至少按5 V/900 mA设计，产品需要更高负载时应预留1.5 A或独立供电；
- 提供可由GPIO控制的USB VBUS开关，以便软件远程断电重启USB设备；
- 增加ESD保护和足够的输入/端口电容；
- USB 3.0差分线按90 Ω差分阻抗设计；
- 对硬盘、无线适配器等高峰值负载，优先使用外部供电或有源Hub。

## 9. MT7621DA/MT7621DAT命名及启动配置

- `MT7621DA` 是集成128 MB DDR3 KGD的型号；
- 资料和设计包名称通常使用 `MT7621DA`；
- 市场及部分BOM中常见完整订货名称 `MT7621DAT`；
- U-Boot中存在专门的 `128MB KGD (MT7621DA)` DDR时序配置；
- OpenWrt中它与其他MT7621变体共用 `ramips/mt7621` 平台，不存在独立的 `mt7621dat` target。

不能将MT7621AT外置DDR参考设计中的DDR部分直接用于MT7621DA。USB、PCIe、交换机、电源和Flash部分可以作为辅助参考，但必须结合MT7621DA专用设计资料复核。

## 10. MT7621DAT硬件参考设计

### 10.1 建议向MediaTek代理商/FAE索取

最匹配的参考设计名称：

```text
AP-MT7621DA+MT7603E+MT7613B-V11-2L-20190430
```

建议明确索取以下文件：

1. OrCAD Capture原理图 `.dsn`；
2. Allegro PCB `.brd`；
3. Allegro封装库 `.dra`、`.psm`、`.pad`；
4. Constraint Manager规则和阻抗约束；
5. PCB层叠和阻抗表；
6. BOM；
7. Gerber和钻孔文件；
8. MT7621DA Design Guide；
9. 电源时序说明；
10. 128 MB KGD DDR启动和时序配置说明。

公开网络上尚未找到能够确认真实性和完整性的原生Cadence工程。部分页面仅有下载说明或README，不能视为已取得HDK文件。

### 10.2 Oolite V8.1

Oolite V8.1是能够确认使用MT7621DAT的量产模块：

- MT7621DAT；
- 内置128 MB DDR3；
- MT7603EN 2.4 GHz；
- MT7613BEN 5 GHz；
- USB 3.0；
- 三路PCIe中两路用于无线，剩余一路扩展；
- 五口千兆交换机。

其公开规格书包含模块管脚、电源、接口和PCB设计提示，但没有公开完整Cadence裸片参考设计。

### 10.3 PADS资料转Cadence

公开的MT7621参考设计较多为PADS格式，而且很多使用外置DDR的MT7621AT。

如果只能获得PADS PCB：

1. 从PADS导出ASCII `.asc`；
2. 在Allegro PCB Editor中选择 `File → Import → CAD Translators → PADS`；
3. 配置层映射后生成Allegro `.brd`；
4. 人工复核焊盘、过孔、铜皮、阻焊、层叠、差分对和约束；
5. 原理图建议在OrCAD中重新整理，并按网表与PCB交叉检查。

格式转换不能替代电源完整性、信号完整性和可制造性复核。

## 11. MT7621DA能否作为PC的PCIe插卡

不能直接实现。

MT7621DA的PCIe控制器只支持Root Complex/Host模式，用于连接Wi-Fi网卡等PCIe Endpoint。PC主板的PCIe控制器同样是Root Complex，两个Root Complex不能直接连接，PC也无法把MT7621DA枚举为PCIe设备。

```text
支持：
MT7621DA PCIe Host → PCIe Wi-Fi Endpoint

不支持：
PC PCIe Host → MT7621DA PCIe Host
```

可以把MT7621DA设备做成PCIe插卡外形并从插槽取电，但数据仍需走千兆网口或Wi-Fi；此时PCIe金手指的数据线不使用。

如果必须通过PCIe直接与PC通信，需要选择支持PCIe Endpoint模式的SoC，并实现：

- PCIe Endpoint控制器驱动；
- DMA或共享内存传输；
- PC端驱动；
- 虚拟网卡、NTB、virtio或自定义协议。

之后才能在该虚拟链路上运行USB/IP。此方案的软件和驱动开发量远高于标准以太网USB/IP。

## 12. 当前结论

按现有需求排序：

1. **MT7621DAT + MT7613/MT7615**：满足内置DDR、USB 3.0、PCIe、5 GHz和成熟OpenWrt，适合低成本USB/IP产品。
2. **MT7981B + MT7976**：外置DDR，但综合性能、无线能力和后续维护更好，适合新产品。
3. **RK3528 + RTL8852BE**：仅在目标设备为USB 2.0且能接受无线驱动风险时考虑。
4. **PCIe直插PC方案**：MT7621DA不支持，应重新选择具备PCIe Endpoint能力的平台。

在确定SoC前，必须先明确目标USB设备类型、USB版本、期望吞吐、客户端操作系统和断线恢复要求。不同USB设备对USB/IP的兼容性差异可能比SoC性能差异更重要。

## 13. 参考链接

### OpenWrt与USB/IP

- [OpenWrt官方源码](https://github.com/openwrt/openwrt)
- [OpenWrt MT7621公共设备树](https://github.com/openwrt/openwrt/blob/main/target/linux/ramips/dts/mt7621.dtsi)
- [OpenWrt MT7621镜像定义](https://github.com/openwrt/openwrt/blob/main/target/linux/ramips/image/mt7621.mk)
- [OpenWrt HLK-7621A参考设备树](https://github.com/openwrt/openwrt/blob/main/target/linux/ramips/dts/mt7621_hilink_hlk-7621a-evb.dts)
- [OpenWrt USB/IP使用说明](https://openwrt.org/docs/guide-user/services/usb.iptunnel)
- [OpenWrt USB/IP软件包源码](https://github.com/openwrt/packages/tree/master/net/usbip)

### MT7621DA/MT7621DAT

- [MediaTek MT7621产品页](https://www.mediatek.com/products/home-networking/mt7621)
- [Oolite V8.1 MT7621DAT规格书](https://file1.elecfans.com/web3/M00/00/3F/wKgZPGdH1J-AAHXWAA3S9eJmUtA353.pdf)
- [Oolite MT7621 OpenWrt源码](https://github.com/GainStrongService/openwrt/tree/2102/mt7621-oolite-8)
- [Oolite V8.1产品介绍](https://www.embeddedrouter.com/info/openwrt-compatible-mt7621dat-module-oolite-103448038.html)
- [MT7621A开源硬件参考](https://github.com/cyijun/MT7621A-Router-Design)
- [MT7621开源硬件项目](https://github.com/Richard-Tung/mt7621_integrated_router)
- [AP-MT7621DA+MT7603E+MT7613B资料说明页](https://gitcode.com/open-source-toolkit/06f5a)

### Cadence转换

- [Cadence官方PADS到Allegro转换说明](https://community.cadence.com/cadence_blogs_8/b/pcb/posts/customer-support-recommended-working-with-pads-to-allegro-pcb-editor-translator)

