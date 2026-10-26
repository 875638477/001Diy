"""Offline exactsourcebyte and allnativegraph identity of foursemantic additions plus2canaries."""
from pathlib import Path
import json,hashlib,importlib.util
M=Path(__file__).resolve().parent;S=importlib.util.spec_from_file_location('native',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(S);S.loader.exec_module(N)
jr=N.jread;sha=N.sha
P=M/'nonpassive_additional_aliases13/NONPASSIVE_FOUR_EXACT_CANONICAL_ADDITIONS_PLAN.json';plan=jr(P);idx={e['stem']:e for p in (M/'nonpassive_exact_targets_review13').glob('e*_SCHEMA_GEOMETRY.json') for e in jr(p)};rows=[]
for r in plan['new_targets']:
 a=N.inspect(Path(r['source_native_path']));assert sha(r['source_native_path'])==r['source_native_sha256'];b=idx[r['target']]
 assert a['full_ordered_graph_fingerprint']==b['full_ordered_graph_fingerprint'],r['target']
 for f in r['pair']:assert sha(f['source'])==f['source_sha256']==sha(f['target'])
 rows.append({'target':r['target'],'source':r['generic_source'],'source_native':r['source_native_path'],'source_native_sha256':r['source_native_sha256'],'new_cold_native':b['native_path'],'new_cold_native_sha256':b['native_sha256'],'full_ordered_native_graph_exact':True,'PSM_and_DRA_full_bytes_exact':True,'pin_numbers':b['pin_numbers']})
for name,i in [('sop-8-150mil',938),('sot23-3',939)]:
 p=M/f'global_suffix_native_v3/e{i:05}/output/0000.sexp';a=N.inspect(p);b=idx[name];assert a['full_ordered_graph_fingerprint']==b['full_ordered_graph_fingerprint'];rows.append({'target':name,'existing_canary':True,'full_ordered_native_graph_exact':True,'source_native':str(p),'source_native_sha256':sha(p),'new_cold_native':b['native_path'],'new_cold_native_sha256':b['native_sha256'],'pin_numbers':b['pin_numbers']})
bp=M/'nonpassive_exact_targets_review13/FULL_PAD_XML_BINDING.json';p=jr(bp);assert not p['errors'] and p['loaded_unique_pad_files']==p['full_native_xml_bound']==7
out=M/'nonpassive_exact_targets_review13/FOUR_SEMANTIC_SOURCE_FULLGRAPH_REVIEW.json';report={'status':'PASS_FOUR_SEMANTIC_EXACTSOURCE_CLONES_AND_TWO_EXISTING_CANARIES_FULL_NATIVE_AND_PAD_XML','new_assets':8,'new_generic_targets':4,'existing_canaries':2,'actual_full_PAD_XML_files':7,'full_PAD_XML_binding':str(bp),'full_PAD_XML_binding_sha256':sha(bp),'source_plan':str(P),'source_plan_sha256':sha(P),'rows':rows,'scope':'Sourceclones preserve allgraphics/font/default fields and everyactualnumberedpad. No oldalias wasretired by this proof; referenceclosure still required.'};N.dump(out,report);print(json.dumps({'path':str(out),'sha256':sha(out),'status':report['status']},indent=2))
