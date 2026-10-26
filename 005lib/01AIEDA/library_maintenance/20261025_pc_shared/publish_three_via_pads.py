import pathlib,json,hashlib,shutil
m=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared');r=json.loads((m/'via_reopen13/report.json').read_text(encoding='utf-8-sig'));assert r['status']=='PASS_FULL_XML_EXCEPT_PADSTACKNAME'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
files=[]
for row in r['rows']:
 s=m/'via_reopen13'/(row['new_name']+'.pad');d=pathlib.Path(r'D:/001DIY/005lib/01Pad_lib')/s.name
 assert not d.exists() and sha(s)==row['sha256']
 files.append((s,d,row['sha256']))
for s,d,h in files:
 with s.open('rb') as a,d.open('xb') as b:shutil.copyfileobj(a,b)
 assert sha(d)==h
(m/'NEW_VIA_PADS_PUBLISH.json').write_text(json.dumps({'status':'PUBLIC_FILES_ADDED_FULL_NATIVE_XML_VERIFIED_PENDING_BOARD_RULE_BINDING','verification':str(m/'via_reopen13/report.json'),'files':[{'source':str(s),'public':str(d),'sha256':h} for s,d,h in files]},indent=2),encoding='utf-8')
print('3_NEW_PUBLIC_VIA_PADS_ADDED_NO_EXISTING_FILE_OVERWRITTEN')