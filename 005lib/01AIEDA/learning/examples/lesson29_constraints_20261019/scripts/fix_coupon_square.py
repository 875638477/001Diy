import pathlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
s=(R/'scripts/coupon29.il').read_text().replace("?figure 'RECTANGLE ?figureSize 0.2:0.2","?figure 'SQUARE ?figureSize 0.2:0.2")
(R/'scripts/coupon29_v2.il').write_text(s,encoding='ascii')
for k in ['package','board']:
 s=(R/f'scripts/coupon_{k}01.scr').read_text().replace('/coupon29.il','/coupon29_v2.il')
 (R/f'scripts/coupon_{k}02.scr').write_text(s,encoding='ascii')
