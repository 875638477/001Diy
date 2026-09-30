# -*- coding: utf-8 -*-
"""Regenerate AST2400 UL-format lib: unique pin names + functional layout."""
from __future__ import annotations

import csv
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(r"D:\001DIY\005lib")
CSV_CANDIDATES = [
    ROOT / "01AIcadence" / "ast2400_lib" / "AST2400_pins.csv",
    ROOT / "AUTOlib" / "ul_AST2400" / "AST2400_pins.csv",
    ROOT / "01script_file" / "AST2400" / "AST2400_pins.csv",
]
UL_BUILDER = ROOT / "AUTOlib" / "ul_TPS65217CRSLR" / "AllegroV17_2" / "builder.ile"
OUT = ROOT / "AUTOlib" / "ul_AST2400"
CAPTURE_OUT = ROOT / "01captureLib" / "AST2400"
STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

BODY_MM = 19.0
PITCH_MM = 0.8
PAD_MM = 0.40
MASK_MM = 0.50
ROWS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
]
ELEC_CODE = {
    "Input": 0,
    "Bidirectional": 1,
    "Output": 2,
    "Passive": 4,
    "NC": 4,
    "Power": 7,
}
# Match reference schematic functional blocks (hetero sections A..H)
SECTION_ORDER = [
    "A_PCIE",
    "B_DDR",
    "C_LPC_SPI",
    "D_MAC",
    "E_FLASH",
    "F_UART_I2C",
    "G_USB_ADC_MISC",
    "H_POWER",
]
SECTION_LETTER = {s: chr(ord("A") + i) for i, s in enumerate(SECTION_ORDER)}
FP_NAME = "LFBGA408_19X19"

# Map old datasheet sections -> new schematic sections (reference style)
def map_section(old_sec: str, pin_name: str) -> str:
    s = old_sec
    n = pin_name.upper()
    if s.startswith("PCI Express") or s.startswith("VGA") or s == "DAC":
        return "A_PCIE"
    if s.startswith("DDR2/DDR3"):
        return "B_DDR"
    if s.startswith("LPC") or s.startswith("System/VGA BIOS SPI") or s.startswith("Serial GPIO"):
        return "C_LPC_SPI"
    if s.startswith("RGMII"):
        return "D_MAC"
    if s.startswith("Static Memory"):
        return "E_FLASH"
    if s.startswith("UART") or s.startswith("I2C") or s.startswith("JTAG"):
        return "F_UART_I2C"
    if (
        s.startswith("USB")
        or s.startswith("ADC")
        or s.startswith("PECI")
        or s.startswith("Miscellaneous")
        or s.startswith("PWM")
        or s.startswith("SD/SDIO")
    ):
        return "G_USB_ADC_MISC"
    if s.startswith("Power") or s.startswith("PLL"):
        return "H_POWER"
    # fallback by name
    if n.startswith("MDQ") or n.startswith("MA") or n.startswith("M"):
        if any(n.startswith(p) for p in ("MDQ", "MDM", "MDQS", "MA", "MBA", "MCK", "MCS", "MRAS", "MCAS", "MWE", "MCKE", "MODT", "MIOZ", "MVREF")):
            return "B_DDR"
    return "G_USB_ADC_MISC"


def mm_to_mil(mm: float) -> float:
    return mm / 0.0254


def ball_xy_mil(ball: str) -> tuple[float, float]:
    m = re.match(r"^([A-Z]+)(\d+)$", ball)
    row, col = m.group(1), int(m.group(2))
    ri = ROWS.index(row)
    x = (col - 11.5) * mm_to_mil(PITCH_MM)
    y = (10.5 - ri) * mm_to_mil(PITCH_MM)
    return x, y


def find_csv() -> Path:
    for p in CSV_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("AST2400_pins.csv not found")


def uniquify_names(pins: list[dict]) -> None:
    """OrCAD requires unique pin names: GND1, GND2, IV12D1..."""
    # per-section uniqueness (hetero part)
    by_sec: dict[str, list[dict]] = defaultdict(list)
    for p in pins:
        by_sec[p["PartSection"]].append(p)

    for sec, items in by_sec.items():
        counts: dict[str, int] = defaultdict(int)
        # first pass count
        base_names = []
        for p in items:
            base = p["PinName"]
            # strip previous suffixes like _2 if any
            base = re.sub(r"_\d+$", "", base)
            base_names.append(base)
            counts[base] += 1

        used: dict[str, int] = defaultdict(int)
        for p, base in zip(items, base_names):
            if counts[base] == 1:
                p["PinName"] = base
            else:
                used[base] += 1
                # GND1 / IV12D1 style (no underscore) per user request
                p["PinName"] = f"{base}{used[base]}"


def sort_key_functional(p: dict) -> tuple:
    """Order pins like reference: buses grouped."""
    n = p["PinName"]
    # strip trailing digits for grouping key
    base = re.sub(r"\d+$", "", n)
    # extract trailing number for bus order
    m = re.search(r"(\d+)$", n)
    num = int(m.group(1)) if m else -1
    # priority groups
    pri = 50
    for i, prefix in enumerate(
        [
            "PERST", "PEWAKE", "PEREFCLK", "PERX", "PETX", "PEREXT", "PEAGND", "NC",
            "MDQ", "MDM", "MDQS", "MA", "MBA", "MCK", "MCS", "MRAS", "MCAS", "MWE", "MCKE", "MODT", "MIOZ", "MVREF",
            "LAD", "LCLK", "LFRAME", "LSIRQ",
            "RGMII", "RMII", "MDC", "MDIO", "RGMIICK",
            "ROM", "FL",
            "SCL", "SDA", "SALT", "TXD", "RXD", "NCTS", "NDCD", "NDSR", "NRI", "NDTR", "NRTS",
            "TCK", "TMS", "TDI", "TDO", "NTRST", "RTCK",
            "USB", "ADC", "DAC", "VGA", "DDC",
            "GND", "IV12", "PV33", "MVDD", "PLL", "PEAV", "R1VDD", "R2VDD",
        ]
    ):
        if base.upper().startswith(prefix) or n.upper().startswith(prefix):
            pri = i
            break
    return (pri, base.upper(), num, p["PinNumber"])


def load_and_rebuild() -> list[dict]:
    src = find_csv()
    raw = list(csv.DictReader(src.open(encoding="utf-8-sig")))
    pins = []
    for r in raw:
        name = r["PinName"]
        new_sec = map_section(r.get("DatasheetSection", r.get("PartSection", "")), name)
        # if old PartSection was already new style, keep mapping from datasheet
        if r.get("DatasheetSection"):
            new_sec = map_section(r["DatasheetSection"], name)
        elif r["PartSection"] in SECTION_ORDER:
            new_sec = r["PartSection"]
        else:
            # old A_POWER style
            old = r["PartSection"]
            remap = {
                "A_POWER": "H_POWER",
                "B_DDR": "B_DDR",
                "C_PCIE_VGA": "A_PCIE",
                "D_MAC": "D_MAC",
                "E_FLASH_SPI": "E_FLASH",
                "F_UART_I2C_JTAG": "F_UART_I2C",
                "G_USB_ADC_MISC": "G_USB_ADC_MISC",
                "H_GPIO_SD_PWM": "G_USB_ADC_MISC",
            }
            # SPI BIOS -> C, Serial GPIO stays C via datasheet; SD/PWM go G
            if "System/VGA" in r.get("DatasheetSection", ""):
                new_sec = "C_LPC_SPI"
            elif "SD/" in r.get("DatasheetSection", "") or "PWM" in r.get("DatasheetSection", ""):
                new_sec = "G_USB_ADC_MISC"
            else:
                new_sec = remap.get(old, map_section(old, name))

        pins.append(
            {
                "PinNumber": r["PinNumber"],
                "PinName": re.sub(r"_\d+$", "", name),
                "Electrical": r["Electrical"],
                "PartSection": new_sec,
                "DatasheetSection": r.get("DatasheetSection", ""),
                "IO_Datasheet": r.get("IO_Datasheet", ""),
                "BufferType": r.get("BufferType", ""),
            }
        )

    # Move LPC from F if wrongly placed - fix by datasheet
    for p in pins:
        ds = p["DatasheetSection"]
        if ds.startswith("LPC"):
            p["PartSection"] = "C_LPC_SPI"
        elif ds.startswith("System/VGA BIOS"):
            p["PartSection"] = "C_LPC_SPI"
        elif ds.startswith("Serial GPIO"):
            p["PartSection"] = "C_LPC_SPI"
        elif ds.startswith("SD/SDIO") or ds.startswith("PWM"):
            p["PartSection"] = "G_USB_ADC_MISC"
        elif ds.startswith("PCI Express") or ds.startswith("VGA") or ds == "DAC":
            p["PartSection"] = "A_PCIE"
        elif ds.startswith("DDR"):
            p["PartSection"] = "B_DDR"
        elif ds.startswith("RGMII"):
            p["PartSection"] = "D_MAC"
        elif ds.startswith("Static Memory"):
            p["PartSection"] = "E_FLASH"
        elif ds.startswith("UART") or ds.startswith("I2C") or ds.startswith("JTAG"):
            p["PartSection"] = "F_UART_I2C"
        elif ds.startswith("Power") or ds.startswith("PLL"):
            p["PartSection"] = "H_POWER"
        elif ds.startswith("USB") or ds.startswith("ADC") or ds.startswith("PECI") or ds.startswith("Miscellaneous"):
            p["PartSection"] = "G_USB_ADC_MISC"

    uniquify_names(pins)

    # assign Side + Order within section after functional sort
    by = defaultdict(list)
    for p in pins:
        by[p["PartSection"]].append(p)
    out = []
    for sec in SECTION_ORDER:
        items = sorted(by[sec], key=sort_key_functional)
        n = len(items)
        # left/right split: first half left, second half right (buses stay contiguous)
        mid = (n + 1) // 2
        for i, p in enumerate(items):
            p["Side"] = "Left" if i < mid else "Right"
            p["Order"] = i + 1
            p["Library"] = "AST2400"
            p["PartName"] = "AST2400"
            p["Package"] = "LFBGA-408_19x19"
            p["Value"] = "AST2400"
            p["PCBFootprint"] = FP_NAME
            out.append(p)
    return out


def pin_xml(name: str, position: int, elec: str, left: bool, y: int) -> str:
    typ = ELEC_CODE.get(elec, 4)
    if left:
        hotpt_x, start_x = -30, 0
        left_pt, right_pt = 0, 1
    else:
        hotpt_x, start_x = 210, 180
        left_pt, right_pt = 1, 0
    return f"""        <SymbolPinScalar>
          <Defn hotptX="{hotpt_x}" hotptY="{y}" name="{escape(name)}" position="{position}" startX="{start_x}" startY="{y}" type="{typ}" visible="1"/>
          <IsLong><Defn val="1"/></IsLong>
          <IsClock><Defn val="0"/></IsClock>
          <IsDot><Defn val="0"/></IsDot>
          <IsLeftPointing><Defn val="{left_pt}"/></IsLeftPointing>
          <IsRightPointing><Defn val="{right_pt}"/></IsRightPointing>
          <IsNetStyle><Defn val="0"/></IsNetStyle>
          <IsNoConnect><Defn val="0"/></IsNoConnect>
          <IsGlobal><Defn val="0"/></IsGlobal>
          <IsNumberVisible><Defn val="1"/></IsNumberVisible>
        </SymbolPinScalar>
"""


def make_libpart(sec: str, pins: list[dict], letter: str) -> str:
    left = [p for p in pins if p["Side"] == "Left"]
    right = [p for p in pins if p["Side"] == "Right"]
    n = max(len(left), len(right), 1)
    y0 = 20
    body_w = 180
    bbox_y2 = y0 + n * 10 + 10

    ordered: list[tuple[dict, bool, int]] = []
    for i, p in enumerate(left):
        ordered.append((p, True, y0 + i * 10))
    for i, p in enumerate(right):
        ordered.append((p, False, y0 + i * 10))

    pin_blocks = []
    pos_map = []
    for idx, (p, is_left, y) in enumerate(ordered):
        pin_blocks.append(pin_xml(p["PinName"], idx, p["Electrical"], is_left, y))
        pos_map.append((p["PinNumber"], idx))

    pinnums = "".join(
        f'        <PinNumber><Defn number="{escape(b)}" position="{pos}"/></PinNumber>\n'
        for b, pos in pos_map
    )
    title = sec  # e.g. A_PCIE shown in Description

    return f"""    <LibPart>
      <Defn/>
      <NormalView>
        <Defn suffix="{letter}.Normal"/>
        <SymbolDisplayProp>
          <Defn locX="90" locY="-30" name="Part Reference" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolDisplayProp>
          <Defn locX="90" locY="-20" name="Value" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolUserProp><Defn name="Datasheet" val="AST2400 Datasheet V1.3"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Description" val="ASPEED AST2400 section {title}"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="AST2400"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="ASPEED"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Section" val="{sec}"/></SymbolUserProp>
        <SymbolColor><Defn val="48"/></SymbolColor>
        <SymbolBBox><Defn x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></SymbolBBox>
        <IsPinNumbersVisible><Defn val="1"/></IsPinNumbersVisible>
        <IsPinNamesRotated><Defn val="1"/></IsPinNamesRotated>
        <IsPinNamesVisible><Defn val="1"/></IsPinNamesVisible>
        <ContentsLibName><Defn name=""/></ContentsLibName>
        <ContentsViewName><Defn name="AST2400"/></ContentsViewName>
        <ContentsViewType><Defn type="0"/></ContentsViewType>
        <PartValue><Defn name="AST2400"/></PartValue>
        <Reference><Defn name="U"/></Reference>
        <Rect><Defn fillStyle="1" hatchStyle="0" lineStyle="0" lineWidth="3" x1="0" x2="{body_w}" y1="0" y2="{bbox_y2}"/></Rect>
{"".join(pin_blocks)}      </NormalView>
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
        items = sorted(by[sec], key=lambda r: int(r["Order"]))
        parts.append(make_libpart(sec, items, SECTION_LETTER[sec]))
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
    cy = half + mm_to_mil(0.25)
    pin_lines = []
    for p in pins:
        x, y = ball_xy_mil(p["PinNumber"])
        pin_lines.append(
            f'    <Pin number="{p["PinNumber"]}" padName="c{int(round(pad))}" '
            f'originX="{x:.4f}" originY="{y:.4f}" rotation="0" isMechanical="no" textBlk="1" />'
        )

    def rect(layer: str, hs: float, lw: float) -> str:
        pts = [(-hs, -hs), (-hs, hs), (hs, hs), (hs, -hs), (-hs, -hs)]
        px = "\n".join(f'        <Point x="{x:.4f}" y="{y:.4f}" />' for x, y in pts)
        return (
            f'    <Layer name="{layer}" packageHeight="0" >\n'
            f'      <Path lineWidth="{lw}" type="open" >\n{px}\n      </Path>\n    </Layer>\n'
        )

    xml = f"""<Footprint name="{FP_NAME}" >
  <Units type="mils" precision="3" />
  <Extents minX="{-cy-50:.4f}" minY="{-cy-50:.4f}" width="{2*cy+100:.4f}" height="{2*cy+100:.4f}" />
  <Padstack name="c{int(round(pad))}" type="single" >
    <Layers>
      <Layer name="TOP"><Pad shape="circle" width="{pad:.4f}" height="{pad:.4f}" /></Layer>
      <Layer name="PASTEMASK_TOP"><Pad shape="circle" width="{pad:.4f}" height="{pad:.4f}" /></Layer>
      <Layer name="SOLDERMASK_TOP"><Pad shape="circle" width="{mask:.4f}" height="{mask:.4f}" /></Layer>
    </Layers>
  </Padstack>
  <TextBlocks>
    <TextBlock name="17" width="6.25" height="25" lineSpacing="25" characterSpacing="6.25" />
  </TextBlocks>
  <Pins>
{chr(10).join(pin_lines)}
  </Pins>
  <Vias></Vias>
  <Layers>
{rect("PACKAGE GEOMETRY/SILKSCREEN_TOP", half, 5)}{rect("PACKAGE GEOMETRY/ASSEMBLY_TOP", half, 1)}{rect("PACKAGE GEOMETRY/PLACE_BOUND_TOP", cy, 1)}  </Layers>
  <Heights></Heights>
</Footprint>
"""
    path.write_text(xml, encoding="utf-8")


def write_csv(pins: list[dict], path: Path) -> None:
    fields = [
        "Library", "PartName", "PartSection", "PinNumber", "PinName", "Electrical",
        "Side", "Order", "IO_Datasheet", "BufferType", "DatasheetSection",
        "Package", "Value", "PCBFootprint",
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for p in pins:
            w.writerow(p)


def write_bat(path: Path) -> None:
    path.write_text(
        "pushd %~dp0\n@echo off\nsetlocal ENABLEDELAYEDEXPANSION\n"
        "Set scriptDir=%cd%\nSet skillScriptPath=!scriptDir:\\=/!\n"
        '@echo skill load "%skillScriptPath%/builder.ile" > builder.scr.txt\n'
        '@echo skill changeWorkingDir "%skillScriptPath%" >> builder.scr.txt\n'
        "for %%g in (*.xml) do (\n"
        '@echo skill LB_createFootprint "%skillScriptPath%/%%g" >> builder.scr.txt\n'
        ")\n@echo exit >> builder.scr.txt\n"
        '@echo Creating footprints..\nSTART /W "" "allegro.exe" -s builder.scr.txt\n\nexit\n',
        encoding="ascii",
    )


def write_readme(path: Path, counts: dict) -> None:
    lines = [
        "# AST2400 Capture/Allegro library (fixed)",
        "",
        "## Fixes vs previous",
        "1. All pin names unique: GND1, GND2, IV12D1... (OrCAD requirement)",
        "2. Sections reorganized like reference schematic:",
    ]
    for sec in SECTION_ORDER:
        lines.append(f"   - {SECTION_LETTER[sec]} = {sec} ({counts.get(sec, 0)} pins)")
    lines += [
        "",
        "## Import",
        "1. Capture: File -> Import -> Library XML -> OrcadCaptureXML/*.xml",
        "2. Place part AST2400: you will get U?A .. U?H (8 sections)",
        "3. Allegro: run AllegroV17_2/*.bat under Cadence 17.2 env",
        "",
        "Section A (PCIE) looks like reference PCI-Express block;",
        "Section B is DDR; Section H is power/GND only.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    pins = load_and_rebuild()
    assert len(pins) == 408, len(pins)

    # verify unique names per section
    by = defaultdict(list)
    for p in pins:
        by[p["PartSection"]].append(p["PinName"])
    for sec, names in by.items():
        if len(names) != len(set(names)):
            from collections import Counter
            d = [n for n, c in Counter(names).items() if c > 1]
            raise SystemExit(f"duplicate names in {sec}: {d}")

    counts = {sec: sum(1 for p in pins if p["PartSection"] == sec) for sec in SECTION_ORDER}

    cap_dir = OUT / "OrcadCaptureXML"
    alg_dir = OUT / "AllegroV17_2"
    cap_dir.mkdir(parents=True, exist_ok=True)
    alg_dir.mkdir(parents=True, exist_ok=True)
    CAPTURE_OUT.mkdir(parents=True, exist_ok=True)

    write_capture_xml(pins, cap_dir / f"{STAMP}.xml")
    write_footprint_xml(pins, alg_dir / f"{FP_NAME}.xml")
    write_bat(alg_dir / f"{STAMP}.bat")
    write_csv(pins, OUT / "AST2400_pins.csv")
    write_csv(pins, CAPTURE_OUT / "AST2400_pins.csv")
    write_csv(pins, ROOT / "01AIcadence" / "ast2400_lib" / "AST2400_pins.csv")
    write_readme(OUT / "README_CN.md", counts)

    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, alg_dir / "builder.ile")

    # checklist
    lines = ["AST2400 pin checklist (unique names)\n"]
    for sec in SECTION_ORDER:
        items = [p for p in pins if p["PartSection"] == sec]
        lines.append(f"===== {SECTION_LETTER[sec]} {sec} ({len(items)}) =====")
        for p in items:
            lines.append(f"{p['Order']}\t{p['PinNumber']}\t{p['PinName']}\t{p['Electrical']}\t{p['Side']}")
        lines.append("")
    (CAPTURE_OUT / "AST2400_pin_checklist.txt").write_text("\n".join(lines), encoding="utf-8")

    print("OK pins", len(pins))
    for sec in SECTION_ORDER:
        print(f"  {SECTION_LETTER[sec]} {sec}: {counts[sec]}")
    # sample power names
    pw = [p["PinName"] for p in pins if p["PartSection"] == "H_POWER"][:8]
    print("H_POWER sample names:", pw)


if __name__ == "__main__":
    main()
