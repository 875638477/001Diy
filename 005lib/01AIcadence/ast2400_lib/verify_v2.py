# -*- coding: utf-8 -*-
from pathlib import Path
import re
from collections import Counter

cap = sorted(Path(r"D:\001DIY\005lib\AUTOlib\ul_AST2400\OrcadCaptureXML").glob("*.xml"))[-1]
t = cap.read_text(encoding="utf-8")
print("file", cap.name)
print("LibParts", t.count("<LibPart>"), "pins", t.count("<SymbolPinScalar>"))
parts = t.split("<LibPart>")[1:]
for i, part in enumerate(parts):
    names = re.findall(r'name="([^"]+)" position=', part)
    # filter only pin defs (have position=)
    d = [n for n, c in Counter(names).items() if c > 1]
    print(f"  {chr(ord('A')+i)}: {len(names)} pins, dupes={d[:5] if d else None}")
print("A sample:", re.findall(r'name="([^"]+)" position=', parts[0])[:12])
print("H GND sample:", [n for n in re.findall(r'name="([^"]+)" position=', parts[7]) if n.startswith("GND")][:8])
