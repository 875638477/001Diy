import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
refs=[('GPIO_PB12',25,37.25,[37,21.25]),('GPIO_PB13',26,37.75,[37.5,20.75]),('GPIO_PB14',27,38.25,[38,21.25]),('GPIO_PB15',28,38.75,[38.5,20.7]),('USB_ATTACH_N',29,39.25,[39,21.2]),('PA9_UART_TX',30,39.75,[39.5,21.7]),('PA10_UART_RX',31,40.25,[40,20.5])]
ops=[];ends={}
for net,pin,x,xy in refs:
 pts=[[x,22.75],[x,22.1],[x-.25,21.85],xy] if pin<30 else [[x,22.75],[x,22.05],[x-.25,21.8],xy]
 tag='SOUTH_SOURCE_'+str(pin)
 ops.append(dict(type='route',id=tag+'_NECK',net=net,layer='TOP',points=pts,width=.16,purpose='Finite dense-source neck before private staggered PTH via; outside source window normal .20mm remains.'))
 ops.append(dict(type='via',id=tag+'_VIA',net=net,xy=xy,padstack='HI_VIA026_C052_TENTED',purpose='Private PTH .26drill/.52Cu, .13annulus, no mask aperture; only source region approved variant, native definition verification pending.'))
 ends[net]=dict(xy=xy,layer='BOTTOM',connectedTo='U1.'+str(pin))
for tag,xy in [('WEST',[36.3,21.1]),('MID',[38.0,20.0]),('EAST',[39.25,20.25])]:ops.append(dict(type='via',id='SOUTH_RETURN_'+tag,net='GND',xy=xy,padstack='HI_VIA026_C052_TENTED',purpose='Dense-source common-plane return stitch, requires actual application GND attachment/branch proof; not quiet HSE.'))
p=dict(status='SOURCE_GROUP_GEOMETRY_CANDIDATE_NOT_NATIVE_APPROVED',batchId='GPIO_south_joint_fanout_01',placementChanges=[dict(ref='R16',xy=[36.9016,19.9],rotation=180,purpose='Free south GPIO/UART fanout window while preserving 33R electrical identity; pin1(36.8,19.9),pin2(35.2252,19.9).')],operations=ops,partialEndpoints=ends,physicalExceptions=[dict(id='HI_SOUTH_DENSE_SOURCE_P',layer='TOP',polygon=[[36.6,20.0],[40.55,20.0],[40.55,23.4],[36.6,23.4]],nets=[x[0] for x in refs],neckWidthMinMM=.16,maxNeckMM=2.9,approvedVias=['L28_VIA030_C060','HI_VIA026_C052_TENTED'],basis='Smallest dense source-only physical clone; parent normal .20 and global exception unchanged. Proposed longest neck22.75→20.5 with.25diagonal=2.35355mm; budget2.9 is provisional needs exact native final length, prefer lower2.4 if sufficient.')],spacingExceptions=[dict(id='HI_SOUTH_DIGITAL_VIA_ESCAPE_S',layer='TOP',polygon=[[36.6,20.0],[40.55,20.0],[40.55,23.4],[36.6,23.4]],nets=[x[0] for x in refs],onlyFields={'via_line':.16,'via_via':.16},basis='0.5pitch adjacent .52via and .16line yields .16 copper gap; staggered via centers .7071 give .1871 edge gap. All other spacing preserved unless actual source screen proves necessary.'),dict(id='HI_UART_RX_USB_ESCAPE_S',layer='TOP',polygon=[[39.65,20.0],[40.55,20.0],[40.55,22.15],[39.65,22.15]],netsA=['PA10_UART_RX'],netsB=['PA11_SHARED','PA12_SHARED'],onlyFields={'via_line':.20,'line_line':.20},basis='UART_RX source via40,20.5 to DM trunk40.6 exact edge gap.24; outside USB-other .5 unchanged. Actual reference antipad and return transition must be inspected.')],remainingSourceTasks=['Route PA9_UART_TX source partial to moved R16.1; receiver-side UART_R17.1 to PA10 partial; USB_ATTACH partial to Q2 remain root-integrated paths.','SWDIO U1.34 source fanout still pending independent right-of-USB geometry; no source slot reserved blindly.'],manufacturingBasis={'2L':'OSH Park published min finished hole .254mm / annular .127mm; .26/.52=.13 annular leaves only .006mm hole and .003mm annulus over published minima, tool availability/tolerance/tenting not certified.','4L':'JLC PCB capabilities archived lesson28 source: multilayer min hole .15/preferred .2, pad minus hole .10/preferred .15. .26/.52 satisfies published geometry, drill pos +/- .075 separate manufacturing tolerance, actual quote/tool confirmation open.'})
report={'variants':{}}
for v in ('4L','2L'):
 f=H/f'inventory/checkpoints/postcritical_{v}_b010';n=load(f/'normalized.json');r16=next(c for c in n['placements'] if c['ref']=='R16');dx=36.9016-r16['xy'][0];dy=19.9-r16['xy'][1]
 for pp in r16['pins']:
  pp['xy']=[pp['xy'][0]+dx,pp['xy'][1]+dy];pp['padBBox']=[[x+dx,y+dy] for x,y in pp['padBBox']]
 r16['xy']=[36.9016,19.9];r16['bodyExtent']=[[x+dx,y+dy] for x,y in r16['bodyExtent']]
 s=CopperScene(n,load(f/'networks.json'),load(f/'base_net_rules.json'),{})
 if v=='2L':s.add_operation(dict(type='via',net='GND',xy=[37.4,27.4],id='PENDING_FLOAT_STITCH'))
 new=[]
 for o in ops:
  if o['type']=='via':
   for l in LAYERS:new.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(.26,quad_segs=64),kind='via',source=o['id']))
  else:
   for a,b in zip(o['points'],o['points'][1:]):
    if a==b:continue
    new.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(.08,quad_segs=64),kind='line',source=o['id']))
 issues=[];below20=[]
 for i,a in enumerate(new):
  for b in s.obstacles+new[:i]:
   if a['layer']!=b['layer'] or a['net']==b['net']:continue
   d=a['geometry'].distance(b['geometry'])
   if d<.19995:below20.append(dict(a=a['source'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d))
   if d<.15995:issues.append(dict(a=a['source'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d,overlap=a['geometry'].intersects(b['geometry'])))
 body=box(*r16['bodyExtent'][0],*r16['bodyExtent'][1]);pb=[]
 for c in n['placements']:
  if c['ref']!='R16' and c.get('bodyExtent'):pb.append((body.distance(box(*c['bodyExtent'][0],*c['bodyExtent'][1])),c['ref']))
 report['variants'][v]=dict(source=str(f),sourceSHA256=hashlib.sha256((f/'normalized.json').read_bytes()).hexdigest(),issuesBelowPoint16=issues,explicitGapBelowPoint20=below20,R16NearestPlaceBounds=sorted(pb)[:5],neckLengths={o['net']:LineString(o['points']).length for o in ops if o['type']=='route'})
(P/'GPIO_south_joint_fanout_01.json').write_text(json.dumps(p,indent=2),encoding='utf8');(P/'GPIO_south_joint_fanout_review_01.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
