"""Finish only read-only validation/receipt after all3069 journalled unlinks.
Never calls plan_assets/apply, never unlinks or modifies a public entry.
"""
from pathlib import Path
import copy,hashlib,importlib.util,json,os
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
W=M/'public_retirement_all_confirmed_stage13_v2'
JOURNAL_SHA='8FA12693BA28254F7FACC9A345515B6301DC25B435F553F7DFD70A248FF3C796'
GUARD_SHA='C2835B5651C473873A8664AC68520E32795B3D09E8BBF0134AE5BA13BA6DBBEC'
CLOSURE_SHA='8EA5E5694F18B663FE2D32B30FCB6128F8C7FD8A6F6465F818FA91F9BBABCDEC'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def art(p):return {'path':str(Path(p)),'sha256':sha(p)}
def norm(p):return str(Path(p).resolve()).casefold()
def need(v,s):
 if not v:raise ValueError(s)
def main():
 need(not (W/'APPLY_RECEIPT.json').exists(),'Actual final receipt already exists; never overwrite')
 stopfile=M/'OWNED_RETIREMENT_READONLY_POSTCHECK_STOP28.json';stopped=load(stopfile);need(stopped['status']=='STOP_ONLY_OWNED_POST_DELETE_READONLY_QUADRATIC_VALIDATION' and stopped['pid']==34752 and stopped['journal_lines']==3070 and stopped['journal_sha256']==JOURNAL_SHA,'Owned interrupted postcheck not frozen')
 jp=W/'APPLY_EXACT_FILES.jsonl';need(sha(jp)==JOURNAL_SHA,'Frozen completed unlink journal changed');lines=jp.read_text(encoding='utf-8-sig').splitlines();need(len(lines)==3070,'Not exactly START+3069 journal rows');rows=[json.loads(s) for s in lines];start=rows[0]
 need(start['status']=='APPLY_STARTED_AFTER_EXACT_NATIVE_CLOSURE' and start['assets']==3069 and start['mode']=='apply','Wrong original apply START')
 pp=Path(start['plan']);gp=Path(start['guard']['path']);cp=Path(start['closure']['path']);plan=load(pp);guard=load(gp)
 need(sha(pp)==start['plan_sha256'] and sha(gp)==start['guard']['sha256']==GUARD_SHA and sha(cp)==start['closure']['sha256']==CLOSURE_SHA,'Original plan/guard/closure changed')
 need(plan['schema']=='EXACT_PUBLIC_FOOTPRINT_RETIREMENT_PLAN_V1' and plan['asset_count']==len(plan['assets'])==3069 and plan['accepted_alias_count']==1067,'Wrong retirement cohort')
 # Resolve each removal key once, not inside the13433-entry expected loop.
 assets={norm(r['path']):r for r in plan['assets']};before={norm(r['path']):r for r in guard['files']};need(len(assets)==3069 and len(before)==13433 and set(assets)<=set(before),'Exact frozen source sets differ')
 seen=set()
 for row in rows[1:]:
  key=norm(row['path']);need(key in assets and key not in seen,'Extra or duplicate unlink journal record');a=assets[key];need(row=={'path':a['path'],'sha256':a['sha256'],'bytes':a['bytes'],'removed_exact_entry':True},'Journal unlink payload differs');need(before[key]['sha256']==a['sha256'] and before[key]['bytes']==a['bytes'],'Journal asset not exact frozen guard');need(not Path(a['path']).exists(),'Journalled retirement entry remains');seen.add(key)
 need(seen==set(assets),'Unlink journal does not biject all3069 planned entries')
 spec=importlib.util.spec_from_file_location('retirement_readonly_postcheck_original',M/'retire_exact_public_assets_v2.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
 expected={k:r for k,r in before.items() if k not in assets};actual=V.actual_files();need(len(expected)==len(actual)==10364 and set(expected)==set(actual),'Unexpected remaining six-root file set')
 for key,r in expected.items():need(actual[key].stat().st_size==r['bytes'] and sha(actual[key])==r['sha256'],'Unretired public entry changed '+str(actual[key]))
 # All1065 source/native/PAD evidence paths are outside the retirement set.
 cl=load(cp);need(not {norm(e['path']) for e in cl['native_evidence']} & set(assets),'Retired historical evidence would require explicit archive-member binding')
 closure=V.closure(cp,pp,plan)
 stage=load(W/'BACKUP_STAGE.json');need(stage['status']=='PASS_ALL_MEMBERS_ZIP_SHA_ROUNDTRIP_PUBLIC_UNCHANGED' and stage['plan_sha256']==sha(pp),'Exact original backup stage changed')
 backup=V.backup_bundle_verify(stage['backup_bundle'],plan['assets']);need(backup==start['backup'],'All original backup members/coverage differ')
 need(sha(jp)==JOURNAL_SHA,'Completed unlink journal changed during validation')
 report={'status':'PASS_READONLY_RESUMED_POSTCHECK_COMPLETE_JOURNAL_BIJECTION_AND_ALL10364_SURVIVORS','owned_stop_record':art(stopfile),'completed_unlink_journal':art(jp),'exact_journal_lines':3070,'exact_removed_asset_bijection':3069,'all_removal_entries_absent':True,'remaining_six_root_files_SHA_and_size_exact':10364,'post_delete_native_evidence_unchanged':closure,'full_original_backup_bundle_roundtrip':backup,'public_files_written':0,'public_files_removed':0,'no_apply_or_plan_assets_called':True,'script_sha256':sha(__file__)}
 rp=W/'READONLY_RESUMED_POSTCHECK.json';V.atomic_json(rp,report)
 receipt=copy.deepcopy(start);receipt.update(status='PASS_EXACT_RETIRED_ENTRIES_BACKED_UP_OTHER_PUBLIC_BYTES_UNCHANGED',public_files_removed=3069,remaining_public_files=10364,closure=closure,backup=backup,resumed_readonly_postcheck=art(rp));V.atomic_json(W/'APPLY_RECEIPT.json',receipt)
 print(json.dumps({'status':receipt['status'],'apply_receipt':art(W/'APPLY_RECEIPT.json'),'resumed_readonly_postcheck':art(rp),'public_files_removed_by_this_resume':0}))
if __name__=='__main__':main()
