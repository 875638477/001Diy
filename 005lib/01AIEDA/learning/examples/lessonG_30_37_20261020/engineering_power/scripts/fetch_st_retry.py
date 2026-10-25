from pathlib import Path
import urllib.request, json, hashlib, sys
B=Path(r'D:\001DIY\005lib\01AIEDA')
R=B/'learning/examples/lessonG_30_37_20261020/engineering_power'
urls=['https://www.st.com/content/ccc/resource/technical/document/datasheet/06/1d/48/9c/6c/20/4a/b2/CD00050750.pdf/files/CD00050750.pdf/jcr%3Acontent/translations/en.CD00050750.pdf','https://www.st.com/resource/en/datasheet/usblc6-2.pdf']
results=[]
sys.path.insert(0,str(B/'learning/tools/pymupdf_1_28_2'))
import fitz
for url in urls:
 r={'url':url}
 try:
  q=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(q,timeout=18) as f:data=f.read()
  if not data.startswith(b'%PDF'):raise ValueError('Response was not PDF')
  dest=R/'sources/usblc6-2_DS4260_Rev7.pdf';dest.write_bytes(data)
  doc=fitz.open(dest)
  r.update(status='OK',sha256=hashlib.sha256(data).hexdigest().upper(),pdfPages=len(doc),file=str(dest))
  txt=[]
  for n in [1,6,11,12]:
   p=doc[n-1];p.get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False).save(str(R/'rendered'/f'usblc6-2_DS4260_Rev7_p{n}.png'))
   txt.append(f'PDF page {n}\n'+p.get_text())
  (R/'readouts/usblc6-2_DS4260_Rev7_selected_pages.txt').write_text('\n'.join(txt),encoding='utf-8')
  results.append(r);break
 except Exception as ex:r.update(status='FAILED',error=repr(ex));results.append(r)
(R/'sources/st_download_retry.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results))
