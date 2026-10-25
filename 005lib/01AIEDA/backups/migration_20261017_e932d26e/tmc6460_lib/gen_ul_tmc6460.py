# -*- coding: utf-8 -*-
"""TMC6460: OrCAD Capture symbol + Allegro TQFN38 5x7 footprint (AST2400-style flow).

Sources:
  - Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/tmc6460.pdf
  - Package: TQFN38 5mm x 7mm, code T3857+1C, outline 21-0172, land 90-0076
  - Land pattern dims aligned with ADI/LTC QFN38 5x7 (05-08-1701 / JEDEC MO-220 WHKD)
"""
from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(r"D:\001DIY\005lib")
OUT = ROOT / "AUTOlib" / "ul_TMC6460"
CAPTURE_OUT = ROOT / "01captureLib" / "TMC6460"
SCRIPT_DIR = ROOT / "01script_file" / "TMC6460"
UL_BUILDER = ROOT / "AUTOlib" / "ul_TPS65217CRSLR" / "AllegroV17_2" / "builder.ile"
ALLEGRO = Path(r"C:\Program0\Cadence\spb172\tools\bin\allegro.exe")
PAD_LIB = ROOT / "01Pad_lib"
PSM_LIB = ROOT / "01Psm_lib"
STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

PART = "TMC6460"
FP_NAME = "TQFN38_5X7"
PAD_LEAD = "r25_70"   # 0.25 x 0.70 mm
PAD_EP = "r315_515"   # 3.15 x 5.15 mm exposed pad

ELEC_CODE = {
    "Input": 0, "Bidirectional": 1, "Output": 2,
    "Passive": 4, "NC": 4, "Power": 7,
}

# Datasheet pin table. Duplicate power names uniquified for Capture.
# Schematic aliases: CS=CSN, SLEEP=SLEEPN, FAULT=FAULTN, UART_TXD=UART_TX, UART_RXD=UART_RX
PINS: list[dict] = [
    {"PinNumber": "1",  "PinName": "CSN",      "Electrical": "Input",  "Side": "L"},
    {"PinNumber": "2",  "PinName": "SLEEPN",   "Electrical": "Input",  "Side": "L"},
    {"PinNumber": "3",  "PinName": "IREF",     "Electrical": "Passive","Side": "L"},
    {"PinNumber": "4",  "PinName": "VCC_IO",   "Electrical": "Power",  "Side": "L"},
    {"PinNumber": "5",  "PinName": "VDD1V8",   "Electrical": "Power",  "Side": "L"},
    {"PinNumber": "6",  "PinName": "GND",      "Electrical": "Power",  "Side": "L"},
    {"PinNumber": "7",  "PinName": "CLK",      "Electrical": "Input",  "Side": "L"},
    {"PinNumber": "8",  "PinName": "UART_TX",  "Electrical": "Output", "Side": "L"},
    {"PinNumber": "9",  "PinName": "UART_RX",  "Electrical": "Input",  "Side": "L"},
    {"PinNumber": "10", "PinName": "REF_L",    "Electrical": "Input",  "Side": "L"},
    {"PinNumber": "11", "PinName": "REF_R",    "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "12", "PinName": "PWM_IN",   "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "13", "PinName": "TEMP",     "Electrical": "Passive","Side": "L"},
    {"PinNumber": "14", "PinName": "ENC_A",    "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "15", "PinName": "ENC_B",    "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "16", "PinName": "ENC_N",    "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "17", "PinName": "HALL_U",   "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "18", "PinName": "HALL_V",   "Electrical": "Bidirectional", "Side": "L"},
    {"PinNumber": "19", "PinName": "HALL_W",   "Electrical": "Bidirectional", "Side": "L"},
    # Right side top->bottom = pin 38 -> 20 (matches reference schematic U301)
    {"PinNumber": "38", "PinName": "SDO",      "Electrical": "Output", "Side": "R"},
    {"PinNumber": "37", "PinName": "SDI",      "Electrical": "Input",  "Side": "R"},
    {"PinNumber": "36", "PinName": "SCK",      "Electrical": "Input",  "Side": "R"},
    {"PinNumber": "35", "PinName": "FAULTN",   "Electrical": "Output", "Side": "R"},
    {"PinNumber": "34", "PinName": "DRV_EN",   "Electrical": "Input",  "Side": "R"},
    {"PinNumber": "33", "PinName": "CPI",      "Electrical": "Passive","Side": "R"},
    {"PinNumber": "32", "PinName": "CPO",      "Electrical": "Passive","Side": "R"},
    {"PinNumber": "31", "PinName": "VCP",      "Electrical": "Passive","Side": "R"},
    {"PinNumber": "30", "PinName": "NC",       "Electrical": "NC",     "Side": "R"},
    {"PinNumber": "29", "PinName": "VS3",      "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "28", "PinName": "OUT1",     "Electrical": "Output", "Side": "R"},
    {"PinNumber": "27", "PinName": "PGND3",    "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "26", "PinName": "PGND2",    "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "25", "PinName": "OUT2",     "Electrical": "Output", "Side": "R"},
    {"PinNumber": "24", "PinName": "VS2",      "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "23", "PinName": "VS1",      "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "22", "PinName": "OUT3",     "Electrical": "Output", "Side": "R"},
    {"PinNumber": "21", "PinName": "PGND1",    "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "20", "PinName": "VCC_IOF",  "Electrical": "Power",  "Side": "R"},
    {"PinNumber": "39", "PinName": "EP",       "Electrical": "Power",  "Side": "L"},
]

# Symbol partition labels (schematic-like)
LAYOUT = [
    ("SPI / Ctrl",
     ["1", "2", "3"],
     ["38", "37", "36", "35", "34"]),
    ("Power / CLK",
     ["4", "5", "6", "7"],
     ["33", "32", "31", "30"]),
    ("UART / IO",
     ["8", "9", "10", "11", "12", "13"],
     ["29", "28", "27", "26", "25", "24"]),
    ("Encoder / Hall",
     ["14", "15", "16", "17", "18", "19"],
     ["23", "22", "21", "20"]),
    ("EP / GND",
     ["39"],
     []),
]


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


def make_libpart(by_num: dict[str, dict]) -> str:
    GRID = 10
    body_w = 280
    y = 20
    gap = 20
    pin_pitch = 10
    graphics: list[str] = []
    pin_blocks: list[str] = []
    maps: list[tuple[str, int]] = []
    pos = 0

    for gi, (label, left_nums, right_nums) in enumerate(LAYOUT):
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
        if gi < len(LAYOUT) - 1:
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
        <Defn suffix="Normal"/>
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
        <SymbolUserProp><Defn name="Description" val="TMC6460 FOC BLDC driver TQFN38 5x7"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="TMC6460"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="Analog Devices / Trinamic"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Package" val="TQFN38 5mm x 7mm (T3857+1C)"/></SymbolUserProp>
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
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Lib xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="olb.xsd">
  <Defn name="{PART}.OLB"/>
  <Package>
    <Defn alphabeticNumbering="1" isHomogeneous="1" name="{PART}" pcbFootprint="{FP_NAME}" pcbLib="" refdesPrefix="U"/>
{make_libpart(by_num)}  </Package>
</Lib>
"""
    path.write_text(xml, encoding="utf-8", newline="\n")


def qfn_pin_xy_mil(num: int) -> tuple[float, float, int]:
    """Physical TQFN38 5x7 pin centers (mils) + pad rotation.

    Land pattern (ADI/LTC QFN38 5x7 recommended):
      pitch 0.50, pad 0.25 x 0.70, outer 7.50 x 5.50, EP 3.15 x 5.15
      center span long=5.50, short=3.00
    Pin1 bottom-left, CCW: bottom 1-12, right 13-19, top 20-31, left 32-38.
    """
    pitch = mm_to_mil(0.50)
    y_pad = (mm_to_mil(7.50) - mm_to_mil(0.70)) / 2.0   # 3.40 mm
    x_pad = (mm_to_mil(5.50) - mm_to_mil(0.70)) / 2.0   # 2.40 mm
    span_long = mm_to_mil(5.50)   # 12 pins on 7mm sides
    span_short = mm_to_mil(3.00)  # 7 pins on 5mm sides

    if 1 <= num <= 12:
        x = -span_long / 2 + (num - 1) * pitch
        return x, -y_pad, 180
    if 13 <= num <= 19:
        y = -span_short / 2 + (num - 13) * pitch
        return x_pad, y, 270
    if 20 <= num <= 31:
        x = span_long / 2 - (num - 20) * pitch
        return x, y_pad, 180
    if 32 <= num <= 38:
        y = span_short / 2 - (num - 32) * pitch
        return -x_pad, y, 270
    if num == 39:
        return 0.0, 0.0, 0
    raise ValueError(num)


def write_footprint_xml(path: Path) -> None:
    lead_w = mm_to_mil(0.25)
    lead_h = mm_to_mil(0.70)
    mask_w = mm_to_mil(0.35)
    mask_h = mm_to_mil(0.80)
    ep_w = mm_to_mil(3.15)
    ep_h = mm_to_mil(5.15)
    body_x = mm_to_mil(5.0) / 2
    body_y = mm_to_mil(7.0) / 2
    place_x = body_x + mm_to_mil(0.25)
    place_y = body_y + mm_to_mil(0.25)
    cy = max(place_x, place_y) + 50

    pins = []
    for n in list(range(1, 39)) + [39]:
        x, y, rot = qfn_pin_xy_mil(n)
        pad = PAD_EP if n == 39 else PAD_LEAD
        pins.append(
            f'    <Pin number="{n}" padName="{pad}" '
            f'originX="{x:.4f}" originY="{y:.4f}" rotation="{rot}" isMechanical="no" textBlk="1" />'
        )

    def rect(layer: str, hx: float, hy: float, lw: float = 5) -> str:
        pts = [(-hx, -hy), (-hx, hy), (hx, hy), (hx, -hy), (-hx, -hy)]
        pts_xml = "\n".join(f'        <Point x="{x:.4f}" y="{y:.4f}" />' for x, y in pts)
        return (
            f'    <Layer name="{layer}" packageHeight="0" >\n'
            f'      <Path lineWidth="{lw}" type="open" >\n{pts_xml}\n'
            f"      </Path>\n    </Layer>\n"
        )

    # Pin1 courtyard mark near bottom-left
    a1x, a1y, _ = qfn_pin_xy_mil(1)
    xml = f"""<Footprint name="{FP_NAME}" >
  <Units type="mils" precision="3" />
  <Extents minX="{-cy:.4f}" minY="{-cy:.4f}" width="{2*cy:.4f}" height="{2*cy:.4f}" />
  <Padstack name="{PAD_LEAD}" type="single" >
    <Layers>
      <Layer name="TOP" >
        <Pad shape="rectangle" width="{lead_w:.4f}" height="{lead_h:.4f}" />
      </Layer>
      <Layer name="PASTEMASK_TOP" >
        <Pad shape="rectangle" width="{lead_w:.4f}" height="{lead_h:.4f}" />
      </Layer>
      <Layer name="SOLDERMASK_TOP" >
        <Pad shape="rectangle" width="{mask_w:.4f}" height="{mask_h:.4f}" />
      </Layer>
    </Layers>
  </Padstack>
  <Padstack name="{PAD_EP}" type="single" >
    <Layers>
      <Layer name="TOP" >
        <Pad shape="rectangle" width="{ep_w:.4f}" height="{ep_h:.4f}" />
      </Layer>
      <Layer name="PASTEMASK_TOP" >
        <Pad shape="rectangle" width="{ep_w * 0.8:.4f}" height="{ep_h * 0.8:.4f}" />
      </Layer>
      <Layer name="SOLDERMASK_TOP" >
        <Pad shape="rectangle" width="{ep_w + mm_to_mil(0.1):.4f}" height="{ep_h + mm_to_mil(0.1):.4f}" />
      </Layer>
    </Layers>
  </Padstack>

  <TextBlocks>
    <TextBlock name="17" width="6.25" height="25" lineSpacing="25" characterSpacing="6.25" />
  </TextBlocks>

  <Pins>
{chr(10).join(pins)}
  </Pins>
  <Vias>
  </Vias>
  <Layers>
{rect("PACKAGE GEOMETRY/ASSEMBLY_TOP", body_x, body_y, 5)}{rect("PACKAGE GEOMETRY/PLACE_BOUND_TOP", place_x, place_y, 0)}{rect("PACKAGE GEOMETRY/SILKSCREEN_TOP", body_x, body_y, 5)}    <Layer name="PACKAGE GEOMETRY/SILKSCREEN_TOP" packageHeight="0" >
      <Path lineWidth="0" type="shape" >
        <Point x="{a1x - 20:.4f}" y="{a1y - 20:.4f}" />
        <Point x="{a1x - 5:.4f}" y="{a1y - 20:.4f}" />
        <Point x="{a1x - 5:.4f}" y="{a1y - 5:.4f}" />
        <Point x="{a1x - 20:.4f}" y="{a1y - 5:.4f}" />
        <Point x="{a1x - 20:.4f}" y="{a1y - 20:.4f}" />
      </Path>
    </Layer>
    <Layer name="REF DES/SILKSCREEN_TOP" packageHeight="0" >
      <Label layer="REF DES/SILKSCREEN_TOP" textBlock="3" angle="0" x="0" y="{-body_y - 40:.4f}" text="Ref" justify="center" />
    </Layer>
    <Layer name="REF DES/ASSEMBLY_TOP" packageHeight="0" >
      <Label layer="REF DES/ASSEMBLY_TOP" textBlock="3" angle="0" x="0" y="{-body_y - 40:.4f}" text="Ref" justify="center" />
    </Layer>
    <Layer name="DEVICE TYPE/SILKSCREEN_TOP" packageHeight="0" >
      <Label layer="DEVICE TYPE/SILKSCREEN_TOP" textBlock="3" angle="0" x="0" y="{body_y + 40:.4f}" text="Dev" justify="center" />
    </Layer>
  </Layers>
  <Heights>
  </Heights>
</Footprint>
"""
    path.write_text(xml, encoding="ascii", newline="\n")


def write_bat(path: Path) -> None:
    content = f"""@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO={ALLEGRO}"
set "FP={FP_NAME}"
set "PAD1={PAD_LEAD}"
set "PAD2={PAD_EP}"
set "PAD_LIB={PAD_LIB}"
set "PSM_LIB={PSM_LIB}"
set "scriptDir=%CD%"
set "skillScriptPath=!scriptDir:\\=/!"

echo ============================================
echo Build footprint: %FP%
echo Work: %CD%
echo ============================================

if not exist "%ALLEGRO%" (
  echo ERROR: allegro.exe not found: %ALLEGRO%
  goto FAIL
)
if not exist "builder.ile" (
  echo ERROR: builder.ile missing
  goto FAIL
)
if not exist "%FP%.xml" (
  echo ERROR: missing %FP%.xml
  goto FAIL
)

del /q "%FP%.dra" "%FP%.psm" "tqfn38_5x7.psm" "%PAD1%.pad" "%PAD2%.pad" *.lck 2>nul

echo skill load "!skillScriptPath!/builder.ile" > builder.scr.txt
echo skill changeWorkingDir "!skillScriptPath%" >> builder.scr.txt
echo skill LB_createFootprint "!skillScriptPath!/%FP%.xml" >> builder.scr.txt
echo exit >> builder.scr.txt

echo ---- builder.scr.txt ----
type builder.scr.txt
echo -------------------------
echo Running Allegro...
START /WAIT "" "%ALLEGRO%" -s builder.scr.txt

if not exist "%FP%.dra" (
  echo ERROR: %FP%.dra not created. See allegro.jrl / %FP%.log
  goto FAIL
)

if exist "tqfn38_5x7.psm" if not exist "%FP%.psm" copy /y "tqfn38_5x7.psm" "%FP%.psm" >nul

if not exist "backup" mkdir "backup"
copy /y "%FP%.xml" "backup\\%FP%.xml" >nul
copy /y "%FP%.bat" "backup\\%FP%.bat" >nul
copy /y "builder.ile" "backup\\builder.ile" >nul
if exist "%FP%.dra" copy /y "%FP%.dra" "backup\\%FP%.dra" >nul
if exist "%PAD1%.pad" copy /y "%PAD1%.pad" "backup\\%PAD1%.pad" >nul
if exist "%PAD2%.pad" copy /y "%PAD2%.pad" "backup\\%PAD2%.pad" >nul
if exist "%FP%.psm" copy /y "%FP%.psm" "backup\\%FP%.psm" >nul

if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if exist "%PAD1%.pad" copy /y "%PAD1%.pad" "%PAD_LIB%\\%PAD1%.pad" >nul
if exist "%PAD2%.pad" copy /y "%PAD2%.pad" "%PAD_LIB%\\%PAD2%.pad" >nul

if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"
copy /y "%FP%.xml" "%PSM_LIB%\\%FP%.xml" >nul
copy /y "%FP%.dra" "%PSM_LIB%\\%FP%.dra" >nul
if exist "%FP%.psm" copy /y "%FP%.psm" "%PSM_LIB%\\%FP%.psm" >nul
if exist "tqfn38_5x7.psm" if not exist "%PSM_LIB%\\%FP%.psm" copy /y "tqfn38_5x7.psm" "%PSM_LIB%\\%FP%.psm" >nul

echo.
echo Done.
echo   Pad -> %PAD_LIB%
echo   Psm -> %PSM_LIB%
popd
pause
exit /b 0

:FAIL
echo.
echo FAILED. Check allegro.jrl
popd
pause
exit /b 1
"""
    path.write_text(content, encoding="ascii", errors="replace", newline="\r\n")


def write_checklist(by_num: dict[str, dict], path: Path) -> None:
    lines = [
        "TMC6460 pin checklist (L/R match reference Motor Driver schematic)",
        "Datasheet names used. Schematic aliases: CS=CSN, SLEEP=SLEEPN, FAULT=FAULTN,",
        "UART_TXD=UART_TX, UART_RXD=UART_RX. Package: TQFN38 5x7 (NOT TQFN-56L).",
        "",
    ]
    for label, L, R in LAYOUT:
        lines.append(f"-- {label} --")
        n = max(len(L), len(R))
        for i in range(n):
            ln = L[i] if i < len(L) else ""
            rn = R[i] if i < len(R) else ""
            lname = by_num[ln]["PinName"] if ln else ""
            rname = by_num[rn]["PinName"] if rn else ""
            lines.append(f"  L {ln:3} {lname:12} | R {rn:3} {rname}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readme(path: Path, xml_name: str) -> None:
    text = f"""# TMC6460 = Motor Driver U301

Source: TMC6460 datasheet (Analog Devices / Trinamic)

| Item | Value |
|------|-------|
| Part | TMC6460 |
| Package | **TQFN38 5mm x 7mm** (T3857+1C / 21-0172) |
| Pins | 38 + EP(39) = 39 |
| PCB Footprint | `{FP_NAME}` |
| Pitch | 0.50 mm |
| Lead land | 0.25 x 0.70 mm |
| Exposed pad | 3.15 x 5.15 mm |

> Schematic label TQFN-56L is wrong; datasheet package is TQFN38.

## Import Capture

1. OrCAD Capture -> File -> Import -> Library XML
2. Select: `OrcadCaptureXML\\{xml_name}`
3. Save as `01captureLib\\TMC6460.OLB`
4. Place `TMC6460` (refdes U)

## Build Allegro footprint

Double-click:

`AUTOlib\\ul_TMC6460\\AllegroV17_2\\{FP_NAME}.bat`

Copies `.pad` -> `01Pad_lib`, `.dra/.psm` -> `01Psm_lib`.

## Name notes

| Datasheet | Schematic (U301) |
|-----------|------------------|
| CSN | CS |
| SLEEPN | SLEEP |
| FAULTN | FAULT |
| UART_TX / UART_RX | UART_TXD / UART_RXD |
| VS1/VS2/VS3 | VS |
| PGND1/PGND2/PGND3 | PGND |
| EP | PAD |
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    by_num = {p["PinNumber"]: p for p in PINS}
    assert len(by_num) == 39, len(by_num)

    placed = []
    for _, L, R in LAYOUT:
        placed.extend(L)
        placed.extend(R)
    assert sorted(placed, key=int) == [str(i) for i in range(1, 40)], placed

    alg_dir = OUT / "AllegroV17_2"
    cap_dir = OUT / "OrcadCaptureXML"
    for d in (
        alg_dir, cap_dir, CAPTURE_OUT, CAPTURE_OUT / "OrcadCaptureXML",
        CAPTURE_OUT / "AllegroV17_2", SCRIPT_DIR, PAD_LIB, PSM_LIB,
    ):
        d.mkdir(parents=True, exist_ok=True)

    xml_name = f"{STAMP}.xml"
    cap_xml = cap_dir / xml_name
    write_capture_xml(by_num, cap_xml)
    shutil.copy2(cap_xml, CAPTURE_OUT / "OrcadCaptureXML" / xml_name)

    fp_xml = alg_dir / f"{FP_NAME}.xml"
    write_footprint_xml(fp_xml)
    shutil.copy2(fp_xml, CAPTURE_OUT / "AllegroV17_2" / f"{FP_NAME}.xml")
    shutil.copy2(fp_xml, PSM_LIB / f"{FP_NAME}.xml")
    shutil.copy2(fp_xml, SCRIPT_DIR / f"{FP_NAME}.xml")

    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, alg_dir / "builder.ile")
        shutil.copy2(UL_BUILDER, CAPTURE_OUT / "AllegroV17_2" / "builder.ile")

    bat = alg_dir / f"{FP_NAME}.bat"
    write_bat(bat)
    shutil.copy2(bat, CAPTURE_OUT / "AllegroV17_2" / f"{FP_NAME}.bat")
    shutil.copy2(bat, SCRIPT_DIR / f"{FP_NAME}.bat")

    fields = ["PinNumber", "PinName", "Electrical", "Side"]
    for dest in (OUT, CAPTURE_OUT, ROOT / "01AIcadence" / "tmc6460_lib", SCRIPT_DIR):
        with (dest / "TMC6460_pins.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            # numeric order for CSV
            for n in range(1, 40):
                w.writerow(by_num[str(n)])

    write_checklist(by_num, CAPTURE_OUT / "TMC6460_pin_checklist.txt")
    write_checklist(by_num, SCRIPT_DIR / "TMC6460_pin_checklist.txt")
    write_readme(CAPTURE_OUT / "README_CN.md", xml_name)
    write_readme(OUT / "README_CN.md", xml_name)

    print(f"pins={len(by_num)}")
    print("OK capture", cap_xml)
    print("OK footprint", fp_xml)
    print("OK bat", bat)
    print()
    print("Next:")
    print(f"  1) Capture Import XML: {cap_xml}")
    print(f"  2) Double-click: {bat}")


if __name__ == "__main__":
    main()
