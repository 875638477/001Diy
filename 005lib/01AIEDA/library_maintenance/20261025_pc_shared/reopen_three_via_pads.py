import pathlib,shutil,json,importlib.util,xml.etree.ElementTree as E,copy,hashlib
p=pathlib.Path(r'D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration');s=importlib.util.spec_from_file_location('b',p/'run_pc_native_audit.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
m=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared');r=m/'via_reopen13';r.mkdir(exist_ok=False)
protected={};files=list((m/'via_new_stage').glob('*.pad'));assert len(files)==3
for f in files:protected[str(f)]=b.sha(f);shutil.copyfile(f,r/f.name)
env=b.envfor(r);run=b.launch([b.CAD/'tools/bin/padstack_editor.exe','-xo','*.pad'],r,env,60,'reexport');assert run['exit_code']==0
src=E.parse(m/'native_audits/pd13/source/pad2xml.pxml').getroot();actual=E.parse(r/'pad2xml.pxml').getroot()
def canon(x):
 return (x.tag,tuple(sorted(x.attrib.items())),(x.text or '').strip(),tuple(canon(y) for y in x if y.tag!='padstackname'))
rows=[]
for f in files:
 name=f.stem;old=name.removesuffix('_pc');a=next(x for x in src.findall('padstack') if x.findtext('padstackname').casefold()==old.casefold());z=next(x for x in actual.findall('padstack') if x.findtext('padstackname').casefold()==name.casefold());rows.append({'source_name':old,'new_name':name,'complete_xml_except_name_equal':canon(a)==canon(z),'sha256':b.sha(f),'new_bytes':f.stat().st_size})
assert all(b.sha(x)==h for x,h in protected.items())
b.dump(r/'report.json',{'status':'PASS_FULL_XML_EXCEPT_PADSTACKNAME' if all(x['complete_xml_except_name_equal'] for x in rows) else 'REVIEW_FULL_XML_DIFFERENCE','rows':rows,'reexport':run,'stage_unchanged':True,'import_warning':'Explicit internal layers L2/L3 preserved; official importer produced files and held informational warning window, owned process timed out at60s. This independent native reexport succeeded.'});print(json.dumps(rows))