from pathlib import Path
import argparse,json,csv,hashlib,subprocess,shutil,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--log',required=True);P.add_argument('--variant',choices=['4L','2L'],required=True);P.add_argument('--tag',required=True);P.add_argument('--stored-state-only',action='store_true');P.add_argument('--no-alias-update',action='store_true');P.add_argument('--interactive-only',action='store_true');P.add_argument('--drc-pending',action='store_true');a=P.parse_args()
assert not a.drc_pending or (a.stored_state_only and a.no_alias_update)
assert not a.interactive_only or (a.stored_state_only and a.no_alias_update)
B=Path(a.log);assert B.resolve().is_relative_to(R.resolve())
key=a.variant;C=R/'inventory/checkpoints'/a.tag;C.mkdir(parents=True,exist_ok=True)
s=(R/'scripts/parse_baseline_HI_v2.py').read_text();exec(s[:s.index('summaries={}')])
launch=json.loads((B/'launch.json').read_text())
actual_exit_evidence=str(B/'launch.json')
if not launch['completed']:
 adopted=json.loads((B/'adopted_exit_observation.json').read_text())
 assert adopted['completed'] and adopted['exitCode']==0
 assert adopted['pid']==launch['pid'] and adopted['originalStartUTC']==launch['startUTC']
 assert adopted['verifiedExecutable'].lower()==launch['args'][0].lower()
 assert adopted['beforeSHA256']==adopted['afterSHA256']==launch['beforeSHA256']==launch['afterSHA256']
 assert hashlib.sha256(Path(launch['args'][-1]).read_bytes()).hexdigest().upper()==adopted['afterSHA256']
 launch={**launch,'completed':True,'exitCode':adopted['exitCode']}
 actual_exit_evidence=str(B/'adopted_exit_observation.json')
assert launch['completed'] and launch['exitCode']==0 and launch['beforeSHA256']==launch['afterSHA256']
assert '*Error*' not in (B/'stdout.txt').read_text()
if not a.drc_pending:assert 'drcs=0' in (B/'native_summary.txt').read_text()
else:
 assert 'HI_PHYSICAL_TERMINAL_CONTRACT_COMPLETE physicalPins=272 namedNetPins=266 ncPseudoPins=6' in (B/'hi_reopen_endpoint_proofs.txt').read_text()
 assert 'HI_REOPEN_ALL_ENDPOINTS_COMPLETE_STORED_STATE_ONLY_NO_DRC_RECOMPUTE' in (B/'hi_reopen_endpoint_proofs.txt').read_text()
raw=rows(B/'hi_net_connectivity.tsv');terms=rows(B/'hi_component_terminals.tsv');nets=[]
for n in raw:
 comps=[]
 for i in range(1,int(n['terminalComponents'])+1):
  tt=[t for t in terms if t['net']==n['net'] and t['component']==i]
  assert tt
  comps.append({'id':i,'graphObjects':tt[0]['graphObjects'],'terminals':[{'ref':t['refdes'],'pin':t['pin'],'xy':t['xy'],'key':t['terminal'],'through':t['through'],'padstack':t['padstack']} for t in tt]})
 assert sum(len(x['terminals']) for x in comps)==n['terminalCount']
 nets.append(dict(n,components=comps))
summary={'netCount':len(nets),'nettedTerminalCount':sum(x['terminalCount'] for x in nets),'nativeRemainingConnections':sum(x['nativeUnconnected'] for x in nets),'graphMinTerminalJoins':sum(x['minTerminalJoins'] for x in nets),'netsNeedingConnection':sum(x['nativeUnconnected']>0 for x in nets),'nativeDRC':0}
if a.stored_state_only:
 assert 'FULL_DRC_RECOMPUTE=NOT_REQUESTED_IN_THIS_READBACK' in (B/'hi_readback_scope.txt').read_text()
 summary['drcEvidenceScope']='BUILD_REQUESTED_FULL_DRC_ZERO; FRESH_STORED_STATE_ONLY; FINAL_FULL_RECOMPUTE_PENDING'
audit=B/'hi_branch_terminal_audit.txt'
if audit.exists():
 text=audit.read_text();assert 'HI_BRANCH_TERMINAL_AUDIT_COMPLETE' in text
 summary['nativeTerminalFreeBranches']=int(re.search(r'branchesWithoutPhysicalTerminals=(\d+)',text)[1])
else:summary['nativeTerminalFreeBranches']=None
if a.drc_pending:
 summary['nativeDRC']=None
 summary['rawStoredDRCsForensicOnly']=int(re.search(r'drcs=(\d+)',(B/'native_summary.txt').read_text())[1])
 summary['drcEvidenceScope']='UNRECOMPUTED_PENDING_WHOLE_BOARD_DRC; RAW_STORED_NOT_A_CURRENT_DRC_RESULT'
if a.interactive_only:summary['drcEvidenceScope']='INTERMEDIATE_WHOLE_BOARD_INTERACTIVE_NIL_ZERO; BATCH_T_PENDING; FRESH_STORED_STATE_ONLY'
d={'status':('NATIVE_INTERMEDIATE_BUILD_DRC_ZERO_FRESH_STORED_STATE_ONLY_FINAL_FULL_CHECK_PENDING' if a.stored_state_only else 'NATIVE_CHECKPOINT_READBACK_ZERO_DRC_PARTIAL_ROUTE'),'variant':key,'actualProcessExitEvidence':actual_exit_evidence,'board':launch['args'][-1],'sha256':launch['afterSHA256'],'readback':str(B),'summary':summary,'nets':nets}
if a.interactive_only:d['status']='INTERMEDIATE_INTERACTIVE_ONLY_BATCH_T_PENDING'
if a.drc_pending:d['status']='SOURCE_GEOMETRY_NATIVE_CONNECTIVITY_PROOFS_PASS_DRC_UNRECOMPUTED_PENDING'
(C/'networks.json').write_text(json.dumps(d,indent=2),encoding='utf8')
PTH=R.parent.parent/'tools/python_3_14_0/python.exe'
subprocess.run([str(PTH),str(R/'scripts/normalize_HI_actual_v5.py'),'--log',str(B),'--variant',key,'--output',str(C/'normalized.json')],check=True)
r=(R/'scripts/resolve_base_rulesHI.py').read_text()
r=r.replace("for key in ['4L','2L']:",f"for key in ['{key}']:")
r=r.replace("B=R/f'logs/baseline_{key}_02'","B=Path("+repr(str(B))+")")
r=r.replace("R/f'inventory/base_net_rules_{key}.json'","Path("+repr(str(C/'base_net_rules.json'))+")")
r=r.replace("R/f'inventory/base_net_rules_{key}.tsv'","Path("+repr(str(C/'base_net_rules.tsv'))+")")
exec(r)
if not a.no_alias_update:
 for name,source in [(f'normalized_actual_{key}.json',C/'normalized.json'),(f'current_networks_{key}.json',C/'networks.json'),(f'base_net_rules_{key}.json',C/'base_net_rules.json'),(f'base_net_rules_{key}.tsv',C/'base_net_rules.tsv')]:
  dest=R/'inventory'/name
  old=R/'inputs'/('initial_'+name)
  if dest.is_file() and not old.exists():shutil.copyfile(dest,old)
  shutil.copyfile(source,dest)
 (R/f'inventory/current_{key}.json').write_text(json.dumps({'board':d['board'],'sha256':d['sha256'],'readback':str(B),'checkpointDirectory':str(C),'summary':summary},indent=2),encoding='utf8')
print(json.dumps({'checkpoint':str(C),'summary':summary,'board':d['board'],'sha256':d['sha256']},indent=2))
