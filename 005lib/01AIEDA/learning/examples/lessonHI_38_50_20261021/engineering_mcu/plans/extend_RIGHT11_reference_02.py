import pathlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');s=(P/'review_RIGHT11_reference_01.py').read_text(encoding='utf-8-sig')
s=s.replace("['U1.47','Y1.2','Y1.4','C22.2','C23.2']","['U1.47','Y1.2','Y1.4','C22.2','C23.2','C15.2','C16.2']")
s=s.replace("return dict(localReachesApplication=find(local)==find(app),",'''guardResults={}
  for op in load(P/'mcu_critical_routes_v6.json')['operations']:
   if op['id'] not in ['HSE_GUARD_LEFT_NORTH','HSE_GUARD_RIGHT_NORTH','HSE_GUARD_RIGHT_LOWER']:continue
   pt=Point(op['points'][-1]);owner=next(i for i,a in enumerate(zz) if a['geom'].covers(pt))
   guardResults[op['id']]=dict(reachesLocal=find(owner)==find(local),reachesApplication=find(owner)==find(app))
  return dict(guardEnds=guardResults,localReachesApplication=find(local)==find(app),''')
s=s.replace('RIGHT11_independent_reference_{v}_01','RIGHT11_independent_reference_{v}_02')
(P/'review_RIGHT11_reference_02.py').write_text(s,encoding='utf8');exec(compile(s,str(P/'review_RIGHT11_reference_02.py'),'exec'))
