# AST2400 OrCAD Capture Schematic Library (Plan B)

## Source
- Datasheet: `ast2400v13.pdf` (ASPEED AST2400/AST1250 A1 Datasheet V1.3)
- Package: **408-ball 19mm x 19mm LFBGA**
- CSV: `AST2400_pins.csv`

## Stats
- Unique balls parsed: **408** (target 408)
- Unknown names: **0**
- Part sections: **8**

| PartSection | Pins | Power |
|---|---:|---:|
| A_POWER | 76 | 76 |
| B_DDR | 50 | 0 |
| C_PCIE_VGA | 24 | 5 |
| D_MAC | 29 | 0 |
| E_FLASH_SPI | 59 | 0 |
| F_UART_I2C_JTAG | 78 | 0 |
| G_USB_ADC_MISC | 44 | 5 |
| H_GPIO_SD_PWM | 48 | 0 |

## Capture steps (semi-auto)

1. OrCAD Capture CIS 17.2 -> File -> New -> Library  
   save as `D:\001DIY\005lib\01captureLib\AST2400.OLB`
2. New Part `AST2400`, create **8 heterogeneous sections**:
   A_POWER / B_DDR / C_PCIE_VGA / D_MAC / E_FLASH_SPI /
   F_UART_I2C_JTAG / G_USB_ADC_MISC / H_GPIO_SD_PWM
3. Open `AST2400_pins.csv` in Excel, filter by `PartSection`,
   add pins with PinNumber=Ball, PinName, Electrical.
4. Part properties:
   - Value = AST2400
   - PCB Footprint = AST2400_LFBGA408 (create later in 01Psm_lib)
   - Manufacturer = ASPEED
5. Multi-function balls use datasheet primary name (not GPIO).

## Notes
- Power pins Electrical = Power (same name shorts in Capture).
- GND / *AVSS / PLLVSS = Power; name nets consistently on schematic.
- Keep NC pins on symbol and leave floating on board.
- If count != 408, cross-check Ball Map in datasheet.
