from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/extract_checkpointHI_v7.py').read_text()
s=s.replace("P.add_argument('--stored-state-only',action='store_true');a=P.parse_args()", "P.add_argument('--stored-state-only',action='store_true');P.add_argument('--no-alias-update',action='store_true');P.add_argument('--interactive-only',action='store_true');a=P.parse_args()\nassert not a.interactive_only or (a.stored_state_only and a.no_alias_update)")
s=s.replace("d={'status':", "if a.interactive_only:summary['drcEvidenceScope']='INTERMEDIATE_WHOLE_BOARD_INTERACTIVE_NIL_ZERO; BATCH_T_PENDING; FRESH_STORED_STATE_ONLY'\nd={'status':")
s=s.replace("(C/'networks.json').write_text", "if a.interactive_only:d['status']='INTERMEDIATE_INTERACTIVE_ONLY_BATCH_T_PENDING'\n(C/'networks.json').write_text")
i=s.index('for name,source in [(');j=s.index('print(json.dumps(',i);s=s[:i]+'if not a.no_alias_update:\n'+''.join(' '+x+'\n' for x in s[i:j].splitlines())+s[j:]
(R/'scripts/extract_checkpointHI_v8.py').write_text(s,encoding='utf8')
