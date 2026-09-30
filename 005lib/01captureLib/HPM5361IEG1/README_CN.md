# HPM5361IEG1 = 先楫 HPM5300 QFN48_EP

按 `ast2400lib` / TMC6460 同款流程生成，目标 **Cadence 17.2**。

| 项目 | 值 |
|------|----|
| 型号 | HPM5361IEG1 |
| 封装 | **QFN48_EP 6×6 mm，P0.4 mm，EP 4.2×4.2 mm** |
| 引脚 | 48 + EP(49) = 49 |
| PCB Footprint | `QFN48_6X6_P0D4` |
| 符号 | 单页；引脚在左，完整外设复用名在右 |
| 焊盘 | `r85_20` 0.85×0.20、`r20_85` 0.20×0.85、`r420` 4.20×4.20 |

引脚来源：先楫官方 KiCad `HPM5300_Library.kicad_sym`（HPM5361IEG1）。  
焊盘来源：官方 `QFN-48_6x6mm_P0.4mm_EP4.2x4.2mm.kicad_mod`。  
坐标系：数据手册顶视，**1 脚左上，逆时针**。

## Capture 导入

1. OrCAD Capture CIS 17.2 → `File` → `Import` → `Library XML`
2. 选择 `OrcadCaptureXML\2026-08-14_18-55-35.xml`
3. 另存为 `01captureLib\HPM5361IEG1.OLB`
4. 放置 `HPM5361IEG1`（单页，全部引脚）

## Allegro 封装生成

双击：

`AUTOlib\ul_HPM5361IEG1\AllegroV17_2\QFN48_6X6_P0D4.bat`

会调用 `padstack_editor -x` 生成 `.pad`，再 `allegro -nograph -s` 生成 `.dra/.psm`，并复制到 `01Pad_lib` / `01Psm_lib`。

## 电源注意（IEG1）

- `VPMC` 与 `DCDC_IN` **内部共用**，接 3.3 V
- `DCDC_LP` 若软件关闭 DCDC：**悬空，禁止接地**
- `VSS`(49) 是散热焊盘，必须焊到 GND
- 多个 `VDD_SOC` / `VIO_B00` 同名 Power，Capture 会自动短接

## 量产前复核

- EP 钢网建议按官方 3×3 开窗（本库 EP 膏铜约 80%）
- 对照 HPM5300 数据手册封装图确认 1 脚方向
