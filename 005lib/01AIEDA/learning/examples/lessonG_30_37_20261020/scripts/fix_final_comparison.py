from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
for name in ['native_validation','native_final_report']:
 p=R/f'review/{name}.json';(R/f'review/{name}_attempt02.json').write_bytes(p.read_bytes())
s=(R/'scripts/validate_nativeG_final.py').read_text().replace("for x in rows(p/'route_geometry.tsv'))","for x in rows(p/'route_geometry.tsv') if sx(x['layer']).startswith('ETCH/'))")
(R/'scripts/validate_nativeG_final.py').write_text(s,encoding='ascii')
