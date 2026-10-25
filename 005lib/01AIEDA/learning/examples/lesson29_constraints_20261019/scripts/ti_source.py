import pathlib,urllib.request,json,hashlib,sys
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
url='https://www.ti.com/lit/an/spraar7j/spraar7j.pdf'
rec={'url':url,'role':'General high-speed layout concepts only; appendix numeric device tables do not apply to STM32F103.'}
try:
 b=urllib.request.urlopen(url,timeout=25).read(); assert b.startswith(b'%PDF')
 (R/'source/TI_SPRAAR7J_202302.pdf').write_bytes(b)
 rec['sha256']=hashlib.sha256(b).hexdigest()
 sys.path.insert(0,r'D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2')
 import fitz
 doc=fitz.open(stream=b,filetype='pdf')
 for i in [5,7,8,9,13]:
  doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(R/f'source/TI_page_{i+1:02}.png')
 rec['pages']=len(doc)
except Exception as e:rec['error']=repr(e)
(R/'source/TI_source.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
print(json.dumps(rec,indent=2))
