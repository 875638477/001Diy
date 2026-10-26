"""Freeze exact four native-reviewed public BRDs; no CAD/public mutations."""
from pathlib import Path
import argparse,hashlib,json
M=Path(__file__).resolve().parent
PUBLIC=Path('D:/001DIY/005lib/01brdlib')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def proof(p):
    q=jr(p);assert q['status'].startswith('PASS'),(p,q['status'])
    return dict(path=str(p),sha256=sha(p),required_status=q['status'])
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--all79-proof',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    guard=M/'public_olb_final13_published13/PUBLIC_GUARD_AFTER_EXACT13_OLB.json'
    assert sha(guard)=='F9D19CC95DCEA9686967EF7CF954EE7E6858225E7F9C949A203C340E6A153D88'
    originals={Path(r['path']).name:r for r in jr(guard)['files'] if Path(r['path']).parent==PUBLIC}
    index=M/'public_three_module_final_acceptance25/FINAL_THREE_MODULE_NATIVE_ACCEPTANCE.json'
    q=jr(index);assert q['status']=='PASS_THREE_FINAL_MODULES_ALL_SCOPED_NATIVE_GATES'
    rows=[]
    for r in q['rows']:
        c=Path(r['final_candidate']);assert sha(c)==r['final_candidate_sha256']
        p=PUBLIC/(r['board']+'.brd');assert sha(p)==originals[p.name]['sha256']
        es=[proof(index)]+[proof(Path(e['path'])) for e in r['proofs'].values()]
        rows.append(dict(public=str(p),candidate=str(c),old_sha256=sha(p),new_sha256=sha(c),new_bytes=c.stat().st_size,native_proofs=es))
    candidate=M/'public0010_original_thermal_restore_run13_v5_pending/PUB0010_ORIGINAL_THERMAL_UNAPPROVED.brd'
    assert sha(candidate)=='07A0F9340CBC89718BD586DEFCC270E299E24242C6AA7A6FA78973C220E82A42'
    proofpaths=[M/'public0010_final2698_partition_gate13_v4/FULL2698_ACTUAL_CONNECTION_PARTITION_REVIEW.json',
    M/'public0010_final_all70_cache_gate13_v2/ALL70_ACTUAL_CACHE_FULLGRAPH_CONTEXT_REVIEW.json',
    M/'public0010_final593_fresh_gate13_v1/FINAL_FULL593_SOURCE_FRESH_REVIEW.json',
    M/'public0010_final_actual_body_gate13_v5/PUBLIC_MODULE_ACTUAL_NATIVE_DEVICE_BODY_REVIEW.json',
    M/'public0010_final4views_gate13_v4/PUBLIC_MODULE_MAPPED_COMPLETE_VIEWS_REVIEW.json',
    M/'public0010_final_bounded_cfx_gate13_v6/PUBLIC0010_COMPLETE_CFX_REVIEW.json',
    M/'public0010_original_thermal_restore_run13_v5_pending/FINITE_ORIGINAL21_THERMAL_CU_REVIEW_V5.json',
    M/'public0010_original_thermal_restore_run13_v5_pending/RAW_CACHE_STRICT_ID_BIJECTION_REVIEW.json',
    M/'public0010_final_private_gates_index13_v1/PUBLIC0010_FINAL_PRIVATE_EXECUTED_PROOFS_INDEX.json',
    M/'w/module0010_final_full28/FRESH79_TYPED_BIJECTION_NEGATIVE_CONTROLS.json',a.all79_proof]
    p=PUBLIC/'0010.brd';assert sha(p)==originals[p.name]['sha256']
    rows.append(dict(public=str(p),candidate=str(candidate),old_sha256=sha(p),new_sha256=sha(candidate),new_bytes=candidate.stat().st_size,native_proofs=[proof(p) for p in proofpaths]))
    assert len(rows)==4 and {Path(r['public']).name for r in rows}=={'00012.brd','0010.brd','006.brd','008.brd'}
    backup=M/'original_public_four_brd_backup13/BACKUP_RECEIPT.json'
    plan=dict(schema='EXACT_FOUR_PUBLIC_BRD_NATIVE_PUBLISH_PLAN_V1',publisher_sha256=sha(M/'publish_exact_four_public_brds13.py'),guard=str(guard),backup_receipt=str(backup),backup_receipt_sha256=sha(backup),replacements=sorted(rows,key=lambda r:r['public']))
    assert not a.out.exists() and a.out.resolve().is_relative_to(M.resolve());a.out.mkdir(parents=True)
    dest=a.out/'EXACT_FOUR_PUBLIC_BRD_NATIVE_PUBLISH_PLAN.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf-8')
    print(json.dumps(dict(plan=str(dest),sha256=sha(dest),rows=4)))
if __name__=='__main__':main()
