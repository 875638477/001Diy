from pathlib import Path
import json,math,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'RIGHT10_source_joint_v3.json').read_text());p['batchId']='RIGHT10_source_joint_v4';tops={a['net'] for a in p['anchors'] if a['pin']%2==0};p['operations']=[o for o in p['operations'] if not(any(o['id']=='RIGHT_'+n+'_VIA' or o['id']=='RIGHT_'+n+'_BOTTOM_ANCHOR' for n in tops))]
for a in p['anchors']:
 if a['net'] in tops:a['via']=None;a['anchorLayer']='TOP';a['anchor']=[47.6,27.8] if a['net']=='GPIO_PB9' else [46.8,round(a['pin']*.5+5.65,4)];a['conservativePadCenterToFlare_mm']=2.1414213562;a['effectivePadEdgeToFlareUpper_mm']=1.5414213562
 else:a['anchor']=[46.8,a['anchor'][1]]
for o in p['operations']:
 for a in p['anchors']:
  n=a['net'];pin=a['pin'];row=round(24.25+(pin-37)*.5,4);yy=round(row-.1,4)
  if o['id']=='RIGHT_'+n+'_TOP' and n in tops:
   o['points']=[[44.25,row],[45,row],[45.1,yy],[46.35,yy]];o.pop('width',None);o['widths']=[.16,.16,.16]
   if n=='GPIO_PB9':o['points'] +=[[46.55,28.65],[47.4,27.8],[47.6,27.8]];o['widths'] +=[.2,.2,.2]
   else:o['points'] +=[a['anchor']];o['widths'] +=[.2]
  if o['id']=='RIGHT_'+n+'_BOTTOM_ANCHOR' and n not in tops:o['points']=[a['via'],a['anchor']];o.pop('widths',None);o['width']=.2
 if o['id']=='RIGHT_C15_COMMON_GND':o['xy']=[48.75,29.27]
 if o['id']=='RIGHT_VSS47_CAP_GROUND':o['points']=[[45.4,29.5],[45.7,29.5],[46.35,29.4],[46.95,29.4],[47.6248,28.7252],[47.95,28.7252],[48.75,28.7252],[48.75,29.27]]
 if o['id']=='RIGHT_VDD48_CAP':o['points']=[[45.3,30.35],[47.95,30.3],[49.8,30.3]]
 if o['id']=='RIGHT_R28_GND_TOP':o['points']=[[51.6236,28],[51.3,28.3236],[51.3,29.2]]
p['operations'].append(dict(type='route',id='RIGHT_C16_GND_BRANCH',net='GND',layer='TOP',points=[[49.8,28.268],[49.3,28.268],[48.75,28.818],[48.75,29.27]],width=.6,purpose='MovedC16 direct normal-width common ground to offpad via'))
p['placementChanges']=[dict(ref='C15',xy=[47.95,30.4016],rotation=270,purpose='Free PB9 TOP source diagonal below local decoupling while keeping direct VSS/VDD return'),dict(ref='C16',xy=[49.8,30.3],rotation=270,purpose='Preserve courtyard separation afterC15 fanout optimization'),dict(ref='R28',xy=[53.3,28],rotation=180,purpose='Preserve C16/body spacing and remove BOOT0 pulldown source obstacle')]
p['partialEndpoints']={a['net']:dict(layer=a['anchorLayer'],xy=a['anchor'],connectedTo='U1.'+str(a['pin'])) for a in p['anchors']};p['partialEndpoints']['GPIO_PC14']=dict(layer='TOP',xy=[49.2,25.2],connectedTo='U1.3');p['requiredProofs']=[dict(net=a['net'],source='U1.'+str(a['pin']),targetXY=a['anchor'],targetLayer=a['anchorLayer']) for a in p['anchors']]
p['revision']='v4 true alternate-layer fanout: five even pins remain continuous TOP and have no idle via/BOTTOM dead stub; five odd pins use private PTH to BOTTOM. C15/C16/R28 jointly moved to allow PB9 normal-width TOP corner. No global rule/innerlayer use change; source/longroute must be reviewed together.'
p['physicalLengths_mm']['TOP_no_via_padCenter_toFlare']=2.1414213562;p['physicalLengths_mm']['TOP_no_via_padCopperEdge_toFlare_upper']=1.5414213562
(R/'RIGHT10_source_joint_v4.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_RIGHT10_v1.py').read_text().replace('source_joint_v1.json','source_joint_v4.json').replace('RIGHT10_v1_','RIGHT10_v4_');(R/'scripts/precheck_RIGHT10_v4.py').write_text(s,encoding='utf-8')
# Replace only declared right-source plans/poses/anchors, preserving all independent future obstacles.
for v in ['2L','4L']:
 pol=json.loads((R/f'RIGHT10_long_policy_{v}_v3.json').read_text());old=json.loads((R/'RIGHT10_source_joint_v3.json').read_text());oldids={x['id'] for x in old['operations']};pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in oldids];pol['pendingOperations'] +=[o for o in p['operations'] if o['type'] not in ['deleteVia','deleteSegment']];pol['pendingPlacementChanges']=[o for o in pol['pendingPlacementChanges'] if o['ref'] not in ['C15','C16','R28']]+p['placementChanges']
 for a in pol['componentAnchors']:
  net=a['net']
  if net in p['partialEndpoints']:a['xy']=p['partialEndpoints'][net]['xy'];a['layers']=[p['partialEndpoints'][net]['layer']]
 pol['sourcePlans']=[x for x in pol['sourcePlans'] if not x['path'].startswith('engineering_power/RIGHT10_source_joint_')];pol['sourcePlans'].append(dict(path='engineering_power/RIGHT10_source_joint_v4.json',sha256=hashlib.sha256((R/'RIGHT10_source_joint_v4.json').read_bytes()).hexdigest()))
 (R/f'RIGHT10_long_policy_{v}_v4.json').write_text(json.dumps(pol,indent=2),encoding='utf-8')
print('ops',len(p['operations']),'tops',tops)