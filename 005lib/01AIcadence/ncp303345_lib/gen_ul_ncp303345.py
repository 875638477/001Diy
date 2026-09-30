# -*- coding: utf-8 -*-
"""Generate the NCP303345 OrCAD Capture symbol and Allegro 17.2 footprint.

Sources:
  - NCP303345/D Rev.2, pin table on page 3
  - onsemi CASE 483BV Issue D / 98AON13704G, page 22

The output layout follows the existing ast2400lib/HPM5361IEG1 workflow.
"""
from __future__ import annotations

import csv
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


PART = "NCP303345MNTWG"
VALUE = "NCP303345"
FP_NAME = "PQFN24_4X5_P0D5_483BV"
STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

ARCHIVE = Path(__file__).resolve().parents[1]
AUTOLIB = ARCHIVE.parent
LIB_ROOT = AUTOLIB.parent
OUT = AUTOLIB / "ul_NCP303345"
CAPTURE_OUT = LIB_ROOT / "01captureLib" / "NCP303345"
SCRIPT_OUT = LIB_ROOT / "01script_file" / "NCP303345"
AI_OUT = LIB_ROOT / "01AIcadence" / "ncp303345_lib"
PAD_LIB = LIB_ROOT / "01Pad_lib"
PSM_LIB = LIB_ROOT / "01Psm_lib"
ALLEGRO_BIN = Path(r"C:\Program0\Cadence\spb172\tools\bin")

ELEC_CODE = {
    "Input": 0,
    "Bidirectional": 1,
    "Output": 2,
    "Passive": 4,
    "NC": 4,
    "Power": 7,
}

PINS: list[dict[str, str]] = [
    {"PinNumber": "1", "PinName": "TMON/FLT", "Electrical": "Output", "Description": "Temperature monitor and fault flag"},
    {"PinNumber": "2", "PinName": "EN", "Electrical": "Input", "Description": "Enable input"},
    {"PinNumber": "3", "PinName": "NC", "Electrical": "NC", "Description": "Leave floating or connect to GND"},
    {"PinNumber": "4", "PinName": "PVCC", "Electrical": "Power", "Description": "Low-side gate-driver supply"},
    {"PinNumber": "5", "PinName": "GL", "Electrical": "Output", "Description": "Low-side gate connection"},
    {"PinNumber": "6", "PinName": "PGND", "Electrical": "Power", "Description": "Power ground"},
    {"PinNumber": "7", "PinName": "PGND", "Electrical": "Power", "Description": "Power ground"},
    {"PinNumber": "8", "PinName": "SW", "Electrical": "Passive", "Description": "Switch node"},
    {"PinNumber": "9", "PinName": "SW", "Electrical": "Passive", "Description": "Switch node"},
    {"PinNumber": "10", "PinName": "SW", "Electrical": "Passive", "Description": "Switch node"},
    {"PinNumber": "11", "PinName": "SW", "Electrical": "Passive", "Description": "Switch node"},
    {"PinNumber": "12", "PinName": "SW", "Electrical": "Passive", "Description": "Switch node"},
    {"PinNumber": "13", "PinName": "PGND", "Electrical": "Power", "Description": "Power ground"},
    {"PinNumber": "14", "PinName": "PGND", "Electrical": "Power", "Description": "Power ground"},
    {"PinNumber": "15", "PinName": "VIN", "Electrical": "Power", "Description": "Power-stage input"},
    {"PinNumber": "16", "PinName": "VIN", "Electrical": "Power", "Description": "Power-stage input"},
    {"PinNumber": "17", "PinName": "VIN", "Electrical": "Power", "Description": "Power-stage input"},
    {"PinNumber": "18", "PinName": "PHASE", "Electrical": "Passive", "Description": "Bootstrap capacitor phase node"},
    {"PinNumber": "19", "PinName": "BOOT", "Electrical": "Power", "Description": "High-side gate-driver bootstrap supply"},
    {"PinNumber": "20", "PinName": "PWM", "Electrical": "Input", "Description": "Three-state PWM input"},
    {"PinNumber": "21", "PinName": "VCC", "Electrical": "Power", "Description": "Analog-control and boost supply"},
    {"PinNumber": "22", "PinName": "AGND", "Electrical": "Power", "Description": "Analog ground"},
    {"PinNumber": "23", "PinName": "NC", "Electrical": "NC", "Description": "Not connected"},
    {"PinNumber": "24", "PinName": "IMON", "Electrical": "Output", "Description": "Current-monitor output"},
    {"PinNumber": "25", "PinName": "PGND", "Electrical": "Power", "Description": "Exposed power-ground pad"},
    {"PinNumber": "26", "PinName": "VIN", "Electrical": "Power", "Description": "Exposed VIN pad"},
    {"PinNumber": "27", "PinName": "GL", "Electrical": "Output", "Description": "Exposed low-side gate pad"},
    {"PinNumber": "28", "PinName": "PGND", "Electrical": "Power", "Description": "Exposed power-ground pad"},
]

# Functional placement in the Capture symbol, independent of package pin order.
LEFT = ["2", "20", "19", "18", "21", "4", "24", "1", "22"]
RIGHT = ["15", "16", "17", "26", "8", "9", "10", "11", "12", "5", "27",
         "6", "7", "13", "14", "25", "28", "3", "23"]

# Copper land definitions from the CASE 483BV recommended mounting footprint.
# Pin 28 is generated as a separate Allegro Shape Symbol to preserve its notch.
PAD_L = "ncp_r54_30"     # left pins 1..7: 0.54 x 0.30 mm
PAD_R = "ncp_r47_30"     # right pins 13..17: 0.47 x 0.30 mm
PAD_B = "ncp_r30_54"     # bottom pins 8..12: 0.30 x 0.54 mm
PAD_T = "ncp_r30_47"     # top pins 18..24: 0.30 x 0.47 mm
PAD_25 = "ncp_ep25"
PAD_26 = "ncp_ep26"
PAD_27 = "ncp_ep27"
PAD_28 = "ncp_ep28"
SHAPE_28 = "ncp_ep28_shape"

PAD_SPECS: dict[str, tuple[float, float, float]] = {
    PAD_L: (0.54, 0.30, 1.00),
    PAD_R: (0.47, 0.30, 1.00),
    PAD_B: (0.30, 0.54, 1.00),
    PAD_T: (0.30, 0.47, 1.00),
    PAD_25: (2.10, 1.86, 0.80),
    PAD_26: (1.35, 1.71, 0.80),
    PAD_27: (0.50, 0.20, 0.80),
    PAD_28: (3.52, 1.42, 0.80),
}


def mm_to_mil(mm: float) -> float:
    return mm / 0.0254


def pin_xml(name: str, position: int, electrical: str, left: bool, y: int, body_w: int) -> str:
    start_x, hotpt_x = ((0, -30) if left else (body_w, body_w + 30))
    no_connect = 1 if electrical == "NC" else 0
    return f"""        <SymbolPinScalar>
          <Defn hotptX="{hotpt_x}" hotptY="{y}" name="{escape(name)}" position="{position}" startX="{start_x}" startY="{y}" type="{ELEC_CODE[electrical]}" visible="1"/>
          <IsLong><Defn val="1"/></IsLong>
          <IsClock><Defn val="0"/></IsClock>
          <IsDot><Defn val="0"/></IsDot>
          <IsLeftPointing><Defn val="0"/></IsLeftPointing>
          <IsRightPointing><Defn val="0"/></IsRightPointing>
          <IsNetStyle><Defn val="0"/></IsNetStyle>
          <IsNoConnect><Defn val="{no_connect}"/></IsNoConnect>
          <IsGlobal><Defn val="0"/></IsGlobal>
          <IsNumberVisible><Defn val="1"/></IsNumberVisible>
        </SymbolPinScalar>
"""


def make_libpart(by_num: dict[str, dict[str, str]]) -> str:
    body_w = 220
    pin_blocks: list[str] = []
    pin_map: list[tuple[str, int]] = []
    position = 0
    for side, numbers in ((True, LEFT), (False, RIGHT)):
        for row, number in enumerate(numbers):
            pin = by_num[number]
            y = 20 + row * 10
            pin_blocks.append(pin_xml(pin["PinName"], position, pin["Electrical"], side, y, body_w))
            pin_map.append((number, position))
            position += 1
    bbox_y2 = 220
    physical = "".join(
        f'        <PinNumber><Defn number="{number}" position="{position}"/></PinNumber>\n'
        for number, position in pin_map
    )
    return f"""    <LibPart>
      <Defn/>
      <NormalView>
        <Defn suffix="Normal"/>
        <SymbolDisplayProp>
          <Defn locX="20" locY="-30" name="Part Reference" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor><PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolDisplayProp>
          <Defn locX="20" locY="-20" name="Value" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor><PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolUserProp><Defn name="Description" val="onsemi NCP303345 45 A DrMOS smart power stage"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="{PART}"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="onsemi"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Package" val="PQFN24 4x5 mm P0.5 CASE 483BV"/></SymbolUserProp>
        <SymbolColor><Defn val="48"/></SymbolColor>
        <SymbolBBox><Defn x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></SymbolBBox>
        <IsPinNumbersVisible><Defn val="1"/></IsPinNumbersVisible>
        <IsPinNamesRotated><Defn val="0"/></IsPinNamesRotated>
        <IsPinNamesVisible><Defn val="1"/></IsPinNamesVisible>
        <ContentsLibName><Defn name=""/></ContentsLibName>
        <ContentsViewName><Defn name="{VALUE}"/></ContentsViewName>
        <ContentsViewType><Defn type="0"/></ContentsViewType>
        <PartValue><Defn name="{VALUE}"/></PartValue>
        <Reference><Defn name="U"/></Reference>
        <Rect><Defn fillStyle="1" hatchStyle="0" lineStyle="0" lineWidth="3" x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></Rect>
{"".join(pin_blocks)}      </NormalView>
      <PhysicalPart><Defn/>
{physical}      </PhysicalPart>
    </LibPart>
"""


def write_capture_xml(by_num: dict[str, dict[str, str]], path: Path) -> None:
    text = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Lib xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="olb.xsd">
  <Defn name="{VALUE}.OLB"/>
  <Package>
    <Defn alphabeticNumbering="1" isHomogeneous="1" name="{VALUE}" pcbFootprint="{FP_NAME}" pcbLib="" refdesPrefix="U"/>
{make_libpart(by_num)}  </Package>
</Lib>
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def write_pxml(path: Path, name: str, width_mm: float, height_mm: float, paste_scale: float) -> None:
    width = mm_to_mil(width_mm)
    height = mm_to_mil(height_mm)
    mask_w = mm_to_mil(width_mm + 0.10)
    mask_h = mm_to_mil(height_mm + 0.10)
    paste_w = width * paste_scale
    paste_h = height * paste_scale
    text = f"""<?xml version="1.0" encoding="iso-8859-1" ?>
<!DOCTYPE padstack>
<padstack version="1.0">
  <padstackname>{name}</padstackname>
  <padstackusage>SMD_PIN</padstackusage>
  <units>MILS</units><accuracy>2</accuracy>
  <pad><layer>BEGIN_LAYER</layer><type>REGULAR_PAD</type><figure>RECTANGLE</figure><width>{width:.2f}</width><height>{height:.2f}</height></pad>
  <pad><layer>SOLDERMASK_TOP</layer><type>REGULAR_PAD</type><figure>RECTANGLE</figure><width>{mask_w:.2f}</width><height>{mask_h:.2f}</height></pad>
  <pad><layer>PASTEMASK_TOP</layer><type>REGULAR_PAD</type><figure>RECTANGLE</figure><width>{paste_w:.2f}</width><height>{paste_h:.2f}</height></pad>
</padstack>
"""
    path.write_text(text, encoding="ascii", newline="\n")


def write_shape_pxml(path: Path) -> None:
    """Pin 28 copper uses the stepped shape shown in 98AON13704G."""
    width = mm_to_mil(3.52)
    height = mm_to_mil(1.42)
    mask_w = mm_to_mil(3.62)
    mask_h = mm_to_mil(1.52)
    paste_w = width * 0.80
    paste_h = height * 0.80
    text = f"""<?xml version="1.0" encoding="iso-8859-1" ?>
<!DOCTYPE padstack>
<padstack version="1.0">
  <padstackname>{PAD_28}</padstackname>
  <padstackusage>SMD_PIN</padstackusage>
  <units>MILS</units><accuracy>2</accuracy>
  <pad><layer>BEGIN_LAYER</layer><type>REGULAR_PAD</type><figure>SHAPE_SYMBOL</figure><shapename>{SHAPE_28}</shapename><width>{width:.2f}</width><height>{height:.2f}</height><shape>{SHAPE_28}</shape></pad>
  <pad><layer>SOLDERMASK_TOP</layer><type>REGULAR_PAD</type><figure>RECTANGLE</figure><width>{mask_w:.2f}</width><height>{mask_h:.2f}</height></pad>
  <pad><layer>PASTEMASK_TOP</layer><type>REGULAR_PAD</type><figure>RECTANGLE</figure><width>{paste_w:.2f}</width><height>{paste_h:.2f}</height></pad>
</padstack>
"""
    path.write_text(text, encoding="ascii", newline="\n")


def write_shape_scr(path: Path) -> None:
    """Build the Pin 28 stepped copper as an Allegro shape symbol."""
    lines = [
        f"# {PART} Pin 28 stepped PGND land from CASE 483BV",
        "version 17.2.048", "setwindow pcb", "new",
        f'newdrawfillin "{SHAPE_28}.dra" "Shape Symbol"',
        "generaledit", "prmed", "setwindow Form.prmedit", "FORM prmedit design",
        "FORM prmedit units Millimeter", "FORM prmedit accuracy 4",
        "FORM prmedit size Other", "FORM prmedit width 6", "FORM prmedit height 4",
        "FORM prmedit Apply", "FORM prmedit x -3", "FORM prmedit y -2",
        "FORM prmedit done", "setwindow pcb",
        "shape add", "setwindow Form.mini", "FORM mini class ETCH",
        "FORM mini subclass TOP", "FORM mini dyns_fill_type Static solid",
        "FORM mini dyns_grid None", "FORM mini dyns_lock_mode Line",
        "setwindow pcb",
        # Local origin is inside the land. Absolute bounds after placement:
        # x=-1.75..1.77, y=-1.77..-0.35; upper-right step y=-0.48.
        "pick -1.76 0.71", "pick -0.51 0.71", "pick -0.51 0.58",
        "pick 1.76 0.58", "pick 1.76 -0.71", "pick -1.76 -0.71",
        "pick -1.76 0.71", "done", "zoom fit", "save", "exit",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")


def footprint_pins() -> list[tuple[int, float, float, str]]:
    pins: list[tuple[int, float, float, str]] = []
    for number in range(1, 8):
        pins.append((number, -2.33, 1.50 - (number - 1) * 0.50, PAD_L))
    for number in range(8, 13):
        pins.append((number, -1.00 + (number - 8) * 0.50, -2.33, PAD_B))
    for number in range(13, 18):
        pins.append((number, 2.365, -1.00 + (number - 13) * 0.50, PAD_R))
    for number in range(18, 25):
        pins.append((number, 1.50 - (number - 18) * 0.50, 2.365, PAD_T))
    pins.extend([
        (25, -0.76, 0.93, PAD_25),    # bounds x=-1.81..0.29, y=0.00..1.86
        (26, 1.075, 1.005, PAD_26),   # bounds x=0.40..1.75, y=0.15..1.86
        (27, -1.50, -0.15, PAD_27),   # keep GL clear of PGND pads 25 and 28
        (28, 0.01, -1.06, PAD_28),    # stepped PGND paddle
    ])
    return pins


def write_allegro_scr(path: Path) -> None:
    lines = [
        f"# Auto-generated {PART}; source onsemi CASE 483BV Issue D",
        "version 17.2.048", "setwindow pcb", "new",
        f'newdrawfillin "{FP_NAME}.dra" "Package Symbol"',
        "generaledit", "prmed", "setwindow Form.prmedit", "FORM prmedit design",
        "FORM prmedit units Millimeter", "FORM prmedit accuracy 4",
        "FORM prmedit size Other", "FORM prmedit width 12", "FORM prmedit height 12",
        "FORM prmedit Apply", "FORM prmedit x -6", "FORM prmedit y -6",
        "FORM prmedit done", "setwindow pcb",
    ]
    for number, x, y, pad in footprint_pins():
        lines.extend([
            "add pin", "setwindow Form.mini", "Form mini rect_or_polar Rectangular",
            "Form mini x_count 1", "Form mini y_count 1", "Form mini rotate_pin 0",
            f"FORM mini pad_name {pad}", f"FORM mini next_pin_number {number}",
            "FORM mini pintype_mechanical NO", "FORM mini offsetx 0",
            "FORM mini offsety 0", "setwindow pcb", f"pick {x:.4f} {y:.4f}", "done",
        ])
    # Silkscreen corner marks preserve clearance from the peripheral pads.
    lines.extend([
        "add line", "setwindow Form.mini", "FORM mini lock_direction Off",
        "FORM mini class PACKAGE GEOMETRY", "FORM mini subclass SILKSCREEN_TOP",
        "FORM mini line_width 0.12", "setwindow pcb",
        "pick -2.15 1.90", "pick -2.15 2.65", "pick -1.75 2.65", "done",
        "add line", "setwindow Form.mini", "FORM mini class PACKAGE GEOMETRY",
        "FORM mini subclass SILKSCREEN_TOP", "FORM mini line_width 0.12",
        "setwindow pcb", "pick 1.75 2.65", "pick 2.15 2.65", "pick 2.15 1.90", "done",
        "add line", "setwindow Form.mini", "FORM mini class PACKAGE GEOMETRY",
        "FORM mini subclass SILKSCREEN_TOP", "FORM mini line_width 0.12",
        "setwindow pcb", "pick 2.15 -1.90", "pick 2.15 -2.65", "pick 1.75 -2.65", "done",
        "add line", "setwindow Form.mini", "FORM mini class PACKAGE GEOMETRY",
        "FORM mini subclass SILKSCREEN_TOP", "FORM mini line_width 0.12",
        "setwindow pcb", "pick -1.75 -2.65", "pick -2.15 -2.65", "pick -2.15 -1.90", "done",
        "add line", "setwindow Form.mini", "FORM mini class PACKAGE GEOMETRY",
        "FORM mini subclass ASSEMBLY_TOP", "FORM mini line_width 0.10",
        "setwindow pcb", "pick -2.0 2.0", "pick -1.5 2.5", "pick 2.0 2.5",
        "pick 2.0 -2.5", "pick -2.0 -2.5", "pick -2.0 2.0", "done",
        "shape add", "setwindow Form.mini", "FORM mini class PACKAGE GEOMETRY",
        "FORM mini subclass PLACE_BOUND_TOP", "FORM mini dyns_fill_type Static solid",
        "FORM mini dyns_grid None", "FORM mini dyns_lock_mode Line", "setwindow pcb",
        "pick -2.75 -3.00", "pick 2.75 -3.00", "pick 2.75 3.00",
        "pick -2.75 3.00", "pick -2.75 -3.00", "done",
        "Label refdes", "setwindow Form.mini", "FORM mini text_block 3",
        "FORM mini angle 0", "FORM mini mirror NO", "FORM mini text_justification Center",
        "FORM mini class REF DES", "FORM mini subclass SILKSCREEN_TOP",
        "setwindow pcb", "pick 0 3.4", 'Text "REF"', "done",
        "zoom fit", "save", "exit",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")


def write_bat(path: Path) -> None:
    pads = " ".join(PAD_SPECS)
    archive_alg = ARCHIVE / "01_成品库_ul_NCP303345" / "AllegroV17_2"
    capture_alg = ARCHIVE / "03_captureLib_NCP303345" / "AllegroV17_2"
    text = f"""@echo off
chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"
set "ALLEGRO_BIN={ALLEGRO_BIN}"
set "FP={FP_NAME}"
set "PAD_LIB={PAD_LIB}"
set "PSM_LIB={PSM_LIB}"
set "ARCHIVE_ALG={archive_alg}"
set "CAPTURE_ALG={capture_alg}"
if not exist "%ALLEGRO_BIN%\\allegro.exe" (echo ERROR: allegro.exe not found& goto FAIL)
if not exist "%ALLEGRO_BIN%\\padstack_editor.exe" (echo ERROR: padstack_editor.exe not found& goto FAIL)
if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"
if not exist "%ARCHIVE_ALG%" mkdir "%ARCHIVE_ALG%"
if not exist "%CAPTURE_ALG%" mkdir "%CAPTURE_ALG%"
if exist "{SHAPE_28}.dra" del /q "{SHAPE_28}.dra"
if exist "{SHAPE_28}.ssm" del /q "{SHAPE_28}.ssm"
START /WAIT "" "%ALLEGRO_BIN%\\allegro.exe" -nograph -s "{SHAPE_28}.scr"
if not exist "{SHAPE_28}.ssm" (echo ERROR: {SHAPE_28}.ssm not created& goto FAIL)
copy /Y "{SHAPE_28}.ssm" "%PSM_LIB%\\{SHAPE_28}.ssm" >nul
set "PSMPATH=%PSM_LIB%;%CD%;%PSMPATH%"
for %%P in ({pads}) do (
  echo [PAD] %%P
  "%ALLEGRO_BIN%\\padstack_editor.exe" -x "%%P.pxml"
  if not exist "%%P.pad" (echo ERROR: %%P.pad not created& goto FAIL)
  copy /Y "%%P.pad" "%PAD_LIB%\\%%P.pad" >nul
  copy /Y "%%P.pad" "%ARCHIVE_ALG%\\%%P.pad" >nul
  copy /Y "%%P.pad" "%CAPTURE_ALG%\\%%P.pad" >nul
)
set "PADPATH=%PAD_LIB%;%CD%;%PADPATH%"
if exist "%FP%.dra" del /q "%FP%.dra"
if exist "%FP%.psm" del /q "%FP%.psm"
if exist "%FP%.dra.lck" del /q "%FP%.dra.lck"
START /WAIT "" "%ALLEGRO_BIN%\\allegro.exe" -nograph -s "%FP%.scr"
if not exist "%FP%.dra" (echo ERROR: %FP%.dra not created. See allegro.jrl& goto FAIL)
findstr /C:"ERROR(" "allegro.jrl" >nul && (echo ERROR: Allegro journal contains errors& goto FAIL)
if not exist "backup" mkdir "backup"
copy /Y "%FP%.scr" "backup\\%FP%.scr" >nul
copy /Y "%FP%.bat" "backup\\%FP%.bat" >nul
copy /Y "{SHAPE_28}.scr" "backup\\{SHAPE_28}.scr" >nul
copy /Y "{SHAPE_28}.dra" "backup\\{SHAPE_28}.dra" >nul
copy /Y "{SHAPE_28}.ssm" "backup\\{SHAPE_28}.ssm" >nul
for %%P in ({pads}) do (
  copy /Y "%%P.pxml" "backup\\%%P.pxml" >nul
  copy /Y "%%P.pad" "backup\\%%P.pad" >nul
)
copy /Y "%FP%.dra" "%PSM_LIB%\\%FP%.dra" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%PSM_LIB%\\%FP%.psm" >nul
copy /Y "%FP%.dra" "%ARCHIVE_ALG%\\%FP%.dra" >nul
copy /Y "%FP%.dra" "%CAPTURE_ALG%\\%FP%.dra" >nul
copy /Y "{SHAPE_28}.dra" "%ARCHIVE_ALG%\\{SHAPE_28}.dra" >nul
copy /Y "{SHAPE_28}.ssm" "%ARCHIVE_ALG%\\{SHAPE_28}.ssm" >nul
copy /Y "{SHAPE_28}.dra" "%CAPTURE_ALG%\\{SHAPE_28}.dra" >nul
copy /Y "{SHAPE_28}.ssm" "%CAPTURE_ALG%\\{SHAPE_28}.ssm" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%ARCHIVE_ALG%\\%FP%.psm" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%CAPTURE_ALG%\\%FP%.psm" >nul
echo Done: %FP%
popd
exit /b 0
:FAIL
echo FAILED
popd
exit /b 1
"""
    # chcp 65001 is set before cmd.exe reaches paths containing Chinese names.
    path.write_text(text, encoding="utf-8", newline="\r\n")


def write_readme(path: Path, xml_name: str) -> None:
    text = f"""# {VALUE} OrCAD / Allegro 库

按 `ast2400lib` 的目录和生成方式制作，目标为 Cadence 17.2。

- 完整料号：`{PART}`
- 原理图符号：单页，28 个物理引脚
- PCB 封装：`{FP_NAME}`
- 封装：PQFN24 4.00×5.00×0.75 mm，0.50 mm pitch，CASE 483BV
- 数据来源：`NCP303345-D.PDF` 第 3 页和第 22 页（98AON13704G）

## Capture 导入

在 OrCAD Capture CIS 17.2 中选择 `File -> Import -> Library XML`，导入：

`OrcadCaptureXML\\{xml_name}`

然后另存为 `NCP303345.OLB`。

## Allegro 封装生成

双击 `AllegroV17_2\\{FP_NAME}.bat`。脚本生成 `.pad/.dra/.psm`，并复制到
`01Pad_lib` 和 `01Psm_lib`。

## 重要复核

- Pin 28 已使用独立 Allegro Shape Symbol 实现规格书中的台阶异形焊盘。
- 外围焊盘、Pin 25/26/27 的位置和尺寸已按推荐 mounting footprint 录入。
- 大裸露焊盘膏层按线性 80% 缩放；实际钢网开窗必须由贴片厂复核。
- PGND 裸露焊盘应布置多颗散热过孔，且不要使用 thermal relief。
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def write_checklist(path: Path) -> None:
    lines = [
        f"{PART} pin checklist",
        f"Footprint: {FP_NAME}",
        "Source: NCP303345/D Rev.2 p.3; CASE 483BV Issue D p.22",
        "",
    ]
    for pin in PINS:
        lines.append(
            f"{int(pin['PinNumber']):>2}  {pin['PinName']:<10} "
            f"{pin['Electrical']:<7}  {pin['Description']}"
        )
    lines.extend(["", "Same-net groups:", "  PGND: 6,7,13,14,25,28",
                  "  SW:   8,9,10,11,12", "  VIN:  15,16,17,26", "  GL:   5,27"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)


def validate(by_num: dict[str, dict[str, str]], xml_path: Path) -> None:
    assert len(PINS) == len(by_num) == 28
    assert set(by_num) == {str(i) for i in range(1, 29)}
    assert set(LEFT + RIGHT) == set(by_num) and len(LEFT + RIGHT) == 28
    assert len(footprint_pins()) == 28
    assert [row[0] for row in footprint_pins()] == list(range(1, 29))
    assert [by_num[n]["PinName"] for n in ("6", "7", "13", "14", "25", "28")] == ["PGND"] * 6
    assert [by_num[n]["PinName"] for n in ("8", "9", "10", "11", "12")] == ["SW"] * 5
    assert [by_num[n]["PinName"] for n in ("15", "16", "17", "26")] == ["VIN"] * 4
    assert [by_num[n]["PinName"] for n in ("5", "27")] == ["GL"] * 2
    root = ET.parse(xml_path).getroot()
    assert len(root.findall(".//SymbolPinScalar")) == 28
    assert len(root.findall(".//PinNumber")) == 28
    assert len(root.findall(".//LibPart")) == 1


def main() -> None:
    by_num = {pin["PinNumber"]: pin for pin in PINS}
    alg = OUT / "AllegroV17_2"
    cap = OUT / "OrcadCaptureXML"
    archive_product = ARCHIVE / "01_成品库_ul_NCP303345"
    archive_script = ARCHIVE / "02_生成脚本_ncp303345_lib"
    archive_capture = ARCHIVE / "03_captureLib_NCP303345"
    archive_files = ARCHIVE / "04_script_file_NCP303345"
    for directory in (
        alg, cap, archive_product / "AllegroV17_2",
        archive_product / "OrcadCaptureXML", archive_script,
        archive_capture / "AllegroV17_2", archive_capture / "OrcadCaptureXML",
        archive_files, CAPTURE_OUT / "AllegroV17_2",
        CAPTURE_OUT / "OrcadCaptureXML", SCRIPT_OUT, AI_OUT,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    xml_name = f"{STAMP}.xml"
    xml_path = cap / xml_name
    write_capture_xml(by_num, xml_path)
    for name, (width, height, paste_scale) in PAD_SPECS.items():
        if name == PAD_28:
            write_shape_pxml(alg / f"{name}.pxml")
        else:
            write_pxml(alg / f"{name}.pxml", name, width, height, paste_scale)
    shape_scr = alg / f"{SHAPE_28}.scr"
    write_shape_scr(shape_scr)
    scr = alg / f"{FP_NAME}.scr"
    bat = alg / f"{FP_NAME}.bat"
    write_allegro_scr(scr)
    write_bat(bat)
    validate(by_num, xml_path)

    csv_path = OUT / f"{VALUE}_pins.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["PinNumber", "PinName", "Electrical", "Description"])
        writer.writeheader()
        writer.writerows(PINS)

    checklist = OUT / f"{VALUE}_pin_checklist.txt"
    write_checklist(checklist)
    readme = OUT / "README_CN.md"
    write_readme(readme, xml_name)

    for destination in (
        archive_product / "OrcadCaptureXML" / xml_name,
        archive_capture / "OrcadCaptureXML" / xml_name,
        CAPTURE_OUT / "OrcadCaptureXML" / xml_name,
    ):
        copy_file(xml_path, destination)

    generated = [scr, bat, shape_scr] + [alg / f"{name}.pxml" for name in PAD_SPECS]
    for source in generated:
        for folder in (
            archive_product / "AllegroV17_2", archive_capture / "AllegroV17_2",
            archive_files, CAPTURE_OUT / "AllegroV17_2", SCRIPT_OUT,
        ):
            copy_file(source, folder / source.name)

    for folder in (archive_product, archive_capture, CAPTURE_OUT, AI_OUT, SCRIPT_OUT):
        copy_file(csv_path, folder / csv_path.name)
        copy_file(checklist, folder / checklist.name)
        write_readme(folder / "README_CN.md", xml_name)
    copy_file(Path(__file__), AI_OUT / Path(__file__).name)
    copy_file(Path(__file__), archive_script / Path(__file__).name)
    write_readme(archive_product / "README_CN.md", xml_name)

    print("OK pins=28 symbol=1 footprint_pads=28")
    print("Capture XML:", xml_path)
    print("Allegro BAT:", bat)
    print("Pin 28: stepped custom shape")


if __name__ == "__main__":
    main()
