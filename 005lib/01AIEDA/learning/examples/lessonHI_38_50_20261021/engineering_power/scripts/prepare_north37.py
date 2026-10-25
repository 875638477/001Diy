from pathlib import Path
import sys,json,math,copy
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import load
P=H/'engineering_mcu/plans';O=H/'engineering_power';
for v in ['2L','4L']:
 n=load(P/f'GPIO_future_{v}_36_snapshot.json');w=load(P/f'GPIO_future_{v}_36_networks.json');r=load(P/f'GPIO_future_{v}_36_rules.json');p=load(P/f'GPIO_future_{v}_36_policy.json');ops=[]
 for net in ['GPIO_PC13','GPIO_PC15','GPIO_PC14']:
  for rr in list(n['routes']):
   if rr['net']==net and rr['layer']=='ETCH/BOTTOM':
    op=dict(type='deleteSegment',id='N37_RIP_'+net+'_'+str(len(ops)),net=net,layer='BOTTOM',points=rr['startEnd'],width=rr['width']);ops.append(op);n['routes'].remove(rr)
  if net=='GPIO_PC14':
   vv=[a for a in n['vias'] if a['net']==net and math.dist(a['xy'],[49.2,25.2])<1e-6];assert len(vv)==1;n['vias'].remove(vv[0]);ops.insert(0,dict(type='deleteVia',id='N37_RIP_PC14_REMOTE_VIA',net=net,xy=[49.2,25.2],padstack='L28_VIA030_C060'))
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PC13':a['xy']=[42,28.9];a['layers']=['BOTTOM','TOP']
  if a['net']=='GPIO_PC15':a['xy']=[40.3,28.9];a['layers']=['BOTTOM','TOP']
  if a['net']=='GPIO_PC14':a['xy']=[41,27.8];a['layers']=['BOTTOM','TOP']
 p['viaCostMM']=3;p['bottomCost']=1.1
 for a in p['componentAnchors']:
  if a['net'] in ['GPIO_PA1','GPIO_PA2','GPIO_PA3']:a['layers']=['TOP','BOTTOM']
 (O/f'N37_base_{v}.json').write_text(json.dumps(dict(operations=ops,reason='Research only: remove PC bar fences and remote stub; retain all original source-via to MCU TOP paths.'),indent=2))
 for typ,data in [('snapshot',n),('networks',w),('rules',r),('policy',p)]: (O/f'N37_{v}_{typ}.json').write_text(json.dumps(data,indent=2))
 print(v,len(ops))