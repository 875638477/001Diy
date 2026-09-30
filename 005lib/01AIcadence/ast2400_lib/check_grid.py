# -*- coding: utf-8 -*-
from pathlib import Path
import re

pat = re.compile(r'startY="(-?\d+)"')
hot = re.compile(r'hotptX="(-?\d+)"[^>]*startX="(-?\d+)"')

t = sorted(Path(r"D:\001DIY\005lib\AUTOlib\ul_TPS65217CRSLR\OrcadCaptureXML").glob("*.xml"))[-1]
text = t.read_text(encoding="utf-8", errors="replace")
ys = sorted(set(int(y) for y in pat.findall(text)))
print("TPS", t.name, "Y", ys, "d", [ys[i + 1] - ys[i] for i in range(len(ys) - 1)])

a = sorted(Path(r"D:\001DIY\005lib\AUTOlib\ul_AST2400\OrcadCaptureXML").glob("*.xml"))[-1]
text = a.read_text(encoding="utf-8")
parts = text.split("<LibPart>")[1:]
for i, part in enumerate(parts):
    ys = sorted(int(y) for y in pat.findall(part))
    uy = sorted(set(ys))
    bad10 = [y for y in uy if y % 10]
    bad5 = [y for y in uy if y % 5]
    print(f"U1{chr(65 + i)} pins={len(ys)} uniq={len(uy)} not_mod10={len(bad10)} not_mod5={len(bad5)}")
    if bad10:
        print("  off10 sample", bad10[:20])
    if len(uy) > 1:
        d = [uy[j + 1] - uy[j] for j in range(min(30, len(uy) - 1))]
        print("  deltas", d)

    # also check Line / CommentText Y
    lines = re.findall(r'y1="(-?\d+)" y2="(-?\d+)"', part)
    # Line uses y1= y2= in Defn differently
    line_ys = re.findall(r'<Line>\s*<Defn[^>]*y1="(-?\d+)"[^>]*y2="(-?\d+)"', part)
    if not line_ys:
        line_ys = re.findall(r'lineWidth="\d+" x1="[^"]+" x2="[^"]+" y1="(-?\d+)" y2="(-?\d+)"', part)
    print("  lines", line_ys)
