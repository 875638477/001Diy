import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');v='2L'
for typ in ['snapshot','networks','rules','policy']:
 z=json.loads((P/f'GPIO_J12south_{v}_68_{typ}.json').read_text())
 if typ=='snapshot':
  for xy in [[35.8,21.95],[38.8,19.7],[34.28,20.45]]:
   vv=[a for a in z['vias'] if a['net']=='GND' and math.dist(a['xy'],xy)<1e-6];assert len(vv)==1;z['vias'].remove(vv[0])
  z['temporaryOrdinaryReturnConstructionStudy']='Remove three ordinary stitch positions only to measure route corridor capacity; their roles must be replaced before any native adoption. VSS/cap/quiet preserved.'
 (P/f'GPIO_J12south_{v}_75_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
