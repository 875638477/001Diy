# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = sorted(Path(r"D:\001DIY\005lib\AUTOlib\ul_AST2400\OrcadCaptureXML").glob("*.xml"))[-1]
t = p.read_text(encoding="utf-8")
print("file", p.name)
bw = re.findall(r'x2="(\d+)"', t)
print("x2 samples", bw[:6])
# right pin: startX should equal body width 280, hotpt 310
rights = re.findall(
    r'hotptX="(\d+)" hotptY="\d+" name="([^"]+)" position="\d+" startX="(\d+)"',
    t,
)
right_pins = [(h, n, s) for h, n, s in rights if int(s) > 0]
left_pins = re.findall(
    r'hotptX="(-?\d+)" hotptY="\d+" name="([^"]+)" position="\d+" startX="(\d+)"',
    t,
)
left_pins = [(h, n, s) for h, n, s in left_pins if s == "0"]
print("left sample", left_pins[:3])
print("right sample", right_pins[:3])
# pointing flags near ADC14
i = t.find('name="ADC14')
print("--- around ADC14 ---")
print(t[i : i + 450] if i > 0 else "missing")
