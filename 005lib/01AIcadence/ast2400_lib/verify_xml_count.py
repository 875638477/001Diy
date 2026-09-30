# -*- coding: utf-8 -*-
from pathlib import Path
import re

xml = Path(r"D:\001DIY\005lib\01captureLib\AST2400\OrcadCaptureXML\2026-07-15_15-40-52.xml").read_text(
    encoding="utf-8"
)
print("SymbolPinScalar", xml.count("<SymbolPinScalar>"))
print("PinNumber", xml.count("<PinNumber>"))
print("LibPart", xml.count("<LibPart>"))
balls = re.findall(r'<PinNumber><Defn number="([^"]+)"', xml)
print("balls", len(balls), "unique", len(set(balls)))
dups = [b for b in set(balls) if balls.count(b) > 1]
print("dups_n", len(dups), "sample", dups[:10])
