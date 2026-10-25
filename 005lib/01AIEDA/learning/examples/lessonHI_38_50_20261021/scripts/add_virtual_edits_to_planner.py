import pathlib
p=pathlib.Path(__file__).parent/'plan_signal_paths.py';s=p.read_text(encoding='utf8')
old="snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy)"
new='''snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy)
# Candidate edits are declared future copper only; source SHA/readback is retained.
for edit in policy.get('pendingDeleteVias',[]):
 matches=[v for v in snapshot.get('vias',[]) if v['net']==edit['net'] and math.dist(v['xy'],edit['xy'])<1e-6 and (not edit.get('padstack') or v['padstack']==edit['padstack'])]
 assert len(matches)==1,('Future via ripup must be unique',edit,len(matches));snapshot['vias'].remove(matches[0])
for change in policy.get('pendingPlacementChanges',[]):
 comp=next(p for p in snapshot['placements'] if p['ref']==change['ref']);old=comp['xy'];new=change['xy'];rad=math.radians(change['rotation']-comp['rotation']);ca,sa=math.cos(rad),math.sin(rad)
 def transform(v):return [new[0]+(v[0]-old[0])*ca-(v[1]-old[1])*sa,new[1]+(v[0]-old[0])*sa+(v[1]-old[1])*ca]
 for pin in comp['pins']:
  pin['xy']=transform(pin['xy']);bb=pin['padBBox'];corners=[transform([x,y]) for x in (bb[0][0],bb[1][0]) for y in (bb[0][1],bb[1][1])];pin['padBBox']=[[min(v[0] for v in corners),min(v[1] for v in corners)],[max(v[0] for v in corners),max(v[1] for v in corners)]]
  for net in networks['nets']:
   for part in net['components']:
    for terminal in part['terminals']:
     if terminal['key']==comp['ref']+'.'+str(pin['number']):terminal['xy']=pin['xy']
 comp['xy']=new;comp['rotation']=change['rotation']
'''
assert old in s;s=s.replace(old,new)
s=s.replace("'sourceNativeLog':networks.get('nativeLog',networks.get('readback')),'operations':operations", "'sourceNativeLog':networks.get('nativeLog',networks.get('readback')),'requiredFutureSourcePlans':policy.get('sourcePlans',[]),'requiredPlacementChanges':policy.get('pendingPlacementChanges',[]),'operations':operations")
p.write_text(s,encoding='utf8')