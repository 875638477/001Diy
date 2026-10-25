import pathlib,json,math
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');P=R/'plans'
p=json.loads((P/'GPIO_left_joint_fanout_04.json').read_text(encoding='utf-8-sig'));p['batchId']='GPIO_left_joint_fanout_05';p['operations']=[o for o in p['operations'] if not(o['type']=='via' and o['net']=='GND' and math.dist(o['xy'],[33.28,26])<1e-6)];p['spacingExceptions']=[e for e in p['spacingExceptions'] if e['id']!='HI_LEFT_GND11_VIA_S'];p['revision']='Only remove proposed GNDvia33.28,26 which closes PB11 source pocket. Existing C13 commonvia32.45,25.2748 remains; PB11 sourcevia33.5,25.3 has1.0503mm center distance. PB1 transition has >1.5mm nearest-via target pending actual top ground path/late stitch after long copper frozen, never add target-driven cage.'
(P/'GPIO_left_joint_fanout_05.json').write_text(json.dumps(p,indent=2),encoding='utf8')
for v in ('4L','2L'):
 n=json.loads((P/f'GPIO_future_{v}_08_snapshot.json').read_text());pol=json.loads((P/f'GPIO_future_{v}_08_policy.json').read_text());n['vias']=[z for z in n['vias'] if not(z['net']=='GND' and math.dist(z['xy'],[33.28,26])<1e-6)]
 if v=='2L':
  removed=[a for a in pol['reservedAreas'] if a['id'].startswith('ADC_REFERENCE') or a['id']=='NO_SPI_BOTTOM_IN_PREFILTER_TOP_REFERENCE_VOID'];pol['reservedAreas']=[a for a in pol['reservedAreas'] if a not in removed];pol['softReferenceReservations']=removed;pol['softReferenceReservationBasis']='Parent authorizes finite orthogonal transition/crossing review with actual same-layer ground/near return, not .25 or .65 prototype buffer as hardkeepout. Any selected parallel run beneath ADC/power opening must be rejected/rewired or explicitly engineered before native.'
 for typ,data in [('snapshot',n),('policy',pol)]: (P/f'GPIO_future_{v}_09_{typ}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
print('left05 + 2L ADC/prefilter reference reservations now engineering-review soft, HSE/guard/USB hard retained')
