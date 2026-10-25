from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/extract_checkpointHI_v8.py').read_text();s=s.replace("P.add_argument('--interactive-only',action='store_true');a=P.parse_args()", "P.add_argument('--interactive-only',action='store_true');P.add_argument('--drc-pending',action='store_true');a=P.parse_args()\nassert not a.drc_pending or (a.stored_state_only and a.no_alias_update)")
s=s.replace("assert 'drcs=0' in (B/'native_summary.txt').read_text()", "if not a.drc_pending:assert 'drcs=0' in (B/'native_summary.txt').read_text()\nelse:\n assert 'HI_PHYSICAL_TERMINAL_CONTRACT_COMPLETE physicalPins=272 namedNetPins=266 ncPseudoPins=6' in (B/'hi_reopen_endpoint_proofs.txt').read_text()\n assert 'HI_REOPEN_ALL_ENDPOINTS_COMPLETE_STORED_STATE_ONLY_NO_DRC_RECOMPUTE' in (B/'hi_reopen_endpoint_proofs.txt').read_text()")
s=s.replace("if a.interactive_only:summary['drcEvidenceScope']=", "if a.drc_pending:\n summary['nativeDRC']=None\n summary['rawStoredDRCsForensicOnly']=int(re.search(r'drcs=(\\d+)',(B/'native_summary.txt').read_text())[1])\n summary['drcEvidenceScope']='UNRECOMPUTED_PENDING_WHOLE_BOARD_DRC; RAW_STORED_NOT_A_CURRENT_DRC_RESULT'\nif a.interactive_only:summary['drcEvidenceScope']=")
s=s.replace("if a.interactive_only:d['status']='INTERMEDIATE_INTERACTIVE_ONLY_BATCH_T_PENDING'", "if a.interactive_only:d['status']='INTERMEDIATE_INTERACTIVE_ONLY_BATCH_T_PENDING'\nif a.drc_pending:d['status']='SOURCE_GEOMETRY_NATIVE_CONNECTIVITY_PROOFS_PASS_DRC_UNRECOMPUTED_PENDING'")
(R/'scripts/extract_checkpointHI_v9.py').write_text(s,encoding='utf8')
for v in ['2L','4L']:
 import subprocess,sys
 tag=f'reopen_source_{v}_b015_DRC_PENDING_stored';plan=R/f'batches/source_service_{v}_b015_guarded_try11_DRC_PENDING.json';meta=R/f'scripts/source_service_{v}_b015_guarded_try11_DRC_PENDING_compiled.json'
 subprocess.run([sys.executable,str(R/'scripts/prepare_stored_readbackHI_v4.py'),'--tag',tag,'--plan',str(plan),'--compiled',str(meta)],check=True)
