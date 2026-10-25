import pathlib,json,math,sys,hashlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
v='4L';n=load(P/'PB15_attach_4L_87_snapshot.json');nw=load(P/'PB15_attach_4L_87_networks.json');rs=load(P/'PB15_attach_4L_87_rules.json');p=load(P/'PB15_attach_4L_87_policy.json');p.pop('routeWindows',None)
ops=[]
def via(net,xy,small=True):ops.append(dict(type='via',id=f'PB15_95_{net}_V{len(ops)}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT' if small else 'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3))
def rt(layer,points):ops.append(dict(type='route',id=f'PB15_95_R{len(ops)}',net='GPIO_PB15',layer=layer,points=points,width=.2))
rt('BOTTOM',[[47.1,23.3],[47.6,23.8],[48.7,23.8],[48.9,23.68]])
via('GPIO_PB15',[48.9,23.68]);rt('L2',[[48.9,23.68],[49,23.78],[49,25.75],[52.2,28.95],[52.2,30.8],[51.6,31.4]]);via('GPIO_PB15',[51.6,31.4]);via('GND',[50.7,31.3],False)
rt('BOTTOM',[[51.6,31.4],[51.2,31.8],[51.2,39.6],[52.3,40.7]])
via('GPIO_PB15',[52.3,40.7]);via('GND',[53.1,40.7],False);rt('TOP',[[52.3,40.7],[52.3,42.4]]);via('GPIO_PB15',[52.3,42.4]);via('GND',[53.4,42.4],False)
rt('BOTTOM',[[52.3,42.4],[58.19,48.29],[58.19,55]])
s=CopperScene(n,nw,rs,p)
for o in s.obstacles:
 if o['kind']=='via'and o['source']=='native_via':
  cc=o['geometry'].centroid;vv=next(z for z in n['vias']if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(vv.get('padDiameterMM',.52 if '026_C052'in vv['padstack'].upper()else .6)/2,quad_segs=16)
for op in ops:
 if op['type']=='via' or op.get('layer')in LAYERS:s.add_operation(op)
checks=[]
for op in ops:
 if op.get('layer')=='L2':continue
 gg=Point(op['xy'])if op['type']=='via'else LineString(op['points']);rr=op['padDiameterMM']/2 if op['type']=='via'else .1;hits=[]
 for lay in LAYERS if op['type']=='via'else[op['layer']]:
  for o in s.obstacles:
   if o['net']==op['net']or o['layer']!=lay:continue
   d=gg.distance(o['geometry'])-rr;g=s.space(op['net'],o['net'],lay,o['kind'],op['type']=='via')
   if d<g:hits.append(dict(layer=lay,net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=d,required=g))
  for z in p['reservedAreas']:
   if lay in z.get('layers',LAYERS)and op['net']not in z.get('allowedNets',[])and gg.distance(Polygon(z['polygon']))<rr+.001:hits.append(dict(reservation=z['id']))
 checks.append(dict(id=op['id'],clear=not hits,hits=hits))
# L2 uses only a conservative through-pad inventory; GND dynamic copper must be repoured/verified natively.
line=LineString(next(o['points']for o in ops if o.get('layer')=='L2'));innerHits=[]
for z in n['vias']:
 if z['net']=='GPIO_PB15':continue
 dia=z.get('padDiameterMM',.52 if '026_C052'in z['padstack'].upper()else .6);g=.3 if z['net']=='GND'else .2;d=line.distance(Point(z['xy']))-dia/2-.1
 if d<g:innerHits.append(dict(net=z['net'],xy=z['xy'],gap=d,required=g))
for q in s.pins.values():
 if not q.get('through')or q.get('synthetic')or q['net']=='GPIO_PB15':continue
 d=line.distance(q['geom'])-.1;g=.3 if q['net']in['V3V3','GND']else .2
 if d<g:innerHits.append(dict(pin=q['key'],gap=d,required=g))
checks.append(dict(id='L2_CONSERVATIVE_THROUGH_PAD_CHECK',clear=not innerHits,hits=innerHits))
lengths={layer:sum(LineString(o['points']).length for o in ops if o.get('layer')==layer)for layer in ['TOP','BOTTOM','L2']}
prefix=next(o for o in load(P/'PB15_attach_4L_87_delta.json')if o['type']=='route'and o['net']=='GPIO_PB15')
sourceTop=sum(LineString(z['startEnd']).length for z in n['routes']if z['net']=='GPIO_PB15'and z['layer']=='ETCH/TOP'and not z.get('generatedThermal'))
data=dict(status='ENGINEERING_COMPARISON_ONLY_NEW_L2_ROUTE_NOT_AUTHORIZED_NATIVE',variant='4L',base='PB15_attach_4L_87 derived b016 + North51 + existing 81 four-net candidates; final must rebase actual b019',sourcePrerequisites='87 ATTACH+.14 and PB1-L change require root/native review',operations=ops,proofs=[dict(fromTerminal='U1.28',toTerminal='J13.3',expectedConnected=True)],checks=checks,signalLength=dict(sourceTOPmm=sourceTop,sourcePortalBOTTOMmm=LineString(prefix['points']).length,newByLayerMM=lengths,totalMM=sourceTop+LineString(prefix['points']).length+sum(lengths.values())),returnPlan=[dict(signalVia=[48.9,23.68],groundVia=[48.2,25],distanceMM=math.dist([48.9,23.68],[48.2,25]),groundRole='Existing actual common-GND return via retained'),dict(signalVia=[51.6,31.4],groundVia=[50.7,31.3],distanceMM=math.dist([51.6,31.4],[50.7,31.3]),groundRole='New common-GND PTH required'),dict(signalVia=[52.3,40.7],groundVia=[53.1,40.7],distanceMM=.8,groundRole='New common-GND PTH required'),dict(signalVia=[52.3,42.4],groundVia=[53.4,42.4],distanceMM=1.1,groundRole='New common-GND PTH required')],requiredNativeRules=['Finite L2 GPIO_PB15 physical allowEtch width.20, inherited spacing preserved; global L2 other signals still no etch','Private via approval all four conductor layers at exact new signal-via points','No broad spacing or neck relaxation'],pending=['Root engineering choice whether L2 short bridge is preferable to outer-layer ordinary-bank relayout','L2 exact actual pad shapes, void and ref-layer patch connectivity','TOP-reference consequences of about9.34mm L2 slot with explicit field-width buffer, and continuous L3 return','All new GND vias true common-terminal graph, no floating patches','Fresh native scoped/full DRC, all pin edges, USB/HSE negatives and wholeboard counts'])
(P/'PB15_4L_short_L2_comparison_95.json').write_text(json.dumps(data,indent=2),encoding='utf8');print(json.dumps(dict(checks=checks,lengths=data['signalLength'])))


