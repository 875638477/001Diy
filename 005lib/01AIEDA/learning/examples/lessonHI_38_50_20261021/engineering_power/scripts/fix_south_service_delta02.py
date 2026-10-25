from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
for v in ['2L','4L']:
 f=R/f'RIGHT10_FULL_{v}_v11.json';p=json.loads(f.read_text());(R/f'RIGHT10_FULL_{v}_v11_failed01.json').write_bytes(f.read_bytes())
 for o in p['operations']:
  if o['id']=='RIGHT_SWCLK_BOTTOM_BRIDGE':o['points']=[[47.95,22.4],[48.65,23.1],[51,23.1],[51.8,22.3],[51.8,21.1],[57.1,21.1],[57.4,20.8]]
  if o['id']=='RIGHT_SWCLK_EAST_RETURN':o['xy']=[57.35,19.31]
 p['operations'].append(dict(type='via',id='RIGHT_SWCLK_MID_RETURN',net='GND',xy=[52.8,22.9],padstack='L28_VIA030_C060',purpose='CommonGND reinforcement adjacent finiteR17opposite-layerprojection; not symbolic reference certification'))
 for a in p['returnReview']:
  if a['signalVia']=='RIGHT_SWCLK_EAST_BRIDGE_V':a['groundXY']=[57.35,19.31];a['distanceMM']=1.49083869012
 for a in p['returnProofs']:
  if a['sourceId']=='RIGHT_SWCLK_EAST_RETURN':a['sourceXY']=[57.35,19.31]
 p['returnProofs'].append(dict(net='GND',sourceXY=[52.8,22.9],sourceId='RIGHT_SWCLK_MID_RETURN',target='U1.23'));p['revision'] += ' Sourcebridge avoids SWOvia54,23.5 and GND53.844,22.614 using y21.1 after RX. EastGNDbetweenheaderrectpads57.35,19.31 instead of tightold57.4,19.35.';f.write_text(json.dumps(p,indent=2),encoding='utf-8')