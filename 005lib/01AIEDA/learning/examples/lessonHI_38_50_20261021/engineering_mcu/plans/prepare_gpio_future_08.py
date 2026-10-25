import pathlib,json
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');P=R/'plans'
s=(P/'plan_gpio_future_local_07.py').read_text(encoding='utf-8-sig')
s=s.replace("starts,viaMasks=scene.masks(net,width,step)",'''# A fine nominal mask is followed by exact continuous path_clear on every segment.
 oldMasks=scene.masks
 def exact_masks(net,width,step):
  xs=np.arange(0,80+step/2,step);ys=np.arange(0,60+step/2,step);xx,yy=np.meshgrid(xs,ys);mm=[];vv=[]
  for lay in LAYERS:
   bad,inside=scene.forbidden(net,lay,width,False,.001);mm.append(shapely.contains_xy(bad,xx,yy)|~shapely.contains_xy(inside,xx,yy))
   bad,inside=scene.forbidden(net,lay,width,True,.001);vv.append(shapely.contains_xy(bad,xx,yy)|~shapely.contains_xy(inside,xx,yy))
  return mm,vv
 starts,viaMasks=exact_masks(net,width,step)''')
s=s.replace('from routing_geometry import CopperScene,load,LAYERS,ROOT,Point','from routing_geometry import CopperScene,load,LAYERS,ROOT,Point,np,shapely')
(P/'plan_gpio_future_local_08.py').write_text(s,encoding='utf8')
for v in ('4L','2L'):
 n=json.loads((P/f'GPIO_future_{v}_07_snapshot.json').read_text());pol=json.loads((P/f'GPIO_future_{v}_07_policy.json').read_text());
 # Root declared future VBUS_PRESENT_N inner source + common ground.
 if v=='4L':n['vias'].append(dict(net='GND',xy=[37.4,27.4],padstack='L28_VIA030_C060',padDiameterMM=.6,drillDiameterMM=.3,futureCandidate='ROOT_VBUS_RETURN_STITCH'))
 n['vias'].append(dict(net='VBUS_PRESENT_N',xy=[36.5,27.6],padstack='L28_VIA030_C060',padDiameterMM=.6,drillDiameterMM=.3,futureCandidate='ROOT_VBUS_PRESENT_N_SOURCE'))
 for a,b in zip([[35.75,27.25],[36.15,27.25],[36.5,27.6]],[[36.15,27.25],[36.5,27.6]]):n['routes'].append(dict(kind='line',net='VBUS_PRESENT_N',layer='ETCH/TOP',startEnd=[a,b],width=.2,generatedThermal=False,fixedManualCline=True,futureCandidate='ROOT_VBUS_PRESENT_N_SOURCE'))
 for typ,data in [('snapshot',n),('policy',pol)]: (P/f'GPIO_future_{v}_08_{typ}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
print('nominal masks + exact continuous geometry; source obstacles updated')
