import pathlib,json,csv,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA')
B=R/'learning/examples/lesson08_review_20261018'
Q=R/'learning/examples/qmi8610'
def J(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return [{k:v.strip('"') for k,v in r.items()} for r in csv.DictReader(f,delimiter='\t')]
s=J(Q/'qmi8610_spec.json');v=J(Q/'final_validation.json')
assert v['status']=='PASS'
assert sha(pathlib.Path(s['source']['path']))==s['source']['sha256']==v['sourceSHA256']
artifacts=[]
for p,info in v['publicArtifacts'].items():
 p=pathlib.Path(p);assert sha(p)==info['sha256']
 artifacts.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
pins=rows(Q/'logs/public_reopen/pins.tsv');pads=rows(Q/'logs/public_reopen/pads.tsv');texts=rows(Q/'logs/public_reopen/texts.tsv')
assert len(pins)==16 and {int(p['number']) for p in pins}==set(range(1,17))
assert len(pads)==96 and len(texts)==3
for p in pins:
 w=s['pins'][int(p['number'])-1]
 assert all(abs(float(p[k])-w[k])<1e-8 for k in ['x','y','rotation'])
 assert p['through']=='nil' and p['hole_type']=='none' and float(p['drill_diameter'])==0
 assert abs(float(p['x']))>1e-8 or abs(float(p['y']))>1e-8
for p in pads:
 if p['layer'].endswith('BOTTOM'):assert p['figure']=='NULL'
 else:
  kind={'ETCH/TOP':'copper','PIN/SOLDERMASK_TOP':'mask','PIN/PASTEMASK_TOP':'paste'}[p['layer']]
  dims=s['pad'][kind][:]
  if s['pins'][int(p['number'])-1]['rotation']%180==90:dims.reverse()
  assert p['figure']=='RECTANGLE'
  assert all(abs(float(p[k])-x)<1e-8 for k,x in zip(['width','height'],dims))
assert {t['layer'] for t in texts}=={t['layer'] for t in s['texts']}
assert all(float(t[k])==0 for t in texts for k in ['x','y','rotation'])
assert v['compiledPsmLoad']['status']=='PASS' and v['compiledPsmLoad']['pinsChecked']==48
launch=J(Q/'logs/public_reopen/launch.json')
assert launch['completed'] and launch['beforeSHA']==launch['afterSHA']
assert 'pins=16 drcs=0 drcState=t' in (Q/'logs/public_reopen/verify.txt').read_text()
result={'lesson':8,'date':'2026-10-18','status':'PASS','source':s['source'],'artifactsUnchanged':artifacts,'pinRows':16,'padRows':96,'textRows':3,'noCenterSolderPad':True,'nativePsmTransformPins':48,'method':'Current source and native artifact hashes plus independent re-audit of original persisted native records','landSource':'Exact Rev A p79 recommended PCB land, not component terminal dimensions','height':'1 MM, matches documented maximum','copperGapMm':v['minCopperGapMm'],'maskWebMm':v['minMaskWebMm'],'limits':['Mask and paste are separately declared engineering selections','Basic/profile package tolerances are not replaced by invented plus/minus values','This is CAD course acceptance; fabricated assembly and board-fabricator process approval are not claimed']}
(B/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['lesson','status','pinRows','padRows','textRows','nativePsmTransformPins']},indent=2))
