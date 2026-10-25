from pathlib import Path
import json, hashlib, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1]
dest=root/'sources'/'de_15_26_20261019'
stage=root/'staging'/'de_15_26_20261019'/'power_sources'
dest.mkdir(parents=True,exist_ok=True); stage.mkdir(parents=True,exist_ok=True)
sources={
 'tps54202_revC.pdf':'https://www.ti.com/lit/ds/symlink/tps54202.pdf',
 'tlv755p_revD.pdf':'https://www.ti.com/lit/ds/symlink/tlv755p.pdf',
 'tcan332_revF.pdf':'https://www.ti.com/lit/ds/symlink/tcan332.pdf',
 'usblc6-2_rev7.pdf':'https://www.st.com/resource/en/datasheet/usblc6-2.pdf',
 'smbj16a_review.pdf':'https://www.st.com/resource/en/datasheet/smbj16a.pdf',
 'ss14_vishay.pdf':'https://www.vishay.com/docs/88746/ss12.pdf',
 '2n7002_nexperia.pdf':'https://assets.nexperia.com/documents/data-sheet/2N7002.pdf',
 'dmp2035u_diodes.pdf':'https://www.diodes.com/datasheet/download/DMP2035U.pdf',
 'littelfuse_467.pdf':'https://www.littelfuse.com/assetdocs/fuse-467-datasheet?assetguid=4a59f034-1cca-460e-a5ba-e1e66247c76d',
 'nxp_um10204_rev7.pdf':'https://cache.nxp.com/docs/en/user-guide/UM10204.pdf',
 'st_an5225.pdf':'https://www.st.com/resource/en/application_note/dm00536349-usb-type-c-power-delivery-using-stm32xx-series-mcus-and-stm32xxx-series-mpus-stmicroelectronics.pdf',
}
import fitz
records=[]
for name,url in sources.items():
 p=dest/name
 if not p.exists():
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   data=urllib.request.urlopen(req,timeout=12).read()
   if not data.startswith(b'%PDF'): raise ValueError('non-PDF response')
   p.write_bytes(data)
  except Exception as exc:
   records.append({'url':url,'local_download':'failed; official web PDF inspected instead','error':str(exc)})
   continue
 doc=fitz.open(p)
 (stage/(p.stem+'.txt')).write_text('\n'.join(f'PDF_PAGE {n+1}\n'+page.get_text() for n,page in enumerate(doc)),encoding='utf-8')
 # Local PDF rendering for read-only pin and reference-design inspection.
 for n in ({'tps54202_revC.pdf':[2,12,14,20], 'tlv755p_revD.pdf':[2,15,16], 'tcan332_revF.pdf':[3,27,28], 'usblc6-2_rev7.pdf':[0,8,10], 'smbj16a_review.pdf':[2],'nxp_um10204_rev7.pdf':[49]}.get(name,[0])):
  doc[n].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(stage/f'{p.stem}_p{n+1}.png')
 records.append({'file':str(p),'url':url,'pages':len(doc),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'download_date':'2026-10-19'})
(stage/'source_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
