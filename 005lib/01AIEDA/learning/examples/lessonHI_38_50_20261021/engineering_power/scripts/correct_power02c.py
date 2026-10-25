from pathlib import Path
import json,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA/learning/examples/lessonHI_38_50_20261021/engineering_power')
shutil.copy2(R/'readouts/power_geometry_precheck.json',R/'readouts/power_geometry_precheck_02b_failed.json')
d=json.loads((R/'power_paths_02b.json').read_text())
d['supersedes']='power_paths_02b.json: IN_D1_C2 first TOP horizontal y13 intersects already planned C2 GNDviaB at22.152,13.45. Independent geometry precheck found before native02 execution.'
for o in d['operations']:
 if o['id']=='IN_D1_C2':
  o['points']=[[16.95,13],[18.0,11.95],[24.0,11.95],[25.2,13.15],[25.2,15.4]]
  o['widths']=[.6]*4
  o['purpose']='Protected rail detours below local C2 GNDvias with .6width; avoid direct y13 crossing.'
(R/'power_paths_02c.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
p=R/'scripts/precheck_power_geometry.py'
s=p.read_text().replace("'power_paths_02b.json'","'power_paths_02c.json'")
s=s.replace("req=clearance(s['net'],t['net']);gap=","req=clearance(s['net'],t['net'])\n  if (s['id'].startswith('STAR_U1_') and t['id']=='BASE_G') or (t['id'].startswith('STAR_U1_') and s['id']=='BASE_G'):req=.2\n  gap=")
p.write_text(s,encoding='utf-8')
print('WROTE corrected02c and explicit localSTAR spacing model')
