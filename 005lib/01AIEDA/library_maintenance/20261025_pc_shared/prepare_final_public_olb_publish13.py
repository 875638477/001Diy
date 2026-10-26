"""Freeze thirteen exact final OLBs/proofs/backups; public reads only."""
from pathlib import Path
import argparse,hashlib,json,zipfile
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def key(p):return str(Path(p).resolve()).casefold()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--remaining-stage',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh preparation directory required')
 sources=[]
 for row in load(M/'public_olb_stage_all13/PUBLIC_OLB_STAGING_RUN.json')['libraries']:
  if Path(row['public']).name not in {'004Diode.OLB','Dream1.OLB'}:sources.append((Path(row['case']),Path(row['review'])))
 for row in load(M/'public_olb_bare9_stage13/PUBLIC_OLB_STAGING_RUN.json')['libraries']:sources.append((Path(row['case']),Path(row['review'])))
 for stem in ['01_004Diode','02_011MCU','03_016Sensor','04_019Connector']:
  d=M/'public_olb_final7_stage13'/stem;sources.append((d/'STAGING_CASE.json',d/'review/PUBLIC_OLB_STAGE_REVIEW.json'))
 d=M/'public_olb_final7_stage13/05_COMMON_PC';sources.append((d/'STAGING_CASE.json',M/'bounded_common_identity_checker13/actual_review_v2/PUBLIC_OLB_STAGE_REVIEW.json'))
 remaining=load(a.remaining_stage/'PUBLIC_OLB_STAGING_RUN.json');need(remaining['status']=='PASS_ALL_EXACT_OLB_STAGING_NATIVE_AND_FULL_INDEPENDENT_REVIEW_NO_PUBLIC_REPLACEMENT','Remaining two libraries not fully native-staged')
 need({Path(x['public']).name for x in remaining['libraries']}=={'Dream1.OLB','2026-08-15_23-35-55.OLB'},'Remaining two library cohort differs')
 sources += [(Path(x['case']),Path(x['review'])) for x in remaining['libraries']]
 need(len(sources)==13,'Expected thirteen final candidate libraries')
 cumulative=M/'public_olb_superset46_plan13/PUBLIC_OLB_SUPERSET46_APPLY_PLAN.json';planfields=load(cumulative)['fields'];expected={(key(x['library']),x['field_path']):(x['attribute'],x['old_value'],x['proposed_value']) for x in planfields};need(len(expected)==len(planfields)==46,'Exactly forty-six unique frozen source fields required')
 guard=M/'nonpassive_exact_additions13/PUBLIC_OLD_PLUS_NEW_GUARD.json';guardrows={key(x['path']):x for x in load(guard)['files']};replacements=[];observed={};evidence={}
 def bind(path):
  p=Path(path);evidence[str(p)]={'path':str(p),'sha256':sha(p)}
 bind(cumulative)
 for casepath,reviewpath in sources:
  case,review=load(casepath),load(reviewpath);public=Path(case['public_original']);candidate=Path(case['candidate'])
  need(review['status']=='PASS_COMPLETE_ORDERED_OLB_FP_FIELDS_AND_NATIVE_ALL_FONT_FIELDS_STAGING_ONLY','Strict review not PASS '+str(reviewpath));need(review['case_sha256']==sha(casepath),'Review not exact case');need(review['candidate_sha256']==case['candidate_sha256']==sha(candidate),'Candidate SHA mismatch');need(review['public_original_unchanged_sha256']==case['original_sha256']==sha(public),'Public original SHA changed')
  need(guardrows[key(public)]['sha256']==case['original_sha256'],'Full13433 guard not exact public original')
  need(len(review['negative_controls'])==10 and all(x['status']=='PASS_REJECTED' for x in review['negative_controls']),'Ten strict negative controls required');need(review['native_fonts']['native_fields_equal']==337,'All native font/default fields required')
  backup=casepath.parent/'ORIGINAL_OLB.zip'
  with zipfile.ZipFile(backup) as z:
   names=z.namelist();need(len(names)==2 and set(names)=={public.name,'SHA256.json'},'Unexpected original ZIP contents');need(json.loads(z.read('SHA256.json'))=={public.name:case['original_sha256']},'Existing ZIP SHA manifest differs');data=z.read(public.name);need(hashlib.sha256(data).hexdigest().upper()==case['original_sha256'] and len(data)==public.stat().st_size,'Existing original ZIP roundtrip mismatch')
  for field in case['fields']:
   k=(key(field['library']),field['field_path']);need(k not in observed,'Duplicate cumulative planned field');observed[k]=(field['attribute'],field['old_value'],field['proposed_value'])
  for p in [casepath,reviewpath,backup,case['font_report'],case['original_defaults'],case['actual_defaults'],case['original_native_xml'],case['candidate_native_xml'],case['frozen_source_xml'],Path(case['apply_job'])/'job_result.json',Path(case['reopen_job'])/'job_result.json',case['original_snapshot']]:bind(p)
  r={'public':str(public),'candidate':str(candidate),'old_sha256':case['original_sha256'],'new_sha256':case['candidate_sha256'],'old_bytes':public.stat().st_size,'new_bytes':candidate.stat().st_size,'case':str(casepath),'review':str(reviewpath),'field_count':len(case['fields']),'source_complete_ordered_sha256':review['proof']['source_full_library_sha256'],'inverse_complete_ordered_sha256':review['proof']['inverse_full_library_sha256'],'all_ordered_elements':review['proof']['all_ordered_elements'],'native_font_default_fields':review['native_fonts']['native_fields_equal'],'existing_original_zip':str(backup),'existing_original_zip_sha256':sha(backup)}
  need(r['source_complete_ordered_sha256']==r['inverse_complete_ordered_sha256'],'Complete ordered XML inverse SHA differs');replacements.append(r)
 need(observed==expected,'Final thirteen candidates do not implement exactly cumulative46 fields');need(len({key(x['public']) for x in replacements})==13,'Duplicate final library target')
 for p in [M/'bounded_common_identity_checker13/COMMON_FROZEN_SOURCE_IDENTITY_EVIDENCE.json',M/'bounded_common_identity_checker13/verify_public_olb_fp_stage_bounded_identity_v2.py',M/'common59_cn4_staged_gate13/COMMON59_DESIGN_CACHE_FULL_REVIEW.json',M/'bounded_common_identity_checker13/identity_negative_controls/IDENTITY_NEGATIVE_CONTROLS.json']:bind(p)
 identity=load(M/'bounded_common_identity_checker13/identity_negative_controls/IDENTITY_NEGATIVE_CONTROLS.json');need(identity['status']=='PASS_BOUNDED_FROZEN_IDENTITY_CONTROLS_ALL_REJECTED','Bounded identity controls missing')
 bounded=load(M/'bounded_common_identity_checker13/COMMON_FROZEN_SOURCE_IDENTITY_EVIDENCE.json')
 for field in ['source_xml','opened_olb','public_original','native_job_result','owned_process','native_identity','original_reviewer']:bind(bounded[field])
 a.out.mkdir(parents=True);archive=a.out/'ORIGINAL_THIRTEEN_PUBLIC_OLBS.zip';members=[]
 with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for r in replacements:
   member=str(Path(r['public']).relative_to(Path('D:/001DIY/005lib/01captureLib'))).replace('\\','/');z.write(r['public'],member);members.append({'path':r['public'],'member':member,'sha256':r['old_sha256'],'bytes':r['old_bytes']})
 with zipfile.ZipFile(archive) as z:
  need(len(z.namelist())==13,'Final original ZIP count mismatch')
  for m in members:
   b=z.read(m['member']);need(len(b)==m['bytes'] and hashlib.sha256(b).hexdigest().upper()==m['sha256'],'Final original ZIP roundtrip mismatch')
 plan={'schema':'EXACT_PUBLIC_OLB_REPLACEMENT_PLAN_V1','status':'PREPARED_ONLY_NO_PUBLIC_REPLACEMENTS','source_guard':{'path':str(guard),'sha256':sha(guard),'files':len(guardrows)},'replacements':sorted(replacements,key=lambda r:r['public'].casefold()),'field_count':46,'backup':{'path':str(archive),'sha256':sha(archive),'members':members,'all_members_SHA_roundtrip_exact':True},'evidence':list(evidence.values()),'publisher':{'path':str(M/'publish_exact_public_olbs.py'),'sha256':sha(M/'publish_exact_public_olbs.py')},'preparer_sha256':sha(__file__),'publication_scope':'Exactly thirteen atomic OLB directory entry replacements; no CAD; no alias retirements; no PAD/PSM/DRA/BRD mutations. Actual public-path native reopen proof still required after publish.'}
 path=a.out/'EXACT_THIRTEEN_PUBLIC_OLB_REPLACEMENT_PLAN.json';path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'status':plan['status'],'plan':str(path),'plan_sha256':sha(path),'backup_sha256':sha(archive),'libraries':13,'fields':46},indent=2))
if __name__=='__main__':main()
