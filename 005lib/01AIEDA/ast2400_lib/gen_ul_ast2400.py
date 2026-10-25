# -*- coding: utf-8 -*-
"""Generate Ultra-Librarian-style AST2400 library package for Cadence 17.2."""
from __future__ import annotations

import csv
import math
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(r"D:\001DIY\005lib")
CSV_PATH = ROOT / "01captureLib" / "AST2400" / "AST2400_pins.csv"
UL_BUILDER = ROOT / "AUTOlib" / "ul_TPS65217CRSLR" / "AllegroV17_2" / "builder.ile"
OUT = ROOT / "AUTOlib" / "ul_AST2400"
STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Package: 19x19mm LFBGA, 0.8mm pitch, 22x22 array (depopulated to 408)
BODY_MM = 19.0
PITCH_MM = 0.8
PAD_MM = 0.40  # NSMD land approx
MASK_MM = 0.50
ROWS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
]
# Capture electrical type codes (UL/OrCAD XML)
ELEC_CODE = {
    "Input": 0,
    "Bidirectional": 1,
    "Output": 2,
    "Passive": 4,
    "NC": 4,
    "Power": 7,
}
SECTION_ORDER = [
    "A_POWER",
    "B_DDR",
    "C_PCIE_VGA",
    "D_MAC",
    "E_FLASH_SPI",
    "F_UART_I2C_JTAG",
    "G_USB_ADC_MISC",
    "H_GPIO_SD_PWM",
]
SECTION_LETTER = {s: chr(ord("A") + i) for i, s in enumerate(SECTION_ORDER)}
FP_NAME = "LFBGA408_19X19"


def mm_to_mil(mm: float) -> float:
    return mm / 0.0254


def ball_xy_mil(ball: str) -> tuple[float, float]:
    m = __import__("re").match(r"^([A-Z]+)(\d+)$", ball)
    row, col = m.group(1), int(m.group(2))
    ri = ROWS.index(row)
    # A1 top-left (datasheet left=col1, top=A)
    x = (col - 11.5) * mm_to_mil(PITCH_MM)
    y = (10.5 - ri) * mm_to_mil(PITCH_MM)
    return x, y


def load_pins() -> list[dict]:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8-sig")))
    # uniquify non-power duplicate names within each section
    for sec in SECTION_ORDER:
        subset = [r for r in rows if r["PartSection"] == sec]
        seen: dict[str, int] = {}
        for r in subset:
            name = r["PinName"]
            if r["Electrical"] == "Power":
                continue
            seen[name] = seen.get(name, 0) + 1
            if seen[name] > 1:
                r["PinName"] = f"{name}_{seen[name]}"
    return rows


def pin_xml(name: str, position: int, elec: str, left: bool, y: int) -> str:
    typ = ELEC_CODE.get(elec, 4)
    if left:
        hotpt_x, start_x = -30, 0
    else:
        hotpt_x, start_x = 210, 180
    # left-pointing when pin is on right side of box
    left_pt = 0 if left else 1
    right_pt = 1 if left else 0
    return f"""        <SymbolPinScalar>
          <Defn hotptX="{hotpt_x}" hotptY="{y}" name="{escape(name)}" position="{position}" startX="{start_x}" startY="{y}" type="{typ}" visible="1"/>
          <IsLong>
            <Defn val="1"/>
          </IsLong>
          <IsClock>
            <Defn val="0"/>
          </IsClock>
          <IsDot>
            <Defn val="0"/>
          </IsDot>
          <IsLeftPointing>
            <Defn val="{left_pt}"/>
          </IsLeftPointing>
          <IsRightPointing>
            <Defn val="{right_pt}"/>
          </IsRightPointing>
          <IsNetStyle>
            <Defn val="0"/>
          </IsNetStyle>
          <IsNoConnect>
            <Defn val="0"/>
          </IsNoConnect>
          <IsGlobal>
            <Defn val="0"/>
          </IsGlobal>
          <IsNumberVisible>
            <Defn val="1"/>
          </IsNumberVisible>
        </SymbolPinScalar>
"""


def make_libpart(sec: str, pins: list[dict], letter: str) -> str:
    # layout: left and right columns
    left = [p for p in pins if p["Side"] == "Left"]
    right = [p for p in pins if p["Side"] != "Left"]
    # rebalance if skewed
    if abs(len(left) - len(right)) > len(pins) // 3:
        left, right = [], []
        for i, p in enumerate(pins):
            (left if i % 2 == 0 else right).append(p)

    n = max(len(left), len(right), 1)
    body_h = max(40, 10 + n * 10)
    body_w = 180
    y0 = 20

    # assign visual order: left top->bottom then right top->bottom
    ordered: list[tuple[dict, bool, int]] = []
    for i, p in enumerate(left):
        ordered.append((p, True, y0 + i * 10))
    for i, p in enumerate(right):
        ordered.append((p, False, y0 + i * 10))

    # rebuild with sequential position index
    pin_blocks = []
    pos_map = []  # (ball, position)
    for idx, (p, is_left, y) in enumerate(ordered):
        pin_blocks.append(pin_xml(p["PinName"], idx, p["Electrical"], is_left, y))
        pos_map.append((p["PinNumber"], idx))

    bbox_y2 = y0 + n * 10 + 10
    suffix = f"{letter}.Normal"
    pins_xml = "".join(pin_blocks)
    pinnums = "".join(
        f"""        <PinNumber>
          <Defn number="{escape(ball)}" position="{pos}"/>
        </PinNumber>
"""
        for ball, pos in pos_map
    )

    return f"""    <LibPart>
      <Defn/>
      <NormalView>
        <Defn suffix="{suffix}"/>
        <SymbolDisplayProp>
          <Defn locX="90" locY="-30" name="Part Reference" rotation="0" textJustification="0"/>
          <PropFont>
            <Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/>
          </PropFont>
          <PropColor>
            <Defn val="48"/>
          </PropColor>
          <PropDispType>
            <Defn val="1"/>
          </PropDispType>
        </SymbolDisplayProp>
        <SymbolDisplayProp>
          <Defn locX="90" locY="-20" name="Value" rotation="0" textJustification="0"/>
          <PropFont>
            <Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/>
          </PropFont>
          <PropColor>
            <Defn val="48"/>
          </PropColor>
          <PropDispType>
            <Defn val="1"/>
          </PropDispType>
        </SymbolDisplayProp>
        <SymbolUserProp>
          <Defn name="Datasheet" val="AST2400 Datasheet V1.3"/>
        </SymbolUserProp>
        <SymbolUserProp>
          <Defn name="Description" val="ASPEED AST2400 BMC / PCIe VGA Processor ({sec})"/>
        </SymbolUserProp>
        <SymbolUserProp>
          <Defn name="Manufacturer_Part_Number" val="AST2400"/>
        </SymbolUserProp>
        <SymbolUserProp>
          <Defn name="Manufacturer_Name" val="ASPEED"/>
        </SymbolUserProp>
        <SymbolUserProp>
          <Defn name="Section" val="{sec}"/>
        </SymbolUserProp>
        <SymbolUserProp>
          <Defn name="Copyright" val="Generated for local Cadence 17.2 library (UL-compatible format)."/>
        </SymbolUserProp>
        <SymbolColor>
          <Defn val="48"/>
        </SymbolColor>
        <SymbolBBox>
          <Defn x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/>
        </SymbolBBox>
        <IsPinNumbersVisible>
          <Defn val="1"/>
        </IsPinNumbersVisible>
        <IsPinNamesRotated>
          <Defn val="1"/>
        </IsPinNamesRotated>
        <IsPinNamesVisible>
          <Defn val="1"/>
        </IsPinNamesVisible>
        <ContentsLibName>
          <Defn name=""/>
        </ContentsLibName>
        <ContentsViewName>
          <Defn name="AST2400"/>
        </ContentsViewName>
        <ContentsViewType>
          <Defn type="0"/>
        </ContentsViewType>
        <PartValue>
          <Defn name="AST2400"/>
        </PartValue>
        <Reference>
          <Defn name="U"/>
        </Reference>
        <Rect>
          <Defn fillStyle="1" hatchStyle="0" lineStyle="0" lineWidth="3" x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/>
        </Rect>
{pins_xml}      </NormalView>
      <PhysicalPart>
        <Defn/>
{pinnums}      </PhysicalPart>
    </LibPart>
"""


def write_capture_xml(pins: list[dict], path: Path) -> None:
    by = defaultdict(list)
    for p in pins:
        by[p["PartSection"]].append(p)

    parts = []
    for sec in SECTION_ORDER:
        letter = SECTION_LETTER[sec]
        # sort by Order
        sec_pins = sorted(by[sec], key=lambda r: int(r["Order"]))
        parts.append(make_libpart(sec, sec_pins, letter))

    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Lib xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="olb.xsd">
 
  <Defn name="AST2400.OLB"/>
 
  <Package>
    <Defn alphabeticNumbering="1" isHomogeneous="0" name="AST2400" pcbFootprint="{FP_NAME}" pcbLib="" refdesPrefix="U"/>
{"".join(parts)}  </Package>
 
</Lib>
"""
    path.write_text(xml, encoding="utf-8")


def write_footprint_xml(pins: list[dict], path: Path) -> None:
    pad = mm_to_mil(PAD_MM)
    mask = mm_to_mil(MASK_MM)
    body = mm_to_mil(BODY_MM)
    half = body / 2
    # courtyard +0.25mm
    cy = half + mm_to_mil(0.25)

    pin_lines = []
    for p in pins:
        x, y = ball_xy_mil(p["PinNumber"])
        pin_lines.append(
            f'    <Pin number="{p["PinNumber"]}" padName="c{int(round(pad))}" '
            f'originX="{x:.4f}" originY="{y:.4f}" rotation="0" isMechanical="no" textBlk="1" />'
        )

    # silk / assembly / courtyard rectangles
    def rect_path(layer: str, half_sz: float, lw: float = 5) -> str:
        pts = [
            (-half_sz, -half_sz),
            (-half_sz, half_sz),
            (half_sz, half_sz),
            (half_sz, -half_sz),
            (-half_sz, -half_sz),
        ]
        pts_xml = "\n".join(f'        <Point x="{x:.4f}" y="{y:.4f}" />' for x, y in pts)
        return f"""    <Layer name="{layer}" packageHeight="0" >
      <Path lineWidth="{lw}" type="open" >
{pts_xml}
      </Path>
    </Layer>
"""

    # pin 1 marker near A1
    a1x, a1y = ball_xy_mil("A1") if any(p["PinNumber"] == "A1" for p in pins) else (-half, half)
    marker = f"""    <Layer name="PACKAGE GEOMETRY/SILKSCREEN_TOP" packageHeight="0" >
      <Path lineWidth="0" type="shape" >
        <Point x="{a1x - 20:.4f}" y="{a1y + 20:.4f}" />
        <Point x="{a1x - 5:.4f}" y="{a1y + 20:.4f}" />
        <Point x="{a1x - 5:.4f}" y="{a1y + 5:.4f}" />
        <Point x="{a1x - 20:.4f}" y="{a1y + 5:.4f}" />
        <Point x="{a1x - 20:.4f}" y="{a1y + 20:.4f}" />
      </Path>
    </Layer>
"""

    xml = f"""<Footprint name="{FP_NAME}" >
  <Units type="mils" precision="3" />
  <Extents minX="{-cy-50:.4f}" minY="{-cy-50:.4f}" width="{2*cy+100:.4f}" height="{2*cy+100:.4f}" />
  <Padstack name="c{int(round(pad))}" type="single" > 
    <Layers>
      <Layer name="TOP" >
        <Pad shape="circle" width="{pad:.4f}" height="{pad:.4f}" /> 
      </Layer>
      <Layer name="PASTEMASK_TOP" >
        <Pad shape="circle" width="{pad:.4f}" height="{pad:.4f}" /> 
      </Layer>
      <Layer name="SOLDERMASK_TOP" >
        <Pad shape="circle" width="{mask:.4f}" height="{mask:.4f}" /> 
      </Layer>
    </Layers>
  </Padstack>

  <TextBlocks>
    <TextBlock name="17" width="6.25" height="25" lineSpacing="25" characterSpacing="6.25" /> 
  </TextBlocks>

  <Pins>
{chr(10).join(pin_lines)}
  </Pins>
  <Vias>
  </Vias>
  <Layers>
{rect_path("PACKAGE GEOMETRY/SILKSCREEN_TOP", half, 5)}{rect_path("PACKAGE GEOMETRY/ASSEMBLY_TOP", half, 1)}{rect_path("PACKAGE GEOMETRY/PLACE_BOUND_TOP", cy, 1)}{marker}    <Layer name="PACKAGE GEOMETRY/SILKSCREEN_TOP" packageHeight="0" >
      <Text locX="{-half:.4f}" locY="{half + 30:.4f}" textBlock="17" rotation="0" mirror="no" >REFDES</Text>
    </Layer>
    <Layer name="PACKAGE GEOMETRY/ASSEMBLY_TOP" packageHeight="0" >
      <Text locX="{-half:.4f}" locY="{-half - 40:.4f}" textBlock="17" rotation="0" mirror="no" >DEVICE</Text>
    </Layer>
  </Layers>
  <Heights>
  </Heights>
</Footprint>
"""
    path.write_text(xml, encoding="utf-8")


def write_device_txt(pins: list[dict], path: Path) -> None:
    balls = [p["PinNumber"] for p in pins]
    # wrap pin list
    chunks = []
    line = []
    for b in balls:
        line.append(b)
        if len(line) >= 12:
            chunks.append(" ".join(line))
            line = []
    if line:
        chunks.append(" ".join(line))
    pinorder = " ,\n     ".join(chunks)
    text = f"""(DEVICE AST2400)
 
PACKAGE {FP_NAME}
PINCOUNT {len(balls)}
PINORDER {FP_NAME} {pinorder}
FUNCTION G1 {FP_NAME} {pinorder}

END
"""
    path.write_text(text, encoding="utf-8")


def write_bat(path: Path) -> None:
    path.write_text(
        """pushd %~dp0
@echo off
setlocal ENABLEDELAYEDEXPANSION
Set scriptDir=%cd%
Set skillScriptPath=!scriptDir:\\=/!
@echo skill load "%skillScriptPath%/builder.ile" > builder.scr.txt
@echo skill changeWorkingDir "%skillScriptPath%" >> builder.scr.txt
for %%g in (*.xml) do (
@echo skill LB_createFootprint "%skillScriptPath%/%%g" >> builder.scr.txt
)
@echo exit >> builder.scr.txt
@echo Creating footprints..
START /W "" "allegro.exe" -s builder.scr.txt

exit
""",
        encoding="ascii",
    )


def write_guides(out: Path) -> None:
    (out / "ImportGuides.html").write_text(
        """<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
<h1>AST2400 UL-format import (Cadence 17.2)</h1>
<ul>
<li><a href="OrcadCaptureXML/ImportGuide.html">OrCAD Capture</a></li>
<li><a href="AllegroV17_2/ImportGuide.html">Allegro PCB Editor</a></li>
</ul>
<p>See README_CN.md for Chinese steps.</p>
</body></html>
""",
        encoding="utf-8",
    )
    (out / "OrcadCaptureXML" / "ImportGuide.html").write_text(
        """<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
<h2>Capture 17.2</h2>
<ol>
<li>Open OrCAD Capture CIS 17.2</li>
<li>File - Import - Library XML</li>
<li>Select the .xml in this folder</li>
<li>Save OLB to D:/001DIY/005lib/01captureLib/AST2400.OLB</li>
</ol>
<p>Part AST2400 is heterogeneous with 8 sections A..H.</p>
</body></html>
""",
        encoding="utf-8",
    )
    (out / "AllegroV17_2" / "ImportGuide.html").write_text(
        """<!DOCTYPE html><html><body style="font-family:sans-serif;padding:24px">
<h2>Allegro 17.2</h2>
<ol>
<li>Load Cadence 17.2 environment so allegro.exe is in PATH</li>
<li>Double-click the .bat in this folder</li>
<li>Copy generated .pad / .psm into 01Pad_lib / 01Psm_lib</li>
</ol>
<p>Footprint name: LFBGA408_19X19 (19mm body, 0.8mm pitch)</p>
</body></html>
""",
        encoding="utf-8",
    )


def write_readme(out: Path, n_pins: int) -> None:
    (out / "README_CN.md").write_text(
        f"""# AST2400 Ultra Librarian 兼容格式库

按 `ul_TPS65217CRSLR` 同款结构生成，目标 **Cadence 17.2**。

## 目录
- `OrcadCaptureXML/` — Capture 原理图符号 XML（异构 8 分符 A~H）
- `AllegroV17_2/` — Allegro 封装 XML + `builder.ile` + 生成 bat

## 器件
- 型号: AST2400
- 封装: {FP_NAME}（19×19 mm LFBGA，0.8 mm pitch，{n_pins} balls）
- 分符: A_POWER / B_DDR / C_PCIE_VGA / D_MAC / E_FLASH_SPI / F_UART_I2C_JTAG / G_USB_ADC_MISC / H_GPIO_SD_PWM

## Capture 导入
1. 打开 Capture 17.2
2. `File` → `Import` → `Library XML`
3. 选择 `OrcadCaptureXML/*AST2400*.xml`
4. 另存为 `D:\\001DIY\\005lib\\01captureLib\\AST2400.OLB`

## Allegro 封装生成
1. 先切换到 Cadence 17.2 环境（`allegro.exe` 可用）
2. 双击 `AllegroV17_2\\*.bat`
3. 把生成的 pad/psm 拷到 `01Pad_lib` / `01Psm_lib`

## 注意
- 封装焊盘按 0.40 mm land / 0.50 mm mask 估算，量产前请对照 ASPEED 封装图复核。
- 原理图电源脚同名（如多个 GND）会自动短接，符合 Capture 习惯。
- 本包无 STEP 3D（UL 付费包才带）；需要可后续补。
""",
        encoding="utf-8",
    )
    (out / "readme.txt").write_text(
        "AST2400 library in Ultra Librarian compatible format for Cadence 17.2.\n"
        "See README_CN.md\n",
        encoding="ascii",
    )


def main() -> None:
    pins = load_pins()
    assert len(pins) == 408, len(pins)

    cap_dir = OUT / "OrcadCaptureXML"
    alg_dir = OUT / "AllegroV17_2"
    cap_dir.mkdir(parents=True, exist_ok=True)
    alg_dir.mkdir(parents=True, exist_ok=True)

    write_capture_xml(pins, cap_dir / f"{STAMP}.xml")
    write_footprint_xml(pins, alg_dir / f"{FP_NAME}.xml")
    write_device_txt(pins, alg_dir / "AST2400.txt")
    write_bat(alg_dir / f"{STAMP}.bat")
    write_guides(OUT)
    write_readme(OUT, len(pins))

    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, alg_dir / "builder.ile")
    else:
        print("WARNING: builder.ile not found, copy from ul_TPS65217CRSLR manually")

    # also mirror pin CSV for reference
    shutil.copy2(CSV_PATH, OUT / "AST2400_pins.csv")

    print(f"OK -> {OUT}")
    print(f"  Capture XML: {cap_dir}")
    print(f"  Allegro: {alg_dir}")
    print(f"  pins={len(pins)} footprint={FP_NAME}")


if __name__ == "__main__":
    main()
