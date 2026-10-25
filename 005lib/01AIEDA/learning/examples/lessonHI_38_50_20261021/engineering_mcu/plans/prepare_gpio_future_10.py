import pathlib,json,math
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');P=R/'plans'
q=json.loads((P/'GPIO_left_joint_fanout_05.json').read_text());q['batchId']='GPIO_left_joint_fanout_06';
for o in q['operations']:
 if o['net']=='GPIO_PB11':
  if o['type']=='via':assert o['xy']==[33.5,25.3];o['xy']=[33.7,25.3]
  elif o['type']=='route':o['points']=[[33.7,25.3] if p==[33.5,25.3] else p for p in o['points']]
q['partialEndpoints']['GPIO_PB11']['xy']=[33.7,25.3];q['revision']+=' SPI_external_2L_b012 introduced actual GNDvia32.8,25.3; old33.5,.52 via Cu gap.14 unacceptable. Final PB11via33.7,25.3 yields.34 Cu gap to that.6GNDvia, both variants unified. TOP neck final segment33.7,25.5->33.7,25.3.'
(P/'GPIO_left_joint_fanout_06.json').write_text(json.dumps(q,indent=2),encoding='utf8')
for v in ('4L','2L'):
 n=json.loads((P/f'GPIO_future_{v}_09_snapshot.json').read_text());pol=json.loads((P/f'GPIO_future_{v}_09_policy.json').read_text())
 for z in n['vias']:
  if z['net']=='GPIO_PB11' and z['xy']==[33.5,25.3]:z['xy']=[33.7,25.3]
 for z in n['routes']:
  if z['net']=='GPIO_PB11':z['startEnd']=[[33.7,25.3] if p==[33.5,25.3] else p for p in z['startEnd']]
 for z in pol['componentAnchors']:
  if z['net']=='GPIO_PB11':z['xy']=[33.7,25.3]
 for typ,data in [('snapshot',n),('policy',pol)]: (P/f'GPIO_future_{v}_10_{typ}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 # Preserve prior selected long candidates; no geometric or electrical claim made by this copy.
 plan=json.loads((P/f'GPIO13_{v}_long_candidate_'+('08' if v=='4L' else '09')+'.json').read_text()) if False else None
 if v=='4L':
  plan=json.loads((P/'GPIO13_4L_long_candidate_08.json').read_text())
  for o in plan['operations']:
   if o['type']=='route':
    for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o['width']]*(len(o['points'])-1))):n['routes'].append(dict(kind='line',net=o['net'],layer='ETCH/'+o['layer'],startEnd=[a,b],width=w,generatedThermal=False,fixedManualCline=True,futureCandidate=o['id']))
   elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=.6,drillDiameterMM=.3,futureCandidate=o['id']))
  (P/'GPIO_future_4L_10_plus12_snapshot.json').write_text(json.dumps(n,indent=2),encoding='utf8')
print('left06 actual new SPI GNDvia conflict corrected')
