import pathlib,json
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');n=json.loads((P/'GPIO_future_2L_10_snapshot.json').read_text());q=json.loads((P/'GPIO13_2L_long_candidate_09.json').read_text())
for o in q['operations']:
 if o['type']=='route':
  for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o['width']]*(len(o['points'])-1))):n['routes'].append(dict(kind='line',net=o['net'],layer='ETCH/'+o['layer'],startEnd=[a,b],width=w,generatedThermal=False,fixedManualCline=True,futureCandidate=o['id']))
 elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=.6,drillDiameterMM=.3,futureCandidate=o['id']))
(P/'GPIO_future_2L_10_plus12_snapshot.json').write_text(json.dumps(n,indent=2),encoding='utf8')
