import pathlib,json,math,copy,sys,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
from shapely import affinity
q=dict(status='ENGINEERING_JOINT_RELAYOUT_CANDIDATE_PENDING_NATIVE',batchId='NSS_pullup_local_relayout_01',placementChanges=[dict(ref='R21',xy=[33.7016,30.6],rotation=180),dict(ref='R23',xy=[32.9,32.2],rotation=180),dict(ref='R25',xy=[31.2,33.7],rotation=0),dict(ref='R32',xy=[31,35.5],rotation=0)],operations=[],variantOperations={},supersedesOperations=['SOUTH_RIP_NSS_PULLUP_0','SOUTH_RIP_NSS_PULLUP_1','SOUTH_RIP_NSS_PULLUP_2','SOUTH_NSS_PULLUP_RELOCATED'],reason='Delete internal TOP+BOTTOM long pullup stub which blocks ordinary south-source exit. R25 lands 1.53231mm from real main NSS source node; move local series rows and ADC input resistor to fit real native PlaceBounds, retain MCU ADC0-cap path unchanged.',pending=['Native exact deletions/create and all net graph proofs','Actual ADC/reference/return geometry','R21/R23 interface complete chain remains connected','No manufacturing or SPI edge-rate qualification claimed'])
def delete(net,l,pts,w=.2,id=None):q['operations'].append(dict(type='deleteSegment',id=id or 'NSS01_DEL_'+str(len(q['operations'])),net=net,layer=l,points=pts,width=w))
def route(net,l,pts,w=.2,id=None):q['operations'].append(dict(type='route',id=id or 'NSS01_ADD_'+str(len(q['operations'])),net=net,layer=l,points=pts,width=w))
def via(net,xy,id):q['operations'].append(dict(type='via',id=id,net=net,xy=xy,padstack='L28_VIA030_C060',padDiameterMM=.6,drillDiameterMM=.3))
for a,b in [([35.75,29.25],[36.8,29.25]),([36.8,29.25],[39,27.05]),([39,27.05],[39,26.2])]:delete('PA4_SPI_NSS','TOP',[a,b])
for a,b in [([39,26.2],[39,21.3]),([39,21.3],[32.2,21.3]),([32.2,21.3],[32.2,22])]:delete('PA4_SPI_NSS','BOTTOM',[a,b])
delete('PA4_SPI_NSS','TOP',[[32.2,22],[32,21]])
for xy in [[39,26.2],[32.2,22]]:q['operations'].append(dict(type='deleteVia',id='NSS01_DEL_VIA_'+str(xy),net='PA4_SPI_NSS',xy=xy,padstack='L28_VIA030_C060'))
for pts in [[[32.93,33.02],[32.7984,33.02]],[[34.8,31.15],[32.93,33.02]]]:delete('PA4_SPI_NSS','TOP',pts)
route('PA4_SPI_NSS','TOP',[[34.8,31.15],[33.75,32.2],[32.7984,32.2]],id='NSS01_MAIN_SOURCE')
route('PA4_SPI_NSS','TOP',[[32.7984,32.2],[32.7984,33.0],[32.8764,33.078],[32.8764,33.7]],id='NSS01_LOCAL_PULLUP_STUB')
delete('PA5_SPI_SCK','TOP',[[34.385,30.215],[33.6,31]])
route('PA5_SPI_SCK','TOP',[[34.385,30.215],[34,30.6],[33.6,30.6]],id='NSS01_SCK_SOURCE')
# ADC only upstream RC input/series-to-cap is rerouted; C24->U1.10 stays exact original native.
for pts in [[[32.8,35],[32.6764,35]],[[34.8,33],[32.8,35]]]:delete('ADC0','TOP',pts)
for pts in [[[29.8,34],[26.27,34]],[[30.8,35],[29.8,34]],[[31.1016,35],[30.8,35]]]:delete('ADC_IN','TOP',pts)
route('ADC0','TOP',[[34.8,33],[34.5,33],[33.88,33.62],[33.88,35.5],[32.6764,35.5]],id='NSS01_ADC_SERIES_TO_LOCAL_CAP')
route('ADC_IN','TOP',[[31.1016,35.5],[30.8,35.5],[29.3,34],[26.27,34]],id='NSS01_ADC_INPUT')
# Move V3star feed away from newly positioned R23 terminal, keeping its long diagonal core unchanged.
delete('V3V3','TOP',[[29.8,30.95],[30.7,32]],.6)
delete('V3V3','BOTTOM',[[30.7,32],[37,25.7]],.6)
q['operations'].append(dict(type='deleteVia',id='NSS01_DEL_STAR_C9_VIA',net='V3V3',xy=[30.7,32],padstack='L28_VIA030_C060'))
via('V3V3',[31,31.1],'NSS01_STAR_C9_VIA')
route('V3V3','TOP',[[29.8,30.95],[30.85,30.95],[31,31.1]],.6,'NSS01_STAR_C9_FEED')
route('V3V3','BOTTOM',[[31,31.1],[31.6,31.1],[37,25.7]],.6,'NSS01_STAR_DIAGONAL_CORE')
via('V3V3',[30.4,33.7],'NSS01_R25_SUPPLY_VIA')
route('V3V3','BOTTOM',[[31,31.1],[31,33.7],[30.4,33.7]],.6,'NSS01_R25_SUPPLY_BOTTOM')
route('V3V3','TOP',[[30.4,33.7],[31.3016,33.7]],.6,'NSS01_R25_SUPPLY_TOP')
for v in ['4L','2L']:
 ops=[]
 def vd(net,pts):ops.append(dict(type='deleteSegment',id=f'NSS01_{v}_DEL_'+str(len(ops)),net=net,layer='TOP',points=pts,width=.2))
 def vr(net,pts):ops.append(dict(type='route',id=f'NSS01_{v}_ADD_'+str(len(ops)),net=net,layer='TOP',points=pts,width=.2))
 if v=='4L':
  for pts in [[[32.05,31],[31,29.95]],[[32.0252,31],[32.05,31]]]:vd('SPI_SCK',pts)
  vr('SPI_SCK',[[32.0252,30.6],[31.65,30.6],[31,29.95]])
  for pts in [[[30.5,33],[29.8,32.3]],[[31.2,33],[30.5,33]],[[31.2236,33.02],[31.2,33]]]:vd('SPI_NSS',pts)
  vr('SPI_NSS',[[31.2236,32.2],[31.1,32.2],[30.5,32.8],[30.3,32.8],[29.8,32.3]])
 else:
  for pts in [[[31.85,31],[30.8,29.95]],[[32.0252,31],[31.85,31]]]:vd('SPI_SCK',pts)
  vr('SPI_SCK',[[32.0252,30.6],[31.65,30.6],[31,29.95],[30.8,29.95]])
  for pts in [[[30.16,33.02],[29.6,32.46]],[[31.2236,33.02],[30.16,33.02]]]:vd('SPI_NSS',pts)
  vr('SPI_NSS',[[31.2236,32.2],[31.1,32.2],[30.5,32.8],[29.94,32.8],[29.6,32.46]])
 q['variantOperations'][v]=ops
q['sourcePlans']=[dict(path=str(H/f'inventory/checkpoints/USB_aux_{v}_b014/normalized.json'),sha256=hashlib.sha256((H/f'inventory/checkpoints/USB_aux_{v}_b014/normalized.json').read_bytes()).hexdigest()) for v in ['4L','2L']]
q['expectedProofs']=[dict(from_=a,to=b) for a,b in [('U1.14','R23.1'),('U1.14','R25.2'),('R23.2','J6.5'),('U1.15','R21.1'),('R21.2','J6.2'),('U1.10','C24.1'),('C24.1','R32.2'),('R32.1','J10.1'),('R25.1','U1.24')]]
q['newPullupStubCenterlineMM']=sum(math.dist(a,b) for a,b in zip([[32.7984,32.2],[32.7984,33],[32.8764,33.078]],[[32.7984,33],[32.8764,33.078],[32.8764,33.7]]))
(P/'NSS_pullup_local_relayout_01.json').write_text(json.dumps(q,indent=2),encoding='utf8')
print('saved',len(q['operations']),'common operations',q['newPullupStubCenterlineMM'],'mm stub')
