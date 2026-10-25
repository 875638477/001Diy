from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
for name in ['native_validation','native_final_report']:
 p=R/f'review/{name}.json';(R/f'review/{name}_attempt01.json').write_bytes(p.read_bytes())
s=(R/'scripts/validate_nativeG.py').read_text().replace("if net=='GND' else","if net==('GND',) else").replace("'No objects updated' in","'No objects were updated.' in")
(R/'scripts/validate_nativeG_v2.py').write_text(s,encoding='ascii')
