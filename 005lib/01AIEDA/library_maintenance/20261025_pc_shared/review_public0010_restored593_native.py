"""Independent complete593 snapshot inverse: exact403 definition names only.
Text snapshots are compared as complete typed multisets; no AUTOSILK allowance.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import argparse,copy,hashlib,json,sys
M=Path(__file__).parent
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025');from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def val(x):
 if isinstance(x,Decimal):return {'number':str(x.normalize())}
 if isinstance(x,Atom):return {'atom':str(x)}
 if isinstance(x,list):return [val(y) for y in x]
 return {'string':x}
stable=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'))
def read(p):return [parse_many(x)[0] for x in Path(p).read_text('utf-8').splitlines()]
def logical(rows):
 xs=[r for r in rows if r[0]=='symbol' and r[1][0]=='LOGICAL'];out={r[1][1]:r for r in xs};need(len(xs)==len(out)==572,'Exactly572 unique logical symbols required');return out
def canonical(row):
 v=val(row)
 if row[0]=='symbol':v[2]=sorted(v[2],key=stable)
 return stable(v)
def review(source,candidate,mapping):
 need(Counter(r[0] for r in source)==Counter(r[0] for r in candidate),'Complete snapshot kind/multiplicity changed');need(sum(r[0]=='symbol' for r in candidate)==593 and sum(r[0]=='component' for r in candidate)==572,'Full593/572 object scope required')
 olds,news=logical(source),logical(candidate);need(set(olds)==set(news),'Logical refdes cohort differs');need(len(mapping)==403 and set(mapping)<=set(olds),'Exact403 permitted name changes required');normalized=copy.deepcopy(candidate);ledger=[]
 for r in normalized:
  if r[0]=='symbol' and r[1][0]=='LOGICAL' and r[1][1] in mapping:
   ref=r[1][1];plan=mapping[ref];s=olds[ref][1];a=r[1];need(s[3].casefold()==s[4].casefold()==plan['old_package'].casefold(),'Source actual definition differs from exact per-ref plan '+ref)
   need(a[3].casefold()==a[4].casefold()==plan['new_package'].casefold(),'Candidate actual definition differs from exact per-ref target '+ref)
   ledger.append({'ref':ref,'source_symbol_name':s[3],'source_definition_name':s[4],'native_target_symbol_name':a[3],'native_target_definition_name':a[4]});a[3],a[4]=s[3],s[4]
 left,right=Counter(map(canonical,source)),Counter(map(canonical,normalized));need(left==right,'Full593 typed pose/text/property/font snapshot differs beyond exact403 definition names')
 return {'objects':593,'logical_components':572,'nonlogical_objects':21,'symbol_owned_text_records':sum(len(r[2]) for r in source if r[0]=='symbol'),'component_property_rows':572,'used_fontblock_rows':sum(r[0]=='textblock' for r in source),'permitted_definition_name_inverse_count':len(ledger),'all_other_fields_and_unknown_snapshot_values_exact':True,'source_complete_typed_multiset_sha256':hashlib.sha256(stable(sorted(left.items())).encode()).hexdigest().upper(),'candidate_inversed_complete_typed_multiset_sha256':hashlib.sha256(stable(sorted(right.items())).encode()).hexdigest().upper(),'exact_definition_name_ledger':ledger}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--fresh-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh proof output required');a.out.mkdir(parents=True)
 control=M/'public0010_source_noop_save13';saved=M/'public0010_netrev_text_restore13';planpath=M/'public_four_module_fp_plans13_v4/0010_EXACT_FOOTPRINT_PLAN.json';plan=jr(planpath);mapping={r['ref']:r for r in plan['changes']};srcpath=control/'CONTROL_BEFORE_ALL593_TEXT_PROPS.ilist';src=read(srcpath);cafter=control/'CONTROL_AFTER_ALL593_TEXT_PROPS.ilist';savedpath=saved/'POSTNETREV_SAVED_ALL593_TEXT_PROPS.ilist';freshpath=a.fresh_dir/'FRESH_ALL593_TEXT_PROPS.ilist';bindings=[srcpath,cafter,savedpath,freshpath,control/'RUN_RECEIPT.json',saved/'RUN_RECEIPT.json',a.fresh_dir/'RUN_RECEIPT.json',planpath]
 result={'status':'FAIL','CAD_started':False,'public_modified':False}
 try:
  need(srcpath.read_bytes()==cafter.read_bytes(),'Actual source-no-op full593 snapshots changed: no annotation allowance possible')
  cr,sr,fr=jr(control/'RUN_RECEIPT.json'),jr(saved/'RUN_RECEIPT.json'),jr(a.fresh_dir/'RUN_RECEIPT.json')
  for r in [cr,sr,fr]:need(r['status']=='PASS_NATIVE_CASE_PHASE_ONLY' and r['public_unchanged'],'Native phase not protectedPASS')
  need(cr['source_sha256_before']==cr['source_sha256_after']==plan['source_board_sha256'],'Control source not exact680500')
  need(sr['phase']=='postnetrev-restore' and fr['phase']=='restored-fresh','Expected restored-save and independent readonlyfresh phases')
  need(sr['candidate_sha256']==sha(sr['candidate'])==fr['source_sha256_before']==fr['source_sha256_after'],'Saved/fresh actual board SHA binding mismatch')
  need(Path(fr['marker']).is_file() and 'FRESH_FULL2698_593POSE_TEXT_PROP_572LOGICAL_NAMES_806TARGET_ADJ_EXACT_ORIGINAL_NO_AUTOSILK_ALLOWANCE_COMPLETE_NO_SAVE' in Path(fr['marker']).read_text('utf-8'),'Fullfresh2698/593/806 native marker missing')
  saveproof=review(src,read(savedpath),mapping);fresh=read(freshpath);proof=review(src,fresh,mapping);controls=[]
  def test(name,mutate):
   b=copy.deepcopy(fresh);mutate(b)
   try:review(src,b,mapping)
   except Exception as ex:controls.append({'case':name,'status':'PASS_REJECTED','reason':str(ex)})
   else:raise ValueError('Negative control accepted '+name)
  sym=lambda xs:next(r for r in xs if r[0]=='symbol' and r[1][0]=='LOGICAL' and r[2])
  test('user_text_changed',lambda xs:sym(xs)[2][0].__setitem__(0,'UNAPPROVED_TEXT'))
  test('extra_AUTOSILK_marker_even_on_existing_layer',lambda xs:sym(xs)[2].append(['UNAPPROVED',[Decimal(0),Decimal(0)],Decimal(0),Atom('nil'),'LEFT','MANUFACTURING/AUTOSILK_TOP','34',Atom('nil')]))
  test('original_text_removed',lambda xs:sym(xs)[2].pop())
  test('symbol_source_pose_changed_one_grid',lambda xs:sym(xs)[1][5].__setitem__(0,sym(xs)[1][5][0]+Decimal('.0001')))
  test('symbol_user_property_added',lambda xs:sym(xs).__setitem__(3,[[Atom('UNAPPROVED'),'X']]))
  test('component_compdef_property_changed',lambda xs:next(r for r in xs if r[0]=='component').__setitem__(3,[[Atom('VALUE'),'UNAPPROVED']]))
  test('used_fontblock_unknown_field_added',lambda xs:next(r for r in xs if r[0]=='textblock')[2].extend([Atom('UNAPPROVED'),Decimal(1)]))
  def wrongname(xs):
   r=next(r for r in xs if r[0]=='symbol' and r[1][0]=='LOGICAL' and r[1][1] in mapping);r[1][4]='WRONG_PACKAGE'
  test('mapped_footprint_wrong_name',wrongname)
  test('nonlogical_zero_pad_object_removed',lambda xs:xs.remove(next(r for r in xs if r[0]=='symbol' and r[1][0]=='NONLOGICAL')))
  result.update(status='PASS_SOURCE_NOOP_ZERO_DELTA_AND_SAVED_FRESH_FULL593_EXACT_SOURCE_ONLY403_DEFINITION_NAMES',source_noop_snapshot_bytes_identical=True,autosilk_additions_allowed=0,saved=saveproof,fresh=proof,negative_controls=controls,candidate_board=sr['candidate'],candidate_board_sha256=sr['candidate_sha256'],native_full2698_and_target806_marker_bound=True,scope='Independent all593 typed pose/text/symbolprops/component/compdefprops/used-fontblocks multiset inverse. Only403 exact symbol/definition names inversed; text child order treated as a complete duplicate-preserving multiset. Fullphysical2698 nativegate/806diagnostic marker bound; actual915GetConnect/copper/CFX approval is separate and still required.')
 except Exception as ex:result['error']=repr(ex)
 result['inputs']=[{'path':str(p),'sha256':sha(p)} for p in bindings if p.is_file()];result['script_sha256']=sha(__file__);(a.out/'FULL593_RESTORED_FRESH_REVIEW.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ['saved','fresh','inputs']},ensure_ascii=False,indent=2));return 0 if result['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
