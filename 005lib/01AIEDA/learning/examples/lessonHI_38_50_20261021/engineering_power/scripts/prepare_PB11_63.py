from pathlib import Path
import sys,json,copy
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
P=H/'engineering_mcu/plans';O=H/'engineering_power'
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');w=load(P/f'GPIO_actualB016_{v}_59_networks.json');r=load(P/f'GPIO_actualB016_{v}_59_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');s=CopperScene(n,w,r,p)
 ops=[dict(type='via',id='PB11_'+v+'_R27_WEST_VIA',net='GPIO_PB11',xy=[36.8,42.4],padstack='L28_VIA030_C060'),dict(type='via',id='PB11_'+v+'_R27_EAST_VIA',net='GPIO_PB11',xy=[40.45,42.4],padstack='L28_VIA030_C060'),dict(type='route',id='PB11_'+v+'_R27_BOTTOM_BRIDGE',net='GPIO_PB11',layer='BOTTOM',width=.2,points=[[36.8,42.4],[37.7,42.4],[38.65,41.45],[39.5,41.45],[40.45,42.4]],purpose='Finite engineered zigzag actual bridge over TOPR27 LIVE vertical, notpower deletion;4L references realL3,2L coplanarguard/groundstitches'),dict(type='route',id='PB11_'+v+'_HEADER_TOP_APPROACH',net='GPIO_PB11',layer='TOP',width=.2,points=[[40.45,42.4],[41.27,43.22],[41.27,55]],purpose='RealJ12.5 approach frominside east of R27LIVE L and below topheaderV3bus'),dict(type='via',id='PB11_'+v+'_R27_WEST_GND',net='GND',xy=[35.5,42.1],padstack='L28_VIA030_C060'),dict(type='via',id='PB11_'+v+'_R27_EAST_GND',net='GND',xy=[41.55,42.4],padstack='L28_VIA030_C060')]
 checks=[]
 for op in ops:
  if op['type']=='route':checks.append(dict(id=op['id'],clear=s.path_clear(op['net'],op['layer'],op['points'],op['width'])))
  else:
   for l in LAYERS:
    bad,inside=s.forbidden(op['net'],l,.2,True,.001);checks.append(dict(id=op['id'],layer=l,clear=not bad.intersects(Point(op['xy'])) and inside.covers(Point(op['xy']))))
  if checks[-1]['clear']==False:
   shapes=[(op['layer'],LineString(op['points']).buffer(op['width']/2),False)] if op['type']=='route' else [(l,Point(op['xy']).buffer(.3),True)for l in LAYERS]
   for l,g,isv in shapes:
    for a in s.obstacles:
     if a['layer']!=l or a['net']==op['net']:continue
     gap=g.distance(a['geometry']);need=s.space(op['net'],a['net'],l,a['kind'],isv)
     if gap<need+.003:print('BLOCK',op['id'],l,a['net'],a['source'],round(gap,5),need,a['geometry'].bounds)
  s.add_operation(op)
 print(v,checks);(O/f'PB11_{v}_63_fixed_review.json').write_text(json.dumps(checks,indent=2));assert all(a['clear']for a in checks)
 p.setdefault('pendingOperations',[]).extend(ops);p['componentAnchors'].append(dict(net='GPIO_PB11',key='PB11_HEADER_ENGINEERED_PORT',xy=[36.8,42.4],layers=['TOP','BOTTOM'],connectedTo='J12.5',replacePinAccess=True));p['bottomCost']=1.2;p['viaCostMM']=3
 for typ,z in [('snapshot',n),('networks',w),('rules',r),('policy',p)]: (O/f'PB11_{v}_63_{typ}.json').write_text(json.dumps(z,indent=2))