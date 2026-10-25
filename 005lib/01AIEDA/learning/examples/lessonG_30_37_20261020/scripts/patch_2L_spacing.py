from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
p=R/'scripts/reconcileG.il'
s=p.read_text().replace('  foreach(row list(list("V3V3"', '''  f29Must(axlCNSCreate('spacing "G2L_POWER_GND_SPACING" nil) "2L power ground spacing CSet")
  foreach(k axlCNSGetSpacing(nil nil nil)
   unless(member(k list('bbvia_gap 'hole_via 'hole_thrupin 'hole_hole 'hole_shape 'hole_line))
    f29Must(axlCNSSetSpacing("G2L_POWER_GND_SPACING" nil k "0.20 MM") "2L power ground spacing")))
  foreach(row list(list("V3V3"''')
s=s.replace('list(list("PHYSICAL_CONSTRAINT_SET" cadr(row)))','list(list("PHYSICAL_CONSTRAINT_SET" cadr(row)) list("SPACING_CONSTRAINT_SET" "G2L_POWER_GND_SPACING"))')
s=s.replace('axlCNSSetSpacing("" nil k "0.2032 MM")','axlCNSSetSpacing("" nil k "0.16 MM")')
p.write_text(s,encoding='ascii')
print('2L_WIDTH2032_SPACE160_PGSPACE200_READY')
