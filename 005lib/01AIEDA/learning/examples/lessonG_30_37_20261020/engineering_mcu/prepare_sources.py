import os,sys,pathlib,json,hashlib
ROOT=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu")
os.environ["TMP"]=os.environ["TEMP"]=str(ROOT/"runtime")
sys.path.insert(0,r"D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2")
import pymupdf
plans={
"DS5319_inherited.pdf":[26,36,52,53,66,74,75,76,77,78],
"AN2586_current.pdf":[8,9,11,21,22],
"AN2867_current.pdf":[13,14,15,16,45,46,47,48,49],
"AN2834_current.pdf":[15,16,21,22,25,26,36,37,38,39],
"ABM3B_inherited.pdf":[1,2,3]}
urls={
"DS5319_inherited.pdf":"https://www.st.com/resource/en/datasheet/stm32f103c8.pdf",
"AN2586_current.pdf":"https://www.st.com/resource/en/application_note/cd00164185-getting-started-with-stm32f10xxx-hardware-development-stmicroelectronics.pdf",
"AN2867_current.pdf":"https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf",
"AN2834_current.pdf":"https://www.st.com/resource/en/application_note/an2834-how-to-optimize-the-adc-accuracy-in-the-stm32-mcus-stmicroelectronics.pdf",
"ABM3B_inherited.pdf":"https://abracon.com/Resonators/abm3b.pdf"}
report=[]
for name,pages in plans.items():
    p=ROOT/"source"/name
    doc=pymupdf.open(p)
    text=chr(10).join("=== PDF_INDEX_1BASED "+str(i+1)+" ==="+chr(10)+page.get_text() for i,page in enumerate(doc))
    (ROOT/"source"/(p.stem+".txt")).write_text(text,encoding="utf-8")
    for number in pages:
        doc[number-1].get_pixmap(matrix=pymupdf.Matrix(1.4,1.4),alpha=False).save(ROOT/"render"/(p.stem+"_pdf%03d.png"%number))
    report.append(dict(file=name,url=urls[name],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),pages=len(doc),rendered_pdf_1based=pages,revision_header=doc[0].get_text().splitlines()[:5]))
p=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\de_15_26_20261019")
c=json.loads((p/"integrated_circuit.json").read_text(encoding="utf-8-sig"))
m=json.loads((p/"mcu_spec.json").read_text(encoding="utf-8-sig"))
sources=[p/"integrated_circuit.json",p/"mcu_spec.json",p/"power_interface_spec.json",pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019\current\F29_CONSTRAINTS_v4.brd")]
(ROOT/"input_manifest.json").write_text(json.dumps([dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size) for f in sources],indent=2),encoding="utf-8")
(ROOT/"source_manifest.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
refs=["U1","C13","C14","C15","C16","C17","R26","C18","C19","C20","R27","C21","J7","R28","R29","R30","J8","J9","Y1","R31","C22","C23","J10","R32","C24"]
sel=[x for x in c["components"] if x["ref"] in refs]
(ROOT/"mcu_actual_connectivity.json").write_text(json.dumps({"status":"SCHEMATIC_INPUT_NOT_NATIVE_PLACEMENT","components":sel,"mcu_pin_source":m["pins"]},indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(report,ensure_ascii=True,indent=2))
