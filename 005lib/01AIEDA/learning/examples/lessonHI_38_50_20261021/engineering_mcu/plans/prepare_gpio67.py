import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans')
for v in ['2L','4L']:
 for typ in ['snapshot','networks','rules','policy']:
  z=json.loads((P/f'GPIO_actualB016_{v}_59_{typ}.json').read_text(encoding='utf-8-sig'))
  if typ=='snapshot':
   for xy in [[37.4,27.4],[39.5,28],[38.7,29.5]]:
    zz=[q for q in z['vias'] if q['net']=='GND' and math.dist(q['xy'],xy)<1e-5];assert len(zz)==(0 if v=='4L' and xy==[37.4,27.4] else 1)
    for q in zz:z['vias'].remove(q)
   z['ordinaryGroundStudy']='Candidate remove obsolete GPIO source returns only; new connected TOP actual return/native evidence pending, not SI improvement claim'
  (P/f'GPIO_sourceGNDstudy_{v}_67_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
