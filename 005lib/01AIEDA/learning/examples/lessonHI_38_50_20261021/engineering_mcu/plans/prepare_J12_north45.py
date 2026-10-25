import json,pathlib,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
for v in ['2L','4L']:
 n=load(P/f'GPIO_N37_{v}_44_snapshot.json');nw=load(P/f'GPIO_N37_{v}_44_networks.json');pol=load(P/f'GPIO_N37_{v}_44_policy.json');rules=load(P/f'GPIO_N37_{v}_44_rules.json');base=load(H/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING/normalized.json');orig=next(c for c in base['placements'] if c['ref']=='J12');j=next(i for i,c in enumerate(n['placements']) if c['ref']=='J12');n['placements'][j]=orig
 n['routes']=[r for r in n['routes'] if r.get('futureCandidate')!='J12_V3_NEW_NORMAL_FEED'];n['routes'].append(dict(kind='line',net='V3V3',layer='ETCH/TOP',width=.6,startEnd=[[31.11,58.2],[31.11,55]],generatedThermal=False,fixedManualCline=True,futureCandidate='RESTORED_ORIGINAL_J12_FEED'))
 xy={'J12.'+p['number']:p['xy'] for p in orig['pins'] if p['number']}
 for nn in nw['nets']:
  for cc in nn['components']:
   for t in cc['terminals']:
    if t['key'] in xy:t['xy']=xy[t['key']]
 n['candidateJ12']='Original north location restored for measured full-route comparison; south move is not assumed necessary.'
 for typ,z in [('snapshot',n),('networks',nw),('rules',rules),('policy',pol)]: (P/f'GPIO_N37_{v}_45north_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
