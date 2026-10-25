from pathlib import Path
import json,hashlib,copy,shutil,sys,csv,subprocess,re
sys.dont_write_bytecode=True
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper();contractPath=R/'engineering_power/GPIO_NORTH6_51_native_contract.json';assert sha(contractPath)=='7F5CD1EAA62849ABA2D813E00481BBC69F2140D22B55929E4BFBD513BF48404C';contract=json.loads(contractPath.read_text());physical=json.loads((R/'review/cumulative_physical_pin_contract_b016.json').read_text());src=(R/'scripts/normalize_HI_actual_v5.py').read_text();ns={'json':json,'re':re};exec(src[src.index('def sx('):src.index('symbols=')],ns);sx=ns['sx']
for v,oldTag in [('4L','05'),('2L','12')]:
 C=R/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING';identity=json.loads((C/'networks.json').read_text());N=json.loads((C/'normalized.json').read_text());spec=next(x for x in contract['variants'] if x['variant']==v);p=Path(spec['plan']);assert sha(p)==spec['sha256'] and identity['sha256']==spec['sourceBoardSHA']==sha(Path(identity['board']));d=json.loads(p.read_text());assert len(d['operations'])==39 and len([o for o in d['operations'] if o['type'].startswith('delete')])==13;snap=R/f'source/engineering_snapshots/north6_{v}_b017';snap.mkdir(exist_ok=False);inputs=[]
 for f in [p,contractPath]:
  dest=snap/f.name;shutil.copyfile(f,dest);inputs.append({'source':str(f),'snapshot':str(dest),'sha256':sha(dest)})
 oldPlan=json.loads((R/f'batches/clearance_remaining_{v}_b016_DRC_PENDING_try{oldTag}.json').read_text());oldMeta=json.loads((R/f'scripts/clearance_remaining_{v}_b016_DRC_PENDING_try{oldTag}_compiled.json').read_text());defs=copy.deepcopy(oldMeta['endpointDefinitions']);oldProofs=copy.deepcopy(oldPlan['proofs']);oldProofs += [{'from':o['from'],'to':o['to'],'connected':True} for o in oldPlan['operations'] if o.get('from') and o.get('to')];active={p[k] for p in oldProofs for k in ['from','to']};mappings=[];retired={}
 for s in spec['retiredLegacyEndpointSelectors']:
  matching=[(k,a) for k,a in defs.items() if k in active and a[0]==s['net'] and a[2]==s['oldXY'] and (a[3]==s['oldType'] or s['oldType']=='historical_point' and a[3]=='point')]
  for key,a in matching:
   target=s.get('replacementOperation',s.get('replacementRealTarget'));assert target;retired[key]=target;mappings.append({'oldAlias':key,'oldDefinition':a,'newTarget':target,'selector':s,'allActualPinContractsRetained':True});del defs[key]
  if not matching:mappings.append({'selector':s,'status':'NO_ACTIVE_OLD_PROOF_MATCH_RECORDED_NO_FAKE_OLD_XY_PASS'})
 for row in oldProofs:
  for k in ['from','to']:row[k]=retired.get(row[k],row[k])
 proofs=oldProofs+physical['variants'][v]['proofs'];assert len(physical['variants'][v]['proofs'])==181
 for row in d['proofs']:proofs.append({'from':row['from'],'to':row.get('to',row.get('toAlias')),'connected':row.get('connected',True)})
 aliases=[{'id':k,'net':a[0],'layer':a[1],'xy':a[2],'type':a[3]} for k,a in defs.items()];pins={'GPIO_PC13':'U1.2','GPIO_PC15':'U1.4','GPIO_PA1':'U1.11','GPIO_PA2':'U1.12','GPIO_PA3':'U1.13'}
 for i,o in enumerate(spec['preserveExistingPhysicalObjects']):
  alias='NORTH_KEEP_EXISTING_'+str(i);aliases.append({'id':alias,'net':o['net'],'xy':o['xy'],'type':'via','layer':'TOP'});proofs.append({'from':pins.get(o['net'],'C1.2'),'to':alias,'connected':True})
 proofs.append({'from':'U1.3','to':next(o['id'] for o in d['operations'] if o['type']=='via' and o['net']=='GPIO_PC14'),'connected':True})
 # Static alloriginalexacttargets; actualnative guard repeats originalownership and non-targetgeometry signatures.
 for o in d['operations']:
  if o['type']=='deleteVia':matches=[x for x in N['vias'] if x['net']==o['net'] and x['xy']==o['xy'] and x['padstack']==o['padstack']]
  elif o['type']=='deleteSegment':matches=[x for x in N['routes'] if x['fixedManualCline'] and x['net']==o['net'] and x['layer']=='ETCH/'+o['layer'] and x['width']==o['width'] and (x['startEnd']==o['points'] or x['startEnd']==list(reversed(o['points'])))]
  else:continue
  assert len(matches)==1,('nonunique b017 target',v,o,len(matches))
 defers=[];restores=[]
 if v=='2L':
  old=[]
  for row in csv.DictReader((Path(identity['readback'])/'hi_dynamic_boundaries.tsv').open(),delimiter='\t',quotechar='\0'):
   if row['layer'].startswith('HI_'):continue
   layer=sx(row['layer']).split('/')[1];a=sx(row['attributes']);a=dict(zip(a[::2],a[1::2]));pp=sx(row['vertices']);assert all(abs(p[1])<1e-9 for p in pp);old.append((layer,a['priority'],[p[0] for p in pp]))
  assert len(old)==4
  for i,(layer,priority,poly) in enumerate(sorted(old)):
   ident='B017_APP_REFERENCE_'+str(i);defers.append({'type':'deferReference','id':ident,'net':'GND','layer':layer,'polygon':poly});restores.append({'type':'restoreReference','id':ident,'net':'GND'})
  restores.append({'type':'verifyReferences','id':'B017_REFERENCE_VERIFY','net':'GND'})
 deletes=[o for o in d['operations'] if o['type'].startswith('delete')];adds=[o for o in d['operations'] if not o['type'].startswith('delete')];unique={}
 for p in proofs:unique.setdefault((p['from'],p['to'],p['connected']),p)
 out={'status':'ROOT_APPROVED_NORTH51_INDEPENDENT_NATIVE_STAGE_NOT_FINAL_ALL13_GPIO','nativeVariant':v,'inputBoardIdentity':identity,'sourceExpectedSHA256':identity['sha256'],'constraintOperations':[],'operations':deletes+defers+adds+restores,'aliases':aliases,'proofs':list(unique.values()),'terminalContract':oldPlan['terminalContract'],'postChecks':[{'type':'changedNetworks','nets':sorted({o['net'] for o in d['operations']})},{'type':'hseIsolation','anchorXY':[46.35,29.4],'localLayer':'BOTTOM' if v=='2L' else 'L2','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}],'legacyAliasRetirementMappings':mappings,'priorNativeCriticalProofsIncludingInline':len(oldProofs),'preservedB016ActualPhysicalEdges':181,'engineeringSources':inputs,'nativeContract':spec,'expectedRemainingJoins':10,'wholeBoardDRC':None,'constructionNote':'2L provenconstruction-only exactdynamicappmother defer/restore preserves permanentvoid andparameters; no finalglobalpour. FourlayerL2/L3 untouched. No rulesmutated.'}
 base=R/f'batches/north6_{v}_b017.json';base.write_text(json.dumps(out,indent=2),encoding='utf8');work=R/f'native_work/b017_{v}_try01';work.mkdir(exist_ok=False);scratch=work/'input.brd';scratch.write_bytes(Path(identity['board']).read_bytes());protected=json.loads((R/f'native_work/b016_{v}_try01/guard_configuration.json').read_text())['protectedOriginals']
 for x in ['2L','4L']:
  p=R/f'native_candidates/HI_{x}_clearance_remaining_b016_DRC_PENDING.brd';protected.append({'path':str(p),'sha256':sha(p),'role':'Actualb016 training source, neveropened bythiswritablebatch'})
 output=R/f'native_candidates/HI_{v}_north6_b017_DRC_PENDING.brd';assert not output.exists();out['outputBoard']=str(output);out['executionGuard']={'scratchWritableWorkingCopy':str(scratch),'inputSHA256':sha(scratch),'protectedOriginals':protected,'scope':'Root explicitly approved North51 asindependent reversible newtaskcopy native stage. FinalSouth/allmanual/fullwholeboardDRC pending.'};tag=f'north6_{v}_b017_DRC_PENDING_try01';planpath=R/f'batches/{tag}.json';planpath.write_text(json.dumps(out,indent=2),encoding='utf8');subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v33.py'),'--plan',str(planpath),'--variant',v,'--tag',tag],check=True);mp=R/f'scripts/{tag}_compiled.json';m=json.loads(mp.read_text());cfg={'variant':v,'tag':tag,'scratchWritableWorkingCopy':str(scratch),'scratchSHA256':sha(scratch),'candidateOutput':str(output),'compiledMetadata':str(mp),'compiledMetadataSHA256':sha(mp),'plan':str(planpath),'planSHA256':sha(planpath),'script':m['script'],'scriptSHA256':sha(Path(m['script'])),'log':m['log'],'protectedOriginals':protected,'allowlistRoot':str(R),'aliasUpdatesAllowed':False};(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8');(snap/'manifest.json').write_text(json.dumps(inputs,indent=2),encoding='utf8');print(v,'uniqueproofs',len(unique),'retiredActualAliasCount',len(retired))
s=(R/'scripts/launch_b016_guardedHI_v2.py').read_text().replace("native_work/b016_{a.variant}","native_work/b017_{a.variant}");(R/'scripts/launch_b017_guardedHI_v1.py').write_text(s,encoding='utf8')