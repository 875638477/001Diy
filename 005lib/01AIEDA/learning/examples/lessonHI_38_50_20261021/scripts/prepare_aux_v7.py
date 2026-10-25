import json,pathlib
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/ordinary_east_{v}_v6.json').read_text())
 keep=[]
 for o in d['operations']:
  net=o['net'];oid=o['id']
  if net in ('BOOT_SERVICE','BOOT1','CAN_TXD'):keep.append(o)
  elif net in ('I2C_SCL','I2C_SDA') and '_1_R' in oid:keep.append(o)
  elif net=='I2C_SDA' and '_1_V' in oid:keep.append(o)
  elif net=='BOOT0' and '_1_' in oid:keep.append(o)
 proofs=[x for x in d['proofs'] if not x['from'].startswith('U1.') and not x['to'].startswith('U1.') and x['from']!='U5.4']
 proofs+=[x for x in d['proofs'] if {x['from'],x['to']}=={'U1.20','R29.1'}]
 out={'batchId':f'ordinary_remote_{v}_v7','variant':v,'sourceExpectedSHA256':d['sourceExpectedSHA256'],'operations':keep,'proofs':proofs,'status':'CANDIDATE_NATIVE_AND_REFERENCE_PENDING','scope':'Only non-MCU remote paths and explicit western BOOT1. Right-side/South source fanouts and CAN_RXD discarded from v6 for joint source engineering.'}
 (h/f'plans/ordinary_remote_{v}_v7.json').write_text(json.dumps(out,indent=2),encoding='utf8')
 p=json.loads((h/f'plans/ordinary_policy_{v}_v6.json').read_text());p['pendingOperations']+=keep
 (h/f'plans/ordinary_policy_{v}_v7.json').write_text(json.dumps(p,indent=2),encoding='utf8')