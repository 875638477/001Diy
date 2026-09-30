# AST2400 = EVB reference U1A/U1B/U1C/U1D

Source: AST2400芯片的官方参考设计.pdf (AST2400 EVB DDR3)

| Section | Content | Pins |
|---------|---------|-----:|
| U1A | PCIE + DDR + LPC + I2C + SD | 108 |
| U1B | Flash + UART + MAC + SPI | 120 |
| U1C | VGA/USB/ADC/PWM/Misc | 88 |
| U1D | Power/GND | 92 |

Pin names follow the reference. Duplicates uniquified: GND1, GND2, IV12D1...
PCB footprint: LFBGA408_19X19. Refdes prefix U (可放成 U2).

## Import

1. Capture File -> Import -> Library XML
2. Select: `OrcadCaptureXML\2026-07-15_15-40-52.xml`
3. Save as `01captureLib\AST2400.OLB`
4. Place AST2400 -> only U?A / U?B / U?C / U?D
