"""Complete actual59 cache gate:51 retained source-exact +8 coldpublic exact.
External manufacturing definitions are reused only through current SHA-bound
complete native PAD XML reports; this script never guesses equivalent pads.
"""
from pathlib import Path
import argparse,csv,hashlib,json,sys,collections
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');G=R.parent/'cadence_geometry_merge_20261025'
sys.path.insert(0,str(G));import compare_native_geometry as n
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def js(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def manifest(p):
 with (p/'manifest.tsv').open(encoding='utf-8-sig',newline='') as f:return {r['name'].casefold():r for r in csv.DictReader(f,delimiter='\t')}
class Context(n.Native):
 def __init__(self,p):
  super().__init__(p)
  for attrs,props in self.nodes.values():
   if 'textBlock' in attrs:
    block=self.textblocks[str(attrs['textBlock'])]
    key='FULL_BLOCK_'+n.digest([(k,self.value(v,k)) for k,v in sorted(block.items()) if k not in ('name','userDefined')])
    self.textblocks[key]=block;attrs['textBlock']=key
ap=argparse.ArgumentParser();ap.add_argument('--actual-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();assert not a.out.exists()
A=manifest(a.actual_dir);S=manifest(R/'w/final_alt13');C=M/'project8_mils2_native13'
assert len(A)==59 and len(S)==81
launch=js(a.actual_dir/'launch_report.json');board=Path(launch['source'])
assert launch['exit_code']==0 and launch['input_unchanged'] and launch['source_sha256_before']==launch['source_sha256_after']==sha(board)
assert 'ALL1066_PACKAGE_SYMBOL_DEFINITION_COMPLETE_EXPLICIT_UNFILTERED' in (a.actual_dir/'ALL81_FINAL_FRESH_COMPLETE.txt').read_text()
cp=js(C/'report.json');assert cp['all_assets_passed'] and cp['public_files_unchanged'] and cp['outputs']==8
public={r['stem'].casefold():r for r in js(C/'manifest.json')}
assert set(public)==A.keys()-S.keys() and len(public)==8
for row in public.values():
 assert sha(row['path'])==row['source_sha256']==row['source_sha256_after']
 assert row['audit_context_units']=='mils' and row['audit_context_accuracy']==2
 assert row['audit_context_copper_layers']==['TOP','L2','L3','BOTTOM']
# Prior complete manufacturing records are not regenerated; bind current bytes
# and the XML evidence bytes anew. Records whose public file changed are ignored.
bindings={};binding_inputs={}
for root in ('project81_exact_targets_review13','project81_current_targets_review13','global_canonical_targets_review13','global_nonpassive_native_review13','global_suffix_native_review_v3','nonpassive_exact_targets_review13','global_nonpassive_increment_review13'):
 p=M/root/'FULL_PAD_XML_BINDING.json';report=js(p);assert not report['errors'];binding_inputs[str(p)]=sha(p)
 for record in report['records']:
  f=Path(record['path'])
  if not f.is_file() or sha(f)!=record['current_sha256']:continue
  xp=Path(record['native_xml_path']);assert sha(xp)==record['native_xml_sha256']
  name=record['native_loaded_pad_name'].casefold();sig=record['all_classified_manufacturing_fields_signature']
  if name in bindings:assert bindings[name]['signature']==sig,(name,'conflicting current fullPAD binding')
  bindings[name]={'signature':sig,'record':record,'binding_report':str(p)}
native={};allpads=set();newpads=set()
for key,row in A.items():
 ob=Context(row['file']);native['actual',key]=ob
 for attrs,props in ob.nodes.values():
  if attrs.get('objType')=='padstack':allpads.add(str(attrs['name']).casefold())
 if key in public:
  pub=Context(public[key]['audit_output']);native['public',key]=pub
  for attrs,props in pub.nodes.values():
   if attrs.get('objType')=='padstack':newpads.add(str(attrs['name']).casefold())
 else:native['source',key]=Context(S[key]['file'])
assert newpads<=bindings.keys(),('Missing current full manufacturing XML binding',sorted(newpads-bindings.keys()))
n.PAD_PUBLIC={p:(bindings[p]['signature'] if p in bindings else 'SAME_SOURCE_REFERENCE_ONLY:'+p) for p in allpads|newpads}
prior_path=R/'w/pcb_migration/FINAL_ALT_PUBLIC_CACHE_REVIEW.json';prior=js(prior_path)
priorrows={r['target'].casefold():r for r in prior['results']}
results=[];private=[]
for key,row in A.items():
 actual=native['actual',key];x=actual.signature()
 for attrs,props in actual.nodes.values():
  if props==n.NIL:continue
  for prop in props:
   if str(prop[0])=='LIBRARY_PATH':
    val=str(prop[1]).lower().replace('\\','/');
    if not val.startswith('d:/001diy/005lib/'):private.append({'target':key,'path':val})
 if key in public:
  p=public[key];y=native['public',key].signature();exact=x['signature']==y['signature'] and not x['issues'] and not y['issues']
  results.append({'name':key,'category':'NEW_TARGET_FULL_COLD_PUBLIC_NATIVE_EXACT','exact':exact,'actual':x,'reference':y,
   'actual_raw':row['file'],'actual_raw_sha256':sha(row['file']),'public_raw':p['audit_output'],'public_raw_sha256':sha(p['audit_output']),'public_psm':p['path'],'public_psm_sha256':sha(p['path'])})
 else:
  y=native['source',key].signature();exact=x['signature']==y['signature'] and not x['issues'] and not y['issues']
  pr=priorrows[key];file_unchanged=Path(pr['public_psm']).is_file() and sha(pr['public_psm'])==pr['public_psm_sha256']
  results.append({'name':key,'category':'RETAINED_ACTUAL_SOURCE_NATIVE_EXACT','exact':exact,'actual':x,'reference':y,
   'actual_raw':row['file'],'actual_raw_sha256':sha(row['file']),'source_raw':S[key]['file'],'source_raw_sha256':sha(S[key]['file']),
   'prior_public_compatibility_psm_unchanged':file_unchanged,'prior_public_full_exact':pr['full_public_native_exact'],'prior_inherited_missing_bound_exception':pr['inherited_bound_exception'],
   'public_psm':pr['public_psm'],'public_psm_sha256':sha(pr['public_psm']) if Path(pr['public_psm']).is_file() else None})
good=all(r['exact'] for r in results) and not private and all(r.get('prior_public_compatibility_psm_unchanged',True) for r in results)
report={'status':'PASS_COMPLETE59_CACHE_51SOURCE_EXACT_8COLDPUBLIC_EXACT' if good else 'FAIL_COMPLETE59_CACHE_REVIEW',
 'actual_board':str(board),'actual_board_sha256':sha(board),'definitions':59,'retained51_source_exact':sum(r['exact'] for r in results if r['category'].startswith('RETAINED')),'new8_full_public_exact':sum(r['exact'] for r in results if r['category'].startswith('NEW')),
 'new8_current_SHA_complete_manufacturing_PAD_XML_bindings':{p:bindings[p] for p in sorted(newpads)},'nonpublic_LIBRARY_PATH':private,
 'scope':'All59 actual embedded definitions:51 retained full native physical graphs match49AF source;8 new names match independently coldloaded current public PSMs in mainmils2/four-copper-layer context. Full textblock content, no geometric tolerance and no omitted internal layer. New8 pad manufacturing fields reuse complete prior nativeXML only with current exact PAD+XML SHA. Existing inherited absence of PLACE_BOUND remains explicitly bounded by prior source/public proof and unchanged publicPSM bytes. Mandatory PCB cache remains embedded; connectivity, routingCu and rules are separate gates.',
 'results':results,'inputs':{str(p):sha(p) for p in (a.actual_dir/'manifest.tsv',R/'w/final_alt13/manifest.tsv',C/'manifest.json',C/'report.json',prior_path,Path(__file__))},'full_PAD_binding_report_sha256':binding_inputs}
a.out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('results','inputs','new8_current_SHA_complete_manufacturing_PAD_XML_bindings','full_PAD_binding_report_sha256')},indent=2));print('REPORT',a.out,'SHA256',sha(a.out))
