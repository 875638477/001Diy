import pathlib,json,hashlib,datetime
B=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson27_mechanical_20261019')
N=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/notes/lesson27_mechanical_20261019.md')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
visual={'reviewed':'2026-10-19 Asia/Shanghai','file':'preview.png','status':'PASS','basis':'native readonly readback TSV; not Cadence screenshot','checked':['four corner holes and symmetric datums','closed C2 outline with expected aspect','USB slot/land/locator alignment and opening -Y/insertion +Y','courtyard local edge exception','hardware and height keepout positions','legend and dimension labels readable after adjustment'],'previewSHA256':sha(B/'preview.png')}
(B/'visual_qa.json').write_text(json.dumps(visual,indent=2),encoding='utf8')
files=sorted(p for p in B.rglob('*') if p.is_file() and p.name!='artifact_manifest.json')+[N]
data={'course':27,'finalStatus':'PASS_NATIVE_CAD_SCOPE','dateAsiaShanghai':'2026-10-19','files':[{'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in files],'finalBoardSHA256':sha(B/'F27_MECHANICAL.brd'),'publicLibrariesModified':False,'userProjectModified':False,'notes':str(N)}
(B/'artifact_manifest.json').write_text(json.dumps(data,indent=2),encoding='utf8')
print('MANIFEST',len(files),'files','NOTE',N.stat().st_size)
print(json.loads((B/'validation.json').read_text())['status'])
