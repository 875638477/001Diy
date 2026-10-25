import pathlib,json
h=pathlib.Path(__file__).resolve().parents[1]
p=h/'scripts/plan_signal_paths.py';s=p.read_text(encoding='utf8')
old=" n=nets[net];comps=[list(c['terminals']) for c in n['components']]"
new=""" n=nets[net];comps=[list(c['terminals']) for c in n['components']]
 # A declaration is used only when both endpoints are real terminals of this net.
 # This avoids duplicating already-planned remote branches as parallel copper loops.
 for proof in policy.get('pendingConnectivityProofs',[]):
  if not proof.get('connected',True):continue
  source,target=proof.get('from'),proof.get('to')
  if source not in scene.pins or target not in scene.pins:continue
  if scene.pins[source]['net']!=net or scene.pins[target]['net']!=net:continue
  owners=[]
  for endpoint in (source,target):owners.append(next((i for i,c in enumerate(comps) if any(t['key']==endpoint for t in c)),None))
  if None in owners or owners[0]==owners[1]:continue
  i,j=sorted(owners);comps[i].extend(comps.pop(j))
"""
assert old in s;s=s.replace(old,new);p.write_text(s,encoding='utf8')
for v in ('2L','4L'):
 p=h/f'plans/ordinary_policy_{v}_v11.json';d=json.loads(p.read_text(encoding='utf8'));d['pendingConnectivityProofs']=[]
 for source in d['sourcePlans']:
  x=json.loads((h/source['path']).read_text(encoding='utf8'));d['pendingConnectivityProofs']+=x.get('proofs',[])
 (h/f'plans/ordinary_policy_{v}_v12.json').write_text(json.dumps(d,indent=2),encoding='utf8')