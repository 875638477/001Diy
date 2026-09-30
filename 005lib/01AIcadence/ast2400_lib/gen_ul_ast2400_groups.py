# -*- coding: utf-8 -*-
"""AST2400 EVB U1A-D with internal group lines + labels (PCI-Express etc.)."""
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

# Group labels matching EVB drawing (order = scan order of pins in each section)
SECTION_GROUPS = {
    "A": [
        ("PCI-Express", ("PERST", "PEWAKE", "PERX", "PEREF", "PEREXT", "PETX")),
        ("DDR2/DDR3", ("MDQ", "MDQS", "MCK", "MCS", "MRAS", "MCAS", "MWE", "MCKE", "MODT", "MDM", "MBA", "MA", "MIOZ", "MVREF")),
        ("LPC", ("LCLK", "LFRAME", "LSIRQ", "LAD")),
        ("I2C", ("SCL", "SDA", "GPIOQ", "GPIOK", "GPIOA4", "GPIOA5", "GPIOB0", "GPIOB1", "GPIOB2", "GPIOB3")),
        ("SD/SDIO", ("GPIOC", "GPIOD")),
    ],
    "B": [
        ("BMC NOR/NAND/SPI", ("ROM", "GPIOH", "GPIOR", "GPIOG6", "GPIOG7", "FLBUSY", "FLWP", "GPIOS")),
        ("UART", ("GPIOL", "GPIOM", "GPIOE", "GPIOF", "TXD5", "RXD5")),
        ("MAC1", ("RGMII1", "RMII1", "GPIOU", "GPIOT", "GPIOR6", "GPIOR7", "GPIOA6", "GPIOA7", "MDC", "MDIO")),
        ("MAC2", ("RGMII2", "RMII2", "RGMIICK", "GPIOV")),
        ("System SPI", ("GPIOI", "SYS", "SPI", "VB")),
    ],
    "C": [
        ("System", ("ENTEST", "SRST", "CLKIN", "GPIOY3", "EXTRST", "OSCCLK", "WDTRST", "USBCKI")),
        ("VGA/DAC", ("DAC", "VGA", "DDC")),
        ("PWM/TACH", ("GPION", "GPIOO", "GPIOP", "PWM", "TACH", "BMCINT")),
        ("USB", ("USB",)),
        ("ADC", ("ADC", "GPIW", "GPIX")),
        ("JTAG/SGPIO", ("NTRST", "TCK", "TMS", "TDI", "TDO", "RTCK", "GPIOJ", "GPIOG")),
        ("Misc", ("GPIO", "PECI", "SALT")),
    ],
    "D": [
        ("GND", ("GND",)),
        ("Power", ("R1VDD", "R2VDD", "MVDD", "PV33D", "PEAV33", "IV12D", "PEAV12")),
        ("PLL", ("MPLL", "HPLL", "V1PLL", "V2PLL", "PLLVSS")),
        ("ADC/DAC Power", ("ADC", "DAC")),
        ("ACPI/NC", ("GPIOY", "NC", "PEAGND", "SIO")),
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


def assign_group(letter: str, pin_name: str) -> str:
    raw = pin_name.split("/")[0]
    for gname, prefixes in SECTION_GROUPS[letter]:
        for pref in prefixes:
            if raw.upper().startswith(pref.upper()) or pin_name.upper().startswith(pref.upper()):
                return gname
    return SECTION_GROUPS[letter][-1][0]


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
    # Approximate text bbox around center
    w = max(40, len(name) * 5)
    h = 10
    x1, y1 = cx - w // 2, cy - h // 2
    x2, y2 = cx + w // 2, cy + h // 2
    return f"""        <CommentText>
          <Defn locX="{cx}" locY="{cy}" name="{escape(name)}" x1="{x1}" x2="{x2}" y1="{y1}" y2="{y2}"/>
          <TextFont>
            <Defn escapement="0" height="-12" italic="0" name="Arial" orientation="0" weight="700" width="5"/>
          </TextFont>
        </CommentText>
"""


def make_libpart(letter: str, title: str, pins: list[dict]) -> str:
    """Stack groups vertically; each group has L/R pins, center label, divider lines."""
    # Preserve reference order but bucket into groups
    group_order = [g for g, _ in SECTION_GROUPS[letter]]
    buckets: dict[str, list[dict]] = {g: [] for g in group_order}
    for p in pins:
        g = assign_group(letter, p["PinName"].split("_")[0] if False else p.get("_rawName", p["PinName"]))
        # use original name before uniquify stored in _raw for grouping - fall back
        raw = p.get("_rawName", p["PinName"])
        # strip uniquify suffix for grouping: GND1 -> try GND
        raw_base = re.sub(r"_\d+$", "", raw)
        raw_base = re.sub(r"(\D)\d+$", r"\1", raw_base) if raw_base.startswith("GND") or raw_base.startswith("IV12") else raw
        g = assign_group(letter, p.get("_rawName", p["PinName"]))
        if g not in buckets:
            buckets[g] = []
            group_order.append(g)
        buckets[g].append(p)

    body_w = 320
    y = 20
    gap = 15  # space between groups for label+line
    pin_pitch = 10
    graphics = []
    pin_blocks = []
    maps = []
    pos = 0

    active_groups = [g for g in group_order if buckets.get(g)]
    for gi, gname in enumerate(active_groups):
        items = buckets[gname]
        # split L/R within group (EVB style): first half left, second right
        mid = (len(items) + 1) // 2
        left, right = items[:mid], items[mid:]
        rows = max(len(left), len(right), 1)
        y_top = y
        # label at vertical center of group
        y_mid = y_top + (rows * pin_pitch) // 2
        graphics.append(comment_xml(gname, body_w // 2, y_mid))

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
        # divider line under group (except last)
        if gi < len(active_groups) - 1:
            ly = y - gap // 2
            graphics.append(line_xml(5, ly, body_w - 5, ly))

    bbox_y2 = y
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

    all_pins = []
    by = {}
    for letter, (title, pairs) in sections.items():
        items = []
        for i, (ball, name) in enumerate(pairs):
            items.append({
                "PartSection": letter,
                "SectionTitle": title,
                "PinNumber": ball,
                "PinName": name,
                "_rawName": name,
                "Electrical": classify_elec(name),
                "Order": i + 1,
            })
        uniquify(items)
        by[letter] = items
        all_pins.extend(items)
        print(f"U1{letter}: {len(items)}")

    assert len(all_pins) == 408 and len({p["PinNumber"] for p in all_pins}) == 408

    parts = [make_libpart(L, by[L][0]["SectionTitle"], by[L]) for L in "ABCD"]
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
    cap_dir.mkdir(parents=True, exist_ok=True)
    alg_dir.mkdir(parents=True, exist_ok=True)
    CAPTURE_OUT.mkdir(parents=True, exist_ok=True)
    (CAPTURE_OUT / "OrcadCaptureXML").mkdir(parents=True, exist_ok=True)

    xml_name = f"{STAMP}.xml"
    (cap_dir / xml_name).write_text(xml, encoding="utf-8")
    (CAPTURE_OUT / "OrcadCaptureXML" / xml_name).write_text(xml, encoding="utf-8")
    write_footprint(all_pins, alg_dir / f"{FP_NAME}.xml")
    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, alg_dir / "builder.ile")

    # verify graphics present
    print("CommentText count", xml.count("<CommentText>"))
    print("Line count", xml.count("<Line>"))
    print("OK", cap_dir / xml_name)


if __name__ == "__main__":
    main()
