"""Freeze the exact native-reviewed five formal13 replacements; no CAD/mutation."""
from pathlib import Path
import hashlib,json
M=Path(__file__).resolve().parent
R=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
proofs=[R/'verification/cache7_superset_xn4_v2/PUBLIC_LIBRARY_XML_REVIEW.json',
M/'cache7_pst1031_full12_gate13/PUBLIC_LIBRARY_PST_REVIEW.json',
M/'common59_cn4_actual_public_gate13/COMMON59_DESIGN_CACHE_FULL_REVIEW.json',
M/'main_all81_exact_vdd_connectivity27/ALL81_EXACT_VDD_REPAIR_TYPED_CONNECTIVITY_REVIEW.json',
M/'main_all81_final_cfx26/PUBLIC_LIBRARY_CFX_REVIEW.json',
R/'w/pcb_migration/FINAL59_CACHE_FULL15_CONTEXT_REVIEW_V2.json',
M/'final59_official_name_export_review27/PACKAGE_EXPORT_NAME_VERIFICATION.json']
sources=[(R/'w/cache7_cn4_v2/LGA1700.DSN',R/'sch/LGA1700.DSN','E421141B8B9DF969E8C654E86FEF6D2B2E06E5C5B8CF82C1DC03C7AC1767D374'),
(R/'w/all81_attached14/ALL81_ATTACHED.brd',R/'pcb/LGA1700_RULES.brd','49B874ED98BD3F66EC23D115848C88E2F744195DEE9B35DC98F143674E055308')]
for n,h in [('pstchip.dat','EC6C3CD7011C347AF27AF4FAE7C372F602F597A6A32CF5FFEA37A3FF66B7DE61'),('pstxprt.dat','DF97A9507DAB1EE7388F9D7119DFC0C9C96AFFCF6572670AF8E83D57BFAC86A1'),('pstxnet.dat','5B1F07D58AFFD6C7A6EB5BE50EA512B195F03083E0F127BA8361F83DD9AFF1FB')]:
    sources.append((R/'w/cache7_pst4/20261025_231655_178b29bf/netlist'/n,R/'sch/netlist'/n,h))
rows=[]
for s,t,h in sources:
    assert sha(s)==h,(s,sha(s),h)
    rows.append(dict(source=str(s),target=str(t),old_sha256=sha(t) if t.is_file() else None,new_sha256=h))
f=jr(R/'verification/SOURCE_FREEZE.json')
protected=[]
for p,h in [('schematic_source','schematic_sha256'),('pcb_source','pcb_sha256'),('formal12_board','formal12_board_sha256'),('source_common_olb','source_common_sha256')]:
    assert sha(f[p])==f[h]
    protected.append(dict(path=f[p],sha256=f[h]))
evidence=[]
for p in proofs:
    q=jr(p);assert q['status'].startswith('PASS'),(p,q['status'])
    evidence.append(dict(path=str(p),sha256=sha(p),required_status=q['status']))
out=M/'final13_five_publication_plan27'
out.mkdir(exist_ok=False)
p=out/'EXACT_FIVE_FORMAL13_PUBLICATION_PLAN.json'
p.write_text(json.dumps(dict(schema='FINAL13_EXACT_FIVE_DESIGN_FILES_NATIVE_PUBLISH_PLAN_V1',publisher_sha256=sha(M/'publish_verified_project13.py'),files=rows,native_proofs=evidence,protected_originals=protected),indent=2),encoding='utf-8')
print(json.dumps(dict(plan=str(p),sha256=sha(p),files=5,proofs=len(evidence))))
