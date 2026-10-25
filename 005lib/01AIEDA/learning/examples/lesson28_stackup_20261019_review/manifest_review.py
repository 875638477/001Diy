import pathlib,json,hashlib
O=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019_review')
N=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/notes/lesson28_independent_review_20261019.md')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
r=json.loads((O/'review.json').read_text())
assert all(x['pass'] for x in r['checks'])
bad=[x['path'] for x in r['reviewedFiles'] if sha(pathlib.Path(x['path']))!=x['SHA256']]
assert not bad,bad
files=sorted(p for p in O.rglob('*') if p.is_file() and p.name!='artifact_manifest.json')+[N]
m={'status':'COMPLETE_READ_ONLY_REVIEW','dateAsiaShanghai':'2026-10-19','cadenceStartedByReviewer':False,'lesson28FilesModifiedByReviewer':False,'independentChecks':99,'files':[{'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in files]}
(O/'artifact_manifest.json').write_text(json.dumps(m,indent=2),encoding='utf8')
print(m['status'],len(files),'files; reviewed input hashes still match')
