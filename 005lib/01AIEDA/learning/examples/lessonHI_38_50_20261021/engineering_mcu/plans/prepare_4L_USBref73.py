import pathlib,json,math,hashlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];v='4L';B=H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
n=load(B/'normalized.json');nw=load(B/'networks.json');rs=load(B/'base_net_rules.json');p=load(P/f'GPIO_actualB016_{v}_59_policy.json')
for o in load(H/f'engineering_power/GPIO_NORTH6_{v}_51.json')['operations']:
 if o['type']=='deleteVia':
  zz=[z for z in n['vias'] if z['net']==o['net'] and math.dist(z['xy'],o['xy'])<1e-5];assert len(zz)==1;n['vias'].remove(zz[0])
 elif o['type']=='deleteSegment':
  zz=[z for z in n['routes'] if z['net']==o['net'] and z['layer']=='ETCH/'+o['layer'] and abs(z['width']-o['width'])<1e-6 and z['startEnd']in[o['points'],o['points'][::-1]]];assert len(zz)==1;n['routes'].remove(zz[0])
 elif o['type']=='via':n['vias'].append(dict(net=o['net'],xy=o['xy'],padstack=o['padstack'],padDiameterMM=.6,drillDiameterMM=.3,futureCandidate=o['id']))
 elif o['type']=='route':
  for a,b in zip(o['points'],o['points'][1:]):n['routes'].append(dict(net=o['net'],layer='ETCH/'+o['layer'],width=o['width'],startEnd=[a,b],generatedThermal=False,futureCandidate=o['id']))
 else:raise Exception(o)
p['reservedAreas']=[a for a in p['reservedAreas'] if not a['id'].startswith('USB_SHARED_REFERENCE_')]
for a in p['reservedAreas']:
 if a['id']=='USB_TRUNK':a['layers']=['TOP'];a['basis']='4L-only candidate: actual TOP USB references L2; BOTTOM ordinary signal references L3. No change to real USB copper or same-layer spacing.'
for a in p['componentAnchors']:
 if a['net'].startswith('GPIO_PB'):
  zz=[z for z in n['vias'] if z['net']==a['net']];assert len(zz)==1;a['xy']=zz[0]['xy'];a['layers']=['TOP','BOTTOM']
for typ,z in [('snapshot',n),('networks',nw),('rules',rs),('policy',p)]: (P/f'GPIO_actual4L_USBref_73_{typ}.json').write_text(json.dumps(z,indent=2),encoding='utf8')
