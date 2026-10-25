import pathlib,urllib.request,hashlib,json,sys
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
url='https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf'
p=R/'source/AN4879_Rev12_202606.pdf'
try:
 r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35)
 b=r.read(); assert b.startswith(b'%PDF');p.write_bytes(b)
 sys.path.insert(0,r'D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2')
 import fitz
 doc=fitz.open(p); rows=[]
 for i,page in enumerate(doc):
  txt=page.get_text()
  if any(w in txt.lower() for w in ['differential impedance','routing guidelines','trace length','length match','length mismatch','pcb layout']):
   (R/f'source/page_{i+1:02}.txt').write_text(txt,encoding='utf8')
   page.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(R/f'source/page_{i+1:02}.png')
   rows.append({'page':i+1,'text':txt})
 (R/'source/usb_source.json').write_text(json.dumps({'url':url,'sha256':hashlib.sha256(b).hexdigest(),'pages':len(doc),'relevant':rows},indent=2),encoding='utf8')
 print(json.dumps(rows,indent=2))
except Exception as e:
 (R/'source/download_failure.json').write_text(json.dumps({'url':url,'error':repr(e)},indent=2))
 print(repr(e))
