# 地平线旭日 X3 / X5：PCIe 记录

记录日期：2026-10-08

结论：旭日 X3（Sunrise 3）和旭日 X5（Sunrise 5）芯片都没有 PCIe 接口。高速外设走 USB，不能按 PCIe 控制器来做板级设计。

## 旭日 X3

官方《X3 与 J3 差异描述》里，X3M、X3E 的外设清单是：

- USB 3.0
- 4× UART
- 3× SPI
- 2× I2S
- 6× I2C
- 9× PWM
- 1× QSPI
- 3× SDIO
- RTC / Timer / Watchdog
- 1 路千兆以太网

主机侧高速接口是 BIF-SPI（66 MHz）、BIF-SD（192 MB/s）和 USB 3.0。清单中没有 PCIe。

同代表对照里的征程 J3 外设列表与 X3M 相同，同样没有 PCIe。

封装：台积电 16 nm，FCBGA483，0.65 mm 间距，15 mm × 15 mm。X3M 为 4× Cortex-A53 @ 1.2 GHz、5 TOPS；X3E 为 2× Cortex-A53、3 TOPS。

RDK X3 开发板引出的是网口、USB 2.0/3.0、MIPI CSI、MIPI DSI、HDMI、TF 卡和 40PIN（UART / SPI / I2C / I2S / GPIO），没有 PCIe 插座。

RDK X3 模组外形兼容树莓派 CM4，但 CM4 的 PCIe 引脚被改成 USB 3.0 差分对，不能当 PCIe 用：

| CM4 引脚 | CM4 信号 | RDK X3 模组 |
| --- | --- | --- |
| 102 | PCIe_CLK_nREQ | 未使用 |
| 109 | PCIe_nRST | 未使用 |
| 110 | PCIe_CLK_P | 未使用 |
| 112 | PCIe_CLK_N | 未使用 |
| 116 | PCIe_RX_P | USB_RX_P |
| 118 | PCIe_RX_N | USB_RX_N |
| 122 | PCIe_TX_P | USB_TX_P |
| 124 | PCIe_TX_N | USB_TX_N |

载板上若有按 CM4 定义的 PCIe 插槽，不要插入 PCIe 设备。

来源：

- https://developer.d-robotics.cc/api/v1/fileData/horizon_xj3_open_explorer_cn_doc/oe_mapper/source/appendix/xj3_introduction/processor_contrast.html
- RDK X3 1.0 Product Brief：https://archive.d-robotics.cc/downloads/hardware/rdk_x3/RDK_X3_1.0_Product_Brief.pdf

## 旭日 X5

《X5 芯片用户手册 2.0.0》概述中的外围接口是：

- 1× USB 3.0（Dual-Role Device）
- 1× USB 2.0（Dual-Role Device）
- 1× 1G Ethernet MAC
- 2× SDIO
- 1× QSPI
- 7× SPI
- 8× I2C
- 8× UART
- 8× PWM
- 8× LPWM
- 8× ADC
- 129× GPIO
- Timer / Watchdog / Mailbox

清单中没有 PCIe。芯片只有 1 路 USB 3.0。

其他规格：8× Cortex-A55 @ 1.5 GHz，贝叶斯架构 BPU 最高 10 TOPS @ 1.0 GHz，x32 LPDDR4/LPDDR4X、最大 8 GB。封装为台积电 12 nm FCCSP563，0.65 mm 间距，16 mm × 16 mm。

RDK X5 开发板的 4 路 USB 3.0 Type-A 是用 GL3510 USB Hub 从这一路 USB 3.0 扩出来的，板载接口是 HDMI、千兆以太网（可 PoE）、USB 2.0、MIPI CSI、MIPI DSI、CAN FD、TF 卡和 40PIN。没有 PCIe 插座。X5 EVB 同样只引出 1 路 USB 3.0 Type-A 和 1 路 Micro USB 2.0。

来源：

- https://developer.d-robotics.cc/x5_sdk_doc_v2.0.0/preface/overview.html
- https://developer.d-robotics.cc/x5_sdk_doc_v2.0.0/quick_start/x5_md_user_guide.html
- https://developer.d-robotics.cc/x5_sdk_doc_v2.0.0/quick_start/x5_evb_v2p0_user_guide.html

## 同厂带 PCIe 的型号

需要片上 PCIe 时，旭日 X3 / X5 不满足。征程 5 官方规格为 1 路 PCIe Gen3、2 Lane。RDK Ultra 开发板引出 3 路 PCIe 3.0（1× M.2-E 无线网卡、2× M.2-M SSD），那是 Ultra 平台，不是 X5。
