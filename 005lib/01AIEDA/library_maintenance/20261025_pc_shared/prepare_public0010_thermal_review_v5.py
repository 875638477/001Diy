"""Derive the pending-candidate review; require the strict raw-ID bijection proof."""
from pathlib import Path
M=Path(__file__).parent
def main():
 s=(M/'review_public0010_original_thermal_restore_v4.py').read_text()
 s=s.replace("ap.add_argument('--partition-review',type=Path);a=ap.parse_args();r=a.run","ap.add_argument('--partition-review',type=Path);ap.add_argument('--cache-bijection-review',type=Path,required=True);a=ap.parse_args();r=a.run")
 s=s.replace("rec['status']=='PASS_FINITE_ORIGINAL21_THERMAL_PATH_PHASE_ONLY'","rec['status']=='SAVED_UNAPPROVED_PRIVATE_CANDIDATE_PENDING_FRESH_COMPLETE70_CACHE_915_CFX'")
 s=s.replace('SOURCE21_ORIGINAL_THERMAL_RESTORE_COMPLETE.txt','SOURCE21_ORIGINAL_THERMAL_PENDING_CACHE_COMPLETE.txt')
 before="proof=dict(source_sha=rec['source_sha256_before']"
 after="""bij=json.loads(a.cache_bijection_review.read_text('utf-8-sig'))
 need(bij['status']=='PASS_COMPLETE_NATIVE_CACHE_EXACT_UNDER_EXPLICIT_ID_BIJECTION','Strict all-field cache ID bijection failed')
 need(bij['before_sha256']==sha(r/'BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist') and bij['after_sha256']==sha(r/'AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist'),'Strict cache bijection does not bind this actual job')
 need(bij['proof']['full_roots']==79 and bij['proof']['full_objects']==20080 and bij['proof']['zero_ignored_attributes'] and bij['proof']['zero_numeric_tolerance'],'Complete79 cached definitions incl9unused all-field proof required')
 proof=dict(source_sha=rec['source_sha256_before']"""
 assert before in s;s=s.replace(before,after)
 s=s.replace("all_cached_graphs_exact=sorted(b)==sorted(e) and len(b)>0","all_cached_graphs_exact=bij['status']=='PASS_COMPLETE_NATIVE_CACHE_EXACT_UNDER_EXPLICIT_ID_BIJECTION'")
 s=s.replace("full915_review=str(a.partition_review) if a.partition_review else None,","cache_raw_byte_difference_preserved_as_historical_identity_FAIL=True,cache_full_typed_id_bijection_review=str(a.cache_bijection_review),cache_full_typed_id_bijection_review_sha256=sha(a.cache_bijection_review),cache_actual_complete_symdefs_including_unused=79,cache_fresh_public70_gate_still_required=True,full915_review=str(a.partition_review) if a.partition_review else None,")
 s=s.replace('FINITE_ORIGINAL21_THERMAL_CU_REVIEW.json','FINITE_ORIGINAL21_THERMAL_CU_REVIEW_V5.json')
 out=M/'review_public0010_original_thermal_restore_v5.py';out.write_text(s,'utf-8');print(out)
if __name__=='__main__':main()
