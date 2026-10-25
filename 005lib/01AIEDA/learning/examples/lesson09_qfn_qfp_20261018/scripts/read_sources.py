import sys,pathlib,json,hashlib
BASE=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parents[1]/'tools'/'pymupdf_1_28_2'))
import pymupdf
meta=[]
for f in sorted((BASE/'source').glob('*.pdf')):
 d=pymupdf.open(f)
 (f.with_suffix('.txt')).write_text('\n'.join('=== PDF PAGE '+str(i+1)+' ===\n'+p.get_text() for i,p in enumerate(d)),encoding='utf-8')
 hits=[]
 for i,p in enumerate(d):
  t=p.get_text()
  keys=['LQFP48','RGT0016','SOLDER PASTE EXAMPLE','PowerPAD','stencil','coverage']
  if any(k.lower() in t.lower() for k in keys):
   hits.append(i+1)
   if ('LQFP48' in t and i>50) or 'RGT0016' in t or f.name.startswith('slua'):
    p.get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(BASE/'source'/f'{f.stem}_page_{i+1:03}.png')
 meta.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest().upper(),'pages':len(d),'metadata':d.metadata,'matchingPages':hits})
(BASE/'source'/'manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(json.dumps(meta,indent=2))
