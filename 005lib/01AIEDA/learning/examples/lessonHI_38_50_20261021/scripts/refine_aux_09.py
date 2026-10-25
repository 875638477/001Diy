import json,pathlib,math
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/aux_remote_{v}_v8.json').read_text(encoding='utf8'))
 if v=='2L':
  alt=json.loads((h/'plans/aux_remote_4L_v8.json').read_text(encoding='utf8'))
  old=[o for o in d['operations'] if o['net']!='USB_ATTACH_N'];old +=[dict(o,id=o['id'].replace('4L','2L')) for o in alt['operations'] if o['net']=='USB_ATTACH_N'];d['operations']=old
  d['notes']=['Old attach via(48.95,14.6) had no fully-screened APP-GND stitch <=1.5mm; change explicit remote crossover topology and recheck actual 2L copper, rather than reusing only 4L clearance claims.']
 # Remove sub-.05mm grid access stubs while retaining actual pin centers and explicit intended route.
 for o in d['operations']:
  if o['type']!='route':continue
  pts=o['points']
  while len(pts)>2 and math.dist(pts[0],pts[1])<.05:pts.pop(1)
  while len(pts)>2 and math.dist(pts[-1],pts[-2])<.05:pts.pop(-2)
 d['batchId']=f'aux_remote_{v}_v9'
 (h/f'plans/aux_remote_{v}_v9.json').write_text(json.dumps(d,indent=2),encoding='utf8')