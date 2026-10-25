from pathlib import Path
import json,hashlib,shutil,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=(R/'scripts/compile_batchHI_v32.py').read_text().replace("elif typ=='secondExactBatch':","elif typ in ['secondExactBatch','exactBatch']:").replace("  statements.extend(placement_statements);placed_moves=True","  if typ=='secondExactBatch':statements.extend(placement_statements);placed_moves=True");(R/'scripts/compile_batchHI_v33.py').write_text(s,encoding='utf8')
for v,t in [('2L','10'),('4L','05')]:
 d=json.loads((R/f'batches/clearance_remaining_{v}_b016_phased.json').read_text());omit=[o for o in d['operations'] if o['id'].startswith('NSS_OLD_R25_V3_BRANCH_CLEANUP_')];assert len(omit)==2;d['operations']=[o for o in d['operations'] if o not in omit];d['rejectedLiveFeedDeletion']={'omittedOriginalOperations':omit,'reason':'Root approved withdrawal in both variants. Actual C11.1->R27.1 supply chain is live. Original frozen01 retained but these2ops explicitly superseded; cannot infer manualdeadstub from generatedGNDorphan count.'};d['proofs'].append({'from':'C11.1','to':'R27.1','connected':True})
 corrected=[]
 for o in d['operations']:
  if o['id'] in ['J2_LEFT_GND_SHELL_WIDE','J2_RIGHT_GND_SHELL_WIDE']:
   old=json.loads(json.dumps(o));o['points'].append([35.68 if 'LEFT' in o['id'] else 44.32,6.78]);corrected.append({'before':old,'after':o,'reason':'Root approved exactPTHpincenter endpoint to ensure nativeactualconnectorpin↔shell connectivity; original hole-internal offcenter endpoint didnotconnect. Normal.6 and.35neck.9 unchanged.'})
 d['J2GroundEndpointCorrection']=corrected
 p=R/f'engineering_mcu/plans/South_UNUSED_BOTTOM_PARTIALS_{v}_01.json';tail=json.loads(p.read_text());snap=R/f'source/engineering_snapshots/clearance_remaining_{v}_b016_DRC_PENDING/05_{p.name}';assert not snap.exists();shutil.copyfile(p,snap);d['engineeringSources'].append({'source':str(p),'snapshot':str(snap),'sha256':sha(snap)});d['sourceTailRemovalAudit']=tail
 at=next((i for i,o in enumerate(d['operations']) if o['type'] in ['restoreReference','verifyReferences']),len(d['operations']));d['operations'].insert(at,{'type':'exactBatch','id':'REMOVE_ONLY_UNUSED_SOUTH_BOTTOM_PARTIALS','net':'GPIO_PB12','targets':tail['operations']})
 remap=[]
 for a in d['aliases']:
  if tail['retireOldVirtualProofTargets'].get(a['net'])==a['xy']:
   row=next(x['toVia'] for x in tail['sourceViaProofs'] if x['toVia']['net']==a['net']);before=json.loads(json.dumps(a));a['xy']=row['xy'];a['layer']='TOP';a['type']='via';remap.append({'before':before,'after':a,'reason':'Retire nonhardware partial endpoint after exactunusedtaildeletion; preserve U1->actualoriginalsourcevia and allphysicalpins; fullheaderconnection remains pending.'})
 assert len(remap)==4,(v,remap);d['retiredVirtualTailProofAliasMappings']=remap
 for i,row in enumerate(tail['sourceViaProofs']):
  a='RETAINED_SOUTH_REAL_SOURCE_'+str(i);n=row['toVia'];d['aliases'].append({'id':a,'net':n['net'],'xy':n['xy'],'type':'via','layer':'TOP'});d['proofs'].append({'from':row['from_'],'to':a,'connected':True})
 for check in d['postChecks']:
  if check['type']=='changedNetworks':check['nets']=sorted(set(check['nets'])|{o['net'] for o in tail['operations']})
 out=R/f'batches/clearance_remaining_{v}_b016_tail_cleanup.json';out.write_text(json.dumps(d,indent=2),encoding='utf8');subprocess.run([sys.executable,str(R/'scripts/prepare_b016_retryHI_v3.py'),'--variant',v,'--try-number',t,'--compiler','33','--plan',str(out)],check=True)