from pathlib import Path
import json,copy
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';s=json.loads((H/'plans/GPIO_south_joint_root_v8.json').read_text());remove=[]
for o in s['operations']:
 if o['id']=='SOUTH_RETURN_SWDIO' or o['id'].startswith('SOUTH_RETURN_SWDIO_'):remove.append(o['id'])
print('Groundids',[(o['id'],o.get('xy'),o.get('points')) for o in s['operations'] if o['net']=='GND']);s['operations']=[o for o in s['operations'] if o['id'] not in remove];(R/'source/GPIO_south_root_v8_groundtest01.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
for v in ['2L','4L']:
 p=json.loads((H/f'plans/root_south_services_{v}_v16.json').read_text())
 for o in p['operations']:
  if o['id']=='ROOT_SWDIO_BOTTOM':o['points']=[[41.5,21.25],[41.5,21.7],[42,22.2],[46.6,22.2],[46.8,22]]
  if o['id']=='ROOT_SWDIO_EAST_V':o['xy']=[46.8,22]
  if o['id']=='ROOT_SWDIO_TOP':o['points']=[[46.8,22],[47,21.8],[47,19.6],[48.1,18.5],[54.58,18.5],[56.08,20]]
 (R/f'source/root_south_service_{v}_delta01.json').write_text(json.dumps(p,indent=2),encoding='utf-8')