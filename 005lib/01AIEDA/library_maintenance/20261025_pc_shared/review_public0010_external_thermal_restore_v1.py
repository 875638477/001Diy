"""Independent bounded audit of the 21 source-only outside-old-land fragments."""
from pathlib import Path
from decimal import Decimal
from copy import deepcopy
import argparse,hashlib,json,sys
M=Path(__file__).parent
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
from sexpr import parse_many
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
KEYS=[1,2,4,5,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25]
def need(v,m):
 if not v:raise ValueError(m)
def read_native(p):return parse_many(p.read_text('utf-8-sig'))
def validate(v):
 need(v['source_sha']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898' and v['partial_sha']=='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A','Frozen protected source/partial binding')
 need(v['pre_keys']==list(range(1,26)) and v['approved_external_keys']==KEYS and v['created_keys']==KEYS,'Whole25/exact21 approved set')
 need(v['foreign_before_zero'] and v['foreign_after_zero'],'Native actual foreign copper intersection')
 need(v['outside_old_pad_after_zero'],'Original source copper lost outside old actual land')
 need(v['cached_graphs_exact'],'A cached package/pad/figure/global-textblock field changed')
 need(v['source_vias_exact'] and v['via_count']==1739,'Complete1739 original typed vias changed')
 need(v['created_actual_source_native_both_directions_exact'],'Actual created shape differs from source-only requested fragment')
 need(v['source_external_polygons_bound_to_v2_exact'],'Source-only approved external polygons changed')
 return True
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--run',type=Path,required=True);ap.add_argument('--partition-review',type=Path);a=ap.parse_args();r=a.run
 rec=json.loads((r/'RUN_RECEIPT.json').read_text('utf-8-sig'))
 need(rec['status']=='PASS_SOURCE_ONLY_EXTERNAL_THERMAL_PHASE_ONLY' and rec['public_unchanged'],'Native owned job incomplete or public modified')
 need(rec['source_sha256_before']==rec['source_sha256_after'] and rec['candidate_input_sha256_before']==rec['candidate_input_sha256_after'],'Protected source/partial changed')
 need((r/'SOURCE25_EXTERNAL_THERMAL_RESTORE_COMPLETE.txt').is_file(),'Missing native phase complete marker')
 pre=read_native(r/'ALL25_EXTERNAL_THERMAL_PREFLIGHT.ilist');post=read_native(r/'ALL25_POST_SOURCE_EXTERNAL_CU_COVERAGE.ilist');created=read_native(r/'CREATED_EXTERNAL_THERMAL_SHAPES.ilist')
 need(len(pre)==25 and len(post)==25 and len(created)==21,'Complete native raw ledgers missing')
 polys={}
 for line in (r/'EXTERNAL_THERMAL_CU_NATIVE_POLYGONS.jsonl').read_text('utf-8').splitlines():
  v=json.loads(line,parse_float=Decimal);polys.setdefault((v['key'],v['role']),[]).extend(v['polys'])
 approved={}
 for line in (M/'public0010_source25_owner_probe_run13_v2/SOURCE25_TARGET_ACTUAL_POLYGONS.jsonl').read_text('utf-8').splitlines():
  v=json.loads(line,parse_float=Decimal)
  if v['role']=='EXACT_MISSING_THERMAL_CU_OUTSIDE_DETACHED_OLD_ACTUAL_PAD':approved[v['key']]=v['polys']
 def zero(role,keys):
  return all((i,role) in polys and not polys[i,role] for i in keys)
 before_cache=(r/'BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist').read_text('utf-8').splitlines()
 after_cache=(r/'AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist').read_text('utf-8').splitlines()
 source_vias=(r/'SOURCE_ALL1739_TYPED_VIAS.ilist').read_text('utf-8').splitlines()
 after_vias=(r/'AFTER_ALL1739_TYPED_VIAS.ilist').read_text('utf-8').splitlines()
 proof=dict(source_sha=rec['source_sha256_before'],partial_sha=rec['candidate_input_sha256_before'],pre_keys=[int(x[0]) for x in pre],approved_external_keys=[int(x[0]) for x in pre if x[5][0]>0],created_keys=sorted(int(x[0]) for x in created),foreign_before_zero=zero('PREFLIGHT_OTHER_NET_ACTUAL_CU_INTERSECTION',range(1,26)),foreign_after_zero=zero('AFTER_CREATED_FRAGMENT_OTHER_NET_ACTUAL_CU_INTERSECTION',KEYS),outside_old_pad_after_zero=zero('AFTER_SOURCE_CU_MISSING_OUTSIDE_OLD_ACTUAL_PAD',range(1,26)) and all(x[3][0]==0 and x[3][1]==0 for x in post),cached_graphs_exact=sorted(before_cache)==sorted(after_cache) and len(before_cache)>0,source_vias_exact=source_vias==after_vias,via_count=len(source_vias),created_actual_source_native_both_directions_exact=all(x[-1]=='ANDNOT_BOTH_DIRECTIONS_EMPTY' and (int(x[0]),'CREATED_EXTERNAL_SOURCE_THERMAL_ACTUAL_CU') in polys for x in created),source_external_polygons_bound_to_v2_exact=all(polys.get((i,'SOURCE_MISSING_OUTSIDE_OLD_ACTUAL_REGULAR_PAD'))==approved[i] for i in range(1,26)))
 validate(proof)
 controls=[]
 for key,value in [('source_sha','BAD'),('pre_keys',list(range(1,25))),('approved_external_keys',KEYS+[3]),('created_keys',KEYS[:-1]),('foreign_before_zero',False),('foreign_after_zero',False),('outside_old_pad_after_zero',False),('cached_graphs_exact',False),('source_vias_exact',False),('via_count',1738),('created_actual_source_native_both_directions_exact',False),('source_external_polygons_bound_to_v2_exact',False)]:
  v=deepcopy(proof);v[key]=value
  try:validate(v)
  except ValueError:controls.append(dict(mutation=key,result='REJECTED'))
  else:raise ValueError('Negative control not rejected '+key)
 partition=None
 if a.partition_review:
  partition=json.loads(a.partition_review.read_text('utf-8-sig'))
  need(partition['status']=='PASS_FULL2698_TYPED_PHYSICAL_CONNECTION_PARTITION_EXACT','Fresh full915 partition gate failed')
  need(partition['candidate_board_sha256']==rec['candidate_sha256'],'Fresh915 candidate SHA mismatch')
  need(partition['partitions']['source_groups']==partition['partitions']['candidate_groups']==915 and partition['partitions']['pass_exact'],'Exact member-wise915 gate required')
 report=dict(status='PASS_BOUNDED_EXTERNAL_SOURCE_THERMAL_PHASE_AND_FRESH915_EXACT' if partition else 'PASS_BOUNDED_EXTERNAL_SOURCE_THERMAL_PHASE_FRESH915_AND_CFX_STILL_REQUIRED',source_board_sha256=proof['source_sha'],partial_board_sha256=proof['partial_sha'],candidate=rec['candidate'],candidate_sha256=rec['candidate_sha256'],approved_source_only_external_fragments=21,source_strokes_evaluated=25,source_only_external_mm2=str(sum(x[5][1] for x in pre)),old_land_internal_canonical_changes_deliberately_not_restored=True,proof=proof,negative_controls=controls,full915_review=str(a.partition_review) if a.partition_review else None,full915_review_sha256=sha(a.partition_review) if a.partition_review else None,CFX_and_final_publication_are_separate_required_gates=True,evidence=[dict(path=str(p),sha256=sha(p)) for p in [r/'RUN_RECEIPT.json',r/'ALL25_EXTERNAL_THERMAL_PREFLIGHT.ilist',r/'ALL25_POST_SOURCE_EXTERNAL_CU_COVERAGE.ilist',r/'CREATED_EXTERNAL_THERMAL_SHAPES.ilist',r/'EXTERNAL_THERMAL_CU_NATIVE_POLYGONS.jsonl',r/'BEFORE_ALL_CACHED_DEFINITION_GRAPHS.ilist',r/'AFTER_ALL_CACHED_DEFINITION_GRAPHS.ilist']])
 out=r/'EXTERNAL_SOURCE_THERMAL_BOUNDED_REVIEW.json';out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(dict(report=str(out),sha256=sha(out),status=report['status'],negative_controls=len(controls)),indent=2))
if __name__=='__main__':main()
