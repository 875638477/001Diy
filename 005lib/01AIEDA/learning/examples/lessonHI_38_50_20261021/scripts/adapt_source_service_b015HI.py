from pathlib import Path
import json,hashlib,copy,csv,runpy,subprocess,sys
sys.dont_write_bytecode=True
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');PTH=R.parent.parent/'tools/python_3_14_0/python.exe';sys.path.insert(0,str(R/'tooling/packages'))
from shapely.geometry import Polygon,box
for v in ['2L','4L']:
 tag=f'source_service_{v}_b015';paths=[R/'engineering_mcu/plans/GPIO_north_joint_fanout_02.json',R/'plans/GPIO_south_joint_root_v9.json',R/'engineering_mcu/plans/GPIO_left_joint_fanout_07.json',R/'engineering_mcu/plans/NSS_pullup_local_relayout_04_SOURCE_ONLY.json',R/f'engineering_power/RIGHT10_FULL_{v}_v11.json',R/f'plans/ordinary_remote_{v}_v9.json',R/f'plans/root_south_services_{v}_v18.json'];snap=R/'source/engineering_snapshots'/tag;snap.mkdir(parents=True,exist_ok=True);d=[];evidence=[]
 for i,p in enumerate(paths):
  dst=snap/f'{i:02d}_{p.name}';assert not dst.exists() or dst.read_bytes()==p.read_bytes(),'Frozen source changed while adapting';dst.write_bytes(p.read_bytes());d.append(json.loads(dst.read_text(encoding='utf-8-sig')));evidence.append({'path':str(p),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
 (snap/'manifest.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
 # Generate full region/CSet copies from the same frozen snapshot inputs.
 rp=R/f'batches/source_service_{v}_b015_rules.json'
 args=[str(PTH),str(R/'scripts/prepare_joint_source_rulesHI.py'),'--variant',v,'--right',evidence[4]['snapshot'],'--north',evidence[0]['snapshot'],'--south',evidence[1]['snapshot'],'--left',evidence[2]['snapshot'],'--output',str(rp)];subprocess.run(args,check=True)
 rules=json.loads(rp.read_text());skip=set(d[3].get('supersedesOperations',[]))|set(d[4].get('rootMustExcludeDuplicateOperations',[]));ops=[];poses=[]
 for i,plan in enumerate(d):
  ops += [copy.deepcopy(o) for o in plan.get('operations',[])+plan.get('variantOperations',{}).get(v,[]) if o['id'] not in set(d[3].get('supersedesOperations',[])) and (i==4 or o['id'] not in set(d[4].get('rootMustExcludeDuplicateOperations',[])))]
  poses += copy.deepcopy(plan.get('placementChanges',[]))
 assert len(ops)==(212 if v=='2L' else 213),(v,len(ops))
 assert len({o['id'] for o in ops})==len(ops);assert len({p['ref'] for p in poses})==len(poses)
 deletions=[o for o in ops if o['type']=='deleteVia']+[o for o in ops if o['type']=='deleteSegment'];adds=[o for o in ops if not o['type'].startswith('delete')]
 right=d[4];old=right['oscillatorReferenceRework']['source'];new=right['oscillatorReference'];shapes=[{'type':'replaceShape','id':'HI_HSE_QUIET_REPLACE','net':'GND','layer':'BOTTOM' if v=='2L' else 'L2','oldPolygon':old['islandPolygon'],'newPolygon':new['islandPolygon'],'dynamic':False}]
 for layer in ['BOTTOM'] if v=='2L' else ['L2','L3']:
  shapes.append({'type':'replaceVoid','id':'HI_HSE_MOAT_REPLACE_'+layer,'net':'GND','layer':layer,'boundaryBBox':[[.5,.5],[79.5,59.5]],'oldPolygon':old['applicationGroundVoidPolygon'],'newPolygon':new['applicationGroundVoidPolygon']})
 identity=json.loads((R/f'inventory/current_{v}.json').read_text());B=Path(identity['readback']);N=json.loads((Path(identity['checkpointDirectory'])/'normalized.json').read_text());builder=runpy.run_path(str(R/'scripts/scoped_rule_builderHI.py'))['ScopedRuleBuilder'](v)
 if v=='2L':
  for row in csv.DictReader((B/'hi_dynamic_boundaries.tsv').open(),delimiter='\t',quotechar='\0'):
   if not row.get('bbox'):continue
   layer=builder.sx(row['layer']);bbox=builder.sx(row['bbox'])
   if layer!='BOUNDARY/TOP' or bbox not in [[[35.8,27.0],[42.4,31.9]],[[39.2,24.6],[47.5,28.4]]]:continue
   vertices=builder.sx(row['vertices']);assert all(abs(a[1])<1e-9 for a in vertices);oldp=[a[0] for a in vertices];newpoly=box(*bbox[0],*bbox[1]).difference(Polygon(new['applicationGroundVoidPolygon']));assert newpoly.geom_type=='Polygon'
   newp=[[round(a,4),round(b,4)] for a,b in list(newpoly.exterior.coords)[:-1]]
   if not Polygon(oldp).equals(Polygon(newp)):shapes.append({'type':'replaceShape','id':'HI_GPIO_TOP_PATCH_RECLIP','net':'GND','layer':'TOP','oldPolygon':oldp,'newPolygon':newp,'dynamic':True})
 ops=deletions+shapes+adds
 known={o['id']:o for o in ops};netOf={c['ref']+'.'+str(p['number']):p['net'] for c in N['placements'] for p in c['pins'] if p['number']};aliases=[];proofs=[];adapted=[]
 def term(x):
  if isinstance(x,list) and len(x)==2:return str(x[0])+'.'+str(x[1])
  if isinstance(x,dict):return str(x['ref'])+'.'+str(x['pin'])
  return x
 def xyAlias(net,xy,layer,why):
  name='NODE_JS_'+str(len(aliases)+1);aliases.append({'id':name,'net':net,'layer':layer,'xy':xy,'type':'point','rationale':why});return name
 for i,plan in enumerate(d):
  for field in ['proofs','expectedProofs','requiredProofs','returnProofs']:
   for row in plan.get(field,[]):
    x=term(row.get('from',row.get('source',row.get('sourceId'))));y=term(row.get('to',row.get('target',row.get('toAlias',row.get('targetViaId')))))
    if x is None and row.get('sourceXY'):x=xyAlias(row['net'],row['sourceXY'],row.get('sourceLayer','TOP'),row)
    if y is None and row.get('targetXY'):
     point=row['targetXY'];layer=row.get('targetLayer',plan.get('partialEndpoints',{}).get(row.get('net'),{}).get('layer','TOP'))
     if row.get('net')=='GPIO_PB15' and point==[38.5,19.7]:point=[38.5,22.3];layer='BOTTOM';adapted.append({'source':evidence[i]['snapshot'],'oldExpectedRow':row,'correction':'Superseded bottom exit delta uses22.3; actual new operation endpoint authoritative.'})
     y=xyAlias(row.get('net',netOf.get(x)),point,layer,row)
    if row.get('targetViaId') and row.get('targetXY'):
     actual=known[row['targetViaId']]['xy']
     if actual!=row['targetXY']:adapted.append({'source':evidence[i]['snapshot'],'oldExpectedRow':row,'actualViaIdXY':actual,'correction':'Native ID resolves actual frozen operation coordinate; historical targetXY ignored.'})
    assert x and y,(field,row)
    proofs.append({'from':x,'to':y,'connected':row.get('connected',row.get('expectedConnected',True))})
 for o in ops:
  if o['type']=='route':
   for key,xy in [('from',o['points'][0]),('to',o['points'][-1])]:
    if o.get(key):
     o[key]=term(o[key])
     if o[key] not in known and o[key] not in netOf and o[key] not in {x['id'] for x in aliases}:aliases.append({'id':o[key],'net':o['net'],'layer':o['layer'],'xy':xy,'type':'point'})
  if o['type']=='via' and o['net']=='GND':proofs.append({'from':o['id'],'to':'U1.23','connected':True})
 # Preserve every previously connected physical pin component without old coordinate aliases.
 cumulative=json.loads((R/f'review/cumulative_physical_proofs_{v}_b014.json').read_text());proofs += [{k:x[k] for k in ['from','to','connected']} for x in cumulative['baselineComponentPreservationProofs']]
 unique={}
 for p in proofs:
  key=(p['from'],p['to'],p['connected']);unique.setdefault(key,p)
 out={'status':'ROOT_APPROVED_SOURCE_SERVICE_NATIVE_BATCH_NOT_YET_EXECUTED','nativeVariant':v,'inputBoardIdentity':identity,'placementSequence':'AFTER_INITIAL_DELETIONS','placementChanges':poses,'constraintOperations':rules['constraintOperations'],'operations':ops,'aliases':aliases,'proofs':list(unique.values()),'terminalContract':cumulative['terminalContract'],'postChecks':[{'type':'hseIsolation','anchorXY':[46.35,29.4],'localLayer':'BOTTOM' if v=='2L' else 'L2','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]},{'type':'finiteViaLineChallenge','cset':'HI_USB_MCU_S_2_2L' if v=='2L' else 'HI_USB_MCU_S_1_4L','layer':'TOP','net':'SWDIO','normal':.2,'strict':.3}],'engineeringSources':evidence,'rootApproval':'Full7source/service input as explicitly authorized, original root precheck19. GPIO13/feed not included.','metadataCorrections':adapted,'operationOrder':'All exact old vias, all exact old manualsegments, then componentmoves, exact quietshape/all-planevoid/TOPpatch replacement, new explicit copper. FullDRC restored on all paths.','scopeAudit':rules['scopeAudit'],'privateViaLayerScope':rules['privateViaLayerScope'],'fineNeckGeometryContracts':[{'net':'GPIO_PB1','pin':'U1.19','layer':'TOP','width':.16,'maxMM':2.8},{'net':'GPIO_PB10','pin':'U1.21','layer':'TOP','width':.16,'maxMM':2.6},{'net':'VBUS_PRESENT_N','pin':'U1.18','layer':'TOP','width':.16,'maxMM':1.4}],'limits':['Intermediate full-board route still incomplete. Native0DRC and component graphs alone do not certify SI/PI/EMI/manufacturing.','No native HSE_SHADOW keepout existed in b014; source JSON reservations remain engineering policy, not a fictional native object replacement.','All-layer private-via approval boxes only add list permission; outer neck/spacing scope explicitly separate and original classes/membership retained.']}
 (R/f'batches/{tag}.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(v,'engineeringOps',212 if v=='2L' else 213,'nativeOps',len(ops),'deletions',len(deletions),'shapes',len(shapes),'poses',len(poses),'proofs',len(out['proofs']))
