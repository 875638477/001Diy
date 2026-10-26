import copy,xml.etree.ElementTree as E,pathlib,json,importlib.util
p=pathlib.Path(r'D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration')
s=importlib.util.spec_from_file_location('b',p/'run_pc_native_audit.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
m=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared');out=m/'via_new_stage';out.mkdir(exist_ok=False)
plan=json.loads((p/'VIA_PUBLIC_DEPENDENCY_DELTA.json').read_text(encoding='utf-8-sig'))
root=E.Element('padstacks');source=E.parse(m/'native_audits/pd13/source/pad2xml.pxml').getroot();protected={};rows=[]
for r in plan['rows']:
 src=pathlib.Path(r['source']['path']);pub=b.PUBLIC/'01Pad_lib'/(r['name']+'.pad');assert b.sha(src)==r['source']['sha256'];protected[str(src)]=b.sha(src);protected[str(pub)]=b.sha(pub)
 x=copy.deepcopy(next(x for x in source.findall('padstack') if x.findtext('padstackname').casefold()==r['name'].casefold()));x.find('padstackname').text=r['target'];root.append(x)
 assert not (b.PUBLIC/'01Pad_lib'/(r['target']+'.pad')).exists()
 rows.append({'old':r['name'],'target':r['target'],'source':str(src),'source_sha256':b.sha(src)})
input=out/'new_vias.pxml';E.indent(root);E.ElementTree(root).write(input,encoding='utf-8',xml_declaration=True)
env=b.envfor(out);imp=b.launch([b.CAD/'tools/bin/padstack_editor.exe','-x',input],out,env,60,'import')
assert imp['exit_code']==0 and len(list(out.glob('*.pad')))==3
exp=b.launch([b.CAD/'tools/bin/padstack_editor.exe','-xo','*.pad'],out,env,60,'export')
assert exp['exit_code']==0
assert all(b.sha(path)==h for path,h in protected.items())
b.dump(out/'report.json',{'status':'OFFICIAL_NEW_PAD_IMPORTED_AND_REOPEN_EXPORTED_PENDING_CANONICAL_REVIEW','rows':rows,'import':imp,'export':exp,'protected':protected,'protected_unchanged':True});print('3_NEW_VIA_PADS_READY_FOR_CANONICAL_REVIEW')