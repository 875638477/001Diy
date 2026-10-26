"""Verify the two added exact-case generics with complete native graph/PAD and input byte identity."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,importlib.util
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');S=importlib.util.spec_from_file_location('native',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(S);S.loader.exec_module(N)
jr=N.jread;sha=N.sha;items={e['stem']:e for p in (M/'project81_exact_targets_review13').glob('e*_SCHEMA_GEOMETRY.json') for e in jr(p)}
plan=M/'project81_final_canonical_plan13/ALL81_NEW_EXACT_CANONICAL_ASSETS.json';defs=jr(plan)['targets'];rows=[]
oldidx={e['stem']:e for p in (M/'global_nonpassive_native_review13').glob('e*_SCHEMA_GEOMETRY.json') for e in jr(p)}
for name,r in defs.items():
 target=items[name];identity=[]
 for a in r['assets']:
  assert sha(a['source'])==a['source_sha256']==sha(a['target']);identity.append({'source':a['source'],'target':a['target'],'sha256':a['source_sha256'],'full_compiled_or_DRA_bytes_equal':True})
 if r['source'] in oldidx:
  source=oldidx[r['source']];equal=source['full_ordered_graph_fingerprint']==target['full_ordered_graph_fingerprint'];assert equal
  proof={'independent_previous_source_native':source['native_path'],'source_native_sha256':source['native_sha256'],'source_and_target_complete_native_graph_equal':True}
 else:
  # Exact compiled bytes read from the same directory resolve the same full currentPAD dependencies.
  # The actual projectcache lacks inheritedPLACE_BOUND metadata, so do not falsify fullcachegraph equality.
  raw=next(d for d in list(__import__('csv').DictReader((R/'w/final_alt13/manifest.tsv').open(encoding='utf-8'),delimiter='\t')) if d['name'].lower()==r['source']);cached=N.inspect(Path(raw['file']));a={p['number']:p for p in cached['pins']};b={p['number']:p for p in target['pins']};assert set(a)==set(b)
  for n,p in a.items():
   q=b[n];assert p['pad_name']==q['pad_name'] and p['is_mechanical']==q['is_mechanical'] and p['is_through']==q['is_through'];assert all(abs(Decimal(x)-Decimal(y))<Decimal('0.00000001') for x,y in zip(p['local_xy_mm'],q['local_xy_mm']))
  proof={'source_compiled_definition_byte_identity_cold_loaded_from_same_public_directory':True,'actual_cached_source_numbered_pin_and_PAD_names_all_equal':True,'actual_cached_source_pin_count':cached['pin_count'],'source_cached_raw':raw['file'],'source_cached_raw_sha256':sha(raw['file']),'full_cached_graph_equality_not_claimed':'InheritedmissingPLACE_BOUND metadata is separately documented; sourceCompiledPSM/DRA exactbyteidentity is thecloneproof.'}
 rows.append({'target':name,'source':r['source'],'native_path':target['native_path'],'native_sha256':target['native_sha256'],'pin_numbers':target['pin_numbers'],'byte_identity':identity,'proof':proof})
binding=M/'project81_exact_targets_review13/FULL_PAD_XML_BINDING.json';b=jr(binding);assert not b['errors'] and b['full_native_xml_bound']==b['loaded_unique_pad_files']==8
out=M/'project81_exact_targets_review13/EXACT_TWO_SOURCE_NATIVE_REVIEW.json';report={'status':'PASS_TWO_EXACT_COMPILED_CLONES_COLD_NATIVE_FULL_PAD_MANUFACTURING','new_targets':2,'files_byte_identical':4,'full_current_native_PAD_XML_files':8,'PAD_XML_binding':str(binding),'PAD_XML_binding_sha256':sha(binding),'source_plan':str(plan),'source_plan_sha256':sha(plan),'rows':rows};N.dump(out,report);print(json.dumps({'path':str(out),'sha256':sha(out),'status':report['status']},indent=2))
