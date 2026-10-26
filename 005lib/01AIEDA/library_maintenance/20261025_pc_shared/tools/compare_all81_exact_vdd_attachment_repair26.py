"""Bounded ALL81 84-ref/246 pin coordinate inverse; all6521 typed pads retained."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
s=importlib.util.spec_from_file_location('complete_typed_partition_tools',R/'tools/compare_copper_pin_partitions.py');P=importlib.util.module_from_spec(s);s.loader.exec_module(P)
need=P.need;sha=P.sha;load=P.load
SOURCE='49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063'
PLAN_SHA='DC6AF5A611D727661DE53FF2FEC2EABFCEB0CDF05AB3D65003DE783A2EC9750A'
def exact_vdd_context(path,before,after):
 need(sha(path)==PLAN_SHA,'Frozen exact VDD repair plan changed');plan=load(path)
 need(plan['schema']=='MAIN13_EXACT_VDD10_1_EXISTING_ATTACHMENT_REPAIR_V1' and plan['source_board_sha256']==before and plan['candidate_board_sha256']==after,'VDD repair not bound to these exact native boards')
 ev=plan['artifacts']
 for v in ev.values():need(sha(v['path'])==v['sha256'],'Exact original-native/PST repair evidence changed')
 chain=load(ev['source49AF_to_touch_source06B8_full_typed_chain']['path']);need(chain['status']=='PASS_FULL6521_SOT34_COORDINATE_INVERSE_TYPED_PARTITIONS' and chain['source_board_sha256']==before and chain['candidate_board_sha256']==plan['touch_source_board_sha256'] and chain['complete_copper_pin_partitions_equal'] and chain['all_stored_netstatus_equal'],'Touch-source cannot bind original same native topology')
 spec=importlib.util.spec_from_file_location('vdd_full_source_readonly_binding',R/'tools/compare_public_noop_full.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
 native=Path(ev['native_touch_launch']['path']).parent;F.bind(native,plan['touch_source_board_sha256'],'VDD_ORIGINAL_TOUCH_COMPLETE.txt')
 text=Path(ev['native_touch_complete']['path']).read_text();need(text.splitlines()==['SOURCE_PIN3_LOGICAL_NET=VDD10_1','SOURCE_PIN3_TO8MIL_CU_POSITIVE_AND','SOURCE8MIL_TO_OTHER15MIL_CU_POSITIVE_AND','READ_ONLY_NO_CREATE_NO_SAVE'],'Original native Cu-touch proof did not complete exact same-net scope')
 polys=[json.loads(line) for line in Path(ev['native_touch_polygons']['path']).read_text().splitlines()];sides={r['side']:r for r in polys};expected={'ORIGINAL_ACTUAL_TOP_PIN_CU','ORIGINAL_8MIL_PATH_CU','ORIGINAL_OTHER_15MIL_PATH_CU','SOURCE_PIN_AND_SHORT_PATH_POSITIVE_TOUCH','ORIGINAL_TWO_PATHS_ALREADY_POSITIVE_CU_TOUCH'};need(len(polys)==5 and set(sides)==expected,'Complete exact original Cu/positive Boolean intersections missing')
 for r in polys:need(isinstance(r['poly']['area'],(int,float)) and r['poly']['area']>0 and len(r['poly']['outer'])>=3 and r['poly']['holes']==[],'Original source positive-area Cu proof invalid')
 need(abs(sides['SOURCE_PIN_AND_SHORT_PATH_POSITIVE_TOUCH']['poly']['area']-145.1327412287)<1e-9 and abs(sides['ORIGINAL_TWO_PATHS_ALREADY_POSITIVE_CU_TOUCH']['poly']['area']-69.6947164630)<1e-9,'Frozen original native intersection payload differs')
 spec=importlib.util.spec_from_file_location('vdd_full_pst_model',R/'tools/verify_library13_pst.py');Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q)
 logical={tuple(plan['source_isolated_endpoint'])}|{tuple(r) for r in plan['source_other_10_endpoints']};need(len(logical)==11,'Exact VDD logical eleven-node set changed')
 for key,hashkey in [('source_pstxnet','source_pstxnet_sha256'),('candidate_pstxnet','candidate_pstxnet_sha256')]:
  p=Path(ev[key]['path']);need(sha(p)==plan[hashkey],'Frozen physical PST changed');bundle=Q.P.load_bundle(p.parent);actual={tuple(k) for k,v in bundle['pinmap'].items() if v=='VDD10_1'};need(actual==logical,'Original or final PST supply logical membership changed')
 proof=load(ev['full_PST_inverse_proof']['path']);need(proof['status']=='PASS_COMPLETE_PST_FP_AND_SOURCE_PATH_ONLY' and len(proof['negative_controls'])==7,'Original/full final PST inverse proof missing')
 return plan

def exact_vdd_expected(source,netstatus,plan):
 logical={tuple(plan['source_isolated_endpoint'])}|{tuple(r) for r in plan['source_other_10_endpoints']}
 groups=[g for g,n in source.items() if any(e[-1]==('STRING','VDD10_1') for e,k in g)]
 need(sum(source.values())==2020 and len(groups)==2 and all(source[g]==1 for g in groups),'Original exact two VDD islands changed')
 need(all(all(e[-1]==('STRING','VDD10_1') and k==1 and e[0][0]==e[1][0]=='STRING' for e,k in g) for g in groups),'Original island includes other net/typed/mechanical/duplicate pad')
 singles=[g for g in groups if len(g)==1];large=[g for g in groups if len(g)==10];need(len(singles)==len(large)==1,'Expected exact1+10 source VDD groups missing')
 need((singles[0][0][0][0][1],singles[0][0][0][1][1])==('U5','3'),'Source isolated power pin changed')
 members=Counter();[members.update(dict(g)) for g in groups];need({(e[0][1],e[1][1]) for e in members}==logical and sum(members.values())==11,'Source native physical endpoints differ from exact source/final PST eleven nodes')
 merged=tuple(sorted(members.items()));expected=source.copy()
 for g in groups:expected[g]-=1
 expected[merged]+=1;expected=+expected;need(sum(expected.values())==2019 and len(expected-source)==1 and sum((source-expected).values())==2,'Repair exceeds exact two→one VDD island operation')
 old=tuple((k,json.dumps(v) if k=='net' else v) for k,v in plan['source_stored_netstatus'].items());new=tuple((k,json.dumps(v) if k=='net' else v) for k,v in plan['expected_candidate_stored_netstatus'].items());need(netstatus[old]==1 and sum(netstatus.values())==1118,'Original exact stored VDD status changed');ns=netstatus.copy();ns[old]-=1;ns[new]+=1;ns=+ns
 return expected,ns,{'net':'VDD10_1','source_groups':groups,'expected_connected_full11_group':merged,'source_full_stored_record':plan['source_stored_netstatus'],'expected_full_stored_record':plan['expected_candidate_stored_netstatus'],'all_other2018_complete_groups_and1117_complete_netstatus_records_must_be_exact':True}

def bounded_controls(expected,status):
 rows=P.controls(expected)
 def reject(name,changed,goal):need(changed!=goal,'Finite repair negative accepted '+name);rows.append({'name':name,'status':'PASS_REJECTED'})
 v=next(g for g in expected if any(e[-1]==('STRING','VDD10_1') for e,k in g));single=next((e,k) for e,k in v if e[0][1]=='U5' and e[1][1]=='3');rest=Counter(dict(v));rest[single[0]]-=1;b=expected.copy();b[v]-=1;b[tuple(sorted((+rest).items()))]+=1;b[(single,)]+=1;reject('restore_original_isolated_U5_3_instead_of_authorized_supply_repair',+b,expected)
 b=status.copy();r=next(k for k in status if dict(k)['net']=='"VDD10_1"');q=dict(r);q['branch_count']='2';b[r]-=1;b[tuple(q.items())]+=1;reject('VDD_stored_branch_count_not_exact_expected1',+b,status)
 r=next(k for k in status if dict(k)['net']!='"VDD10_1"');q=dict(r);q['unconnected_stored']='WRONG';b=status.copy();b[r]-=1;b[tuple(q.items())]+=1;reject('unrelated_netstatus_field_changed',+b,status)
 return rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--repair-plan',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh output required');a.out.mkdir(parents=True);src=R/'w/final_alt13';report={'status':'FAIL'}
 original=R/'w/pcb_migration/EXPECTED_BOARD_PINS_V3.json';planned=M/'project81_expected_pins13/ALL81_EXPECTED_BOARD_PINS6521.json';changed=M/'project81_expected_pins13/ALL81_PIN_CHANGES.json'
 try:
  before=P.binding(src,SOURCE);after=P.binding(a.candidate);old,new,delta=load(original),load(planned),load(changed)
  need(sha(original)=='B4DFF9DE601EBB186954761BAC079FE44F6CB2FA10807CA78CDAA3CA121E0254' and sha(planned)=='D83EE798900B525603591307E438293FC347244408281C57D84CDF77F705FCEE' and sha(changed)=='E3BDB88A360A7259D8BB8C7A7356DB3925079E88AEC349FD6E59F129698C7EA6','Frozen ALL81 source/full-target/delta plan SHA differs')
  need(len(old)==len(new)==6521 and len(delta)==1066 and len({r['ref'] for r in delta})==84,'Full6521/84ref/1066mapped pads frozen cohort required')
  need(all((r['before']['ref'],r['before']['pin'],r['before']['native_net_type'],r['before']['net'],r['before']['isMech'],r['before']['isThrough'])==(r['after']['ref'],r['after']['pin'],r['after']['native_net_type'],r['after']['net'],r['after']['isMech'],r['after']['isThrough']) for r in delta),'ALL81 source electrical or mechanical identity changed in planned delta')
  moves=[r for r in delta if P.key(r['before'],True)!=P.key(r['after'],True)]
  need(len(moves)==246 and sum(bool(r['world_coordinate_changed']) for r in delta)==246,'Full ALL81 coordinate-move ledger is not exact246')
  expectedold=Counter(P.key(r,True) for r in old);expectednew=Counter(P.key(r,True) for r in new)
  olddelta=Counter(P.key(r['before'],True) for r in delta);newdelta=Counter(P.key(r['after'],True) for r in delta)
  need(expectedold-olddelta==expectednew-newdelta and sum(olddelta.values())==sum(newdelta.values())==1066,'Unlisted pin change outside frozen ALL81 84refs')
  need(expectedold>=olddelta and expectednew>=newdelta,'Delta rows do not bind complete pin cohort')
  aa=P.tab(src/'native_copper_pin_groups.tsv');bb=P.tab(a.candidate/'native_copper_pin_groups.tsv');sa=P.tab(src/'all_symbol_pins.tsv');sb=P.tab(a.candidate/'all_symbol_pins.tsv')
  ba=P.bound_symbol_rows(sa,aa);bc=P.bound_symbol_rows(sb,bb)
  need(Counter(P.symbol_identity(r,t) for r,t in ba)==expectedold,'Source49AF actual pins differ from its already-applied public13 V3 expected coordinates')
  need(Counter(P.symbol_identity(r,t) for r,t in bc)==expectednew,'Candidate ALL81 actual pins differ from full6521 exact coordinate/net plan')
  ca=Counter(P.identity(r) for r in aa);cb=Counter(P.identity(r) for r in bb);need(len(aa)==len(bb)==6521,'Pad multiplicity lost')
  need(Counter(P.symbol_copper_identity(r,t) for r,t in ba)==ca and Counter(P.symbol_copper_identity(r,t) for r,t in bc)==cb,'Typed physical ownership and actual BFS endpoints disagree')
  inverse={k:k for k in cb};sourceidentity={k:k for k in ca}
  for row in moves:
   oldr=dict(row['before']);newr=dict(row['after']);oldr['old_x']=oldr['expected_x'];oldr['old_y']=oldr['expected_y'];newr['old_x']=newr['expected_x'];newr['old_y']=newr['expected_y']
   x,y=P.copper_plan_identity(newr),P.copper_plan_identity(oldr);need(cb[x]==ca[y]==1,'ALL81 native endpoint inverse is not unique');inverse[x]=y
  need(Counter(inverse[P.identity(r)] for r in bb)==ca,'Actual complete typed endpoint multiset changed beyond exact246 planned ALL81 coordinates')
  x,y=P.partition(aa,sourceidentity),P.partition(bb,inverse);ns=P.tab(src/'stored_net_status.tsv');nt=P.tab(a.candidate/'stored_net_status.tsv');cs=Counter(tuple(v.items()) for v in ns);ct=Counter(tuple(v.items()) for v in nt)
  plan=exact_vdd_context(a.repair_plan,before,after);expected,expectedstatus,repair=exact_vdd_expected(x,cs,plan)
  report.update({'explicit_existing_same_net_attachment_repair':repair,'expected_repaired_partition_equal':expected==y,'expected_repaired_netstatus_equal':expectedstatus==ct,'frozen_repair_plan':{'path':str(a.repair_plan),'sha256':sha(a.repair_plan)},'all_original_PST_source_nodes_preserved':True,'native_original_positive_area_touch_proof_bound':True,'status_is_source_repair_not_original_partition_identity':True})
  report.update({'source_board_sha256':before,'candidate_board_sha256':after,'physical_pad_rows':6521,'planned_coordinate_inverse':246,'full_mapped_pad_rows':1066,'full_mapped_refs':84,'source_copper_groups':sum(x.values()),'candidate_copper_groups':sum(y.values()),'complete_copper_pin_partitions_equal':x==y,'partition_residual':P.diff(x,y),'all_stored_netstatus_equal':cs==ct,'netstatus_source_only_count':sum((cs-ct).values()),'netstatus_candidate_only_count':sum((ct-cs).values()),'full_source_pin_context_including_SC37_already_modified':True,'source_partition_sha256':hashlib.sha256(repr(sorted(x.items())).encode()).hexdigest().upper(),'candidate_partition_sha256':hashlib.sha256(repr(sorted(y.items())).encode()).hexdigest().upper(),'negative_controls':bounded_controls(expected,expectedstatus),'status':'PASS_FULL6521_ALL81_WITH_EXACT_ORIGINAL_VDD_ATTACHMENT_REPAIR' if expected==y and expectedstatus==ct else 'FAIL_ALL81_OUTSIDE_EXACT_APPROVED_VDD_REPAIR'})
 except Exception as ex:report['error']=str(ex)
 report['inputs']={str(p):sha(p) for d in [src,a.candidate] for p in [d/'launch_report.json',d/'all_symbol_pins.tsv',d/'native_copper_pin_groups.tsv',d/'stored_net_status.tsv']};report['frozen_complete_pin_plans']={str(p):sha(p) for p in [original,planned,changed]};report['script_sha256']=sha(__file__);report['scope']='Exact246 coordinate inverse plus only frozen source VDD10_1 native1+10 island→11 same-original-PST-node supply attachment repair. Original strict partition-identity FAIL is preserved. All other2018groups/1117netstatus and all6521typed endpoints remain exact. A native expected-pin ledger pass does not replace real GetConnect topology, route-end attachment and full actual copper constraints proof.'
 p=a.out/'ALL81_EXACT_VDD_REPAIR_TYPED_CONNECTIVITY_REVIEW.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:report.get(k) for k in ['status','error','source_copper_groups','candidate_copper_groups','netstatus_source_only_count','netstatus_candidate_only_count']}));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
