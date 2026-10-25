import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
old=[dict(type='deleteSegment',id='GPIO_NORTH_RIP_PC15_VERTICAL',net='GPIO_PC15',layer='BOTTOM',points=[[40.3,28.9],[40.3,30.3]],width=.2),dict(type='deleteSegment',id='GPIO_NORTH_RIP_PC15_WEST',net='GPIO_PC15',layer='BOTTOM',points=[[40.3,30.3],[35.4,30.3]],width=.2)]
ops=[dict(type='route',id='GPIO_NORTH_PC15_DIRECT_WEST',net='GPIO_PC15',layer='BOTTOM',points=[[40.3,28.9],[35.4,28.9]],width=.2),dict(type='route',id='GPIO_PA1_INWARD_FANOUT',net='GPIO_PA1',layer='TOP',points=[[37.75,31.25],[37.75,30.6],[38.35,30.0],[38.35,29.7]],width=.2),dict(type='via',id='GPIO_PA1_INWARD_VIA',net='GPIO_PA1',xy=[38.35,29.7],padstack='L28_VIA030_C060'),dict(type='route',id='GPIO_PA2_INWARD_FANOUT',net='GPIO_PA2',layer='TOP',points=[[37.25,31.25],[37.25,30.2],[37.5,29.95],[37.5,29.7]],width=.2),dict(type='via',id='GPIO_PA2_INWARD_VIA',net='GPIO_PA2',xy=[37.5,29.7],padstack='L28_VIA030_C060'),dict(type='route',id='GPIO_PA3_INWARD_FANOUT',net='GPIO_PA3',layer='TOP',points=[[35.75,29.75],[36.1,29.75],[36.6,30.25],[36.6,30.4]],width=.2),dict(type='via',id='GPIO_PA3_INWARD_VIA',net='GPIO_PA3',xy=[36.6,30.4],padstack='L28_VIA030_C060'),dict(type='via',id='GPIO_NORTH_COMMON_RETURN',net='GND',xy=[39.5,28.0],padstack='L28_VIA030_C060')]
p=dict(status='ENGINEERED_SOURCE_GROUP_NOT_NATIVE_APPROVAL',batchId='GPIO_north_joint_fanout_01',operations=old+ops,placementChanges=[],rationale=['Existing PC15 BOTTOM y30.3 traverses the entire inward-via fanout bank and blocks three north GPIOs. Shorten that already-partial GPIO track to y28.9, retaining its actual source via and removing obsolete 1.4mm rise.','Do not move HSE island, moat, oscillator/case routing, ADC RC path or native SPI source lines.','All three PA source escape paths are deliberately staged before any global ordinary routing so a single net cannot consume the others fanout.','New PC15 crosses TOP NSS source diagonally in projection on two-layer board; this is a finite reference transition requiring actual same-layer GND return and nearby app-GND via, not a continuous opposite reference claim.'],partialEndpoints={'GPIO_PA1':dict(xy=[38.35,29.7],layer='BOTTOM',connectedTo='U1.11'),'GPIO_PA2':dict(xy=[37.5,29.7],layer='BOTTOM',connectedTo='U1.12'),'GPIO_PA3':dict(xy=[36.6,30.4],layer='BOTTOM',connectedTo='U1.13'),'GPIO_PC15':dict(xy=[35.4,28.9],layer='BOTTOM',connectedTo='U1.4')},pending=['Native CSet/DRC create and new-process reopen.','All endpoint graph and HSE anchor deletion/rollback.','2L TOP generated GND patch after stitch37.4,27.4 must be app-common connected; inspect actual reference return around finite GPIO/SPI crossing.'])
report={'variants':{}}
for v in ('4L','2L'):
 f=H/f'inventory/checkpoints/postcritical_{v}_b010';n=load(f/'normalized.json');cnt=[]
 for o in old:
  m=[r for r in n['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in (o['points'],list(reversed(o['points']))) and abs(r['width']-o['width'])<1e-8];cnt.append(len(m));assert len(m)==1;n['routes'].remove(m[0])
 pol=load(P/f'gpio_policy_{v}_03.json');s=CopperScene(n,load(f/'networks.json'),load(f/'base_net_rules.json'),pol)
 if v=='2L':s.add_operation(dict(type='via',net='GND',xy=[37.4,27.4],id='PENDING_NATIVE_GPIO_FLOAT_STITCH'))
 new=[]
 for o in ops:
  if o['type']=='via':
   for l in LAYERS:new.append(dict(net=o['net'],layer=l,geometry=Point(o['xy']).buffer(.3,quad_segs=64),kind='via',source=o['id']))
  else:
   for a,b in zip(o['points'],o['points'][1:]):new.append(dict(net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(o['width']/2,quad_segs=64),kind='line',source=o['id']))
 issues=[]
 for i,a in enumerate(new):
  for b in s.obstacles+new[:i]:
   if a['layer']!=b['layer'] or a['net']==b['net']:continue
   d=a['geometry'].distance(b['geometry'])
   if d<.19995:issues.append(dict(a=a['source'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d,overlap=a['geometry'].intersects(b['geometry'])))
 report['variants'][v]={'source':str(f),'sourceSHA256':hashlib.sha256((f/'normalized.json').read_bytes()).hexdigest(),'uniqueDeleteCounts':cnt,'belowPoint20Issues':issues}
(P/'GPIO_north_joint_fanout_01.json').write_text(json.dumps(p,indent=2),encoding='utf8');(P/'GPIO_north_joint_fanout_review_01.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))
