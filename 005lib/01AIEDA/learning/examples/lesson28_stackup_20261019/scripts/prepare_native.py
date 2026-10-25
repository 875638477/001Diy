from pathlib import Path
import re,json,hashlib
r=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
src=(r/'scripts'/'launch28.py').read_text()
src=src.replace("choices=['create','readonly']","choices=['create','readonly','edit']")
src=src.replace("assert board.is_file() if a.mode=='readonly' else not board.exists()","assert board.is_file() if a.mode in ('readonly','edit') else not board.exists()")
(r/'scripts'/'launch28.py').write_text(src,encoding='utf-8')
px=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson09_qfn_qfp_20261018\library\l09_thermal_via020_c040.pxml').read_text()
px=px.replace('l09_thermal_via020_c040','l28_via030_c060').replace('0.200','0.300').replace('0.400','0.600')
(r/'native'/'l28_via030_c060.pxml').write_text(px,encoding='utf-8')
filmdata={}
for n in (2,4):
 f=Path(r'D:\001DIY\005lib\01env')/('drill%d.txt'%n)
 s=f.read_text(encoding='utf-8',errors='replace')
 films=[]
 for m in re.finditer(r'axlFilmCreate\(\s*"([^"]+)"([\s\S]*?)(?=axlFilmCreate|\Z)',s):
  name,body=m.groups()
  seq=re.search(r'\?sequence\s+(\d+)',body)
  layers=re.findall(r'"([^"]+)"',body)
  films.append({'name':name,'sequence':int(seq[1]) if seq else None,'layers':layers})
 filmdata[str(n)]={'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'films':films}
(r/'film_template_readonly.json').write_text(json.dumps(filmdata,indent=2),encoding='utf-8')
print('Prepared launcher, via PXML, readonly film map')
