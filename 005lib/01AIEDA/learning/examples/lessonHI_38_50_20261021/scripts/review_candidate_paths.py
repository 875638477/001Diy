"""Independent actual-copper conservative precheck of explicit engineering path proposals."""
import sys,pathlib,json,argparse,copy,math
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from routing_geometry import CopperScene,ROOT,load,LAYERS,LineString,Point,Polygon,box
A=argparse.ArgumentParser();A.add_argument('--checkpoint',required=True);A.add_argument('--plans',nargs='+',required=True);A.add_argument('--out',required=True);args=A.parse_args();C=pathlib.Path(args.checkpoint)
snapshot=copy.deepcopy(load(C/'normalized.json'));plans=[load(p) for p in args.plans]
changes={}
deleted=[]
replacementQuiet=[]
for plan in plans:
 rework=plan.get('oscillatorReferenceRework')
 if not rework:continue
 sourceLayer=rework['source']['localLayer'][snapshot['variant']]
 matches=[p for p in snapshot['planes'] if p['net']=='GND' and p['layer']=='ETCH/'+sourceLayer and p.get('filled') and not p.get('generated')]
 assert len(matches)==1,'Source quiet static shape must be uniquely identified'
 snapshot['planes'].remove(matches[0]);deleted.append({'oldQuietShape':matches[0],'replacementFromPlan':plan.get('batchId')})
 replacementQuiet.append({'type':'shape','id':'FUTURE_HSE_QUIET_STATIC','net':'GND','layer':sourceLayer,'polygon':rework['islandPolygon'],'dynamic':False})

for plan in plans:
 for op in plan.get('operations',[])+plan.get('commonOperations',[])+plan.get('variantOperations',{}).get(snapshot['variant'],[]):
  if op['type']=='deleteVia':
   matches=[v for v in snapshot.get('vias',[]) if v['net']==op['net'] and math.dist(v['xy'],op['xy'])<1e-6 and (not op.get('padstack') or v['padstack']==op['padstack'])]
   assert len(matches)==1,('Candidate via ripup must uniquely match actual copper',op,len(matches))
   snapshot['vias'].remove(matches[0]);deleted.append({'operation':op['id'],'actualVia':matches[0]});continue
  if op['type']!='deleteSegment':continue
  matches=[r for r in snapshot['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points']))) ]
  assert len(matches)==1,('Candidate ripup must uniquely match actual copper',op,len(matches))
  snapshot['routes'].remove(matches[0]);deleted.append({'operation':op['id'],'actual':matches[0]})
for plan in plans:
 for c in plan.get('placementChanges',[]):changes[c['ref']]=c
for p in snapshot['placements']:
 if p['ref'] not in changes:continue
 c=changes[p['ref']];old=p['xy'];new=c['xy'];rad=math.radians(c['rotation']-p['rotation']);ca,sa=math.cos(rad),math.sin(rad)
 def xf(v):return [new[0]+(v[0]-old[0])*ca-(v[1]-old[1])*sa,new[1]+(v[0]-old[0])*sa+(v[1]-old[1])*ca]
 for pin in p['pins']:
  pin['xy']=xf(pin['xy']);bb=pin['padBBox'];pts=[xf([x,y]) for x in (bb[0][0],bb[1][0]) for y in (bb[0][1],bb[1][1])];pin['padBBox']=[[min(v[0] for v in pts),min(v[1] for v in pts)],[max(v[0] for v in pts),max(v[1] for v in pts)]]
 if p.get('bodyExtent'):
  bb=p['bodyExtent'];pts=[xf([x,y]) for x in (bb[0][0],bb[1][0]) for y in (bb[0][1],bb[1][1])];p['bodyExtent']=[[min(v[0] for v in pts),min(v[1] for v in pts)],[max(v[0] for v in pts),max(v[1] for v in pts)]]
 p['xy']=new;p['rotation']=c['rotation']
policy=load(ROOT/f'plans/ordinary_policy_{snapshot["variant"]}_v6.json');policy['reservedAreas']=[]
scene=CopperScene(snapshot,load(C/'networks.json'),load(C/'base_net_rules.json'),policy)
for op in replacementQuiet:scene.add_operation(op)
issues=[];checked=0;opN=0;movedPadPairs=0;placeBoundIssues=[]
# Moved pads must actively be checked against EXISTING copper as well as being
# obstacles for new routes. Source-only checks missed R21pad-to-oldMISOvia.
for pad in scene.obstacles:
 if pad['kind'] not in ('smdpin','thrupin') or pad['source'].split('.')[0] not in changes:continue
 found=[]
 for other in scene.obstacles:
  if other['layer']!=pad['layer'] or other['net']==pad['net']:continue
  movedPadPairs+=1;gap=float(pad['geometry'].distance(other['geometry']));kind=other['kind']
  if kind=='keepout':required=0.
  elif kind=='via':required=scene.space(pad['net'],other['net'],pad['layer'],pad['kind'],True)
  elif kind=='line':required=scene.space(pad['net'],other['net'],pad['layer'],pad['kind'])
  else:
   field={'smdpin':'smdpin_smdpin','thrupin':'thrupin_smdpin','shape':'smdpin_shape','hole':'hole_smdpin'}.get(kind,'smdpin_line');required=max(scene.rule(n,pad['layer']).get('allSpacingKeys',{}).get(field,.2) for n in (pad['net'],other['net']))
  if gap<required-.0001:found.append({'otherNet':other['net'],'otherSource':other['source'],'otherKind':kind,'otherBounds':list(other['geometry'].bounds),'actualCopperGapMM':round(gap,6),'baseRuleMM':required,'actualOverlap':pad['geometry'].intersection(other['geometry']).area>1e-7})
 if found:issues.append({'operation':'MOVED_PAD_'+pad['source'],'net':pad['net'],'type':'moved_'+pad['kind'],'segment':None,'layer':pad['layer'],'issues':found})
for c in snapshot['placements']:
 if c['ref'] not in changes or not c.get('bodyExtent'):continue
 g=box(*c['bodyExtent'][0],*c['bodyExtent'][1])
 for other in snapshot['placements']:
  if other['ref']==c['ref'] or not other.get('bodyExtent'):continue
  h=box(*other['bodyExtent'][0],*other['bodyExtent'][1]);area=g.intersection(h).area
  if area>1e-7:placeBoundIssues.append({'moved':c['ref'],'other':other['ref'],'overlapAreaMM2':area,'scope':'Native PlaceBound/AABB only; not exact MPN body/courtyard or assembly approval.'})
for plan in plans:
 for op in plan.get('operations',[])+plan.get('commonOperations',[])+plan.get('variantOperations',{}).get(snapshot['variant'],[]):
  opN+=1;typ=op['type'];items=[]
  if typ=='route':
   pts=op['points'];widths=op.get('widths',[op.get('width',.2)]*(len(pts)-1))
   for k,(a,b,w) in enumerate(zip(pts,pts[1:],widths)):
    if math.dist(a,b)>1e-8:items.append((op['layer'],LineString([a,b]).buffer(w/2,quad_segs=16),'line',k))
  elif typ=='via':
   for layer in LAYERS:items.append((layer,Point(op['xy']).buffer(op.get('padDiameterMM',.6)/2,quad_segs=20),'via',None))
  elif typ=='shape' and not op.get('dynamic') and op['layer'] in LAYERS:
   g=Polygon(op['polygon'])
   for v in op.get('voids',[]):g=g.difference(Polygon(v))
   items.append((op['layer'],g,'shape',None))
  for layer,g,kind,k in items:
   checked+=1;found=[]
   for other in scene.obstacles:
    if other['net']==op['net'] or other['layer']!=layer:continue
    gap=float(g.distance(other['geometry']));required=scene.space(op['net'],other['net'],layer,other['kind'],kind=='via')
    # Actual overlap is definitive even when new CSet/region exceptions have not been applied.
    if gap<required-.0001:
     found.append({'otherNet':other['net'],'otherSource':other['source'],'otherKind':other['kind'],'otherBounds':list(other['geometry'].bounds),'actualCopperGapMM':round(gap,6),'baseRuleMM':required,'actualOverlap':g.intersection(other['geometry']).area>1e-7})
   if found:
    found.sort(key=lambda x:(not x['actualOverlap'],x['actualCopperGapMM']))
    issues.append({'operation':op['id'],'net':op['net'],'type':kind,'segment':k,'layer':layer,'issues':found[:12]})
  scene.add_operation(op)
definite=[i for i in issues if any(a['actualOverlap'] for a in i['issues'])]
report={'status':'DEFINITE_COPPER_OVERLAPS' if definite else 'NO_DEFINITE_OVERLAP_SPACING_AND_NATIVE_REVIEW_PENDING','checkpoint':str(C),'plans':args.plans,'placementChanges':list(changes.values()),'deletedSegments':deleted,'operations':opN,'piecesChecked':checked,'movedPadPairsChecked':movedPadPairs,'placeBoundOverlapPairs':placeBoundIssues,'definiteOverlapPieces':len(definite),'spacingWarningPieces':len(issues),'issues':issues,'scope':'Conservative native pad BBOX plus actual cline-width copper; bbox rounded/circle corners may overestimate. New candidate rules/regions not fully resolved, so spacing warnings are BASE-rule diagnostics, not native errors. No-overlap does not certify clearance, conductive graph, neck counts, dynamic/reference copper, thermal/EMI or manufacturing.'}
out=pathlib.Path(args.out).resolve();assert out.is_relative_to(ROOT.resolve());out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps({k:report[k] for k in ('status','operations','piecesChecked','definiteOverlapPieces','spacingWarningPieces')}))
for i in definite[:16]:print(json.dumps(i))