import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');q=json.loads((P/'NSS_pullup_local_relayout_01.json').read_text());
for c in q['placementChanges']:
 if c['ref']=='R23':c['xy']=[33.5,32]
for o in q['operations']:
 if o['id']=='NSS01_MAIN_SOURCE':o['points']=[[34.8,31.15],[33.95,32],[33.3984,32]]
 if o['id']=='NSS01_LOCAL_PULLUP_STUB':o['points']=[[33.3984,32],[33.3984,32.9],[32.6764,33.622],[32.6764,33.7]]
 if o['id']=='NSS01_STAR_C9_VIA':o['xy']=[30.7,31.7]
 if o['id']=='NSS01_STAR_C9_FEED':o['points']=[[29.8,30.95],[30.55,31.7],[30.7,31.7]]
 if o['id']=='NSS01_STAR_DIAGONAL_CORE':o['points']=[[30.7,31.7],[31,31.7],[37,25.7]]
 if o['id']=='NSS01_R25_SUPPLY_BOTTOM':o['points']=[[30.7,31.7],[31,32],[31,33.7],[30.4,33.7]]
for v,ops in q['variantOperations'].items():
 for o in ops:
  if o['type']=='route' and o['net']=='SPI_NSS':o['points']=[[31.8236,32],[31.5,32],[30.7,32.8],[30.3 if v=='4L' else 29.94,32.8],[29.8,32.3] if v=='4L' else [29.6,32.46]]
 if v=='2L':ops += [dict(type='deleteSegment',id='NSS01_2L_SHORTEN_GUARD_DEL',net='GND',layer='BOTTOM',points=[[29.9,31.55],[27.1,31.55]],width=.6),dict(type='route',id='NSS01_2L_SHORTEN_GUARD_ADD',net='GND',layer='BOTTOM',points=[[29.7,31.55],[27.1,31.55]],width=.6,purpose='Only trim .2mm free-end of existing common-GND guard to preserve .3 clearance to minimally moved V3 feedvia; guard electrical attachment unchanged, actual return native review required.')]
q['newPullupStubCenterlineMM']=.9+math.sqrt(2)*.722+.078
q['reason']+=' 2L native MISO bottom bridge blocks earlier feedvia31,31.1. Final common feedvia30.7,31.7 (0.3mm from old), R23(33.5,32) and 2L GNDguard free endpoint29.9->29.7 retain full .3gap without global relaxation. C24 PlaceBound gap to R23 only.03mm, actual pad clearance and real MPN/assembly allowance still require validation.'
n=json.loads((P.parent.parent/'inventory/checkpoints/USB_aux_2L_b014/normalized.json').read_text());j6=next(c for c in n['placements'] if c['ref']=='J6');jm={p['net']:'J6.'+p['number'] for p in j6['pins'] if p['number']}
q['expectedProofs']=[{'from':'U1.14','to':'R23.1'},{'from':'U1.14','to':'R25.2'},{'from':'R23.2','to':jm['SPI_NSS']},{'from':'U1.15','to':'R21.1'},{'from':'R21.2','to':jm['SPI_SCK']},{'from':'U1.10','to':'C24.1'},{'from':'C24.1','to':'R32.2'},{'from':'R32.1','to':'J10.1'},{'from':'R25.1','to':'U1.24'}]
(P/'NSS_pullup_local_relayout_01.json').write_text(json.dumps(q,indent=2),encoding='utf8')
print(q['newPullupStubCenterlineMM'],q['expectedProofs'])
