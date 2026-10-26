"""Create a new checker; never modify prior evidence or the original reviewer."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
OLD=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/tools/verify_public_olb_fp_stage.py')
OUT=M/'bounded_common_identity_checker13'
OUT.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
manifest={
 'schema':'EXACT_NATIVE_FROZEN_SOURCE_LIBRARY_IDENTITY_V1',
 'source_xml':str(M/'capture_defaults_reopened/native_library.xml'),
 'source_xml_sha256':sha(M/'capture_defaults_reopened/native_library.xml'),
 'opened_olb':str(M/'capture_stage/COMMON_PC.OLB'),
 'opened_olb_sha256':sha(M/'capture_stage/COMMON_PC.OLB'),
 'public_original':str(Path('D:/001DIY/005lib/01captureLib/COMMON_PC.OLB')),
 'public_original_sha256':sha('D:/001DIY/005lib/01captureLib/COMMON_PC.OLB'),
 'native_job_result':str(M/'capture_defaults_reopen_job/job_result.json'),
 'native_job_result_sha256':sha(M/'capture_defaults_reopen_job/job_result.json'),
 'owned_process':str(M/'capture_defaults_reopen_job/owned_process.json'),
 'owned_process_sha256':sha(M/'capture_defaults_reopen_job/owned_process.json'),
 'native_identity':str(M/'capture_defaults_reopened/NATIVE_LIBRARY_IDENTITY.tcldict'),
 'native_identity_sha256':sha(M/'capture_defaults_reopened/NATIVE_LIBRARY_IDENTITY.tcldict'),
 'original_reviewer':str(OLD),'original_reviewer_sha256':sha(OLD),
 'reason':'Frozen COMMON XML was natively exported from byte-identical pre-publication stage OLB; only this precise opened-path identity is admitted. All other library content remains fully ordered and exact.'
}
(OUT/'COMMON_FROZEN_SOURCE_IDENTITY_EVIDENCE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
source=OLD.read_text(encoding='utf-8-sig')
insert='''
def bounded_frozen_identity(evidence_path,case,root):
 z=load(evidence_path)
 need(z['schema']=='EXACT_NATIVE_FROZEN_SOURCE_LIBRARY_IDENTITY_V1','Unknown bounded source identity evidence schema')
 for field in ['source_xml','opened_olb','public_original','native_job_result','owned_process','native_identity','original_reviewer']:
  need(sha(z[field])==z[field+'_sha256'],'Bounded source identity artifact changed '+field)
 need(Path(z['source_xml']).resolve()==Path(case['frozen_source_xml']).resolve(),'Bounded source evidence names another frozen XML')
 need(z['source_xml_sha256']==case['frozen_source_xml_sha256'],'Bounded source XML SHA differs from frozen case')
 need(Path(z['public_original']).resolve()==Path(case['public_original']).resolve(),'Bounded evidence names another public library')
 need(z['opened_olb_sha256']==z['public_original_sha256']==case['original_sha256'],'Opened stage and actual original public bytes are not identical')
 job=load(z['native_job_result']);need(job['status']=='COMPLETE' and job['exit_code']==0 and job['protected_unchanged'] and job['protected_before']==job['protected_after'],'Incomplete/mutating bounded source native export')
 opened=str(Path(z['opened_olb']).resolve())
 need(job['protected_before'].get(opened)==case['original_sha256'],'Bounded native source was not SHA protected')
 argv=load(z['owned_process'])['command'];need(len(argv)==5,'Unexpected native source export argv count')
 need(Path(argv[2]).resolve()==Path(z['opened_olb']).resolve(),'Native export argv opened another OLB')
 need(Path(argv[4]).resolve()==Path(z['source_xml']).parent.resolve(),'Native export argv wrote another output')
 identity=Path(z['native_identity']).read_text(encoding='utf-8-sig')
 need('save_calls 0' in identity and z['opened_olb'] in identity,'Readonly native identity record does not bind opened source')
 norm_name(root,z['opened_olb'])
 return {'opened_identity':z['opened_olb'],'public_identity':z['public_original'],'identical_OLB_sha256':case['original_sha256'],'evidence_path':str(evidence_path),'evidence_sha256':sha(evidence_path),'native_argv':argv,'source_xml_sha256':z['source_xml_sha256']}
'''
token='def main():\n'
assert source.count(token)==1
source=source.replace(token,insert+'\n'+token)
token="ap.add_argument('--case',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);"
assert source.count(token)==1
source=source.replace(token,token+"ap.add_argument('--frozen-source-identity-evidence',type=Path);")
token="need(can(norm_name(base,public))==can(norm_name(src,original)),'Re-exported original snapshot is not complete original frozen library XML')"
assert source.count(token)==1
source=source.replace(token,"source_identity=bounded_frozen_identity(a.frozen_source_identity_evidence,c,base) if a.frozen_source_identity_evidence else None\n  frozen_expected=source_identity['opened_identity'] if source_identity else public\n  need(can(norm_name(base,frozen_expected))==can(norm_name(src,original)),'Re-exported original snapshot is not complete original frozen library XML')")
token="'public_files_replaced':0})"
assert source.count(token)==1
source=source.replace(token,"'public_files_replaced':0,'bounded_frozen_source_identity':source_identity})")
target=OUT/'verify_public_olb_fp_stage_bounded_identity_v2.py'
target.write_text(source,encoding='utf-8')
print(json.dumps({'checker':str(target),'checker_sha256':sha(target),'evidence':str(OUT/'COMMON_FROZEN_SOURCE_IDENTITY_EVIDENCE.json'),'evidence_sha256':sha(OUT/'COMMON_FROZEN_SOURCE_IDENTITY_EVIDENCE.json')},indent=2))
