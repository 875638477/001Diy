import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
for v in ['2L','4L']:
 n=load(H/f'engineering_power/N47_{v}_snapshot.json');nw=load(H/f'engineering_power/N47_{v}_networks.json');rs=load(H/f'engineering_power/N47_{v}_rules.json');pol=load(H/f'engineering_power/N47_{v}_policy.json');base=load(H/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING/normalized.json')
 n['routes']=[r for r in n['routes'] if not (r['net'] in ['GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15'] and r['layer']=='ETCH/BOTTOM')]
 n['routes']=[r for r in n['routes'] if r.get('futureCandidate')!='WEST_GND_APPLICATION_BRIDGE_ROOT'];n['vias']=[z for z in n['vias'] if not(z['net']=='GND' and (math.dist(z['xy'],[35.8,20.5])<1e-6 or math.dist(z['xy'],[36.55,20.05])<1e-6))]
 if not any(z['net']=='GND' and math.dist(z['xy'],[38,20])<1e-6 for z in n['vias']):n['vias'].append(next(z for z in base['vias'] if z['net']=='GND' and math.dist(z['xy'],[38,20])<1e-6))
 for a in pol['componentAnchors']:
  if a['net'] in ['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']:
   vv=[z for z in n['vias'] if z['net']==a['net']];assert len(vv)==1,(a,vv);a['xy']=vv[0]['xy'];a['layers']=['TOP','BOTTOM']
 pol['bottomCost']=1.15;pol['viaCostMM']=2.;pol['candidateGround']='Original WEST/MID/EAST ground vias preserved, no ground relocation. Root temporary WEST35.8,20.5 bridge removed from derived study only; native must prove originalWESTcommon after frozen source-tail cleanup.'
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_N47_{v}_50_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,len(pol['pendingOperations']),next(c['xy']for c in n['placements']if c['ref']=='J12'))
