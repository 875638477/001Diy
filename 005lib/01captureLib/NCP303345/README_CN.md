# NCP303345 OrCAD / Allegro 库

按 `ast2400lib` 的目录和生成方式制作，目标为 Cadence 17.2。

- 完整料号：`NCP303345MNTWG`
- 原理图符号：单页，28 个物理引脚
- PCB 封装：`PQFN24_4X5_P0D5_483BV`
- 封装：PQFN24 4.00×5.00×0.75 mm，0.50 mm pitch，CASE 483BV
- 数据来源：`NCP303345-D.PDF` 第 3 页和第 22 页（98AON13704G）

## Capture 导入

在 OrCAD Capture CIS 17.2 中选择 `File -> Import -> Library XML`，导入：

`OrcadCaptureXML\2026-09-07_16-28-33.xml`

然后另存为 `NCP303345.OLB`。

## Allegro 封装生成

双击 `AllegroV17_2\PQFN24_4X5_P0D5_483BV.bat`。脚本生成 `.pad/.dra/.psm`，并复制到
`01Pad_lib` 和 `01Psm_lib`。

## 重要复核

- Pin 28 已使用独立 Allegro Shape Symbol 实现规格书中的台阶异形焊盘。
- 外围焊盘、Pin 25/26/27 的位置和尺寸已按推荐 mounting footprint 录入。
- 大裸露焊盘膏层按线性 80% 缩放；实际钢网开窗必须由贴片厂复核。
- PGND 裸露焊盘应布置多颗散热过孔，且不要使用 thermal relief。
