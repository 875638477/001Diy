from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/reopen_power_2L_b001.scr';s=p.read_text()
s=s.replace('skill errset(axlDRCUpdate(t) t)','skill errset(hiChallengeNeck("'+(R/'logs/reopen_power_2L_b001').as_posix()+'" "HI_U2_SW_ESCAPE_P" 1.2 1.0) t)\nskill errset(axlDRCUpdate(t) t)')
p.write_text(s,encoding='ascii')
