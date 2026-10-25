import json,pathlib
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/ordinary_aux_{v}_v7.json').read_text());keep=[]
 for o in d['operations']:
  net=o['net'];oid=o['id']
  if net in ('USB_PULLUP_SRC','VBUS_GATE'):keep.append(o)
  elif net in ('VBUS_PRESENT_N','USB_ATTACH_N','UART_RX') and '_1_' in oid:keep.append(o)
 proofs=[x for x in d['proofs'] if not any(k.startswith('U1.') or k.startswith('R16.') or k.startswith('R17.') for k in (x['from'],x['to']))]
 out={'batchId':f'aux_remote_{v}_v8','variant':v,'sourceExpectedSHA256':d['sourceExpectedSHA256'],'operations':keep,'proofs':proofs,'status':'CANDIDATE_NATIVE_AND_REFERENCE_PENDING','scope':'Only transistor/pullup/header remote sections. All stale R16/R17 and MCU source paths removed pending joint fanout.'}
 (h/f'plans/aux_remote_{v}_v8.json').write_text(json.dumps(out,indent=2),encoding='utf8')
 print(v,len(keep),'proofs',proofs)
 for o in keep:print(o['net'],o['type'],o.get('layer'),o.get('xy',o.get('points')))