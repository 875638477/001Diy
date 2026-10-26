"""Include explicit native zero-difference rows for all eleven contour keys."""
from pathlib import Path
import ast,hashlib
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
s=(W/'review_native_material_ledger13_v3.py').read_text(encoding='utf-8')
old=" summary=collections.defaultdict(lambda:collections.defaultdict(list))\n for r in rows:summary[r['key']][r['side']].append(r['poly'])"
new=""" summary=collections.defaultdict(lambda:collections.defaultdict(list))
 for r in shape_summary:
  summary[r['key']]['ACTUAL_SHAPE_COPPER_REMOVED']=[]
  summary[r['key']]['ACTUAL_SHAPE_COPPER_ADDED']=[]
 for r in rows:summary[r['key']][r['side']].append(r['poly'])"""
assert old in s
s=s.replace(old,new)
ast.parse(s)
out=W/'review_native_material_ledger13_v4.py'
assert not out.exists()
out.write_text(s,encoding='utf-8')
print(out)
print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
