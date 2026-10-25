from pathlib import Path
import json,copy,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power'
p=json.loads((R/'RIGHT10_source_joint_v5.json').read_text());p['batchId']='RIGHT10_source_joint_v6';p['operations']=[o for o in p['operations'] if o['id'] not in ['RIGHT_SWCLK_VIA','RIGHT_SWCLK_BOTTOM_ANCHOR']]
for a in p['anchors']:
 if a['net']=='SWCLK':a['anchor']=[46.2,24.15];a['anchorLayer']='TOP';a.pop('via',None)
p['partialEndpoints']['SWCLK']=dict(layer='TOP',xy=[46.2,24.15],connectedTo='U1.37');p['requiredProofs']=[dict(net=a['net'],source='U1.'+str(a['pin']),targetXY=a['anchor'],targetLayer=a['anchorLayer']) for a in p['anchors']]
p['revision']='v6 complete-crossbar planning removes SWCLK idle source via/BOTTOM deadstub; source+alllong required. Six remaining real signal PTH transitions only as used by complete topology.'
(R/'RIGHT10_source_joint_v6.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
m=json.loads((R/'RIGHT10_interface_corridors_v6.json').read_text());m['operations']=[o for o in m['operations'] if o['net'] not in ['BOOT0','I2C_SDA']]
def route(i,n,l,pts,w=.2):m['operations'].append(dict(type='route',id=i,net=n,layer=l,points=pts,width=w,purpose='Explicit joint crossbar corridor. Actual full native/reference review mandatory.'))
def via(i,n,xy):m['operations'].append(dict(type='via',id=i,net=n,xy=xy,padstack='L28_VIA030_C060',padDiameterMM=.6,drillDiameterMM=.3,purpose='Real layer transition'))
route('RIGHT_SDA_EXPLICIT_BOTTOM','I2C_SDA','BOTTOM',[[46.8,27.15],[60,27.15],[60,36.4]]);via('RIGHT_SDA_FAR_VIA','I2C_SDA',[60,36.4]);route('RIGHT_SDA_FAR_TOP','I2C_SDA','TOP',[[60,36.4],[59.4,37],[58.5,37]])
route('RIGHT_BOOT_DIRECT_TOP','BOOT0','TOP',[[46.8,27.65],[47.1,27.35],[50.4,27.35],[51.05,28],[52.8984,28]])
route('RIGHT_BOOT_R28_J8','BOOT0','TOP',[[52.8984,28],[53.3,28],[54,28.7],[54,30.73]])
route('RIGHT_PA15_DIRECT_EAST','GPIO_PA15','TOP',[[46.8,24.65],[48,23.45],[51.5,23.45],[52.7,24.65],[61,24.65]]);via('RIGHT_PA15_FAR_VIA','GPIO_PA15',[61,24.65])
route('RIGHT_PB4_DIRECT_EAST','GPIO_PB4','TOP',[[46.8,25.65],[61.8,25.65]]);via('RIGHT_PB4_FAR_VIA','GPIO_PB4',[61.8,25.65])
route('RIGHT_PB5_BOTTOM_EAST','GPIO_PB5','BOTTOM',[[46.8,26.15],[47.2,26.55],[56.5,26.55]]);via('RIGHT_PB5_MID_VIA','GPIO_PB5',[56.5,26.55]);route('RIGHT_PB5_TOP_EAST','GPIO_PB5','TOP',[[56.5,26.55],[62.6,26.55]]);via('RIGHT_PB5_FAR_VIA','GPIO_PB5',[62.6,26.55])
route('RIGHT_PB8_BOTTOM_EAST','GPIO_PB8','BOTTOM',[[46.8,28.15],[47.2,27.95],[59,27.95]]);via('RIGHT_PB8_MID_VIA','GPIO_PB8',[59,27.95]);route('RIGHT_PB8_TOP_EAST','GPIO_PB8','TOP',[[59,27.95],[64,27.95]]);via('RIGHT_PB8_FAR_VIA','GPIO_PB8',[64,27.95])
route('RIGHT_PB9_BOTTOM_ESCAPE','GPIO_PB9','BOTTOM',[[46.8,28.65],[47.2,29.05],[47.2,29.5],[49.8,32.1]]);via('RIGHT_PB9_FAR_VIA','GPIO_PB9',[49.8,32.1])
route('RIGHT_SWO_BOTTOM_ESCAPE','SWO','BOTTOM',[[46.8,25.15],[47.5,25.85],[50.7,25.85],[53.05,23.5],[54,23.5]]);via('RIGHT_SWO_FAR_VIA','SWO',[54,23.5])
m['revision']='v7 joint orthogonal crossing: TOP east leads/BOTTOM north leads, explicit lowerROW avoiding source-pocket closure and no idle SWCLK/BOOT PTH';(R/'RIGHT10_interface_corridors_v7.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
newanchors={'GPIO_PA15':([61,24.65],'BOTTOM'),'GPIO_PB4':([61.8,25.65],'BOTTOM'),'GPIO_PB5':([62.6,26.55],'BOTTOM'),'GPIO_PB8':([64,27.95],'BOTTOM'),'GPIO_PB9':([49.8,32.1],'TOP'),'SWO':([54,23.5],'TOP'),'SWCLK':([46.2,24.15],'TOP')}
for v in ['2L','4L']:
 pol=json.loads((R/f'RIGHT10_long_policy_{v}_v6.json').read_text());oldids={o['id'] for o in json.loads((R/'RIGHT10_source_joint_v5.json').read_text())['operations']+json.loads((R/'RIGHT10_interface_corridors_v6.json').read_text())['operations']};pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in oldids]+[o for o in p['operations'] if o['type'] not in ['deleteVia','deleteSegment']]+m['operations']
 for a in pol['componentAnchors']:
  if a['net'] in newanchors:a['xy'],layer=newanchors[a['net']];a['layers']=[layer]
 (R/f'RIGHT10_long_policy_{v}_v7.json').write_text(json.dumps(pol,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_RIGHT10_v6_interfaces.py').read_text().replace('RIGHT10_source_joint_v5.json','RIGHT10_source_joint_v6.json').replace('RIGHT10_interface_corridors_v6.json','RIGHT10_interface_corridors_v7.json').replace('RIGHT10_v6_interfaces_','RIGHT10_v7_interfaces_');(R/'scripts/precheck_RIGHT10_v7_interfaces.py').write_text(s,encoding='utf-8')
print('source',len(p['operations']),'manual',len(m['operations']))