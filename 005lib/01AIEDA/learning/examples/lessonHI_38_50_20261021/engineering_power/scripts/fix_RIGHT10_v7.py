from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'RIGHT10_source_joint_v6.json').read_text());m=json.loads((R/'RIGHT10_interface_corridors_v7.json').read_text());(R/'RIGHT10_interface_corridors_v7_failed01.json').write_bytes((R/'RIGHT10_interface_corridors_v7.json').read_bytes())
for o in p['operations']:
 if o['id']=='RIGHT_PC14_RETURN':o['xy']=[48.2,25.0]
for o in m['operations']:
 if o['id']=='RIGHT_PA15_DIRECT_EAST':o['points']=[[46.8,24.65],[47.2,24.25],[61,24.25]]
 if o['id']=='RIGHT_PA15_FAR_VIA':o['xy']=[61,24.25]
 if o['id']=='RIGHT_PB4_DIRECT_EAST':o['points']=[[46.8,25.65],[47,25.85],[61.8,25.85]]
 if o['id']=='RIGHT_PB4_FAR_VIA':o['xy']=[61.8,25.85]
 if o['id']=='RIGHT_PB9_BOTTOM_ESCAPE':o['points']=[[46.8,28.65],[47.3,28.65],[47.5,28.85],[47.5,29.5],[49.8,31.8]]
 if o['id']=='RIGHT_PB9_FAR_VIA':o['xy']=[49.8,31.8]
 if o['id']=='RIGHT_BOOT_DIRECT_TOP':o['points']=[[46.8,27.65],[47.15,27.3],[53.1,27.3],[53.1,27.7984],[52.8984,28]]
(R/'RIGHT10_source_joint_v6.json').write_text(json.dumps(p,indent=2),encoding='utf-8');(R/'RIGHT10_interface_corridors_v7.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
for v in ['2L','4L']:
 f=R/f'RIGHT10_long_policy_{v}_v7.json';pol=json.loads(f.read_text());ids={o['id'] for o in m['operations']+p['operations']};pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in ids]+[o for o in p['operations'] if o['type'] not in ['deleteVia','deleteSegment']]+m['operations']
 for a in pol['componentAnchors']:
  if a['net']=='GPIO_PA15':a['xy']=[61,24.25]
  if a['net']=='GPIO_PB4':a['xy']=[61.8,25.85]
  if a['net']=='GPIO_PB9':a['xy']=[49.8,31.8]
 f.write_text(json.dumps(pol,indent=2),encoding='utf-8')