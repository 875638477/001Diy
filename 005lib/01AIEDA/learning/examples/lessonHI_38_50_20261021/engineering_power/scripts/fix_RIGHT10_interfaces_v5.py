from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');r=R/'readouts/RIGHT10_v5_interfaces_2L_precheck.json'
if r.exists():(R/'readouts/RIGHT10_v5_interfaces_2L_failed01.json').write_bytes(r.read_bytes())
f=R/'RIGHT10_interface_corridors_v5.json';p=json.loads(f.read_text())
for o in p['operations']:
 if o['id']=='RIGHT_SCL_EXPLICIT':o['points']=[[46.8,26.65],[47,26.45],[54,26.45],[58,30.45],[58,34.5],[58.5,35]]
 if o['id']=='RIGHT_SDA_EXPLICIT_BOTTOM':o['points']=[[46.8,27.15],[47.2,26.75],[47.2,25.85],[58.5,25.85],[60,27.35],[60,36.4]]
f.write_text(json.dumps(p,indent=2),encoding='utf-8')
ids={o['id'] for o in p['operations']}
for v in ['2L','4L']:
 f=R/f'RIGHT10_long_policy_{v}_v5.json';pol=json.loads(f.read_text());pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in ids]+p['operations'];f.write_text(json.dumps(pol,indent=2),encoding='utf-8')