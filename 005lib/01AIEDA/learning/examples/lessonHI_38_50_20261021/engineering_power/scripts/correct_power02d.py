from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA/learning/examples/lessonHI_38_50_20261021/engineering_power')
d=json.loads((R/'power_paths_02c.json').read_text())
d['supersedes']='power_paths_02c.json: root independent review prefers y10.6 INPUT rail avoiding long broadside overlap with BOTTOM V5sense y12. No other operation changed.'
for o in d['operations']:
 if o['id']=='IN_D1_C2':
  o['points']=[[16.95,13],[16.95,10.6],[25.2,10.6],[25.2,15.4]]
  o['widths']=[.6]*3
  o['purpose']='Root-approved protected input detour below C2 groundvias and1.4mm away from BOTTOM V5sense long horizontal; never long thin power.'
(R/'power_paths_02d.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
p=R/'scripts/precheck_power_geometry.py';p.write_text(p.read_text().replace("'power_paths_02c.json'","'power_paths_02d.json'"),encoding='utf-8')
print('WROTE02d')
