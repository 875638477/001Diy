# -*- coding: utf-8 -*-
"""Parse U1A/B/C/D ball+name lists from AST2400 EVB reference text."""
from pathlib import Path
import re

TEXT = Path(r"D:\001DIY\005lib\01AIcadence\ast2400_lib\ref_design.txt").read_text(
    encoding="utf-8", errors="replace"
)
BALL_RE = re.compile(r"^[A-Z]{1,2}\d{1,2}$")
VALID_ROWS = {
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
}


def is_ball(tok: str) -> bool:
    m = BALL_RE.match(tok)
    if not m:
        return False
    row = re.match(r"[A-Z]+", tok).group(0)
    col = int(re.search(r"\d+", tok).group(0))
    return row in VALID_ROWS and 1 <= col <= 22


def extract_block(label: str, next_labels: list[str]) -> str:
    i = TEXT.find(label)
    if i < 0:
        raise SystemExit(f"missing {label}")
    # start after label
    start = i
    end = len(TEXT)
    for nl in next_labels:
        j = TEXT.find(nl, start + len(label))
        if j >= 0:
            end = min(end, j)
    return TEXT[start:end]


def parse_section(block: str, section: str) -> list[tuple[str, str]]:
    """Extract ordered balls then names after first signal-like token cluster."""
    lines = [ln.strip() for ln in block.splitlines()]
    # find first ball after U1x / AST2400 header
    balls = []
    names = []
    mode = "seek"
    i = 0
    while i < len(lines):
        ln = lines[i]
        if mode == "seek":
            if is_ball(ln):
                mode = "balls"
                continue
            i += 1
            continue
        if mode == "balls":
            if is_ball(ln):
                balls.append(ln)
                i += 1
                continue
            if not ln:
                i += 1
                continue
            # start of names
            mode = "names"
            continue
        if mode == "names":
            if not ln:
                i += 1
                continue
            # stop on junk
            if ln in ("AST2400", "U1A", "U1B", "U1C", "U1D") or ln.startswith("AST2400"):
                i += 1
                continue
            if re.match(r"^\d+(\.\d+)?[KMG]?$", ln):  # resistor values
                break
            if ln.endswith("K") and ln[:-1].replace(".", "").isdigit():
                break
            if ln in ("PCI-Express", "DDR2/DDR3", "LPC", "I2C", "SD/SDIO", "PS2", "Power"):
                i += 1
                continue
            if is_ball(ln):
                # sometimes balls again? stop
                break
            # skip pure numbers page refs
            if re.fullmatch(r"\d+", ln):
                i += 1
                continue
            # signal name
            if re.match(r"^[A-Za-z][A-Za-z0-9_#/]*$", ln):
                names.append(ln)
            i += 1
            if len(names) >= len(balls) and len(balls) > 20:
                # peek ahead - if next few are not signal, stop
                pass
            continue
        i += 1

    print(f"{section}: balls={len(balls)} names={len(names)}")
    if len(balls) != len(names):
        print(f"  MISMATCH! first balls {balls[:5]} ... last {balls[-3:]}")
        print(f"  first names {names[:5]} ... last {names[-3:]}")
        n = min(len(balls), len(names))
        return list(zip(balls[:n], names[:n]))
    return list(zip(balls, names))


# Split by page markers
blocks = {
    "A": extract_block("U1A\n", ["AST2400 EVB - DDR3\n1.1\n\nAST2400 2/4", "U1B\n"]),
    "B": extract_block("U1B\n", ["AST2400 EVB - DDR3\n1.1\n\nAST2400 3/4", "U1C\n"]),
    "C": extract_block("U1C\n", ["AST2400 EVB - DDR3\n1.1\n\nAST2400 4/4", "U1D\n"]),
    "D": extract_block("U1D\n", ["AST2400 EVB - DDR3\n1.1\n\nVGA", "Title\n"]),
}

out_dir = Path(r"D:\001DIY\005lib\01AIcadence\ast2400_lib\ref_sections")
out_dir.mkdir(exist_ok=True)
all_maps = {}
for sec, blk in blocks.items():
    (out_dir / f"U1{sec}_raw.txt").write_text(blk[:8000], encoding="utf-8")
    pairs = parse_section(blk, f"U1{sec}")
    all_maps[sec] = pairs
    lines = [f"{b}\t{n}" for b, n in pairs]
    (out_dir / f"U1{sec}_pins.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {len(pairs)} pairs")

# summary coverage
used = set()
for sec, pairs in all_maps.items():
    for b, _ in pairs:
        used.add(b)
print("unique balls in U1A-D:", len(used))
