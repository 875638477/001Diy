"""Independent complete ordered OLB XML inverse and native LOGFONT stage review."""
from pathlib import Path
from collections import Counter
import argparse,copy,csv,hashlib,json,re,xml.etree.ElementTree as E
FONT_FIELDS={'Name','Height','Width','Escapement','Orientation','Weight','Italic','Underline','StrikeOut','CharSet','OutPrecision','ClipPrecision','Quality','PitchAndFamily'}
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def can(e):return [e.tag,sorted(e.attrib.items()),(e.text or '').strip(),[can(c) for c in e]]
def dig(e):return hashlib.sha256(json.dumps(can(e),ensure_ascii=False,separators=(',',':')).encode()).hexdigest().upper()
def path_node(root,field):
 parts=field.split('/');attr=parts.pop();need(attr.startswith('@'),'Expected exact attribute path')
 parts=[p for p in parts if p];need(parts.pop(0)=='Lib[1]' and root.tag=='Lib','Unexpected OLB root selector')
 e=root
 for p in parts:
  m=re.fullmatch(r'([A-Za-z][A-Za-z0-9_]*)\[([1-9][0-9]*)\]',p);need(m is not None,'Unexpected exact XML path '+p);matches=[c for c in e if c.tag==m[1]];i=int(m[2])-1;need(i<len(matches),'XML field path missing '+field);e=matches[i]
 return e,attr[1:]
def norm_name(root,expected):
 q=copy.deepcopy(root);d=q.find('Defn');need(d is not None and set(d.attrib)=={'name'},'Unexpected top-level Lib identity fields')
 need(Path(d.get('name')).resolve()==Path(expected).resolve(),'Native XML opened a different library identity')
 d.set('name','@EXACT_OPENED_OLB_PATH@');return q
def inverse_package_order(original,candidate):
 """Only top-level Package serialization order; no subtree/other-tag changes."""
 q=copy.deepcopy(candidate);source=[e for e in original if e.tag=='Package'];actual=[e for e in q if e.tag=='Package']
 def names(es):
  out=[]
  for e in es:
   d=e.find('Defn');need(d is not None and d.get('name') is not None,'Package lacks exact native name');out.append(d.get('name'))
  need(len(out)==len(set(out)),'Top-level Package name/multiplicity ambiguous');return out
 sn,tn=names(source),names(actual);need(len(sn)==len(tn) and set(sn)==set(tn),'Top-level Package cohort/names/multiplicity changed')
 need([c.tag for c in original]==[c.tag for c in q],'Top-level non-Package layout/ordered tag cohort changed')
 byname=dict(zip(tn,actual));positions=[i for i,c in enumerate(q) if c.tag=='Package']
 for i,name in zip(positions,sn):q[i]=byname[name]
 ledger={'scope':'Only top-level Package object serialization order is inversed by exact unique Defn/@name; all full Package contents/child orders and Lib defaults/fonts remain strict.','package_count':len(sn),'source_order':sn,'native_after_save_order':tn,'source_root_child_indices':positions,'position_changes':[{'name':name,'source_Package_index':i,'native_after_save_Package_index':tn.index(name),'source_root_child_index':positions[i],'native_root_child_index':positions[tn.index(name)]} for i,name in enumerate(sn) if tn.index(name)!=i],'same_name_multiplicity_bijection':True}
 return q,ledger
def review(original,candidate,fields,original_path,candidate_path):
 target,order=inverse_package_order(original,candidate);ledger=[];seen=set()
 for row in fields:
  field=row['field_path'];need(field not in seen,'Duplicate exact XML mutation field');seen.add(field)
  s,attribute=path_node(original,field);t,attribute2=path_node(target,field);need(attribute==attribute2==row['attribute'],'Mutation attribute differs from frozen plan')
  need(s.get(attribute)==row['old_value'],'Original field precondition differs '+field)
  need(t.get(attribute)==row['proposed_value'],'Candidate field not exact planned target '+field)
  need(set(s.attrib)==set(t.attrib),'Field attribute presence changed '+field)
  t.set(attribute,row['old_value']);ledger.append({'field':field,'before':row['old_value'],'after':row['proposed_value']})
 a,b=norm_name(original,original_path),norm_name(target,candidate_path);need(can(a)==can(b),'Full ordered library XML differs beyond exact PCB Footprint fields and opened path')
 return {'all_ordered_elements':sum(1 for _ in a.iter()),'original_objects':dict(Counter(c.tag for c in a)),'inverse_full_library_sha256':dig(b),'source_full_library_sha256':dig(a),'field_ledger':ledger,'top_level_Package_native_serialization_order_inverse':order}
def font_review(path):
 rows=list(csv.DictReader(Path(path).open(encoding='utf-8-sig'),delimiter='\t'));need(len(rows)==337,'Expected24 fonts x14 fields +primitive')
 keys=Counter((r['kind'],r['index'],r['field']) for r in rows);need(all(v==1 for v in keys.values()),'Native font field multiplicity changed')
 expected={('font',str(i),f) for i in range(24) for f in FONT_FIELDS}|{('library','','DefaultPlacedInstIsPrimitive')}
 need(set(keys)==expected,'Native LOGFONT/default property cohort changed')
 need(all(r['equal']=='1' and r['expected']==r['before']==r['actual'] for r in rows),'Native LOGFONT/default property changed')
 return {'fonts':24,'LOGFONT_fields_each':14,'native_fields_equal':337,'report_sha256':sha(path)}

def bounded_frozen_identity(evidence_path,case,root):
 z=load(evidence_path)
 need(z['schema']=='EXACT_NATIVE_FROZEN_SOURCE_LIBRARY_IDENTITY_V1','Unknown bounded source identity evidence schema')
 for field in ['source_xml','opened_olb','public_original','native_job_result','owned_process','native_identity','original_reviewer']:
  need(sha(z[field])==z[field+'_sha256'],'Bounded source identity artifact changed '+field)
 need(Path(z['source_xml']).resolve()==Path(case['frozen_source_xml']).resolve(),'Bounded source evidence names another frozen XML')
 need(z['source_xml_sha256']==case['frozen_source_xml_sha256'],'Bounded source XML SHA differs from frozen case')
 need(Path(z['public_original']).resolve()==Path(case['public_original']).resolve(),'Bounded evidence names another public library')
 need(z['opened_olb_sha256']==z['public_original_sha256']==case['original_sha256'],'Opened stage and actual original public bytes are not identical')
 job=load(z['native_job_result']);need(job['status']=='COMPLETE' and job['exit_code']==0 and job['protected_unchanged'] and job['protected_before']==job['protected_after'],'Incomplete/mutating bounded source native export')
 opened=str(Path(z['opened_olb']).resolve())
 need(job['protected_before'].get(opened)==case['original_sha256'],'Bounded native source was not SHA protected')
 argv=load(z['owned_process'])['command'];need(len(argv)==5,'Unexpected native source export argv count')
 need(Path(argv[2]).resolve()==Path(z['opened_olb']).resolve(),'Native export argv opened another OLB')
 need(Path(argv[4]).resolve()==Path(z['source_xml']).parent.resolve(),'Native export argv wrote another output')
 identity=Path(z['native_identity']).read_text(encoding='utf-8-sig')
 need('save_calls 0' in identity and z['opened_olb'] in identity,'Readonly native identity record does not bind opened source')
 norm_name(root,z['opened_olb'])
 return {'opened_identity':z['opened_olb'],'public_identity':z['public_original'],'identical_OLB_sha256':case['original_sha256'],'evidence_path':str(evidence_path),'evidence_sha256':sha(evidence_path),'native_argv':argv,'source_xml_sha256':z['source_xml_sha256']}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--case',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--frozen-source-identity-evidence',type=Path);a=ap.parse_args();need(not a.out.exists(),'Fresh review output required');a.out.mkdir(parents=True)
 report={'status':'FAIL','CAD_started':False,'input_modified':False}
 try:
  c=load(a.case);need(c['schema']=='PUBLIC_OLB_STAGING_CASE_V1','Unknown staging case schema')
  original,candidate,public=Path(c['original_snapshot']),Path(c['candidate']),Path(c['public_original'])
  need(sha(original)==sha(public)==c['original_sha256'],'Original public/snapshot bytes changed')
  need(sha(candidate)==c['candidate_sha256'],'Saved staging candidate bytes changed')
  for key in ['apply_job','reopen_job']:
   q=load(Path(c[key])/'job_result.json');need(q['status']=='COMPLETE' and q['exit_code']==0 and q['protected_unchanged'] and q['protected_before']==q['protected_after'],'Incomplete/source-mutating native staging job '+key)
   need(q['protected_before'].get(str(public.resolve()))==c['original_sha256'],'Native job did not protect actual original public path')
  q=load(Path(c['reopen_job'])/'job_result.json');need(q['protected_before'].get(str(candidate.resolve()))==c['candidate_sha256'],'Native readonly reopen not bound to exact saved candidate')
  base=E.parse(c['frozen_source_xml']).getroot();src=E.parse(c['original_native_xml']).getroot();dst=E.parse(c['candidate_native_xml']).getroot()
  need(sha(c['frozen_source_xml'])==c['frozen_source_xml_sha256'],'Frozen36-library source XML changed')
  source_identity=bounded_frozen_identity(a.frozen_source_identity_evidence,c,base) if a.frozen_source_identity_evidence else None
  frozen_expected=source_identity['opened_identity'] if source_identity else public
  need(can(norm_name(base,frozen_expected))==can(norm_name(src,original)),'Re-exported original snapshot is not complete original frozen library XML')
  proof=review(src,dst,c['fields'],original,candidate);fonts=font_review(c['font_report'])
  need(Path(c['original_defaults']).read_bytes()==Path(c['actual_defaults']).read_bytes(),'Complete original/staging native default specs changed')
  controls=[]
  def trial(name,mutate):
   bad,_=inverse_package_order(src,dst);mutate(bad)
   try:review(src,bad,c['fields'],original,candidate)
   except Exception as e:controls.append({'name':name,'status':'PASS_REJECTED','reason':str(e)[:600]})
   else:raise ValueError('OLB negative control accepted '+name)
  row=c['fields'][0]
  trial('PCB_Footprint_wrong_target',lambda r:path_node(r,row['field_path'])[0].set(row['attribute'],'UNPLANNED'))
  def alter_pin(r):
   d=r.find('.//SymbolPinScalar/Defn');need(d is not None,'No pin negative control available');d.set('hotptX','999999')
  trial('pin_hotspot_changed',alter_pin)
  trial('Package_removed',lambda r:r.remove(r.find('Package')))
  trial('Package_name_changed',lambda r:r.find('./Package/Defn').set('name','UNPLANNED_PACKAGE'))
  trial('Package_duplicate_multiplicity',lambda r:r.append(copy.deepcopy(r.find('Package'))))
  trial('Package_unrelated_field_changed',lambda r:r.find('./Package/Defn').set('refdesPrefix','UNPLANNED'))
  trial('pin_number_or_name_changed',lambda r:r.find('.//SymbolPinScalar/Defn').set('name','UNPLANNED_PIN'))
  def child_order(r):
   p=r.find('Package');need(len(p)>1,'No child order negative control available');p[0],p[1]=p[1],p[0]
  trial('Package_internal_child_order_changed',child_order)
  trial('DefaultFont_changed',lambda r:r.find('./DefaultValues/DefaultFont/Defn').set('weight','9999'))
  trial('unlisted_symbol_property_added',lambda r:E.SubElement(r.find('Package'), 'UnplannedProperty'))
  report.update({'status':'PASS_COMPLETE_ORDERED_OLB_FP_FIELDS_AND_NATIVE_ALL_FONT_FIELDS_STAGING_ONLY','proof':proof,'native_fonts':fonts,'negative_controls':controls,'public_original_unchanged_sha256':sha(public),'candidate_sha256':sha(candidate),'public_files_replaced':0,'bounded_frozen_source_identity':source_identity})
 except Exception as e:report['error']=repr(e)
 report.update({'case':str(a.case),'case_sha256':sha(a.case),'script_sha256':sha(__file__),'scope':'Only independent staging validation. Does not publish any public library or supersede the full global native SHA guard.'})
 p=a.out/'PUBLIC_OLB_STAGE_REVIEW.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'status':report['status'],'error':report.get('error'),'report':str(p)},ensure_ascii=False));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
