from pathlib import Path
import sys,json,copy
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
P=H/'engineering_mcu/plans';O=H/'engineering_power'
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');w=load(P/f'GPIO_actualB016_{v}_59_networks.json');r=load(P/f'GPIO_actualB016_{v}_59_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');s=CopperScene(n,w,r,p)
 ops=[dict(type='via',id='PB11_'+v+'_R27_WEST_VIA',net='GPIO_PB11',xy=[36.8,45],padstack='L28_VIA030_C060'),dict(type='via',id='PB11_'+v+'_R27_EAST_VIA',net='GPIO_PB11',xy=[39.2,45],padstack='L28_VIA030_C060'),dict(type='route',id='PB11_'+v+'_R27_BOTTOM_BRIDGE',net='GPIO_PB11',layer='BOTTOM',width=.2,points=[[36.8,45],[39.2,45]],purpose='Finite2.4mm actual bridge over TOPR27 LIVE vertical, notpower deletion;4L references realL3,2L coplanarguard/groundstitches'),dict(type='route',id='PB11_'+v+'_HEADER_TOP_APPROACH',net='GPIO_PB11',layer='TOP',width=.2,points=[[39.2,45],[41.27,47.07],[41.27,55]],purpose='RealJ12.5 approach frominside east of R27LIVE L and below topheaderV3bus'),dict(type='via',id='PB11_'+v+'_R27_WEST_GND',net='GND',xy=[36.8,44],padstack='L28_VIA030_C060'),dict(type='via',id='PB11_'+v+'_R27_EAST_GND',net='GND',xy=[39.2,44],padstack='L28_VIA030_C060'),dict(type='route',id='PB11_'+v+'_R27_BOTTOM_RETURN_GUARD',net='GND',layer='BOTTOM',width=.6,points=[[36.8,44],[39.2,44]],purpose='True commonGNDguard crossing TOPV3slot on BOTTOM,spans both signaltransition groundvias;2L is finite coplanar return not continuousbroadside reference')]
 checks=[]
 for op in ops:
  if op['type']=='route':checks.append(dict(id=op['id'],clear=s.path_clear(op['net'],op['layer'],op['points'],op['width'])))
  else:
   for l in LAYERS:
    bad,inside=s.forbidden(op['net'],l,.2,True,.001);checks.append(dict(id=op['id'],layer=l,clear=not bad.intersects(Point(op['xy'])) and inside.covers(Point(op['xy']))))
  s.add_operation(op)
 print(v,checks);(O/f'PB11_{v}_61_fixed_review.json').write_text(json.dumps(checks,indent=2));assert all(a['clear']for a in checks)
 p.setdefault('pendingOperations',[]).extend(ops);p['componentAnchors'].append(dict(net='GPIO_PB11',key='PB11_HEADER_ENGINEERED_PORT',xy=[36.8,45],layers=['TOP','BOTTOM'],connectedTo='J12.5',replacePinAccess=True));p['bottomCost']=1.2;p['viaCostMM']=3
 for typ,z in [('snapshot',n),('networks',w),('rules',r),('policy',p)]: (O/f'PB11_{v}_61_{typ}.json').write_text(json.dumps(z,indent=2))