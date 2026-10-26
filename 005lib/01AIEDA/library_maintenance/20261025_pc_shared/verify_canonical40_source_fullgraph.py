"""Full graph equality for independently cold-reopened canonical targets. No CAD."""
from pathlib import Path
import hashlib,importlib.util,json
M=Path(__file__).resolve().parent;S=importlib.util.spec_from_file_location('native',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(S);S.loader.exec_module(N)
jr=N.jread;sha=N.sha
P=M/'global_canonical_publish_v1/CANONICAL_ADDITIONS_ONLY_PLAN.json';plan=jr(P)
items={e['stem'].lower():e for p in (M/'global_canonical_targets_review13').glob('e*_SCHEMA_GEOMETRY.json') for e in jr(p)}
assert len(items)==40
rows=[]
for r in plan['targets']:
 p=Path(r['source_evidence'] if r['existing'] else r['source_native_path']);h=r['source_native_sha256'];assert sha(p)==h
 a=N.inspect(p);b=items[r['target']];same=a['full_ordered_graph_fingerprint']==b['full_ordered_graph_fingerprint']
 rows.append({'target':r['target'],'existing':r['existing'],'source_native':str(p),'source_native_sha256':h,'target_cold_native':b['native_path'],'target_cold_native_sha256':b['native_sha256'],'all_graph_fields_equal_except_exact_runtime_admin_and_selected_asset_name':same,'source_graph_fingerprint':a['full_ordered_graph_fingerprint'],'target_graph_fingerprint':b['full_ordered_graph_fingerprint'],'pin_numbers':b['pin_numbers'],'loaded_PAD_dependencies':b['actual_loaded_pad_files']})
for name,idx in [('sot23-3',939),('sop-8-150mil',938)]:
 p=M/f'global_suffix_native_v3/e{idx:05}/output/0000.sexp';a=N.inspect(p);b=items[name];rows.append({'target':name,'existing':True,'source_native':str(p),'source_native_sha256':sha(p),'target_cold_native':b['native_path'],'target_cold_native_sha256':b['native_sha256'],'all_graph_fields_equal_except_exact_runtime_admin_and_selected_asset_name':a['full_ordered_graph_fingerprint']==b['full_ordered_graph_fingerprint'],'source_graph_fingerprint':a['full_ordered_graph_fingerprint'],'target_graph_fingerprint':b['full_ordered_graph_fingerprint'],'pin_numbers':b['pin_numbers'],'loaded_PAD_dependencies':b['actual_loaded_pad_files']})
pad=M/'global_canonical_targets_review13/FULL_PAD_XML_BINDING.json';binding=jr(pad);assert binding['full_native_xml_bound']==binding['loaded_unique_pad_files']==31 and not binding['errors']
report={'status':'PASS_ALL40_COLD_TARGETS_COMPLETE_GRAPH_AND_FULL_PAD_MANUFACTURING' if all(r['all_graph_fields_equal_except_exact_runtime_admin_and_selected_asset_name'] for r in rows) else 'FAIL_TARGET_SOURCE_GRAPH_MISMATCH','canonical_targets':40,'new_targets':30,'existing_passive_targets':8,'existing_SOT_SOP_targets':2,'complete_current_PAD_XML_files':31,'full_PAD_XML_binding':str(pad),'full_PAD_XML_binding_sha256':sha(pad),'source_plan':str(P),'source_plan_sha256':sha(P),'rows':rows,'scope':'Source-to-new-target cloning/native integrity only. Ordinary variants may differ physically from selected standard; each migration records that difference. This is not old-reference closure or deletion approval.'}
out=M/'global_canonical_targets_review13/CANONICAL40_SOURCE_FULLGRAPH_REVIEW.json';N.dump(out,report);print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
