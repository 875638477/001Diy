"""Independent exact source21 path/material phase review; no global tolerance."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from decimal import Decimal
import argparse,hashlib,json,sys
M=Path(__file__).parent
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
KEYS=[1,2,4,5,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25]
def need(v,m):
 if not v:raise ValueError(m)
def rows(p):return parse_many(p.read_text('utf-8-sig'))
def validate(v):
 need(v['source_sha']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898' and v['partial_sha']=='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A','Protected source/partial binding')
 need(v['source_keys']==KEYS and v['preflight_keys']==KEYS and v['created_keys']==KEYS,'Finite exact21 real paths, exclude4 purely-land cases')
 need(v['source_rpaths_native_exact'],'Source actual paths vs detached r_path copper differs')
 need(v['foreign_before_zero'] and v['foreign_after_zero'],'Actual foreign copper intersection')
 need(v['full_three_net_after_subset_before_plus_source'] and v['full_three_net_preexisting_retained'] and v['full_source21_retained'],'Exact full affected3net union AFTER=BEFORE union SOURCE21 failed')
 need(v['all25_missing_outside_old_pad_zero'],'Original thermal material still lost outside actual old regular pads')
 need(v['all_cached_graphs_exact'],'Package/pad/figure/textblock/property cache changed')
 need(v['all1739_source_vias_exact'] and v['via_count']==1739,'Full typed original1739 via inventory changed')
 need(v['root_finite_decision_bound'],'Unbound scope change')
 return True
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run',type=Path,required=True);ap.add_argument('--partition-review',type=Path);ap.add_argument('--cache-bijection-review',type=Path,required=True);a=ap.parse_args();r=a.run
 rec=json.loads((r/'RUN_RECEIPT.json').read_text('utf-8-sig'))
 need(rec['status']=='SAVED_UNAPPROVED_PRIVATE_CANDIDATE_PENDING_FRESH_COMPLETE70_CACHE_915_CFX' and rec['public_unchanged'],'Native phase incomplete/public changed')
 need(rec['source_sha256_before']==rec['source_sha256_after'] and rec['candidate_input_sha256_before']==rec['candidate_input_sha256_after'],'Protected inputs changed')
 need((r/'SOURCE21_ORIGINAL_THERMAL_PENDING_CACHE_COMPLETE.txt').is_file(),'Missing complete native marker')
 source=rows(r/'SOURCE21_ACTUAL_PATH_RPATH_PROOF.ilist');pre=rows(r/'SOURCE21_FULL_PATH_FOREIGN_CU_PREFLIGHT.ilist');created=rows(r/'RECREATED_SOURCE21_NATIVE_PATHS.ilist');union=rows(r/'FULL_THREE_NET_BOTTOM_CU_UNION_EQUIVALENCE.ilist')
 tags=Counter(x[0] for x in union)
 need(set(tags)=={'AFTER_MINUS_BEFORE_AND_SOURCE21','PREEXISTING_CU_MINUS_AFTER','SOURCE21_PATH_MINUS_AFTER','ALL25_MISSING_OUTSIDE_OLD_ACTUAL_PAD_AFTER'} and tags['AFTER_MINUS_BEFORE_AND_SOURCE21']>0 and tags['PREEXISTING_CU_MINUS_AFTER']>0 and tags['SOURCE21_PATH_MINUS_AFTER']==21 and tags['ALL25_MISSING_OUTSIDE_OLD_ACTUAL_PAD_AFTER']==25,'Complete global3-net raw proof missing')
 def allzero(values):return all(v[0]==0 and v[1]==0 for v in values)
 b=(r/'BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist').read_text('utf-8').splitlines();e=(r/'AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist').read_text('utf-8').splitlines()
 sv=(r/'SOURCE_ALL1739_TYPED_VIAS.ilist').read_text('utf-8').splitlines();av=(r/'AFTER_ALL1739_TYPED_VIAS.ilist').read_text('utf-8').splitlines()
 decision=M/'FINITE_SOURCE_THERMAL_PATH_RESTORE_DECISION27.json'
 bij=json.loads(a.cache_bijection_review.read_text('utf-8-sig'))
 need(bij['status']=='PASS_COMPLETE_NATIVE_CACHE_EXACT_UNDER_EXPLICIT_ID_BIJECTION','Strict all-field cache ID bijection failed')
 need(bij['before_sha256']==sha(r/'BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist') and bij['after_sha256']==sha(r/'AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist'),'Strict cache bijection does not bind this actual job')
 need(bij['proof']['full_roots']==79 and bij['proof']['full_objects']==20080 and bij['proof']['zero_ignored_attributes'] and bij['proof']['zero_numeric_tolerance'],'Complete79 cached definitions incl9unused all-field proof required')
 proof=dict(source_sha=rec['source_sha256_before'],partial_sha=rec['candidate_input_sha256_before'],source_keys=[int(x[0]) for x in source],preflight_keys=[int(x[0]) for x in pre],created_keys=sorted(set(int(x[0]) for x in created)),source_rpaths_native_exact=all(x[-1]=='DETACHED_RPATH_VS_SOURCE_NATIVE_ANDNOT_BOTH_EMPTY' for x in source),foreign_before_zero=allzero(x[5] for x in pre),foreign_after_zero=allzero(x[4] for x in union if x[0]=='SOURCE21_PATH_MINUS_AFTER'),full_three_net_after_subset_before_plus_source=allzero(x[3] for x in union if x[0]=='AFTER_MINUS_BEFORE_AND_SOURCE21'),full_three_net_preexisting_retained=allzero(x[3] for x in union if x[0]=='PREEXISTING_CU_MINUS_AFTER'),full_source21_retained=allzero(x[2] for x in union if x[0]=='SOURCE21_PATH_MINUS_AFTER'),all25_missing_outside_old_pad_zero=allzero(x[2] for x in union if x[0]=='ALL25_MISSING_OUTSIDE_OLD_ACTUAL_PAD_AFTER'),all_cached_graphs_exact=bij['status']=='PASS_COMPLETE_NATIVE_CACHE_EXACT_UNDER_EXPLICIT_ID_BIJECTION',all1739_source_vias_exact=sv==av,via_count=len(sv),root_finite_decision_bound=sha(decision)=='9DB6EEC822612E12D76174C5098E7A362BDDCC18B69F919E1EAC4272FDF5F086')
 validate(proof)
 controls=[]
 for k,v in [('source_sha','BAD'),('source_keys',KEYS+[3]),('created_keys',KEYS[:-1]),('source_rpaths_native_exact',False),('foreign_before_zero',False),('foreign_after_zero',False),('full_three_net_after_subset_before_plus_source',False),('full_three_net_preexisting_retained',False),('full_source21_retained',False),('all25_missing_outside_old_pad_zero',False),('all_cached_graphs_exact',False),('all1739_source_vias_exact',False),('via_count',1738),('root_finite_decision_bound',False)]:
  p=deepcopy(proof);p[k]=v
  try:validate(p)
  except ValueError:controls.append(dict(mutation=k,result='REJECTED'))
  else:raise ValueError('Negative control not rejected '+k)
 partition=None
 if a.partition_review:
  partition=json.loads(a.partition_review.read_text('utf-8-sig'));need(partition['status']=='PASS_FULL2698_TYPED_PHYSICAL_CONNECTION_PARTITION_EXACT','Fresh full2698/915 gate failed');need(partition['candidate_board_sha256']==rec['candidate_sha256'],'Fresh partition source candidate mismatch');need(partition['partitions']['pass_exact'] and partition['partitions']['source_groups']==partition['partitions']['candidate_groups']==915,'Member-exact915 partition required')
 thermal_flags=Counter(str(x[-2]) for x in created)
 report=dict(status='PASS_FINITE_SOURCE21_THERMAL_CU_PHASE_AND_FRESH915_EXACT' if partition else 'PASS_FINITE_SOURCE21_THERMAL_CU_PHASE_FRESH915_AND_CFX_REQUIRED',source_board_sha256=proof['source_sha'],partial_board_sha256=proof['partial_sha'],candidate=rec['candidate'],candidate_sha256=rec['candidate_sha256'],finite_source_paths=21,proof=proof,zero_numeric_tolerance=True,zero_source_external_Cu_exception=True,created_native_thermal_flag_counts=dict(thermal_flags),created_paths_not_claimed_dynamic_thermal=True,whole_old_pad_not_cloned=True,original_board_path_Cu_inside_old_pad_permitted_only_under_bound_finite_decision=True,global_native_union_raw_counts=dict(tags),negative_controls=controls,cache_raw_byte_difference_preserved_as_historical_identity_FAIL=True,cache_full_typed_id_bijection_review=str(a.cache_bijection_review),cache_full_typed_id_bijection_review_sha256=sha(a.cache_bijection_review),cache_actual_complete_symdefs_including_unused=79,cache_fresh_public70_gate_still_required=True,full915_review=str(a.partition_review) if a.partition_review else None,full915_review_sha256=sha(a.partition_review) if a.partition_review else None,CFX_full_public_PAD_cache_and_final_publication_still_separate_gates=True,evidence=[dict(path=str(p),sha256=sha(p)) for p in [r/'RUN_RECEIPT.json',r/'SOURCE21_ACTUAL_PATH_RPATH_PROOF.ilist',r/'SOURCE21_FULL_PATH_FOREIGN_CU_PREFLIGHT.ilist',r/'RECREATED_SOURCE21_NATIVE_PATHS.ilist',r/'FULL_THREE_NET_BOTTOM_CU_UNION_EQUIVALENCE.ilist',r/'ORIGINAL21_THERMAL_CU_NATIVE_POLYGONS.jsonl',decision]])
 out=r/'FINITE_ORIGINAL21_THERMAL_CU_REVIEW_V5.json';out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(dict(report=str(out),sha256=sha(out),status=report['status'],negative_controls=len(controls)),indent=2))
if __name__=='__main__':main()
