from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
s=(R/'scripts/validate_nativeG_v3.py').read_text().replace("'outsidePhysicalNeckMM':1.0","'outsideRegionNeckLimitMM':1.0").replace("'spacingOnly4L':{'smdpin_line':.2,'line_line':.2}","'spacingOnly4L':({'smdpin_line':.2,'line_line':.2} if key=='4L' else None)")
needle="check(f'{key}.manual_TOP_segments27',len(top)==27,len(top))"
# Explicit scope checks apply after the board dictionary is built.
needle2="inputs=json.loads((R/'source/input_manifest.json').read_text())[:2]"
extra="""twonets=rows(R/'logs/final_reopen_2L_01/net_rules.tsv')
for r in twonets:
 if r['net'] not in ['V3V3','GND']:
  check(f'2L.remaining67_default_only.{r["net"]}',all(sx(r[k]) is None for k in ['physicalClass','spacingClass','electricalClass']) and all(k not in r['props'] for k in ['PHYSICAL_CONSTRAINT_SET','SPACING_CONSTRAINT_SET','ELECTRICAL_CONSTRAINT_SET']))
boards['2L']['independentRuleProfile']['remaining67Nets']='No per-net CSet override or netclass; only DEFAULT width .2032mm and copper spacing .16mm. This is incomplete full-board power/signal rule classification.'
"""
assert needle2 in s;s=s.replace(needle2,extra+needle2)
(R/'scripts/validate_nativeG_v4.py').write_text(s,encoding='ascii')
