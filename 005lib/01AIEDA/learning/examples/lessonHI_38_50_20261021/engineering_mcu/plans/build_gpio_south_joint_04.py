import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
p=load(P/'GPIO_south_joint_fanout_01.json');p['batchId']='GPIO_south_joint_fanout_04';p['status']='ENGINEERED_SOURCE_GROUP_PENDING_NATIVE_DRC_REFERENCE'
ops=p['operations'];by={o['id']:o for o in ops}
by['SOUTH_SOURCE_30_VIA']['xy']=[39.7,21.7];by['SOUTH_SOURCE_30_NECK']['points']=[[39.75,22.75],[39.75,21.75],[39.7,21.7]];p['partialEndpoints']['PA9_UART_TX']['xy']=[39.7,21.7]
by['SOUTH_SOURCE_31_NECK']['points']=[[40.25,22.75],[40.25,22.05],[40.22,22.02],[40.22,21.3],[40,21.08],[40,20.5]]
by['SOUTH_RETURN_WEST']['xy']=[36.1,21.1];by['SOUTH_RETURN_EAST']['xy']=[39.25,20.3]
ops.extend([dict(type='route',id='SOUTH_SOURCE_34_NECK',net='SWDIO',layer='TOP',points=[[41.75,22.75],[41.75,22.1],[41.85,22.0],[41.85,21.6]],width=.16,purpose='Right-of-pair SWDIO finite source escape; actual USB/via reference clearance must pass.'),dict(type='via',id='SOUTH_SOURCE_34_VIA',net='SWDIO',xy=[41.85,21.6],padstack='HI_VIA026_C052_TENTED'),dict(type='via',id='SOUTH_RETURN_SWDIO',net='GND',xy=[42.0,20.7],padstack='HI_VIA026_C052_TENTED')]);p['partialEndpoints']['SWDIO']=dict(xy=[41.85,21.6],layer='BOTTOM',connectedTo='U1.34')
old=[[[39,26.2],[39,21.3]],[[39,21.3],[32.2,21.3]],[[32.2,21.3],[32.2,22]]]
for i,pts in enumerate(old):ops.insert(i,dict(type='deleteSegment',id='SOUTH_RIP_NSS_PULLUP_'+str(i),net='PA4_SPI_NSS',layer='BOTTOM',points=pts,width=.2,purpose='Release south fanout bank by moving only low-current R25 pullup branch; main TOP U1-to-R23 NSS unchanged.'))
ops.append(dict(type='route',id='SOUTH_NSS_PULLUP_RELOCATED',net='PA4_SPI_NSS',layer='BOTTOM',points=[[39,26.2],[39,23.2],[32.2,23.2],[32.2,22]],width=.2,purpose='Preserve same pullup branch endpoints via39,26.2 and32.2,22; altered finite two-layer reference shadow must be checked.'))
p['sourceBranchTradeoff']='Only NSS pullup branch BOTTOM y21.3 is moved to y23.2. Main TOP SPI source/corner/series resistor path unchanged. On2L this moves a finite reference slot under inner end of MCU bottom-row SMD pads and C13 power-node vicinity; inspect direct-TOP local cap/VSS loops and same-layer application-GND returns. Not continuous opposite-plane claim.'
p['physicalExceptions'][0]['polygon']=[[36.6,20],[42.2,20],[42.2,23.4],[36.6,23.4]];p['physicalExceptions'][0]['nets'].append('SWDIO');p['physicalExceptions'][0]['maxNeckMM']=2.4;p['physicalExceptions'][0]['basis']='Longest explicit proposed neck2.353553mm (U1.31 to via40,20.5). Local max2.4 only, parent unchanged; native may include connect graph endpoint differently and must report actual.'
p['spacingExceptions'][0]['onlyFields']={'line_line':.16,'via_line':.16,'via_via':.16};p['spacingExceptions'][0]['layers']=['TOP','BOTTOM'];p['spacingExceptions'][0]['nets'].append('SWDIO')
p['spacingExceptions'].append(dict(id='HI_SOUTH_GND_RX_VIA_ONLY_S',layers=['TOP','BOTTOM'],polygon=[[39,20],[40.4,20],[40.4,21.1],[39,21.1]],netsA=['GND'],netsB=['PA10_UART_RX'],onlyFields={'via_via':.20},basis='Proposed tiny common-GNDvia39.25,20.3 to RXvia40,20.5 actual gap .2562; original GND global .3 unchanged outside finite source transition.'))
p['spacingExceptions'].append(dict(id='HI_SWDIO_USB_VIA_ESCAPE_S',layer='TOP',polygon=[[41.5,21.2],[42.1,21.2],[42.1,23.4],[41.5,23.4]],netsA=['SWDIO'],netsB=['PA12_SHARED'],onlyFields={'via_line':.20},basis='Source via41.85,21.6 copper clears actual sharedDP bend by .3108; original .5 outside source retained.'))
p['privateViaSource']={'name':'hi_via026_c052_tented','spec':'native/private_padstacks/spec.json','status':'Prepared definition only; native import/readback pending.'}
p['remainingSourceTasks']=['Root-integrated source UART_TX via39.7,21.7→movedR16.1; UART_RX R17.1→via40,20.5; PA8Attach partial→Q2; SWDIO partial→serviceheader. These are explicit unresolved joins, not claimed connected.']

# Preserve direct TOP VSS35/cap closure while shortening its previous leftward dogleg.
for o in ops:
 if o['id']=='SOUTH_SOURCE_34_NECK':o['points']=[[41.75,22.75],[41.75,21.7],[41.5,21.45],[41.5,21.25]]
 if o['id']=='SOUTH_SOURCE_34_VIA':o['xy']=[41.5,21.25]
 if o['id']=='SOUTH_RETURN_SWDIO':o['xy']=[42.3,21.35]
p['partialEndpoints']['SWDIO']['xy']=[41.5,21.25]
gndold=[([[42.25,22.75],[42.25,21.95]],.25),([[42.25,21.95],[41.85,21.55]],.25),([[41.85,21.55],[42.3252,21.0748]],.6),([[42.3252,21.0748],[42.3252,20.3]],.6)]
for i,(pts,w) in enumerate(gndold):ops.append(dict(type='deleteSegment',id='SOUTH_RIP_C14_GND_'+str(i),net='GND',layer='TOP',points=pts,width=w,purpose='Shorten existing direct VSS35-C14 TOP return to release SWDIO; retained cap-ground globalvia unchanged.'))
ops.extend([dict(type='route',id='SOUTH_C14_GND_NECK',net='GND',layer='TOP',points=[[42.25,22.75],[42.25,21.36]],width=.25),dict(type='route',id='SOUTH_C14_GND_WIDE',net='GND',layer='TOP',points=[[42.25,21.36],[42.3252,21.2848],[42.3252,20.3]],width=.6)])

for o in ops:
 if o.get('padstack')=='HI_VIA026_C052_TENTED':o['padstack']='hi_via026_c052_tented'
p['directDecouplingLoopChange']='C14/VSS35 remains direct TOP cap return. New source neck1.39mm .25, below inherited1.4mm local allowance; wide return1.091149mm versus old1.446834mm, cap and original globalvia unchanged. Added near-source GNDvia42.3,21.35 supplies SWDIO transition return. Verify actual endpoint graph/native pad/DRC and trace-length ownership.'
p['spacingExceptions'][-1]['onlyFields']={'smdpin_line':.20,'line_line':.20,'via_line':.20};p['spacingExceptions'][-1]['polygon']=[[41.3,21.0],[42.1,21.0],[42.1,23.4],[41.3,23.4]]
p['spacingExceptions'].append(dict(id='HI_SWDIO_GND_VIA_ESCAPE_S',layers=['TOP','BOTTOM'],polygon=[[41.2,21],[42.6,21],[42.6,21.8],[41.2,21.8]],netsA=['SWDIO'],netsB=['GND'],onlyFields={'via_line':.20,'via_via':.20},basis='Tiny signalvia41.5,21.25 to relocated direct TOP GND wide trace and commonGNDvia42.3,21.35: finite .2 transition spacing, GND global.3 elsewhere retained.'))
report={'status':'INDEPENDENT_CANDIDATE_SCREEN_NATIVE_REQUIRED','variants':{}}
for v in ('4L','2L'):
 f=H/f'inventory/checkpoints/postcritical_{v}_b010';n=load(f/'normalized.json');r16=next(c for c in n['placements'] if c['ref']=='R16');dx=36.9016-r16['xy'][0];dy=19.9-r16['xy'][1]
 for pp in r16['pins']:pp['xy']=[pp['xy'][0]+dx,pp['xy'][1]+dy];pp['padBBox']=[[x+dx,y+dy] for x,y in pp['padBBox']]
 r16['xy']=[36.9016,19.9];r16['bodyExtent']=[[x+dx,y+dy] for x,y in r16['bodyExtent']]
 cnt=[]
 for o in ops:
  if o['type']!='deleteSegment':continue
  m=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in (o['points'],list(reversed(o['points']))) and abs(r['width']-o['width'])<1e-8];cnt.append(len(m));assert len(m)==1,(o,m);n['routes'].remove(m[0])
 s=CopperScene(n,load(f/'networks.json'),load(f/'base_net_rules.json'),{})
 if v=='2L':s.add_operation(dict(type='via',net='GND',xy=[37.4,27.4],id='PENDING_FLOAT_STITCH'))
 new=[]
 for o in ops:
  if o['type']=='via':
   for l in LAYERS:new.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(.26,quad_segs=64),kind='via',source=o['id']))
  elif o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):
    if a!=b:new.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(o['width']/2,quad_segs=64),kind='line',source=o['id']))
 issues=[];below20=[];checks=0
 for i,a in enumerate(new):
  for b in s.obstacles+new[:i]:
   if a['layer']!=b['layer'] or a['net']==b['net']:continue
   checks+=1;d=a['geometry'].distance(b['geometry'])
   if d<.19995:below20.append(dict(a=a['source'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d))
   if d<.15995:issues.append(dict(a=a['source'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d,overlap=a['geometry'].intersects(b['geometry'])))
 rv=[];gs=[o['xy'] for o in ops if o['type']=='via' and o['net']=='GND']+[z['xy'] for z in n['vias'] if z['net']=='GND' and z['xy'] not in ([45.45,28.85],[47.1,35.5748],[37.7,37.7])]
 for o in ops:
  if o['type']=='via' and o['net']!='GND':
   d,xy=min((math.dist(o['xy'],xy),xy) for xy in gs);rv.append(dict(id=o['id'],distance=d,commonGNDvia=xy,within1Point5=d<=1.5))
 report['variants'][v]=dict(source=str(f),sourceSHA256=hashlib.sha256((f/'normalized.json').read_bytes()).hexdigest(),uniqueNSSPullupDeleteCounts=cnt,comparisons=checks,issuesBelowPoint16=issues,explicitGapBelowPoint20=below20,sourceViaReturnDistances=rv,neckLengths={o['net']:LineString(o['points']).length for o in ops if o['type']=='route' and o['id'].startswith('SOUTH_SOURCE')})
(P/'GPIO_south_joint_fanout_04.json').write_text(json.dumps(p,indent=2),encoding='utf8');(P/'GPIO_south_joint_fanout_review_04.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({v:{'comparisons':d['comparisons'],'issues16':d['issuesBelowPoint16'],'countExplicitSub20':len(d['explicitGapBelowPoint20']),'return':d['sourceViaReturnDistances']} for v,d in report['variants'].items()},indent=2))
