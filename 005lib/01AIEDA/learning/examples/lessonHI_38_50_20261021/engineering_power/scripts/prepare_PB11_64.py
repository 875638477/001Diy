from pathlib import Path
import sys,json,copy
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
P=H/'engineering_mcu/plans';O=H/'engineering_power'
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');w=load(P/f'GPIO_actualB016_{v}_59_networks.json');r=load(P/f'GPIO_actualB016_{v}_59_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');others=[a for a in load(P/f'GPIO_TARGET63_{v}_policy.json').get('pendingOperations',[]) if a['net']!='GPIO_PB11'];p['pendingOperations']=others;s=CopperScene(n,w,r,p)
 for a in others:s.add_operation(a)
 ops=[dict(type='via',id='PB11_'+v+'_HEADER_TRANSITION',net='GPIO_PB11',xy=[36.2,43.9],padstack='L28_VIA030_C060',purpose='Only retain if incoming sourcepath is TOP; drop if final sourcepath remains BOTTOM to avoid idle signalvia'),dict(type='route',id='PB11_'+v+'_HEADER_BOTTOM_APPROACH',net='GPIO_PB11',layer='BOTTOM',width=.2,points=[[36.2,43.9],[36.2,49.93],[41.27,55]],purpose='Joint targetbus PB11 lane; finite orthogonal crossing TOPR27 LIVE y47, no power ripup'),dict(type='via',id='PB11_'+v+'_POWER_CROSS_RETURN_LOW',net='GND',xy=[34.1,44],padstack='L28_VIA030_C060'),dict(type='via',id='PB11_'+v+'_POWER_CROSS_RETURN_HIGH',net='GND',xy=[34.1,48],padstack='L28_VIA030_C060'),dict(type='route',id='PB11_'+v+'_POWER_CROSS_BOTTOM_GND_GUARD',net='GND',layer='BOTTOM',width=.6,points=[[34.1,44],[34.1,48]],purpose='Real commonGND crosses TOPR27 horizontal power opening outside sixBOTTOM GPIO lanes, linking actualTOP reference regions after fill; not continuous microstrip or GPIOhighspeed certification')]
 checks=[]
 for op in ops:
  if op['type']=='route':checks.append(dict(id=op['id'],clear=s.path_clear(op['net'],op['layer'],op['points'],op['width'])))
  else:
   for l in LAYERS:
    bad,inside=s.forbidden(op['net'],l,.2,True,.001);checks.append(dict(id=op['id'],layer=l,clear=not bad.intersects(Point(op['xy'])) and inside.covers(Point(op['xy']))))
  s.add_operation(op)
 print(v,checks);(O/f'PB11_{v}_64_fixed_review.json').write_text(json.dumps(checks,indent=2));assert all(a['clear']for a in checks)
 p['pendingOperations']=others+ops;p['componentAnchors'].append(dict(net='GPIO_PB11',key='PB11_HEADER_ENGINEERED_PORT',xy=[36.2,43.9],layers=['TOP','BOTTOM'],connectedTo='J12.5',replacePinAccess=True));p['bottomCost']=1.2;p['viaCostMM']=3
 for typ,z in [('snapshot',n),('networks',w),('rules',r),('policy',p)]: (O/f'PB11_{v}_64_{typ}.json').write_text(json.dumps(z,indent=2))