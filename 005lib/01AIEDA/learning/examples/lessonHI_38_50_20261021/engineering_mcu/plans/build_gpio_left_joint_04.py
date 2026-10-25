import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
old=[('GND',[[35.75,24.75],[34.95,24.75]],.25),('GND',[[34.95,24.75],[34.55,25.15]],.25),('GND',[[34.55,25.15],[33.4,25.2748]],.6),('GND',[[33.4,25.2748],[32.45,25.2748]],.6),('V3V3',[[35.75,24.25],[34.95,24.25]],.25),('V3V3',[[34.95,24.25],[34.55,23.85]],.25),('V3V3',[[34.55,23.85],[33.4,23.7]],.6),('V3V3',[[33.3,22.5],[33.3,24]],.6),('V3V3',[[33.3,24],[37,24]],.6)]
ops=[dict(type='deleteSegment',id='LEFT_RIP_'+str(i),net=net,layer='TOP',points=pts,width=w) for i,(net,pts,w) in enumerate(old)]
ops.extend([dict(type='route',id='LEFT_C13_VDD24_NECK',net='V3V3',layer='TOP',points=[[35.75,24.25],[35.1,23.6],[35.1,23.2]],width=.25),dict(type='route',id='LEFT_C13_VDD24_WIDE',net='V3V3',layer='TOP',points=[[35.1,23.2],[34.5,22.6],[34.0,22.6]],width=.6),dict(type='route',id='LEFT_C13_VSS23_NECK',net='GND',layer='TOP',points=[[35.75,24.75],[34.7,24.75]],width=.25),dict(type='route',id='LEFT_C13_VSS23_WIDE',net='GND',layer='TOP',points=[[34.7,24.75],[34.0,24.05],[34.0,24.1748]],width=.6),dict(type='route',id='LEFT_C13_COMMON_RETURN',net='GND',layer='TOP',points=[[34.0,24.1748],[33.55,24.1748],[32.45,25.2748]],width=.6),dict(type='route',id='LEFT_V3_PERIPHERAL_REROUTE',net='V3V3',layer='TOP',points=[[33.3,22.5],[34.8,22.5],[36,23.7],[37,24]],width=.6)])
for pin,net,xy,pts in [(19,'GPIO_PB1',[34.55,26.75],[[35.75,26.75],[34.55,26.75]]),(21,'GPIO_PB10',[38,26.4],[[35.75,25.75],[36.65,25.75],[37.3,26.4],[38,26.4]]),(22,'GPIO_PB11',[33.5,25.3],[[35.75,25.25],[35,25.25],[34.75,25.5],[33.7,25.5],[33.5,25.3]])]:
 ops.extend([dict(type='route',id='LEFT_SOURCE_'+str(pin)+'_NECK',net=net,layer='TOP',points=pts,width=.16),dict(type='via',id='LEFT_SOURCE_'+str(pin)+'_VIA',net=net,xy=xy,padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26)])
ops.append(dict(type='via',id='LEFT_GPIO_COMMON_RETURN',net='GND',xy=[33.28,26.0],padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26))
p=dict(status='ENGINEERING_SOURCE_CANDIDATE_NOT_NATIVE_APPROVAL',batchId='GPIO_left_joint_fanout_04',placementChanges=[dict(ref='C13',xy=[34.0,22.4984],rotation=90,purpose='Move +.6X/-1.1Y to release leftGPIO bank while preserving direct TOP cap loops; VDD leg slightly longer, VSS leg shorter, total loop length modestly reduced.')],operations=ops,partialEndpoints={'GPIO_PB1':dict(xy=[34.55,26.75],layer='BOTTOM',connectedTo='U1.19'),'GPIO_PB10':dict(xy=[38,26.4],layer='BOTTOM',connectedTo='U1.21'),'GPIO_PB11':dict(xy=[33.5,25.3],layer='BOTTOM',connectedTo='U1.22')},replacePendingOperationIds=['HI_4L_BOOT1_1_R2','HI_2L_BOOT1_1_R2'],pendingReplacement=dict(type='route',id='LEFT_BOOT1_BOTTOM_RESHAPE',net='BOOT1',layer='BOTTOM',points=[[34.4,26],[35.6,24.8],[35.6,23.85],[32.35,23.85]],width=.2,purpose='Only replace unexecuted root BOOT1 source-bottom route; all existing destination/source terminal connectivity preserved.'),physicalExceptions=[dict(id='HI_LEFT_DIGITAL_SOURCE_P',layer='TOP',polygon=[[33.6,24.9],[36.5,24.9],[36.5,25.4],[37.4,25.4],[37.4,27.4],[33.6,27.4]],nets=['GPIO_PB1','GPIO_PB10','GPIO_PB11'],neckWidthMinMM=.16,maxNeckMM=2.6,approvedVias=['L28_VIA030_C060','HI_VIA026_C052_TENT'])],spacingExceptions=[dict(id='HI_LEFT_GND_SOURCE_S',layer='TOP',polygon=[[36.4,25.4],[37.0,25.4],[37,26.9],[36.4,26.9]],netsA=['GPIO_PB10'],netsB=['GND'],onlyFields={'line_line':.20,'smdpin_line':.20},basis='PB10 inward horizontal at36.65,25.75 clears retained VSS23 east return bridge by ~.214; normal .3 elsewhere retained.'),dict(id='HI_LEFT_STITCH_VIA_S',layers=['TOP','BOTTOM'],polygon=[[36.7,26.3],[37.8,26.3],[37.8,27.8],[36.7,27.8]],netsA=['GPIO_PB10'],netsB=['GND'],onlyFields={'via_via':.20},basis='2L native commonTOPstitch37.4,27.4 to sourcevia37,26.7 edge gap~.246; global GND.3 unchanged outside source.')],expectedProofs=[dict(source='U1.24',target='C13.1',net='V3V3',expectedConnected=True),dict(source='U1.23',target='C13.2',net='GND',expectedConnected=True),dict(source='C13.2',target='U1.35',net='GND',expectedConnected=True)],scope='Only learning副本; no netlist, HSE/ADC/USB/mainSPI geometry changes. Readback native DRC/loops/allpins and exact reference proof pending.')

p['replacePendingOperationIds'].extend(['HI_'+v+'_BOOT1_1_V1' for v in ('4L','2L')]+['HI_'+v+'_BOOT1_1_R1' for v in ('4L','2L')])
ops.extend([dict(type='route',id='LEFT_BOOT1_SOURCE_NECK',net='BOOT1',layer='TOP',points=[[35.75,26.25],[35.1,26.25],[34.85,26],[34.4,26]],width=.16),dict(type='via',id='LEFT_BOOT1_SOURCE_VIA',net='BOOT1',xy=[34.4,26],padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26)])
p['physicalExceptions'][0]['nets'].append('BOOT1');p['physicalExceptions'][0]['polygon']=[[33.6,24.9],[36.5,24.9],[36.5,25.4],[38.4,25.4],[38.4,27.4],[33.6,27.4]]
p['expectedProofs'].append(dict(source='U1.20',target='R29.1',net='BOOT1',expectedConnected=True))
p['physicalGroundViaApproval']=dict(xy=[33.28,26.0],delta={'approvedViasAdd':['HI_VIA026_C052_TENT']},scope='Small GND-only region around this exact via, all actual conductive layers; other physical fields copied unchanged.')


p['spacingExceptions'].extend([dict(id='HI_LEFT_DIGITAL_DENSE_S',layer='TOP',polygon=[[33.2,25.0],[35.2,25],[35.2,27.0],[33.2,27.0]],nets=['GPIO_PB1','GPIO_PB11','BOOT1'],onlyFields={'line_line':.16,'via_line':.16,'via_via':.16},basis='BOOT1 privatevia34.4,26 to PB11 .16neck row25.5 edgegap.16. Copy only finite same-digital source fields, parent.2 outside retained.'),dict(id='HI_LEFT_GND11_VIA_S',layers=['TOP','BOTTOM'],polygon=[[32.9,25.0],[33.9,25.0],[33.9,26.35],[32.9,26.35]],netsA=['GPIO_PB11'],netsB=['GND'],onlyFields={'via_via':.20},basis='PrivatecommonGND33.28,26 to sourcevia33.5,25.3 actualgap.2137. GNDglobal.3 outside retained.')])


p['spacingExceptions']=[x for x in p['spacingExceptions'] if x['id']!='HI_LEFT_STITCH_VIA_S']
p['physicalExceptions'][0]['polygon']=[[33.1,24.9],[36.5,24.9],[36.5,25.4],[38.4,25.4],[38.4,27.4],[33.1,27.4]]
for net,ep in p['partialEndpoints'].items():
 actual=[o for o in ops if o['type']=='via' and o['net']==net];assert len(actual)==1 and actual[0]['xy']==ep['xy'],(net,ep,actual)
p['directLoopLengthsMM']={'newVDD24ToC13':1.319238815542512+1.348528137423857,'newVSS23ToC13':1.05+.9899494936611665+.1248,'sourceNeckVDD24':1.319238815542512,'sourceNeckVSS23':1.05,'oldVDD24ToC13':1.365685424949238+1.159741350474602,'oldVSS23ToC13':1.365685424949238+1.1567521416802142,'scope':'Explicit candidate centerline sums, not full inductance/current distribution; native readback and conductive graph proof required.'}

report={'variants':{}}
for v in ('4L','2L'):
 f=H/f'inventory/checkpoints/postcritical_{v}_b010';n=load(f/'normalized.json');baseSHA=hashlib.sha256((f/'normalized.json').read_bytes()).hexdigest();pending=[]
 for q in [load(P/'GPIO_south_joint_fanout_05.json'),load(P/'GPIO_north_joint_fanout_02.json'),p]:
  for c in q.get('placementChanges',[]):
   z=next(a for a in n['placements'] if a['ref']==c['ref']);assert z['rotation']==c['rotation'];dx=c['xy'][0]-z['xy'][0];dy=c['xy'][1]-z['xy'][1]
   for a in z['pins']:a['xy']=[a['xy'][0]+dx,a['xy'][1]+dy];a['padBBox']=[[x+dx,y+dy] for x,y in a['padBBox']]
   z['xy']=c['xy'];z['bodyExtent']=[[x+dx,y+dy] for x,y in z['bodyExtent']]
  for o in q['operations']:
   if o['type']=='deleteSegment':
    ms=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in (o['points'],list(reversed(o['points']))) and abs(r['width']-o['width'])<1e-6];assert len(ms)==1,(o,ms);n['routes'].remove(ms[0])
   elif o['type'] in ('route','via'):pending.append(o)
 for name in (f'ordinary_remote_{v}_v7.json',f'aux_remote_{v}_v8.json',f'CC_entry_{v}_v3.json'):
  for o in load(H/'plans'/name)['operations']:
   if o['id'] not in p['replacePendingOperationIds']:pending.append(o)
 pending.append(p['pendingReplacement'])
 if v=='2L':pending.append(dict(type='via',id='PENDING_NATIVE_FLOAT_STITCH',net='GND',xy=[37.4,27.4],padstack='L28_VIA030_C060'))
 scene=CopperScene(n,load(f/'networks.json'),load(f/'base_net_rules.json'),{})
 allnew=[]
 for o in pending:
  if o['type']=='via':
   for l in LAYERS:allnew.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(o.get('padDiameterMM',.6)/2,quad_segs=48),kind='via',source=o['id']))
  elif o['type']=='route':
   for a,b,w in zip(o['points'],o['points'][1:],o.get('widths',[o['width']]*(len(o['points'])-1))):
    if a!=b:allnew.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(w/2,quad_segs=48),kind='line',source=o['id']))
 wanted=[a for a in allnew if a['source'].startswith('LEFT_')];others=scene.obstacles+[a for a in allnew if not a['source'].startswith('LEFT_')];issues=[];count=0
 for i,a in enumerate(wanted):
  for b in others+wanted[:i]:
   if a['layer']!=b['layer'] or a['net']==b['net']:continue
   count+=1;d=a['geometry'].distance(b['geometry'])
   if d<.15995:issues.append(dict(a=a['source'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d,overlap=a['geometry'].intersects(b['geometry'])))
 c13=next(z for z in n['placements'] if z['ref']=='C13');g=box(*c13['bodyExtent'][0],*c13['bodyExtent'][1]);near=sorted((g.distance(box(*z['bodyExtent'][0],*z['bodyExtent'][1])),z['ref']) for z in n['placements'] if z['ref']!='C13' and z.get('bodyExtent'))[:5]
 report['variants'][v]=dict(sourceCheckpoint=str(f),baseSHA256=baseSHA,comparisons=count,issuesBelowPoint16=issues,newC13PadXY=[(a['number'],a['xy']) for a in c13['pins']],newC13NearestPlaceBounds=near)
(P/'GPIO_left_joint_fanout_04.json').write_text(json.dumps(p,indent=2),encoding='utf8');(P/'GPIO_left_joint_fanout_review_04.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
