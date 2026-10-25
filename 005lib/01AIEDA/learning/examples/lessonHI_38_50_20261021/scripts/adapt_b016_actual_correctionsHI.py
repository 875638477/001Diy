from pathlib import Path
import json,hashlib,copy,csv,runpy,sys,math,shutil
sys.dont_write_bytecode=True
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'tooling/packages'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
Builder=runpy.run_path(str(R/'scripts/scoped_rule_builderHI_v2.py'))['ScopedRuleBuilder']
for v in ['2L','4L']:
 C=R/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING';identity=json.loads((C/'networks.json').read_text());assert sha(Path(identity['board']))==identity['sha256'];N=json.loads((C/'normalized.json').read_text());B=Path(identity['readback']);tag=f'clearance_remaining_{v}_b016_DRC_PENDING';snap=R/'source/engineering_snapshots'/tag;snap.mkdir(parents=True,exist_ok=True)
 paths=[R/f'plans/root_source_clearance_cleanup_{v}_01.json',R/'engineering_mcu/plans/GPIO_LEFT_NORTH_spacing_fix_09.json',R/f'engineering_power/RIGHT_actual_clearance_{v}_01.json',R/f'plans/remaining_services_{v}_b015_01.json']
 if v=='4L':paths.append(R/'plans/root_south_private_via_spacing_4L_01.json')
 plans=[];evidence=[]
 for i,p in enumerate(paths):
  dst=snap/f'{i:02d}_{p.name}';assert not dst.exists() or dst.read_bytes()==p.read_bytes(),'Frozen b016 input changed';shutil.copyfile(p,dst);d=json.loads(dst.read_text(encoding='utf-8-sig'));plans.append(d);evidence.append({'source':str(p),'snapshot':str(dst),'sha256':sha(dst)})
 (snap/'manifest.json').write_text(json.dumps(evidence,indent=2),encoding='utf8')
 raw=[copy.deepcopy(o) for p in plans for o in p['operations']];assert len({o['id'] for o in raw})==len(raw);poses=[copy.deepcopy(o) for p in plans for o in p.get('placementChanges',[])];assert len({p['ref'] for p in poses})==len(poses)
 deletes=[o for o in raw if o['type']=='deleteVia']+[o for o in raw if o['type']=='deleteSegment'];adds=[o for o in raw if not o['type'].startswith('delete')]
 # Every requested object is preflight matched against actual saved/fresh native geometry before any mutation.
 for o in deletes:
  if o['type']=='deleteVia':
   m=[x for x in N['vias'] if x['net']==o['net'] and x['xy']==o['xy'] and (not o.get('padstack') or x.get('padstack',x.get('name')).upper()==o['padstack'].upper())]
   assert len(m)==1,('Missing padstack must resolve one actual owned via',v,o,len(m))
   if not o.get('padstack'):o['padstack']=m[0].get('padstack',m[0].get('name'));o['padstackResolution']={'method':'Unique fresh native net+XY via identity','sourceReadback':str(B),'resolvedPadstack':o['padstack']}
  else:m=[x for x in N['routes'] if x['net']==o['net'] and x['layer']=='ETCH/'+o['layer'] and x.get('fixedManualCline') and abs(x['width']-o['width'])<1e-7 and (x['startEnd']==o['points'] or x['startEnd']==list(reversed(o['points']))) ]
  assert len(m)==1,('nonunique original-owned exact target',v,o,len(m))
 builder=Builder(v,C/'base_net_rules.json',prefix='HI_B016');rules=builder.operations;checks=[]
 # Only old SMT field is changed; extension clones the actually effective existing MCU pair.
 cl1=builder.rules['PA10_UART_RX','TOP']['spacingClass'];cl2=builder.rules['PA11_SHARED','TOP']['spacingClass'];assert cl2==builder.rules['PA12_SHARED','TOP']['spacingClass']
 targetRegion=next(x for x in builder.regions if x['data1']=='CONSTRAINT REGION/TOP' and x['data2']==[[39.65,20.0],[40.55,22.15]])
 table=next(x for x in builder.tables if x['name']==targetRegion['name'] and {x['data1'],x['data2']}=={cl1,cl2} and x['data3'][1]);oldC=table['data3'][1]
 rules.append({'type':'existingSpacingLayerFields','name':oldC,'layerValues':{'TOP':{'smdpin_line':.2}},'reason':'Only TOP SMT spacing changes in existing finite source rectangle; all otherfields/layers remain unchanged.'})
 upperParent=next(x['data3'][1] for x in builder.tables if x['name']=='HI_USB_MCU_ESCAPE' and {x['data1'],x['data2']}=={cl1,cl2} and x['data3'][1]);newC=builder.copy('spacing',upperParent,{}, {'onlyDelta':'TOP.smdpin_line','actualPriorEffectiveSource':upperParent,'sourceReadback':str(B)})
 rules[-1]['layerValues']={'TOP':{'smdpin_line':.2}}
 builder.region(builder.newname('R'),'TOP',[[39.8,22.15],[40.55,22.15],[40.55,23.4],[39.8,23.4]],[{'domain':'spacing','netClass':cl1,'otherNetClass':cl2,'cset':newC}],['PA10_UART_RX','PA11_SHARED','PA12_SHARED'])
 for name in [oldC,newC]:checks.append({'type':'spacingFieldChallenge','cset':name,'layer':'TOP','field':'smdpin_line','net':'PA10_UART_RX','normal':.2,'strict':.4})
 viaScope=[];layers=[x.replace('ETCH/','') for x in N['actualEtchLayers']]
 for o in adds:
  if o['type']!='via' or o['padstack'].upper()!='HI_VIA026_C052_TENT':continue
  for layer in layers:
   parent,why=builder.existing_physical_template_at(o['net'],layer,o['xy']);approved=builder.physical[parent,'TOP']['vias'].split(':')
   if 'HI_VIA026_C052_TENT' not in approved:
    builder.via_point_permission(builder.newname('R'),o['net'],o['xy'],layer,parent);why['newPointPermissionAdded']=True
   else:why['existingMacroRegionAlreadyAllowsPrivateVia']=True
   viaScope.append({'net':o['net'],'xy':o['xy'],'layer':layer,'template':parent,'why':why,'onlyPotentialFieldDelta':'vias; preserve width/neck/allow_etch/otherfields'})
 # Reuse exact original source proofs, replacing intentionally reworked object locations transparently.
 oldPlan=json.loads((R/f'batches/source_service_{v}_b015_guarded_try11_DRC_PENDING.json').read_text());oldMeta=json.loads((R/f'scripts/source_service_{v}_b015_guarded_try11_DRC_PENDING_compiled.json').read_text());defs=copy.deepcopy(oldMeta['endpointDefinitions']);maps=[]
 changes=[('GPIO_PB10',[38,26.4],[38,26.3],'PB10 exact tail/via geometry clearance correction'),('GPIO_PC15',[35.4,28.9],[35.4,28.75],'PC15 partial endpoint between two existing GNDvias'),('GPIO_PB9',[45.7,28.65],[45.65,28.65],'PB9 actual outer+inner clearance correction'),('GND',[61.8,24.95],[62.6,25.65],'Retire redundantGNDvia to clear receiver; retained adjacentGNDvia explicitly provides PB4return, not same original object')]
 if v=='4L':changes += [('GPIO_PB13',[37.5,20.75],[37.5,20.725],'Alllayer via-via .205mm geometry correction'),('GPIO_PB15',[38.5,20.7],[38.5,20.675],'Alllayer via-via .205mm geometry correction')]
 for a in poses:
  oldp=next(x for x in N['placements'] if x['ref']==a['ref']);rad=math.radians(a['rotation']-oldp['rotation'])
  for p in oldp['pins']:
   dx,dy=[p['xy'][j]-oldp['xy'][j] for j in [0,1]];xy=[round(a['xy'][0]+dx*math.cos(rad)-dy*math.sin(rad),4),round(a['xy'][1]+dx*math.sin(rad)+dy*math.cos(rad),4)];changes.append((p['net'],p['xy'],xy,'Moved physical '+a['ref']+'.'+p['number']+'; actual native physical pin is final authority'))
 for key,val in defs.items():
  for net,old,new,why in changes:
   if val[0]==net and val[2]==old:maps.append({'oldAlias':key,'net':net,'oldXY':old,'newXY':new,'type':val[3],'reason':why});val[2]=new
 known={o['id']:o for o in adds};aliases=[{'id':k,'net':x[0],'layer':x[1],'xy':x[2],'type':x[3],'origin':'Preserved source proof alias, with explicit coordinate relocation map where required'} for k,x in defs.items() if k not in known];proofs=copy.deepcopy(oldPlan['proofs']);netOf={c['ref']+'.'+p['number']:p['net'] for c in N['placements'] for p in c['pins'] if p['number']}
 def term(x):
  if isinstance(x,dict):return str(x['ref'])+'.'+str(x['pin'])
  if isinstance(x,list) and len(x)==2:return str(x[0])+'.'+str(x[1])
  return x
 def xyAlias(net,xy,layer,kind,reason):
  key='B016_NODE_'+str(len(aliases)+1);aliases.append({'id':key,'net':net,'layer':layer,'xy':xy,'type':kind,'rationale':reason});return key
 for plan in plans:
  for field in ['proofs','expectedProofs','requiredProofs','returnProofs']:
   for row in plan.get(field,[]):
    x=term(row.get('from',row.get('fromTerminal',row.get('source',row.get('sourceId')))));y=term(row.get('to',row.get('target',row.get('toAlias',row.get('targetAlias',row.get('targetViaId'))))))
    if y is None and row.get('toVia'):y=xyAlias(row['net'],row['toVia'],row.get('layer','TOP'),'via',row)
    if y is None and row.get('toPoint'):y=xyAlias(row['net'],row['toPoint'],row.get('layer','TOP'),'point',row)
    if y is None and row.get('targetXY'):y=xyAlias(row.get('net',netOf.get(x)),row['targetXY'],row.get('targetLayer','TOP'),'point',row)
    if x is None and row.get('sourceXY'):x=xyAlias(row['net'],row['sourceXY'],row.get('sourceLayer','TOP'),'point',row)
    assert x and y,('Unadapted proof',plan['batchId'],field,row)
    proofs.append({'from':x,'to':y,'connected':row.get('connected',row.get('expectedConnected',True))})
 for o in adds:
  if o['type']=='via' and o['net']=='GND':proofs.append({'from':o['id'],'to':'U1.23','connected':True})
  if o['type']=='route':
   for key,xy in [('from',o['points'][0]),('to',o['points'][-1])]:
    if o.get(key):
     o[key]=term(o[key])
     if o[key] not in known and o[key] not in netOf and o[key] not in {a['id'] for a in aliases}:aliases.append({'id':o[key],'net':o['net'],'layer':o['layer'],'xy':xy,'type':'point'})
 preservation=[]
 for n in identity['nets']:
  for component in n['components']:
   keys=[t['key'] for t in component['terminals']]
   for key in keys[1:]:preservation.append({'from':keys[0],'to':key,'connected':True})
 assert len(preservation)==172;proofs+=preservation
 unique={}
 for p in proofs:unique.setdefault((p['from'],p['to'],p['connected']),p)
 #2L construction only: defer appdynamic boundaries and later restore exact definition/voids and relative priority order.
 defers=[];restores=[];definitionSource=[]
 if v=='2L':
  bounds=[]
  for row in csv.DictReader((B/'hi_dynamic_boundaries.tsv').open(),delimiter='\t',quotechar='\0'):
   if row['layer'].startswith('HI_'):continue
   layer=builder.sx(row['layer']);attrs=builder.sx(row['attributes']);ad=dict(zip(attrs[::2],attrs[1::2]));verts=builder.sx(row['vertices']);assert all(abs(p[1])<1e-8 for p in verts);bounds.append({'layer':layer.split('/')[1],'polygon':[p[0] for p in verts],'priority':ad['priority'],'attributes':ad,'voids':builder.sx(row['permanentVoids'])})
  assert len(bounds)==4 and sum(b['layer']=='TOP' for b in bounds)==3
  for i,b in enumerate(sorted(bounds,key=lambda b:(b['layer'],b['priority']))):
   ident='B016_APP_REFERENCE_'+str(i);defers.append({'type':'deferReference','id':ident,'net':'GND','layer':b['layer'],'polygon':b['polygon']});restores.append({'type':'restoreReference','id':ident,'net':'GND'});definitionSource.append(b)
  restores.append({'type':'verifyReferences','id':'B016_REFERENCE_DEFINITIONS_VERIFY','net':'GND'})
 changed=sorted({o['net'] for o in raw});assert not set(changed)&{'USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'}
 post=[{'type':'changedNetworks','nets':changed}]+checks+[{'type':'hseIsolation','anchorXY':[46.35,29.4],'localLayer':'BOTTOM' if v=='2L' else 'L2','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}]
 out={'status':'ROOT_APPROVED_ACTUAL_SOURCE_CLEARANCE_AND_REMAINING_NATIVE_BATCH_PREPARED','nativeVariant':v,'inputBoardIdentity':identity,'sourceExpectedSHA256':identity['sha256'],'placementSequence':'AFTER_INITIAL_DELETIONS','placementChanges':poses,'constraintOperations':rules,'operations':deletes+defers+adds+restores,'aliases':aliases,'proofs':list(unique.values()),'terminalContract':oldPlan['terminalContract'],'postChecks':post,'engineeringSources':evidence,'scopeAudit':builder.audit,'newPrivateViaActualLayerScope':viaScope,'preservedSourceProofCount':len(oldPlan['proofs']),'baselinePhysicalEdgePreservationCount':len(preservation),'sourceAliasRelocations':maps,'allOriginalAliasRelocationSpecs':changes,'referenceConstructionDefinitionSnapshot':definitionSource,'expectedRemainingJoins':16,'wholeBoardDRC':None,'drcScope':'Final complete board remains pending; changednonDPnets scoped checks and field challenges cannot be presented as wholeboardDRC.'}
 (R/f'batches/{tag}.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(v,'ops',len(out['operations']),'deleteObjects',len(deletes),'csetsRegions',len(rules),'proofs',len(out['proofs']),'aliasRelocations',len(maps),'changedNets',len(changed))
