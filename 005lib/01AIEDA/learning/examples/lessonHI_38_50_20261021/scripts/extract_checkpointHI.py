from pathlib import Path
import argparse,json,csv,hashlib,subprocess,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
P=argparse.ArgumentParser();P.add_argument('--log',required=True);P.add_argument('--variant',choices=['4L','2L'],required=True);P.add_argument('--tag',required=True);a=P.parse_args()
B=Path(a.log);assert B.resolve().is_relative_to(R.resolve())
key=a.variant;C=R/'inventory/checkpoints'/a.tag;C.mkdir(parents=True,exist_ok=True)
s=(R/'scripts/parse_baseline_HI_v2.py').read_text();exec(s[:s.index('summaries={}')])
launch=json.loads((B/'launch.json').read_text());assert launch['completed'] and launch['exitCode']==0 and launch['beforeSHA256']==launch['afterSHA256']
assert '*Error*' not in (B/'stdout.txt').read_text()
assert 'drcs=0' in (B/'native_summary.txt').read_text()
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
d={'status':'NATIVE_CHECKPOINT_READBACK_ZERO_DRC_PARTIAL_ROUTE','variant':key,'board':launch['args'][-1],'sha256':launch['afterSHA256'],'readback':str(B),'summary':summary,'nets':nets}
(C/'networks.json').write_text(json.dumps(d,indent=2),encoding='utf8')
PTH=R.parent.parent/'tools/python_3_14_0/python.exe'
subprocess.run([str(PTH),str(R/'scripts/normalize_HI_actual.py'),'--log',str(B),'--variant',key,'--output',str(C/'normalized.json')],check=True)
r=(R/'scripts/resolve_base_rulesHI.py').read_text()
r=r.replace("for key in ['4L','2L']:",f"for key in ['{key}']:")
r=r.replace("B=R/f'logs/baseline_{key}_02'","B=Path("+repr(str(B))+")")
r=r.replace("R/f'inventory/base_net_rules_{key}.json'","Path("+repr(str(C/'base_net_rules.json'))+")")
r=r.replace("R/f'inventory/base_net_rules_{key}.tsv'","Path("+repr(str(C/'base_net_rules.tsv'))+")")
exec(r)
for name,source in [(f'normalized_actual_{key}.json',C/'normalized.json'),(f'current_networks_{key}.json',C/'networks.json'),(f'base_net_rules_{key}.json',C/'base_net_rules.json'),(f'base_net_rules_{key}.tsv',C/'base_net_rules.tsv')]:
 dest=R/'inventory'/name
 old=R/'inputs'/('initial_'+name)
 if dest.is_file() and not old.exists():shutil.copyfile(dest,old)
 shutil.copyfile(source,dest)
(R/f'inventory/current_{key}.json').write_text(json.dumps({'board':d['board'],'sha256':d['sha256'],'readback':str(B),'checkpointDirectory':str(C),'summary':summary},indent=2),encoding='utf8')
print(json.dumps({'checkpoint':str(C),'summary':summary,'board':d['board'],'sha256':d['sha256']},indent=2))
