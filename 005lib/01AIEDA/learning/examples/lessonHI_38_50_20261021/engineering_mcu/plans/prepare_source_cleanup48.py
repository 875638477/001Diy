import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
for v in ['2L','4L']:
 n=load(P/f'GPIO_N37_{v}_46north_snapshot.json');nw=load(P/f'GPIO_N37_{v}_46north_networks.json');rs=load(P/f'GPIO_N37_{v}_46north_rules.json');pol=load(P/f'GPIO_N37_{v}_46north_policy.json');old=[r for r in n['routes'] if r['net'] in ['GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15'] and r['layer']=='ETCH/BOTTOM'];n['routes']=[r for r in n['routes'] if r not in old];ground=[z for z in n['vias'] if z['net']=='GND' and math.dist(z['xy'],[36.55,20.05])<1e-6];assert len(ground)==1;n['vias'].remove(ground[0]);ops=[dict(type='deleteSegment',id='DROP_UNUSED_'+str(i),net=r['net'],layer='BOTTOM',width=r['width'],points=r['startEnd']) for i,r in enumerate(old)]
 for a in pol['componentAnchors']:
  if a['net'] in ['GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']:
   z=[z for z in n['vias'] if z['net']==a['net']];assert len(z)==1;a['xy']=z[0]['xy'];a['layers']=['TOP','BOTTOM']
 pol['candidateMIDGround']='Original ordinary MID38,20 deleted in study; defer replacement until complete signal topology, actual GND plane/BFS/return review mandatory. Power-cap ground branches retained.'
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_N37_{v}_48north_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
 (P/f'GPIO_source_tail_cleanup_{v}_48.json').write_text(json.dumps(dict(status='DERIVED_ACCESS_STUDY',operations=ops,preserve='All original MCU TOP-to-source-via copper and source via retained; only unused bottom tails removed before joint routing.',MIDGroundDeleted=[38,20]),indent=2),encoding='utf8');print(v,len(old))
