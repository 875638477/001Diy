from pathlib import Path
import json,sys,math,copy
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power';sys.path.insert(0,str(R/'scripts'));from routing_geometry import CopperScene,load,Point,Polygon,LineString,LAYERS
sys.path.insert(0,str(P/'scripts'));from cadence_poly import conservative_plane
allrows=[]
for v in ['2L','4L']:
 snap=copy.deepcopy(load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_snapshot.json'));policy=load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_policy.json');policy['reservedAreas']=[]
 # Source21 already includes frozen joint source/service18. Repose only R17 for UART03, preserving this review's source identity.
 uart=load(P/f'UART_RX_receiver_bridge_{v}_03.json');c=next(c for c in snap['placements'] if c['ref']=='R17');new=uart['placementChanges'][0];old=c['xy'];rr=math.radians(new['rotation']-c['rotation']);co,si=math.cos(rr),math.sin(rr)
 def xf(a):return [new['xy'][0]+co*(a[0]-old[0])-si*(a[1]-old[1]),new['xy'][1]+si*(a[0]-old[0])+co*(a[1]-old[1])]
 for pin in c['pins']:
  pin['xy']=xf(pin['xy']);bb=pin['padBBox'];pts=[xf([x,y])for x in [bb[0][0],bb[1][0]]for y in [bb[0][1],bb[1][1]]];pin['padBBox']=[[min(a[0]for a in pts),min(a[1]for a in pts)],[max(a[0]for a in pts),max(a[1]for a in pts)]]
 c['xy']=new['xy'];c['rotation']=new['rotation']
 for op in uart['operations']:
  if op['type']=='deleteVia':snap['vias']=[q for q in snap['vias']if not(q['net']==op['net']and math.dist(q['xy'],op['xy'])<1e-6)]
  if op['type']=='deleteSegment':snap['routes']=[q for q in snap['routes']if not(q['net']==op['net']and q['layer']=='ETCH/'+op['layer']and abs(q['width']-op['width'])<1e-6 and(q['startEnd']==op['points']or q['startEnd']==op['points'][::-1]))]
 scene=CopperScene(snap,load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_networks.json'),load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_rules.json'),policy)
 pending=[]
 for plan in [load(R/f'plans/root_remaining_{v}_v19.json'),uart]:
  for op in plan['operations']:
   if op['type']in ['via','route']:scene.add_operation(op);pending.append(op)
 right=load(P/f'RIGHT10_FULL_{v}_v11.json');quietVoid=Polygon(right['oscillatorReferenceRework']['applicationGroundVoidPolygon'])
 guardShadow=[]
 for a in right['quietTopGuardShadows']:
  if 'polygon'in a:guardShadow.append(Polygon(a['polygon']))
 refs=['BOTTOM']if v=='2L'else['L2','L3'];common={}
 for layer in refs:
  ps=[p for p in snap['planes']if p['layer']=='ETCH/'+layer and p.get('filled')and p.get('generated')];common[layer]=[conservative_plane(dict(p,holes=p.get('holes')or[]))for p in ps]
 choices=load(P/f'remaining_returns_{v}_v19_01.json')['engineeringReturns'];newops=[];selected=[]
 def evaluate(xy):
  copper=Point(xy).buffer(.3,quad_segs=24);drill=Point(xy).buffer(.15,quad_segs=20)
  if copper.intersects(quietVoid)or any(copper.intersects(g)for g in guardShadow):return None
  if not scene.board.buffer(-.5).covers(copper):return None
  for pin in scene.pins.values():
   if not pin.get('through')and drill.intersects(pin['geom']):return None
  # Hole-to-hole applies even for same-net ground copper.
  for q in snap['vias']+pending:
   if q.get('type','via')!='via' or 'xy'not in q:continue
   otherDrill=.26 if 'HI_VIA026' in q.get('padstack','')else .3
   if math.dist(xy,q['xy'])<.15+otherDrill/2+.2032-.00001:return None
  minMargin=1e9;nearest=None
  for ob in scene.obstacles:
   if ob['net']=='GND':continue
   d=copper.distance(ob['geometry']);need=scene.space('GND',ob['net'],ob['layer'],ob['kind'],True);margin=d-need
   if margin<-.00005:return None
   if margin<minMargin:minMargin=margin;nearest=dict(net=ob['net'],kind=ob['kind'],source=ob['source'],layer=ob['layer'],copperGapMM=d,requiredMM=need,marginMM=margin)
  coverage={l:any(g.covers(copper)for g in gs)for l,gs in common.items()}
  return dict(xy=xy,minRuleMarginMM=minMargin,nearest=nearest,frozenCommonPlaneCoversWholePad=coverage)
 for row in choices:
  sig=row['signalViaXY'];preferred=row['groundViaXY'];options=[]
  for ix in range(-20,21):
   for iy in range(-20,21):
    xy=[round(sig[0]+ix*.1,4),round(sig[1]+iy*.1,4)];dist=math.dist(sig,xy)
    if dist<.7 or dist>1.9:continue
    e=evaluate(xy)
    if e:
     e['signalDistanceMM']=dist;e['parentPointDistanceMM']=math.dist(xy,preferred);e['score']=dist+max(0,.1-e['minRuleMarginMM'])*1.2+(.75 if not all(e['frozenCommonPlaneCoversWholePad'].values())else 0);options.append(e)
  options.sort(key=lambda e:e['score']);assert options,('No feasiblecommonreturncandidate',v,row)
  # Keep >=.02 margin when feasible inside1.6mm; no requirement to force an unsafe1.5mm.
  marginOptions=[e for e in options if e['minRuleMarginMM']>=.02 and e['signalDistanceMM']<=1.6]
  chosen=(marginOptions or options)[0];op=dict(type='via',id='REM19_RETURN_'+row['signal'],net='GND',xy=chosen['xy'],padstack='L28_VIA030_C060',purpose='CommonGNDreturn '+row['signal']+'; independentallfuturegeometry, nativeactualcommonfill proofpending');newops.append(op);scene.add_operation(op);pending.append(op);selected.append(dict(signal=row['signal'],signalViaXY=sig,parentCandidateXY=preferred,selected=chosen,alternatives=options[:8]))
 out=dict(batchId='remaining_returns_'+v+'_v19_02',variant=v,status='EXPLICIT_COMMON_GND_CANDIDATES_FULL_NATIVE_REFERENCE_PENDING',operations=newops,returnReview=selected,proofRequirements=['EachaddedGNDvia must connect applicationcommonGND, not isolatedquietisland','Refresh L2/L3 or2L BOTTOM actualground and recompute allnew padcoverage/narrowneck','HSE uniqueanchor negative after allreturns added; completeDRC andfreshreopen','2L TOPglobalpour stillpending; same-netthroughcopperalone is not HFreturncert'],scope='AllfutureSOURCE21+UART03+remaining19 obstacles; privatequietgroundnoteligible; actualfrozenreferencecoverage is historical andmust be refreshed fornewantipads')
 (P/f'remaining_returns_{v}_v19_02.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');allrows.append(out)
 print(json.dumps(dict(variant=v,chosen=[dict(signal=s['signal'],xy=s['selected']['xy'],distance=s['selected']['signalDistanceMM'],minMargin=s['selected']['minRuleMarginMM'],coverage=s['selected']['frozenCommonPlaneCoversWholePad'])for s in selected])))
(P/'readouts/remaining_returns_v19_02_selection.json').write_text(json.dumps(dict(status='CANDIDATE_GEOMETRY_AND_HISTORICAL_COMMON_REFERENCE_SCOPE',variants=allrows),indent=2)+'\n',encoding='utf-8')