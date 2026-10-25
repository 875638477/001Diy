from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');p=R/'plans/SPI_NSS_explicit_v3.json';d=json.loads(p.read_text(encoding='utf8'))
for o in d['operations']:
 if o['id']=='NSS_PULLUP_GND_RETURN':o['xy']=[31,21.6]
d['status']='EXPLICIT_NSS_V3B_GND_VIA_MOVED_AWAY_BOOT1';d['errata']='First 32,23.2 GND via intersected R29.1 BOOT1, rejected before any native writes. Moved31,21.6 subject to complete native/reference checks.'
(R/'plans/SPI_NSS_explicit_v3b.json').write_text(json.dumps(d,indent=2),encoding='utf8')