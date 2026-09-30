# -*- coding: utf-8 -*-
"""AST2400 EVB-exact U1A~D: L/R pin order + partition lines + group labels."""
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
ROW_ORDER = [
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
]
ELEC_CODE = {
    "Input": 0, "Bidirectional": 1, "Output": 2,
    "Passive": 4, "NC": 4, "Power": 7,
}

# Explicit EVB L/R layout by ball (unique). Order = top¡úbottom on that side.
# Labels match EVB center text; divider drawn under each group except last.
LAYOUT = {
    "A": [
        ("PCI-Express",
         ["K19", "J22", "G22", "G21", "F21", "F22"],
         ["E22", "E21", "D20"]),
        ("DDR2/DDR3",
         ["W12", "V12", "AB11", "AA11", "Y11", "W11", "V11", "Y10",
          "V10", "AB9", "AA9", "Y9", "W9", "V9", "Y8", "W8",
          "AB10", "AA8", "AA10", "AB8", "V16", "V13"],
         ["AB12", "AA12", "Y12", "V14", "AA13", "W13", "AB13", "Y13",
          "W14", "AA14", "Y14",
          "AB14", "W15", "V15", "Y16", "AB15", "W16", "AA15",
          "AB18", "AB16", "AA17", "Y15", "AA16", "W17", "Y17", "AB17",
          "W10", "V8"]),
        ("LPC",
         ["B20", "A21", "E17"],
         ["B21", "A22", "F19", "C19"]),
        ("SDIO / I2C",
         ["C4", "B3", "A2", "E5", "D4", "C3", "B2", "A1",
          "H4", "H3", "H2", "H1",
          "A18", "D16", "B17", "A17", "C16", "B16", "A16", "E15"],
         ["K21", "K22", "J19", "J18",
          "D3", "C2", "B1", "F5",
          "E3", "D2", "C1", "F4", "E2", "D1", "G5", "F3",
          "C5", "B4", "J21", "J20", "H18", "F18"]),
    ],
    "B": [
        ("BMC NOR/NAND/SPI",
         ["R19", "V20", "W21", "Y22", "U19", "R18", "N21",
          "T22", "T21", "T20", "U22", "U21", "T19", "V22", "U20",
          "A8", "C7", "B7", "A7", "D7", "B6", "A6", "E7"],
         ["R20", "R21", "R22", "P18", "P19", "P20", "P21", "P22",
          "M19", "M20", "M21", "M22", "L18", "L19", "L20", "L21",
          "T18", "N18", "N19", "M18", "N22", "N20", "L22", "K18",
          "V21", "W22"]),
        ("System UART",
         ["U1", "T5", "U3", "V1", "U4", "V2", "W1", "U5"],
         ["V3", "W2", "Y1", "V4", "W3", "Y2", "AA1", "V5"]),
        ("BMC UART",
         ["D15", "C15", "B15", "A15", "E14", "D14", "C14", "B14", "G1"],
         ["D18", "B19", "A20", "D17", "B18", "A19", "E16", "C17", "H5"]),
        ("MAC1",
         ["E11", "D11", "C11", "B11", "A11", "E10"],
         ["A12", "B12", "C12", "D12", "E12", "A13", "C6", "A5"]),
        ("MAC2",
         ["C9", "B9", "A9", "E8", "D8", "C8", "B8"],
         ["D9", "E9", "A10", "B10", "C10", "D10", "A3", "D5"]),
        ("System SPI",
         ["C22", "G18", "D19", "C20"],
         ["B22", "G19", "C18", "E20"]),
    ],
    "C": [
        ("MISC",
         ["E4", "K20"],
         ["AB22", "W20"]),
        ("VGA",
         ["R4", "R3", "R2", "T2", "T1", "T4", "U2"],
         []),
        ("FAN",
         ["V6", "Y5", "AA4", "AB3", "W6", "AA5", "AB4", "V7",
          "Y6", "AB5", "W7", "AA6", "AB6", "Y7", "AA7", "AB7"],
         ["W4", "Y3", "AA2", "AB1", "W5", "Y4", "AA3", "AB2"]),
        ("USB",
         ["J2", "J1", "K4", "K3"],
         ["W18", "Y19", "AA20", "AB21", "AB20", "AA21", "V19"]),
        ("ADC",
         ["L5", "L4", "L3", "L2", "L1", "M5", "M4", "M3",
          "M2", "M1", "N5", "N4", "N3", "N2", "N1", "P5"],
         []),
        ("JTAG / SGPIO",
         ["E1", "F1", "G2", "F2", "G4", "G3",
          "A14", "E13", "D13", "C13"],
         ["J5", "J4", "K5", "J3",
          "Y21", "AA22", "U18", "B13"]),
        ("GPIO Misc",
         ["D6", "B5", "A4", "E6", "E19", "H19", "H20", "E18"],
         []),
    ],
    "D": [
        ("Power / GND",
         ["F8", "F9", "F10", "F11", "U10", "U11", "U14", "U15",
          "F12", "F13", "H6", "H17", "J6", "J17", "M6", "M17",
          "N6", "N17", "U8", "U9",
          "F14", "F15", "K6", "K17", "L6", "L17", "P6", "P17",
          "R6", "R17", "U12", "U13",
          "AB19", "V17", "Y18", "W19", "Y20", "AA19", "AA18", "V18",
          "P1", "R5", "R1", "T3",
          "K2", "K1", "P4", "P3", "P2",
          "F20", "C21", "G20", "H21", "H22", "D21", "D22"],
         ["J10", "J11", "J12", "J13", "J14", "J9",
          "K10", "K11", "K12", "K13", "K14", "K9",
          "L10", "L11", "L12", "L13", "L14", "L9",
          "M10", "M11", "M12", "M13", "M14", "M9",
          "N10", "N11", "N12", "N13", "N14", "N9",
          "P10", "P11", "P12", "P13", "P14", "P9"]),
    ],
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
    if (tok.startswith("C") or tok.startswith("R") or tok.startswith("L")) and len(tok) <= 4 and tok[1:].isdigit():
        return False
    if tok in ("AST2400", "U1A", "U1B", "U1C", "U1D", "CON3", "ESD"):
        return False
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9_#/.]*$", tok))


def extract_block(text: str, label: str, stops: list[str]) -> str:
    i = text.find(label)
    if i < 0:
        raise SystemExit("missing " + label)
    end = len(text)
    for m in stops:
        j = text.find(m, i + len(label))
        if j >= 0:
            end = min(end, j)
    return text[i:end]


def parse_u1_section(block: str, expect: int) -> list[tuple[str, str]]:
    lines = [ln.strip() for ln in block.splitlines()]
    balls, names = [], []
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
                if len(names) >= len(balls):
                    break
            elif is_ball(ln):
                break
            else:
                if len(names) >= len(balls) * 0.9:
                    break
    n = min(len(balls), len(names), expect)
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
    if base == "NC":
        return "NC"
    if base in ("DACRSET", "ADCREXT", "ADCVREFP", "ADCVREFN", "USB2VRES", "PEREXT", "MVREF", "MIOZ"):
        return "Passive"
    if any(base.startswith(p) for p in (
        "PETX", "MDM", "MCK", "MCS", "MRAS", "MCAS", "MWE", "MCKE", "MODT",
        "MA", "MBA", "ROMCS", "ROMOE", "ROMWE", "VGA", "DACR", "DACG", "DACB",
    )):
        if re.match(r"^(PETX|MDM|MCK|MCS|MRAS|MCAS|MWE|MCKE|MODT|MBA|ROMCS|ROMOE|ROMWE|VGAHS|VGAVS|DACR|DACG|DACB)(#)?$", base) or re.match(r"^MA\d+$", base) or re.match(r"^MBA\d+$", base) or re.match(r"^MDM\d+$", base):
            return "Output"
    if base in ("PERST#", "CLKIN", "SRST#", "ENTEST", "LCLK", "LFRAME#", "LSIRQ#") or base.startswith("PERX") or base.startswith("PEREF"):
        return "Input"
    if base.startswith("GPIO") or "/" in name or base.startswith("MDQ") or base.startswith("LAD"):
        return "Bidirectional"
    return "Bidirectional"


def uniquify(pins: list[dict]) -> None:
    counts: dict[str, int] = defaultdict(int)
    for p in pins:
        counts[p["PinName"]] += 1
    used: dict[str, int] = defaultdict(int)
    for p in pins:
        base = p["PinName"]
        if counts[base] == 1:
            continue
        used[base] += 1
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


def make_libpart(letter: str, title: str, by_ball: dict[str, dict]) -> str:
    # All pin/line coords snap to GRID.
    # Capture/UL unit: pin-to-pin 10 ~= 0.1 inch.
    # Grid "1/2 of pin to pin" snap=5; GRID=10 hits both 1/2 and 1/10.
    groups = LAYOUT[letter]
    placed: set[str] = set()
    GRID = 10  # must divide pin_pitch / gap / body / pin_len
    body_w = 340  # 34 * GRID
    y = 20        # 2 * GRID
    gap = 20      # was 16 -> off-grid after first partition
    pin_pitch = 10
    assert body_w % GRID == 0 and y % GRID == 0 and gap % GRID == 0
    graphics: list[str] = []
    pin_blocks: list[str] = []
    maps: list[tuple[str, int]] = []
    pos = 0

    active = []
    for label, left_balls, right_balls in groups:
        left = [by_ball[b] for b in left_balls if b in by_ball]
        right = [by_ball[b] for b in right_balls if b in by_ball]
        for b in left_balls + right_balls:
            if b in by_ball:
                placed.add(b)
        if left or right:
            active.append((label, left, right))

    missing = [b for b in by_ball if b not in placed]
    if missing:
        print(f"WARN U1{letter} unplaced {len(missing)}:", missing[:12])
        mid = (len(missing) + 1) // 2
        active.append((
            "Other",
            [by_ball[b] for b in missing[:mid]],
            [by_ball[b] for b in missing[mid:]],
        ))

    for gi, (label, left, right) in enumerate(active):
        rows = max(len(left), len(right), 1)
        y_top = y
        y_mid = y_top + (rows * pin_pitch) // 2
        y_mid = y_mid - (y_mid % GRID)  # keep label on grid
        graphics.append(comment_xml(label, body_w // 2, y_mid))
        for i, p in enumerate(left):
            yy = y_top + i * pin_pitch
            assert yy % GRID == 0
            pin_blocks.append(pin_xml(p["PinName"], pos, p["Electrical"], True, yy, body_w))
            maps.append((p["PinNumber"], pos))
            pos += 1
        for i, p in enumerate(right):
            yy = y_top + i * pin_pitch
            assert yy % GRID == 0
            pin_blocks.append(pin_xml(p["PinName"], pos, p["Electrical"], False, yy, body_w))
            maps.append((p["PinNumber"], pos))
            pos += 1
        y = y_top + rows * pin_pitch + gap
        if gi < len(active) - 1:
            ly = y - gap // 2  # with gap=20 -> on GRID
            assert ly % GRID == 0
            graphics.append(line_xml(8, ly, body_w - 8, ly))

    # final pin-grid check
    for block in pin_blocks:
        m = re.search(r'startY="(-?\d+)"', block)
        assert m and int(m.group(1)) % GRID == 0, block

    bbox_y2 = y
    assert bbox_y2 % GRID == 0
    pinnums = "".join(
        f'        <PinNumber><Defn number="{escape(b)}" position="{p}"/></PinNumber>\n'
        for b, p in maps
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
        <SymbolUserProp><Defn name="Description" val="AST2400 EVB {title}"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Part_Number" val="AST2400"/></SymbolUserProp>
        <SymbolUserProp><Defn name="Manufacturer_Name" val="ASPEED"/></SymbolUserProp>
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
{"".join(graphics)}{"".join(pin_blocks)}      </NormalView>
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
    path.write_text(
        f"""<Footprint name="{FP_NAME}" >
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
  <Vias></Vias><Layers></Layers><Heights></Heights>
</Footprint>
""",
        encoding="utf-8",
    )


def main() -> None:
    text = REF_TXT.read_text(encoding="utf-8", errors="replace")
    sections = {
        "A": ("1/4 PCIE_DDR_LPC_I2C_SD", parse_u1_section(extract_block(text, "U1A\n", ["U1B\n"]), 108)),
        "B": ("2/4 FLASH_UART_MAC_SPI", parse_u1_section(extract_block(text, "U1B\n", ["U1C\n"]), 120)),
        "C": ("3/4 VGA_USB_ADC_PWM", parse_u1_section(extract_block(text, "U1C\n", ["U1D\n"]), 88)),
        "D": ("4/4 POWER", parse_u1_section(extract_block(text, "U1D\n", ["100p\n"]), 92)),
    }

    all_pins: list[dict] = []
    by_sec: dict[str, dict[str, dict]] = {}
    for letter, (title, pairs) in sections.items():
        items = []
        for i, (ball, name) in enumerate(pairs):
            items.append({
                "PartSection": letter,
                "SectionTitle": title,
                "PinNumber": ball,
                "PinName": name,
                "Electrical": classify_elec(name),
                "Order": i + 1,
            })
        # coverage vs layout
        layout_balls = []
        for _, L, R in LAYOUT[letter]:
            layout_balls.extend(L)
            layout_balls.extend(R)
        parsed = {b for b, _ in pairs}
        missing_in_layout = parsed - set(layout_balls)
        extra_in_layout = set(layout_balls) - parsed
        dups_layout = [b for b in layout_balls if layout_balls.count(b) > 1]
        print(f"U1{letter}: parsed={len(pairs)} layout={len(layout_balls)} "
              f"missing_layout={len(missing_in_layout)} extra={len(extra_in_layout)} dups={dups_layout[:5]}")
        if missing_in_layout:
            print("  missing:", sorted(missing_in_layout)[:20])
        if extra_in_layout:
            print("  extra:", sorted(extra_in_layout)[:20])
        uniquify(items)
        by_ball = {p["PinNumber"]: p for p in items}
        by_sec[letter] = by_ball
        all_pins.extend(items)

    assert len(all_pins) == 408 and len({p["PinNumber"] for p in all_pins}) == 408

    parts = [make_libpart(L, sections[L][0], by_sec[L]) for L in "ABCD"]
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Lib xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="olb.xsd">
  <Defn name="AST2400.OLB"/>
  <Package>
    <Defn alphabeticNumbering="1" isHomogeneous="0" name="AST2400" pcbFootprint="{FP_NAME}" pcbLib="" refdesPrefix="U"/>
{"".join(parts)}  </Package>
</Lib>
"""
    cap_dir = OUT / "OrcadCaptureXML"
    alg_dir = OUT / "AllegroV17_2"
    for d in (cap_dir, alg_dir, CAPTURE_OUT, CAPTURE_OUT / "OrcadCaptureXML"):
        d.mkdir(parents=True, exist_ok=True)

    xml_name = f"{STAMP}.xml"
    (cap_dir / xml_name).write_text(xml, encoding="utf-8")
    (CAPTURE_OUT / "OrcadCaptureXML" / xml_name).write_text(xml, encoding="utf-8")
    write_footprint(all_pins, alg_dir / f"{FP_NAME}.xml")
    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, alg_dir / "builder.ile")
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

    fields = ["PartSection", "SectionTitle", "PinNumber", "PinName", "Electrical", "Order"]
    for dest in (OUT, CAPTURE_OUT, ROOT / "01AIcadence" / "ast2400_lib"):
        with (dest / "AST2400_pins.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for letter in "ABCD":
                for p in by_sec[letter].values():
                    w.writerow(p)

    # checklist in visual L/R order
    lines = ["AST2400 EVB layout (L/R match reference) + partition labels\n"]
    for letter in "ABCD":
        lines.append(f"===== U1{letter} =====")
        for label, L, R in LAYOUT[letter]:
            lines.append(f"-- {label} --")
            n = max(len(L), len(R))
            for i in range(n):
                lb = L[i] if i < len(L) else ""
                rb = R[i] if i < len(R) else ""
                ln = by_sec[letter][lb]["PinName"] if lb else ""
                rn = by_sec[letter][rb]["PinName"] if rb else ""
                lines.append(f"  L {lb:4} {ln:28} | R {rb:4} {rn}")
        lines.append("")
    (CAPTURE_OUT / "AST2400_pin_checklist.txt").write_text("\n".join(lines), encoding="utf-8")

    print("CommentText", xml.count("<CommentText>"))
    print("Line", xml.count("<Line>"))
    print("OK", cap_dir / xml_name)
    # sample U1A PCIE L/R
    print("U1A PCIE L", [by_sec["A"][b]["PinName"] for b in LAYOUT["A"][0][1]])
    print("U1A PCIE R", [by_sec["A"][b]["PinName"] for b in LAYOUT["A"][0][2]])


if __name__ == "__main__":
    main()
