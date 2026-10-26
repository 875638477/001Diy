import json,hashlib,pathlib,shutil,datetime
m=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared')
plan=pathlib.Path(r'D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/PUBLIC_NEW_ASSETS.json')
rows=json.loads(plan.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
jobs=[]
for r in rows:
 for ext in ['psm','dra']:
  src=pathlib.Path(r[ext+'_source']);dst=pathlib.Path(r[ext+'_public']);expected=r[ext+'_sha256']
  assert sha(src)==expected,(src,'source sha changed')
  assert not dst.exists(),(dst,'refuse overwrite public')
  assert dst.parent.resolve()==pathlib.Path(r'D:/001DIY/005lib/01Psm_lib').resolve()
  jobs.append((src,dst,expected))
receipt={'status':'NEW_ASSETS_COPIED_PENDING_FINAL_NATIVE_PUBLIC_LOAD','plan':str(plan),'plan_sha256':sha(plan),'created_local':datetime.datetime.now().astimezone().isoformat(),'files':[]}
for src,dst,h in jobs:
 with src.open('rb') as a,dst.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(dst)==h and sha(src)==h
 receipt['files'].append({'source':str(src),'public':str(dst),'sha256':h,'bytes':dst.stat().st_size})
(m/'NEW_PCB_ASSETS_PUBLISH.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':receipt['status'],'new_psm':len(rows),'new_dra':len(rows),'receipt':str(m/'NEW_PCB_ASSETS_PUBLISH.json')}))