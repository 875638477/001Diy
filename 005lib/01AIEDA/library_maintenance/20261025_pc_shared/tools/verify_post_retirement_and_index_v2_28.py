"""Read-only post-retirement six-root verification and derived expected guard.
Derives expected remaining entries from the frozen pre-delete guard minus exactly
the approved3069 assets; never adopts a new scan as expected state.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,importlib.util,json
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
GUARD_SHA='C2835B5651C473873A8664AC68520E32795B3D09E8BBF0134AE5BA13BA6DBBEC'
CLOSURE_SHA='8EA5E5694F18B663FE2D32B30FCB6128F8C7FD8A6F6465F818FA91F9BBABCDEC'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def art(p):return {'path':str(Path(p)),'sha256':sha(p)}
def norm(p):return str(Path(p).resolve()).casefold()
def need(v,s):
 if not v:raise ValueError(s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--apply-receipt',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists(),'Fresh post-retirement output required')
 receipt=load(a.apply_receipt);need(receipt['status']=='PASS_EXACT_RETIRED_ENTRIES_BACKED_UP_OTHER_PUBLIC_BYTES_UNCHANGED' and receipt['mode']=='apply' and receipt['public_files_removed']==3069 and receipt['remaining_public_files']==10364,'Actual retirement apply is not complete PASS')
 gp=Path(receipt['guard']['path']);need(sha(gp)==receipt['guard']['sha256']==GUARD_SHA,'Wrong frozen pre-retirement public guard')
 pp=Path(receipt['plan']);plan=load(pp);need(sha(pp)==receipt['plan_sha256'],'Exact retirement plan changed');need(plan['accepted_alias_count']==1067 and len(plan['assets'])==plan['asset_count']==3069,'Wrong exact retirement cohort')
 cp=Path(receipt['closure']['path']);closure=load(cp);need(sha(cp)==receipt['closure']['sha256']==CLOSURE_SHA and closure['status']=='PASS_NATIVE_REFERENCE_CLOSURE','Final actual reference closure changed')
 need(closure['current_public_guard']==art(gp),'Closure did not bind published pre-delete public bytes')
 spec=importlib.util.spec_from_file_location('retirement_post_readonly_check',M/'retire_exact_public_assets_v2.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
 guard=load(gp);before={norm(v['path']):v for v in guard['files']};assets={norm(v['path']):v for v in plan['assets']};need(len(before)==13433 and len(assets)==3069 and set(assets)<=set(before),'Frozen public source/removal set differs')
 for key,v in assets.items():
  need(not Path(v['path']).exists(),'Approved retirement entry still exists '+v['path']);need(before[key]['sha256']==v['sha256'] and before[key]['bytes']==v['bytes'],'Retirement row not exact original guarded bytes')
 expected={k:v for k,v in before.items() if k not in assets};actual=V.actual_files();need(len(expected)==len(actual)==10364 and set(expected)==set(actual),'Remaining six-root file set differs from exact subtraction')
 byroot=Counter();actualbytes=0;root_prefixes=[(norm(root)+'\\',str(root)) for root in V.ALLOWED_ROOTS]
 for key,v in expected.items():
  p=actual[key];need(p.stat().st_size==v['bytes'] and sha(p)==v['sha256'],'Unretired file bytes changed '+str(p));actualbytes+=v['bytes'];byroot[next(root for prefix,root in root_prefixes if key.startswith(prefix))]+=1
 # Recheck all actual design/source/native/PAD evidence after deletion; none
 # of these necessary files may be an accidentally retired live dependency.
 postcl=V.closure(cp,pp,plan)
 stage=load(a.apply_receipt.parent/'BACKUP_STAGE.json');need(stage['status']=='PASS_ALL_MEMBERS_ZIP_SHA_ROUNDTRIP_PUBLIC_UNCHANGED' and stage['plan_sha256']==sha(pp),'Frozen exact backup stage changed')
 backup=V.backup_bundle_verify(stage['backup_bundle'],plan['assets'])
 # Retain all13 original OLB ZIPs in addition to the retirement bundle and
 # original four BRD backup; current formal files are never modified here.
 olbplan=M/'public_olb_final13_publish_plan13/EXACT_THIRTEEN_PUBLIC_OLB_REPLACEMENT_PLAN.json';oldolbs=[]
 for row in load(olbplan)['replacements']:
  p=Path(row['existing_original_zip']);need(sha(p)==row['existing_original_zip_sha256'],'Original OLB backup archive changed');oldolbs.append(art(p))
 br=load(M/'original_public_four_brd_backup13/BACKUP_RECEIPT.json');need(sha(br['archive'])==br['archive_sha256'],'Original four BRD backup archive changed')
 derived=copy.deepcopy(guard);derived['files']=[v for v in guard['files'] if norm(v['path']) not in assets];derived.update(status='EXPECTED_PUBLIC_BYTES_BY_EXACT3069_RETIREMENT_WITH_ALL10364_SURVIVORS_UNCHANGED',source_guard=art(gp),exact_retirement_plan=art(pp),exact_native_reference_closure=art(cp),exact_apply_receipt=art(a.apply_receipt),exact_removed_assets=plan['assets'])
 a.out.mkdir(parents=True);dg=a.out/'PUBLIC_GUARD_AFTER_EXACT3069_RETIREMENT.json';dg.write_text(json.dumps(derived,ensure_ascii=False,indent=2),encoding='utf-8')
 report={'status':'PASS_POST_RETIREMENT_EXACT3069_REMOVED_ALL10364_SIX_ROOT_FILES_UNCHANGED','before_guard':art(gp),'derived_expected_guard':art(dg),'apply_receipt':art(a.apply_receipt),'retirement_plan':art(pp),'removed_exact_assets':3069,'remaining_exact_files':10364,'remaining_files_by_root':dict(byroot),'remaining_bytes':actualbytes,'all1067_source_stems_predelete_actual_zero_in_all8_categories':True,'post_delete_all1065_actual_evidence_SHA_still_valid':postcl,'retirement_backup_allmembers_roundtrip':backup,'original13_OLB_ZIP_archives_preserved':oldolbs,'original_four_BRD_ZIP_preserved':art(br['archive']),'expected_guard_is_frozen_source_minus_exact_plan_not_new_scan':True,'CAD_started':False,'public_files_written':0,'public_files_removed':0,'script_sha256':sha(__file__)}
 rp=a.out/'POST_RETIREMENT_SIX_ROOT_VERIFICATION.json';rp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 proofs=[rp,cp,M/'canonical_retirement_target127_v127/REQUIRED_CANONICAL_NATIVE_TARGET_INDEX.json',M/'retirement_native_negative_controls27/RETIREMENT_NATIVE_NEGATIVE_CONTROLS.json',M/'public_olb_final13_published13/PUBLIC_OLB_PUBLISH_RECEIPT.json',M/'common59_cn4_actual_public_gate13/COMMON59_DESIGN_CACHE_FULL_REVIEW.json',M/'public_four_final_native_published28/PUBLISH_RECEIPT.json',M/'public_three_module_final_acceptance25/FINAL_THREE_MODULE_NATIVE_ACCEPTANCE.json',M/'public0010_final_private_gates_index13_v1/PUBLIC0010_FINAL_PRIVATE_EXECUTED_PROOFS_INDEX.json',R/'verification/final13_five_publication27/PUBLICATION_RECEIPT.json',M/'main_all81_final_cfx26/PUBLIC_LIBRARY_CFX_REVIEW.json',M/'main_all81_exact_vdd_connectivity27/ALL81_EXACT_VDD_REPAIR_TYPED_CONNECTIVITY_REVIEW.json']
 for p in proofs:need(str(load(p)['status']).startswith('PASS'),'Completion proof not PASS '+str(p))
 index={'status':'PASS_PUBLIC_LIBRARY_STANDARDIZATION_PUBLICATION_REFERENCE_CLOSURE_AND_EXACT_RETIREMENT','scope':'Library maintenance completion index; linked design gates retain their exact geometry, connectivity and bounded metadata decisions. Does not claim post-ECO DRC was rerun on module008.','main_formal_DSN':art(R/'sch/LGA1700.DSN'),'main_formal_BRD':art(R/'pcb/LGA1700_RULES.brd'),'current_expected_public_guard':art(dg),'proofs':[dict(art(p),status=load(p)['status']) for p in proofs],'method_document':art(M/'RETIREMENT_ACTUAL_REFERENCE_CLOSURE_METHOD_20261026.md'),'actual_retirement_execution':{'deleter':art(M/'retire_exact_public_assets_v2.py'),'read_only_resume':art(M/'tools/resume_retirement_readonly_postcheck28.py'),'future_optimized_deleter':art(M/'retire_exact_public_assets_v3.py'),'future_v3_was_not_applied_in_this_task':True},'reusable_tools':[art(M/'tools'/n) for n in ['scan_retirement_native_references_final27.py','complete_retirement_four_brd_sources27.py','run_public7_reference_inventory27.py','public_all_reference_inventory27.il','verify_retirement_canonical_targets_v2_27.py','verify_post_retirement_and_index_v2_28.py']],'actual_result':{'retired_alias_stems':1067,'deleted_exact_PSM_DRA_selfTXT_files':3069,'remaining_unchanged_public_files':10364,'native_actual_source_coverage':48,'reference_categories_each_stem':8,'all_actual_alias_reference_counts':0,'canonical_targets':127,'full_manufacturing_PAD_objects':154},'historical_failure_reports_and_original_ZIPs_preserved':True,'CAD_started':False,'public_files_written':0}
 ix=a.out/'FINAL_LIBRARY_MAINTENANCE_COMPLETION_INDEX.json';ix.write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'report':art(rp),'new_guard':art(dg),'completion_index':art(ix)},ensure_ascii=False))
if __name__=='__main__':main()
