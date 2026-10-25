import pathlib,urllib.request,json,zipfile,hashlib,sys,datetime
R=pathlib.Path(__file__).resolve().parents[1];T=R/'tooling';P=T/'packages';D=T/'downloads'
P.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
records=[]
for name in ('numpy','shapely'):
 url=f'https://pypi.org/pypi/{name}/json'
 with urllib.request.urlopen(url,timeout=25) as response:data=response.read()
 (D/f'{name}_pypi.json').write_bytes(data);meta=json.loads(data)
 wheels=[v for v in meta['urls'] if v['filename'].endswith('cp314-cp314-win_amd64.whl') and not v.get('yanked')]
 assert len(wheels)==1,(name,[v['filename'] for v in meta['urls']]);wheel=wheels[0]
 assert wheel['url'].startswith('https://files.pythonhosted.org/')
 f=D/wheel['filename']
 if not f.exists():
  with urllib.request.urlopen(wheel['url'],timeout=40) as response:f.write_bytes(response.read())
 digest=hashlib.sha256(f.read_bytes()).hexdigest();assert digest==wheel['digests']['sha256']
 with zipfile.ZipFile(f) as archive:
  for member in archive.infolist():
   path=(P/member.filename).resolve();assert path.is_relative_to(P.resolve())
  archive.extractall(P)
 records.append({'package':name,'version':meta['info']['version'],'metadataURL':url,'wheel':wheel['filename'],'url':wheel['url'],'sha256':digest,'bytes':f.stat().st_size})
 print(name,meta['info']['version'],f.stat().st_size,flush=True)
sys.path.insert(0,str(P))
import numpy,shapely
from shapely.geometry import LineString,Point
assert abs(LineString([(0,0),(1,0)]).distance(Point(.5,.3))-.3)<1e-12
report={'purpose':'Task-local actual copper geometry, clearance and reference checks; not SI/PI simulation or full-board automatic routing','generatedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packages':records,'importedVersions':{'numpy':numpy.__version__,'shapely':shapely.__version__},'scope':'All downloads/extraction and imports only inside this HI task directory; no system Python/package modifications'}
(T/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('Task-local geometry tools ready')