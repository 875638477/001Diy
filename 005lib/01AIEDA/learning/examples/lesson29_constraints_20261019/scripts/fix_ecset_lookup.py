import pathlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
s=(R/'scripts/challenges29_v2.il').read_text()
s=s.replace('axlNetEcsetValueGet("USB_DP"','axlNetEcsetValueGet(axlDBFindByName(\'net "USB_DP")')
s=s.replace('list("MIN_LINE_WIDTH" "0.20 MM" "MIN_NECK_WIDTH" "0.20 MM")','list(list("MIN_LINE_WIDTH" "0.20 MM"))')
(R/'scripts/challenges29_v3.il').write_text(s,encoding='ascii')
s=(R/'scripts/challenge02.scr').read_text().replace('scripts/challenges29_v2.il','scripts/challenges29_v3.il').replace('logs/challenge02','logs/challenge03')
(R/'scripts/challenge03.scr').write_text(s,encoding='ascii')
