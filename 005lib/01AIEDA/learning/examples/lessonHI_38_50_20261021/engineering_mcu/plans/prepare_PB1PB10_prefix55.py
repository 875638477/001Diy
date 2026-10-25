import pathlib,json,math,sys
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
ops=[dict(type='route',id='S55_PB1_ENGINEERED_ACCESS',net='GPIO_PB1',layer='BOTTOM',width=.2,points=[[38.3,27.35],[38.1,27.55],[38.1,27.75],[34.1,31.75],[33.15,31.75],[31.75,33.15],[31.75,33.5]],purpose='Joint .2mm access below north GPIO fanout with explicit dogleg west of PA3 bar and clearance to live R25/R27 supply.'),dict(type='route',id='S55_PB10_ENGINEERED_ACCESS',net='GPIO_PB10',layer='BOTTOM',width=.2,points=[[38,26.3],[38.9,27.2],[38.9,27.55],[38.75,27.7],[34.28,32.17],[33.31,32.17],[32.33,33.15],[32.33,34.1]],purpose='Joint .2mm parallel fanout maintains .2mm to PB1/north PA3 and original .3mm to ground/power; no new via or source neck.')]
for v in ['2L','4L']:
 n=load(P/f'GPIO_N47_{v}_54_snapshot.json');nw=load(P/f'GPIO_N47_{v}_54_networks.json');rs=load(P/f'GPIO_N47_{v}_54_rules.json');pol=load(P/f'GPIO_N47_{v}_54_policy.json');north=load(H/f'engineering_power/N49_{v}_policy.json')['pendingOperations']+load(H/f'engineering_power/N49_{v}_search01.json')['operations'];pol['pendingOperations']=north;s=CopperScene(n,nw,rs,pol)
 for o in s.obstacles:
  if o['kind']=='via'and o['source']=='native_via':
   z=next(z for z in n['vias']if math.dist(z['xy'],[o['geometry'].centroid.x,o['geometry'].centroid.y])<1e-6);o['geometry']=Point(z['xy']).buffer(.26 if '026_C052'in z['padstack'].upper()else .3,quad_segs=32)
 for o in north:s.add_operation(o)
 issues=[]
 for o in ops:
  for a,b in zip(o['points'],o['points'][1:]):
   if not s.path_clear(o['net'],'BOTTOM',[a,b],.2):
    g=LineString([a,b]).buffer(.1,quad_segs=32)
    for z in s.obstacles:
     if z['layer']!='BOTTOM'or z['net']==o['net']:continue
     d=g.distance(z['geometry']);gap=s.space(o['net'],z['net'],'BOTTOM',z['kind'])
     if d<gap+.001:issues.append(dict(id=o['id'],segment=[a,b],other=z['source'],otherNet=z['net'],d=d,gap=gap,bbox=z['geometry'].bounds))
  s.add_operation(o)
 for a in pol['componentAnchors']:
  if a['net']=='GPIO_PB1':a['xy']=[31.75,33.5];a['layers']=['BOTTOM']
  if a['net']=='GPIO_PB10':a['xy']=[32.33,34.1];a['layers']=['BOTTOM']
 pol['pendingOperations']=north+ops
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_N49_{v}_55_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 (P/f'GPIO_PB1PB10_engineered_access_{v}_55.json').write_text(json.dumps(dict(status='JOINT_PREFIX_REVIEW_PENDING'if not issues else'REJECTED_PREFIX',operations=ops,issues=issues),indent=2),encoding='utf8');print(v,len(issues));print(json.dumps(issues,indent=1))
