import pathlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
s=(R/'scripts/challenges29.il').read_text().replace('dr=make_axlPadStackPad(?usage','dr=make_axlPadStackDrill(?usage')
(R/'scripts/challenges29_v2.il').write_text(s,encoding='ascii')
s=(R/'scripts/challenge01.scr').read_text().replace('scripts/challenges29.il','scripts/challenges29_v2.il').replace('logs/challenge01','logs/challenge02')
(R/'scripts/challenge02.scr').write_text(s,encoding='ascii')
print('Use official dbcreate/pad.il drill constructor; docs API paragraph confused Pad vs Drill.')
