"""Complete only four pending BRD source rows after exact public publication.
All other 44 source rows, active config hashes, canonical proof and parser hashes
remain byte-for-byte equal as JSON values to the already reviewed manifest.
"""
from pathlib import Path
import argparse,copy,hashlib,json
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
PUBLIC=Path(r'D:\001DIY\005lib\01brdlib')
NAMES={'00012.brd','0010.brd','006.brd','008.brd'}
BASE_GUARD_SHA='F9D19CC95DCEA9686967EF7CF954EE7E6858225E7F9C949A203C340E6A153D88'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def norm(p):return str(Path(p).resolve()).casefold()
def art(p):return {'path':str(Path(p)),'sha256':sha(p)}
def need(v,s):
 if not v:raise ValueError(s)
def main():
 p=argparse.ArgumentParser();p.add_argument('--base-manifest',type=Path,required=True);p.add_argument('--base-manifest-sha256',required=True);p.add_argument('--new-guard',type=Path,required=True);p.add_argument('--new-guard-sha256',required=True);p.add_argument('--inventory-map',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 need(not a.out.exists(),'Fresh final completion directory required');need(sha(a.base_manifest)==a.base_manifest_sha256.upper(),'Frozen base manifest changed');need(sha(a.new_guard)==a.new_guard_sha256.upper(),'Frozen four-BRD new guard changed')
 base=load(a.base_manifest);old=load(base['public_guard']['path']);new=load(a.new_guard)
 need(base['schema']=='FINAL_NATIVE_REFERENCE_SOURCES_V1' and base['public_guard']['sha256']==sha(base['public_guard']['path'])==BASE_GUARD_SHA,'Only reviewed post13OLB base allowed')
 need(new['status']=='EXPECTED_PUBLIC_BYTES_BY_EXPLICIT_FOUR_BRD_REPLACEMENT' and new['source_guard']['sha256']==BASE_GUARD_SHA and norm(new['source_guard']['path'])==norm(base['public_guard']['path']),'Final public guard is not exact four-BRD successor')
 before={norm(v['path']):v for v in old['files']};after={norm(v['path']):v for v in new['files']};need(set(before)==set(after),'Final public file coverage changed')
 rows=new['explicit_replacements'];need(len(rows)==4 and {Path(v['public']).name.casefold() for v in rows}==NAMES,'Wrong four native public replacements');bypublic={norm(v['public']):v for v in rows}
 for key,b in before.items():
  n=after[key]
  if key not in bypublic:need(n==b,'Unrelated public file metadata changed')
  else:
   r=bypublic[key];need(Path(r['public']).resolve().parent==PUBLIC.resolve(),'Public BRD root escape');need(b['sha256']==r['old_sha256'] and n['sha256']==r['new_sha256']==sha(r['public'])==sha(r['candidate']) and n['bytes']==r['new_bytes'],'Published/candidate/guard BRD bytes disagree')
   need({k:v for k,v in n.items() if k not in {'bytes','sha256'}}=={k:v for k,v in b.items() if k not in {'bytes','sha256'}},'Unrelated BRD guard metadata changed')
   for e in r['native_proofs']:need(sha(e['path'])==e['sha256'] and load(e['path'])['status']==e['required_status'] and e['required_status'].startswith('PASS'),'Final native semantic proof not bound')
 receipt=a.new_guard.parent/'PUBLISH_RECEIPT.json';pr=load(receipt);need(pr['status']=='PASS_FOUR_PUBLIC_BRD_ATOMIC_REPLACEMENTS_OTHER_PUBLIC_FILES_UNCHANGED' and pr['public_files_replaced']==4 and pr['new_guard_sha256']==sha(a.new_guard) and norm(pr['new_guard'])==norm(a.new_guard),'Final four native publication receipt not exact')
 need(sha(pr['plan'])==pr['plan_sha256'] and load(pr['plan'])['replacements']==rows,'Published native proof plan changed')
 inv=load(a.inventory_map);need(set(inv)=={Path(n).stem for n in NAMES},'Exactly four final native inventory directories required')
 result=copy.deepcopy(base);changed=[]
 for i,row in enumerate(result['sources']):
  key=norm(row['public_path'])
  if key not in bypublic:continue
  need(row['kind']=='public_brd' and row['inventory_mode']=='PENDING_COMPLETE_NATIVE_REFERENCE_INVENTORY','Base is not the four reviewed pending public source rows');r=bypublic[key];entry=inv[Path(r['public']).stem];d=Path(entry['directory'] if isinstance(entry,dict) else entry)
  need(d.resolve().is_relative_to((M/'w').resolve()),'Final native inventory outside owned audit root');job=load(d/'launch_report.json');need(job['exit_code']==0 and job['input_unchanged'] and not job['write_candidate'] and '-readonly' in job['arguments'] and job['source_sha256_before']==job['source_sha256_after']==job['staged_sha256']==r['new_sha256'],'Final native inventory is not protected published bytes')
  need((d/'ALL_NATIVE_REFERENCE_INVENTORY_COMPLETE.txt').is_file(),'Final complete native marker missing')
  newrow={'kind':'public_brd','public_path':row['public_path'],'public_sha256':r['new_sha256'],'inventory_mode':'complete_native_reference_inventory_v1','native_job':art(d/'launch_report.json'),'inventory_files':{k:art(d/f) for k,f in [('components','ALL_COMPONENT_PACKAGE_REFERENCES.tsv'),('symbols','ALL_SYMBOL_NAME_DEFINITION_REFERENCES.tsv'),('symdefs','ALL_PACKAGE_DEFINITIONS.tsv')]},'acceptance_proofs':[{'path':e['path'],'sha256':e['sha256']} for e in r['native_proofs']]+[art(receipt)]}
  result['sources'][i]=newrow;changed.append({'source_index':i,'public_path':row['public_path'],'old_sha256':row['public_sha256'],'new_sha256':r['new_sha256'],'only_source_row_replaced':True})
 need(len(changed)==4,'Not exactly four pending source rows replaced');result['public_guard']=art(a.new_guard);result['source_state']='FINAL_PUBLIC_FILES_MATCH_MANIFEST'
 # Prove the complete source delta is limited to those four rows plus guard
 # pointer/state; no rehash-based rewrite of the already verified44 sources.
 inverse=copy.deepcopy(result)
 for e in changed:inverse['sources'][e['source_index']]=base['sources'][e['source_index']]
 inverse['public_guard']=base['public_guard'];inverse['source_state']=base['source_state'];need(inverse==base,'Unexpected metadata refresh outside four final BRD rows')
 a.out.mkdir(parents=True);out=a.out/'FINAL_NATIVE_REFERENCE_SOURCES.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 ledger={'status':'PASS_ONLY_FOUR_FINAL_PUBLIC_BRD_SOURCE_ROWS_COMPLETED','base_manifest':art(a.base_manifest),'final_manifest':art(out),'new_public_guard':art(a.new_guard),'publication_receipt':art(receipt),'exact_changed_source_rows':changed,'other44_source_rows_activeconfigs_canonical_proof_and_parser_identical':True,'script_sha256':sha(__file__),'CAD_started':False,'public_files_written':0};lp=a.out/'FOUR_SOURCE_COMPLETION_LEDGER.json';lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':ledger['status'],'manifest':art(out),'ledger':str(lp)}))
if __name__=='__main__':main()
