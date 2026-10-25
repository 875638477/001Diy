import pathlib,json,urllib.request,hashlib,zipfile,sys
J=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022')
W=J/'tooling/wheels';P=J/'tooling/packages';W.mkdir(parents=True,exist_ok=True);P.mkdir(parents=True,exist_ok=True)
M=[]
for name in ['gerbonara','rtree','click']:
 j=json.load(urllib.request.urlopen('https://pypi.org/pypi/'+name+'/json',timeout=20))
 us=[u for u in j['urls'] if u['filename'].endswith('.whl') and (u['filename'].endswith('py3-none-any.whl') or u['filename'].endswith('py3-none-win_amd64.whl'))]
 assert len(us)==1,(name,[u['filename'] for u in us])
 u=us[0];f=W/u['filename'];data=urllib.request.urlopen(u['url'],timeout=30).read();sha=hashlib.sha256(data).hexdigest();assert sha==u['digests']['sha256']
 f.write_bytes(data)
 with zipfile.ZipFile(f) as z:
  for entry in z.infolist():
   target=(P/entry.filename).resolve()
   assert target.is_relative_to(P.resolve()),entry.filename
  z.extractall(P)
 M.append({'package':name,'version':j['info']['version'],'url':u['url'],'sha256':sha,'requires':j['info']['requires_dist'],'localWheel':str(f)})
(J/'tooling/manifest.json').write_text(json.dumps({'status':'TASK_LOCAL_VERIFIED_OFFICIAL_PYPI_WHEELS_NO_SYSTEM_INSTALL','packages':M,'scope':'Gerbonara file API only. Quart web server dependencies not installed or invoked; all design files stay local.','docs':'https://gerbolyze.gitlab.io/gerbonara/api-concepts.html'},indent=2),encoding='utf8')
sys.path.insert(0,str(P))
from gerbonara import GerberFile,ExcellonFile
print('IMPORT_OK',GerberFile,ExcellonFile)
print('TASK_LOCAL_GERBONARA_FILE_API_READY')
