from pathlib import Path
import json,csv,shutil,hashlib,urllib.request,sys
B=Path(r'D:\001DIY\005lib\01AIEDA')
R=B/'learning/examples/lessonG_30_37_20261020/engineering_power'
for sub in ['scripts','sources','rendered','readouts']: (R/sub).mkdir(parents=True,exist_ok=True)
c=json.loads((B/'learning/examples/de_15_26_20261019/integrated_circuit.json').read_text(encoding='utf-8'))
s=json.loads((B/'learning/examples/de_15_26_20261019/power_interface_spec.json').read_text(encoding='utf-8'))
rows=[{'ref':x['ref'],'id':x['id'],'page':x['page'],'value':x['value'],'mpn':x.get('mpn',''),'pins':x['pins'],'populate':x.get('populate',''),'requirements':x.get('properties',{}).get('REQUIREMENTS','')} for x in c['components']]
(R/'readouts/component_map.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
(R/'readouts/engineering_limits.json').write_text(json.dumps({k:s.get(k) for k in ['supply_limits','normal_current_budget_mA','calculations','unpopulated_or_rejected','release_gates']},indent=2,ensure_ascii=False),encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
sources=[
('tps54202_revC.pdf','https://www.ti.com/lit/ds/symlink/tps54202.pdf',[3,20,21],B/'learning/sources/de_15_26_20261019/tps54202_revC.pdf'),
('tlv755p_revD.pdf','https://www.ti.com/lit/ds/symlink/tlv755p.pdf',[3,17,21],B/'learning/sources/de_15_26_20261019/tlv755p_revD.pdf'),
('tcan332_revF.pdf','https://www.ti.com/lit/ds/symlink/tcan332.pdf',[4,29,30],B/'learning/sources/de_15_26_20261019/tcan332_revF.pdf'),
('coilcraft_xal60xx_20260225.pdf','https://www.coilcraft.com/getmedia/ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf',[1,4],B/'learning/sources/de_15_26_20261019/coilcraft_xal60xx_20260225.pdf'),
('GCT_USB4105_RevB4.pdf','https://gct.co/files/drawings/usb4105.pdf',[1],B/'learning/examples/lesson10_connector_20261018/source/usb4105.pdf'),
('ss14_vishay.pdf','https://www.vishay.com/docs/88746/ss12.pdf',[1,2],B/'learning/sources/de_15_26_20261019/ss14_vishay.pdf'),
('usblc6-2_DS4260_Rev7.pdf','https://www.st.com/resource/en/datasheet/usblc6-2.pdf',[1,6,11,12],None)]
records=[]
sys.path.insert(0,str(B/'learning/tools/pymupdf_1_28_2'))
import fitz
for name,url,pages,local in sources:
 dest=R/'sources'/name
 record={'file':str(dest),'url':url,'printedPages':pages,'retrieval':'existing local official PDF copied' if local else 'official download'}
 try:
  if local:
   shutil.copy2(local,dest);record['originalLocal']=str(local)
  else:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=35) as response:dest.write_bytes(response.read())
  record['sha256']=sha(dest)
  doc=fitz.open(dest);record['pdfPages']=len(doc)
  excerpts=[]
  for page in pages:
   p=doc[page-1]
   namepart=name.removesuffix('.pdf')+f'_p{page}'
   p.get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False).save(str(R/'rendered'/(namepart+'.png')))
   excerpts.append(f'===== PDF page {page} =====\n'+p.get_text())
  (R/'readouts'/(name.removesuffix('.pdf')+'_selected_pages.txt')).write_text('\n'.join(excerpts),encoding='utf-8')
  record['status']='OK'
 except Exception as ex:record['status']='FAILED';record['error']=str(ex)
 records.append(record)
(R/'sources/source_manifest.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'components':len(rows),'sources':[{'file':Path(r['file']).name,'status':r['status'],'pages':r.get('pdfPages')} for r in records]},ensure_ascii=False))
print(json.dumps([x for x in rows if x['page'] in ['POWER','USB_CAN','INTERFACES']],indent=1,ensure_ascii=False))
