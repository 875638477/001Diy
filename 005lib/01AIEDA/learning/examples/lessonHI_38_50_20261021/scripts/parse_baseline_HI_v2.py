from pathlib import Path
import re,json,csv,hashlib,shutil
from collections import Counter
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
G=R.parent/'lessonG_30_37_20261020'
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=='(':
   q=[]
   while t[i]!=')':q.append(take())
   i+=1;return q
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def rows(p):return [{k:sx(v) for k,v in r.items()} for r in csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0')]
summaries={}
for key in ['4L','2L']:
 B=R/f'logs/baseline_{key}_02'
 launch=json.loads((B/'launch.json').read_text())
 assert launch['readonly'] and launch['completed'] and launch['exitCode']==0 and launch['beforeSHA256']==launch['afterSHA256']
 assert '*Error*' not in (B/'stdout.txt').read_text()
 raw=rows(B/'hi_net_connectivity.tsv');terminalrows=rows(B/'hi_component_terminals.tsv')
 nets=[]
 for n in raw:
  comps=[]
  for idx in range(1,int(n['terminalComponents'])+1):
   terms=[t for t in terminalrows if t['net']==n['net'] and t['component']==idx]
   assert terms
   comps.append({'id':idx,'terminals':[{'ref':t['refdes'],'pin':t['pin'],'key':t['terminal'],'xy':t['xy'],'through':t['through'],'padstack':t['padstack']} for t in terms],'graphObjects':terms[0]['graphObjects']})
  assert sum(len(x['terminals']) for x in comps)==n['terminalCount']
  assert n['nativeUnconnected']==n['minTerminalJoins'] and n['unplaced']==0
  nets.append(dict(n,components=comps))
 summary={'netCount':len(nets),'terminalCount':sum(x['terminalCount'] for x in nets),'nativeRemainingConnections':sum(x['nativeUnconnected'] for x in nets),'independentGraphMinJoins':sum(x['minTerminalJoins'] for x in nets),'netsNeedingConnection':sum(x['nativeUnconnected']>0 for x in nets),'terminalConnectedNets':sum(x['terminalComponents']==1 for x in nets),'nativeDRC':0}
 data={'status':'VERIFIED_READONLY_NATIVE_BASELINE','variant':key,'sourceBoard':launch['args'][-1],'sourceSHA256':launch['afterSHA256'],'nativeLog':str(B),'summary':summary,'nets':nets,'scope':'Unconnected is official net.unconnected (excludes unplaced pins, here zero). Components are actual axlDBGetConnect terminal components; min joins are an independent connectivity count. This baseline is partial routing, not a complete engineering route.'}
 (R/f'inventory/baseline_networks_{key}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 shutil.copyfile(G/f'inventory/inventory_{key}.json',R/f'inventory/inventory_{key}.json')
 summaries[key]=dict(summary,largestRemaining=sorted([(n['net'],n['nativeUnconnected']) for n in nets],key=lambda x:-x[1])[:12])
(R/'inventory/baseline_summary.json').write_text(json.dumps(summaries,indent=2),encoding='utf8')
print(json.dumps(summaries,indent=2))
