# -*- coding: utf-8 -*-
"""HPM5361IEG1: OrCAD Capture symbol + Allegro QFN48 6x6 footprint (AST2400-style flow).

Sources:
  - Official: HPM5300 series, HPM5361IEG1 = QFN48_EP 6x6 mm P0.4
  - Pinout: AUTOlib/HPM_LIB_20251229/HPM_symbols/HPM5300_Library.kicad_sym
  - Land: HPM_footprints.pretty/QFN-48_6x6mm_P0.4mm_EP4.2x4.2mm.kicad_mod
  - Process: 01AIcadence/ast2400_lib + tmc6460_lib
"""
from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(r"D:\001DIY\005lib")
PART = "HPM5361IEG1"
FP_NAME = "QFN48_6X6_P0D4"
PAD_H = "r85_20"     # 0.85 x 0.20 mm, left/right
PAD_V = "r20_85"     # 0.20 x 0.85 mm, top/bottom
PAD_EP = "r420"      # 4.20 x 4.20 mm exposed pad

STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ALLEGRO_BIN = Path(r"C:\Program0\Cadence\spb172\tools\bin")
PAD_LIB = ROOT / "01Pad_lib"
PSM_LIB = ROOT / "01Psm_lib"

OUT = ROOT / "AUTOlib" / "ul_HPM5361IEG1"
ARCHIVE = ROOT / "AUTOlib" / "5361IEG1"
CAPTURE_OUT = ROOT / "01captureLib" / "HPM5361IEG1"
SCRIPT_DIR = ROOT / "01script_file" / "HPM5361IEG1"
AI_DIR = ROOT / "01AIcadence" / "hpm5361ieg1_lib"

ELEC_CODE = {
    "Input": 0, "Bidirectional": 1, "Output": 2,
    "Passive": 4, "NC": 4, "Power": 7,
}

# Primary names for Capture. Full pinmux kept in Pinmux column.
PINS: list[dict] = [
    {"PinNumber": "1",  "PinName": "PA04",        "Electrical": "Bidirectional", "Pinmux": "PA04/URT1.CTS/SPI0.CS0/CAN1.RXD/PWM0.P0/PWM1.P4/TRGM0.P04/RDC0.EXC_P/QEI1.A/QEO1.A/SEI1.DE/JTAG.TDO"},
    {"PinNumber": "2",  "PinName": "PA08",        "Electrical": "Bidirectional", "Pinmux": "PA08/TMR0.COMP1/URT2.TXD/I2C2.SCL/SPI3.CS2/CAN2.TXD/PWM0.P4/PWM0.FAULT0/JTAG.TRST"},
    {"PinNumber": "3",  "PinName": "PA09",        "Electrical": "Bidirectional", "Pinmux": "PA09/TMR0.CAPT1/URT2.RXD/I2C2.SDA/SPI3.CS1/CAN2.RXD/PWM0.P5/PWM0.FAULT1"},
    {"PinNumber": "4",  "PinName": "PA10",        "Electrical": "Bidirectional", "Pinmux": "PA10/TMR0.COMP2/URT2.DE/URT2.RTS/SPI3.CS0/CAN2.STBY/PWM0.P6/PWM1.FAULT0/ACMP.COMP0/QEI1.A/QEO0.A/SEI1.DE"},
    {"PinNumber": "5",  "PinName": "VDD_SOC",     "Electrical": "Power",         "Pinmux": "VDD_SOC"},
    {"PinNumber": "6",  "PinName": "VIO_B00",     "Electrical": "Power",         "Pinmux": "VIO_B00"},
    {"PinNumber": "7",  "PinName": "PA03",        "Electrical": "Bidirectional", "Pinmux": "PA03/TMR1.CAPT1/URT0.CTS/I2C0.SDA/SPI3.CS3/CAN1.STBY/ACMP.COMP1/PWM1.P3/TRGM0.P03/PWM1.FAULT1/QEI1.H1/ADC0.DBG"},
    {"PinNumber": "8",  "PinName": "PA02",        "Electrical": "Bidirectional", "Pinmux": "PA02/TMR1.COMP1/URT0.DE/URT0.RTS/I2C0.SCL/CAN0.STBY/ACMP.COMP0/PWM1.P2/TRGM0.P02/ACMP.COMP1/QEI1.F/ADC1.DBG"},
    {"PinNumber": "9",  "PinName": "VDD_SOC",     "Electrical": "Power",         "Pinmux": "VDD_SOC"},
    {"PinNumber": "10", "PinName": "VDD_OTPCAP",  "Electrical": "Power",         "Pinmux": "VDD_OTPCAP"},
    {"PinNumber": "11", "PinName": "PA01",        "Electrical": "Bidirectional", "Pinmux": "PA01/TMR1.CAPT0/URT0.RXD/CAN0.RXD/PWM0.FAULT1/PWM1.P1/TRGM0.P01/ACMP.COMP0  ISP_UART_RX"},
    {"PinNumber": "12", "PinName": "PA00",        "Electrical": "Bidirectional", "Pinmux": "PA00/TMR1.COMP0/URT0.TXD/CAN0.TXD/PWM0.FAULT0/PWM1.P0/TRGM0.P00/PWM1.FAULT0  ISP_UART_TX"},
    {"PinNumber": "13", "PinName": "RESETN",      "Electrical": "Input",         "Pinmux": "RESETN"},
    {"PinNumber": "14", "PinName": "WAKEUP",      "Electrical": "Input",         "Pinmux": "WAKEUP"},
    {"PinNumber": "15", "PinName": "DCDC_LP",     "Electrical": "Power",         "Pinmux": "DCDC_LP  IEG1: float if DCDC disabled; do not GND"},
    {"PinNumber": "16", "PinName": "VPMC",        "Electrical": "Power",         "Pinmux": "VPMC  IEG1: shared with DCDC_IN internally, tie 3.3V"},
    {"PinNumber": "17", "PinName": "VDD_PMCCAP",  "Electrical": "Power",         "Pinmux": "VDD_PMCCAP"},
    {"PinNumber": "18", "PinName": "PY01",        "Electrical": "Bidirectional", "Pinmux": "PY01/TMR3.CAPT0/URT0.RXD/CAN2.RXD/PWM0.P1/PWM1.P5/PWM0.FAULT1/WDG0.RST/USB0.OC/PMIC_PY01/PURT.RXD/PTMR.COMP1/SOC.GPIO_Y01"},
    {"PinNumber": "19", "PinName": "PY00",        "Electrical": "Bidirectional", "Pinmux": "PY00/TMR3.COMP0/URT0.TXD/CAN2.TXD/PWM0.P0/PWM1.P4/PWM0.FAULT0/USB0.ID/PMIC_PY00/PURT.TXD/PTMR.COMP0/SOC.GPIO_Y00"},
    {"PinNumber": "20", "PinName": "PB15",        "Electrical": "Bidirectional", "Pinmux": "PB15/TMR0.COMP3/URT3.TXD/SPI2.DAT3/CAN3.TXD/PWM0.FAULT1/PWM1.P3/TRGM0.P03/RDC0.EXC_N/QEI0.H0/SEI0.RX/ADC0.IN7/ADC1.IN7/CMP0.INP1/CMP1.INP1/OPA1.INN1"},
    {"PinNumber": "21", "PinName": "PB14",        "Electrical": "Bidirectional", "Pinmux": "PB14/URT3.RXD/SPI2.DAT2/CAN3.RXD/PWM0.FAULT0/PWM1.P2/TRGM0.P02/RDC0.EXC_P/QEI0.Z/QEO1.Z/SEI0.TX/ADC0.IN6/ADC1.IN6/CMP0.INN1/CMP1.INN1/OPA1.INP1"},
    {"PinNumber": "22", "PinName": "PB13",        "Electrical": "Bidirectional", "Pinmux": "PB13/TMR1.COMP3/URT3.DE/URT3.RTS/I2C3.SCL/SPI2.MOSI/CAN3.STBY/PWM1.FAULT1/PWM1.P1/TRGM0.P01/QEI0.B/QEO1.B/SEI0.CK/ADC0.IN5/ADC1.IN5/CMP0.INP2/CMP1.INP2/OPA1.INN0"},
    {"PinNumber": "23", "PinName": "PB12",        "Electrical": "Bidirectional", "Pinmux": "PB12/URT3.CTS/I2C3.SDA/SPI2.MISO/PWM1.FAULT0/PWM1.P0/TRGM0.P00/QEI0.A/QEO1.A/SEI0.DE/ADC0.IN4/ADC1.IN4/CMP0.INN2/CMP1.INN2/OPA1.INP0"},
    {"PinNumber": "24", "PinName": "PB11",        "Electrical": "Bidirectional", "Pinmux": "PB11/URT2.CTS/SPI2.SCLK/ACMP.COMP1/PWM1.P7/QEI0.F/SEI1.RX/ADC0.IN3/ADC1.IN3/CMP0.INN4/CMP1.INN4/OPA0.INN3/OPA1.INN3"},
    {"PinNumber": "25", "PinName": "PB10",        "Electrical": "Bidirectional", "Pinmux": "PB10/TMR0.COMP2/URT2.DE/URT2.RTS/SPI2.CS0/CAN2.STBY/ACMP.COMP0/PWM1.P6/QEI0.H1/QEO1.Z/SEI1.TX/USB0.PWR/ADC0.IN2/ADC1.IN2/CMP0.INP4/CMP1.INP4/OPA0.INP3/OPA1.INP3"},
    {"PinNumber": "26", "PinName": "PB09",        "Electrical": "Bidirectional", "Pinmux": "PB09/TMR0.CAPT1/URT2.RXD/I2C2.SDA/SPI2.CS1/CAN2.RXD/ACMP.COMP1/PWM1.P5/QEI1.F/QEO1.B/SEI1.CK/USB0.OC/ADC0.IN1/ADC1.IN1/DAC1.OUT/CMP0.INP6/CMP1.INP6/OPA0.INN2/OPA1.INN2"},
    {"PinNumber": "27", "PinName": "PB08",        "Electrical": "Bidirectional", "Pinmux": "PB08/TMR0.COMP1/URT2.TXD/I2C2.SCL/SPI2.CS2/CAN2.TXD/ACMP.COMP0/PWM1.P4/QEI1.H1/QEO1.A/SEI1.DE/USB0.ID/ADC0.IN11/ADC1.IN11/DAC0.OUT/CMP0.INN6/CMP1.INN6/OPA0.INP2/OPA1.INP2"},
    {"PinNumber": "28", "PinName": "VDD_SOC",     "Electrical": "Power",         "Pinmux": "VDD_SOC"},
    {"PinNumber": "29", "PinName": "VIO_B01",     "Electrical": "Power",         "Pinmux": "VIO_B01"},
    {"PinNumber": "30", "PinName": "VREFL",       "Electrical": "Power",         "Pinmux": "VREFL"},
    {"PinNumber": "31", "PinName": "VREFH",       "Electrical": "Power",         "Pinmux": "VREFH"},
    {"PinNumber": "32", "PinName": "VANA",        "Electrical": "Power",         "Pinmux": "VANA"},
    {"PinNumber": "33", "PinName": "VDD_SOC",     "Electrical": "Power",         "Pinmux": "VDD_SOC"},
    {"PinNumber": "34", "PinName": "VIO_B00",     "Electrical": "Power",         "Pinmux": "VIO_B00"},
    {"PinNumber": "35", "PinName": "XTALI",       "Electrical": "Input",         "Pinmux": "XTALI"},
    {"PinNumber": "36", "PinName": "XTALO",       "Electrical": "Output",        "Pinmux": "XTALO"},
    {"PinNumber": "37", "PinName": "PA31",        "Electrical": "Bidirectional", "Pinmux": "PA31/TMR2.COMP3/URT7.TXD/SPI1.DAT3/CAN3.TXD/XPI0.CA_CS0/PWM0.P7/PWM1.P7/TRGM0.P07/QEI0.F/USB0.ID"},
    {"PinNumber": "38", "PinName": "PA30",        "Electrical": "Bidirectional", "Pinmux": "PA30/URT7.RXD/SPI1.DAT2/CAN3.RXD/XPI0.CA_D1/PWM0.P6/PWM1.P6/TRGM0.P06/QEI0.H1/USB0.PWR"},
    {"PinNumber": "39", "PinName": "PA29",        "Electrical": "Bidirectional", "Pinmux": "PA29/TMR3.COMP3/URT7.DE/URT7.RTS/I2C3.SCL/SPI1.MOSI/CAN3.STBY/XPI0.CA_D2/PWM0.P5/PWM1.P5/TRGM0.P05/RDC0.EXC_N/QEI0.H0/SEI0.RX/USB0.OC"},
    {"PinNumber": "40", "PinName": "PA28",        "Electrical": "Bidirectional", "Pinmux": "PA28/URT7.CTS/I2C3.SDA/SPI1.MISO/XPI0.CA_D0/PWM0.P4/PWM1.P4/TRGM0.P04/RDC0.EXC_P/QEI0.Z/QEO0.Z/SEI0.TX"},
    {"PinNumber": "41", "PinName": "PA27",        "Electrical": "Bidirectional", "Pinmux": "PA27/URT6.CTS/SPI1.SCLK/XPI0.CA_SCLK/PWM0.P3/PWM1.P3/TRGM0.P03/QEI0.B/QEO0.B/SEI0.CK"},
    {"PinNumber": "42", "PinName": "PA26",        "Electrical": "Bidirectional", "Pinmux": "PA26/TMR2.COMP2/URT6.DE/URT6.RTS/SPI1.CS0/CAN2.STBY/XPI0.CA_D3/PWM0.P2/PWM1.P2/TRGM0.P02/QEI0.A/QEO0.A/SEI0.DE"},
    {"PinNumber": "43", "PinName": "PA25",        "Electrical": "Bidirectional", "Pinmux": "PA25/TMR2.CAPT1/URT6.RXD/I2C2.SDA/SPI1.CS1/CAN2.RXD/XPI0.CA_DQS/PWM0.P1/PWM1.P1/TRGM0.P01/QEI0.F  USB_DM"},
    {"PinNumber": "44", "PinName": "PA24",        "Electrical": "Bidirectional", "Pinmux": "PA24/TMR2.COMP1/URT6.TXD/I2C2.SCL/SPI1.CS2/CAN2.TXD/XPI0.CA_CS1/PWM0.P0/PWM1.P0/TRGM0.P00/QEI0.H1  USB_DP"},
    {"PinNumber": "45", "PinName": "VDD_SOC",     "Electrical": "Power",         "Pinmux": "VDD_SOC"},
    {"PinNumber": "46", "PinName": "PA07",        "Electrical": "Bidirectional", "Pinmux": "PA07/TMR0.COMP0/URT1.TXD/I2C1.SCL/SPI0.MOSI/PWM0.P3/PWM1.P7/TRGM0.P07/QEI1.H0/SEI1.RX/JTAG.TMS"},
    {"PinNumber": "47", "PinName": "PA06",        "Electrical": "Bidirectional", "Pinmux": "PA06/TMR0.CAPT0/URT1.RXD/I2C1.SDA/SPI0.MISO/PWM0.P2/PWM1.P6/TRGM0.P06/QEI1.Z/QEO1.Z/SEI1.TX/JTAG.TCK"},
    {"PinNumber": "48", "PinName": "PA05",        "Electrical": "Bidirectional", "Pinmux": "PA05/TMR1.COMP2/URT1.DE/URT1.RTS/SPI0.SCLK/CAN1.TXD/PWM0.P1/PWM1.P5/TRGM0.P05/RDC0.EXC_N/QEI1.B/QEO1.B/SEI1.CK/JTAG.TDI"},
    {"PinNumber": "49", "PinName": "VSS",         "Electrical": "Power",         "Pinmux": "VSS  EP / thermal pad, must solder to GND"},
]

# Heterogeneous sections A..D, L/R top->bottom. Matches official HPM KiCad units.
SECTIONS = {
    "A": {
        "title": "POWER",
        "layout": [
            ("DCDC", ["15"], ["5", "9", "28", "33", "45"]),
            ("Analog", ["32"], ["31", "30"]),
            ("EP / GND", ["49"], []),
        ],
    },
    "B": {
        "title": "SYS",
        "layout": [
            ("Reset / Wake", ["13", "14"], []),
            ("XTAL 24M", ["35"], ["36"]),
        ],
    },
    "C": {
        "title": "PMIC",
        "layout": [
            ("LDO / PMC", ["16"], ["10", "17"]),
            ("PY / PMIC GPIO", ["19", "18"], []),
        ],
    },
    "D": {
        "title": "GPIO",
        "layout": [
            ("PA00-PA10", ["12", "11", "8", "7", "1", "48"], ["47", "46", "2", "3", "4"]),
            ("PA24-PA31 USB/XPI", ["44", "43", "42", "41"], ["40", "39", "38", "37"]),
            ("PB08-PB15 ADC", ["27", "26", "25", "24"], ["23", "22", "21", "20"]),
            ("VIO", ["6", "34"], ["29"]),
        ],
    },
}


def mm_to_mil(mm: float) -> float:
    return mm / 0.0254


def pin_xml(name: str, position: int, elec: str, left: bool, y: int, body_w: int) -> str:
    typ = ELEC_CODE.get(elec, 4)
    pin_len = 30
    if left:
        start_x, hotpt_x = 0, -pin_len
    else:
        start_x, hotpt_x = body_w, body_w + pin_len
    return f"""        <SymbolPinScalar>
          <Defn hotptX="{hotpt_x}" hotptY="{y}" name="{escape(name)}" position="{position}" startX="{start_x}" startY="{y}" type="{typ}" visible="1"/>
          <IsLong><Defn val="1"/></IsLong>
          <IsClock><Defn val="0"/></IsClock>
          <IsDot><Defn val="0"/></IsDot>
          <IsLeftPointing><Defn val="0"/></IsLeftPointing>
          <IsRightPointing><Defn val="0"/></IsRightPointing>
          <IsNetStyle><Defn val="0"/></IsNetStyle>
          <IsNoConnect><Defn val="0"/></IsNoConnect>
          <IsGlobal><Defn val="0"/></IsGlobal>
          <IsNumberVisible><Defn val="1"/></IsNumberVisible>
        </SymbolPinScalar>
"""


def line_xml(x1: int, y1: int, x2: int, y2: int) -> str:
    return f"""        <Line>
          <Defn lineStyle="0" lineWidth="1" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}"/>
        </Line>
"""


def comment_xml(name: str, cx: int, cy: int) -> str:
    w = max(50, len(name) * 6)
    h = 12
    x1, y1 = cx - w // 2, cy - h // 2
    x2, y2 = cx + w // 2, cy + h // 2
    return f"""        <CommentText>
          <Defn locX="{cx}" locY="{cy}" name="{escape(name)}" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}"/>
          <TextFont>
            <Defn escapement="0" height="-11" italic="0" name="Arial" orientation="0" weight="700" width="5"/>
          </TextFont>
        </CommentText>
"""


def make_libpart(letter: str, title: str, by_num: dict[str, dict]) -> str:
    GRID = 10
    body_w = 280
    y = 20
    gap = 20
    pin_pitch = 10
    graphics: list[str] = []
    pin_blocks: list[str] = []
    maps: list[tuple[str, int]] = []
    pos = 0
    layout = SECTIONS[letter]["layout"]

    for gi, (label, left_nums, right_nums) in enumerate(layout):
        left = [by_num[n] for n in left_nums]
        right = [by_num[n] for n in right_nums]
        rows = max(len(left), len(right), 1)
        y_top = y
        y_mid = y_top + (rows * pin_pitch) // 2
        y_mid -= y_mid % GRID
        graphics.append(comment_xml(label, body_w // 2, y_mid))
        for i, p in enumerate(left):
            yy = y_top + i * pin_pitch
            pin_blocks.append(pin_xml(p["PinName"], pos, p["Electrical"], True, yy, body_w))
            maps.append((p["PinNumber"], pos))
            pos += 1
        for i, p in enumerate(right):
            yy = y_top + i * pin_pitch
            pin_blocks.append(pin_xml(p["PinName"], pos, p["Electrical"], False, yy, body_w))
            maps.append((p["PinNumber"], pos))
            pos += 1
        y = y_top + rows * pin_pitch + gap
        if gi < len(layout) - 1:
            ly = y - gap // 2
            graphics.append(line_xml(8, ly, body_w - 8, ly))

    bbox_y2 = y
    pinnums = "".join(
        f'        <PinNumber><Defn number="{escape(n)}" position="{p}"/></PinNumber>\n'
        for n, p in maps
    )
    return f"""    <LibPart>
      <Defn/>
      <NormalView>
        <Defn suffix="{letter}.Normal"/>
        <SymbolDisplayProp>
          <Defn locX="{body_w // 2}" locY="-30" name="Part Reference" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolDisplayProp>
          <Defn locX="{body_w // 2}" locY="-20" name="Value" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolUserProp><Defn name="Description" val="HPMicro HPM5361IEG1 QFN48_EP ({title})"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="{PART}"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="HPMicro"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Package" val="QFN48_EP 6x6mm P0.4 EP4.2"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Section" val="{title}"/></SymbolUserProp>
        <SymbolColor><Defn val="48"/></SymbolColor>
        <SymbolBBox><Defn x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></SymbolBBox>
        <IsPinNumbersVisible><Defn val="1"/></IsPinNumbersVisible>
        <IsPinNamesRotated><Defn val="1"/></IsPinNamesRotated>
        <IsPinNamesVisible><Defn val="1"/></IsPinNamesVisible>
        <ContentsLibName><Defn name=""/></ContentsLibName>
        <ContentsViewName><Defn name="{PART}"/></ContentsViewName>
        <ContentsViewType><Defn type="0"/></ContentsViewType>
        <PartValue><Defn name="{PART}"/></PartValue>
        <Reference><Defn name="U"/></Reference>
        <Rect><Defn fillStyle="1" hatchStyle="0" lineStyle="0" lineWidth="3" x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></Rect>
{"".join(graphics)}{"".join(pin_blocks)}      </NormalView>
      <PhysicalPart>
        <Defn/>
{pinnums}      </PhysicalPart>
    </LibPart>
"""


def write_capture_xml(by_num: dict[str, dict], path: Path) -> None:
    parts = []
    for letter in "ABCD":
        parts.append(make_libpart(letter, SECTIONS[letter]["title"], by_num))
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Lib xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="olb.xsd">
  <Defn name="{PART}.OLB"/>
  <Package>
    <Defn alphabeticNumbering="1" isHomogeneous="0" name="{PART}" pcbFootprint="{FP_NAME}" pcbLib="" refdesPrefix="U"/>
{"".join(parts)}  </Package>
</Lib>
"""
    path.write_text(xml, encoding="utf-8", newline="\n")


def qfn_pin_xy_mm(num: int) -> tuple[float, float, str]:
    """Datasheet top view, pin1 top-left, CCW. Y+ up."""
    if 1 <= num <= 12:
        return -2.95, 2.2 - (num - 1) * 0.4, PAD_H
    if 13 <= num <= 24:
        return -2.2 + (num - 13) * 0.4, -2.95, PAD_V
    if 25 <= num <= 36:
        return 2.95, -2.2 + (num - 25) * 0.4, PAD_H
    if 37 <= num <= 48:
        return 2.2 - (num - 37) * 0.4, 2.95, PAD_V
    if num == 49:
        return 0.0, 0.0, PAD_EP
    raise ValueError(num)


def write_pxml(path: Path, name: str, w_mm: float, h_mm: float, mask_scale: float = 1.15, paste_scale: float = 1.0) -> None:
    w = mm_to_mil(w_mm)
    h = mm_to_mil(h_mm)
    mw, mh = w * mask_scale, h * mask_scale
    pw, ph = w * paste_scale, h * paste_scale
    text = f"""<?xml version="1.0" encoding="iso-8859-1" ?>
<!DOCTYPE padstack>
<padstack version="1.0">
  <padstackname>{name}</padstackname>
  <padstackusage>SMD_PIN</padstackusage>
  <units>MILS</units>
  <accuracy>2</accuracy>
  <pad>
    <layer>BEGIN_LAYER</layer>
    <type>REGULAR_PAD</type>
    <figure>RECTANGLE</figure>
    <width>{w:.2f}</width>
    <height>{h:.2f}</height>
  </pad>
  <pad>
    <layer>END_LAYER</layer>
    <type>REGULAR_PAD</type>
    <figure>RECTANGLE</figure>
    <width>{w:.2f}</width>
    <height>{h:.2f}</height>
  </pad>
  <pad>
    <layer>SOLDERMASK_TOP</layer>
    <type>REGULAR_PAD</type>
    <figure>RECTANGLE</figure>
    <width>{mw:.2f}</width>
    <height>{mh:.2f}</height>
  </pad>
  <pad>
    <layer>PASTEMASK_TOP</layer>
    <type>REGULAR_PAD</type>
    <figure>RECTANGLE</figure>
    <width>{pw:.2f}</width>
    <height>{ph:.2f}</height>
  </pad>
</padstack>
"""
    path.write_text(text, encoding="ascii", newline="\n")


def write_allegro_scr(path: Path) -> None:
    lines = [
        f"# Auto-generated {PART} {FP_NAME} from official HPM QFN48 land",
        "version 17.2.048",
        "setwindow pcb",
        "new",
        f'newdrawfillin "{FP_NAME}.dra" "Package Symbol"',
        "generaledit",
        "prmed",
        "setwindow Form.prmedit",
        "FORM prmedit design",
        "FORM prmedit units Millimeter",
        "FORM prmedit accuracy 4",
        "FORM prmedit size Other",
        "FORM prmedit width 12",
        "FORM prmedit height 12",
        "FORM prmedit Apply",
        "FORM prmedit x -6",
        "FORM prmedit y -6",
        "FORM prmedit done",
        "setwindow pcb",
    ]
    for n in list(range(1, 50)):
        x, y, pad = qfn_pin_xy_mm(n)
        lines.extend(
            [
                "add pin",
                "setwindow Form.mini",
                "Form mini rect_or_polar Rectangular",
                "Form mini x_count 1",
                "Form mini y_count 1",
                "Form mini rotate_pin 0",
                f"FORM mini pad_name {pad}",
                f"FORM mini next_pin_number {n}",
                "FORM mini pintype_mechanical NO",
                f"FORM mini offsetx {x}",
                f"FORM mini offsety {y}",
                "setwindow pcb",
                f"pick {x} {y}",
                "done",
            ]
        )

    # silk body 6x6 + pin1 tick at top-left
    lines.extend(
        [
            "add line",
            "setwindow Form.mini",
            "FORM mini lock_direction Off",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick -3.11 2.56",
            "pick -3.11 3.11",
            "pick -2.56 3.11",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick 2.56 3.11",
            "pick 3.11 3.11",
            "pick 3.11 2.56",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick 3.11 -2.56",
            "pick 3.11 -3.11",
            "pick 2.56 -3.11",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick -2.56 -3.11",
            "pick -3.11 -3.11",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass ASSEMBLY_TOP",
            "FORM mini line_width 0.10",
            "setwindow pcb",
            "pick -3.0 2.0",
            "pick -2.0 3.0",
            "pick 3.0 3.0",
            "pick 3.0 -3.0",
            "pick -3.0 -3.0",
            "pick -3.0 2.0",
            "done",
            "shape add",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass PLACE_BOUND_TOP",
            "FORM mini dyns_fill_type Static solid",
            "FORM mini dyns_grid None",
            "FORM mini dyns_lock_mode Line",
            "setwindow pcb",
            "pick -3.62 -3.62",
            "pick 3.62 -3.62",
            "pick 3.62 3.62",
            "pick -3.62 3.62",
            "pick -3.62 -3.62",
            "done",
            "Label refdes",
            "setwindow Form.mini",
            "FORM mini text_block 3",
            "FORM mini angle 0",
            "FORM mini mirror NO",
            "FORM mini text_justification Center",
            "FORM mini class REF DES",
            "FORM mini subclass SILKSCREEN_TOP",
            "setwindow pcb",
            "pick 0 4.2",
            'Text "REF"',
            "done",
            "zoom fit",
            "save",
            "exit",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")


def write_bat(path: Path) -> None:
    content = f"""@echo off
chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO_BIN={ALLEGRO_BIN}"
set "FP={FP_NAME}"
set "PAD_LIB={PAD_LIB}"
set "PSM_LIB={PSM_LIB}"

echo ============================================
echo Build footprint: %FP%
echo Work: %CD%
echo ============================================

if not exist "%ALLEGRO_BIN%\\allegro.exe" (
  echo ERROR: allegro.exe not found
  goto FAIL
)
if not exist "%ALLEGRO_BIN%\\padstack_editor.exe" (
  echo ERROR: padstack_editor.exe not found
  goto FAIL
)

if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"

echo ---- 1) padstack pxml -^> .pad ----
for %%P in ({PAD_H} {PAD_V} {PAD_EP}) do (
  echo [PAD] %%P
  "%ALLEGRO_BIN%\\padstack_editor.exe" -x "%%P.pxml"
  if exist "%%P.pad" copy /Y "%%P.pad" "%PAD_LIB%\\%%P.pad" >nul
  if not exist "%%P.pad" (
    echo ERROR: %%P.pad not created
    goto FAIL
  )
)

set "PADPATH=%PAD_LIB%;%CD%;%PADPATH%"

echo ---- 2) Allegro package symbol ----
if exist "%FP%.dra" del /q "%FP%.dra"
if exist "%FP%.psm" del /q "%FP%.psm"
if exist "%FP%.dra.lck" del /q "%FP%.dra.lck"

START /WAIT "" "%ALLEGRO_BIN%\\allegro.exe" -nograph -s "%FP%.scr"
if not exist "%FP%.dra" (
  echo ERROR: %FP%.dra not created. See allegro.jrl
  goto FAIL
)

if not exist "backup" mkdir "backup"
copy /Y "%FP%.scr" "backup\\%FP%.scr" >nul
copy /Y "%FP%.bat" "backup\\%FP%.bat" >nul
for %%P in ({PAD_H} {PAD_V} {PAD_EP}) do (
  if exist "%%P.pxml" copy /Y "%%P.pxml" "backup\\%%P.pxml" >nul
  if exist "%%P.pad" copy /Y "%%P.pad" "backup\\%%P.pad" >nul
)
if exist "%FP%.dra" copy /Y "%FP%.dra" "backup\\%FP%.dra" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "backup\\%FP%.psm" >nul

copy /Y "%FP%.dra" "%PSM_LIB%\\%FP%.dra" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%PSM_LIB%\\%FP%.psm" >nul

echo.
echo Done.
echo   Pad -^> %PAD_LIB%
echo   Psm -^> %PSM_LIB%
popd
exit /b 0

:FAIL
echo FAILED
popd
exit /b 1
"""
    path.write_text(content, encoding="ascii", errors="replace", newline="\r\n")


def write_checklist(by_num: dict[str, dict], path: Path) -> None:
    lines = [
        f"{PART} pin checklist  QFN48_EP 6x6 P0.4  footprint={FP_NAME}",
        "Primary names on symbol. Full pinmux in CSV.",
        "IEG1: VPMC shared with DCDC_IN, tie 3.3V; DCDC_LP float if DCDC off.",
        "PA00=ISP_UART_TX  PA01=ISP_UART_RX  PA24=USB_DP  PA25=USB_DM",
        "Pin1 top-left, CCW (datasheet top view).",
        "",
    ]
    for letter in "ABCD":
        title = SECTIONS[letter]["title"]
        lines.append(f"==== U?{letter}  {title} ====")
        for label, L, R in SECTIONS[letter]["layout"]:
            lines.append(f"-- {label} --")
            n = max(len(L), len(R))
            for i in range(n):
                ln = L[i] if i < len(L) else ""
                rn = R[i] if i < len(R) else ""
                lname = by_num[ln]["PinName"] if ln else ""
                rname = by_num[rn]["PinName"] if rn else ""
                lines.append(f"  L {ln:>3} {lname:12} | R {rn:>3} {rname}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readme(path: Path, xml_name: str) -> None:
    text = f"""# {PART} = 先楫 HPM5300 QFN48_EP

按 `ast2400lib` / TMC6460 同款流程生成，目标 **Cadence 17.2**。

| 项目 | 值 |
|------|----|
| 型号 | {PART} |
| 封装 | **QFN48_EP 6×6 mm，P0.4 mm，EP 4.2×4.2 mm** |
| 引脚 | 48 + EP(49) = 49 |
| PCB Footprint | `{FP_NAME}` |
| 分符 | A_POWER / B_SYS / C_PMIC / D_GPIO |
| 焊盘 | `{PAD_H}` 0.85×0.20、`{PAD_V}` 0.20×0.85、`{PAD_EP}` 4.20×4.20 |

引脚来源：先楫官方 KiCad `HPM5300_Library.kicad_sym`（HPM5361IEG1）。  
焊盘来源：官方 `QFN-48_6x6mm_P0.4mm_EP4.2x4.2mm.kicad_mod`。  
坐标系：数据手册顶视，**1 脚左上，逆时针**。

## Capture 导入

1. OrCAD Capture CIS 17.2 → `File` → `Import` → `Library XML`
2. 选择 `OrcadCaptureXML\\{xml_name}`
3. 另存为 `01captureLib\\{PART}.OLB`
4. 放置 `{PART}`，只用 U?A / U?B / U?C / U?D

## Allegro 封装生成

双击：

`AUTOlib\\ul_HPM5361IEG1\\AllegroV17_2\\{FP_NAME}.bat`

会调用 `padstack_editor -x` 生成 `.pad`，再 `allegro -nograph -s` 生成 `.dra/.psm`，并复制到 `01Pad_lib` / `01Psm_lib`。

## 电源注意（IEG1）

- `VPMC` 与 `DCDC_IN` **内部共用**，接 3.3 V
- `DCDC_LP` 若软件关闭 DCDC：**悬空，禁止接地**
- `VSS`(49) 是散热焊盘，必须焊到 GND
- 多个 `VDD_SOC` / `VIO_B00` 同名 Power，Capture 会自动短接

## 量产前复核

- EP 钢网建议按官方 3×3 开窗（本库 EP 膏铜约 80%）
- 对照 HPM5300 数据手册封装图确认 1 脚方向
"""
    path.write_text(text, encoding="utf-8")


def write_guides(out: Path, xml_name: str) -> None:
    (out / "ImportGuides.html").write_text(
        f"""<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
<h1>{PART} UL-format import (Cadence 17.2)</h1>
<ul>
<li><a href="OrcadCaptureXML/ImportGuide.html">OrCAD Capture</a></li>
<li><a href="AllegroV17_2/ImportGuide.html">Allegro PCB Editor</a></li>
</ul>
<p>See README_CN.md</p>
</body></html>
""",
        encoding="utf-8",
    )
    (out / "OrcadCaptureXML" / "ImportGuide.html").write_text(
        f"""<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
<h2>Capture 17.2</h2>
<ol>
<li>Open OrCAD Capture CIS 17.2</li>
<li>File - Import - Library XML</li>
<li>Select {xml_name}</li>
<li>Save OLB to D:/001DIY/005lib/01captureLib/{PART}.OLB</li>
</ol>
<p>Part {PART} is heterogeneous A_POWER / B_SYS / C_PMIC / D_GPIO.</p>
</body></html>
""",
        encoding="utf-8",
    )
    (out / "AllegroV17_2" / "ImportGuide.html").write_text(
        f"""<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
<h2>Allegro 17.2</h2>
<ol>
<li>Double-click {FP_NAME}.bat</li>
<li>Copies .pad to 01Pad_lib and .dra/.psm to 01Psm_lib</li>
</ol>
<p>Footprint: {FP_NAME} (QFN48 6x6 P0.4 EP4.2)</p>
</body></html>
""",
        encoding="utf-8",
    )


def copy_into(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return
    shutil.copy2(src, dst)


def main() -> None:
    by_num = {p["PinNumber"]: p for p in PINS}
    assert len(by_num) == 49, len(by_num)

    placed: list[str] = []
    for letter in "ABCD":
        for _, L, R in SECTIONS[letter]["layout"]:
            placed.extend(L)
            placed.extend(R)
    assert sorted(placed, key=int) == [str(i) for i in range(1, 50)], placed

    alg_dir = OUT / "AllegroV17_2"
    cap_dir = OUT / "OrcadCaptureXML"
    arch_alg = ARCHIVE / "01_成品库_ul_HPM5361IEG1" / "AllegroV17_2"
    arch_cap = ARCHIVE / "01_成品库_ul_HPM5361IEG1" / "OrcadCaptureXML"
    arch_fin = ARCHIVE / "01_成品库_ul_HPM5361IEG1"
    dests = [
        alg_dir, cap_dir, arch_alg, arch_cap,
        CAPTURE_OUT, CAPTURE_OUT / "OrcadCaptureXML", CAPTURE_OUT / "AllegroV17_2",
        SCRIPT_DIR, AI_DIR, PAD_LIB, PSM_LIB,
        ARCHIVE / "02_生成脚本_hpm5361ieg1_lib",
        ARCHIVE / "03_captureLib_HPM5361IEG1" / "OrcadCaptureXML",
        ARCHIVE / "03_captureLib_HPM5361IEG1" / "AllegroV17_2",
        ARCHIVE / "04_script_file_HPM5361IEG1",
    ]
    for d in dests:
        d.mkdir(parents=True, exist_ok=True)

    xml_name = f"{STAMP}.xml"
    cap_xml = cap_dir / xml_name
    write_capture_xml(by_num, cap_xml)

    write_pxml(alg_dir / f"{PAD_H}.pxml", PAD_H, 0.85, 0.20)
    write_pxml(alg_dir / f"{PAD_V}.pxml", PAD_V, 0.20, 0.85)
    write_pxml(alg_dir / f"{PAD_EP}.pxml", PAD_EP, 4.20, 4.20, paste_scale=0.80)

    scr = alg_dir / f"{FP_NAME}.scr"
    write_allegro_scr(scr)
    bat = alg_dir / f"{FP_NAME}.bat"
    write_bat(bat)

    fields = ["PinNumber", "PinName", "Electrical", "Pinmux"]
    csv_rows = [by_num[str(n)] for n in range(1, 50)]

    def dump_csv(dest: Path) -> None:
        with dest.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(csv_rows)

    write_guides(OUT, xml_name)
    write_readme(OUT / "README_CN.md", xml_name)
    write_readme(CAPTURE_OUT / "README_CN.md", xml_name)
    write_readme(arch_fin / "README_CN.md", xml_name)
    write_checklist(by_num, CAPTURE_OUT / f"{PART}_pin_checklist.txt")
    write_checklist(by_num, SCRIPT_DIR / f"{PART}_pin_checklist.txt")
    write_checklist(by_num, ARCHIVE / "03_captureLib_HPM5361IEG1" / f"{PART}_pin_checklist.txt")

    for dest in (OUT, CAPTURE_OUT, AI_DIR, SCRIPT_DIR, arch_fin, ARCHIVE / "03_captureLib_HPM5361IEG1"):
        dump_csv(dest / f"{PART}_pins.csv")

    xml_copies = [
        CAPTURE_OUT / "OrcadCaptureXML" / xml_name,
        arch_cap / xml_name,
        ARCHIVE / "03_captureLib_HPM5361IEG1" / "OrcadCaptureXML" / xml_name,
    ]
    for d in xml_copies:
        copy_into(cap_xml, d)

    for src in (scr, bat, alg_dir / f"{PAD_H}.pxml", alg_dir / f"{PAD_V}.pxml", alg_dir / f"{PAD_EP}.pxml"):
        for folder in (
            CAPTURE_OUT / "AllegroV17_2",
            SCRIPT_DIR,
            arch_alg,
            ARCHIVE / "03_captureLib_HPM5361IEG1" / "AllegroV17_2",
            ARCHIVE / "04_script_file_HPM5361IEG1",
        ):
            copy_into(src, folder / src.name)

    this = Path(__file__).resolve()
    copy_into(this, AI_DIR / this.name)
    copy_into(this, ARCHIVE / "02_生成脚本_hpm5361ieg1_lib" / this.name)
    readme_lib = f"""# {PART} OrCAD / Allegro library

- Datasheet family: HPM5300
- Package: QFN48_EP 6x6 mm P0.4, EP 4.2x4.2
- Pins: 49 (48 + EP)
- Footprint: {FP_NAME}
- Sections: A_POWER / B_SYS / C_PMIC / D_GPIO
- Run: python gen_ul_hpm5361ieg1.py
- Then: {FP_NAME}.bat
"""
    (AI_DIR / f"{PART}_library_readme.md").write_text(readme_lib, encoding="utf-8")
    (ARCHIVE / "02_生成脚本_hpm5361ieg1_lib" / f"{PART}_library_readme.md").write_text(readme_lib, encoding="utf-8")

    print(f"pins={len(by_num)}")
    print("OK capture", cap_xml)
    print("OK footprint bat", bat)
    print()
    print("Next:")
    print(f"  1) Capture Import XML: {cap_xml}")
    print(f"  2) Double-click: {bat}")


if __name__ == "__main__":
    main()
