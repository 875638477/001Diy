# -*- coding: utf-8 -*-
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / "AST2400_pins.csv").open(encoding="utf-8-sig")))
print("count", len(rows))
bad = [r for r in rows if r["PinName"].startswith("UNK") or len(r["PinName"]) > 30]
print("bad", len(bad))
for r in bad[:30]:
    print(" ", r["PinNumber"], r["PinName"], "|", r["DatasheetSection"])

c = Counter(r["PinNumber"] for r in rows)
print("unique balls", len(c))

BALL = re.compile(r"^[A-Z]{1,2}\d{1,2}$")
inv = [r for r in rows if not BALL.match(r["PinNumber"])]
print("invalid", inv)

letters = sorted({re.match(r"([A-Z]+)", b).group(1) for b in c})
print("letters", letters)
print("maxcol", max(int(re.match(r"[A-Z]+(\d+)", b).group(1)) for b in c))

# Expected 22x22 minus corners for 408-ball? Common is 22x22=484 with depopulated
# ASPEED 408 LFBGA 19x19 typically 22x22 array with some NC removed from matrix
# Generate full 22x22 with letters A-V? Let's see datasheet ball letters
print("--- sample by section ---")
from collections import defaultdict

by = defaultdict(list)
for r in rows:
    by[r["DatasheetSection"]].append(r["PinNumber"] + ":" + r["PinName"])
for sec, items in by.items():
    print(sec, len(items))

# Find balls outside A-AB / 1-22
weird = []
for b in c:
    m = re.match(r"([A-Z]+)(\d+)$", b)
    lett, col = m.group(1), int(m.group(2))
    if col < 1 or col > 22:
        weird.append(b)
    if lett not in [
        "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N",
        "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
    ] and lett not in ["I", "O", "Q", "S", "X"]:  # S exists? check
        weird.append(b)
print("weird balls", sorted(set(weird))[:50], "n=", len(set(weird)))

# Letters present that might be wrong (I O Q often skipped in BGA; ASPEED may use them)
print("has I", any(b.startswith("I") and b[1].isdigit() for b in c))
print("has O", any(re.match(r"^O\d+$", b) for b in c))
print("has Q", any(re.match(r"^Q\d+$", b) for b in c))
print("has S", any(re.match(r"^S\d+$", b) for b in c))
print("has X", any(re.match(r"^X\d+$", b) for b in c))

ball_map = (ROOT / "ball_map.txt").read_text(encoding="utf-8", errors="replace")
print("ball_map snippet:\n", ball_map[:2500])
