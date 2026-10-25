import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans')
for v in ['2L','4L']:
 n=json.loads((P/f'GPIO_actualB016_{v}_59_snapshot.json').read_text());nw=json.loads((P/f'GPIO_actualB016_{v}_59_networks.json').read_text());r=json.loads((P/f'GPIO_actualB016_{v}_59_rules.json').read_text());p=json.loads((P/f'GPIO_actualB016_{v}_59_policy.json').read_text())
 pp=next(z for z in n['placements'] if z['ref']=='J12');assert pp['xy']==[40,55];pp['xy']=[18,9];shift=[-22,-46]
 for pin in pp['pins']:
  pin['xy']=[a+b for a,b in zip(pin['xy'],shift)]
  pin['padBBox']=[[a+b for a,b in zip(pt,shift)]for pt in pin['padBBox']]
 for nk in nw['nets']:
  for c in nk['components']:
   for t in c['terminals']:
    if t['key'].startswith('J12.'):t['xy']=[a+b for a,b in zip(t['xy'],shift)]
 p['pendingOperations']=[dict(type='route',id='J12_SOUTH_V3_SUPPLY_68',net='V3V3',layer='TOP',points=[[33.3,1],[9.11,1],[9.11,9]],width=.6,purpose='Comparison candidate only, all R27 live supply kept; native actual connectivity and height/mechanical review pending')]
 for typ,z in [('snapshot',n),('networks',nw),('rules',r),('policy',p)]: (P/f'GPIO_J12south_{v}_68_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
