import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
for v in ['2L','4L']:
 n=load(P/f'GPIO_N37_{v}_45north_snapshot.json');nw=load(P/f'GPIO_N37_{v}_45north_networks.json');rs=load(P/f'GPIO_N37_{v}_45north_rules.json');pol=load(P/f'GPIO_N37_{v}_45north_policy.json')
 for pts in [[[31.11,55],[31.11,47]],[[31.11,47],[38.1016,47]]]:
  assert not any(r['net']=='V3V3' and r['layer']=='ETCH/TOP' and r['startEnd'] in [pts,list(reversed(pts))] for r in n['routes']);n['routes'].append(dict(kind='line',net='V3V3',layer='ETCH/TOP',width=.6,startEnd=pts,generatedThermal=False,fixedManualCline=True,futureCandidate='RESTORED_LIVE_R27_SUPPLY'))
 z=[r for r in n['routes'] if r['net']=='V3V3' and r['layer']=='ETCH/TOP' and r['startEnd'] in [[[35.1,23.6],[35.1,23.2]],[[35.1,23.2],[35.1,23.6]]] and abs(r['width']-.25)<1e-6];assert len(z)==1;z[0]['width']=.6;z[0]['futureCandidate']='VDD24_NORMAL_FLARE_NATIVE_SCOPED_VALIDATED'
 if v=='2L':
  n['vias'].append(dict(net='GND',xy=[35.8,20.5],padstack='L28_VIA030_C060',padDiameterMM=.6,drillDiameterMM=.3,futureCandidate='WEST_GND_APPLICATION_BRIDGE_ROOT'))
  n['routes'].append(dict(kind='line',net='GND',layer='ETCH/TOP',width=.6,startEnd=[[35.8,21.95],[35.8,20.5]],generatedThermal=False,fixedManualCline=True,futureCandidate='WEST_GND_APPLICATION_BRIDGE_ROOT'))
 n['candidateCorrection']='Both previous old-R25 deadstub classifications were wrong. Full original live V3 feed restored to R27 via x38.1016,y47..41.3 before any routing acceptance.'
 for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',pol)]: (P/f'GPIO_N37_{v}_46north_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
