# -*- coding: utf-8 -*-
"""Build AST2400 Capture lib matching EVB reference U1A/B/C/D exactly."""
from __future__ import annotations

import csv
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(r"D:\001DIY\005lib")
REF_TXT = ROOT / "01AIcadence" / "ast2400_lib" / "ref_design.txt"
OUT = ROOT / "AUTOlib" / "ul_AST2400"
CAPTURE_OUT = ROOT / "01captureLib" / "AST2400"
UL_BUILDER = ROOT / "AUTOlib" / "ul_TPS65217CRSLR" / "AllegroV17_2" / "builder.ile"
STAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
FP_NAME = "LFBGA408_19X19"

BALL_RE = re.compile(r"^[A-Z]{1,2}\d{1,2}$")
VALID_ROWS = {
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
}
ELEC_CODE = {
    "Input": 0, "Bidirectional": 1, "Output": 2,
    "Passive": 4, "NC": 4, "Power": 7,
}
ROWS = list(VALID_ROWS)  # for footprint; order fixed below
ROW_ORDER = [
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
]

# Reference functional groups for pin side layout (approx left/right like EVB drawing)
GROUP_SIDE = {
    # U1A
    "PERST#": "L", "PEWAKE#": "L", "PERXP": "L", "PERXN": "L",
    "PEREFCLKP": "L", "PEREFCLKN": "L", "PEREXT": "L", "PETXP": "L", "PETXN": "L",
}


def is_ball(tok: str) -> bool:
    if not BALL_RE.match(tok):
        return False
    row = re.match(r"[A-Z]+", tok).group(0)
    col = int(re.search(r"\d+", tok).group(0))
    return row in VALID_ROWS and 1 <= col <= 22


def is_signal(tok: str) -> bool:
    if not tok or is_ball(tok):
        return False
    if re.fullmatch(r"\d+(\.\d+)?[uUnNpPfF]?", tok):
        return False
    if tok.endswith("K") and tok[:-1].replace(".", "").isdigit():
        return False
    if tok.startswith("C") and tok[1:].isdigit():  # capacitor C73
        return False
    if tok.startswith("R") and tok[1:].isdigit():
        return False
    if tok.startswith("L") and tok[1:].isdigit() and len(tok) <= 3:
        return False
    if tok in ("AST2400", "U1A", "U1B", "U1C", "U1D", "CON3", "ESD"):
        return False
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9_#/.]*$", tok))


def extract_block(text: str, label: str, stop_markers: list[str]) -> str:
    i = text.find(label)
    if i < 0:
        raise SystemExit(f"missing {label}")
    end = len(text)
    for m in stop_markers:
        j = text.find(m, i + len(label))
        if j >= 0:
            end = min(end, j)
    return text[i:end]


def parse_u1_section(block: str, expect: int | None = None) -> list[tuple[str, str]]:
    lines = [ln.strip() for ln in block.splitlines()]
    balls: list[str] = []
    names: list[str] = []
    mode = "seek"
    for ln in lines:
        if mode == "seek":
            if is_ball(ln):
                balls.append(ln)
                mode = "balls"
            continue
        if mode == "balls":
            if is_ball(ln):
                balls.append(ln)
                continue
            if not ln:
                continue
            if is_signal(ln):
                names.append(ln)
                mode = "names"
            continue
        if mode == "names":
            if not ln:
                continue
            if is_signal(ln):
                names.append(ln)
                if expect and len(names) >= expect:
                    break
                if len(names) >= len(balls):
                    break
            elif is_ball(ln):
                break
            else:
                # junk after names
                if len(names) >= len(balls) * 0.9:
                    break
    n = min(len(balls), len(names))
    if expect and n != expect:
        print(f"WARN expect {expect} got balls={len(balls)} names={len(names)} using {n}")
    return list(zip(balls[:n], names[:n]))


def classify_elec(name: str) -> str:
    base = name.split("/")[0].upper()
    if base in ("GND", "PEAGND") or base.endswith("AVSS") or base.endswith("VSS") or base == "PLLVSS":
        return "Power"
    if base in (
        "IV12D", "PV33D", "MVDD", "R1VDD", "R2VDD", "PEAV33", "PEAV12",
        "MPLLAV33", "HPLLAV33", "MPLLDV12", "V1PLLAV12", "V2PLLAV12",
        "DACAV33", "DACDV33", "ADCAV33", "USB2AV33", "PECIVDD",
    ):
        return "Power"
    if base in ("NC",):
        return "NC"
    if base in ("DACRSET", "ADCREXT", "ADCVREFP", "ADCVREFN", "USB2VRES", "PEREXT", "MVREF", "MIOZ"):
        return "Passive"
    # outputs-ish
    if any(base.startswith(p) for p in ("PETX", "MDM", "MCK", "MCS", "MRAS", "MCAS", "MWE", "MCKE", "MODT", "MA", "MBA", "ROMCS", "ROMOE", "ROMWE", "VGA", "DACR", "DACG", "DACB")):
        if base.startswith("MA") and base not in ("MA0",) and not re.match(r"^MA\d+$", base):
            pass
        else:
            if re.match(r"^(PETX|MDM|MCK|MCS|MRAS|MCAS|MWE|MCKE|MODT|MBA|ROMCS|ROMOE|ROMWE|VGAHS|VGAVS|DACR|DACG|DACB)(#)?$", base) or re.match(r"^MA\d+$", base) or re.match(r"^MBA\d+$", base) or re.match(r"^MDM\d+$", base):
                return "Output"
    if any(base.startswith(p) for p in ("PERX", "PEREF", "PERST", "MDQ", "MDQS", "LAD", "LCLK", "LFRAME", "LSIRQ", "SCL", "SDA", "USB", "ADC", "CLKIN", "SRST", "ENTEST")):
        if base.startswith("MDQ") or base.startswith("MDQS"):
            return "Bidirectional"
        if base.startswith("LAD") or base.startswith("SCL") or base.startswith("SDA") or base.startswith("USB") or base.startswith("GPIO"):
            return "Bidirectional"
        if base.startswith("PERX") or base.startswith("PEREF") or base in ("PERST#", "CLKIN", "SRST#", "ENTEST", "LCLK", "LFRAME#", "LSIRQ#"):
            return "Input" if base not in ("LCLK", "LFRAME#", "LSIRQ#", "LAD0") else "Bidirectional"
    if base.startswith("GPIO") or "/" in name:
        return "Bidirectional"
    if base.startswith("RGMII") or base.startswith("RMII") or base.startswith("ROM"):
        return "Bidirectional"
    return "Bidirectional"


def uniquify(pins: list[dict]) -> None:
    counts: dict[str, int] = defaultdict(int)
    bases = []
    for p in pins:
        # use full reference name; for uniquify key use full string
        base = p["PinName"]
        bases.append(base)
        counts[base] += 1
    used: dict[str, int] = defaultdict(int)
    for p, base in zip(pins, bases):
        if counts[base] == 1:
            p["PinName"] = base
        else:
            used[base] += 1
            # GND1 style: if name has no slash, append number; else append _n
            if "/" in base or "#" in base:
                p["PinName"] = f"{base}_{used[base]}"
            else:
                p["PinName"] = f"{base}{used[base]}"


def mm_to_mil(mm: float) -> float:
    return mm / 0.0254


def ball_xy_mil(ball: str) -> tuple[float, float]:
    m = re.match(r"^([A-Z]+)(\d+)$", ball)
    row, col = m.group(1), int(m.group(2))
    ri = ROW_ORDER.index(row)
    x = (col - 11.5) * mm_to_mil(0.8)
    y = (10.5 - ri) * mm_to_mil(0.8)
    return x, y


def pin_xml(name: str, position: int, elec: str, left: bool, y: int) -> str:
    typ = ELEC_CODE.get(elec, 4)
    if left:
        hotpt_x, start_x, lp, rp = -30, 0, 0, 1
    else:
        hotpt_x, start_x, lp, rp = 210, 180, 1, 0
    return f"""        <SymbolPinScalar>
          <Defn hotptX="{hotpt_x}" hotptY="{y}" name="{escape(name)}" position="{position}" startX="{start_x}" startY="{y}" type="{typ}" visible="1"/>
          <IsLong><Defn val="1"/></IsLong>
          <IsClock><Defn val="0"/></IsClock>
          <IsDot><Defn val="0"/></IsDot>
          <IsLeftPointing><Defn val="{lp}"/></IsLeftPointing>
          <IsRightPointing><Defn val="{rp}"/></IsRightPointing>
          <IsNetStyle><Defn val="0"/></IsNetStyle>
          <IsNoConnect><Defn val="0"/></IsNoConnect>
          <IsGlobal><Defn val="0"/></IsGlobal>
          <IsNumberVisible><Defn val="1"/></IsNumberVisible>
        </SymbolPinScalar>
"""


def make_libpart(letter: str, title: str, pins: list[dict]) -> str:
    # keep reference order; left = first half, right = second half (EVB style columns)
    n = len(pins)
    mid = (n + 1) // 2
    left = pins[:mid]
    right = pins[mid:]
    y0 = 20
    nh = max(len(left), len(right), 1)
    body_w = 220
    bbox_y2 = y0 + nh * 10 + 10
    ordered = []
    for i, p in enumerate(left):
        ordered.append((p, True, y0 + i * 10))
    for i, p in enumerate(right):
        ordered.append((p, False, y0 + i * 10))
    blocks = []
    maps = []
    for idx, (p, is_left, y) in enumerate(ordered):
        blocks.append(pin_xml(p["PinName"], idx, p["Electrical"], is_left, y))
        maps.append((p["PinNumber"], idx))
    pinnums = "".join(
        f'        <PinNumber><Defn number="{escape(b)}" position="{pos}"/></PinNumber>\n'
        for b, pos in maps
    )
    return f"""    <LibPart>
      <Defn/>
      <NormalView>
        <Defn suffix="{letter}.Normal"/>
        <SymbolDisplayProp>
          <Defn locX="110" locY="-30" name="Part Reference" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolDisplayProp>
          <Defn locX="110" locY="-20" name="Value" rotation="0" textJustification="0"/>
          <PropFont><Defn escapement="0" height="-9" italic="0" name="Arial" orientation="0" weight="400" width="4"/></PropFont>
          <PropColor><Defn val="48"/></PropColor>
          <PropDispType><Defn val="1"/></PropDispType>
        </SymbolDisplayProp>
        <SymbolUserProp><Defn name="Description" val="AST2400 EVB ref section {title}"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="AST2400"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="ASPEED"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Section" val="{title}"/></SymbolUserProp>
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
{"".join(blocks)}      </NormalView>
      <PhysicalPart>
        <Defn/>
{pinnums}      </PhysicalPart>
    </LibPart>
"""


def write_footprint(pins: list[dict], path: Path) -> None:
    pad = mm_to_mil(0.40)
    mask = mm_to_mil(0.50)
    half = mm_to_mil(19.0) / 2
    cy = half + mm_to_mil(0.25)
    lines = []
    for p in pins:
        x, y = ball_xy_mil(p["PinNumber"])
        lines.append(
            f'    <Pin number="{p["PinNumber"]}" padName="c{int(round(pad))}" '
            f'originX="{x:.4f}" originY="{y:.4f}" rotation="0" isMechanical="no" textBlk="1" />'
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
  <TextBlocks><TextBlock name="17" width="6.25" height="25" lineSpacing="25" characterSpacing="6.25" /></TextBlocks>
  <Pins>
{chr(10).join(lines)}
  </Pins>
  <Vias></Vias>
  <Layers></Layers>
  <Heights></Heights>
</Footprint>
"""
    path.write_text(xml, encoding="utf-8")


def main() -> None:
    text = REF_TXT.read_text(encoding="utf-8", errors="replace")
    sections = {
        "A": ("AST2400_1of4_PCIE_DDR_LPC_I2C_SD", parse_u1_section(
            extract_block(text, "U1A\n", ["U1B\n", "AST2400 2/4"]), 108)),
        "B": ("AST2400_2of4_FLASH_UART_MAC_SPI", parse_u1_section(
            extract_block(text, "U1B\n", ["U1C\n", "AST2400 3/4"]), 120)),
        "C": ("AST2400_3of4_VGA_USB_ADC_PWM", parse_u1_section(
            extract_block(text, "U1C\n", ["U1D\n", "AST2400 4/4"]), 88)),
        "D": ("AST2400_4of4_POWER", parse_u1_section(
            extract_block(text, "U1D\n", ["100p\n", "VGA/PS2", "Title\n"]), 92)),
    }

    all_pins: list[dict] = []
    for letter, (title, pairs) in sections.items():
        print(f"U1{letter}: {len(pairs)} pins")
        for i, (ball, name) in enumerate(pairs):
            all_pins.append({
                "PartSection": letter,
                "SectionTitle": title,
                "PinNumber": ball,
                "PinName": name,
                "Electrical": classify_elec(name),
                "Order": i + 1,
            })

    # coverage check
    balls = [p["PinNumber"] for p in all_pins]
    print("total", len(balls), "unique", len(set(balls)))
    if len(balls) != 408 or len(set(balls)) != 408:
        from collections import Counter
        c = Counter(balls)
        dups = [b for b, n in c.items() if n > 1]
        print("DUPS", dups[:20])
        raise SystemExit("ball count error")

    # uniquify within each section
    by = defaultdict(list)
    for p in all_pins:
        by[p["PartSection"]].append(p)
    for letter, items in by.items():
        uniquify(items)

    # write capture xml - ONLY 4 parts
    parts_xml = []
    for letter in "ABCD":
        items = by[letter]
        title = items[0]["SectionTitle"]
        parts_xml.append(make_libpart(letter, title, items))

    cap_dir = OUT / "OrcadCaptureXML"
    alg_dir = OUT / "AllegroV17_2"
    cap_dir.mkdir(parents=True, exist_ok=True)
    alg_dir.mkdir(parents=True, exist_ok=True)
    CAPTURE_OUT.mkdir(parents=True, exist_ok=True)

    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Lib xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="olb.xsd">
  <Defn name="AST2400.OLB"/>
  <Package>
    <Defn alphabeticNumbering="1" isHomogeneous="0" name="AST2400" pcbFootprint="{FP_NAME}" pcbLib="" refdesPrefix="U"/>
{"".join(parts_xml)}  </Package>
</Lib>
"""
    xml_path = cap_dir / f"{STAMP}.xml"
    xml_path.write_text(xml, encoding="utf-8")
    write_footprint(all_pins, alg_dir / f"{FP_NAME}.xml")

    # bat + builder
    (alg_dir / f"{STAMP}.bat").write_text(
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
    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, alg_dir / "builder.ile")

    # CSV + checklist
    fields = ["PartSection", "SectionTitle", "PinNumber", "PinName", "Electrical", "Order"]
    for dest in (OUT, CAPTURE_OUT, ROOT / "01AIcadence" / "ast2400_lib"):
        dest.mkdir(parents=True, exist_ok=True)
        with (dest / "AST2400_pins.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for letter in "ABCD":
                for p in by[letter]:
                    w.writerow(p)

    lines = ["AST2400 EVB reference U1A-U1D (unique OrCAD names)\n"]
    for letter in "ABCD":
        items = by[letter]
        lines.append(f"===== U1{letter} {items[0]['SectionTitle']} ({len(items)}) =====")
        for p in items:
            lines.append(f"{p['Order']}\t{p['PinNumber']}\t{p['PinName']}\t{p['Electrical']}")
        lines.append("")
    (CAPTURE_OUT / "AST2400_pin_checklist.txt").write_text("\n".join(lines), encoding="utf-8")

    (OUT / "README_CN.md").write_text(
        f"""# AST2400 = EVB reference U1A/U1B/U1C/U1D

Source: AST2400芯片的官方参考设计.pdf (AST2400 EVB DDR3)

| Section | Content | Pins |
|---------|---------|-----:|
| U1A | PCIE + DDR + LPC + I2C + SD | {len(by['A'])} |
| U1B | Flash + UART + MAC + SPI | {len(by['B'])} |
| U1C | VGA/USB/ADC/PWM/Misc | {len(by['C'])} |
| U1D | Power/GND | {len(by['D'])} |

Pin names follow the reference (GPIOQ0/SCL3 style).
Duplicates uniquified: GND1, GND2, IV12D1...

## Import
1. Capture File -> Import -> Library XML
2. Select: `{xml_path.name}`
3. Save as `01captureLib\\AST2400.OLB`
4. Place AST2400 -> get U?A U?B U?C U?D only (4 sections)
""",
        encoding="utf-8",
    )

    print("OK XML", xml_path)
    print("U1A sample", [(p["PinNumber"], p["PinName"]) for p in by["A"][:8]])
    print("U1D GND sample", [p["PinName"] for p in by["D"] if p["PinName"].startswith("GND")][:6])


if __name__ == "__main__":
    main()
