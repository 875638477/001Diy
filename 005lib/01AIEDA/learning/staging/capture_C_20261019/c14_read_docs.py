"""Read local official Cadence pages for lesson 14; never execute Capture."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import sys
from datetime import datetime, timezone, timedelta

ROOT = Path(r"D:\001DIY\005lib\01AIEDA\learning\staging\capture_C_20261019")
DOC = Path(r"C:\Program0\Cadence\SPB172\doc")
sys.stdout.reconfigure(encoding="utf-8")

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.ignored=0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"): self.ignored+=1
        if tag in ("p", "div", "li", "br", "tr", "h1", "h2", "h3", "h4", "pre"): self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self.ignored=max(0,self.ignored-1)
        if tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "pre"): self.parts.append("\n")
    def handle_data(self, data):
        if not self.ignored: self.parts.append(data)

names = [
    "cap_ug/Replacing_and_Updating_Cache.html",
    "cap_ug/Replacing_and_Updating_the_cache.html",
    "cap_ug/Exporting_Part_and_Pin_Properties.html",
    "cap_ug/Assigning_Footprint_Properties.html",
    "cap_ug/Exporting_and_Importing_a_Capture_Library.html",
    "cap_ug/Exporting_and_Importing_a_Design_from_XML.html",
    "orctclcap/Getting_Library_Part_User_properties.html",
    "orctclcap/Getting_Pin_Names_from_a_Library_Part.html",
    "orctclcap/Change_pin_name_or_pin_number__in_a_library.html",
]
sources=[]; sections=[]
for name in names:
    path=DOC/name; raw=path.read_bytes()
    parser=Text(); parser.feed(raw.decode("utf-8",errors="replace"))
    lines=[" ".join(line.split()) for line in "".join(parser.parts).splitlines()]
    plain="\n".join(line for line in lines if line)
    sources.append({"path":str(path),"sha256":hashlib.sha256(raw).hexdigest(),"text_length":len(plain)})
    sections.append("SOURCE: "+str(path)+"\n"+plain+"\n")
text_path=ROOT/"c14_official_sources.txt"
text_path.write_text("\n".join(sections),encoding="utf-8")
(ROOT/"c14_official_source_manifest.json").write_text(json.dumps({"read_at_local":datetime.now(timezone(timedelta(hours=8))).isoformat(),"sources":sources},ensure_ascii=True,indent=2),encoding="utf-8")
for section in sections[:4]: print(section)
