# -*- coding: utf-8 -*-
"""HPM5361ICF1: OrCAD Capture symbol + Allegro LQFP64 10x10 footprint (IEG1-style flow).

Sources:
  - Official: HPM5300 series, HPM5361ICF1 = LQFP-64 10x10 mm P0.5
  - Pinout: AUTOlib/HPM_LIB_20251229/HPM_symbols/HPM5300_Library.kicad_sym
  - Land: HPM_footprints.pretty/LQFP-64_10x10mm_P0.5mm.kicad_mod
  - Process: 01AIcadence/hpm5361ieg1_lib (single page, full pinmux on pin name)
"""
from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(r"D:\001DIY\005lib")
PART = "HPM5361ICF1"
FP_NAME = "LQFP64_10X10_P0D5"
PAD_H = "r155_30"    # 1.55 x 0.30 mm, left/right
PAD_V = "r30_155"    # 0.30 x 1.55 mm, top/bottom
PIN_COUNT = 64

STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
ALLEGRO_BIN = Path(r"C:\Program0\Cadence\spb172\tools\bin")
PAD_LIB = ROOT / "01Pad_lib"
PSM_LIB = ROOT / "01Psm_lib"
KICAD_SYM = ROOT / "AUTOlib" / "HPM_LIB_20251229" / "HPM_symbols" / "HPM5300_Library.kicad_sym"

OUT = ROOT / "AUTOlib" / "ul_HPM5361ICF1"
ARCHIVE = ROOT / "AUTOlib" / "5361ICF1"
CAPTURE_OUT = ROOT / "01captureLib" / "HPM5361ICF1"
SCRIPT_DIR = ROOT / "01script_file" / "HPM5361ICF1"
AI_DIR = ROOT / "01AIcadence" / "hpm5361icf1_lib"
DOC_DIR = ROOT / "01captureLib" / "5361ICF1"

ELEC_CODE = {
    "Input": 0, "Bidirectional": 1, "Output": 2,
    "Passive": 4, "NC": 4, "Power": 7,
}

ELEC_FROM_KICAD = {
    "input": "Input",
    "output": "Output",
    "bidirectional": "Bidirectional",
    "passive": "Bidirectional",
    "power_in": "Power",
    "power_out": "Power",
    "tri_state": "Bidirectional",
    "unspecified": "Passive",
}

# Extra tags appended to mux (same style as IEG1 / official KiCad labels)
MUX_TAG = {
    "10": "BOOT1",
    "11": "BOOT0",
    "15": "ISP_UART_RX",
    "16": "ISP_UART_TX",
    "56": "USB_DM",
    "57": "USB_DP",
}

# Power pins that KiCad marked incorrectly (e.g. pin 59 VSS as bidirectional)
FORCE_ELEC = {
    "59": "Power",
}


def parse_official_pins() -> list[dict]:
    text = KICAD_SYM.read_text(encoding="utf-8")
    start = text.find('(symbol "HPM5361ICF1"')
    if start < 0:
        raise RuntimeError("HPM5361ICF1 symbol not found in official KiCad library")
    nxt = text.find('\n  (symbol "', start + 10)
    block = text[start: nxt if nxt > 0 else None]
    pin_re = re.compile(
        r'\(pin\s+(\S+)\s+\S+[^\n]*\n'
        r'\s+\(name\s+"([^"]*)"[^\n]*\n'
        r'\s+\(number\s+"(\d+)"'
    )
    by_num: dict[str, dict] = {}
    for typ, name, num in pin_re.findall(block):
        elec = FORCE_ELEC.get(num, ELEC_FROM_KICAD.get(typ, "Passive"))
        by_num[num] = {
            "PinNumber": num,
            "PinName": name.split("/")[0],
            "Electrical": elec,
            "Pinmux": name,
        }
    missing = [str(i) for i in range(1, PIN_COUNT + 1) if str(i) not in by_num]
    if missing:
        raise RuntimeError(f"parsed={sorted(by_num, key=int)} missing={missing}")
    return [by_num[str(i)] for i in range(1, PIN_COUNT + 1)]


def symbol_name(p: dict) -> str:
    """Full peripheral list as pin name; strip English notes."""
    main = p["Pinmux"].split("  ")[0].strip()
    tag = MUX_TAG.get(p["PinNumber"])
    if tag and tag not in main.split("/"):
        return f"{main}/{tag}"
    return main


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


def make_libpart(by_num: dict[str, dict]) -> str:
    names = {n: symbol_name(by_num[n]) for n in (str(i) for i in range(1, PIN_COUNT + 1))}
    max_len = max(len(s) for s in names.values())
    # Capture font width ~5; keep on GRID=10. Pins left, full mux name to the right.
    body_w = max(400, ((max_len * 5 + 40 + 9) // 10) * 10)
    y0 = 20
    pin_pitch = 10
    pin_blocks: list[str] = []
    maps: list[tuple[str, int]] = []
    for i in range(1, PIN_COUNT + 1):
        n = str(i)
        p = by_num[n]
        yy = y0 + (i - 1) * pin_pitch
        pin_blocks.append(pin_xml(names[n], i - 1, p["Electrical"], True, yy, body_w))
        maps.append((n, i - 1))

    bbox_y2 = y0 + PIN_COUNT * pin_pitch
    pinnums = "".join(
        f'        <PinNumber><Defn number="{escape(n)}" position="{p}"/></PinNumber>\n'
        for n, p in maps
    )
    return f"""    <LibPart>
      <Defn/>
      <NormalView>
        <Defn suffix="Normal"/>
        <SymbolDisplayProp>
          <Defn locX="20" locY="-30" name="Part Reference" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolDisplayProp>
          <Defn locX="20" locY="-20" name="Value" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolUserProp><Defn name="Description" val="HPMicro HPM5361ICF1 LQFP64 (1 page, pin left, full mux right)"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="{PART}"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="HPMicro"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Package" val="LQFP-64 10x10mm P0.5"/></SymbolUserProp>
        <SymbolColor><Defn val="48"/></SymbolColor>
        <SymbolBBox><Defn x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></SymbolBBox>
        <IsPinNumbersVisible><Defn val="1"/></IsPinNumbersVisible>
        <IsPinNamesRotated><Defn val="0"/></IsPinNamesRotated>
        <IsPinNamesVisible><Defn val="1"/></IsPinNamesVisible>
        <ContentsLibName><Defn name=""/></ContentsLibName>
        <ContentsViewName><Defn name="{PART}"/></ContentsViewName>
        <ContentsViewType><Defn type="0"/></ContentsViewType>
        <PartValue><Defn name="{PART}"/></PartValue>
        <Reference><Defn name="U"/></Reference>
        <Rect><Defn fillStyle="1" hatchStyle="0" lineStyle="0" lineWidth="3" x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></Rect>
{"".join(pin_blocks)}      </NormalView>
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


def lqfp_pin_xy_mm(num: int) -> tuple[float, float, str]:
    """Datasheet top view, pin1 top-left, CCW. Y+ up.

    Official HPM5300 LQFP64: pin1 = PA08 at left-top, then down the left side.
    Land from official KiCad LQFP-64_10x10mm_P0.5mm (pad 1.55x0.30, center 5.675).
    """
    pitch = 0.5
    span = 3.75
    radial = 5.675
    if 1 <= num <= 16:
        return -radial, span - (num - 1) * pitch, PAD_H
    if 17 <= num <= 32:
        return -span + (num - 17) * pitch, -radial, PAD_V
    if 33 <= num <= 48:
        return radial, -span + (num - 33) * pitch, PAD_H
    if 49 <= num <= 64:
        return span - (num - 49) * pitch, radial, PAD_V
    raise ValueError(num)


def write_pxml(path: Path, name: str, w_mm: float, h_mm: float, mask_scale: float = 1.15) -> None:
    w = mm_to_mil(w_mm)
    h = mm_to_mil(h_mm)
    mw, mh = w * mask_scale, h * mask_scale
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
    <width>{w:.2f}</width>
    <height>{h:.2f}</height>
  </pad>
</padstack>
"""
    path.write_text(text, encoding="ascii", newline="\n")


def write_allegro_scr(path: Path) -> None:
    lines = [
        f"# Auto-generated {PART} {FP_NAME} from official HPM LQFP64 land",
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
        "FORM prmedit width 20",
        "FORM prmedit height 20",
        "FORM prmedit Apply",
        "FORM prmedit x -10",
        "FORM prmedit y -10",
        "FORM prmedit done",
        "setwindow pcb",
    ]
    for n in range(1, PIN_COUNT + 1):
        x, y, pad = lqfp_pin_xy_mm(n)
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
                f"FORM mini offsetx {x:.4f}",
                f"FORM mini offsety {y:.4f}",
                "setwindow pcb",
                "pick 0 0",
                "done",
            ]
        )

    # silk 10x10 corners + pin1 tick at top-left
    lines.extend(
        [
            "add line",
            "setwindow Form.mini",
            "FORM mini lock_direction Off",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick -5.11 4.16",
            "pick -5.11 5.11",
            "pick -4.16 5.11",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick 4.16 5.11",
            "pick 5.11 5.11",
            "pick 5.11 4.16",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick 5.11 -4.16",
            "pick 5.11 -5.11",
            "pick 4.16 -5.11",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.12",
            "setwindow pcb",
            "pick -4.16 -5.11",
            "pick -5.11 -5.11",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass SILKSCREEN_TOP",
            "FORM mini line_width 0.15",
            "setwindow pcb",
            "pick -6.45 4.16",
            "pick -5.11 4.16",
            "done",
            "add line",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass ASSEMBLY_TOP",
            "FORM mini line_width 0.10",
            "setwindow pcb",
            "pick -5.0 4.0",
            "pick -4.0 5.0",
            "pick 5.0 5.0",
            "pick 5.0 -5.0",
            "pick -5.0 -5.0",
            "pick -5.0 4.0",
            "done",
            "shape add",
            "setwindow Form.mini",
            "FORM mini class PACKAGE GEOMETRY",
            "FORM mini subclass PLACE_BOUND_TOP",
            "FORM mini dyns_fill_type Static solid",
            "FORM mini dyns_grid None",
            "FORM mini dyns_lock_mode Line",
            "setwindow pcb",
            "pick -6.70 -6.70",
            "pick 6.70 -6.70",
            "pick 6.70 6.70",
            "pick -6.70 6.70",
            "pick -6.70 -6.70",
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
            "pick 0 6.4",
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
for %%P in ({PAD_H} {PAD_V}) do (
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
for %%P in ({PAD_H} {PAD_V}) do (
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
        f"{PART} pin checklist  LQFP64 10x10 P0.5  footprint={FP_NAME}",
        "Symbol: SINGLE PAGE, pin number LEFT, full mux name RIGHT, 1..64.",
        "ICF1: DCDC_IN / DCDC_LP / DCDC_GND / VPMC are separate pins (not shared like IEG1).",
        "PA00=ISP_UART_TX  PA01=ISP_UART_RX  PA02=BOOT0  PA03=BOOT1  PA24=USB_DP  PA25=USB_DM",
        "",
    ]
    for i in range(1, PIN_COUNT + 1):
        n = str(i)
        lines.append(f"  {n:>3}  {symbol_name(by_num[n])}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readme(path: Path, xml_name: str) -> None:
    text = f"""# {PART} = 先楫 HPM5300 LQFP64

按 `5361IEG1` / `ast2400lib` 同款流程生成，目标 **Cadence 17.2**。

| 项目 | 值 |
|------|----|
| 型号 | {PART} |
| 封装 | **LQFP-64 10×10 mm，P0.5 mm** |
| 引脚 | **64**（无 EP） |
| PCB Footprint | `{FP_NAME}` |
| 符号 | **单页**；引脚在左，完整外设复用名在右 |
| 焊盘 | `{PAD_H}` 1.55×0.30、`{PAD_V}` 0.30×1.55 |

引脚来源：先楫官方 KiCad `HPM5300_Library.kicad_sym`（HPM5361ICF1）。  
焊盘来源：官方 `LQFP-64_10x10mm_P0.5mm.kicad_mod`。  
坐标系：数据手册顶视，**1 脚左上，逆时针**。

## Capture 导入

1. OrCAD Capture CIS 17.2 → `File` → `Import` → `Library XML`
2. 选择 `OrcadCaptureXML\\{xml_name}`
3. 另存为 `01captureLib\\{PART}.OLB`
4. 放置 `{PART}`（单页，全部 64 脚，不分立）

## Allegro 封装生成

双击：

`AUTOlib\\ul_HPM5361ICF1\\AllegroV17_2\\{FP_NAME}.bat`

会调用 `padstack_editor -x` 生成 `.pad`，再 `allegro -nograph -s` 生成 `.dra/.psm`，并复制到 `01Pad_lib` / `01Psm_lib`。

## 电源注意（ICF1）

- `DCDC_IN`(21) / `DCDC_LP`(20) / `DCDC_GND`(19) / `VPMC`(22) **各自独立**（与 IEG1 的 VPMC=DCDC_IN 内部共用不同）
- `DCDC_LP` 若软件关 DCDC：**悬空，禁止接地**
- 多个 `VSS` / `VDD_SOC` / `VIO_B00` 同名 Power，Capture 会自动短接
- `PA00` = ISP_UART_TX，`PA01` = ISP_UART_RX
- `PA02` = BOOT0，`PA03` = BOOT1
- `PA24` = USB_DP，`PA25` = USB_DM
"""
    path.write_text(text, encoding="utf-8")


def write_doc_md(path: Path, xml_name: str) -> None:
    text = f"""# HPM5361ICF1 原理图库 / PCB 封装库

按 `5361IEG1` 同款历程生成：解析官方引脚 → Capture XML → padstack pxml → Allegro `.dra/.psm`。

与 IEG1 的关键差异：

| 项目 | IEG1 | ICF1 |
|------|------|------|
| 封装 | QFN48_EP 6×6 P0.4 | **LQFP-64 10×10 P0.5** |
| 引脚 | 48+EP=49 | **64（无 EP）** |
| 符号 | 可四分符 | **单页，不分立** |
| 引脚名 | 完整 pinmux | **完整 pinmux + BOOT/ISP/USB 标注** |
| DCDC | VPMC 与 DCDC_IN 内部共用 | **DCDC_IN / LP / GND / VPMC 独立** |

## 器件

| 项目 | 值 |
|------|----|
| 型号 | **HPM5361ICF1**（先楫 HPM5300） |
| 封装 | **LQFP-64** 10×10 mm，P0.5 mm |
| 引脚 | **64** |
| PCB Footprint | `{FP_NAME}` |
| 符号 | 单页；引脚号在左，完整复用功能在右 |

引脚来源：先楫官方 KiCad `HPM_LIB_20251229/HPM_symbols/HPM5300_Library.kicad_sym`。  
焊盘来源：官方 `LQFP-64_10x10mm_P0.5mm.kicad_mod`。  
1 脚：数据手册顶视 **左上，逆时针**。

## 目录（对照 5361IEG1）

| 本目录 | 对应 IEG1 | 内容 |
|--------|-----------|------|
| `01_成品库_ul_HPM5361ICF1` | `01_成品库_ul_HPM5361IEG1` | Capture XML + Allegro 成品 |
| `02_生成脚本_hpm5361icf1_lib` | `02_生成脚本_hpm5361ieg1_lib` | `gen_ul_hpm5361icf1.py` |
| `03_captureLib_HPM5361ICF1` | `03_captureLib_HPM5361IEG1` | 原理图库源 / 核对清单 |
| `04_script_file_HPM5361ICF1` | `04_script_file_HPM5361IEG1` | `.bat/.scr/.pad/.dra/.psm` |

工作副本：

- `AUTOlib\\ul_HPM5361ICF1\\`
- `01captureLib\\HPM5361ICF1\\`
- `01AIcadence\\hpm5361icf1_lib\\`
- `01script_file\\HPM5361ICF1\\`

## 生成步骤

1. **解析引脚**：官方符号 4 个 unit → 64 脚主键名 + 完整 pinmux，合并到单页
2. **Capture XML**：同构 1 页，`File → Import → Library XML`
3. **焊盘 pxml**：`{PAD_H}` / `{PAD_V}`，`padstack_editor -x`
4. **封装脚本**：`allegro -nograph -s {FP_NAME}.scr`
5. **入库**：`.pad` → `01Pad_lib`，`.dra/.psm` → `01Psm_lib`

重新生成：

```bat
python 01captureLib\\5361ICF1\\02_生成脚本_hpm5361icf1_lib\\gen_ul_hpm5361icf1.py
AUTOlib\\ul_HPM5361ICF1\\AllegroV17_2\\{FP_NAME}.bat
```

## Capture 导入

1. OrCAD Capture CIS 17.2 → `File` → `Import` → `Library XML`
2. 选 `ul_HPM5361ICF1\\OrcadCaptureXML\\{xml_name}`
3. 另存为 `01captureLib\\HPM5361ICF1.OLB`
4. 放置 **HPM5361ICF1**（单页，全部 64 脚）

## 电源注意（ICF1）

- `DCDC_IN`(21) / `DCDC_LP`(20) / `DCDC_GND`(19) / `VPMC`(22) **各自独立**
- `DCDC_LP` 若软件关 DCDC：**悬空，禁止接地**
- 多个 `VSS` / `VDD_SOC` / `VIO_B00` 同名 Power，Capture 会自动短接
- `PA00` = ISP_UART_TX，`PA01` = ISP_UART_RX
- `PA02` = BOOT0，`PA03` = BOOT1
- `PA24` = USB_DP，`PA25` = USB_DM
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
<p>Part {PART} is homogeneous: all 64 pins on one page, full pinmux visible.</p>
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
<p>Footprint: {FP_NAME} (LQFP64 10x10 P0.5)</p>
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
    pins = parse_official_pins()
    by_num = {p["PinNumber"]: p for p in pins}
    assert len(by_num) == PIN_COUNT, len(by_num)
    assert [p["PinNumber"] for p in pins] == [str(i) for i in range(1, PIN_COUNT + 1)]

    alg_dir = OUT / "AllegroV17_2"
    cap_dir = OUT / "OrcadCaptureXML"
    arch_alg = ARCHIVE / "01_成品库_ul_HPM5361ICF1" / "AllegroV17_2"
    arch_cap = ARCHIVE / "01_成品库_ul_HPM5361ICF1" / "OrcadCaptureXML"
    arch_fin = ARCHIVE / "01_成品库_ul_HPM5361ICF1"
    dests = [
        alg_dir, cap_dir, arch_alg, arch_cap,
        CAPTURE_OUT, CAPTURE_OUT / "OrcadCaptureXML", CAPTURE_OUT / "AllegroV17_2",
        SCRIPT_DIR, AI_DIR, PAD_LIB, PSM_LIB,
        ARCHIVE / "02_生成脚本_hpm5361icf1_lib",
        ARCHIVE / "03_captureLib_HPM5361ICF1" / "OrcadCaptureXML",
        ARCHIVE / "03_captureLib_HPM5361ICF1" / "AllegroV17_2",
        ARCHIVE / "04_script_file_HPM5361ICF1",
        DOC_DIR / "AllegroV17_2",
        DOC_DIR / "01_成品库_ul_HPM5361ICF1" / "OrcadCaptureXML",
        DOC_DIR / "01_成品库_ul_HPM5361ICF1" / "AllegroV17_2",
        DOC_DIR / "03_captureLib_HPM5361ICF1" / "OrcadCaptureXML",
        DOC_DIR / "03_captureLib_HPM5361ICF1" / "AllegroV17_2",
        DOC_DIR / "04_script_file_HPM5361ICF1",
    ]
    for d in dests:
        d.mkdir(parents=True, exist_ok=True)

    xml_name = f"{STAMP}.xml"
    cap_xml = cap_dir / xml_name
    write_capture_xml(by_num, cap_xml)

    write_pxml(alg_dir / f"{PAD_H}.pxml", PAD_H, 1.55, 0.30)
    write_pxml(alg_dir / f"{PAD_V}.pxml", PAD_V, 0.30, 1.55)

    scr = alg_dir / f"{FP_NAME}.scr"
    write_allegro_scr(scr)
    bat = alg_dir / f"{FP_NAME}.bat"
    write_bat(bat)

    fields = ["PinNumber", "PinName", "Electrical", "Pinmux"]
    csv_rows = [by_num[str(n)] for n in range(1, PIN_COUNT + 1)]

    def dump_csv(dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(csv_rows)

    write_guides(OUT, xml_name)
    write_readme(OUT / "README_CN.md", xml_name)
    write_readme(CAPTURE_OUT / "README_CN.md", xml_name)
    write_readme(arch_fin / "README_CN.md", xml_name)
    write_doc_md(DOC_DIR / "5361ICF1.md", xml_name)
    write_checklist(by_num, CAPTURE_OUT / f"{PART}_pin_checklist.txt")
    write_checklist(by_num, SCRIPT_DIR / f"{PART}_pin_checklist.txt")
    write_checklist(by_num, ARCHIVE / "03_captureLib_HPM5361ICF1" / f"{PART}_pin_checklist.txt")
    write_checklist(by_num, DOC_DIR / "03_captureLib_HPM5361ICF1" / f"{PART}_pin_checklist.txt")

    for dest in (
        OUT, CAPTURE_OUT, AI_DIR, SCRIPT_DIR, arch_fin,
        ARCHIVE / "03_captureLib_HPM5361ICF1",
        DOC_DIR / "03_captureLib_HPM5361ICF1",
    ):
        dump_csv(dest / f"{PART}_pins.csv")

    xml_copies = [
        CAPTURE_OUT / "OrcadCaptureXML" / xml_name,
        arch_cap / xml_name,
        ARCHIVE / "03_captureLib_HPM5361ICF1" / "OrcadCaptureXML" / xml_name,
        DOC_DIR / "01_成品库_ul_HPM5361ICF1" / "OrcadCaptureXML" / xml_name,
        DOC_DIR / "03_captureLib_HPM5361ICF1" / "OrcadCaptureXML" / xml_name,
    ]
    for d in xml_copies:
        copy_into(cap_xml, d)

    for src in (scr, bat, alg_dir / f"{PAD_H}.pxml", alg_dir / f"{PAD_V}.pxml"):
        for folder in (
            CAPTURE_OUT / "AllegroV17_2",
            SCRIPT_DIR,
            arch_alg,
            ARCHIVE / "03_captureLib_HPM5361ICF1" / "AllegroV17_2",
            ARCHIVE / "04_script_file_HPM5361ICF1",
            DOC_DIR / "AllegroV17_2",
            DOC_DIR / "01_成品库_ul_HPM5361ICF1" / "AllegroV17_2",
            DOC_DIR / "03_captureLib_HPM5361ICF1" / "AllegroV17_2",
            DOC_DIR / "04_script_file_HPM5361ICF1",
        ):
            copy_into(src, folder / src.name)

    this = Path(__file__).resolve()
    copy_into(this, AI_DIR / this.name)
    copy_into(this, ARCHIVE / "02_生成脚本_hpm5361icf1_lib" / this.name)
    copy_into(this, DOC_DIR / "02_生成脚本_hpm5361icf1_lib" / this.name)
    readme_lib = f"""# {PART} OrCAD / Allegro library

- Datasheet family: HPM5300
- Package: LQFP-64 10x10 mm P0.5
- Pins: 64
- Footprint: {FP_NAME}
- Symbol: single page, all 64 pins, full pinmux on each pin
- Run: python gen_ul_hpm5361icf1.py
- Then: {FP_NAME}.bat
"""
    (AI_DIR / f"{PART}_library_readme.md").write_text(readme_lib, encoding="utf-8")
    (ARCHIVE / "02_生成脚本_hpm5361icf1_lib" / f"{PART}_library_readme.md").write_text(readme_lib, encoding="utf-8")
    (DOC_DIR / "02_生成脚本_hpm5361icf1_lib" / f"{PART}_library_readme.md").write_text(readme_lib, encoding="utf-8")

    print(f"pins={len(by_num)}")
    print("OK capture", cap_xml)
    print("OK footprint bat", bat)
    print()
    print("Next:")
    print(f"  1) Capture Import XML: {cap_xml}")
    print(f"  2) Double-click: {bat}")


if __name__ == "__main__":
    main()
