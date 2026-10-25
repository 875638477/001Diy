from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'RIGHT10_source_joint_v4.json').read_text());old=json.loads((R/'RIGHT10_source_joint_v3.json').read_text());oldop={o['id']:o for o in old['operations']};p['batchId']='RIGHT10_source_joint_v5';p['placementChanges']=old['placementChanges']
restore={'RIGHT_VSS47_CAP_GROUND','RIGHT_VDD48_CAP','RIGHT_C15_COMMON_GND','RIGHT_R28_GND_TOP'}
p['operations']=[oldop[o['id']] if o['id'] in restore else o for o in p['operations'] if o['id']!='RIGHT_C16_GND_BRANCH']
for a in p['anchors']:
 if a['net']=='GPIO_PB9':a.update(via=[45.7,28.65],anchorLayer='BOTTOM',anchor=[46.8,28.65]);a['topNeck_mm']=1.49142135623731
for i,o in enumerate(p['operations']):
 if o['id']=='RIGHT_GPIO_PB9_TOP':p['operations'][i]=oldop['RIGHT_GPIO_PB9_TOP']
for opid in ['RIGHT_GPIO_PB9_VIA','RIGHT_GPIO_PB9_BOTTOM_ANCHOR']:
 o=dict(oldop[opid]);
 if o['type']=='route':o['points']=[[45.7,28.65],[46.35,28.65],[46.8,28.65]];o['widths']=[.16,.2]
 p['operations'].append(o)
p['partialEndpoints']={a['net']:dict(layer=a['anchorLayer'],xy=a['anchor'],connectedTo='U1.'+str(a['pin'])) for a in p['anchors']};p['partialEndpoints']['GPIO_PC14']=dict(layer='TOP',xy=[49.2,25.2],connectedTo='U1.3');p['requiredProofs']=[dict(net=a['net'],source='U1.'+str(a['pin']),targetXY=a['anchor'],targetLayer=a['anchorLayer']) for a in p['anchors']];p['revision']='v5 retains true alternate-layer fanout for eight rows and PB9 true BOTTOM, with explicit localBOOT/I2C corridors before externalGPIO. Returns C15/R28 to smaller initialnecessaryposes and leavesC16 unmoved to reduce loop penalty. No duplicate deadPTH for TOPfour. Entire source+alllong must be reviewed together.'
(R/'RIGHT10_source_joint_v5.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
m=dict(status='EXPLICIT_LOCAL_INTERFACE_CORRIDOR_CANDIDATE',operations=[])
def route(i,n,l,pts,w=.2):m['operations'].append(dict(type='route',id=i,net=n,layer=l,points=pts,width=w,purpose='Manual interface corridor before long GPIO; actual return and full native review mandatory'))
def via(i,n,xy,small=False):m['operations'].append(dict(type='via',id=i,net=n,xy=xy,padstack='HI_VIA026_C052_TENT' if small else 'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3,purpose='Real interface layer transition, no idle via'))
route('RIGHT_SCL_EXPLICIT','I2C_SCL','TOP',[[46.8,26.65],[47,26.45],[54,26.45],[55.5,27.95],[55.5,33.2],[57.3,33.2],[58.5,34.4],[58.5,35]])
route('RIGHT_SDA_EXPLICIT_BOTTOM','I2C_SDA','BOTTOM',[[46.8,27.15],[47.2,26.75],[47.2,25.7],[58.5,25.7],[60,27.2],[60,36.4]])
via('RIGHT_SDA_FAR_VIA','I2C_SDA',[60,36.4]);route('RIGHT_SDA_FAR_TOP','I2C_SDA','TOP',[[60,36.4],[59.4,37],[58.5,37]])
via('RIGHT_BOOT_SOURCE_VIA','BOOT0',[47.3,27.45],True);route('RIGHT_BOOT_SOURCE_TOP','BOOT0','TOP',[[46.8,27.65],[47.1,27.65],[47.3,27.45]])
route('RIGHT_BOOT_BOTTOM','BOOT0','BOTTOM',[[47.3,27.45],[51.15,27.45],[52.9,29.2]])
via('RIGHT_BOOT_FAR_VIA','BOOT0',[52.9,29.2]);route('RIGHT_BOOT_FAR_TOP','BOOT0','TOP',[[52.9,29.2],[52.9,28.0016],[52.8984,28]])
route('RIGHT_BOOT_R28_J8','BOOT0','TOP',[[52.8984,28],[53.3,28],[54,28.7],[54,30.73]])
(R/'RIGHT10_interface_corridors_v5.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
for v in ['2L','4L']:
 pol=json.loads((R/f'RIGHT10_long_policy_{v}_v4.json').read_text());oldids={o['id'] for o in json.loads((R/'RIGHT10_source_joint_v4.json').read_text())['operations']};pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in oldids];pol['pendingOperations'] +=[o for o in p['operations'] if o['type'] not in ['deleteVia','deleteSegment']]+m['operations'];pol['pendingPlacementChanges']=[x for x in pol['pendingPlacementChanges'] if x['ref'] not in ['C15','C16','R28']]+p['placementChanges']
 for a in pol['componentAnchors']:
  if a['net'] in p['partialEndpoints']:a['xy']=p['partialEndpoints'][a['net']]['xy'];a['layers']=[p['partialEndpoints'][a['net']]['layer']]
 # Explicitly allow reach to own sourcevia only when real route uses it; normal source geometry remains fixed.
 for win in pol['routeWindows']:
  if set(win['nets'])&{a['net'] for a in p['anchors']}:win['polygon'][0][0]=45.8;win['polygon'][-1][0]=45.8
 (R/f'RIGHT10_long_policy_{v}_v5.json').write_text(json.dumps(pol,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_RIGHT10_v1.py').read_text().replace("p=json.loads((R/'RIGHT10_source_joint_v1.json').read_text());", "p=json.loads((R/'RIGHT10_source_joint_v5.json').read_text());p['operations']+=json.loads((R/'RIGHT10_interface_corridors_v5.json').read_text())['operations'];").replace('RIGHT10_v1_','RIGHT10_v5_interfaces_');(R/'scripts/precheck_RIGHT10_v5_interfaces.py').write_text(s,encoding='utf-8')
print(len(p['operations']),len(m['operations']))