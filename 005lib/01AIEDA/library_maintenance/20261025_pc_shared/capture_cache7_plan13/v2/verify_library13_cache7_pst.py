"""Independent complete PST proof: only frozen JEDEC_TYPE/source-library paths.
Preserves values, all pin uses/names/numbers, NC/DNP membership, all net names and
per-pin net assignment; validates every effective primitive in expanded context.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,importlib.util,json,re
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
LEGACY=R.parent/'12electrical_fixed_20261025/tools/verify_eco12.py'
s=importlib.util.spec_from_file_location('complete_pst_parser',LEGACY);P=importlib.util.module_from_spec(s);s.loader.exec_module(P)
XS=R/'tools/verify_library13_xml.py';s=importlib.util.spec_from_file_location('xml_plan_selectors',XS);X=importlib.util.module_from_spec(s);s.loader.exec_module(X)
need=P.require
SOURCE_SHA={'pstchip.dat':'2FA5DBC1451A0E75BD79D5C6C0DEEA92268604D4CE3B165F1802A3BCA3B7D891','pstxprt.dat':'2D33B12A9A7DFC7F049D8B991E8D179C31BA4E15A2F1FBE4C2907BB201C35067','pstxnet.dat':'03F7C4E77C2A0D531EB4D2E5AA5A85E782EFF4BD8154B0B0CF8DBD1416953C4F'}
def pathmap(plan):
 raw=Path(plan['source_design_xml']).read_bytes();need(X.U.sha(raw)==plan['source_xml_sha256'],'PST path binding source XML SHA mismatch')
 root=X.U.parse(raw);byid={X.U.defn(e).get('dbId'):X.U.defn(e) for e in root.findall('.//PartInst')};result={}
 for row in plan['instance_source_changes']:
  if row['kind']!='PartInst':continue
  d=byid[str(row['id'])];need(row['name'] in {d.get('name'),d.get('pkgName')},'Instance package/name differs from source plan')
  need(d.get('libName')==row['old_source'],'Source instance library differs from source plan')
  token=d.get('name').upper();need(bool(re.fullmatch('INS[0-9]+',token)) and token not in result,'Duplicate/invalid INS path identity')
  result[token]=(Path(row['old_source']).stem,Path(row['new_source']).stem)
 return result
PAT=re.compile(r'(?P<prefix>:(?:page_)?)(?P<ins>ins\d+)@(?P<lib>[^.\s\'"\\]+)\.',re.I)
def restore_paths(text,paths,candidate=True):
 def fix(m):
  token=m['ins'].upper();need(token in paths,'PST occurrence INS not in full XML source plan '+token)
  old,new=paths[token];expected=new if candidate else old
  need(m['lib'].upper()==expected.upper(),'Unexpected source library in PST occurrence '+token)
  target=old.upper() if m['lib'].isupper() else old.lower() if m['lib'].islower() else old
  need(m['lib'].isupper() or m['lib'].islower() or m['lib']==expected,'Unexpected mixed-case PST source stem')
  return m['prefix']+m['ins']+'@'+target+'.'
 return PAT.sub(fix,text)
def mappings(plan):
 result={}
 for row in X.fp_rows(plan):
  pair=(row['before'],row['after']);ref=row['ref']
  need(ref not in result or result[ref]==pair,'Multiunit footprint conflict '+ref);result[ref]=pair
 return result
def review(a,b,fp,paths):
 errors=[]
 def check(ok,code,**context):
  if not ok:errors.append({'code':code,**context})
 check(set(a['parts'])==set(b['parts']),'physical_ref_set_changed')
 check(a['prefixes']==b['prefixes'],'PST_header_directives_changed')
 check(a['pinmap']==b['pinmap'],'pin_net_assignment_changed')
 check(set(a['nets'])==set(b['nets']),'net_set_changed')
 check(P.partitions(a)==P.partitions(b),'connectivity_partition_count_changed')
 changes=[];aliases=[];nc=[]
 for ref in sorted(set(a['parts'])&set(b['parts'])):
  x,y=a['parts'][ref],b['parts'][ref];expected=x['body']
  if ref in fp:
   old,new=fp[ref]
   check(P.property_value(x['body'],'JEDEC_TYPE').upper()==old.upper(),'source_footprint_precondition',ref=ref)
   actual=P.property_value(y['body'],'JEDEC_TYPE')
   check(actual in {new,new.upper()},'candidate_footprint_not_plan',ref=ref,actual=actual,expected=new)
   expected=P.change_property(expected,'JEDEC_TYPE',P.property_value(expected,'JEDEC_TYPE'),actual)
   changes.append({'ref':ref,'before_JEDEC_TYPE':P.property_value(x['body'],'JEDEC_TYPE'),'after_JEDEC_TYPE':actual,'plan_after':new})
  check(y['body']==expected,'complete_effective_primitive_changed_beyond_FP',ref=ref)
  check(restore_paths(x['tail'],paths,False)==restore_paths(y['tail'],paths,True),'expanded_part_tail_or_path_changed',ref=ref)
  if x['primitive']!=y['primitive']:aliases.append({'ref':ref,'before':x['primitive'],'after':y['primitive'],'complete_effective_body_exact_after_FP_only_inverse':y['body']==expected})
  if P.property_value(x['body'],'VALUE').startswith('NC_'):
   nc.append(ref);check(P.property_value(x['body'],'VALUE')==P.property_value(y['body'],'VALUE'),'DNP_value_changed',ref=ref)
 for name in set(a['nets'])&set(b['nets']):
  check(a['nets'][name]['header']==b['nets'][name]['header'],'net_header_or_C_SIGNAL_changed',net=name)
  check(Counter(a['nets'][name]['members'])==Counter(b['nets'][name]['members']),'net_member_multiset_changed',net=name)
 for key in set(a['payload'])&set(b['payload']):
  check(restore_paths(a['payload'][key],paths,False)==restore_paths(b['payload'][key],paths,True),'complete_node_payload_or_path_changed',pin='.'.join(key))
 return {'status':'PASS_COMPLETE_PST_FP_AND_SOURCE_PATH_ONLY' if not errors else 'FAIL_PST_UNPLANNED_CHANGE','errors':errors,'physical_parts':len(b['parts']),'physical_pins':len(b['pinmap']),'nets':len(b['nets']),'connectivity_partitions':P.partitions(b),'planned_physical_FP_changes':changes,'planned_FP_refs_originally_excluded_from_physical_PST':sorted(set(fp)-set(a['parts'])),'physical_NC_value_refs_unchanged':nc,'generated_primitive_alias_changes':aliases,'source_primitives':len(a['primitives']),'candidate_primitives':len(b['primitives']),'all_primitive_definitions_referenced_and_fully_parsed':True}
def controls(a,b,fp,paths):
 out=[]
 def test(name,fn):
  z=copy.deepcopy(b);fn(z)
  try:r=review(a,z,fp,paths);bad=not r['status'].startswith('PASS')
  except ValueError:bad=True
  need(bad,'Negative control accepted '+name);out.append({'name':name,'status':'PASS_REJECTED'})
 ref=next(iter(b['parts']));key=next(iter(b['pinmap']))
 def body(z,field,val):
  item=z['parts'][ref];item['body']=P.change_property(item['body'],field,P.property_value(item['body'],field),val)
 test('unplanned_VALUE',lambda z:body(z,'VALUE','WRONG'))
 test('unplanned_JEDEC_TYPE',lambda z:body(z,'JEDEC_TYPE','WRONG'))
 test('unplanned_PART_NAME',lambda z:body(z,'PART_NAME','WRONG'))
 test('physical_pin_net_changed',lambda z:z['pinmap'].__setitem__(key,'WRONG'))
 test('physical_part_removed',lambda z:z['parts'].pop(ref))
 test('node_function_or_path_changed',lambda z:z['payload'].__setitem__(key,z['payload'][key]+'UNPLANNED'))
 test('primitive_pinuse_changed',lambda z:z['parts'][ref].__setitem__('body',z['parts'][ref]['body'].replace("PINUSE='UNSPEC'","PINUSE='INPUT'",1)))
 return out
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--xml-proof',type=Path,required=True);ap.add_argument('--export-meta',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--negative-controls',action='store_true');ar=ap.parse_args()
 need(not ar.out.exists(),'Fresh output required');ar.out.mkdir(parents=True)
 try:
  need({n:P.sha(ar.source/n) for n in P.FILES}==SOURCE_SHA,'Source is not published12 PST')
  plan=X.load(ar.plan);proof=X.load(ar.xml_proof)
  need(proof['status']=='PASS_PUBLIC_LIBRARY_FP_AND_EXACT_SEVEN_CACHE_DEFAULTS_FULL_ORDERED_XML' and proof['inputs']['plan_sha256']==P.sha(ar.plan),'Exact Cache7 XML proof not bound to frozen plan')
  need(len(plan['cache_default_pcb_footprint_changes'])==7 and proof['cache_default_pcb_footprint_changes']==plan['cache_default_pcb_footprint_changes'],'ExactsevenCacheDefault rows differ from independent proof')
  need(proof['inputs']['script_sha256']==P.sha(R/'tools/verify_library13_cache_defaults_xml.py') and proof['original_checker_sha256']==P.sha(R/'tools/verify_library13_xml.py'),'Cache7 proof checker bindings changed')
  need(P.sha(proof['inputs']['candidate_xml'])==proof['inputs']['candidate_xml_sha256'],'Actual candidate XML differs from proof')
  meta=X.load(ar.export_meta);need(meta['status']=='PASS_NATIVE_PST255_EXPORT' and meta['maximum_name_characters']==255 and meta['pstswp_exit']==0 and meta['error_count']==0 and meta['part_name_truncation_warnings']==0,'Native PST255 export gate failed')
  need(meta['source_not_written_by_exporter'] and meta['source_sha256_at_snapshot']==meta['source_sha256_after_export']==P.sha(meta['source']),'Native export wrote or no longer binds source DSN')
  need(Path(meta['netlist_directory']).resolve()==ar.candidate.resolve(),'Native meta not actual candidate PST directory')
  need({n:P.sha(ar.candidate/n) for n in P.FILES}=={row['name']:row['sha256'] for row in meta['files']},'Candidate PST files differ from original native export')
  need(P.sha(meta['configuration'])==meta['configuration_sha256'],'Native PST configuration changed')
  need(P.sha(meta['staged_dsn'])==meta['staged_dsn_sha256_after_packaging'],'Native packaged snapshot changed')
  iterator=X.U.ET.iterparse(proof['inputs']['candidate_xml'],events=['start']);design_name=None
  for event,e in iterator:
   if e.tag=='Defn':design_name=e.get('name');break
  need(design_name and Path(design_name).resolve()==Path(meta['source']).resolve(),'Native PST DSN path differs from actual XML-exported design identity')
  a,b=P.load_bundle(ar.source),P.load_bundle(ar.candidate);fp,paths=mappings(plan),pathmap(plan)
  report=review(a,b,fp,paths)
  report['native_export_binding']={'meta':str(ar.export_meta),'meta_sha256':P.sha(ar.export_meta),'source_dsn':meta['source'],'source_dsn_sha256':meta['source_sha256_at_snapshot'],'source_not_written_by_exporter':True,'packaged_snapshot_sha256':meta['staged_dsn_sha256_after_packaging'],'formal_DSN_must_be_the_untouched_source_not_packaged_snapshot':True,'maximum_name_characters':255,'pstswp_exit':0,'error_count':0,'part_name_truncation_warnings':0}
  if ar.negative_controls and report['status'].startswith('PASS'):report['negative_controls']=controls(a,b,fp,paths)
 except Exception as ex:report={'status':'FAIL_PST_GUARD_OR_SCHEMA','error':str(ex)}
 report['inputs']={'source':str(ar.source),'source_sha256':{n:P.sha(ar.source/n) for n in P.FILES},'candidate':str(ar.candidate),'candidate_sha256':{n:P.sha(ar.candidate/n) for n in P.FILES},'plan':str(ar.plan),'plan_sha256':P.sha(ar.plan),'xml_proof':str(ar.xml_proof),'xml_proof_sha256':P.sha(ar.xml_proof),'strict_parser_sha256':P.sha(LEGACY),'script_sha256':P.sha(__file__)}
 (ar.out/'PUBLIC_LIBRARY_PST_REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'status':report['status'],'report':str(ar.out/'PUBLIC_LIBRARY_PST_REVIEW.json'),'error':report.get('error')},ensure_ascii=False));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
