"""Keep the strict margin FAIL while publishing complete finite evidence."""
from pathlib import Path
import hashlib,ast
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'review_native_material_ledger13_v9.py').read_text(encoding='utf-8')
old=";assert counts['CROSS_NET_INTERSECTIONS_INCLUDING_0D01MIL_MARGIN']==len(cross)==0,'Cross-net contact cannot be accepted'"
assert old in s
s=s.replace(old,";assert counts['CROSS_NET_INTERSECTIONS_INCLUDING_0D01MIL_MARGIN']==len(cross),'Native cross counts must agree'")
old=" assert all(int(x['direct_intersections'])==int(x['margin_intersections'])==0 for x in checks)"
assert old in s
s=s.replace(old,""" direct_count=sum(int(x['direct_intersections']) for x in checks)
 margin_count=sum(int(x['margin_intersections']) for x in checks)
 assert direct_count+margin_count==len(cross)
 assert direct_count==0,'Actual copper intersects another net; cannot accept'
 assert all(x['side']=='ADDITION_PLUS_0D01MIL_INTERSECTS_OTHER_NET' for x in cross), 'Unexpected actual cross-net hit geometry'
 contact_checks=[dict(method=x['method'],input_native_area=x['input_native_area'],input_bbox=x['input_bbox'],**y) for x,y in zip(methods,checks) if int(y['direct_intersections']) or int(y['margin_intersections'])]""")
s=s.replace("status='PASS_BOUNDED_NATIVE_DYNAMIC_COPPER_REGENERATION_NO_NEW_CROSS_NET_CONTACT'", "status='REVIEW_REQUIRED_CONSERVATIVE_MARGIN_INTERSECTIONS' if margin_count else 'PASS_BOUNDED_NATIVE_DYNAMIC_COPPER_REGENERATION_NO_NEW_CROSS_NET_CONTACT'")
s=s.replace("new_other_net_contact_count=0,", "actual_other_net_polygon_intersection_count=direct_count,conservative_margin_polygon_intersection_count=margin_count,strict_margin_gate='FAIL' if margin_count else 'PASS',publication_gate='HOLD' if margin_count else 'READY_FOR_OTHER_GATES',nonzero_contact_checks=contact_checks,")
s=s.replace("scope='Explicitly accepts the documented finite native regenerated copper differences, not total copper equality.", "scope='Complete finite native regenerated-copper evidence. A nonzero conservative guard intersection retains strict margin FAIL and publication HOLD; actual original fragments are checked independently. This report does not claim total copper equality.")
s=s.replace('.read_text()', ".read_text(encoding='utf-8-sig')")
ast.parse(s)
out=W/'review_native_material_diagnostic13_v11.py';assert not out.exists();out.write_text(s,encoding='utf-8');print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
