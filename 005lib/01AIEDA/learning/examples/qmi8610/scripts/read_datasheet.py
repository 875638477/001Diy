"""Reproduce source text and the reviewed package/pin-page renders without altering the PDF."""
import pathlib,sys,json,hashlib
BASE=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parents[1]/'tools'/'pymupdf_1_28_2'))
import pymupdf
s=json.loads((BASE/'qmi8610_spec.json').read_text(encoding='utf-8-sig'))
src=pathlib.Path(s['source']['path'])
assert hashlib.sha256(src.read_bytes()).hexdigest().upper()==s['source']['sha256']
out=BASE/'source';out.mkdir(exist_ok=True)
d=pymupdf.open(src)
(out/'datasheet_extracted.txt').write_text('\n'.join('=== PDF PAGE '+str(i+1)+' ===\n'+p.get_text() for i,p in enumerate(d)),encoding='utf-8')
(out/'source.json').write_text(json.dumps({'path':str(src),'sha256':s['source']['sha256'],'pages':len(d),'metadata':d.metadata,'engine':'PyMuPDF 1.28.2'},ensure_ascii=False,indent=2),encoding='utf-8')
for n in [8,9,79]:
    d[n-1].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(out/('page_'+str(n).zfill(2)+'.png'))
print('Reviewed pin/package pages rendered: 8, 9, 79')
