from pathlib import Path
import json,hashlib
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
x=json.loads((M/'global_suffix_intent_overrides_v2.json').read_text(encoding='utf-8'))
x['supersedes']='global_suffix_intent_overrides_v2.json (zero-drill SMD variants are ordinarySMT without functional TH or corruption inference)'
x['overrides']=[r for r in x['overrides'] if r['anomaly_kind']=='PAD_NAME_COLLISION']
x['classification_correction']='c0402_fcs/c0805big/r0402_fcs have actualisThrough=nil and0drill; holeTypecircle_drill alone does not establish a hole. They remain ordinarySMT with legacyusage metadata retained in raw evidence/deltas.'
p=M/'global_suffix_intent_overrides_v3.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8');print(hashlib.sha256(p.read_bytes()).hexdigest().upper())
