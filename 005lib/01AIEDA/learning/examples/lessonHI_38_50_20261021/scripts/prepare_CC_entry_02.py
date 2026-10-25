import json,pathlib
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/CC_entry_{v}_v1.json').read_text())
 for o in d['operations']:
  if o['id']=='CC2_ENTRY':o['points']=[[41.75,7.355],[41.75,8.0],[42.1,8.35],[44.4,8.35],[45.5,9.45],[45.5,10.1016]]
  if o['id']=='CC_R4_GND':o['points']=[[45.5,11.6764],[43.9,11.6764],[43.8,11.5764]]
 d['operations']=[o for o in d['operations'] if o['id']!='CC_R4_GND_V']
 (h/f'plans/CC_entry_{v}_v2.json').write_text(json.dumps(d,indent=2),encoding='utf8')