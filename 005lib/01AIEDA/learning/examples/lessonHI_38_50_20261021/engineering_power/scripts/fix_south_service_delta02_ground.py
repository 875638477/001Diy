from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
for v in ['2L','4L']:
 f=R/f'RIGHT10_FULL_{v}_v11.json';p=json.loads(f.read_text())
 for o in p['operations']:
  if o['id']=='RIGHT_SWCLK_MID_RETURN':o['xy']=[52.8,22.8]
 for a in p['returnProofs']:
  if a['sourceId']=='RIGHT_SWCLK_MID_RETURN':a['sourceXY']=[52.8,22.8]
 f.write_text(json.dumps(p,indent=2),encoding='utf-8')