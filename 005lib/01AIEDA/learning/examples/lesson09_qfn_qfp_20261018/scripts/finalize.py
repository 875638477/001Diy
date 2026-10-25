import pathlib,json,hashlib,datetime
BASE=pathlib.Path(__file__).resolve().parent.parent
NOTE=BASE.parents[1]/'notes'/'lesson09_qfn_qfp_20261018.md'
ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA').resolve()
assert BASE.is_relative_to(ROOT) and NOTE.is_relative_to(ROOT)
result=json.loads((BASE/'validation.json').read_text(encoding='utf-8-sig'))
assert result['status']=='PASS_CAD_LESSON09' and result['thermalVias']['uniqueNativeDBIDs']==5
assert 'COUNT=5 COMPLETE' in (BASE/'logs'/'via_ids_reopen'/'via_complete.txt').read_text(encoding='utf-8-sig')
for sp in json.loads((BASE/'lesson09_spec.json').read_text(encoding='utf-8-sig'))['packages']:
 for ext in ['dra','psm']:assert (BASE/'library'/(sp['name']+'.'+ext)).stat().st_size>1000
assert NOTE.stat().st_size>10000
assert (BASE/'preview'/'lesson09_footprints.png').stat().st_size>10000
rows=[]
for p in sorted(BASE.rglob('*')):
 if p.is_file() and p!=BASE/'manifest.json':
  rows.append({'path':str(p),'relative':p.relative_to(BASE).as_posix(),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()})
rows.append({'path':str(NOTE),'relative':'../../notes/'+NOTE.name,'size':NOTE.stat().st_size,'sha256':hashlib.sha256(NOTE.read_bytes()).hexdigest().upper()})
manifest={'lesson':9,'dateClient':'2026-10-18 Asia/Shanghai','status':'PASS_CAD_LESSON09','root':str(BASE),'recordsRoot':str(ROOT),'allFilesInside01AIEDA':all(pathlib.Path(r['path']).resolve().is_relative_to(ROOT) for r in rows),'includesHistoryFailures':True,'noPublicLibraryPublication':True,'manifestExcludesItself':True,'fileCount':len(rows),'files':rows}
(BASE/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'status':manifest['status'],'files':len(rows),'allFilesInside01AIEDA':manifest['allFilesInside01AIEDA'],'note':str(NOTE),'preview':str(BASE/'preview'/'lesson09_footprints.png'),'manifest':str(BASE/'manifest.json')},indent=2))

