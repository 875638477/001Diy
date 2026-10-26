"""Complete clean native axlWriteDeviceFile bodies and actual component CLASS gate.
Separate per-definition directories prevent native26-char filename collisions.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,csv,hashlib,importlib.util,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=module('complete_device_body_gate',R/'tools/verify_public_module_device_bodies_v2.py');D=module('native_device_parser',R/'tools/audit_native_device_views_v3.py');F=module('protected_native_full_bindings',R/'tools/compare_public_noop_full.py');S=module('exact_two_singletons',R/'tools/verify_module008_singleton_control_v2.py')
need=G.need;sha=G.sha;load=G.load
def table(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def native(d,expected=None):
 q=load(d/'launch_report.json');h=q['source_sha256_before'];F.bind(d,expected or h,'NATIVE_DEVICE_BODIES_COMPLETE.txt')
 before=table(d/'PLAIN_NATIVE_COMPONENT_CLASSES.tsv');after=table(d/'AFTER_NATIVE_EXPORT_COMPONENT_CLASSES.tsv');need(Counter(json.dumps(r,sort_keys=True) for r in before)==Counter(json.dumps(r,sort_keys=True) for r in after),'Native readonly export altered actual component/class fields')
 rows=table(d/'NATIVE_DEVICE_BODY_MANIFEST.tsv');seen=set();devs=[];artifacts={}
 for r in rows:
  name=r['device_type'];need(name not in seen and r['api_return']=='t' and r['component_class']==r['compdef_class'],'Native definition manifest is not unique/class-consistent');seen.add(name)
  out=Path(r['output_directory']);need(out.resolve().parent==d.resolve() and out.name.startswith('device_'),'Native device source outside unique owned directory')
  files=[p for p in out.glob('*.txt') if p.read_text(encoding='utf-8-sig').startswith('(DEVICE FILE: ')];need(len(files)==1,'Native per-definition output not exactly one full device body')
  p=files[0];v=json.loads(json.dumps(D.parse_device(p)));need(v['device_type']==name and v['scalar']['CLASS']==r['compdef_class'] and v['scalar']['PACKAGE']==r['package'],'Full native device body disagrees with actual compdef/class identity')
  devs.append(v);artifacts[str(p)]=sha(p)
 need('DEVICES='+str(len(rows))+'\n' in (d/'NATIVE_DEVICE_BODIES_COMPLETE.txt').read_text(encoding='utf-8-sig'),'Inner native body count differs from complete unique manifest')
 return {'status':'UNIQUE_DEVICE_FUNCTION_PIN_BIJECTION','devices':devs},before,h,artifacts
def classes(source,candidate,plan):
 x={r['refdes']:r for r in source};y={r['refdes']:r for r in candidate};need(len(x)==len(source) and len(y)==len(candidate) and set(x)==set(y),'Full actual component/class rows not bijective');changes={r['ref']:r for r in plan['changes']};ledger=[]
 for ref,a in x.items():
  b=dict(y[ref])
  if ref in changes:
   p=changes[ref];need(a['package']==p['old_package'] and b['package']==p['new_package'].upper(),'Actual class row package not exact source/target footprint');b['package']=a['package']
  need(a==b,'Actual complete component/compdef CLASS or identity changed '+ref);ledger.append({'ref':ref,'device_type':a['device_type'],'actual_component_CLASS':a['component_class'],'actual_compdef_CLASS':a['compdef_class']})
 return ledger
def main():
 ap=argparse.ArgumentParser()
 for n in ['source-readonly','candidate-readonly','source-model','plan','out']:ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--singleton-proof',type=Path);a=ap.parse_args();need(not a.out.exists(),'Fresh output required');a.out.mkdir(parents=True);report={'status':'FAIL_COMPLETE_ACTUAL_NATIVE_DEVICE_BODY_OR_CLASS'}
 try:
  model,plan=load(a.source_model),load(a.plan);need(sha(a.source_model)==plan['source_model_sha256'],'Frozen source model differs')
  x,ca,sh,sa=native(a.source_readonly,model['native_source_sha256']);y,cb,ch,sb=native(a.candidate_readonly)
  # Bind the new API source against the original full source device evidence.
  source_reparse=[]
  if any('hidden_package_pins' not in d for d in model['devices']):
   need(sha(a.source_model)=='AA6CEDF852D7AFBEC95B85D005BFDA7696CB827AAFC9676723A34AF5EBF8C85D' and model['native_source_sha256']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898' and len(model['devices'])==101,'Only frozen0010 legacy-model parse completion allowed')
   reparsed=copy.deepcopy(model)
   for i,old in enumerate(model['devices']):
    need(sha(old['source'])==old['sha256'],'Frozen original full source device bytes changed');new=json.loads(json.dumps(D.parse_device(Path(old['source']))))
    need(all(k in new and new[k]==v for k,v in old.items()),'Existing frozen source model field differs from raw-device reparse');need(set(new)-set(old)=={'hidden_package_pins','native_header_device_identity_preserved','homogeneous_body_type_identity_used_if_native_comment_corrupt'} and new['hidden_package_pins']==[],'Unlisted schema completion or hidden package pins in0010')
    source_reparse.append({'device_type':old['device_type'],'original_raw_device_file':old['source'],'sha256':old['sha256'],'all_existing_frozen_model_fields_exact':True,'only_new_canonical_device_field':'hidden_package_pins','actual_raw_parsed_value':[],'additional_parser_identity_diagnostics':{k:new[k] for k in ['native_header_device_identity_preserved','homogeneous_body_type_identity_used_if_native_comment_corrupt']}});reparsed['devices'][i]=new
   model_for_body=reparsed
  else:model_for_body=model
  G.review(model_for_body,x,{'changes':[]});cl=classes(ca,cb,plan);singleton=[]
  if a.singleton_proof:
   proof=load(a.singleton_proof);need(proof['status']=='PASS_EXACT_SOURCE_VALUE_NATIVE_SINGLETON_SERIALIZATION_ONLY' and proof['source_model_sha256']==sha(a.source_model),'Exact same-value singleton serialization proof missing')
   source={d['device_type']:d for d in x['devices']};seen=0
   for i,d in enumerate(y['devices']):
    if d['device_type']==S.DEVICE:y['devices'][i],singleton=S.inverse_singletons(source[S.DEVICE],d);seen+=1
   need(seen==1,'Exact singleton device not unique')
  ledger=G.review(x,y,plan);controls=[]
  def reject(name,fn):
   z=copy.deepcopy(y);fn(z)
   try:G.review(x,z,plan)
   except (ValueError,KeyError):controls.append({'name':name,'status':'PASS_REJECTED'})
   else:raise ValueError('Negative control accepted '+name)
  reject('CLASS_changed',lambda z:z['devices'][0]['scalar'].__setitem__('CLASS','WRONG'))
  reject('PINUSE_changed',lambda z:next(iter(z['devices'][0]['function_types'].values())).__setitem__('pinuse',['WRONG']))
  reject('physical_pin_changed',lambda z:z['devices'][0]['functions'][0]['physical_pins'].__setitem__(0,'WRONG'))
  reject('source_VALUE_changed',lambda z:next(p for d in z['devices'] for p in d['package_properties'] if p['name']=='VALUE').__setitem__('value','WRONG'))
  reject('missing_device',lambda z:z['devices'].pop())
  report.update({'status':'PASS_ALL_ACTUAL_NATIVE_DEVICE_BODIES_AND_SOURCE_CLASSES','source_board_sha256':sh,'candidate_board_sha256':ch,'source_definition_count':len(x['devices']),'candidate_definition_count':len(y['devices']),'actual_all_component_CLASS_ledger':cl,'complete_ordered_device_body_ledger':ledger,'exact_bound_singleton_serialization_ledger':singleton,'source_native_body_sha256':sa,'exact_original_source_schema_completion_ledger':source_reparse,'candidate_native_body_sha256':sb,'negative_controls':controls})
 except Exception as ex:report['error']=str(ex)
 report['inputs']={str(p):sha(p) for p in [a.source_model,a.plan]+([a.singleton_proof] if a.singleton_proof else [])};report['native_launches']={str(d/'launch_report.json'):sha(d/'launch_report.json') for d in [a.source_readonly,a.candidate_readonly]};report['script_sha256']=sha(__file__);report['scope']='Actual freshly opened native database component+compdef classes and complete per-compdef axlWriteDeviceFile bodies. Standalone CLI export mismatches are retained as separate evidence, never used to excuse a native CLASS change. Only exact per-ref FP serialization, opaque TYPE allocation and optionally the proved two singleton groups may inverse; all other ordered device fields remain exact.'
 out=a.out/'PUBLIC_MODULE_ACTUAL_NATIVE_DEVICE_BODY_REVIEW.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'error':report.get('error'),'definitions':report.get('candidate_definition_count'),'report':str(out)}));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
