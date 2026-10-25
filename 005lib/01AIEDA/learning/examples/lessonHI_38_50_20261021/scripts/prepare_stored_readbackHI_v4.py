from pathlib import Path
import argparse,json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
A=argparse.ArgumentParser();A.add_argument('--tag',required=True);A.add_argument('--plan',required=True);A.add_argument('--compiled',required=True);a=A.parse_args();planpath=Path(a.plan);d=json.loads(planpath.read_text());meta=json.loads(Path(a.compiled).read_text());assert meta['planSHA256']==hashlib.sha256(planpath.read_bytes()).hexdigest().upper()
Q=json.dumps;out=(R/'logs'/a.tag).as_posix();pt=lambda xy:'list('+' '.join(str(float(x)) for x in xy)+')';defs='list('+' '.join('list('+Q(k)+' '+Q(v[0])+' '+Q(v[1])+' '+pt(v[2])+' '+Q(v[3])+')' for k,v in meta['endpointDefinitions'].items())+')'
sdk=(R/'scripts/batchHI_shapes_v3.il').read_text();i=sdk.index('procedure(hiGroundPointCheck(');j=sdk.find('\nprocedure(',i+1);fn=sdk[i:j if j>0 else len(sdk)].replace('procedure(hiGroundPointCheck(', 'procedure(hiGroundPointCheckReadOnly(',1).replace('  axlShapeDynamicUpdate(nil t) axlDBRefreshId(nil)\n','',1)
il=fn+'\nprocedure(hiStoredReadback()\n let((f)\n f=outfile('+Q(out+'/hi_reopen_endpoint_proofs.txt')+')\n hiRegistry=nil hiNodeDefinitions='+defs+'\n'
if d.get('terminalContract'):
 contract='list('+' '.join('list('+Q(x['ref'])+' '+Q(x['pin'])+' '+(Q(x['net']) if x['net'] else 'nil')+' '+Q(x['padstack'])+')' for x in d['terminalContract'])+')'
 il+=' hiPhysicalTerminalContract(f '+contract+')\n'
for op in d.get('operations',[]):
 if op['type']=='via':il+=' hiBindExistingVia(f '+Q(op['id'])+' '+Q(op['net'])+' '+pt(op['xy'])+' '+Q(op['padstack'])+')\n'
lastChecks={tuple(o['xy']):o for o in d.get('operations',[]) if o['type']=='groundPointCheck'}
for op in lastChecks.values():il+=' hiGroundPointCheckReadOnly(f '+Q(op['id'])+' '+pt(op['xy'])+' '+('t' if op['topConnected'] else 'nil')+' '+('t' if op['bottomConnected'] else 'nil')+')\n'
proofs=[{'from':o['from'],'to':o['to'],'connected':True} for o in d.get('operations',[]) if o.get('from') and o.get('to')]+d.get('proofs',[])
for p in proofs:il+=' hiProof(f '+Q(p['from'])+' '+Q(p['to'])+' '+('t' if p.get('connected',True) else 'nil')+')\n'
il+=' fprintf(f "HI_REOPEN_ALL_ENDPOINTS_COMPLETE_STORED_STATE_ONLY_NO_DRC_RECOMPUTE\\n") close(f)\n f=outfile('+Q(out+'/hi_readback_scope.txt')+')\n fprintf(f "READBACK_SCOPE=FRESH_STORED_STATE_GEOMETRY_CONNECTIVITY_ONLY\\nFULL_DRC_RECOMPUTE=NOT_REQUESTED_IN_THIS_READBACK\\nFINAL_WHOLE_BOARD_DRC_PENDING=t\\nHSE_NEGATIVE_NOT_REPEATED_HERE_BUILD_EVIDENCE_REMAINS\\nDRC_ENABLE=%L\\nSTORED_DRC_COUNT=%d\\nPHYSICAL_MODES=%L\\nSPACING_MODES=%L\\nELECTRICAL_MODES=%L\\n" axlDBControl(\'drcEnable) length(axlDBGetDesign()->drcs) axlCNSPhysicalModeGet(\'all) axlCNSSpacingModeGet(\'all) axlCNSEcsetModeGet(\'all)) close(f) t))\n'
pp=R/f'scripts/{a.tag}.il';pp.write_text(il,encoding='ascii')
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',R/'scripts/extraReadHI.il',pp]
snap=R/'source/readback_snapshots'/a.tag;snap.mkdir(parents=True,exist_ok=False);h='set NOCONFIRM\n';manifest=[]
for j,src in enumerate(loads):
 dst=snap/(f'{j:02d}_'+src.name);shutil.copyfile(src,dst);h+='skill errset(load('+Q(dst.as_posix())+') t)\n';manifest.append({'source':str(src),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiStoredReadback() t)\n'
for function in ['gSnapshot','hiNetworkInventory','hiExtraRead','hiShapeBoundaryRead','hiRouteRoles','hiUSBMaskRead','hiBranchAudit','hiMechanicalPinRead','hiReferenceCoverageRead']:
 args=Q(out)+((' '+Q((R/'library').as_posix())) if function=='gSnapshot' else ' 0.1' if function=='hiReferenceCoverageRead' else '')
 h+='skill errset('+function+'('+args+') t)\n'
h+='quit\nfillin "yes"\n';(R/f'scripts/{a.tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(manifest,indent=2));print(R/f'scripts/{a.tag}.scr')
