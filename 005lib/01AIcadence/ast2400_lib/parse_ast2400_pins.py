# -*- coding: utf-8 -*-
"""Parse AST2400 datasheet pin_section.txt -> OrCAD Capture multi-part CSV."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN_TXT = ROOT / "pin_section.txt"
OUT_CSV = ROOT / "AST2400_pins.csv"
OUT_PARTS = ROOT / "AST2400_parts_summary.csv"
OUT_MD = ROOT / "AST2400_library_readme.md"

# AST2400 LFBGA row letters (no I/O/Q/S/X; includes AA/AB)
VALID_ROWS = {
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N",
    "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
}
BALL_RE = re.compile(r"^([A-Z]{1,2})(\d{1,2})$")
SECTION_RE = re.compile(r"^(.+?)\s+(\d+)\s+pins\s*$", re.I)
IO_RE = re.compile(
    r"^(I|O|IU|ID|IR|IS|On|Op|I/O|IS/O|IU/O|ID/O|IR/O|IS/O8|IU/O8|ID/O8|IR/O8|"
    r"ID/Op|IR/Op|IS/Op|IU/Op|O8|O16|-)$",
    re.I,
)
TYPE_SET = {"PCI66", "CMOS", "CMOS3", "SSTL", "A", "P", "VREF"}

ELEC_MAP = {
    "POWER": "Power",
    "INPUT": "Input",
    "OUTPUT": "Output",
    "BIDIR": "Bidirectional",
    "PASSIVE": "Passive",
    "NC": "NC",
}


def is_ball(tok: str) -> bool:
    m = BALL_RE.match(tok.strip())
    if not m:
        return False
    row, col = m.group(1), int(m.group(2))
    return row in VALID_ROWS and 1 <= col <= 22


def classify_io(io: str, signal: str, typ: str) -> str:
    s = signal.upper()
    io_u = (io or "").upper().replace(" ", "")
    typ_u = (typ or "").upper()

    if s == "NC":
        return "NC"
    if (
        s == "GND"
        or s.endswith("AVSS")
        or s.endswith("VSS")
        or "GND" in s
    ):
        return "POWER"
    if typ_u == "P":
        return "POWER"
    if any(
        k in s
        for k in (
            "VDD", "V33", "V12", "MVDD", "PV33", "R1VDD", "R2VDD",
            "IV12", "AV33", "AV12", "DV33", "DV12", "PECIVDD",
        )
    ) and ("I/O" not in io_u) and (io_u in ("-", "") or typ_u == "P"):
        return "POWER"
    if typ_u in ("A", "VREF") and io_u in ("-", ""):
        return "PASSIVE"
    if "I/O" in io_u or io_u in ("IO",):
        return "BIDIR"
    if any(io_u.startswith(p) for p in ("IS/O", "IU/O", "ID/O", "IR/O")):
        return "BIDIR"
    if io_u in ("O",) or io_u.startswith("O8") or io_u.startswith("O16") or io_u.startswith("OP"):
        return "OUTPUT"
    if io_u.startswith("I") and "/O" not in io_u:
        return "INPUT"
    if "O" in io_u and "I" in io_u:
        return "BIDIR"
    if io_u.startswith("O"):
        return "OUTPUT"
    if io_u.startswith("I"):
        return "INPUT"
    return "PASSIVE"


PART_RULES = [
    ("A_POWER", ["Power", "PLL Power"]),
    ("B_DDR", ["DDR2/DDR3 DRAM Interface"]),
    ("C_PCIE_VGA", ["PCI Express Interface", "VGA Interface", "DAC"]),
    ("D_MAC", ["RGMII/RMII/NCSI Dual Interface"]),
    ("E_FLASH_SPI", ["Static Memory Interface", "System/VGA BIOS SPI Interface"]),
    ("F_UART_I2C_JTAG", ["UART Port", "I2C/SMBUS Interface", "JTAG Port", "LPC/SuperIO Interface"]),
    ("G_USB_ADC_MISC", ["USB 2.0 Slave Port", "USB 1.1 Host/Slave Port", "ADC", "PECI Port", "Miscellaneous"]),
    ("H_GPIO_SD_PWM", ["SD/SDIO Interface", "Serial GPIO Interface", "PWM/Fan Tachometer"]),
]


def section_to_part(section: str) -> str:
    for part, secs in PART_RULES:
        for s in secs:
            if section.startswith(s) or s in section:
                return part
    return "H_GPIO_SD_PWM"


def is_noise(ln: str) -> bool:
    if not ln:
        return True
    if ln.startswith("ASPEED") or ln.startswith("All rights"):
        return True
    if ln in ("to next page", "from previous page"):
        return True
    if re.fullmatch(r"\d+", ln):
        return True
    if "Datasheet" in ln or "Confidential" in ln:
        return True
    if ln in ("Ball", "Signal", "I/O", "Type", "Description"):
        return True
    if ln.startswith("Oct ") or ln.startswith("Apr "):
        return True
    if ln.startswith("IO Power Domain"):
        return True
    if ln.startswith("Note"):
        return True
    return False


def looks_like_io(tok: str) -> bool:
    if IO_RE.match(tok):
        return True
    if tok in TYPE_SET:
        return True
    # IS/O8 style
    if re.match(r"^(I|O|IU|ID|IR|IS|Op)(/O\d*|/Op)?$", tok, re.I):
        return True
    return False


def looks_like_signal(tok: str) -> bool:
    if is_ball(tok) or is_noise(tok) or looks_like_io(tok):
        return False
    if len(tok) > 32:
        return False
    # signal-like: letters/digits/#/_ and spaces (USB2 DP -> USB2_DP later)
    if re.match(r"^[A-Za-z][A-Za-z0-9_#/ ]*$", tok):
        return True
    return False


def normalize_signal(name: str) -> str:
    return re.sub(r"\s+", "_", name.strip())


# Manual overrides where PDF text is awkward
BALL_NAME_FIX = {
    "AB21": "USB2_DP",
    "AB20": "USB2_DN",
    "J1": "USB11_HDP",
    "J2": "USB11_HDN",
    "K4": "USB11_DP",
    "K3": "USB11_DN",
}


def parse_sections(text: str) -> list[tuple[str, list[dict]]]:
    lines = [ln.rstrip() for ln in text.splitlines()]
    sections: list[tuple[str, list[dict]]] = []
    cur_name = None
    i = 0
    n = len(lines)

    def skip(j: int) -> int:
        while j < n and is_noise(lines[j].strip()):
            j += 1
        return j

    while i < n:
        ln = lines[i].strip()
        m = SECTION_RE.match(ln)
        if m:
            cur_name = m.group(1).strip()
            sections.append((cur_name, []))
            i = skip(i + 1)
            continue

        if cur_name is None:
            i += 1
            continue

        i = skip(i)
        if i >= n:
            break
        ln = lines[i].strip()
        if SECTION_RE.match(ln):
            continue
        if not is_ball(ln):
            i += 1
            continue

        balls: list[str] = []
        while i < n:
            i = skip(i)
            if i >= n or not is_ball(lines[i].strip()):
                break
            balls.append(lines[i].strip())
            i += 1

        signals: list[str] = []
        while i < n:
            i = skip(i)
            if i >= n:
                break
            tok = lines[i].strip()
            if is_ball(tok) or SECTION_RE.match(tok):
                break
            if looks_like_io(tok):
                break
            if not looks_like_signal(tok):
                break
            signals.append(tok)
            i += 1
            if len(signals) >= len(balls):
                peek = skip(i)
                if peek < n and (looks_like_io(lines[peek].strip()) or is_ball(lines[peek].strip())):
                    break

        i = skip(i)
        io = ""
        if i < n and looks_like_io(lines[i].strip()) and lines[i].strip() not in TYPE_SET:
            io = lines[i].strip()
            i += 1

        i = skip(i)
        typ = ""
        if i < n and lines[i].strip() in TYPE_SET:
            typ = lines[i].strip()
            i += 1

        # consume description until next ball/section
        while i < n:
            i = skip(i)
            if i >= n:
                break
            tok = lines[i].strip()
            if is_ball(tok) or SECTION_RE.match(tok):
                break
            # stop if another signal+io block without ball (alias lines already collected)
            i += 1

        pins = sections[-1][1]
        if len(signals) == len(balls):
            pairs = list(zip(balls, signals))
        elif len(signals) == 1:
            pairs = [(b, signals[0]) for b in balls]
        elif not signals:
            pairs = [(b, f"UNK_{b}") for b in balls]
        else:
            pairs = []
            for idx_b, b in enumerate(balls):
                s = signals[idx_b] if idx_b < len(signals) else signals[-1]
                pairs.append((b, s))

        for b, s in pairs:
            s_norm = BALL_NAME_FIX.get(b, normalize_signal(s))
            pins.append(
                {
                    "ball": b,
                    "signal": s_norm,
                    "aliases": "/".join(normalize_signal(x) for x in signals) if signals else s_norm,
                    "io": io,
                    "type": typ,
                    "section": cur_name,
                }
            )

    return sections


def pin_side(elec: str, order: int) -> str:
    return "Left" if order % 2 == 0 else "Right"


def main() -> None:
    text = PIN_TXT.read_text(encoding="utf-8", errors="replace")
    sections = parse_sections(text)

    all_pins: list[dict] = []
    seen: set[str] = set()
    for sec_name, pins in sections:
        for p in pins:
            ball = p["ball"]
            if ball in seen:
                continue
            seen.add(ball)
            sig = BALL_NAME_FIX.get(ball, p["signal"])
            if sig.startswith("UNK_"):
                sig = BALL_NAME_FIX.get(ball, sig)
            elec = classify_io(p["io"], sig, p["type"])
            all_pins.append(
                {
                    "Part": section_to_part(sec_name),
                    "Ball": ball,
                    "PinName": sig,
                    "Electrical": ELEC_MAP[elec],
                    "ElecCode": elec,
                    "IO": p["io"],
                    "BufferType": p["type"],
                    "Section": sec_name,
                    "Aliases": p["aliases"],
                }
            )

    part_order = [p for p, _ in PART_RULES]
    all_pins.sort(
        key=lambda x: (
            part_order.index(x["Part"]) if x["Part"] in part_order else 99,
            0 if x["ElecCode"] == "POWER" else 1 if x["ElecCode"] == "NC" else 2,
            x["PinName"],
            x["Ball"],
        )
    )

    part_counters: dict[str, int] = {}
    rows = []
    for p in all_pins:
        part = p["Part"]
        part_counters[part] = part_counters.get(part, 0) + 1
        ord_i = part_counters[part]
        rows.append(
            {
                "Library": "AST2400",
                "PartName": "AST2400",
                "PartSection": p["Part"],
                "PinNumber": p["Ball"],
                "PinName": p["PinName"],
                "Electrical": p["Electrical"],
                "Side": pin_side(p["ElecCode"], ord_i),
                "Order": ord_i,
                "IO_Datasheet": p["IO"],
                "BufferType": p["BufferType"],
                "DatasheetSection": p["Section"],
                "Package": "LFBGA-408_19x19",
                "Value": "AST2400",
                "PCBFootprint": "AST2400_LFBGA408",
            }
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = []
    for part in part_order:
        subset = [r for r in rows if r["PartSection"] == part]
        if not subset:
            continue
        summary.append(
            {
                "PartSection": part,
                "PinCount": len(subset),
                "PowerPins": sum(1 for r in subset if r["Electrical"] == "Power"),
                "SamplePins": ",".join(r["PinName"] for r in subset[:8]),
            }
        )
    with OUT_PARTS.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["PartSection", "PinCount", "PowerPins", "SamplePins"])
        w.writeheader()
        w.writerows(summary)

    unk = [r for r in rows if r["PinName"].startswith("UNK_")]
    md = f"""# AST2400 OrCAD Capture Schematic Library (Plan B)

## Source
- Datasheet: `ast2400v13.pdf` (ASPEED AST2400/AST1250 A1 Datasheet V1.3)
- Package: **408-ball 19mm x 19mm LFBGA**
- CSV: `{OUT_CSV.name}`

## Stats
- Unique balls parsed: **{len(rows)}** (target 408)
- Unknown names: **{len(unk)}**
- Part sections: **{len(summary)}**

| PartSection | Pins | Power |
|---|---:|---:|
"""
    for s in summary:
        md += f"| {s['PartSection']} | {s['PinCount']} | {s['PowerPins']} |\n"

    md += """
## Capture steps (semi-auto)

1. OrCAD Capture CIS 17.2 -> File -> New -> Library  
   save as `D:\\001DIY\\005lib\\01captureLib\\AST2400.OLB`
2. New Part `AST2400`, create **8 heterogeneous sections**:
   A_POWER / B_DDR / C_PCIE_VGA / D_MAC / E_FLASH_SPI /
   F_UART_I2C_JTAG / G_USB_ADC_MISC / H_GPIO_SD_PWM
3. Open `AST2400_pins.csv` in Excel, filter by `PartSection`,
   add pins with PinNumber=Ball, PinName, Electrical.
4. Part properties:
   - Value = AST2400
   - PCB Footprint = AST2400_LFBGA408 (create later in 01Psm_lib)
   - Manufacturer = ASPEED
5. Multi-function balls use datasheet primary name (not GPIO).

## Notes
- Power pins Electrical = Power (same name shorts in Capture).
- GND / *AVSS / PLLVSS = Power; name nets consistently on schematic.
- Keep NC pins on symbol and leave floating on board.
- If count != 408, cross-check Ball Map in datasheet.
"""
    OUT_MD.write_text(md, encoding="utf-8")

    print(f"OK pins={len(rows)} sections={len(sections)} parts={len(summary)} unk={len(unk)}")
    for s in summary:
        print(f"  {s['PartSection']}: {s['PinCount']}")
    print(f"vs 408: delta={408 - len(rows)}")
    if unk:
        print("UNK:", [r["PinNumber"] for r in unk])


if __name__ == "__main__":
    main()
