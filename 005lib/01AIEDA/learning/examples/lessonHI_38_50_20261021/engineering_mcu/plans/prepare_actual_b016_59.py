import pathlib,json,math,hashlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
for v in ['2L','4L']:
 B=H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING';n=load(B/'normalized.json');nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');pol=load(P/f'GPIO_N47_{v}_57_policy.json');deps=[B/'normalized.json',H/f'engineering_power/GPIO_NORTH6_{v}_51.json',P/f'PB15_engineered_access_{v}_57.json'];q=load(deps[2])
 if v=='2L':
  for oo in q['operations']:
   if oo['id']=='PB15_2L_VBUS_CLEAR_RIP_0':oo['points']=[[34.75,23.15],[34.4,22.8]]
   if oo['id']=='PB15_2L_VBUS_FINITE_BYPASS':oo['points']=[[34.75,23.15],[34.95,22.95],[34.95,19.45],[34.4,18.9],[34.4,18.15]]
 q['sourceCheckpoint']=str(B);q['sourceNormalizedSHA256']=hashlib.sha256((B/'normalized.json').read_bytes()).hexdigest();q['base']='actualb016 source, all South8 deletion already executed; do not repeat';f=P/f'PB15_engineered_access_{v}_59.json';f.write_text(json.dumps(q,indent=2),encoding='utf8');deps[2]=f
 allops=load(deps[1])['operations']+q['operations'];delids=[]
 for o in allops:
  if o['type']=='deleteVia':
   z=[z for z in n['vias']if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-6];assert len(z)==1,(v,o,len(z));n['vias'].remove(z[0]);delids.append(o['id'])
  elif o['type']=='deleteSegment':
   z=[r for r in n['routes']if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and abs(r['width']-o['width'])<1e-6 and r['startEnd'] in [o['points'],list(reversed(o['points']))]];assert len(z)==1,(v,o,len(z));n['routes'].remove(z[0]);delids.append(o['id'])
  elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=o.get('padDiameterMM',.6),drillDiameterMM=o.get('drillDiameterMM',.3),futureCandidate=o['id']))
  elif o['type']=='route':
   for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=o['width'],startEnd=[a,b],kind='line',generatedThermal=False,futureCandidate=o['id']))
  else:raise ValueError(o)
 pol['pendingOperations']=[]
 for a in pol['componentAnchors']:
  if a['net']in ['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14']:
   z=[z for z in n['vias']if z['net']==a['net']];assert len(z)==1;a['xy']=z[0]['xy'];a['layers']=['TOP','BOTTOM']
  if a['net']=='GPIO_PB15':a['xy']=[34.2,19.6];a['layers']=['TOP','BOTTOM']
 pol['sourceRebasedToActualB016']=str(B);pol['pendingDeleteSegments']=[];pol['bottomCost']=1.15;pol['viaCostMM']=2.;n['derivedActualB016']=True;n['derivedDeleteIDs']=delids;n['candidateInputs']=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest())for f in deps]
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_actualB016_{v}_59_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 print(v,len(delids),len(pol['pendingOperations']),n['readbackDirectory'])

