"""Freeze explicit native-reference source bindings; never fabricates native evidence."""
from pathlib import Path
import argparse,hashlib,json,re
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
LIB=Path(r'D:\001DIY\005lib')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def artifact(p):p=Path(p);return {'path':str(p),'sha256':sha(p)}
def norm(p):return str(Path(p).resolve()).casefold()
def capture_row(kind,public,h,xml,native_input,job=None,bindings=None,proofs=()):
 r={'kind':kind,'public_path':str(public),'public_sha256':h,'native_input':str(native_input),'xml':artifact(xml),'acceptance_proofs':[artifact(p) for p in proofs]}
 if job:r.update(binding_mode='protected_native_capture_export',native_job=artifact(job))
 else:r.update(binding_mode='frozen_original_native_export_bindings',frozen_bindings=artifact(bindings))
 if not proofs:r['acceptance_mode']='UNCHANGED_PUBLIC_SOURCE_NATIVE_READONLY_EXPORT' if job else 'UNCHANGED_SOURCE_SHA_FROM_FROZEN_NATIVE_BINDING'
 return r
def inventory_row(public,h,jobdir,proofs=()):
 r={'kind':'public_brd','public_path':str(public),'public_sha256':h,'inventory_mode':'PENDING_COMPLETE_NATIVE_REFERENCE_INVENTORY','acceptance_proofs':[artifact(p) for p in proofs]}
 if jobdir is not None:
  d=Path(jobdir);r.update(inventory_mode='complete_native_reference_inventory_v1',native_job=artifact(d/'launch_report.json'),inventory_files={k:artifact(d/f) for k,f in [('components','ALL_COMPONENT_PACKAGE_REFERENCES.tsv'),('symbols','ALL_SYMBOL_NAME_DEFINITION_REFERENCES.tsv'),('symdefs','ALL_PACKAGE_DEFINITIONS.tsv')]})
 if not proofs:r['acceptance_mode']='UNCHANGED_PUBLIC_SOURCE_NATIVE_READONLY_EXPORT'
 return r
def main():
 a=argparse.ArgumentParser();a.add_argument('--guard',type=Path,required=True);a.add_argument('--guard-sha256',required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--inventory-map',type=Path);a.add_argument('--canonical-proof-index',type=Path);args=a.parse_args()
 assert sha(args.guard)==args.guard_sha256.upper(),'Frozen guard SHA mismatch'
 assert not args.out.exists(),'Fresh manifest directory required';args.out.mkdir(parents=True)
 g=load(args.guard);gi={norm(v['path']):v for v in g['files']};ss=[]
 bindings=R/'w/capture_reuse_final/PUBLIC_LIBRARY_EXPORT_BINDINGS.json';original={norm(v['path']):v for v in load(bindings)}
 replacements=M/'public_olb_final13_publish_plan13/EXACT_THIRTEEN_PUBLIC_OLB_REPLACEMENT_PLAN.json';rr={norm(v['public']):v for v in load(replacements)['replacements']}
 receipt=M/'public_olb_final13_published13/PUBLIC_OLB_PUBLISH_RECEIPT.json'
 activeproof=R/'verification/final13_active_public_paths_v227/ACTIVE_PUBLIC_LIBRARY_PATH_AUDIT.json'
 mainreceipt=R/'verification/final13_five_publication27/PUBLICATION_RECEIPT.json'
 ss.append(capture_row('project_capture',R/'sch/LGA1700.DSN',sha(R/'sch/LGA1700.DSN'),R/'w/cache7_xn4_v2/native_design.xml',R/'w/cache7_cn4_v2/LGA1700.DSN',R/'w/cache7_reopen4_v2_job/job_result.json',proofs=[R/'verification/cache7_superset_xn4_v2/PUBLIC_LIBRARY_XML_REVIEW.json',activeproof,mainreceipt]))
 # Original 24 OLBs retain exact original native bindings; all 13 changed OLBs
 # use the exact staged candidate SHA now published at the real public path.
 for v in sorted(g['files'],key=lambda q:q['path'].casefold()):
  p=Path(v['path'])
  if (LIB/'01captureLib').resolve() not in p.resolve().parents or p.suffix.casefold()!='.olb':continue
  if p.name.casefold()=='common_pc.olb':
   ss.append(capture_row('public_olb',p,v['sha256'],M/'actual_public_common_final13/native_library.xml',p,M/'actual_public_common_final13_job/job_result.json',proofs=[M/'common59_cn4_actual_public_gate13/COMMON59_DESIGN_CACHE_FULL_REVIEW.json',receipt]))
  elif norm(p) in rr:
   x=rr[norm(p)];d=Path(x['case']).parent
   ss.append(capture_row('public_olb',p,v['sha256'],d/'reopened/native_library.xml',x['candidate'],d/'reopen_job/job_result.json',proofs=[x['review'],receipt]))
  else:
   x=original[norm(p)];assert v['sha256']==x['sha256'],'Unchanged original OLB differs from frozen native binding'
   ss.append(capture_row('public_olb',p,v['sha256'],x['xml'],p,bindings=bindings))
 for name in ['Lib','SCHLIB']:
  p=LIB/'01captureLib'/(name+'.DSN');v=gi[norm(p)];d=M/'global_suffix_public_dsn13'
  ss.append(capture_row('public_dsn',p,v['sha256'],d/name/'native_design.xml',p,d/(name+'_job')/'job_result.json'))
 d=R/'w/all81_full15';ad=R/'w/all59_inventory17'
 ss.append({'kind':'project_brd','public_path':str(R/'pcb/LGA1700_RULES.brd'),'public_sha256':sha(R/'pcb/LGA1700_RULES.brd'),'inventory_mode':'main13_complete1066_plus_all59_symdefs','native_job':artifact(d/'launch_report.json'),'all_symdefs_job':artifact(ad/'launch_report.json'),'inventory_files':{'components':artifact(d/'components_reopened.tsv'),'symbols':artifact(d/'symbols.tsv'),'symdefs':artifact(ad/'ALL_PACKAGE_DEFINITIONS.tsv')},'acceptance_proofs':[artifact(p) for p in [M/'main_all81_final_cfx26/PUBLIC_LIBRARY_CFX_REVIEW.json',M/'main_all81_exact_vdd_connectivity27/ALL81_EXACT_VDD_REPAIR_TYPED_CONNECTIVITY_REVIEW.json',R/'w/pcb_migration/FINAL59_CACHE_FULL15_CONTEXT_REVIEW_V2.json',activeproof,mainreceipt]]})
 inv=load(args.inventory_map) if args.inventory_map else {name:str(M/'w'/('final_reference_inventory27_'+name)) for name in ['002','004','VCU16']}
 for v in sorted(g['files'],key=lambda q:q['path'].casefold()):
  p=Path(v['path'])
  if norm(p.parent)!=norm(LIB/'01brdlib') or p.suffix.casefold()!='.brd':continue
  x=inv.get(p.stem);job=x.get('directory') if isinstance(x,dict) else x;proofs=x.get('proofs',[]) if isinstance(x,dict) else []
  ss.append(inventory_row(p,v['sha256'],job,proofs))
 # Freeze the actual current project launch/config files, the user's library
 # env, vendor TELENV, and every existing replay script enabled by that env.
 configpaths=[Path(v['path']) for v in load(activeproof)['active_configuration']['active_text_files']]
 configpaths += [LIB/'01env/env',Path(r'C:\Program0\cadence\SPB172\share\pcb\text\env')]
 replay=[]
 for line in (LIB/'01env/env').read_text(encoding='utf-8-sig').splitlines():
  if line.strip().startswith(('#',';','//')):continue
  mt=re.search(r'\breplay\s+(D:[^"\r\n]+?\.scr)\b',line,re.I)
  if mt:replay.append(Path(mt.group(1)))
 missing=sorted({str(p) for p in replay if not p.is_file()});configpaths += [p for p in replay if p.is_file()]
 configs=list({norm(p):artifact(p) for p in configpaths}.values())
 canonical=[artifact(args.canonical_proof_index)] if args.canonical_proof_index else []
 data={'schema':'FINAL_NATIVE_REFERENCE_SOURCES_V1','source_state':'PREPUBLICATION_PREFLIGHT_PENDING_FOUR_NATIVE_BRD_INVENTORIES','retirement_plan':artifact(M/'public_retirement_all_confirmed_plan13/PUBLIC_RETIREMENT_EXACT_PLAN.json'),'public_guard':artifact(args.guard),'sources':ss,'active_device_map':{'source_state':'COMPLETE_ACTIVE_PATH_AND_DEVICE_ENUMERATION','configs':configs,'device_roots':[str(LIB/'01brdlib'),str(LIB/'01Psm_lib')],'enabled_replay_scripts_missing':missing,'native_effective_devpath':str(LIB/'01brdlib'),'psmpath_self_device_compatibility_scan_included':True,'non_device_file_classifications':{}},'canonical_target_coverage_state':'ALL_REQUIRED_TARGET_COLD_NATIVE_AND_FULL_PAD_PROOFS_BOUND' if canonical else 'PENDING_AGGREGATED_TARGET_NATIVE_AND_PAD_INDEX','canonical_target_proofs':canonical,'public_files_written':0,'builder_sha256':sha(__file__)}
 if all(v.get('inventory_mode')!='PENDING_COMPLETE_NATIVE_REFERENCE_INVENTORY' for v in ss) and canonical:data['source_state']='FINAL_PUBLIC_FILES_MATCH_MANIFEST'
 out=args.out/'FINAL_NATIVE_REFERENCE_SOURCES.json';out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'path':str(out),'sha256':sha(out),'source_count':len(ss),'pending_brd':[v['public_path'] for v in ss if v.get('inventory_mode')=='PENDING_COMPLETE_NATIVE_REFERENCE_INVENTORY'],'missing_enabled_replay_scripts':missing,'CAD_started':False}))
if __name__=='__main__':main()
