import pathlib,json,sys,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'))
from routing_geometry import CopperScene,load,Point
nets=['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']
for v in ['2L','4L']:
 n=load(P/f'GPIO_actualB016_{v}_59_snapshot.json');nw=load(P/f'GPIO_actualB016_{v}_59_networks.json');r=load(P/f'GPIO_actualB016_{v}_59_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json');zz=[z for z in n['vias'] if z['net']=='GND' and math.dist(z['xy'],[37.4,27.4])<1e-5];assert len(zz)==(1 if v=='2L' else 0);[n['vias'].remove(z) for z in zz];s=CopperScene(n,nw,r,p)
 for o in s.obstacles:
  if o['kind']=='via' and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias'] if math.dist(z['xy'],[cc.x,cc.y])<1e-5);o['geometry']=Point(vv['xy']).buffer(.26 if '026_C052' in vv['padstack'].upper() else .3,quad_segs=16)
 ops=[];checks=[]
 for i,net in enumerate(nets):
  x=round(35+.6*i,2);target=[36.19+2.54*i,55] if i<6 else [58.19,55]
  pts=([[x,44.4],[x,55-(target[0]-x)],target] if 55-(target[0]-x)>=44.4 else [[x,44.4],[target[0]-10.6,44.4],target]) if i<6 else [[38.6,43.8],[46.99,43.8],target]
  op=dict(type='route',id=f'GPIO_{v}_{net}_TARGET64',net=net,layer='BOTTOM',points=pts,width=.2,purpose='Manual target escape to original PTH header; source transition candidate pending')
  clear=s.path_clear(net,'BOTTOM',pts,.2);checks.append(dict(net=net,clear=clear,points=pts));ops.append(op);s.add_operation(op)
  key=f'{net}_TARGET64';p['componentAnchors'].append(dict(key=key,net=net,connectedTo=f'J12.{i+3}' if i<6 else 'J13.3',xy=([38.6,43.8] if i==6 else [x,44.4]),layers=['BOTTOM'],replacePinAccess=True))
 p['pendingOperations']=ops
 for typ,z in [('snapshot',n),('networks',nw),('rules',r),('policy',p)]: (P/f'GPIO_TARGET64_{v}_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 (P/f'GPIO_TARGET64_{v}_check.json').write_text(json.dumps(checks,indent=2),encoding='utf8');print(v,checks)




