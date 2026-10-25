from pathlib import Path
import concurrent.futures, hashlib, json, shutil, urllib.request
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'/'de_15_26_20261019'
STAGE=ROOT/'staging'/'de_15_26_20261019'/'mcu'
SRC.mkdir(parents=True,exist_ok=True)
STAGE.mkdir(parents=True,exist_ok=True)
SOURCES={
 'DS5319':'https://www.st.com/resource/en/datasheet/stm32f103cb.pdf',
 'AN2586':'https://www.st.com/resource/en/application_note/cd00164185-getting-started-with-stm32f10xxx-hardware-development-stmicroelectronics.pdf',
 'AN2867':'https://www.st.com/content/ccc/resource/technical/document/application_note/c6/eb/5e/11/e3/69/43/eb/CD00221665.pdf/files/CD00221665.pdf/jcr:content/translations/en.CD00221665.pdf',
 'AN2834':'https://www.st.com/content/ccc/resource/technical/document/application_note/group0/3f/4c/a4/82/bd/63/4e/92/CD00211314/files/CD00211314.pdf/jcr:content/translations/en.CD00211314.pdf',
 'RM0008':'https://www.st.com/content/ccc/resource/technical/document/reference_manual/59/b9/ba/7f/11/af/43/d5/CD00171190.pdf/files/CD00171190.pdf/jcr:content/translations/en.CD00171190.pdf',
 'ES096':'https://www.st.com/resource/en/errata_sheet/es096-stm32f101x8b-stm32f102x8b-and-stm32f103x8b-mediumdensity-device-limitations-stmicroelectronics.pdf',
 'AN4879':'https://www.st.com/resource/en/application_note/DM00296349-.pdf',
 'ABM3B':'https://abracon.com/Resonators/abm3b.pdf',
}

def fetch(item):
    name,url=item
    path=SRC/(name+'.pdf')
    try:
        if not path.exists():
            data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=12).read()
            if not data.startswith(b'%PDF'):raise ValueError('not PDF')
            path.write_bytes(data)
        doc=pymupdf.open(path)
        text=''.join('\n\nPDF_PAGE %d\n%s'%(i+1,page.get_text()) for i,page in enumerate(doc))
        (STAGE/(name+'.txt')).write_text(text,encoding='utf-8')
        return {'id':name,'url':url,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':len(doc),'first_page':doc[0].get_text()[:250]}
    except Exception as ex:return {'id':name,'url':url,'error':str(ex)}

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        result=list(pool.map(fetch,SOURCES.items()))
    (STAGE/'source_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2))
