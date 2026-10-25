import pathlib,json
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans')
for v in ['2L','4L']:
 p=json.loads((P/f'GPIO_actualB016_{v}_59_policy.json').read_text());p['bottomCost']=1.;p['viaCostMM']=.6;(P/f'GPIO_actualB016_{v}_69_policy.json').write_text(json.dumps(p,indent=2),encoding='utf8')
