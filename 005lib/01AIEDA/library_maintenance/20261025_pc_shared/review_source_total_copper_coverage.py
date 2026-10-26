"""Review a complete V11 native source-total copper run, without CAD access."""
import argparse,collections,csv,hashlib,json
from decimal import Decimal
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def read(p):return Path(p).read_text(encoding='utf-8-sig')
def js(p):return json.loads(read(p),parse_float=Decimal)
def jsonl(p):return [json.loads(x,parse_float=Decimal) for x in read(p).splitlines()]
def tsv(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def safe(v):
 if isinstance(v,Decimal):return str(v)
 if isinstance(v,Path):return str(v)
 if isinstance(v,dict):return {str(k):safe(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [safe(x) for x in v]
 return v
def canonical(p):return json.dumps(safe(p),sort_keys=True,separators=(',',':'))
def box_union(ps):
 if not ps:return None
 return [[min(p['bbox'][0][0] for p in ps),min(p['bbox'][0][1] for p in ps)],[max(p['bbox'][1][0] for p in ps),max(p['bbox'][1][1] for p in ps)]]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native-dir',type=Path,required=True);ap.add_argument('--frozen-v10-dir',type=Path,required=True);ap.add_argument('--plan-receipt',type=Path,required=True);ap.add_argument('--final-board',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();assert not a.out.exists();n=a.native_dir;v=a.frozen_v10_dir
 receipt=js(a.plan_receipt);assert sha(receipt['plan'])==receipt['plan_sha256'];assert all(sha(p)==s for p,s in receipt['inputs'].items());assert receipt['pieces']==150 and receipt['normal_margin_windows']==6
 complete=read(n/'SOURCE_TOTAL_CU_COVERAGE_COMPLETE.txt');assert complete.startswith('NATIVE_SOURCE_TOTAL_CU_COVERAGE_V11_COMPLETE');counts={l.split('=',1)[0]:int(l.split('=',1)[1]) for l in complete.splitlines() if '=' in l};assert counts['ADDED_INPUT_PIECES']==150
 steps=read(n/'STEP.txt').splitlines();assert 'SOURCE_V11_150_PRELOAD_COMPLETE_TOP_LEVEL_OPEN_TARGET' in steps and 'ENTER_V11_TARGET_AFTER_TOP_LEVEL_OPEN' in steps and steps[-1]=='V11_ALL_COMPLETE';assert sum(s.startswith('V11_KEY_COMPLETE ') for s in steps)==11
 assert any(s.startswith('SOURCE150_INDEX_COMPLETE objects=') and 'pins=6521 vias=4541' in s for s in steps)
 assert any(s.startswith('TARGET150_INDEX_COMPLETE objects=') and 'pins=6521 vias=4541' in s for s in steps)
 launch=js(n/'launch_report.json');final_hash=sha(a.final_board);assert launch['input_unchanged'] and launch['source_sha256_before']==launch['source_sha256_after'];assert sha(n/'COMPARE_COPY.brd')==final_hash
 oldlaunch=js(v/'launch_report.json');assert oldlaunch['input_unchanged'] and oldlaunch['source_sha256_before']==launch['source_sha256_before'] and oldlaunch['compare_source_sha256_before']==oldlaunch['compare_source_sha256_after']==final_hash
 assert launch['compare_source_sha256_before']==launch['compare_source_sha256_after']==final_hash
 frozen_material=[x for x in jsonl(v/'actual_material_differences.jsonl') if not x['key'].startswith('PC184.2')]
 current_material=jsonl(n/'v11_actual_material_differences.jsonl')
 assert collections.Counter(canonical(x) for x in frozen_material)==collections.Counter(canonical(x) for x in current_material),'Full native material arc/holes differs from V10'
 frozen_added=[x for x in frozen_material if x['side']=='ACTUAL_SHAPE_COPPER_ADDED'];assert len(frozen_added)==150
 current_added=jsonl(n/'all150_added_native.jsonl');assert len(current_added)==150
 for i,(old,new) in enumerate(zip(frozen_added,current_added),1):
  assert new['key']==f"PIECE{i}|{old['key']}" and new['side']=='ACTUAL_ADDED_INPUT'
  assert canonical(old['poly'])==canonical(new['poly']),'Full frozen original added polygon changed'
 outside=jsonl(n/'added_outside_source_total_cu.jsonl');assert len(outside)==counts['OUTSIDE_SOURCE_SAME_NET_POLYS'];coverage=tsv(n/'added_source_total_coverage.tsv');assert len(coverage)==150 and [int(x['piece']) for x in coverage]==list(range(1,151))
 out_by=collections.defaultdict(list)
 for x in outside:
  assert x['side']=='ADDED_OUTSIDE_SOURCE_SAME_NET_TOTAL_CU';out_by[x['key']].append(x['poly'])
 ledger=[]
 for i,(old,r) in enumerate(zip(frozen_added,coverage),1):
  key=f"PIECE{i}|{old['key']}";ps=out_by[key];assert r['key']==old['key'] and int(r['outside_polys'])==len(ps)
  ledger.append(dict(piece=i,key=old['key'],input_native_area_mil2=old['poly']['area'],input_bbox=old['poly']['bbox'],source_nearby_actual_polygon_count=int(r['source_candidate_polys']),outside_source_total_polygons=len(ps),outside_source_total_native_area_mil2=sum((p['area'] for p in ps),Decimal(0)),outside_source_total_bbox=box_union(ps),outside_pieces=[dict(area=p['area'],bbox=p['bbox'],outer_vertices=len(p['outer']),holes=len(p['holes'])) for p in ps]))
 oldm=tsv(v/'margin_validation_methods.tsv');oldc=tsv(v/'cross_net_checks.tsv');oldcross=jsonl(v/'cross_net_intersections.jsonl');cursor=0;normal_contacts=[];normal_ids=[]
 for i,(m,c) in enumerate(zip(oldm,oldc),1):
  direct=int(c['direct_intersections']);margin=int(c['margin_intersections']);segment=oldcross[cursor:cursor+direct+margin];cursor+=direct+margin
  if m['method']=='NATIVE_EXPAND_0D01MIL' and margin:
   assert direct==0;normal_ids.append(i);normal_contacts.extend(dict(key=f'SOURCE6|{i}',poly=x['poly']) for x in segment)
 assert cursor==len(oldcross) and len(normal_ids)==6
 regression=jsonl(n/'six_margin_contact_regression.jsonl');actual_normal=[dict(key=x['key'],poly=x['poly']) for x in regression if x['side']=='TARGET_0D01_MARGIN_CONTACTS']
 assert collections.Counter(canonical(x) for x in normal_contacts)==collections.Counter(canonical(x) for x in actual_normal),'Target6 normal contacts differ from frozenV10'
 reg=tsv(n/'six_margin_contact_regression.tsv');source6=tsv(n/'source6_summary.tsv');objects=tsv(n/'source6_object_identity.tsv');assert len(reg)==len(source6)==6 and [int(r['piece']) for r in reg]==normal_ids
 assert sum(int(x['new_margin_contact_polys']) for x in reg)==counts['SIX_NORMAL_MARGIN_NEW_CONTACT_POLYS']
 source6geo=jsonl(n/'source6_actual_and_margin_geometry.jsonl')
 native_source_contacts=collections.Counter((x['key'],x['side']) for x in source6geo)
 for o in objects:
  key=f"SOURCE6|{o['piece']}|OBJECT{o['object_index']}"
  assert int(o['direct_intersections'])==native_source_contacts[(key,'SOURCE_ACTUAL_INTERSECTS_OTHER_NET')]
  assert int(o['margin_intersections'])==native_source_contacts[(key,'SOURCE_MARGIN_INTERSECTS_OTHER_NET')]
 full_covered=not outside
 status='PASS_ALL150_GENERATED_COPPER_ADDITIONS_WITHIN_ORIGINAL_SAME_NET_TOTAL_CU' if full_covered else 'BOUNDED_ADDED_COPPER_REMAINS_OUTSIDE_ORIGINAL_SAME_NET_TOTAL_CU'
 files=['SOURCE_TOTAL_CU_COVERAGE_COMPLETE.txt','STEP.txt','launch_report.json','all150_added_native.jsonl','added_outside_source_total_cu.jsonl','added_source_total_coverage.tsv','source6_summary.tsv','source6_object_identity.tsv','source6_actual_and_margin_geometry.jsonl','six_margin_contact_regression.tsv','six_margin_contact_regression.jsonl','v11_actual_material_differences.jsonl','v11_actual_material_summary.tsv']
 report=dict(status=status,scope='Only the150 native added generated-shape material fragments are compared with original actual same-net total copper. Full native ANDNOT operands are original actual pads/vias/whole paths/shapes. Bboxes select candidate objects and never accept geometry. This is not a claim that removed copper or approved footprint-pad changes are globally equal.',source_board_sha256=launch['source_sha256_before'],candidate_board=dict(path=a.final_board,sha256=final_hash),all150_full_native_arc_and_holes_exact_to_frozen_v10=True,full11_native_material_differences_exact_to_frozen_v10=True,all150_inside_original_actual_same_net_total_copper=full_covered,outside_source_total_copper_polygons=len(outside),outside_source_total_native_area_mil2=sum((x['poly']['area'] for x in outside),Decimal(0)),outside_source_total_native_area_mm2=sum((x['poly']['area'] for x in outside),Decimal(0))*Decimal('.00064516'),pc184_source_old_hole_total_copper_outside=counts['PC184_SOURCE_OLD_HOLE_TOTAL_CU_OUTSIDE'],six_original_normal_margin_windows=normal_ids,six_source_native_probe=source6,six_actual_other_net_objects=[x for x in objects if int(x['direct_intersections']) or int(x['margin_intersections'])],six_margin_regression=reg,six_new_margin_contact_polygons=counts['SIX_NORMAL_MARGIN_NEW_CONTACT_POLYS'],source_normal_margin_containment_failures=sum(int(x['source_guard_lost_input']) for x in reg),target_normal_margin_containment_failures=sum(int(x['target_guard_lost_input']) for x in reg),prior_v10_strict_additional_margin_gate='FAIL remains unchanged; not reclassified by this report',ledger=ledger,inputs={str(n/f):sha(n/f) for f in files},frozen_plan=dict(path=a.plan_receipt,sha256=sha(a.plan_receipt)))
 a.out.write_text(json.dumps(safe(report),indent=2),encoding='utf-8');print(json.dumps(safe({k:v for k,v in report.items() if k not in ('ledger','inputs','six_actual_other_net_objects','six_source_native_probe')}),indent=2))
if __name__=='__main__':main()
