"""Exercise source identity proof rejection without modifying native inputs."""
from pathlib import Path
import copy,hashlib,importlib.util,json,xml.etree.ElementTree as E
M=Path(__file__).parent;D=M/'bounded_common_identity_checker13';OUT=D/'identity_negative_controls';OUT.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('bounded',D/'verify_public_olb_fp_stage_bounded_identity_v2.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
source=D/'COMMON_FROZEN_SOURCE_IDENTITY_EVIDENCE.json';e=json.loads(source.read_text('utf-8'));case=json.loads((M/'public_olb_final7_stage13/05_COMMON_PC/STAGING_CASE.json').read_text('utf-8'));root=E.parse(case['frozen_source_xml']).getroot();controls=[]
def trial(name,mutate):
 c,z,r=copy.deepcopy(case),copy.deepcopy(e),copy.deepcopy(root);mutate(c,z,r);path=OUT/(name+'.json');path.write_text(json.dumps(z,indent=2),encoding='utf-8')
 try:mod.bounded_frozen_identity(path,c,r)
 except Exception as ex:controls.append({'name':name,'status':'PASS_REJECTED','reason':str(ex)})
 else:raise RuntimeError('Identity negative control accepted '+name)
trial('wrong_frozen_XML_SHA',lambda c,z,r:z.update(source_xml_sha256='0'*64))
trial('wrong_stage_OLB_SHA',lambda c,z,r:z.update(opened_olb_sha256='0'*64))
trial('different_public_library_even_identical_bytes',lambda c,z,r:z.update(public_original=c['original_snapshot']))
trial('different_library_name_in_XML',lambda c,z,r:r.find('Defn').set('name','D:/WRONG.OLB'))
def wrong_argv(c,z,r):
 q=json.loads(Path(z['owned_process']).read_text('utf-8'));q['command'][2]=c['public_original'];p=OUT/'wrong_argv_owned_process.json';p.write_text(json.dumps(q,indent=2),encoding='utf-8');z['owned_process']=str(p);z['owned_process_sha256']=mod.sha(p)
trial('native_job_argv_opened_other_library',wrong_argv)
def wrong_output(c,z,r):
 q=json.loads(Path(z['owned_process']).read_text('utf-8'));q['command'][4]='D:/wrong_output';p=OUT/'wrong_output_owned_process.json';p.write_text(json.dumps(q,indent=2),encoding='utf-8');z['owned_process']=str(p);z['owned_process_sha256']=mod.sha(p)
trial('native_job_argv_wrote_other_XML_directory',wrong_output)
report={'status':'PASS_BOUNDED_FROZEN_IDENTITY_CONTROLS_ALL_REJECTED','controls':controls,'count':len(controls),'original_case_sha256':mod.sha(M/'public_olb_final7_stage13/05_COMMON_PC/STAGING_CASE.json'),'identity_evidence_sha256':mod.sha(source),'checker_sha256':mod.sha(D/'verify_public_olb_fp_stage_bounded_identity_v2.py'),'public_files_modified':0}
(OUT/'IDENTITY_NEGATIVE_CONTROLS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
