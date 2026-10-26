"""Aggregate/recheck complete cold-native target graphs and current full PAD XML.
No native process, design, public library, or old evidence is modified.
"""
from pathlib import Path
from collections import defaultdict
import argparse,csv,hashlib,importlib.util,json,sys,xml.etree.ElementTree as E
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
B=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025')
LIB=Path(r'D:\001DIY\005lib')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def art(p):return {'path':str(Path(p)),'sha256':sha(p)}
def norm(p):return str(Path(p).resolve()).casefold()
def need(x,s):
 if not x:raise ValueError(s)
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
N=module('full_native_cold_target_schema27',M/'review_global_suffix_native_chunks.py')
G=module('complete_manufacturing_pad_schema27',B/'analyze_pad_geometry.py')
GROUPS=[('global_canonical_targets_native13','global_canonical_targets_review13'),('nonpassive_exact_targets_native13','nonpassive_exact_targets_review13'),('project81_exact_targets_native13','project81_exact_targets_review13'),('project81_current_targets_native13','project81_current_targets_review13'),('global_nonpassive_native13','global_nonpassive_native_review13'),('global_nonpassive_increment_native13','global_nonpassive_increment_review13'),('global_suffix_native_v3','global_suffix_native_review_v3'),('native_audits/final13_4layer',None)]
def required(plan):return {r['target'].casefold() for r in plan['ordinary_or_explicit_standardization_rows'] if r['target']}
def full_pad(el):
 unknown=sorted({x.tag for x in el.iter()}-G.KNOWN_TAGS);need(not unknown,'Unknown PAD manufacturing fields '+str(unknown));factor=G.FACTORS[el.findtext('units')]
 return {'full_native_xml_object_sha256':hashlib.sha256(E.tostring(el)).hexdigest().upper(),'all_classified_manufacturing_fields_signature':G.digest(G.canonical(el,factor,G.IGNORED)),'all_manufacturing_fields_except_drill_symbol_signature':G.digest(G.canonical(el,factor,G.IGNORED|{'drillsymbol'})),'parts':{k:G.part(el,factor,k) for k in ('copper','mask_paste','thermal_antipad','drill','drillsymbol','behavior')},'geometry_mm':G.summary(el,factor),'custom_shape_flash_references_preserved_not_erased':[{'kind':x.tag,'name':(x.text or '').strip()} for x in el.iter() if x.tag in ('shapename','flashname') and (x.text or '').strip()]}
class PadReader:
 def __init__(self):self.xml={}
 def get(self,path,name):
  k=str(Path(path))
  if k not in self.xml:
   root=E.parse(path).getroot();ix=defaultdict(list)
   for el in root.findall('padstack'):ix[(el.findtext('padstackname') or '').casefold()].append(el)
   self.xml[k]=ix
  found=self.xml[k][name.casefold()];need(len(found)==1,'PAD XML full object ambiguous/missing '+name);return found[0]
def validate_index(index,plan,current_guard):
 need(index['schema']=='EXACT_REQUIRED_CANONICAL_NATIVE_AND_PAD_TARGET_INDEX_V1','Wrong canonical index class')
 need(index['retirement_plan_sha256']==sha(index['retirement_plan']),'Canonical retirement input changed')
 need(sha(index['canonicalizer']['path'])==index['canonicalizer']['sha256'] and Path(index['canonicalizer']['path']).resolve()==(B/'analyze_pad_geometry.py').resolve(),'PAD canonicalizer code changed')
 need(sha(index['native_schema_parser']['path'])==index['native_schema_parser']['sha256'] and Path(index['native_schema_parser']['path']).resolve()==(M/'review_global_suffix_native_chunks.py').resolve(),'Native full-graph parser code changed')
 want=required(plan);need(len(index['targets'])==len(want)==127 and {v['target'] for v in index['targets']}==want,'Canonical target127 complete unique coverage missing')
 need(not index['errors'] and index['status']=='PASS_REQUIRED127_CANONICAL_COLD_NATIVE_AND_FULL_PAD_CURRENT_BINDING','Canonical index has unresolved target failure')
 gi={norm(v['path']):v for v in current_guard['files']};reader=PadReader();evidence={};seenpads={}
 for v in index['evidence']:
  need(sha(v['path'])==v['sha256'],'Canonical frozen native/PAD evidence changed '+v['path']);evidence[v['path']]=v['sha256']
 for row in index['targets']:
  path=Path(row['public_psm']['path']);need(path.parent.resolve()==(LIB/'01Psm_lib').resolve() and path.stem.casefold()==row['target'],'Target is not the exact authoritative public PSM stem')
  need(sha(path)==row['public_psm']['sha256']==row['native_source_psm_sha256']==gi[norm(path)]['sha256'],'Target current/guard/cold source PSM binding changed '+row['target'])
  need(sha(row['native_graph']['path'])==row['native_graph']['sha256'],'Cold full-native graph changed')
  schema=N.inspect(Path(row['native_graph']['path']));need(not schema['issues'] and schema['full_ordered_graph_fingerprint']==row['full_ordered_graph_fingerprint'] and schema['physical_core_fingerprint']==row['physical_core_fingerprint'],'Target full graph/schema no longer identical')
  deps=schema['actual_loaded_pad_files'];need(len(row['pads'])==len(deps) and {(norm(x['path']),x['sha256']) for x in deps}=={(norm(x['public_pad']['path']),x['public_pad']['sha256']) for x in row['pads']},'Target complete loaded PAD dependency set differs')
  for pad in row['pads']:
   p=pad['public_pad'];need(sha(p['path'])==p['sha256']==gi[norm(p['path'])]['sha256'],'Actual PAD bytes changed')
   x=pad['native_xml'];need(sha(x['path'])==x['sha256'],'Full native PAD XML changed');key=(x['path'],pad['original_native_exported_name'])
   if key not in seenpads:seenpads[key]=full_pad(reader.get(x['path'],pad['original_native_exported_name']))
   need(seenpads[key]==pad['complete_manufacturing'],'Full PAD manufacturing signature/payload changed')
 return {'status':'PASS_EXACT127_TARGETS_RECOMPUTED_CURRENT_FULL_NATIVE_AND_PAD','targets':127,'unique_PAD_objects':len(seenpads),'evidence_files':len(evidence)}
def build(plan_path,guard_path,out):
 need(not out.exists(),'Fresh canonical index output required');out.mkdir(parents=True);plan=load(plan_path);guard=load(guard_path);gi={norm(v['path']):v for v in guard['files']};want=required(plan);candidates=defaultdict(list);padrefs=defaultdict(list);evidence={};reader=PadReader()
 def use(p):evidence[str(Path(p))]=sha(p);return art(p)
 for native,review in GROUPS:
  mp=M/native/'manifest.json';manifest=load(mp);use(mp)
  for row in manifest:
   paths=row.get('byte_identical_members',[])+[row['source_path']]
   for p in paths:
    target=Path(p).stem.casefold()
    if target in want:candidates[target].append((native,row,mp))
  if review:
   pp=M/review/'FULL_PAD_XML_BINDING.json';pr=load(pp);need(pr['status']=='CURRENT_LOADED_PAD_BYTES_BOUND_TO_COMPLETE_PRIOR_NATIVE_XML_RECOMPUTED' and not pr['errors'],'Full native PAD coverage incomplete '+str(pp));use(pp)
   for r in pr['records']:padrefs[norm(r['path'])].append((r,pp))
 # Current full native PAD exports for first13 generic assets complement the
 # byte-identical prior catalog. Full paths/source SHAs are frozen by this CSV.
 cp=M/'native_audits/pd13/public/manifest.csv';use(cp)
 with cp.open(encoding='utf-8-sig',newline='') as f:
  for r in csv.DictReader(f):
   need(r['Status']=='ok','Native PAD export failure in first13 public cohort')
   padrefs[norm(r['FullPath'])].append(({'path':r['FullPath'],'current_sha256':r['SHA256'],'native_xml_path':r['XMLPath'],'native_xml_sha256':sha(r['XMLPath']),'original_native_exported_name':r['ExportedName']},cp))
 rows=[];errors=[]
 for target in sorted(want):
  try:
   choices=candidates[target];need(choices,'No actual cold native source for target '+target)
   # Prefer a native load of the canonical exact stem, then byte-identical
   # member source. Both are exact current PSM bytes, never geometry guessing.
   choices.sort(key=lambda q:Path(q[1]['source_path']).stem.casefold()!=target)
   native,src,mp=choices[0];p=LIB/'01Psm_lib'/(target+'.psm');need(p.is_file(),'Canonical target PSM missing');h=sha(p);need(h==src['source_sha256']==gi[norm(p)]['sha256'],'Canonical actual PSM bytes do not match native input')
   np=Path(src['audit_output']);e=N.inspect(np);need(not e['issues'],'Target native unknown/unresolved graph fields '+str(e['issues']));use(np);d=np.parent.parent
   launch=d/'launch_report.json'
   if launch.is_file():
    q=load(launch);need(q['exit_code']==0 and q['complete'] and q['source_unchanged'] and q['source_sha256_before']==q['source_sha256_after']==h and q['audit_output_sha256']==sha(np),'Cold per-target native load/protection incomplete');use(launch);use(d/'manifest.json')
   else:
    q=load(M/native/'report.json');need(q['complete'] and q['source_files_unchanged'] and q['launch']['exit_code']==0 and {norm(k):v for k,v in q['protected'].items()}[norm(src['source_path'])]==h,'Full batch native source protection incomplete');use(M/native/'report.json')
   pads=[]
   for dep in e['actual_loaded_pad_files']:
    pp=Path(dep['path']);ph=sha(pp);need(ph==dep['sha256']==gi[norm(pp)]['sha256'],'Cold target resolved PAD current SHA mismatch')
    options=[(r,b) for r,b in padrefs[norm(pp)] if r['current_sha256']==ph];need(options,'Complete manufacturing PAD XML missing '+str(pp));pr,pf=options[0];el=reader.get(pr['native_xml_path'],pr['original_native_exported_name']);full=full_pad(el)
    for k,v in full.items():
     if k in pr:need(pr[k]==v,'Prior complete PAD XML recomputation mismatch '+k+' '+str(pp))
    use(pr['native_xml_path']);pads.append({'public_pad':art(pp),'actual_native_loaded_name':dep['source_name'],'native_xml':art(pr['native_xml_path']),'original_native_exported_name':pr['original_native_exported_name'],'complete_manufacturing':full,'frozen_original_full_PAD_binding':art(pf)})
   rows.append({'target':target,'public_psm':art(p),'native_source_psm':src['source_path'],'native_source_psm_sha256':h,'source_binding':'EXACT_CANONICAL_SOURCE_NATIVE_LOAD' if Path(src['source_path']).stem.casefold()==target else 'FROZEN_MANIFEST_BYTE_IDENTICAL_MEMBER_TO_NATIVE_SOURCE','native_manifest':art(mp),'native_graph':art(np),'full_ordered_graph_fingerprint':e['full_ordered_graph_fingerprint'],'physical_core_fingerprint':e['physical_core_fingerprint'],'pin_numbers':e['pin_numbers'],'native_complete_issues':e['issues'],'pads':pads})
  except Exception as ex:errors.append({'target':target,'error':str(ex)})
 report={'schema':'EXACT_REQUIRED_CANONICAL_NATIVE_AND_PAD_TARGET_INDEX_V1','status':'PASS_REQUIRED127_CANONICAL_COLD_NATIVE_AND_FULL_PAD_CURRENT_BINDING' if not errors and len(rows)==len(want)==127 else 'FAIL_REQUIRED_CANONICAL_NATIVE_TARGET_COVERAGE','retirement_plan':str(plan_path),'retirement_plan_sha256':sha(plan_path),'guard_at_aggregation':art(guard_path),'targets':rows,'errors':errors,'ambiguous_bare_retirements_without_single_target':[r['source'] for r in plan['ordinary_or_explicit_standardization_rows'] if r['target'] is None],'evidence':[{'path':p,'sha256':h} for p,h in evidence.items()],'canonicalizer':art(B/'analyze_pad_geometry.py'),'native_schema_parser':art(M/'review_global_suffix_native_chunks.py'),'script_sha256':sha(__file__),'CAD_started':False,'public_files_written':0}
 if not errors:report['independent_recheck']=validate_index(report,plan,guard)
 p=out/'REQUIRED_CANONICAL_NATIVE_TARGET_INDEX.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'targets':len(rows),'errors':errors,'path':str(p),'sha256':sha(p)},ensure_ascii=False));return 0 if report['status'].startswith('PASS') else 2
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();return build(a.plan,a.guard,a.out)
if __name__=='__main__':raise SystemExit(main())
