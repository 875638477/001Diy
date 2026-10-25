from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
tag='reopen_island_stitch_2L_b011_stored_only';out=(R/'logs'/tag).as_posix();Q=json.dumps
meta=json.loads((R/'scripts/island_stitch_2L_b011_compiled.json').read_text())
pt=lambda xy:'list('+' '.join(str(float(x)) for x in xy)+')'
defs='list('+' '.join('list('+Q(k)+' '+Q(v[0])+' '+Q(v[1])+' '+pt(v[2])+' '+Q(v[3])+')' for k,v in meta['endpointDefinitions'].items())+')'
base=(R/'scripts/batchHI_shapes_v3.il').read_text();i=base.index('procedure(hiGroundPointCheck(');fn=base[i:].replace('procedure(hiGroundPointCheck(', 'procedure(hiGroundPointCheckReadOnly(',1).replace('  axlShapeDynamicUpdate(nil t) axlDBRefreshId(nil)\n','',1)
program=fn+'\nprocedure(hiStoredReadback()\n let((f)\n f=outfile('+Q(out+'/hi_reopen_endpoint_proofs.txt')+')\n hiRegistry=nil hiNodeDefinitions='+defs+'\n hiBindExistingVia(f "V_HI_GPIO_ISLAND_STITCH" "GND" list(37.4 27.4) "L28_VIA030_C060")\n hiGroundPointCheckReadOnly(f "FRESH_STITCH_ACTUAL_SHAPE" list(37.4 27.4) t t)\n hiProof(f "V_HI_GPIO_ISLAND_STITCH" "U1.23" t)\n fprintf(f "HI_REOPEN_ALL_ENDPOINTS_COMPLETE_STORED_STATE_ONLY_NO_DRC_RECOMPUTE\\n") close(f)\n f=outfile('+Q(out+'/hi_readback_scope.txt')+')\n fprintf(f "READBACK_SCOPE=FRESH_STORED_STATE_GEOMETRY_CONNECTIVITY_ONLY\\nFULL_DRC_RECOMPUTE=NOT_REQUESTED_IN_THIS_READBACK\\nFINAL_WHOLE_BOARD_DRC_PENDING=t\\nDRC_ENABLE=%L\\nSTORED_DRC_COUNT=%d\\nPHYSICAL_MODES=%L\\nSPACING_MODES=%L\\nELECTRICAL_MODES=%L\\n" axlDBControl(\'drcEnable) length(axlDBGetDesign()->drcs) axlCNSPhysicalModeGet(\'all) axlCNSSpacingModeGet(\'all) axlCNSEcsetModeGet(\'all)) close(f) t))\n'
pp=R/f'scripts/{tag}.il';pp.write_text(program,encoding='ascii')
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il','inventoryG.il','placementG.il','local_copperG_v2.il']
loads=[R/'source'/x for x in helpers]+[R/'scripts/network_inventoryHI_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',R/'scripts/extraReadHI.il',pp]
snap=R/'source/readback_snapshots'/tag;snap.mkdir(parents=True,exist_ok=False);h='set NOCONFIRM\n';manifest=[]
for j,src in enumerate(loads):
 dst=snap/(f'{j:02d}_'+src.name);shutil.copyfile(src,dst);h+='skill errset(load('+Q(dst.as_posix())+') t)\n';manifest.append({'source':str(src),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiStoredReadback() t)\n'
for function in ['gSnapshot','hiNetworkInventory','hiExtraRead','hiShapeBoundaryRead','hiRouteRoles','hiUSBMaskRead','hiBranchAudit','hiReferenceCoverageRead']:
 args=Q(out)+((' '+Q((R/'library').as_posix())) if function=='gSnapshot' else ' 0.1' if function=='hiReferenceCoverageRead' else '')
 h+='skill errset('+function+'('+args+') t)\n'
h+='quit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(manifest,indent=2))
s=(R/'scripts/extract_checkpointHI_v5.py').read_text().replace('a=P.parse_args()',"P.add_argument('--stored-state-only',action='store_true');a=P.parse_args()")
s=s.replace("d={'status':'NATIVE_CHECKPOINT_READBACK_ZERO_DRC_PARTIAL_ROUTE'", "d={'status':('NATIVE_INTERMEDIATE_BUILD_DRC_ZERO_FRESH_STORED_STATE_ONLY_FINAL_FULL_CHECK_PENDING' if a.stored_state_only else 'NATIVE_CHECKPOINT_READBACK_ZERO_DRC_PARTIAL_ROUTE')")
s=s.replace("audit=B/'hi_branch_terminal_audit.txt'", "if a.stored_state_only:\n assert 'FULL_DRC_RECOMPUTE=NOT_REQUESTED_IN_THIS_READBACK' in (B/'hi_readback_scope.txt').read_text()\n summary['drcEvidenceScope']='BUILD_REQUESTED_FULL_DRC_ZERO; FRESH_STORED_STATE_ONLY; FINAL_FULL_RECOMPUTE_PENDING'\naudit=B/'hi_branch_terminal_audit.txt'")
(R/'scripts/extract_checkpointHI_v6.py').write_text(s,encoding='ascii')
print('stored-state-only fresh readback explicitly scoped; no DRC update or shape mutation or challenge replay')
