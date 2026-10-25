import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
for v in ['2L','4L']:
 n=load(H/f'review/b020_engineering/PB10_NW_{v}_v46_snapshot.json');B=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');p=load(P/f'GPIO_PB1_inward_{v}_80_policy.json');p['pendingOperations']=[]
 ops=[]
 def via(net,xy,small=True):ops.append(dict(type='via',id=f'PB10_93_{net}_V{len(ops)}',net=net,xy=xy,padstack='HI_VIA026_C052_TENT'if small else'L28_VIA030_C060',padDiameterMM=.52 if small else .6,drillDiameterMM=.26 if small else .3))
 def rt(net,l,pts,w):ops.append(dict(type='route',id=f'PB10_93_R{len(ops)}',net=net,layer=l,points=pts,width=w))
 rt('GPIO_PB10','TOP',[[28,36.1],[27.8,36.1]],.2);via('GPIO_PB10',[27.8,36.1]);rt('GPIO_PB10','BOTTOM',[[27.8,36.1],[27.8,37.94]],.2);via('GPIO_PB10',[27.8,37.94]);rt('GPIO_PB10','TOP',[[27.8,37.94],[27.8,44.5],[34.8,44.5]],.2);via('GPIO_PB10',[34.8,44.5]);rt('GPIO_PB10','BOTTOM',[[34.8,44.5],[34.8,51.07],[38.73,55]],.2)
 via('GND',[26.8,36.08],False);via('GND',[26.8,37.94],False);rt('GND','BOTTOM',[[26.8,36.08],[26.8,37.94]],.6);via('GND',[35.8,44.5],False);via('GND',[33.5,45.8],False);via('GND',[33.5,48.2],False);rt('GND','BOTTOM',[[33.5,45.8],[33.5,48.2]],.6)
 s=CopperScene(n,nw,rs,p)
 for o in s.obstacles:
  if o['kind']=='via'and o['source']=='native_via':
   cc=o['geometry'].centroid;vv=next(z for z in n['vias']if math.dist(z['xy'],[cc.x,cc.y])<1e-6);o['geometry']=Point(vv['xy']).buffer(vv.get('padDiameterMM',.52 if '026_C052'in vv['padstack'].upper()else .6)/2,quad_segs=16)
 for op in ops:s.add_operation(op)
 checks=[]
 for op in ops:
  gg=Point(op['xy'])if op['type']=='via'else LineString(op['points']);rr=op['padDiameterMM']/2 if op['type']=='via'else op['width']/2;hits=[]
  for lay in LAYERS if op['type']=='via'else[op['layer']]:
   for o in s.obstacles:
    if o['net']==op['net']or o['layer']!=lay:continue
    d=gg.distance(o['geometry'])-rr;g=s.space(op['net'],o['net'],lay,o['kind'],op['type']=='via')
    if d<g:hits.append(dict(layer=lay,net=o['net'],kind=o['kind'],source=o['source'],bbox=o['geometry'].bounds,gap=d,required=g))
   for z in p['reservedAreas']:
    if lay in z.get('layers',LAYERS)and op['net']not in z.get('allowedNets',[])and gg.distance(Polygon(z['polygon']))<rr+.001:hits.append(dict(reservation=z['id']))
  checks.append(dict(id=op['id'],clear=not hits,hits=hits))
 sourceLen=sum(math.dist(*z['startEnd'])for z in n['routes']if z['net']=='GPIO_PB10'and not z.get('generatedThermal'));newLen=sum(LineString(z['points']).length for z in ops if z['net']=='GPIO_PB10'and z['type']=='route')
 data=dict(status='PB10_ORIGINAL_HEADER_MANUAL_COMPARISON_NOT_NATIVE',variant=v,source='b019 + f29 candidate46; originalJ12 unchanged; other81southpaths NOT included because this is target-layout comparison',operations=ops,checks=checks,signalLengthMM=sourceLen+newLen,sourceLengthMM=sourceLen,newLengthMM=newLen,returnPlan='New actual common-GND stitches and BOTTOM .6 bridges at x26.8 across TOP V3prefilter and x33.5 across LIVE V3 y47; native graph/fill/field-width review pending',pending=['All7 original-header complete routing not yet established','f29 North4 candidate46 native and reference review','Native true plane connectivity and guards + no floating branches','Private via four-layer finite permission at new signal points'])
 (P/f'PB10_original_header_{v}_93.json').write_text(json.dumps(data,indent=2),encoding='utf8');print(v,json.dumps(data))
