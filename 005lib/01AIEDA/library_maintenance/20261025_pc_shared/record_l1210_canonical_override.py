from pathlib import Path
import json,hashlib
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
p=json.loads((M/'global_suffix_inventory_v1/PSM_NATIVE_AUDIT_PLAN.json').read_text(encoding='utf-8'))
idx={r['stem'].lower():r for r in p['representatives']}
rows=[]
for name in ('l1210h22','l1210h22_pc'):
 x=idx[name];t=idx['l1210h22_pc'];rows.append({'stem':x['stem'],'source_sha256':x['sha256'],'canonical':'l1210h22_pc','canonical_source_sha256':t['sha256'],'reason':'Existing compatible l1210-family_pc with H22 height semantics already used in current13; root confirmed preserve it rather than create redundantl1210_pc.'})
x={'status':'CANONICAL_SELECTION_OVERRIDE_ONLY_NO_PUBLIC_MUTATION','overrides':rows,'authority':'Root confirmed existing compatible_pc canonical preference; do not change frozen941 native source plan.'}
(M/'global_suffix_canonical_overrides_v1.json').write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
print(hashlib.sha256((M/'global_suffix_canonical_overrides_v1.json').read_bytes()).hexdigest().upper())
