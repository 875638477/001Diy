from pathlib import Path
import json,hashlib,csv,re,datetime
R=Path(r'D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';A=J/'audits';N=R/'learning/notes/lessonJK_51_54_20261022.md';checks=[]
def ld(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def ck(name,ok,detail=None):checks.append(dict(id=name,passed=bool(ok),detail=detail))
reg=ld(A/'j51_54_issues.json');ids=[x['id'] for x in reg['issues']];ck('unique_stable_issue_IDs',len(ids)==len(set(ids))==54);ck('new_stack_legacy_issues_present',{'JK52_STACK_LEGACY','JK53_STACK_LEGACY'}<=set(ids))
with (A/'j51_54_issues.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
ck('CSV_and_JSON_issue_IDs_equal',[x['id'] for x in rows]==ids)
for p in sorted(A.glob('j5*.json')):
 try:ld(p);ok=True
 except Exception:ok=False
 ck('JSON_parse_'+p.name,ok)
ck('primary138_no_failure',ld(A/'j51_consistency_and_drc.json')['checkCount']==138 and not ld(A/'j51_consistency_and_drc.json')['failedChecks'])
rev=ld(A/'j54_stored_corrections_rechecked.json');ck('six_existing_native_correction_proofs',len(rev['checks'])==6 and all(x['passed']for x in rev['checks']))
ck('69net_rows_each',len(ld(A/'j51_all69_net_matrix.json')['rows'])==138)
ck('56GNDpin_each',all(sum(x['variant']==v and x['kind']=='physicalPin' for x in ld(A/'j51_all56_ground_pins_and_all_vias.json')['rows'])==56 for v in ['2L','4L']))
ck('USB14_gap_IDs',len(ld(A/'j52_USB14_gap_piece_register.json')['pieces'])==14)
ck('32_power_domains',len(ld(A/'j53_actual_power_domains.json')['domains'])==32)
ck('12_MPNs',ld(A/'j53_powerup_prerequisites_handoff.json')['realMPNCount']==12)
for m in re.finditer(r'\[[^\]]+\]\(([^)]+)\)',N.read_text(encoding='utf-8')):
 link=m.group(1)
 if link.startswith('http'):continue
 ck('note_link_'+link,(N.parent/link).resolve().exists())
# The complete frozen input set is hashed again after all our reports/notes are written.
frozen=ld(A/'j51_54_input_integrity.json');after=[]
for e in frozen['entries']:
 p=Path(e['path']);actual=hashlib.sha256(p.read_bytes()).hexdigest().upper() if p.exists() else None;after.append(dict(path=str(p),expected=e['expectedSHA256'],actual=actual,match=actual==e['expectedSHA256']))
ck('all597_frozen_originals_still_exact',len(after)==597 and all(x['match'] for x in after))
known=ld(A/'j51_54_consumed_input_files.json')['files'];ck('all_consumed_inputs_still_exact',all(Path(x['path']).exists() and hashlib.sha256(Path(x['path']).read_bytes()).hexdigest().upper()==x['sha256'] for x in known))
for v in ['2L','4L']:
 ck('risk_SVG_and_PNG_'+v,all((A/f'j54_actual_risk_map_{v}.{ext}').exists() for ext in ['svg','png']))
result=dict(status='PASS_J51_54_RECORD_AND_EVIDENCE_COMPLETENESS_NOT_BOARD_RELEASE' if all(x['passed']for x in checks) else 'REVIEW_REQUIRED',created=datetime.datetime.now().isoformat(),checkCount=len(checks),failed=[x for x in checks if not x['passed']],checks=checks,originalSHARecheck=after,newNativeExecution=False,boardAcceptance=False,new4LDefaultApplied=False,knownOpen='SevenGPIO per board, USB4 and wholeDRC, actual SI/PI/EMI/MPN/thermal/hardware; newdefault physical application belongs to separate JK derived trial.')
(A/'j51_54_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Explicit ownership list: do not seal another agent's in-progress output.
owned=list(A.glob('j51*.json'))+list(A.glob('j52*.json'))+list(A.glob('j53*.json'))+list(A.glob('j54*.json'))+list(A.glob('j51*.csv'))+list(A.glob('j54*.svg'))+list(A.glob('j54*.png'))
owned+=[J/'scripts'/x for x in ['audit_j51_54_actual.py','audit_j53_power_geometry.py','write_j51_54_issue_register.py','finalize_j51_54_note.py','seal_j51_54_records.py']]
owned+=[J/'logs/j51_54_review_script_corrections.json',N]
manifestpath=A/'j51_54_artifact_manifest.json';files=[]
for p in sorted(set(owned)):
 if p==manifestpath:continue
 files.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),bytes=p.stat().st_size))
manifest=dict(status='SEALED_J51_54_REVIEW_RECORDS_NOT_BOARD_RELEASE',created=datetime.datetime.now().isoformat(),files=files,sourceInputs=known,nativeBoardSources=ld(A/'j51_consistency_and_drc.json')['variants'],validation='j51_54_validation.json',excludes=['this manifest itself','other agents outputs','parent EDA/index/mainJK/notes','any future derived default-stack board/readback'],stage='Input b019 legacyL3GND reviewed; new4Ldefault contract delivered, actual newplane report not yet consumed')
# Avoid embedding the large full input report redundantly in the manifest.
manifest['nativeBoardSources']={v:dict(board=x['board'],sha256=x['boardSHA256'],checkpoint=x['checkpoint']) for v,x in manifest['nativeBoardSources'].items()}
manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest().upper()==x['sha256'] for x in files)
print(json.dumps(dict(validation=result['status'],checks=len(checks),failed=result['failed'],files=len(files),manifest=str(manifestpath),sha256=hashlib.sha256(manifestpath.read_bytes()).hexdigest().upper()),ensure_ascii=False))