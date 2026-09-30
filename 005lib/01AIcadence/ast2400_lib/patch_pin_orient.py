# -*- coding: utf-8 -*-
"""Fix right-side pin orientation and regenerate AST2400 XML."""
from pathlib import Path
import re
import runpy

# Patch gen_ul_ast2400_ref.py pin_xml / body_w then exec main
SRC = Path(r"D:\001DIY\005lib\01AIcadence\ast2400_lib\gen_ul_ast2400_ref.py")
text = SRC.read_bytes().decode("utf-8", errors="replace")
if "hotpt_x, start_x, lp, rp = -30, 0, 0, 1" not in text and "lp, rp = -30" not in text:
    # try gbk
    text = SRC.read_bytes().decode("gbk", errors="replace")

# Replace pin_xml function body via regex - find def pin_xml through def make_libpart
new_pin_xml = '''
def pin_xml(name: str, position: int, elec: str, left: bool, y: int, body_w: int) -> str:
    """UL/OrCAD: start on body edge, hotpt outside; both pointing flags = 0."""
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

'''

# Simpler approach: write a standalone regenerator that imports parse logic
# Actually just write complete fixed script as ASCII-only file

FIXED = Path(r"D:\001DIY\005lib\01AIcadence\ast2400_lib\gen_ul_ast2400_ref_fix.py")
# Copy original content by importing modules from existing by rewriting key parts only

# Load original as module after normalizing newlines
norm = text.replace("\r\n", "\n")
# collapse double blank lines from gbk mess somewhat
while "\n\n\n" in norm:
    norm = norm.replace("\n\n\n", "\n\n")

# Replace pin_xml function
pat = re.compile(r"def pin_xml\(.*?\n(?=def make_libpart)", re.S)
if not pat.search(norm):
    raise SystemExit("pin_xml not found")
norm = pat.sub(new_pin_xml + "\n", norm)

# Fix make_libpart body_w and pin_xml call
norm = norm.replace("body_w = 220", "body_w = 280")
norm = norm.replace(
    "blocks.append(pin_xml(p[\"PinName\"], idx, p[\"Electrical\"], is_left, y))",
    "blocks.append(pin_xml(p[\"PinName\"], idx, p[\"Electrical\"], is_left, y, body_w))",
)
# also without escapes
norm = re.sub(
    r"blocks\.append\(pin_xml\(p\[.PinName.\], idx, p\[.Electrical.\], is_left, y\)\)",
    "blocks.append(pin_xml(p[\"PinName\"], idx, p[\"Electrical\"], is_left, y, body_w))",
    norm,
)

FIXED.write_text(norm, encoding="utf-8")
print("wrote", FIXED)
print("has body_w param", "body_w: int" in FIXED.read_text(encoding="utf-8"))
print("has body_w=280", "body_w = 280" in FIXED.read_text(encoding="utf-8"))
print("call with body_w", ", y, body_w)" in FIXED.read_text(encoding="utf-8"))
