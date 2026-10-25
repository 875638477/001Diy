from pathlib import Path
import sys,json,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power'
plans=[('GPIO_PC13','BOTTOM',[[42,28.9],[41.3,28.9],[35.25,34.95],[34.05,34.95]]),('GPIO_PC15','BOTTOM',[[40.3,28.9],[40.3,29],[34.8,34.5],[33.55,34.5]]),('GPIO_PA1','BOTTOM',[[37.5,29.6],[37.5,30.9],[34.4,34.0]]),('GPIO_PA2','BOTTOM',[[36.6,30.4],[36.6,31.1],[34.1,33.6]]),('GPIO_PA3','BOTTOM',[[35.2,31.65],[33.7,33.15]])]
for v in ['2L','4L']:
 n=load(O/f'N37_{v}_snapshot.json');w=load(O/f'N37_{v}_networks.json');r=load(O/f'N37_{v}_rules.json');p=load(O/f'N37_{v}_policy.json');p['pendingOperations']=[];s=CopperScene(n,w,r,p);ops=[];checks=[]
 for i,(net,l,pts) in enumerate(plans):
  op=dict(type='route',id='N39_'+net+'_ACCESS',net=net,layer=l,points=pts,width=.2,purpose='Joint parallel bottom access corridor; preserve original MCU-to-via TOP connection; complete long paths/actual returns pending')
  checks.append(dict(net=net,clear=s.path_clear(net,l,pts,.2)));ops.append(op);s.add_operation(op)
  for a in p['componentAnchors']:
   if a['net']==net:a['xy']=pts[-1];a['layers']=['BOTTOM']
 extra=[dict(type='route',id='N39_PC14_TOP_TEMP',net='GPIO_PC14',layer='TOP',points=[[41,27.8],[41,29.15],[41.5,29.65]],width=.2),dict(type='via',id='N39_PC14_VIA',net='GPIO_PC14',xy=[41.5,29.65],padstack='L28_VIA030_C060'),dict(type='route',id='N39_PC14_ACCESS',net='GPIO_PC14',layer='BOTTOM',points=[[41.5,29.65],[35.05,36.1]],width=.2)]
 for op in extra:
  if op['type']=='route':checks.append(dict(net=op['net'],clear=s.path_clear(op['net'],op['layer'],op['points'],.2)))
  s.add_operation(op)
 ops.extend(extra)
 for a in p['componentAnchors']:
  if a['net']=='GPIO_PC14':a['xy']=[35.05,36.1];a['layers']=['BOTTOM']
 p['pendingOperations']=ops;p['bottomCost']=1.1;p['viaCostMM']=2
 for t,d in [('snapshot',n),('networks',w),('rules',r),('policy',p)]: (O/f'N39_{v}_{t}.json').write_text(json.dumps(d,indent=2))
 (O/f'N39_{v}_access_review.json').write_text(json.dumps(checks,indent=2));print(v,checks)