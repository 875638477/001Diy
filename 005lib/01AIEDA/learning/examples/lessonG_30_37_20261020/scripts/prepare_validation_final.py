from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
s=(R/'scripts/validate_nativeG_v4.py').read_text()
needle="inputs=json.loads((R/'source/input_manifest.json').read_text())[:2]"
extra="""for key,attempt in [('4L','01'),('2L','02')]:
 before=R/f'logs/bulk_{key}_{attempt}';after=R/f'logs/final_reopen_{key}_01'
 check(f'{key}.reference_fill_exact_after_coupon_rollback',(before/'g_copper_shapes.tsv').read_bytes()==(after/'g_copper_shapes.tsv').read_bytes())
 def simplepaths(p):
  return sorted((x['net'],x['layer'],x['startEnd'],x['width']) for x in rows(p/'route_geometry.tsv'))
 check(f'{key}.route_geometry_exact_after_coupon_rollback',simplepaths(before)==simplepaths(after))
"""
assert needle in s;s=s.replace(needle,extra+needle)
(R/'scripts/validate_nativeG_final.py').write_text(s,encoding='ascii')
