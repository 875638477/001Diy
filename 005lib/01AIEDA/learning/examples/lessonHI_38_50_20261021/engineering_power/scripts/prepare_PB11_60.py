from pathlib import Path
import sys,json,copy
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
P=H/'engineering_mcu/plans';O=H/'engineering_power'
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');w=load(P/f'GPIO_actualB016_{v}_59_networks.json');r=load(P/f'GPIO_actualB016_{v}_59_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');s=CopperScene(n,w,r,p);leg=dict(type='route',id='PB11_'+v+'_HEADER_TOP_APPROACH',net='GPIO_PB11',layer='TOP',width=.2,points=[[30.4,53.7],[41.27,53.7],[41.27,55]],purpose='Approach realJ12.5 frombelow; stay below oldV3verticalstart55 and aboveR27horizontal47 by going aroundits westend31.11. No criticalpower ripup.')
 print(v,'targetlegClear',s.path_clear('GPIO_PB11','TOP',leg['points'],.2));assert s.path_clear('GPIO_PB11','TOP',leg['points'],.2)
 p.setdefault('pendingOperations',[]).append(leg);p['componentAnchors'].append(dict(net='GPIO_PB11',key='PB11_HEADER_ENGINEERED_PORT',xy=[30.4,53.7],layers=['TOP'],connectedTo='J12.5',replacePinAccess=True));p['bottomCost']=1.2;p['viaCostMM']=3
 for typ,z in [('snapshot',n),('networks',w),('rules',r),('policy',p)]: (O/f'PB11_{v}_60_{typ}.json').write_text(json.dumps(z,indent=2))