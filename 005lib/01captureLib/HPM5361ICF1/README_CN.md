# HPM5361ICF1 = 先楫 HPM5300 LQFP64

按 `5361IEG1` / `ast2400lib` 同款流程生成，目标 **Cadence 17.2**。

| 项目 | 值 |

|------|----|

| 型号 | HPM5361ICF1 |

| 封装 | **LQFP-64 10×10 mm，P0.5 mm** |

| 引脚 | **64**（无 EP） |

| PCB Footprint | `LQFP64_10X10_P0D5` |

| 符号 | **单页**；引脚在左，完整外设复用名在右 |

| 焊盘 | `r155_30` 1.55×0.30、`r30_155` 0.30×1.55 |

引脚来源：先楫官方 KiCad `HPM5300_Library.kicad_sym`（HPM5361ICF1）。

焊盘来源：官方 `LQFP-64_10x10mm_P0.5mm.kicad_mod`。

坐标系：数据手册顶视，**1 脚左上，逆时针**。

## Capture 导入

1. OrCAD Capture CIS 17.2 → `File` → `Import` → `Library XML`

2. 选择 `OrcadCaptureXML\2026-08-15_23-35-55.xml`

3. 另存为 `01captureLib\HPM5361ICF1.OLB`

4. 放置 `HPM5361ICF1`（单页，全部 64 脚，不分立）

## Allegro 封装生成

双击：

`AUTOlib\ul_HPM5361ICF1\AllegroV17_2\LQFP64_10X10_P0D5.bat`

会调用 `padstack_editor -x` 生成 `.pad`，再 `allegro -nograph -s` 生成 `.dra/.psm`，并复制到 `01Pad_lib` / `01Psm_lib`。

## 电源注意（ICF1）

- `DCDC_IN`(21) / `DCDC_LP`(20) / `DCDC_GND`(19) / `VPMC`(22) **各自独立**（与 IEG1 的 VPMC=DCDC_IN 内部共用不同）

- `DCDC_LP` 若软件关 DCDC：**悬空，禁止接地**

- 多个 `VSS` / `VDD_SOC` / `VIO_B00` 同名 Power，Capture 会自动短接

- `PA00` = ISP_UART_TX，`PA01` = ISP_UART_RX

- `PA02` = BOOT0，`PA03` = BOOT1

- `PA24` = USB_DP，`PA25` = USB_DM

