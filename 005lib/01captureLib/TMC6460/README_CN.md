# TMC6460 库说明

与 AST2400 相同流程：Capture 符号 XML + Allegro TQFN38 封装。

| 项目 | 路径/值 |
|------|---------|
| Capture XML | `01captureLib\TMC6460\OrcadCaptureXML\` 最新 `.xml` |
| 引脚清单 | `01captureLib\TMC6460\TMC6460_pin_checklist.txt` |
| 引脚 CSV | `01captureLib\TMC6460\TMC6460_pins.csv` |
| 封装名 | `TQFN38_5X7` |
| 封装源 | `AUTOlib\ul_TMC6460\AllegroV17_2\` |
| Pad | `01Pad_lib\r25_70.pad` / `r315_515.pad` |
| Psm | `01Psm_lib\TQFN38_5X7.dra/.psm` |

## 导入 Capture
1. File -> Import -> Library XML
2. 选最新 `OrcadCaptureXML\*.xml`
3. 另存为 `01captureLib\TMC6460.OLB`

## 注意
- 封装是 **TQFN38 5x7**（datasheet），原理图标 TQFN-56L 有误
- 管脚名按 datasheet：CSN/SLEEPN/FAULTN；原理图 CS/SLEEP/FAULT 为同脚
- VS1/2/3、PGND1/2/3 为同名电源脚拆分；EP=散热焊盘接 GND
