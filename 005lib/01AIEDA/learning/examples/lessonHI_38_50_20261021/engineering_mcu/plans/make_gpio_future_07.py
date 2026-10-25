import pathlib,json,sys,itertools
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
s=(P/'prepare_gpio_future_06.py').read_text(encoding='utf-8-sig').replace('RIGHT10_source_joint_v2','RIGHT10_source_joint_v3').replace('_06_','_07_').replace('_06.py','_07.py')
s=s.replace("pol['reservedAreas']=areas;",'''for o in load(P/'mcu_critical_routes_v6.json')['operations']:
  if o['id'] in ('HSE_GUARD_LEFT_NORTH','HSE_GUARD_RIGHT_NORTH','HSE_GUARD_RIGHT_LOWER'):
   g=LineString(o['points']).buffer(.6,quad_segs=12);areas.append(dict(id='HSE_GUARD_SHADOW_'+o['id'],layers=['TOP','BOTTOM'],allowedNets=['GND','OSC_IN','OSC_OUT','XTAL_OUT'],polygon=[list(p) for p in g.exterior.coords[:-1]],basis='Actual .6mm TOP oscillator guard copper plus .3mm engineering margin, reject ordinary signal under guard on either layer.'))
 pol['reservedAreas']=areas;''')
s=s.replace("n['status']='DERIVED_PLANNING_SCENE_NOT_NATIVE_READBACK';",'''# Map only explicitly declared spacing fields to candidate trace-versus-obstacle regions.
 for qp in ownPlans:
  for ex in qp.get('spacingExceptions',[]):
   pairs=ex.get('netPairs')
   if not pairs and ex.get('netsA'):pairs=[list(z) for z in itertools.product(ex['netsA'],ex['netsB'])]
   if not pairs:pairs=[list(z) for z in itertools.combinations(ex.get('nets',[]),2)]
   kinds={'line_line':'line','via_line':'via','smdpin_line':'smdpin','thrupin_line':'thrupin','line_shape':'shape'}
   for field,gap in ex.get('onlyFields',{}).items():
    if field not in kinds:continue
    for layer in ex.get('layers',[ex.get('layer','TOP')]):
     pol.setdefault('regionOverrides',[]).append(dict(id=ex['id']+'_'+field+'_'+layer,layer=layer,polygon=ex['polygon'],netPairs=pairs,kinds=[kinds[field]],gap=gap,basis='Exact declared source finite spacing field only; outside native parent retained.'))
 n['status']='DERIVED_PLANNING_SCENE_NOT_NATIVE_READBACK';''')
s=s.replace('import pathlib,json,sys,math,hashlib,copy','import pathlib,json,sys,math,hashlib,copy,itertools')
(P/'prepare_gpio_future_07.py').write_text(s,encoding='utf8')
exec(compile(s,str(P/'prepare_gpio_future_07.py'),'exec'))

