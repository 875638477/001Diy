from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'RIGHT10_source_joint_v1.json').read_text());p['batchId']='RIGHT10_source_joint_v2'
for a in p['anchors']:a['anchor'][0]=46.5
for o in p['operations']:
 if o['id'].endswith('_BOTTOM_ANCHOR'):o['points'][-1][0]=46.5
 if o['id'].startswith('RIGHT_GROUND_STITCH_'):
  j=int(o['id'].split('_')[-1]);o['xy']=[47.1,[25.15,26.65,28.0][j]]
for a in p['requiredProofs']:a['targetXY'][0]=46.5
for net,a in p['partialEndpoints'].items():
 if net!='GPIO_PC14':a['xy'][0]=46.5
p['operations'] += [dict(type='via',id='RIGHT_R28_GND_RETURN',net='GND',xy=[51.3,29.2],padstack='L28_VIA030_C060',purpose='Dedicated real offpad ground connection for moved BOOT0 pulldown'),dict(type='route',id='RIGHT_R28_GND_TOP',net='GND',layer='TOP',points=[[51.3236,28],[51.3,28.0236],[51.3,29.2]],width=.6,purpose='MovedR28.2 direct .6 to nearby common GND via; do not rely on floating TOP dynamic patch')]
p['revision']='v2 only extendsBOTTOManchor.1mm and relocates3GNDstitches to remove Astar grid false blockage, adds movedR28 actual GND. No source via/quiet/pose/neck/rule widening changes. Actual geometric/native prerequisites remain.'
(R/'RIGHT10_source_joint_v2.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_RIGHT10_v1.py').read_text().replace('source_joint_v1.json','source_joint_v2.json').replace('RIGHT10_v1_','RIGHT10_v2_');(R/'scripts/precheck_RIGHT10_v2.py').write_text(s,encoding='utf-8')
# return audit use metadata script but avoid re-freeze/overwrite original
s=(R/'scripts/freeze_RIGHT10_v1.py').read_text();start=s.index("b=json.loads((H/");s=s[start:];s='from pathlib import Path\nimport json,math\nH=Path(r"'+str(R.parent)+'");R=H/"engineering_power";p=json.loads((R/"RIGHT10_source_joint_v2.json").read_text())\n'+s;s=s.replace('RIGHT10_v1_return','RIGHT10_v2_return');(R/'scripts/review_RIGHT10_v2_return.py').write_text(s,encoding='utf-8')
for v in ['2L','4L']:
 pol=json.loads((R/f'RIGHT10_long_policy_{v}_v1.json').read_text());ids={o['id'] for o in p['operations']};pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in ids];pol['pendingOperations'] +=[o for o in p['operations'] if o['type'] not in ['deleteSegment','deleteVia']]
 for a in pol['componentAnchors']:
  if a['key'] in ['ANCHOR_'+z['net'] for z in p['anchors']]:a['xy'][0]=46.5
 pol['sourcePlans']=[x for x in pol['sourcePlans'] if x['path']!='engineering_power/RIGHT10_source_joint_v1.json'];pol['sourcePlans'].append(dict(path='engineering_power/RIGHT10_source_joint_v2.json',sha256=hashlib.sha256((R/'RIGHT10_source_joint_v2.json').read_bytes()).hexdigest()))
 (R/f'RIGHT10_long_policy_{v}_v2.json').write_text(json.dumps(pol,indent=2),encoding='utf-8')
print('source',len(p['operations']))