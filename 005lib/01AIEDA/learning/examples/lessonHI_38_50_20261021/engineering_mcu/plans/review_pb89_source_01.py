import pathlib,json,sys,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent
sys.path.insert(0,str(H/'tooling/packages'));sys.path.insert(0,str(H/'scripts'))
from shapely.geometry import Point,LineString,Polygon,box
from routing_geometry import CopperScene,load
old=[([[44.25,29.25],[45.05,29.25]],.25),([[45.05,29.25],[45.45,28.85]],.25),([[45.45,28.85],[46.5,28.7252]],.6)]
ops=[dict(type='route',id='PB89_VSS47_NECK',net='GND',layer='TOP',points=[[44.25,29.25],[45.35,29.25],[45.4,29.2]],width=.25),dict(type='route',id='PB89_C15_RETURN',net='GND',layer='TOP',points=[[45.4,29.2],[46.0252,29.2],[46.5,28.7252]],width=.6),dict(type='via',id='PB89_HSE_SINGLE_ANCHOR',net='GND',xy=[45.45,28.95],padstack='L28_VIA030_C060'),dict(type='route',id='PB9_SOURCE_NECK',net='GPIO_PB9',layer='TOP',points=[[44.25,28.75],[44.76,28.75],[45.96,27.55]],width=.16),dict(type='route',id='PB9_SOURCE_TO_VIA',net='GPIO_PB9',layer='TOP',points=[[45.96,27.55],[46.5,27.55]],width=.2),dict(type='via',id='PB9_SOURCE_VIA',net='GPIO_PB9',xy=[46.5,27.55],padstack='L28_VIA030_C060'),dict(type='route',id='PB8_SOURCE_TO_VIA',net='GPIO_PB8',layer='TOP',points=[[44.25,28.25],[44.6,28.25],[45.6,27.25],[45.6,26.9]],width=.2),dict(type='via',id='PB8_SOURCE_VIA',net='GPIO_PB8',xy=[45.6,26.9],padstack='L28_VIA030_C060'),dict(type='via',id='PB89_GLOBAL_RETURN_VIA',net='GND',xy=[45.7,26.0],padstack='L28_VIA030_C060')]
p=dict(status='UNEXECUTED_ROOT_SUGGESTION_GEOMETRY_REVIEW',batchId='gpio_pb89_source_rework_01',operations=ops,deleteSegments=[dict(net='GND',layer='TOP',points=a,width=w) for a,w in old],deleteVia={'net':'GND','xy':[45.45,28.85]},preserved=['HSE island polygon and permanent application-ground void exactly unchanged.','All original power branch including VDD48 and C15 original globalvia preserved.'],necessaryPhysicalExceptions=[dict(net='GPIO_PB9',layer='TOP',polygon=[[43.5,28.45],[44.65,28.45],[46.3,26.8],[46.3,28.2],[44.85,29.05],[43.5,29.05]],neckWidthMinMM=.16,maxNeckMM=2.25,basis='0.51+sqrt(2)*1.2=2.207056mm actual proposed neck, manufacturing min152.4um two-layer/127um four-layer; local exception only, no global width/spacing waiver.')],warning='PB9 short source-mouth projection comes within 0.01mm of quiet island projection; not a zero-field-coupling claim. Must inspect native all-layer pad/DRC, unique-anchor deletion, actual return and final native path. Existing root generic HSE reservation excludes GPIO; explicit source-mouth-only allowance required, not global island release.')
report=dict(status='GEOMETRIC_CANDIDATE_NOT_NATIVE_APPROVED',variants={})
island=Polygon(load(R/'plans/mcu_critical_routes_v6.json')['oscillatorReference']['islandPolygon'])
for v in ('4L','2L'):
 f=H/f'inventory/checkpoints/postcritical_{v}_b010/normalized.json';n=load(f)
 counts=[]
 for pts,w in old:
  matches=[r for r in n['routes'] if r['net']=='GND' and r['layer']=='ETCH/TOP' and abs(r['width']-w)<1e-8 and r['startEnd'] in (pts,list(reversed(pts)))];counts.append(len(matches));n['routes']=[r for r in n['routes'] if r not in matches]
 vm=[z for z in n['vias'] if z['net']=='GND' and math.dist(z['xy'],[45.45,28.85])<1e-8];n['vias']=[z for z in n['vias'] if z not in vm]
 scene=CopperScene(n,load(f.parent/'networks.json'),load(f.parent/'base_net_rules.json'),{})
 new=[]
 for o in ops:
  if o['type']=='via':
   for l in ('TOP','BOTTOM'):new.append(dict(id=o['id'],net=o['net'],layer=l,geometry=Point(o['xy']).buffer(.3,quad_segs=64),kind='via',source=o['id']))
  else:
   for a,b in zip(o['points'],o['points'][1:]):new.append(dict(id=o['id'],net=o['net'],layer=o['layer'],geometry=LineString([a,b]).buffer(o['width']/2,quad_segs=64),kind='line',source=o['id']))
 issues=[];mins=[]
 for i,a in enumerate(new):
  ds=[]
  for b in scene.obstacles+new[:i]:
   if a['layer']!=b['layer'] or a['net']==b['net']:continue
   d=a['geometry'].distance(b['geometry']);req=scene.space(a['net'],b['net'],a['layer'],b['kind'],a['kind']=='via')
   ds.append(dict(distance=d,required=req,other=b['source'],net=b['net'],kind=b['kind']))
   if d<.19995:issues.append(dict(a=a['id'],b=b['source'],layer=a['layer'],nets=[a['net'],b['net']],distance=d,required=req,overlap=a['geometry'].intersects(b['geometry'])))
  ds.sort(key=lambda z:z['distance']);mins.append(dict(id=a['id'],layer=a['layer'],nearest=ds[:4]))
 anchor=Point([45.45,28.95]).buffer(.3,quad_segs=64)
 pb9=LineString(ops[3]['points']).buffer(.08,quad_segs=64)
 report['variants'][v]=dict(source=str(f),sourceSHA256=hashlib.sha256(f.read_bytes()).hexdigest(),readback=n['readbackDirectory'],deleteSegmentUniqueCounts=counts,deleteViaUniqueCount=len(vm),issuesBelowPoint20=issues,minimumDistances=mins,anchorFullPadInsideQuietIsland=island.covers(anchor),anchorPadToIslandEdge=anchor.boundary.distance(island.boundary),PB9CopperProjectionToIsland=pb9.distance(island),PB9NeckLength=LineString(ops[3]['points']).length,PB8toNearestReturnVia=math.dist([45.6,26.9],[45.7,26]),PB9toNearestReturnVia=math.dist([46.5,27.55],[45.7,26]))
(R/'plans/gpio_pb89_source_rework_01.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
(R/'plans/gpio_pb89_source_rework_review_01.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({v:{k:d[k] for k in ('issuesBelowPoint20','deleteSegmentUniqueCounts','deleteViaUniqueCount','anchorFullPadInsideQuietIsland','anchorPadToIslandEdge','PB9CopperProjectionToIsland','PB9NeckLength','PB8toNearestReturnVia','PB9toNearestReturnVia')} for v,d in report['variants'].items()},indent=2))
