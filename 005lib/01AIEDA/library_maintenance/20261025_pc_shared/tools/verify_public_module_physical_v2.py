"""Full native board geometry, copper, placement and typed connectivity gate for unplaced module migrations.
Only exact per-ref native component PACKAGE fields may inverse to their source.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,importlib.util,json,re
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
s=importlib.util.spec_from_file_location('complete_native_physical_gate',R/'tools/compare_public_noop_full.py');F=importlib.util.module_from_spec(s);s.loader.exec_module(F)
need=F.need;sha=F.sha;read=F.read;tab=F.tab;stable=F.stable
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def components(d,plan,inverse):
 rows=F.SX.parse_many(read(d/'components_full.ilist'));mapping={r['ref']:r for r in plan['changes']};seen=set();out=Counter()
 for row in rows:
  need(isinstance(row,list) and len(row)==6 and row[0]=='component','Malformed complete native component tuple')
  ref=row[1]
  if ref in mapping:
   p=mapping[ref];need(ref not in seen and row[2]==p['device_type'],'Per-ref original component/device identity changed');seen.add(ref)
   expected=p['new_package'].upper() if inverse else p['old_package'];need(row[3]==expected,'Native component package not exact planned serialization '+ref)
   need(str(row[4])=='nil','These three modules must not place an alias-mapped component')
   if inverse:row[3]=p['old_package']
  out[stable(F.typed(row))]+=1
 need(seen==set(mapping),'Incomplete native component footprint cohort')
 return out
def actual_vias(d):
 _,rr=tab(d/'via_properties.tsv');need(all(F.DB.fullmatch(r['id']) for r in rr),'Malformed actual via native ID')
 return Counter(stable({k:v for k,v in r.items() if k!='id'}) for r in rr)
def ownership(d):
 _,syms=tab(d/'symbol_component_values.tsv');_,texts=tab(d/'symbol_owned_texts.tsv')
 if not syms:need(not texts,'Owned texts exist without any actual symbol binding');return {}
 return F.ownership_ids(d)
def main():
 ap=argparse.ArgumentParser()
 for name in ['source','candidate','source-model','plan','view-proof','out']:ap.add_argument('--'+name,type=Path,required=True)
 a=ap.parse_args();need(not a.out.exists(),'Fresh output required');a.out.mkdir(parents=True);report={'status':'FAIL_FULL_PUBLIC_MODULE_NATIVE_PHYSICAL','checks':[]};checks=report['checks']
 def check(name,x,y):
  checks.append({'artifact':name,'equal':x==y,'source_rows':sum(x.values()) if isinstance(x,Counter) else None,'candidate_rows':sum(y.values()) if isinstance(y,Counter) else None,'source_only_count':sum((x-y).values()) if isinstance(x,Counter) else None,'candidate_only_count':sum((y-x).values()) if isinstance(y,Counter) else None})
 try:
  model,plan,proof=load(a.source_model),load(a.plan),load(a.view_proof);need(sha(a.source_model)==plan['source_model_sha256'],'Frozen source complete model mismatch');need(proof['status'] in {'PASS_COMPLETE_PUBLIC_MODULE_VIEWS_ONLY_PLANNED_FP_AND_FUNCTION_IDS','PASS_COMPLETE_PUBLIC_MODULE_VIEWS_FP_FUNCTION_IDS_EXACT_PENDING_DRC_METADATA'} and proof['inputs'][str(a.plan)]==sha(a.plan),'Actual complete views/per-ref plan proof missing')

  if proof['status']=='PASS_COMPLETE_PUBLIC_MODULE_VIEWS_FP_FUNCTION_IDS_EXACT_PENDING_DRC_METADATA':
   jl=load(Path(proof['job_metadata_ledger_path']));need(sha(proof['job_metadata_ledger_path'])==proof['job_metadata_ledger_sha256'] and jl==proof['exact_job_DRC_status_metadata_ledger'] and jl['schema']=='MODULE008_EXACT_POST_ECO_DRC_STATUS_METADATA_V1' and jl['candidate_board_sha256']=='63CE53B7FBEB0063B56A957DFF958352CFAC5EE3153A8988D4395BDFC3674F10','Unproved exact008 post-ECO J metadata ledger')
  after=load(a.candidate/'launch_report.json')['source_sha256_before'];F.bind(a.source,model['native_source_sha256'],'PUBLIC_BOARD_COMPLETE.txt');F.bind(a.candidate,after,'PUBLIC_BOARD_COMPLETE.txt')
  expected=[v for p,v in proof['inputs'].items() if p.lower().endswith('.brd')];need(expected==[after],'Native view proof candidate SHA differs')
  need(read(a.source/'PUBLIC_BOARD_COMPLETE.txt')==read(a.candidate/'PUBLIC_BOARD_COMPLETE.txt'),'Complete native object/cached placed definition counts changed')
  need('COMPONENTS='+str(len(model['views']['comp']['rows']))+'\n' in read(a.source/'PUBLIC_BOARD_COMPLETE.txt'),'Native inner component count differs from complete source model')
  for name in ['symbols.tsv','all_symbol_pins.tsv','stored_net_status.tsv','physical_object_properties.ilist','shape_polygons.jsonl','shape_metadata.tsv','dynamic_settings.txt','stored_drcs.txt']:
   check(name,Counter(read(a.source/name).splitlines()),Counter(read(a.candidate/name).splitlines()))
  check('complete_component_props_only_exact_FP_inverse',components(a.source,plan,False),components(a.candidate,plan,True))
  check('all_actual_via_payloads',actual_vias(a.source),actual_vias(a.candidate))
  x,ex=F.partition(a.source);y,ey=F.partition(a.candidate);check('all_complete_typed_physical_endpoints',ex,ey);check('all_actual_copper_pin_partitions',x,y)
  for n in ['explicit_and_boundary_geometry.tsv','before/explicit_and_boundary_geometry.tsv']:
   left,right=read(a.source/n),read(a.candidate/n);need(not F.PTR.search(left+right),'Actual fill pointer requires separate complete native fill struct evidence')
   check(n,Counter(left.splitlines()),Counter(right.splitlines()))
  ia,ib=ownership(a.source),ownership(a.candidate)
  for n in ['symbol_component_values.tsv','symbol_owned_texts.tsv','unowned_design_texts.tsv','all_textblocks.tsv']:
   ka,ca=F.owner_table(a.source,n,ia);kb,cb=F.owner_table(a.candidate,n,ib);need(ka==kb,'Complete owner/text/font field headers changed');check(n,ca,cb)
  report.update({'status':'PASS_FULL_PUBLIC_MODULE_NATIVE_PHYSICAL_ONLY_PLANNED_COMPONENT_FP' if all(c['equal'] for c in checks) else 'FAIL_REAL_PUBLIC_MODULE_NATIVE_PHYSICAL_DIFFERENCES','source_board_sha256':model['native_source_sha256'],'candidate_board_sha256':after,'actual_physical_pads':sum(ex.values()),'actual_copper_groups':sum(x.values()),'all_actual_polygon_objects':len(read(a.source/'shape_polygons.jsonl').splitlines()),'all_explicit_geometry_rows':len(read(a.source/'explicit_and_boundary_geometry.tsv').splitlines()),'planned_unplaced_alias_refs':len(plan['changes']),'negative_controls':[]})
  for name,c in [('physical_pin_or_NC_drop',ex),('actual_copper_partition_duplicate',x),('full_geometry_object_drop',Counter(read(a.source/'explicit_and_boundary_geometry.tsv').splitlines()))]:
   if not c:continue
   bad=c.copy();key=next(iter(bad));bad[key]+=1;need(bad!=c,'Physical multiset negative control accepted');report['negative_controls'].append({'name':name,'status':'PASS_REJECTED'})
 except Exception as ex:report['error']=str(ex)
 report['inputs']={str(p):sha(p) for p in [a.source_model,a.plan,a.view_proof]};report['native_artifact_sha256']={str(p):sha(p) for d in [a.source,a.candidate] for p in d.iterdir() if p.is_file() and p.suffix.lower() not in {'.brd','.jrl','.lck','.dmp'}};report['script_sha256']=sha(__file__);report['scope']='Only complete actual native physical/geometry/copper/typed connectivity and text/font data. Three modules have no alias-mapped placed parts; all existing nonlogical placed objects must remain exact. Complete device schema/CLASS and full CFX/TCFX are separate required gates. No runtime fill pointer, copper contour, pin count, net-type or ownership differences are hidden.'
 out=a.out/'PUBLIC_MODULE_COMPLETE_PHYSICAL_REVIEW.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'error':report.get('error'),'checks':len(checks),'failed':[c['artifact'] for c in checks if not c['equal']],'report':str(out)}));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
